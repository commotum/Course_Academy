"""tmux windows and resumable per-account supervision for the new capture."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
import fcntl
import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys
import threading
import time

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = 'scripts'

from .config import Config
from .fleet import ACCOUNTS
from .monitor import process_running, render, snapshot
from .runtime import shutdown_signals
from .storage import atomic_json, file_lock, read_json

WINDOWS = dict(zip(ACCOUNTS, ('Mathematical Methods', 'Linear Algebra', 'Multivariable Calculus', 'Differential Equations')))
SCRIPT = Path(__file__).resolve()


def tmux(*args, check=True):
    result = subprocess.run(['tmux', *map(str, args)], capture_output=True, text=True)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or 'tmux command failed')
    return result


def config_for(args, account):
    return Config.from_file(args.config, account=account, capture_only=args.capture_only,
                            headless=False if args.visible else None, learner_id=args.learner_id)


def options(args):
    result = ['--session', args.session]
    if args.config:
        result += ['--config', str(args.config.resolve())]
    if args.capture_only:
        result += ['--capture-only']
    if args.visible:
        result += ['--visible']
    if args.learner_id:
        result += ['--learner-id', args.learner_id]
    return result


def invocation(args, command, *extra):
    return shlex.join([sys.executable, str(SCRIPT), command, *extra, *options(args)])


def child_command(args, account):
    command = [sys.executable, '-u', str(SCRIPT.parent), 'inspect' if args.dry_run else 'run', '--account', account]
    forwarded = options(args)[2:]  # Session names are only for the terminal UI.
    return command + forwarded


def ensure_layout(args):
    session = args.session
    repo = config_for(args, ACCOUNTS[0]).repo_root
    if tmux('has-session', '-t', '=' + session, check=False).returncode:
        tmux('new-session', '-d', '-s', session, '-n', WINDOWS[ACCOUNTS[0]], '-c', repo, 'exec bash')
        tmux('set-option', '-t', session, '@capture_version', '2')
    elif tmux('show-options', '-v', '-t', session, '@capture_version', check=False).stdout.strip() != '2':
        raise RuntimeError(f'Session {session!r} belongs to another program; use a different --session')
    rows = tmux('list-windows', '-t', session, '-F', '#{window_id}\t#{window_name}').stdout.splitlines()
    windows = {name: wid for wid, name in (row.split('\t', 1) for row in rows)}
    panes = {}
    for account, name in WINDOWS.items():
        if name not in windows:
            windows[name] = tmux('new-window', '-d', '-P', '-F', '#{window_id}', '-t', session,
                                 '-n', name, '-c', repo, 'exec bash').stdout.strip()
        window = windows[name]
        tmux('set-window-option', '-t', window, 'automatic-rename', 'off')
        tmux('set-window-option', '-t', window, 'remain-on-exit', 'on')
        rows = tmux('list-panes', '-t', window, '-F', '#{pane_id}\t#{@capture_dashboard}').stdout.splitlines()
        candidates = [row.split('\t')[0] for row in rows if not row.endswith('\t1')]
        if len(candidates) != 1:
            raise RuntimeError(f'{name}: expected one capture log pane; leave other panes untouched')
        panes[account] = candidates[0]
    first = windows[WINDOWS[ACCOUNTS[0]]]
    rows = tmux('list-panes', '-t', first, '-F', '#{pane_id}\t#{@capture_dashboard}\t#{pane_dead}').stdout.splitlines()
    dashboard = next((row.split('\t') for row in rows if row.split('\t')[1] == '1'), None)
    if dashboard is None:
        pane = tmux('split-window', '-d', '-b', '-v', '-l', '18', '-P', '-F', '#{pane_id}',
                    '-t', first, '-c', repo, invocation(args, 'dashboard')).stdout.strip()
        tmux('set-option', '-p', '-t', pane, '@capture_dashboard', '1')
    elif dashboard[2] == '1':
        tmux('respawn-pane', '-t', dashboard[0], invocation(args, 'dashboard'))
    tmux('set-option', '-t', session, 'status-interval', '5')
    tmux('set-option', '-t', session, 'status-right-length', '65')
    tmux('set-option', '-t', session, 'status-right', '#(' + invocation(args, 'status', '--compact') + ')')
    return panes


def profile_busy(config):
    """Detect an existing old/new owner without taking its browser profile."""
    with ExitStack() as stack:
        for path in {config.state_root / 'capture.lock', config.profile.parent / 'capture.lock'}:
            if not path.exists():
                continue
            stream = stack.enter_context(path.open('r'))
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return True
    return False


def start(args, accounts):
    config = config_for(args, accounts[0])
    with file_lock(config.repo_root / '.local/capture/terminal.lock'):
        panes = ensure_layout(args)
        for account in accounts:
            config = config_for(args, account)
            if process_running(read_json(config.state_root / 'worker.json', {})):
                print(f'{account}: already running')
                continue
            if profile_busy(config):
                print(f'{account}: an existing worker owns this profile; no duplicate started')
                continue
            if not config.profile.is_dir():
                print(f'{account}: browser profile is missing: {config.profile}')
                continue
            pane = panes[account]
            state = tmux('display-message', '-p', '-t', pane, '#{pane_dead}\t#{pane_current_command}').stdout.strip().split('\t')
            if state[0] != '1' and state[1] not in ('bash', 'sh'):
                print(f'{account}: log pane is busy; leaving it running')
                continue
            extra = ['--dry-run'] if args.dry_run else []
            tmux('respawn-pane', '-k', '-t', pane, '-c', config.repo_root, invocation(args, 'worker', account, *extra))
            print(f'{account}: starting new capture' + (' (queue inspection only)' if args.dry_run else ''))


def process_token(pid):
    try:
        return Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[19]
    except (OSError, IndexError):
        return None


def cleanup_group(pid, grace=2):
    """Retire descendants of an exited capture before reusing its profile."""
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    deadline = time.monotonic() + grace
    while time.monotonic() < deadline:
        try:
            os.killpg(pid, 0)
        except ProcessLookupError:
            return
        time.sleep(.05)
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def supervise(args, account):
    config = config_for(args, account)
    stop = threading.Event()
    record_path = config.state_root / 'worker.json'
    with file_lock(config.state_root / 'supervisor.lock', blocking=False), shutdown_signals(stop):
        log_path = config.state_root / 'console.log'
        record = {'pid': os.getpid(), 'process_token': process_token(os.getpid()), 'started_at': time.time(),
                  'account': account, 'log': str(log_path), 'command': child_command(args, account), 'restarts': 0}
        atomic_json(record_path, record)
        child = None
        try:
            with log_path.open('a+', buffering=1) as output:
                output.seek(0, os.SEEK_END)
                position = output.tell()
                while not stop.is_set():
                    print(f'{WINDOWS[account]}: new capture starting; checkpoint recovery enabled', flush=True)
                    try:
                        child = subprocess.Popen(record['command'], cwd=config.repo_root, stdout=output,
                                                 stderr=subprocess.STDOUT, start_new_session=True)
                    except OSError as error:
                        record['error'] = str(error)
                        atomic_json(record_path, record)
                        print(f'Launch failed: {error}; retrying in five seconds.', flush=True)
                        stop.wait(5)
                        continue
                    record.pop('exit_code', None)
                    record.pop('error', None)
                    record.update(child_pid=child.pid, child_token=process_token(child.pid))
                    atomic_json(record_path, record)
                    stopping_at = None
                    while True:
                        with log_path.open() as incoming:
                            incoming.seek(position)
                            text = incoming.read()
                            position = incoming.tell()
                        if text:
                            print(text, end='', flush=True)
                        if child.poll() is not None:
                            with log_path.open() as incoming:
                                incoming.seek(position)
                                print(incoming.read(), end='', flush=True)
                                position = incoming.tell()
                            break
                        if stop.is_set() and stopping_at is None:
                            # Signal the capture first so it can save its checkpoint.
                            child.terminate()
                            stopping_at = time.monotonic()
                        if stopping_at is not None and time.monotonic() - stopping_at >= 60:
                            os.killpg(child.pid, signal.SIGKILL)
                        time.sleep(.25)
                    cleanup_group(child.pid)
                    record.update(exit_code=child.returncode)
                    atomic_json(record_path, record)
                    if stop.is_set() or args.dry_run:
                        return child.returncode
                    record['restarts'] += 1
                    print(f'Capture exited ({child.returncode}); resuming from its checkpoint in five seconds.', flush=True)
                    stop.wait(5)
        finally:
            if child is not None and child.poll() is None:
                child.terminate()
                try:
                    child.wait(timeout=60)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
            # Clean up only this supervisor's own remaining child processes.
            if child is not None:
                cleanup_group(child.pid)
            record.update(finished_at=time.time(), stop_requested=stop.is_set())
            atomic_json(record_path, record)
    return 0


def stop_workers(args, accounts):
    for account in accounts:
        config = config_for(args, account)
        record = read_json(config.state_root / 'worker.json', {})
        if process_running(record):
            os.kill(record['pid'], signal.SIGTERM)
            print(f'{account}: checkpoint stop requested')
        elif profile_busy(config):
            print(f'{account}: running outside this launcher; use its original supervisor to stop it')
        else:
            print(f'{account}: stopped')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('start', 'stop', 'status', 'attach', 'layout', 'dashboard', 'worker', 'check'))
    parser.add_argument('workers', nargs='*', help='Account names; defaults to all four')
    parser.add_argument('--session', default='ma-capture')
    parser.add_argument('--config', type=Path, help='Shared new capture configuration (not old workers.json)')
    parser.add_argument('--attach', action='store_true')
    parser.add_argument('--capture-only', action='store_true', default=None)
    parser.add_argument('--visible', action='store_true')
    parser.add_argument('--learner-id')
    parser.add_argument('--dry-run', action='store_true', help='Inspect the queue without starting activities')
    parser.add_argument('--compact', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_intermixed_args(argv)
    accounts = list(dict.fromkeys(args.workers or ACCOUNTS))
    if set(accounts) - set(ACCOUNTS):
        parser.error('Accounts: ' + ', '.join(ACCOUNTS))
    if not args.session or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_' for c in args.session):
        parser.error('Session name must contain only letters, digits, hyphens, or underscores')
    if args.command == 'worker' and len(accounts) != 1:
        parser.error('worker requires one account')
    saved = read_json(args.config, {}) if args.config else {}
    if any(saved.get(key) for key in ('account', 'profile', 'state_root', 'output_root', 'course_id', 'browser_cdp_url')):
        parser.error('tmux uses separate standard account paths; use capture/scripts run for account-specific configuration')
    try:
        if args.command == 'start':
            start(args, accounts)
        elif args.command == 'layout':
            ensure_layout(args)
        elif args.command == 'worker':
            return supervise(args, accounts[0])
        elif args.command == 'stop':
            stop_workers(args, accounts)
        elif args.command == 'check':
            from .cli import main as capture_main
            return max(capture_main(['check', '--account', account, *options(args)[2:]]) for account in accounts)
        elif args.command == 'status':
            rows = [snapshot(config_for(args, account)) for account in accounts]
            print(json.dumps(rows, indent=2) if args.json else render(rows, compact=args.compact, color=sys.stdout.isatty()))
        elif args.command == 'dashboard':
            try:
                while True:
                    print('\033[?25l\033[H' + render([snapshot(config_for(args, account)) for account in accounts], color=True) + '\033[J', end='', flush=True)
                    time.sleep(5)
            finally:
                print('\033[?25h', end='', flush=True)
        if args.command == 'attach' or (args.command == 'start' and args.attach):
            verb = 'switch-client' if os.environ.get('TMUX') else 'attach-session'
            os.execvp('tmux', ['tmux', verb, '-t', args.session])
    except KeyboardInterrupt:
        return 0
    except Exception as error:
        print(f'{type(error).__name__}: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
