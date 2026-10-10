"""Named account profiles, tmux workers and a local status display."""
import argparse
import contextlib
import fcntl
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from core import ROOT, atomic_json
from solver import process_token

PACKAGE = Path(__file__).resolve().parent
CONFIG = PACKAGE/'workers.json'
FLEET_DIR = ROOT/'.local/question_capture-fleet'


def read_json(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return {}


def config(path=CONFIG):
    data=json.loads(Path(path).read_text())
    data['config_path']=str(Path(path).resolve())
    for worker in data['workers']:
        for name in ('state_dir','output'):
            worker[name]=(ROOT/worker[name]).resolve()
        worker['profile']=worker['state_dir']/'browser-profile'
        worker['auth_file']=worker['state_dir']/'profile-auth.json'
        worker['supervision']=worker['state_dir']/'supervision'
    for field in ('id','window','state_dir','output','profile'):
        values=[w[field] for w in data['workers']]
        if len(set(values))!=len(values):
            raise ValueError('Worker '+field+' must be unique')
    return data


def selected(data, names):
    names=set(names or [w['id'] for w in data['workers']])
    unknown=names-{w['id'] for w in data['workers']}
    if unknown:
        raise ValueError('Unknown worker: '+', '.join(sorted(unknown)))
    return [w for w in data['workers'] if w['id'] in names]


@contextlib.contextmanager
def file_lock(path, *, blocking=False):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a') as handle:
        fcntl.flock(handle,fcntl.LOCK_EX|(0 if blocking else fcntl.LOCK_NB))
        yield


def capture_running(worker):
    try:
        with file_lock(worker['state_dir']/'capture.lock'):
            return False
    except BlockingIOError:
        return True


def supervisor_running(worker):
    saved=read_json(worker['supervision']/'fleet-worker.json')
    return bool(saved.get('process_token') and process_token(saved.get('pid'))==saved['process_token'])


def ready(worker):
    auth=read_json(worker['auth_file'])
    return bool(auth.get('course_id') and auth.get('username') and
                auth.get('course_name')==worker['course'] and
                (worker['profile']/'Default/Cookies').is_file())


def worker_command(data, worker, *, dry_run=False, limit=None, capture_only=None):
    auth=read_json(worker['auth_file'])
    course_id=auth.get('course_id') or worker.get('course_id')
    command=[sys.executable,'-u',str(PACKAGE),'run','--headless',
             '--state-dir',str(worker['state_dir']),'--output',str(worker['output']),
             '--profile',str(worker['profile']),'--codex-bin','/home/jake/.local/bin/codex',
             '--diagnostic-topics',worker['topics']]
    for key, option in [('database','--database'),('endpoint','--endpoint'),
                        ('math_root','--math-root'),('postgres_url','--postgres-url')]:
        if data.get(key):command += [option,str(data[key])]
    if worker.get('diagnostic_covered_topics'):
        command += ['--diagnostic-covered-topics',str((ROOT/worker['diagnostic_covered_topics']).resolve())]
    if course_id:
        command += ['--diagnostic-course-id',str(course_id)]
    if worker.get('progress_mode')=='fixed' and worker.get('progress_urls'):
        for url in worker['progress_urls']:command += ['--progress-url',url]
    elif worker.get('progress_mode')=='fixed':
        for cid in worker.get('progress_course_ids') or [course_id]:
            command += ['--progress-course-id',str(cid)]
    for other in data['workers']:
        command += ['--capture-root',str(other['output'])]
    if dry_run:command.append('--dry-run')
    if (data.get('capture_only',False) if capture_only is None else capture_only):
        command.append('--capture-only')
    if limit is not None:command += ['--limit',str(limit)]
    return command


def profile_identity(page):
    page.locator('#userMenu-username').wait_for(state='attached')
    course=page.locator('a#courseNameLink, a.courseNameLink').first
    course.wait_for(state='attached')
    match=re.fullmatch(r'/courses/(\d+)/progress',course.get_attribute('href') or '')
    if not match:
        raise ValueError('The logged-in page did not expose its enrolled course')
    return {'username':page.locator('#userMenu-username').text_content().strip(),
            'course_name':course.text_content().strip(),'course_id':int(match[1])}


def save_profile(worker, browser_spec=None):
    """Copy MA cookies once, then verify and persist the independent profile."""
    from capture import arguments, import_cookies, locked
    from browser import LEARN, repair_math_editor_document
    from playwright.sync_api import sync_playwright
    with locked(worker['state_dir']):
        worker['profile'].mkdir(parents=True,exist_ok=True)
        os.chmod(worker['state_dir'],0o700);os.chmod(worker['profile'],0o700)
        with sync_playwright() as runtime:
            context=runtime.chromium.launch_persistent_context(str(worker['profile']),headless=True)
            try:
                if browser_spec:
                    args=arguments(['run','--browser-spec',browser_spec])
                    import_cookies(args,context)
                context.route('https://mathacademy.com/**',repair_math_editor_document)
                page=context.pages[0] if context.pages else context.new_page()
                page.set_default_timeout(15000)
                page.goto(LEARN,wait_until='domcontentloaded',timeout=45000)
                identity=profile_identity(page)
                if identity['course_name']!=worker['course']:
                    raise ValueError('Profile belongs to '+identity['course_name']+', expected '+worker['course'])
                if worker.get('username') and identity['username']!=worker['username']:
                    raise ValueError('Profile account differs from the configured original account')
                identity.update(verified_at=time.time(),profile=str(worker['profile']))
                from dashboard import capture as capture_dashboard
                page.wait_for_timeout(1000)
                capture_dashboard(page,worker['state_dir'])
                atomic_json(worker['auth_file'],identity);os.chmod(worker['auth_file'],0o600)
                print(worker['id']+': saved '+identity['username']+' / '+identity['course_name'])
                return identity
            finally:
                context.close()


def tmux(*args, check=True):
    result=subprocess.run(['tmux',*map(str,args)],text=True,capture_output=True)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or 'tmux command failed')
    return result


