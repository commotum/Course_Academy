#!/usr/bin/env python3
"""Capture lessons, reviews, multisteps, diagnostics, assessments and quiz retakes; import content only."""
import argparse
import contextlib
import fcntl
import itertools
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

from core import ROOT, CAPTURE_EDB_BIN, Pacer, atomic_json, choose_activity, journal
from queue_wait import clear_queue_wait, record_queue_wait
from database import Database
from retry_policy import apply_policy, update_policy


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['run','login','priorities','import-saved','sweep-saved'])
    parser.add_argument('--database',default=os.environ.get('EDB_DATABASE','course-academy-v2'))
    parser.add_argument('--endpoint',default=os.environ.get('EDB_ENDPOINT','/tmp/course-academy-edb-v2/writer.sock'))
    parser.add_argument('--edb-bin',default=os.environ.get('EDB_BIN',str(CAPTURE_EDB_BIN)))
    parser.add_argument('--learner-id',type=uuid.UUID,default=uuid.UUID('59d5cf13-351c-4114-be19-4c3bb64ee051'))
    parser.add_argument('--output',type=Path,default=ROOT/'reference/mathacademy/question-capture')
    parser.add_argument('--capture-root',type=Path,action='append',default=[],
                        help='Additional workers’ capture roots for shared import provenance; repeat for each worker')
    parser.add_argument('--state-dir',type=Path,default=ROOT/'.local/question_capture')
    parser.add_argument('--profile',type=Path,help='Dedicated Playwright profile; defaults to STATE_DIR/browser-profile')
    parser.add_argument('--content',type=Path,help='Saved content.json for import-saved')
    parser.add_argument('--resume',type=Path,help='Select a saved run first; saved activities in the live queue also recover automatically')
    parser.add_argument('--limit',type=int,help='Maximum attempted activities; default keeps running until the queue is empty or interrupted')
    parser.add_argument('--preview',action='store_true',help='Preview EDB writes. With run, MA answers are still submitted.')
    parser.add_argument('--capture-only',action='store_true',help='Run MA activities and save evidence; skip all EDB imports, previews and backlog sweeps. Database lookups are read-only.')
    parser.add_argument('--dry-run',action='store_true',help='With run: inspect queue and priorities without starting an activity')
    parser.add_argument('--headless',action='store_true',help='Default is a visible Chromium window')
    parser.add_argument('--browser-spec',help='Optional existing browser cookie source, using the original MA cookiekit syntax')
    parser.add_argument('--ma-root',type=Path,default=Path('/home/jake/Developer/MA'))
    parser.add_argument('--diagnostic-topics',type=Path,
                        help='Diagnostic course Topics.csv or graph directory; otherwise resolve the enrolled course graph under MA/COURSES')
    parser.add_argument('--diagnostic-covered-topics',type=Path,
                        help='Explicit account-specific JSON covered_topics allowlist with provenance; all other diagnostic skills skip')
    parser.add_argument('--diagnostic-course-id',type=int,
                        help='Fallback enrolled course ID for diagnostics when the queue does not expose it')
    parser.add_argument('--cwcwc-weight',type=float,default=0.7)
    parser.add_argument('--review-question-limit',type=int,default=20,
                        help='Stop a review before submitting more than this many questions')
    parser.add_argument('--seed',type=int,help='Optional reproducible sequence/pacing seed')
    parser.add_argument('--timeout-ms',type=int,default=45000)
    parser.add_argument('--settle-ms',type=int,default=1000)
    parser.add_argument('--ui-delay-ms',type=int,default=500,
                        help='Small delay for browser interactions, in addition to randomized waits; default 500 ms')
    parser.add_argument('--progress-course-id', dest='progress_course_ids', action='append', type=int,
                        help='Course progress to snapshot after each completed activity; repeat to override defaults 113,111,136')
    parser.add_argument('--progress-url',dest='progress_urls',action='append',
                        help='Exact course progress URL, including optional unitId; repeat instead of --progress-course-id')
    parser.add_argument('--solver-command',help='Command receiving JSON on stdin and returning solver JSON on stdout; no shell')
    parser.add_argument('--codex-bin',default='codex')
    parser.add_argument('--solver-model',help='Optional explicit Codex model for the solver')
    parser.add_argument('--solver-timeout',type=int,default=300)
    parser.add_argument('--no-import-repair',action='store_true',help='Defer failed imports without the persistent Codex repair session')
    parser.add_argument('--import-repair-timeout',type=int,default=600,help='Maximum seconds per completed-activity import repair turn')
    parser.add_argument('--no-capture-repair',action='store_true',help='Take ordinary cooldowns without inspecting capture failures')
    parser.add_argument('--capture-repair-timeout',type=int,default=180,help='Maximum seconds per capture repair diagnosis during a cooldown')
    parser.add_argument('--capture-repair-test-timeout',type=int,default=1800,
                        help='Maximum seconds for the complete offline suite validating a capture repair; default 1800 (30 minutes)')
    parser.add_argument('--batch-checkpoint',type=Path,help=argparse.SUPPRESS)
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
    args.progress_course_ids_explicit = args.progress_course_ids is not None or args.progress_urls is not None
    if args.progress_urls:
        if args.progress_course_ids is not None:parser.error('Use progress URLs or course IDs, rather than both')
        from progress import target
        try:scopes=[target(url) for url in args.progress_urls]
        except ValueError as error:parser.error(str(error))
        args.progress_urls=[s['source_url'] for s in scopes]
        args.progress_course_ids=[s['course_id'] for s in scopes]
    if args.progress_course_ids is None:
        args.progress_course_ids = [113, 111, 136]
    args.progress_mode='fixed' if args.progress_course_ids_explicit else 'sidebar'
    if any(c < 1 for c in args.progress_course_ids) or len(set(args.progress_course_ids)) != len(args.progress_course_ids):
        parser.error('Progress course IDs must be positive and unique')
    if args.diagnostic_course_id is not None and args.diagnostic_course_id < 1:
        parser.error('Diagnostic course ID must be positive')
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
    if (args.limit is not None and args.limit<1) or args.review_question_limit<1 or args.rest_every<0 or args.timeout_ms<1 or args.solver_timeout<1 or args.import_repair_timeout<1 or args.capture_repair_timeout<1 or args.capture_repair_test_timeout<1 or args.settle_ms<0 or args.ui_delay_ms<0:
        parser.error('Invalid limit, timeout, or rest frequency')
    if args.command=='import-saved' and not args.content:
        parser.error('import-saved requires --content')
    if args.capture_only and (args.command!='run' or args.preview):
        parser.error('--capture-only requires run and cannot be combined with --preview')
    if args.resume and (args.command!='run' or args.dry_run):
        parser.error('--resume requires run without --dry-run')
    if args.batch_checkpoint and (args.command!='run' or args.dry_run):
        parser.error('Maintenance checkpoints require run without --dry-run')
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
    assessments = []
    for source in sorted(args.output.glob('*/state.json')):
        state = json.loads(source.read_text())
        if superseded_before_start(state):
            continue
        directory = source.parent.resolve()
        verification = directory/'edb-import/verification.json'
        receipt = json.loads(verification.read_text()) if verification.exists() else {}
        if state.get('activity_complete') and state.get('history_complete') and (directory/'content.json').exists():
            # Completed captures belong to content-only recovery, even when
            # their import is still deferred. Never navigate to resume them.
            continue
        finished = state.get('import_complete') or receipt.get('committed') or receipt.get('already_complete')
        if args.preview:
            finished = finished or state.get('preview_complete')
        if (not finished and state.get('task_type') in ('assessment','diagnostic') and
                (state.get('assessment_started') or state.get('assessment_question_count') or
                 state.get('diagnostic_started') or state.get('diagnostic_start_intent')) and
                (not state.get('activity_complete') or not state.get('history_complete'))):
            if queued_resume(args,[{'task_id':state['task_id']}],set()):
                assessments.append(directory)
        if not finished and not state.get('deferred_error'):
            candidates.append(directory)
    if assessments:
        return max(assessments,key=lambda p:(p/'state.json').stat().st_mtime)
    return max(candidates,key=lambda p:(p/'state.json').stat().st_mtime) if candidates else None


