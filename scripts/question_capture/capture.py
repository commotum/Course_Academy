#!/usr/bin/env python3
"""Capture lessons, reviews, multisteps, required assessments and quiz retakes; import content only."""
import argparse
import contextlib
import fcntl
import json
import logging
import os
import random
import shutil
import signal
import sys
import time
import threading
import traceback
import uuid
from pathlib import Path

from core import ROOT, Pacer, atomic_json, choose_activity, journal
from database import Database
from retry_policy import apply_policy, update_policy


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['run','login','priorities','import-saved'])
    parser.add_argument('--database',default=os.environ.get('EDB_DATABASE','course-academy-v2'))
    parser.add_argument('--endpoint',default=os.environ.get('EDB_ENDPOINT','/tmp/course-academy-edb-v2/writer.sock'))
    parser.add_argument('--edb-bin',default=os.environ.get('EDB_BIN','/home/jake/Developer/EDB/target/release/edb'))
    parser.add_argument('--learner-id',type=uuid.UUID,default=uuid.UUID('59d5cf13-351c-4114-be19-4c3bb64ee051'))
    parser.add_argument('--output',type=Path,default=ROOT/'reference/mathacademy/question-capture')
    parser.add_argument('--state-dir',type=Path,default=ROOT/'.local/question_capture')
    parser.add_argument('--profile',type=Path,help='Dedicated Playwright profile; defaults to STATE_DIR/browser-profile')
    parser.add_argument('--content',type=Path,help='Saved content.json for import-saved')
    parser.add_argument('--resume',type=Path,help='Select a saved run, including a deferred failure; otherwise a single non-deferred unfinished run resumes automatically')
    parser.add_argument('--limit',type=int,default=1,help='Maximum attempted activities (lessons, reviews, multisteps, required assessments or quiz retakes); default 1')
    parser.add_argument('--preview',action='store_true',help='Preview EDB writes. With run, MA answers are still submitted.')
    parser.add_argument('--dry-run',action='store_true',help='With run: inspect queue and priorities without starting an activity')
    parser.add_argument('--headless',action='store_true',help='Default is a visible Chromium window')
    parser.add_argument('--browser-spec',help='Optional existing browser cookie source, using the original MA cookiekit syntax')
    parser.add_argument('--ma-root',type=Path,default=Path('/home/jake/Developer/MA'))
    parser.add_argument('--cwcwc-weight',type=float,default=0.7)
    parser.add_argument('--review-question-limit',type=int,default=20,
                        help='Stop a review before submitting more than this many questions')
    parser.add_argument('--seed',type=int,help='Optional reproducible sequence/pacing seed')
    parser.add_argument('--timeout-ms',type=int,default=45000)
    parser.add_argument('--settle-ms',type=int,default=1000)
    parser.add_argument('--progress-course-id', dest='progress_course_ids', action='append', type=int,
                        help='Course progress to snapshot after each completed activity; repeat to override defaults 113,111,136')
    parser.add_argument('--solver-command',help='Command receiving JSON on stdin and returning solver JSON on stdout; no shell')
    parser.add_argument('--codex-bin',default='codex')
    parser.add_argument('--solver-model',help='Optional explicit Codex model for the solver')
    parser.add_argument('--solver-timeout',type=int,default=300)
    parser.add_argument('--assessment-correct-weight',type=float,default=0.8717,
                        help='Independent probability of a correct quiz question; default 0.8717')
    parser.add_argument('--assessment-time-min',type=float,default=0.7,
                        help='Minimum fraction of a quiz time limit targeted by pacing; default 0.7')
    parser.add_argument('--assessment-time-max',type=float,default=0.85,
                        help='Maximum fraction of a quiz time limit targeted by pacing; default 0.85; set both to 0 to disable')
    for kind, low, high in [('event',0.8,2.5),('answer',5.0,12.0),('lesson',10.0,25.0),('rest',120.0,360.0)]:
        parser.add_argument('--'+kind+'-min',type=float,default=low)
        parser.add_argument('--'+kind+'-max',type=float,default=high)
    parser.add_argument('--rest-every',type=int,default=20)
    args = parser.parse_args(argv)
    if args.progress_course_ids is None:
        args.progress_course_ids = [113, 111, 136]
    if any(c < 1 for c in args.progress_course_ids) or len(set(args.progress_course_ids)) != len(args.progress_course_ids):
        parser.error('Progress course IDs must be positive and unique')
    import math
    for kind in ('event','answer','lesson','rest'):
        lo, hi = getattr(args,kind+'_min'),getattr(args,kind+'_max')
        if not math.isfinite(lo) or not math.isfinite(hi) or lo<0 or hi<lo:
            parser.error('Invalid '+kind+' wait range')
    if not math.isfinite(args.cwcwc_weight) or not 0<=args.cwcwc_weight<=1:
        parser.error('--cwcwc-weight must be in [0,1]')
    if not math.isfinite(args.assessment_correct_weight) or not 0<=args.assessment_correct_weight<=1:
        parser.error('--assessment-correct-weight must be in [0,1]')
    if (not math.isfinite(args.assessment_time_min) or not math.isfinite(args.assessment_time_max) or
            not 0<=args.assessment_time_min<=args.assessment_time_max<=0.95):
        parser.error('Assessment time fractions must satisfy 0 <= min <= max <= 0.95')
    if args.limit<1 or args.review_question_limit<1 or args.rest_every<0 or args.timeout_ms<1 or args.solver_timeout<1 or args.settle_ms<0:
        parser.error('Invalid limit, timeout, or rest frequency')
    if args.command=='import-saved' and not args.content:
        parser.error('import-saved requires --content')
    if args.resume and (args.command!='run' or args.dry_run):
        parser.error('--resume requires run without --dry-run')
    args.profile = (args.profile or args.state_dir/'browser-profile').resolve()
    return args


