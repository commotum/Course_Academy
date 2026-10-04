#!/usr/bin/env python3
"""Capture highest-priority queued lessons and import their question content."""
import argparse
import contextlib
import fcntl
import json
import logging
import os
import random
import sys
import uuid
from pathlib import Path

from core import ROOT, Pacer, atomic_json, choose_lesson, journal
from database import Database


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
    parser.add_argument('--resume',type=Path,help='Resume a run directory containing state.json')
    parser.add_argument('--limit',type=int,default=1,help='Maximum lessons per invocation; default 1')
    parser.add_argument('--preview',action='store_true',help='Preview EDB writes. With run, MA answers are still submitted.')
    parser.add_argument('--dry-run',action='store_true',help='With run: inspect queue and priorities without starting a lesson')
    parser.add_argument('--headless',action='store_true',help='Default is a visible Chromium window')
    parser.add_argument('--browser-spec',help='Optional existing browser cookie source, using the original MA cookiekit syntax')
    parser.add_argument('--ma-root',type=Path,default=Path('/home/jake/Developer/MA'))
    parser.add_argument('--cwcwc-weight',type=float,default=0.7)
    parser.add_argument('--seed',type=int,help='Optional reproducible sequence/pacing seed')
    parser.add_argument('--timeout-ms',type=int,default=45000)
    parser.add_argument('--settle-ms',type=int,default=1000)
    parser.add_argument('--progress-course-id', dest='progress_course_ids', action='append', type=int,
                        help='Course progress to snapshot after every step; repeat to override defaults 113,111,136')
    parser.add_argument('--solver-command',help='Command receiving JSON on stdin and returning solver JSON on stdout; no shell')
    parser.add_argument('--codex-bin',default='codex')
    parser.add_argument('--solver-model',help='Optional explicit Codex model for the solver')
    parser.add_argument('--solver-timeout',type=int,default=300)
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
    if args.limit<1 or args.rest_every<0 or args.timeout_ms<1 or args.solver_timeout<1 or args.settle_ms<0:
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
    from playwright.sync_api import sync_playwright
    from browser import CaptureBrowser, LEARN
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
            browser = CaptureBrowser(page,args,pacer,Solver(args))
            if args.command=='login':
                page.goto(LEARN,wait_until='domcontentloaded')
                input('Sign in to Math Academy in this window, then press Enter here: ')
                browser.check()
                logging.info('Session retained in the dedicated private profile')
                return
            completed = set()
            log = args.state_dir/'journal.jsonl'
            if log.exists():
                for line in log.read_text().splitlines():
                    entry = json.loads(line)
                    if entry['event']=='lesson_captured':
                        completed.add(entry['topic_id'])
            for n in range(args.limit):
                if args.resume and n==0:
                    directory = args.resume.resolve()
                    state = json.loads((directory/'state.json').read_text())
                    topic = db.topic(state['topic_id'],directory/'selection')
                    if not state.get('lesson_complete'):
                        browser.navigate(state['lesson_url'])
                else:
                    priorities = db.priorities(args.learner_id,args.state_dir/'selection')
                    queue = browser.queue()
                    lesson = choose_lesson(queue,priorities,completed)
                    atomic_json(args.state_dir/'selection/queue.json',{'queue':queue,'selected':lesson,'unranked_topics':[i['topic_id'] for i in queue if i['topic_id'] not in priorities]})
                    if not lesson:
                        logging.info('No new lesson is both available in Math Academy and ranked/unlocked in EDB. Required reviews may be occupying the queue.')
                        break
                    logging.info('Selected %s: priority %.6f',lesson['title'],lesson['priority'])
                    if args.dry_run:
                        print(json.dumps(lesson,indent=2))
                        break
                    directory = args.output/str(lesson['task_id'])
                    if (directory/'state.json').exists():
                        raise RuntimeError('Saved run exists; use --resume '+str(directory))
                    topic = db.topic(lesson['topic_id'],directory/'selection')
                    state = {'task_id':lesson['task_id'],'topic_id':lesson['topic_id'],
                             'lesson_url':'https://mathacademy.com'+lesson['href'],
                             'selected_priority':lesson['priority'],'kps':{},'examples':{},'questions':{}}
                    atomic_json(directory/'state.json',state)
                    browser.knowledge_snapshot(state,directory,'baseline')
                    browser.start(lesson)
                try:
                    browser.lesson(state,directory,topic)
                    if state.get('history_complete') and (directory/'content.json').exists():
                        content = json.loads((directory/'content.json').read_text())
                    else:
                        content = browser.history(state,directory)
                    # Record capture completion separately from an EDB receipt. Never retake
                    # a completed MA lesson because its database commit needs recovery.
                    journal(log,'lesson_captured',task_id=state['task_id'],topic_id=state['topic_id'],directory=str(directory))
                    completed.add(state['topic_id'])
                    result = db.import_content(content,directory/'edb-import',not args.preview)
                    journal(log,'content_imported' if not args.preview else 'content_previewed',task_id=state['task_id'],**result)
                    print(json.dumps({'run_directory':str(directory),'database':result},indent=2),flush=True)
                except BaseException:
                    atomic_json(directory/'state.json',state)
                    try:
                        page.screenshot(path=str(directory/'stopped.png'))
                    except Exception:
                        pass
                    journal(log,'stopped',task_id=state['task_id'],directory=str(directory))
                    raise
                if n+1<args.limit:
                    pacer.wait('lesson','between lessons')
                    if args.rest_every and (n+1)%args.rest_every==0:
                        pacer.wait('rest','periodic cooldown')
        finally:
            context.close()


def main(argv=None):
    args = arguments(argv)
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s')
    try:
        with locked(args.state_dir):
            run(args)
    except (Exception,KeyboardInterrupt) as exc:
        logging.error('%s: %s',type(exc).__name__,exc)
        return 1
    return 0


if __name__=='__main__':
    raise SystemExit(main())