def superseded_before_start(state):
    recovery = state.get('source_recovery', {})
    return (recovery.get('resolution') == 'verified_superseded_before_start' and
            recovery.get('superseded_by_captured_task') and not state.get('questions') and
            not state.get('examples'))


def queued_resume(args, queue, resumed):
    """Recover queued saved work once per worker, after fresh eligible work."""
    from capture_repair import deferred_failure, migrate_ledger, source_version
    ledger_path = args.state_dir/'capture-repair/failures.json'
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
    migrate_ledger(args,ledger)
    generation = None
    for activity in queue:
        if activity['task_id'] in resumed:
            continue
        directory = args.output/str(activity['task_id'])
        source = directory/'state.json'
        if not source.is_file():
            continue
        state = json.loads(source.read_text())
        if superseded_before_start(state):
            continue
        if (state.get('activity_complete') and state.get('history_complete') or
                state.get('import_complete')):
            continue
        diagnostic = Path(state.get('deferred_error',{}).get('diagnostics',''))/'error.json'
        if diagnostic.is_file():
            generation = generation or source_version()
            if deferred_failure(args,diagnostic,ledger,generation,legacy_evidence=True,resume=True):
                continue
        return directory.resolve()
    return None


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


def idle_capture_repair(args, pacer, queue, attempted, completed, captured_tasks):
    """Inspect one backlog failure, then let the caller refresh the live queue."""
    if (args.dry_run or args.no_capture_repair or not queue or
            args.limit is not None and attempted >= args.limit):
        return False
    from capture_repair import cooldown, next_failure
    ledger_path = args.state_dir/'capture-repair/failures.json'
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
    if next_failure(args,ledger) is None:
        return False
    logging.info('No eligible live activity; inspecting one outstanding capture failure')
    cooldown(args,pacer,{'attempted':attempted,'limit':args.limit,
                        'completed_topics':sorted(completed),'captured_tasks':sorted(captured_tasks)},
             pause=False)
    return True