@contextlib.contextmanager
def locked(directory):
    directory.mkdir(parents=True,exist_ok=True)
    os.chmod(directory,0o700)
    with (directory/'capture.lock').open('a') as handle:
        try:
            fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError('Another question capture is already running') from exc
        yield


def import_cookies(args, context):
    if not args.browser_spec:
        return
    kit = args.ma_root/'PIPELINE/Math-Academy/0-Ingest/1-Course-Source/dl/cookiekit/src'
    sys.path.insert(0,str(kit))
    from cookiekit import load_browser_cookies, parse_browser_spec
    imported = []
    for cookie in load_browser_cookies(parse_browser_spec(args.browser_spec)):
        domain = (cookie.domain or '').lstrip('.').lower()
        if domain!='mathacademy.com' and not domain.endswith('.mathacademy.com'):
            continue
        record = {'name':cookie.name,'value':cookie.value or '', 'domain':cookie.domain,
                  'path':cookie.path or '/', 'secure':bool(cookie.secure),
                  'httpOnly':bool(getattr(cookie,'_rest',{}).get('HttpOnly'))}
        if cookie.expires is not None:
            record['expires'] = float(cookie.expires)
        imported.append(record)
    if not imported:
        raise RuntimeError('No Math Academy cookies found in the specified browser')
    context.add_cookies(imported)
    logging.info('Imported Math Academy session cookies; cookie values are never logged')


def unfinished_run(args):
    """Recover captures and incomplete imports before consuming another live task."""
    if args.resume:
        return args.resume.resolve()
    candidates = []
    for source in sorted(args.output.glob('*/state.json')):
        state = json.loads(source.read_text())
        directory = source.parent.resolve()
        verification = directory/'edb-import/verification.json'
        receipt = json.loads(verification.read_text()) if verification.exists() else {}
        finished = state.get('import_complete') or receipt.get('committed') or receipt.get('already_complete')
        if args.preview:
            finished = finished or state.get('preview_complete')
        if not finished and not state.get('deferred_error'):
            candidates.append(directory)
    if len(candidates) > 1:
        logging.warning('Multiple unfinished captures are left for explicit --resume: %s',
                        ', '.join(map(str,candidates)))
        return None
    return candidates[0] if candidates else None