def invocation(data, command, *args):
    return shlex.join([sys.executable,str(Path(__file__).resolve()),'--config',data['config_path'],command,*args])


def ensure_layout(data):
    session=data['session'];first=data['workers'][0]['window']
    placeholder='printf "%s\\n" "Worker is stopped. Run scripts/ma-workers start to resume."; exec bash'
    if tmux('has-session','-t',session,check=False).returncode:
        tmux('new-session','-d','-s',session,'-n',first,'-c',str(ROOT),placeholder)
    rows=tmux('list-windows','-t',session,'-F','#{window_id}\t#{window_name}').stdout.splitlines()
    windows={name:wid for wid,name in (r.split('\t',1) for r in rows)}
    if first not in windows:
        # Reuse the stopped original capture shell, without touching other sessions.
        for name in ('capture','bash'):
            if name not in windows:continue
            panes=tmux('list-panes','-t',windows[name],'-F','#{pane_current_command}').stdout.splitlines()
            if panes==['bash']:
                wid=windows.pop(name);tmux('rename-window','-t',wid,first);windows[first]=wid;break
    for worker in data['workers']:
        name=worker['window']
        if name not in windows:
            wid=tmux('new-window','-d','-P','-F','#{window_id}','-t',session,'-n',name,
                     '-c',str(ROOT),placeholder).stdout.strip()
            windows[name]=wid
        tmux('set-window-option','-t',windows[name],'automatic-rename','off')
        tmux('set-window-option','-t',windows[name],'remain-on-exit','on')
    target=windows[first]
    panes=tmux('list-panes','-t',target,'-F','#{pane_id}\t#{@ma_dashboard}').stdout.splitlines()
    dashboard=next((p.split('\t')[0] for p in panes if p.endswith('\t1')),None)
    if dashboard is None:
        dashboard=tmux('split-window','-d','-b','-v','-l','18','-P','-F','#{pane_id}',
                       '-t',target,'-c',str(ROOT),invocation(data,'dashboard')).stdout.strip()
        tmux('set-option','-p','-t',dashboard,'@ma_dashboard','1')
    elif tmux('display-message','-p','-t',dashboard,'#{pane_dead}').stdout.strip()=='1':
        tmux('respawn-pane','-t',dashboard,invocation(data,'dashboard'))
    tmux('resize-pane','-t',dashboard,'-y','18')
    tmux('set-option','-t',session,'status-interval','5')
    tmux('set-option','-t',session,'status-right-length','45')
    tmux('set-option','-t',session,'status-right',"#("+invocation(data,'status','--compact')+")")
    return windows