def queued_capture_repair(args, pacer, queue, attempted, completed, captured_tasks):
    """Inspect one queued unfinished failure at a completed activity boundary."""
    if (args.dry_run or args.no_capture_repair or
            args.limit is not None and attempted >= args.limit):
        return False
    task_ids = set()
    for activity in queue:
        source = args.output/str(activity['task_id'])/'state.json'
        if source.is_file():
            saved = json.loads(source.read_text())
            if not saved.get('activity_complete') and saved.get('deferred_error'):
                task_ids.add(activity['task_id'])
    if not task_ids:
        return False
    from capture_repair import cooldown, next_failure
    ledger_path = args.state_dir/'capture-repair/failures.json'
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {}
    if next_failure(args,ledger,task_ids=task_ids) is None:
        return False
    import copy
    scoped = copy.copy(args)
    scoped.capture_repair_task_ids = task_ids
    logging.info('Completed activity; inspecting one queued unfinished capture failure')
    cooldown(scoped,pacer,{'attempted':attempted,'limit':args.limit,
                          'completed_topics':sorted(completed),'captured_tasks':sorted(captured_tasks)},
             pause=False)
    return True


def observe_queue(args, db, browser, completed, captured_tasks, after_task_id=None, directory=None):
    queue = browser.queue()
    retry_policy = update_policy(args.state_dir,getattr(browser,'completed_outcomes',()))
    priorities = db.priorities(args.learner_id,args.state_dir/'selection',
                              topic_ids=[i['topic_id'] for i in queue if i['task_type'] in ('lesson','review') and i['topic_id'] is not None],
                              knowledge_snapshot=previous_activity_snapshot(args))
    retry_topics = {int(key.split(':')[1]) for key in retry_policy['pending'] if key.startswith('lesson:')}
    blocked_topics = set(completed)-retry_topics
    # A placement/course change can assign a new lesson for a topic captured
    # earlier. The live unlocked task identity is authoritative for that new
    # assignment; it must not be suppressed forever by the historical topic.
    observed_captured = set(captured_tasks) | {
        item['task_id'] for item in getattr(browser,'completed_outcomes',())}
    reassigned = [item for item in queue if
        item.get('task_type') == 'lesson' and item.get('topic_id') in blocked_topics and
        item['task_id'] not in observed_captured and item.get('capture_supported') is True and
        item.get('in_progress') is False and item.get('progress') == 0 and
        item.get('card_id') == 'task-'+str(item['task_id']) and
        item.get('start_id') == 'taskStartButton-'+str(item['task_id']) and
        item.get('href') == '/tasks/%s/topics/%s/lesson' % (item['task_id'],item['topic_id'])]
    reassigned_tasks = {item['task_id'] for item in reassigned}
    historically_blocked_tasks = {item['task_id'] for item in queue if (
        item.get('task_type','lesson') == 'lesson' and item.get('topic_id') in blocked_topics and
        item['task_id'] not in reassigned_tasks)}
    selected = apply_policy(choose_activity(queue, priorities,
        blocked_topics-{item['topic_id'] for item in reassigned},
        observed_captured|historically_blocked_tasks),retry_policy)
    observation = {'queue':queue, 'selected':selected,'completed_outcomes':getattr(browser,'completed_outcomes',[]),
                   'reassigned_lessons':[{'task_id':item['task_id'],'topic_id':item['topic_id'],
                       'href':item['href'],'reason':'fresh_unlocked_task_overrides_historical_topic'}
                       for item in reassigned],
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
                     ' [in progress; saved recovery]' if item.get('in_progress') else
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
                               ('limit','preview','capture_only','timeout_ms','solver_timeout','solver_model','seed','ui_delay_ms',
                                'edb_bin','database')},
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
    if args.command == 'run':
        clear_queue_wait(args.state_dir)
        if args.capture_only:
            logging.info('CAPTURE ONLY: saving source evidence locally; database imports, previews and saved-import sweeps are disabled')
    if args.command=='import-saved':
        content = json.loads(args.content.read_text())
        from import_repair import import_with_repair
        directory = args.content.parent
        source = directory/'state.json'
        state = json.loads(source.read_text()) if source.exists() else {}
        result = import_with_repair(Database(args),content,directory,state,args)
        if state and (result.get('previewed') or result.get('committed') or result.get('already_complete')):
            from saved_imports import complete
            complete(args,directory,state,result)
        print(json.dumps(result,indent=2))
        return
    db = Database(args)
    if args.command=='priorities':
        priorities = db.priorities(args.learner_id,args.state_dir/'selection')
        print(json.dumps(sorted(priorities.items(),key=lambda p:p[1],reverse=True),indent=2))
        return
    if args.command in ('run','sweep-saved'):
        from saved_imports import sweep
        results = sweep(db,args,trigger='startup',exclude=[args.resume] if args.resume else (),
                        repair_budget=1 if args.command == 'run' else None)
        if args.command == 'sweep-saved':
            print(json.dumps(results,indent=2))
            return
        if args.resume and not args.batch_checkpoint:
            from saved_imports import eligible, read_json, complete
            directory = args.resume.resolve()
            state,content = read_json(directory/'state.json'),read_json(directory/'content.json')
            if not args.dry_run and eligible(directory,state,content):
                from import_repair import import_with_repair
                try:
                    result = import_with_repair(db,content,directory,state,args)
                    if result.get('previewed') or result.get('committed') or result.get('already_complete'):
                        complete(args,directory,state,result)
                    sweep(db,args,trigger='batch-end',exclude=[directory])
                    print(json.dumps(result,indent=2))
                except Exception as error:
                    if args.limit == 1:
                        raise
                    logging.warning('Saved import remains pending; continuing the activity queue: %s',error)
                if args.limit == 1:
                    return
                # --resume selects the first task, not the lifetime of the batch.
                args.resume = None
    batch = json.loads(args.batch_checkpoint.read_text()) if args.batch_checkpoint else {}
    start_n = batch.get('attempted',0)
    if batch and (batch.get('limit')!=args.limit or start_n<0 or
                  args.limit is not None and start_n>args.limit):
        raise ValueError('Maintenance checkpoint does not match the batch limit')
    if batch and start_n==args.limit:
        if args.command == 'run':
            sweep(db,args,trigger='batch-end')
        logging.info('Maintenance checkpoint reached the activity limit; batch is complete.')
        return
    resume_directory = (Path(batch['next_resume']) if batch.get('next_resume') else None) if batch else (
        unfinished_run(args) if args.command=='run' else None)
    if resume_directory and batch:
        saved = json.loads((resume_directory/'state.json').read_text())
        if saved.get('activity_complete') and saved.get('history_complete') and (resume_directory/'content.json').exists():
            resume_directory = None
    if resume_directory and args.dry_run:
        state = json.loads((resume_directory/'state.json').read_text())
        print(json.dumps({'resume_directory':str(resume_directory),'task_id':state['task_id'],
                          'task_type':state.get('task_type','lesson'),
                          'captured_questions':len(state.get('questions',{}))},indent=2))
        return
    from playwright.sync_api import sync_playwright
    from browser import AccessBlocked, RateLimited, CaptureBrowser, LEARN, repair_math_editor_document
    from solver import Solver
    from capture_repair import RestartWorker
    rng = random.Random(args.seed)
    if batch.get('rng_state'):
        from capture_repair import tuple_tree
        rng.setstate(tuple_tree(batch['rng_state']))
    pacer = Pacer(args,rng)
    args.profile.mkdir(parents=True,exist_ok=True)
    os.chmod(args.profile,0o700)
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(str(args.profile),
            headless=args.headless if args.command!='login' else False,slow_mo=args.ui_delay_ms)
        try:
            import_cookies(args,context)
            page = context.pages[0] if context.pages else context.new_page()
            context.route('https://mathacademy.com/**',repair_math_editor_document)
            browser = CaptureBrowser(page,args,pacer,Solver(args))
            browser.database = db
            if args.command=='login':
                page.goto(LEARN,wait_until='domcontentloaded')
                input('Sign in to Math Academy in this window, then press Enter here: ')
                browser.check()
                logging.info('Session retained in the dedicated private profile')
                return
            completed = set(batch.get('completed_topics',[]))
            captured_tasks = set(batch.get('captured_tasks',[]))
            log = args.state_dir/'journal.jsonl'
            for entry in read_journal(log):
                if entry['event'] in ('lesson_captured','activity_captured'):
                    captured_tasks.add(entry['task_id'])
                    if entry.get('task_type','lesson') == 'lesson' and entry.get('activity_outcome') != 'failed':
                        completed.add(entry['topic_id'])
            deferred, pending_imports = [], []
            for source in args.output.glob('*/state.json'):
                saved = json.loads(source.read_text())
                captured_tasks.add(saved['task_id'])
                if saved.get('import_complete') or args.preview and saved.get('preview_complete'):
                    continue
                if resume_directory and source.parent.resolve() == resume_directory.resolve():
                    continue
                if saved.get('deferred_error'):
                    if saved.get('activity_complete') and saved.get('history_complete'):
                        pending_imports.append(saved['task_id'])
                    else:
                        deferred.append(saved['task_id'])
            if pending_imports:
                logging.debug('Completed captures awaiting database import: %s',sorted(pending_imports))
            if deferred:
                logging.debug('Saved captures awaiting automatic recovery: %s',sorted(deferred))
            queue_observation = None
            queue_failures = 0
            consecutive_failures = 0
            idle_cycles = 0
            resumed_tasks = set()
            imported_directories = set()
            attempts = itertools.count(start_n) if args.limit is None else range(start_n,args.limit)
            for n in attempts:
                pacer.check_stop()
                clear_queue_wait(args.state_dir)
                directory, state, phase = None, None, 'queue'
                try:
                    if not resume_directory and queue_observation is None:
                        queue_observation = observe_queue(args,db,browser,completed,captured_tasks)
                    if not resume_directory and not queue_observation['selected']:
                        inspected = idle_capture_repair(args,pacer,queue_observation['queue'],n,completed,captured_tasks)
                        if inspected:
                            queue_observation = observe_queue(args,db,browser,completed,captured_tasks)
                        if not queue_observation['selected']:
                            resume_directory = queued_resume(args,queue_observation['queue'],resumed_tasks)
                            if not resume_directory:
                                if queue_observation['queue'] and not args.dry_run:
                                    idle_cycles += 1
                                    record_queue_wait(args,queue_observation['queue'])
                                    logging.info('Queued work is awaiting recovery; keeping the worker available')
                                    pacer.backoff(idle_cycles)
                                    queue_observation = None
                                    continue
                                logging.info('No queued activity; batch is complete.')
                                break
                    if resume_directory:
                        directory = resume_directory
                        resume_directory = None
                        logging.info('Resuming saved activity %s',directory)
                        state = json.loads((directory/'state.json').read_text())
                        resumed_tasks.add(state['task_id'])
                        state.setdefault('task_type', 'lesson')
                        state.setdefault('previous_activity_snapshot',previous_activity_snapshot(args))
                        phase = 'topic'
                        topic = db.topic if state['task_type'] in ('assessment','multistep','diagnostic') else db.topic(state['topic_id'],directory/'selection')
                        if state['task_type'] == 'diagnostic' and not state.get('diagnostic_policy'):
                            from diagnostic import configure
                            configure(args, state, state, directory)
                        if not state.get('activity_complete') and not state.get(state['task_type'] + '_complete'):
                            phase = 'navigation'
                            browser.navigate(state.get('activity_url') or state['lesson_url'], force=True)
                            if state['task_type'] == 'diagnostic':
                                state['diagnostic_restored'] = True
                    else:
                        if queue_observation is None:
                            queue_observation = observe_queue(args,db,browser,completed,captured_tasks)
                        activity = queue_observation['selected']
                        logging.info('Selected %s %s%s',activity['task_type'],activity['title'],
                                     ': priority %.6f' % activity['priority'] if activity['selection_reason'] == 'priority'
                                     else ': assessment is required' if activity['selection_reason'] == 'required_assessment'
                                     else ': quiz retake is available' if activity['selection_reason'] == 'quiz_retake'
                                     else ': optional assessment; no other eligible activity' if activity['selection_reason'] == 'optional_assessment_fallback'
                                     else ': review queue order' if activity['selection_reason'] == 'review_queue_order'
                                     else ': assessment requirement needs inspection' if activity['selection_reason'] == 'assessment_requires_inspection'
                                     else ': next available activity in queue order')
                        if args.dry_run:
                            print(json.dumps(activity,indent=2))
                            break
                        if activity.get('stop_before_start'):
                            journal(log,'assessment_not_started',task_id=activity['task_id'],activity=activity)
                            raise ValueError('Assessment task %s needs eligibility/layout recovery; queue details are saved' % activity['task_id'])
                        directory = args.output/str(activity['task_id'])
                        if (directory/'state.json').exists():
                            raise RuntimeError('Saved run exists; use --resume '+str(directory))
                        state = {'task_id':activity['task_id'],'topic_id':activity['topic_id'],'task_type':activity['task_type'],
                                 'activity_url':'https://mathacademy.com'+activity['href'],
                                 'selected_priority':activity.get('priority'),'kps':{},'examples':{},'questions':{},
                                 'previous_activity_snapshot':previous_activity_snapshot(args)}
                        if state['task_type']!='diagnostic':
                            state['progress_course_ids']=args.progress_course_ids
                            state['progress_mode']=args.progress_mode
                            if args.progress_urls:state['progress_urls']=args.progress_urls
                        if state['task_type'] == 'assessment':
                            state.update({key:activity.get(key) for key in
                                          ('test_id','assessment_details','assessment_notice','optional_xp_remaining','assessment_requirement','assessment_requirement_evidence','assessment_is_retake','assessment_optional_fallback')})
                            atomic_json(directory/'assessment-queue.json',activity)
                        elif state['task_type'] == 'multistep':
                            state.update(multistep_id=activity['multistep_id'],title=activity['title'],answer_policy='all_correct')
                            atomic_json(directory/'multistep-queue.json',activity)
                        elif state['task_type'] == 'diagnostic':
                            from diagnostic import configure
                            state.update(diagnostic_id=activity['diagnostic_id'], title=activity['title'])
                            configure(args, activity, state, directory)
                            atomic_json(directory/'diagnostic-queue.json',activity)
                        else:
                            state.update({key:activity[key] for key in ('answer_policy','perfect_retake_of') if key in activity})
                        atomic_json(directory/'state.json',state)
                        phase = 'topic'
                        topic = db.topic if state['task_type'] in ('assessment','multistep','diagnostic') else db.topic(activity['topic_id'],directory/'selection')
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
                    journal(log,'activity_captured',task_id=state['task_id'],topic_id=state['topic_id'],task_type=state['task_type'],directory=str(directory),activity_outcome=state.get('activity_outcome'))
                    captured_tasks.add(state['task_id'])
                    if state['task_type'] == 'lesson' and state.get('activity_outcome') != 'failed':
                        completed.add(state['topic_id'])
                    # Inspect even after the last allowed activity, and retain
                    # this fresh observation for selecting the next one.
                    phase = 'queue-after'
                    queue_observation = observe_queue(args,db,browser,completed,captured_tasks,
                                                      state['task_id'],directory)
                    phase = 'import'
                    from import_repair import import_with_repair
                    result = import_with_repair(db,content,directory,state,args)
                    from saved_imports import complete
                    if result.get('previewed') or result.get('committed') or result.get('already_complete'):
                        complete(args,directory,state,result)
                        imported_directories.add(directory)
                    print(json.dumps({'run_directory':str(directory),'database':result},indent=2),flush=True)
                    if queue_observation['selected']:
                        queued_capture_repair(args,pacer,queue_observation['queue'],n+1,completed,captured_tasks)
                    consecutive_failures = 0
                    idle_cycles = 0
                except RestartWorker:
                    raise  # Early maintenance is control flow, not a queue failure.
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
                    if isinstance(error, RateLimited):
                        # A rejected/ambiguous submission is never replayed here.
                        # Reopen its checkpoint and reconcile the current grade.
                        pacer.backoff(1, retry_after=error.retry_after)
                        if state is not None and not state.get('activity_complete'):
                            resume_directory = directory
                            resumed_tasks.discard(state['task_id'])
                        queue_observation = None
                        continue
                    if state is None:
                        # Queue layout failures used to exit before maintenance.
                        # Inspect them now, and retry transient reads with a pause.
                        from capture_repair import cooldown
                        cooldown(args,pacer,{'attempted':n,'limit':args.limit,
                                            'completed_topics':sorted(completed),
                                            'captured_tasks':sorted(captured_tasks)},pause=False)
                        queue_failures += 1
                        # If MA forces an active quiz, reopen its existing
                        # checkpoint instead of repeatedly asking for the queue.
                        import re
                        redirect = re.search(r'/tasks/(\d+)/(?:tests|diagnostics)/\d+',browser.page.url)
                        if redirect:
                            saved = args.output/redirect[1]
                            if (saved/'state.json').is_file():
                                resume_directory = saved
                        queue_observation = None
                        pacer.backoff(queue_failures)
                        continue
                    consecutive_failures += 1
                    if ((state.get('task_type') in ('assessment','diagnostic') and not state.get('activity_complete')) or
                            consecutive_failures >= 2):
                        # A forced assessment redirect may prevent queue access.
                        # Repair at this boundary instead of exiting before the
                        # 20-activity maintenance break can ever be reached.
                        from capture_repair import cooldown
                        cooldown(args,pacer,{'attempted':n+1,'limit':args.limit,
                                            'completed_topics':sorted(completed),
                                            'captured_tasks':sorted(captured_tasks)},pause=False)
                        consecutive_failures = 0
                    queue_observation = None
                    logging.info('Saved task %s for automatic recovery; continuing with available activities: %s',
                                 state['task_id'],directory)
                queue_failures = 0
                if args.limit is None or n+1<args.limit:
                    pacer.wait('lesson','between activities')
                    if args.rest_every and (n+1)%args.rest_every==0:
                        from capture_repair import cooldown
                        cooldown(args,pacer,{'attempted':n+1,'limit':args.limit,
                                            'completed_topics':sorted(completed),
                                            'captured_tasks':sorted(captured_tasks)})
            from saved_imports import sweep
            sweep(db,args,trigger='batch-end',exclude=imported_directories)
        finally:
            context.close()