def previous_activity_snapshot(args):
    sources = list(args.output.glob('*/knowledge-state/*-completed.json'))
    if not sources:
        return None
    return str(max(sources,key=lambda p:json.loads(p.read_text())['finished_at']).resolve())


def read_journal(path):
    if not path.exists():
        return []
    source = path.read_text()
    lines = source.splitlines(keepends=True)
    entries, complete = [], ''
    for number, line in enumerate(lines):
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            if number != len(lines)-1:
                raise
            # Preserve a torn final append, then restore a valid append boundary.
            path.with_suffix('.interrupted-tail.txt').write_text(line)
            logging.warning('Recovered interrupted final journal entry in %s',path)
            path.write_text(complete)
            break
        complete += line
    else:
        if source and not source.endswith('\n'):
            path.write_text(source+'\n')
    return entries


def observe_queue(args, db, browser, completed, captured_tasks, after_task_id=None, directory=None):
    queue = browser.queue()
    retry_policy = update_policy(args.state_dir,getattr(browser,'completed_outcomes',()))
    priorities = db.priorities(args.learner_id,args.state_dir/'selection',
                              topic_ids=[i['topic_id'] for i in queue if i['task_type'] in ('lesson','review') and i['topic_id'] is not None],
                              knowledge_snapshot=previous_activity_snapshot(args))
    retry_topics = {int(key.split(':')[1]) for key in retry_policy['pending'] if key.startswith('lesson:')}
    selected = apply_policy(choose_activity(queue, priorities,set(completed)-retry_topics,captured_tasks),retry_policy)
    observation = {'queue':queue, 'selected':selected,'completed_outcomes':getattr(browser,'completed_outcomes',[]),
                   'perfect_retakes_pending':retry_policy['pending'],
                   'unranked_topics':[i['topic_id'] for i in queue
                                      if i['task_type'] in ('lesson','review') and i['topic_id'] not in priorities],
                   'after_task_id':after_task_id,
                   'priority_scores':{i['topic_id']:priorities[i['topic_id']] for i in queue
                                      if i['task_type'] in ('lesson','review') and i['topic_id'] in priorities}}
    atomic_json(args.state_dir/'selection/queue.json', observation)
    if directory is not None:
        atomic_json(directory/'queue-after.json', observation)
    journal(args.state_dir/'journal.jsonl', 'queue_observed', **observation)
    logging.info('Available queue%s: %d activities',
                 ' after task ' + str(after_task_id) if after_task_id is not None else '', len(queue))
    for position, item in enumerate(queue, 1):
        priority = priorities.get(item['topic_id']) if item['task_type'] in ('lesson','review') else None
        logging.info('  %d. %s %s (task %s, topic %s%s)%s', position, item['task_type'],
                     item['title'], item['task_id'], item['topic_id'],
                     ', priority ' + str(priority) if priority is not None else '',
                     ' [in progress; explicit resume]' if item.get('in_progress') else
                     ' [recorded; capture unsupported]' if not item.get('capture_supported',True) else '')
        if item['task_type'] == 'assessment':
            logging.info('     Assessment: %s; optional XP remaining: %s; notice: %s',
                         'retake' if item.get('assessment_is_retake') else item.get('assessment_requirement','unknown'),item.get('optional_xp_remaining'),
                         item.get('assessment_notice'))
    return observation