def start(data, workers, *, dry_run=False, limit=None, capture_only=None):
    FLEET_DIR.mkdir(parents=True,exist_ok=True)
    with file_lock(FLEET_DIR/'launch.lock'):
        windows=ensure_layout(data)
        for worker in workers:
            if capture_running(worker) or supervisor_running(worker):
                print(worker['id']+': already running');continue
            if not ready(worker):
                print(worker['id']+': not configured; save its profile first');continue
            target=windows[worker['window']]
            panes=tmux('list-panes','-t',target,'-F','#{pane_id}\t#{@ma_dashboard}\t#{pane_current_command}\t#{pane_dead}').stdout.splitlines()
            candidates=[row.split('\t') for row in panes if row.split('\t')[1]!='1']
            if len(candidates)!=1 or (candidates[0][2] not in ('bash','sh') and candidates[0][3]!='1'):
                print(worker['id']+': window is busy; leaving it alone');continue
            pane=candidates[0][0]
            args=[worker['id']]+(['--dry-run'] if dry_run else [])
            if (data.get('capture_only',False) if capture_only is None else capture_only):
                args.append('--capture-only')
            if limit is not None:args += ['--limit',str(limit)]
            tmux('respawn-pane','-k','-t',pane,'-c',str(ROOT),invocation(data,'worker',*args))
            print(worker['id']+': starting'+(' (queue inspection only)' if dry_run else ''))


def run_worker(data, worker, *, dry_run=False, limit=None, capture_only=None):
    root=worker['supervision'];root.mkdir(parents=True,exist_ok=True);os.chmod(root,0o700)
    with file_lock(root/'fleet-supervisor.lock'):
        if capture_running(worker):
            print('Existing worker owns this account; no duplicate started.');return 0
        command=worker_command(data,worker,dry_run=dry_run,limit=limit,capture_only=capture_only)
        stop=threading.Event()
        original={sig:signal.signal(sig,lambda *_:stop.set()) for sig in (signal.SIGINT,signal.SIGTERM)}
        log=root/('console-'+str(time.time_ns())+'.log')
        saved={'pid':os.getpid(),'process_token':process_token(os.getpid()),'started_at':time.time(),
               'command':command,'log':str(log),'worker':worker['id'],'dry_run':dry_run}
        process=None
        try:
            with log.open('w',buffering=1) as output:
                os.chmod(log,0o600)
                process=subprocess.Popen(command,cwd=ROOT,stdout=output,stderr=subprocess.STDOUT,start_new_session=True)
                saved.update(worker_pid=process.pid,worker_token=process_token(process.pid))
                atomic_json(root/'fleet-worker.json',saved)
                (root/'worker-pid').write_text(str(process.pid)+'\n')
                (root/'started-at').write_text(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+'\n')
                for name in ('exit-code','finished-at'):(root/name).unlink(missing_ok=True)
                position=0;stopping=None
                while True:
                    with log.open() as incoming:
                        incoming.seek(position);text=incoming.read();position=incoming.tell()
                    if text:print(text,end='',flush=True)
                    code=process.poll()
                    if code is not None:break
                    if stop.is_set() and stopping is None:
                        process.send_signal(signal.SIGTERM);stopping=time.monotonic()
                        print('Stopping at the worker checkpoint…',flush=True)
                    if stopping is not None and time.monotonic()-stopping>=60:
                        # Only this launcher's owned process group, after checkpoint grace.
                        try:os.killpg(process.pid,signal.SIGKILL)
                        except ProcessLookupError:pass
                    time.sleep(.25)
                with log.open() as incoming:
                    incoming.seek(position);remaining=incoming.read()
                if remaining:print(remaining,end='',flush=True)
                saved.update(finished_at=time.time(),exit_code=code,stop_requested=stop.is_set())
                atomic_json(root/'fleet-worker.json',saved)
                (root/'exit-code').write_text(str(code)+'\n')
                (root/'finished-at').write_text(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+'\n')
                print('\nWorker exited ('+str(code)+'). Start it again to resume.',flush=True)
                return code
        finally:
            if process is not None and process.poll() is None:
                # Preserve checkpoints if the supervisor itself encounters an error.
                process.terminate()
                try:process.wait(timeout=60)
                except subprocess.TimeoutExpired:
                    try:os.killpg(process.pid,signal.SIGKILL)
                    except ProcessLookupError:pass
                    process.wait()
            for sig,handler in original.items():signal.signal(sig,handler)


def stop_workers(workers):
    for worker in workers:
        saved=read_json(worker['supervision']/'fleet-worker.json')
        if supervisor_running(worker):
            os.kill(saved['pid'],signal.SIGTERM);print(worker['id']+': checkpoint stop requested')
        elif capture_running(worker):
            print(worker['id']+': running outside this launcher; use its existing supervisor to stop')
        else:print(worker['id']+': stopped')


def tail(path, size=12000):
    try:
        with Path(path).open('rb') as stream:
            stream.seek(max(0,os.fstat(stream.fileno()).st_size-size))
            return stream.read().decode('utf-8',errors='replace')
    except OSError:return ''