def main(argv=None):
    args = arguments(argv)
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s')
    run_handler = None
    restart = None
    from capture_repair import RestartWorker
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
    except RestartWorker as request:
        if args.stop_event.is_set():
            logging.info('Stopped before maintenance restart; checkpoint: %s',request.checkpoint)
            return 1
        restart = request.checkpoint
    except KeyboardInterrupt as exc:
        if args.stop_event.is_set():
            logging.info('Stopped; saved checkpoints are retained')
            return 0
        logging.error('%s: %s',type(exc).__name__,exc)
        return 1
    except Exception as exc:
        logging.error('%s: %s',type(exc).__name__,exc)
        return 1
    finally:
        signal.signal(signal.SIGTERM,original_sigterm)
        signal.signal(signal.SIGINT,original_sigint)
        if run_handler is not None:
            logging.getLogger().removeHandler(run_handler)
            run_handler.close()
    if restart:
        values = list(sys.argv[1:] if argv is None else argv)
        if '--batch-checkpoint' in values:
            index = values.index('--batch-checkpoint');del values[index:index+2]
        values = [v for v in values if not v.startswith('--batch-checkpoint=')]
        if '--resume' in values:
            index = values.index('--resume');del values[index:index+2]
        values = [v for v in values if not v.startswith('--resume=')]
        logging.info('Restarting capture worker with the remaining batch limit and saved sessions')
        os.execv(sys.executable,[sys.executable,str(Path(__file__).parent),*values,
                                '--batch-checkpoint',str(restart)])
    return 0


if __name__=='__main__':
    raise SystemExit(main())