def record_failure(args, browser, state, directory, phase, error):
    """Preserve the failing state and visible page without interacting with it."""
    import hashlib
    target = (directory or args.state_dir)/'diagnostics'/str(time.time_ns())
    target.mkdir(parents=True,exist_ok=True)
    os.chmod(target,0o700)
    report = {'phase':phase, 'task_id':(state or {}).get('task_id'),
              'exception_type':type(error).__name__, 'message':str(error),
              'traceback':''.join(traceback.format_exception(type(error),error,error.__traceback__)),
              'configuration':{k:getattr(args,k,None) for k in
                               ('limit','preview','timeout_ms','solver_timeout','solver_model','seed')},
              'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in Path(__file__).parent.iterdir() if p.suffix in ('.py','.js')},
              'artifact_errors':[]}
    for name in ('stdout','stderr'):
        value = getattr(error,name,None)
        if isinstance(value,bytes): value = value.decode(errors='replace')
        if isinstance(value,str): report[name] = value
    # Write the original failure before attempting optional browser artifacts.
    atomic_json(target/'error.json',report)
    artifacts = []
    if state is not None:
        artifacts.append(('state.json',lambda:atomic_json(target/'state.json',state)))
    queue = args.state_dir/'selection/queue.json'
    if queue.exists():
        artifacts.append(('queue.json',lambda:shutil.copy2(queue,target/'queue.json')))
    if browser is not None:
        page = browser.page
        report['http_block'] = getattr(browser,'http_block',None)
        artifacts += [('page-url',lambda:report.update(page_url=str(page.url))),
                      ('browser-events.json',lambda:atomic_json(target/'browser-events.json',
                          list(getattr(browser,'diagnostic_events',[])))),
                      ('page.html',lambda:(target/'page.html').write_text(page.content())),
                      ('page.png',lambda:page.screenshot(path=str(target/'page.png'),timeout=5000)),
                      ('current-step',lambda:report.update(current_step=browser.current_step()))]
        def save_scope():
            from browser import by_id, EXTRACT
            current = report.get('current_step')
            if current:
                scope = by_id(page,current.replace('stepButton-','step-'))
                atomic_json(target/'current-question.json',scope.evaluate(EXTRACT))
        artifacts.append(('current-question.json',save_scope))
    for name, save_artifact in artifacts:
        try:
            save_artifact()
        except Exception as artifact_error:
            report['artifact_errors'].append({'artifact':name,'error':str(artifact_error)})
    atomic_json(target/'error.json',report)
    return target