def queue_wait_status(worker, runtime, running, text):
    saved=read_json(worker['state_dir']/'selection/queue-wait.json')
    if saved.get('tasks') and saved.get('worker_pid') and saved.get('process_token'):
        if running:
            if process_token(saved['worker_pid'])==saved['process_token']:
                return saved
        elif (saved['worker_pid']==runtime.get('worker_pid') and
              saved.get('observed_at',0)>=runtime.get('started_at',0)):
            return saved
    # Older stopped runs have no explicit wait record. Only attest a queue
    # wait from its log and saved queue; never infer a live hang from log age.
    if not running and not saved:
        wait=text.rfind('Queued work is awaiting recovery; keeping the worker available')
        if wait>=0 and text.rfind('Selected ')<wait and text.rfind('Resuming ')<wait:
            queue=read_json(worker['state_dir']/'selection/queue.json')
            if queue.get('queue') and queue.get('selected') is None:
                from queue_wait import waiting_tasks
                return {'tasks':waiting_tasks(worker['output'],queue['queue']), 'evidence':'saved queue and shutdown log'}
    return {}


def worker_status(worker):
    runtime=read_json(worker['supervision']/'fleet-worker.json');auth=read_json(worker['auth_file'])
    running=capture_running(worker) or supervisor_running(worker)
    status=('RUNNING' if running else 'NOT CONFIGURED' if not ready(worker) else
            'EXIT '+str(runtime['exit_code']) if runtime.get('exit_code') else 'READY')
    sources=list(worker['output'].glob('*/state.json'))
    source=max(sources,key=lambda p:p.stat().st_mtime) if sources else None
    state=read_json(source) if source else {}
    if not running and ready(worker) and not runtime.get('exit_code'):
        if state.get('activity_complete') and not state.get('history_complete'):
            status='HISTORY PENDING'
        elif state.get('history_complete') and (state.get('import_deferred') or state.get('deferred_error',{}).get('phase')=='import'):
            status='IMPORT PENDING'
        elif state.get('activity_complete') and state.get('history_complete'):
            status='COMPLETE'
    records=list(state.get('questions',{}).values())
    graded=sum(bool(q.get('actual_result') or q.get('finalized')) for q in records)
    task=(str(state.get('task_type','activity'))+' '+str(state['task_id'])) if state else 'No activity yet'
    if state.get('deferred_error') and not running:task+=' (deferred)'
    log=runtime.get('log')
    if not log:
        logs=list((worker['state_dir']/'logs').glob('run-*.log'))
        if logs:log=str(max(logs,key=lambda p:p.stat().st_mtime))
    text=tail(log) if log else ''
    if not running and (runtime.get('stop_requested') or
                        runtime.get('exit_code') and 'KeyboardInterrupt: Stopped' in text):
        status='STOPPED'
    queue_wait=queue_wait_status(worker,runtime,running,text)
    if running and queue_wait:status='BLOCKED'
    recent=next((s for s in reversed(text.splitlines()) if s.strip()),'')
    if status in ('IMPORT PENDING','HISTORY PENDING'):recent=state.get('deferred_error',{}).get('message',recent)
    age=time.time()-Path(log).stat().st_mtime if log and Path(log).exists() else None
    stats=read_json(worker['state_dir']/'dashboard.json')
    from dashboard import local_date, activity_counts, import_totals
    xp=stats.get('daily_xp',{})
    if xp.get('date')!=local_date():xp={}
    ledger=read_json(worker['state_dir']/'daily-xp.json').get(local_date(),{})
    recent_activities=stats.get('recent_activities')
    if recent_activities is None:
        recent_activities=[{'task_id':mid,'date':date,**task} for date,tasks in sorted(read_json(worker['state_dir']/'daily-xp.json').items())
                for mid,task in reversed(list(tasks.items()))][-20:]
    if state.get('activity_complete') and not state.get('history_complete'):detail='Saving explanations'
    elif state.get('import_deferred'):detail='Capture saved · import deferred'
    elif state.get('history_complete') and not state.get('import_complete'):detail='Importing capture'
    elif state.get('import_complete'):detail=state.get('task_type','Activity').capitalize()+' complete'
    else:detail='Capturing '+state.get('task_type','activity') if state else 'No activity yet'
    if queue_wait:detail=str(len(queue_wait['tasks']))+' queued activities await recovery'
    if not running and status=='STOPPED':
        from answer_policy import recovery_available
        resumable = sum(recovery_available(Path(read_json(worker['output']/str(task['task_id'])/'state.json')
            .get('deferred_error', {}).get('diagnostics', ''))/'error.json') for task in queue_wait.get('tasks', []))
        detail=('Stopped · '+str(len(queue_wait['tasks']))+' queued activities blocked'
                if queue_wait else 'Stopped · checkpoints retained')
        if resumable:
            detail='Stopped · '+str(resumable)+' queued activities ready for best-effort recovery'
    return {'worker':worker['id'],'window':worker['window'],'account':auth.get('username','—'),
            'status':status,'process_running':running,'queue_wait':queue_wait,
            'activity':task,'questions':str(graded)+'/'+str(len(records))+' graded',
            'uptime':int(time.time()-runtime['started_at']) if running and runtime.get('started_at') else None,
            'log_age':int(age) if age is not None else None,'recent':recent,'log':log,
            'daily_xp':xp,'percent_complete':stats.get('percent_complete'),
            'activity_counts':activity_counts(ledger.values()),'recent_activities':recent_activities,
            'database_questions':import_totals(worker['state_dir']),'detail':detail,
            'capture_only':'--capture-only' in runtime.get('command',[]),
            'stats_observed_at':stats.get('observed_at')}