def run(args):
    if args.command=='import-saved':
        content = json.loads(args.content.read_text())
        print(json.dumps(Database(args).import_content(content,args.content.parent/'edb-import',not args.preview),indent=2))
        return
    db = Database(args)
    if args.command=='priorities':
        priorities = db.priorities(args.learner_id,args.state_dir/'selection')
        print(json.dumps(sorted(priorities.items(),key=lambda p:p[1],reverse=True),indent=2))
        return
    resume_directory = unfinished_run(args) if args.command=='run' else None
    if resume_directory and args.dry_run:
        state = json.loads((resume_directory/'state.json').read_text())
        print(json.dumps({'resume_directory':str(resume_directory),'task_id':state['task_id'],
                          'task_type':state.get('task_type','lesson'),
                          'captured_questions':len(state.get('questions',{}))},indent=2))
        return
    from playwright.sync_api import sync_playwright
    from browser import AccessBlocked, CaptureBrowser, LEARN, repair_math_editor_document
    from solver import Solver
    rng = random.Random(args.seed)
    pacer = Pacer(args,rng)
    args.profile.mkdir(parents=True,exist_ok=True)
    os.chmod(args.profile,0o700)
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(str(args.profile),headless=args.headless if args.command!='login' else False)
        try:
            import_cookies(args,context)
            page = context.pages[0] if context.pages else context.new_page()
            context.route('https://mathacademy.com/**',repair_math_editor_document)
            browser = CaptureBrowser(page,args,pacer,Solver(args))
            if args.command=='login':
                page.goto(LEARN,wait_until='domcontentloaded')
                input('Sign in to Math Academy in this window, then press Enter here: ')
                browser.check()
                logging.info('Session retained in the dedicated private profile')
                return
            completed = set()
            captured_tasks = set()
            log = args.state_dir/'journal.jsonl'
            for entry in read_journal(log):
                if entry['event'] in ('lesson_captured','activity_captured'):
                    captured_tasks.add(entry['task_id'])
                    if entry.get('task_type','lesson') == 'lesson':
                        completed.add(entry['topic_id'])
            deferred = []
            for source in args.output.glob('*/state.json'):
                saved = json.loads(source.read_text())
                captured_tasks.add(saved['task_id'])
                if saved.get('deferred_error'):
                    deferred.append(saved['task_id'])
            if deferred:
                logging.info('Skipping deferred activities until explicit --resume: %s',deferred)
            queue_observation = None
            for n in range(args.limit):
                pacer.check_stop()
                directory, state, phase = None, None, 'queue'
                try:
                    if resume_directory and n==0:
                        directory = resume_directory
                        logging.info('Resuming saved activity %s',directory)
                        state = json.loads((directory/'state.json').read_text())
                        state.setdefault('task_type', 'lesson')
                        state.setdefault('previous_activity_snapshot',previous_activity_snapshot(args))
                        phase = 'topic'
                        topic = db.topic if state['task_type'] in ('assessment','multistep') else db.topic(state['topic_id'],directory/'selection')
                        if not state.get('activity_complete') and not state.get(state['task_type'] + '_complete'):
                            phase = 'navigation'
                            browser.navigate(state.get('activity_url') or state['lesson_url'], force=True)
                    else:
                        if queue_observation is None:
                            queue_observation = observe_queue(args,db,browser,completed,captured_tasks)
                        activity = queue_observation['selected']
                        if not activity:
                            logging.info('No eligible activity. Optional assessments remain queued; deferred/in-progress tasks require explicit --resume.')
                            break
                        logging.info('Selected %s %s%s',activity['task_type'],activity['title'],
                                     ': priority %.6f' % activity['priority'] if activity['selection_reason'] == 'priority'
                                     else ': assessment is required' if activity['selection_reason'] == 'required_assessment'
                                     else ': quiz retake is available' if activity['selection_reason'] == 'quiz_retake'
                                     else ': review queue order' if activity['selection_reason'] == 'review_queue_order'
                                     else ': assessment requirement needs inspection' if activity['selection_reason'] == 'assessment_requires_inspection'
                                     else ': next available activity in queue order')
                        if args.dry_run:
                            print(json.dumps(activity,indent=2))
                            break
                        if activity.get('stop_before_start'):
                            logging.info('Stopped before assessment task %s: requirement or layout needs inspection. Queue details are saved.',activity['task_id'])
                            journal(log,'assessment_not_started',task_id=activity['task_id'],activity=activity)
                            break
                        directory = args.output/str(activity['task_id'])
                        if (directory/'state.json').exists():
                            raise RuntimeError('Saved run exists; use --resume '+str(directory))
                        state = {'task_id':activity['task_id'],'topic_id':activity['topic_id'],'task_type':activity['task_type'],
                                 'activity_url':'https://mathacademy.com'+activity['href'],
                                 'selected_priority':activity.get('priority'),'kps':{},'examples':{},'questions':{},
                                 'previous_activity_snapshot':previous_activity_snapshot(args)}
                        if state['task_type'] == 'assessment':
                            state.update({key:activity.get(key) for key in
                                          ('test_id','assessment_details','assessment_notice','optional_xp_remaining','assessment_requirement','assessment_requirement_evidence','assessment_is_retake')})
                            atomic_json(directory/'assessment-queue.json',activity)
                        elif state['task_type'] == 'multistep':
                            state.update(multistep_id=activity['multistep_id'],title=activity['title'],answer_policy='all_correct')
                            atomic_json(directory/'multistep-queue.json',activity)
                        else:
                            state.update({key:activity[key] for key in ('answer_policy','perfect_retake_of') if key in activity})
                        atomic_json(directory/'state.json',state)
                        phase = 'topic'
                        topic = db.topic if state['task_type'] in ('assessment','multistep') else db.topic(activity['topic_id'],directory/'selection')
                        (directory/'selection').mkdir(parents=True,exist_ok=True)
                        for name in ('queue.json','priorities.edn','priorities-query.edn','priorities-inputs.edn','capture-priorities.json'):
                            source = args.state_dir/'selection'/name
                            if source.is_file():
                                shutil.copy2(source, directory/'selection'/source.name)
                        phase = 'start'
                        browser.start(activity)
                    phase = 'activity'
                    browser.activity(state,directory,topic)
                    update_policy(args.state_dir,completed_state=state)
                    phase = 'history'
                    if state.get('history_complete') and (directory/'content.json').exists():
                        content = json.loads((directory/'content.json').read_text())
                    else:
                        content = browser.history(state,directory,topic)
                    # Record capture completion separately from an EDB receipt. Never retake
                    # a completed MA activity because its database commit needs recovery.
                    journal(log,'activity_captured',task_id=state['task_id'],topic_id=state['topic_id'],task_type=state['task_type'],directory=str(directory))
                    captured_tasks.add(state['task_id'])
                    if state['task_type'] == 'lesson':
                        completed.add(state['topic_id'])
                    # Inspect even after the last allowed activity, and retain
                    # this fresh observation for selecting the next one.
                    phase = 'queue-after'
                    queue_observation = observe_queue(args,db,browser,completed,captured_tasks,
                                                      state['task_id'],directory)
                    phase = 'import'
                    result = db.import_content(content,directory/'edb-import',not args.preview)
                    state['preview_complete' if args.preview else 'import_complete'] = True
                    state.pop('deferred_error',None)
                    atomic_json(directory/'state.json',state)
                    journal(log,'content_imported' if not args.preview else 'content_previewed',task_id=state['task_id'],**result)
                    print(json.dumps({'run_directory':str(directory),'database':result},indent=2),flush=True)
                except (Exception,KeyboardInterrupt) as error:
                    if state is not None:
                        update_policy(args.state_dir,completed_state=state)
                    diagnostics = record_failure(args,browser,state,directory,phase,error)
                    blocking = isinstance(error,(AccessBlocked,KeyboardInterrupt))
                    if state is not None:
                        if not blocking:
                            state['deferred_error'] = {'phase':phase,'message':str(error),
                                                       'diagnostics':str(diagnostics)}
                            captured_tasks.add(state['task_id'])
                        atomic_json(directory/'state.json',state)
                    journal(log,'stopped' if blocking else 'activity_deferred',
                            task_id=(state or {}).get('task_id'),phase=phase,diagnostics=str(diagnostics))
                    logging.warning('%s during %s: %s; diagnostics: %s',type(error).__name__,phase,error,diagnostics)
                    if blocking:
                        raise
                    if state is None:
                        logging.error('Cannot read/select another activity; saved diagnostics and stopped this batch.')
                        break
                    queue_observation = None
                    logging.info('Deferred task %s; continuing with other available activities. Retry with --resume %s',
                                 state['task_id'],directory)
                if queue_observation is not None and not queue_observation['selected']:
                    logging.info('No eligible activity. Optional assessments remain queued; deferred/in-progress tasks require explicit --resume.')
                    break
                if n+1<args.limit:
                    pacer.wait('lesson','between activities')
                    if args.rest_every and (n+1)%args.rest_every==0:
                        pacer.wait('rest','periodic cooldown')
        finally:
            context.close()


def main(argv=None):
    args = arguments(argv)
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s')
    run_handler = None
    if args.command == 'run':
        log_directory = args.state_dir/'logs'
        log_directory.mkdir(parents=True,exist_ok=True)
        os.chmod(args.state_dir,0o700)
        run_handler = logging.FileHandler(log_directory/('run-' + str(time.time_ns()) + '.log'))
        run_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        logging.getLogger().addHandler(run_handler)
        logging.info('Run log: %s',run_handler.baseFilename)
    args.stop_event = threading.Event()
    def interrupted(*_):
        # Raising inside Playwright's event-loop/greenlet wait can strand its
        # shutdown. Request a stop; normal capture checkpoints perform it.
        args.stop_event.set()
    original_sigterm = signal.signal(signal.SIGTERM,interrupted)
    original_sigint = signal.signal(signal.SIGINT,interrupted)
    try:
        with locked(args.state_dir):
            run(args)
            if args.stop_event.is_set():
                raise KeyboardInterrupt('Stopped; saved checkpoints are retained')
    except (Exception,KeyboardInterrupt) as exc:
        logging.error('%s: %s',type(exc).__name__,exc)
        return 1
    finally:
        signal.signal(signal.SIGTERM,original_sigterm)
        signal.signal(signal.SIGINT,original_sigint)
        if run_handler is not None:
            logging.getLogger().removeHandler(run_handler)
            run_handler.close()
    return 0


if __name__=='__main__':
    raise SystemExit(main())