def progress_line(row):
    xp=row.get('daily_xp',{})
    points=str(xp['earned'])+'/'+str(xp['base']) if xp else '—/—'
    percent=row.get('percent_complete')
    if percent is None:completion='—% [??????????]'
    else:
        filled=max(0,min(10,int(percent/10)))
        completion=f'{percent:g}% ['+'#'*filled+'-'*(10-filled)+']'
    return '  Today '+points+' XP  |  Course '+completion


def render(rows, *, compact=False, color=False):
    if compact:
        counts={kind:sum(r['status']==kind for r in rows) for kind in ('RUNNING','READY','NOT CONFIGURED','BLOCKED','STOPPED')}
        result='MA '+str(counts['RUNNING'])+' running / '+str(counts['READY'])+' ready / '+str(counts['NOT CONFIGURED'])+' unset'
        for status in ('BLOCKED','STOPPED'):
            if counts[status]:result+=' / '+str(counts[status])+' '+status.lower()
        return result
    from terminal_monitor import render as cards
    return cards(rows,shutil.get_terminal_size().columns,color=color)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,default=CONFIG)
    subs=parser.add_subparsers(dest='command',required=True)
    for name in ('start','stop','check','status','attach','layout','dashboard','worker','save-profile'):
        sub=subs.add_parser(name);sub.add_argument('workers',nargs='*')
        if name in ('start','worker'):
            sub.add_argument('--dry-run',action='store_true');sub.add_argument('--limit',type=int)
            sub.add_argument('--capture-only',action='store_true',default=None)
        if name=='start':sub.add_argument('--attach',action='store_true')
        if name=='status':sub.add_argument('--compact',action='store_true');sub.add_argument('--json',action='store_true')
        if name=='save-profile':sub.add_argument('--browser-spec',required=True)
    args=parser.parse_args(argv)
    try:data=config(args.config);workers=selected(data,args.workers)
    except ValueError as error:parser.error(str(error))
    if getattr(args,'limit',None) is not None and args.limit<1:
        parser.error('--limit must be positive')
    if args.command in ('save-profile','worker') and len(workers)!=1:
        parser.error(args.command+' requires one worker name')
    try:
        if args.command=='start':
            start(data,workers,dry_run=args.dry_run,limit=args.limit,capture_only=args.capture_only)
            if args.attach:os.execvp('tmux',['tmux','attach-session','-t',data['session']])
        elif args.command=='layout':ensure_layout(data)
        elif args.command=='attach':os.execvp('tmux',['tmux','attach-session','-t',data['session']])
        elif args.command=='stop':stop_workers(workers)
        elif args.command in ('check','save-profile'):
            for worker in workers:
                if args.command=='check' and not (worker['profile']/'Default/Cookies').exists():
                    print(worker['id']+': not configured');continue
                save_profile(worker,getattr(args,'browser_spec',None))
        elif args.command=='worker':return run_worker(data,workers[0],dry_run=args.dry_run,limit=args.limit,capture_only=args.capture_only)
        elif args.command=='status':
            rows=[worker_status(w) for w in workers]
            print(json.dumps(rows,indent=2) if args.json else render(rows,compact=args.compact,color=sys.stdout.isatty()))
        elif args.command=='dashboard':
            while True:
                print('\033[?25l\033[H'+render([worker_status(w) for w in workers],color=True)+'\033[J',end='',flush=True)
                time.sleep(5)
    except (Exception,KeyboardInterrupt) as error:
        print(type(error).__name__+': '+str(error),file=sys.stderr);return 1
    return 0


if __name__=='__main__':raise SystemExit(main())
