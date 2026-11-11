#!/usr/bin/env python3
"""Start, inspect, or gracefully stop the detached generator."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import fcntl
import json
import math
import os
from pathlib import Path
import signal
import socket
import socketserver
import subprocess
import sys
import threading
import time
import traceback
import uuid

from generator_lifecycle import process_identity
from inventory_jobs import InventoryJobs, save

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.local/generator'
UNIT = 'course-academy-generator.service'
CONTROL_ENV = 'COURSE_ACADEMY_GENERATOR_CONTROL_SOCKET'
SERVICE_ENV = {'PATH', 'CODEX_HOME', 'LEARNING_REQUEST_DIR',
               'COURSE_ACADEMY_CODEX_EXECUTABLE', 'COURSE_ACADEMY_GENERATOR_PYTHON',
               'COURSE_ACADEMY_GENERATOR_REVIEW_WORKERS'}


def policy(remaining, reserve, workers):
    """Percentage-point margins; active turns are never cancelled to shrink."""
    margin = remaining - reserve
    if margin <= 0:
        return 0, 300
    if margin <= 5:
        return 1, 300
    if margin <= 10:
        return max(1, math.ceil(workers / 2)), 900
    return workers, 1800


def usage_failure(path, offset=0):
    """Read only structured errors from this launch, never tool-output text."""
    with Path(path).open('rb') as stream:
        if type(offset) is not int or not 0 <= offset <= os.fstat(stream.fileno()).st_size:
            raise ValueError('Invalid agent event offset')
        stream.seek(offset)
        for line in stream:
            try:
                row = json.loads(line)
            except (ValueError, UnicodeDecodeError):
                continue
            if not isinstance(row, dict) or row.get('type') not in {'error', 'turn.failed'}:
                continue
            error = row.get('error', row)
            if not isinstance(error, dict):
                continue
            code = str(error.get('code', '')).lower()
            message = str(error.get('message', '')).lower().replace('’', "'")
            if (code in {'usage_limit_reached', 'quota_exceeded', 'insufficient_quota'}
                    or "you've hit your usage limit" in message
                    or 'usage limit has been reached' in message
                    or 'exceeded your current quota' in message):
                return True
    return False


def request(socket_path, payload, timeout=5):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.settimeout(timeout)
        client.connect(str(socket_path))
        client.sendall(json.dumps(payload).encode() + b'\n')
        with client.makefile('rb') as stream:
            return json.loads(stream.readline(65537))


def read_status(runtime=RUNTIME):
    try:
        value = json.loads((runtime / 'run.json').read_text())
    except FileNotFoundError:
        return {'state': 'stopped', 'reason': 'not started'}
    observed = process_identity(value.get('pid'))
    alive = bool(observed and observed['start_ticks'] == value.get('start_ticks')
                 and observed['state'] not in {'Z', 'X'})
    if value.get('state') != 'stopped' and not alive:
        value = {**value, 'state': 'stopped', 'reason': 'supervisor exited unexpectedly'}
    elif value.get('state') == 'stopped' and alive:
        value = {**value, 'state': 'draining', 'reason': 'finishing shutdown', 'finishing': True}
    return value


def print_status(value):
    state = value.get('state', 'unknown')
    detail = f"Generator {state}"
    if state != 'stopped':
        detail += (f" — {value.get('active_turns', 0)} active turns; "
                   f"{value.get('allowed_workers', 0)}/{value.get('workers', 6)} workers allowed")
    if value.get('reason'):
        detail += ' — ' + value['reason']
    print(detail + '.')
    quota = value.get('quota')
    if quota:
        print(f"Quota: {quota['remaining_percent']:g}% remaining; reserve {value['until']:g}%.")
        if value.get('next_poll') and state not in {'draining', 'stopped'}:
            print('Next quota check: ' + time.strftime('%H:%M:%S', time.localtime(value['next_poll'])) + '.')
    if state != 'stopped':
        print('Status: uv run gen -s   Stop: uv run gen -k')


def live_status(*, stop=False):
    """An exit between the status read and socket request is still success."""
    value = read_status()
    if value['state'] == 'stopped' or value.get('finishing'):
        return value
    try:
        return request(RUNTIME / 'control.sock', {'event': 'stop' if stop else 'status'})
    except (OSError, ValueError):
        observed = read_status()
        if observed['state'] != 'stopped' and not observed.get('finishing'):
            raise
        return observed


class ControlServer(socketserver.ThreadingUnixStreamServer):
    daemon_threads = True


class Supervisor:
    def __init__(self, jobs, runtime, workers=6, until=None, *, quota_reader=None, clock=time.time):
        self.jobs, self.runtime = jobs, Path(runtime)
        self.workers, self.until, self.clock = workers, until, clock
        self.quota_reader = quota_reader
        self.lock = threading.RLock()
        self.wake = threading.Event()
        self.ready = threading.Event()
        self.refresh_requested = threading.Event()
        self.closed = threading.Event()
        self.draining = False
        self.reason = None
        self.allowed = 0 if until is not None else workers
        self.quota = None
        self.next_poll = None
        self.tickets = {}
        self.active_jobs = 0
        self.refresh_error = None
        self.started = self.clock()
        self.run_id = uuid.uuid4().hex
        self.developer_mode = lambda: False
        self.server = None

    def state(self):
        with self.lock:
            self.prune_tickets()
            identity = process_identity(os.getpid()) or {}
            return {'state': 'draining' if self.draining else 'running' if self.ready.is_set() else 'starting',
                    'pid': os.getpid(), 'start_ticks': identity.get('start_ticks'),
                    'started_at': self.started, 'updated_at': self.clock(), 'workers': self.workers,
                    'allowed_workers': self.allowed, 'active_turns': len(self.tickets),
                    'active_jobs': self.active_jobs, 'until': self.until,
                    'quota': self.quota, 'next_poll': self.next_poll,
                    'reason': self.reason, 'inventory_error': self.refresh_error}

    def persist(self, **extra):
        with self.lock:
            save(self.runtime / 'run.json', {**self.state(), **extra})

    def drain(self, reason):
        with self.lock:
            if not self.draining:
                self.draining, self.reason, self.allowed = True, reason, 0
                self.persist()
                print('Draining generator: ' + reason, flush=True)
            self.wake.set()

    def prune_tickets(self):
        for ticket, identity in list(self.tickets.items()):
            observed = process_identity(identity['pid'])
            if (not observed or observed['start_ticks'] != identity['start_ticks']
                    or observed['state'] in {'Z', 'X'}):
                del self.tickets[ticket]

    def quota_poll(self):
        if self.until is None or self.draining:
            return
        try:
            snapshot = self.quota_reader()
            remaining = snapshot['remaining_percent']
            if type(remaining) not in (float, int) or not math.isfinite(remaining) or not 0 <= remaining <= 100:
                raise ValueError('Quota response has no usable remaining percentage')
            allowed, seconds = policy(remaining, self.until, self.workers)
            with self.lock:
                self.quota = snapshot
                self.next_poll = self.clock() + seconds
                if not self.draining:
                    self.allowed = allowed
                # Admission also checks next_poll, closing the stale-data gap
                # while a scheduled quota request is in flight.
                if snapshot.get('exhausted') or snapshot.get('ordinary_usage_allowed') is False:
                    self.drain('account quota exhausted')
                elif allowed == 0:
                    self.drain(f'quota reserve reached ({remaining:g}% remaining)')
                self.persist()
        except Exception as error:
            self.drain('quota unavailable: ' + str(error))

    def admission_allowed(self):
        return (not self.draining and self.allowed > 0
                and (self.until is None or self.next_poll is not None and self.clock() < self.next_poll))

    def handle(self, payload):
        event = payload.get('event')
        with self.lock:
            if event == 'status':
                return self.state()
            if event == 'stop':
                self.drain('stop requested')
                return self.state()
            if event == 'admit':
                if self.draining:
                    return {'action': 'halt', 'reason': self.reason}
                self.prune_tickets()
                if self.developer_mode() or not self.admission_allowed() or len(self.tickets) >= self.allowed:
                    return {'action': 'wait'}
                identity = process_identity(payload.get('pid'))
                if not identity or identity['state'] in {'Z', 'X'}:
                    return {'action': 'halt', 'reason': 'worker process is unavailable'}
                ticket = self.run_id + ':' + uuid.uuid4().hex
                self.tickets[ticket] = identity
                self.persist()
                return {'action': 'run', 'ticket': ticket}
            if event == 'complete':
                # Completion may be replayed from an interrupted previous run.
                # Unknown tickets never release someone else's capacity.
                ticket = payload.get('ticket')
                if ticket in self.tickets and payload.get('pid') == self.tickets[ticket]['pid']:
                    del self.tickets[ticket]
                path = Path(payload['events_path']).resolve()
                directory = Path(payload['directory']).resolve()
                if (path != directory / 'events.jsonl'
                        or not path.is_relative_to(self.jobs.directory.resolve())):
                    raise ValueError('Agent evidence is outside the inventory directory')
                if usage_failure(path, payload.get('events_offset', 0)):
                    reason = 'account quota exhausted; start again explicitly when ready'
                    if isinstance(ticket, str) and ticket.startswith(self.run_id + ':'):
                        self.drain(reason)
                    # An old rejection needs its replacement credit, but is
                    # not evidence that this explicitly restarted run is out.
                    return {'action': 'halt', 'reason': reason, 'exempt': True}
                self.persist()
                return {'action': 'continue'}
            raise ValueError('Unknown generator control request')

    def start_server(self):
        supervisor = self
        class Handler(socketserver.StreamRequestHandler):
            def handle(self):
                self.connection.settimeout(5)
                try:
                    data = self.rfile.readline(65537)
                    if len(data) > 65536:
                        raise ValueError('Oversized generator control request')
                    result = supervisor.handle(json.loads(data))
                except Exception as error:
                    supervisor.drain('control error: ' + str(error))
                    result = {'action': 'halt', 'reason': 'parent control failed'}
                self.wfile.write(json.dumps(result).encode() + b'\n')
        path = self.runtime / 'control.sock'
        path.unlink(missing_ok=True)
        self.server = ControlServer(str(path), Handler)
        path.chmod(0o600)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def refresh_loop(self, refresh):
        while not self.closed.is_set() and not self.draining:
            try:
                refresh()
                self.ready.set()
                self.refresh_error = None
            except Exception as error:
                self.refresh_error = str(error)
                print('Inventory refresh deferred: ' + str(error), flush=True)
            self.wake.set()
            self.refresh_requested.wait(30)
            self.refresh_requested.clear()

    def run(self, refresh, *, developer_mode=lambda: False):
        self.developer_mode = developer_mode
        self.runtime.mkdir(parents=True, exist_ok=True)
        self.start_server()
        self.persist()
        # No quota reader or app-server process is touched without -u.
        self.quota_poll()
        if not self.draining:
            threading.Thread(target=self.refresh_loop, args=(refresh,), daemon=True).start()
        futures = {}
        pool = ThreadPoolExecutor(max_workers=self.workers + 1)
        try:
            while True:
                self.wake.clear()
                if not self.draining and self.until is not None and self.clock() >= self.next_poll:
                    self.quota_poll()
                with self.lock:
                    for key, future in list(futures.items()):
                        if future.done():
                            del futures[key]
                            try:
                                if future.result():
                                    self.refresh_requested.set()
                            except Exception:
                                traceback.print_exc()
                                self.drain('worker supervisor failed; inspect the service log')
                    self.active_jobs = len(futures)
                    if self.draining and not futures:
                        break
                    if self.ready.is_set() and self.admission_allowed() and not developer_mode():
                        for slot in range(self.allowed):
                            key = ('build', slot)
                            if key not in futures:
                                futures[key] = pool.submit(self.jobs.run_one, lane='build', slot=slot)
                        if ('refill', 0) not in futures:
                            futures[('refill', 0)] = pool.submit(self.jobs.run_one, lane='refill', slot=0)
                    self.active_jobs = len(futures)
                    self.persist()
                self.wake.wait(2)
        except BaseException:
            self.drain('supervisor error; active turns are finishing')
            raise
        finally:
            self.closed.set()
            self.refresh_requested.set()
            # Leave the control server alive while workers finish and checkpoint.
            pool.shutdown(wait=True)
            self.persist(state='stopped', active_jobs=0, active_turns=0, stopped_at=self.clock())
            self.server.shutdown()
            self.server.server_close()
            (self.runtime / 'control.sock').unlink(missing_ok=True)


def run_daemon(workers, until):
    from serve_graph_explorer import database_environment, DEFAULT_DATABASE, DEFAULT_LEARNER, developer_mode
    RUNTIME.mkdir(parents=True, exist_ok=True)
    with (RUNTIME / 'daemon.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 1
        environment = database_environment(DEFAULT_DATABASE)
        settings = ROOT / '.local/ui.env'
        if settings.exists():
            for line in settings.read_text().splitlines():
                if line.strip() and not line.lstrip().startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    environment[key] = value
        environment.update(os.environ)
        environment.update(COURSE_ACADEMY_GENERATOR_BUILD_WORKERS=str(workers),
                           COURSE_ACADEMY_GENERATOR_REVIEW_WORKERS=str(min(1, workers - 1)),
                           COURSE_ACADEMY_DISABLE_GENERATION='0',
                           COURSE_ACADEMY_GENERATOR_CONTROL_SOCKET=str(RUNTIME / 'control.sock'))
        jobs = InventoryJobs(ROOT, ROOT / '.local/learning/inventory' / DEFAULT_DATABASE / DEFAULT_LEARNER,
                             DEFAULT_LEARNER, environment)
        quota_reader = None
        if until is not None:
            from generator_quota import fetch_quota
            quota_reader = lambda: fetch_quota(environment=environment)
        supervisor = Supervisor(jobs, RUNTIME, workers, until, quota_reader=quota_reader)
        signal.signal(signal.SIGTERM, lambda *_: supervisor.drain('stop requested'))
        signal.signal(signal.SIGINT, lambda *_: supervisor.drain('stop requested'))
        sys.path.insert(0, str(ROOT / 'generate/scripts'))
        from find_candidates import build, discover
        binary = None
        def refresh():
            nonlocal binary
            if binary is None:
                binary = build(Path(environment.get('EDB_ROOT', ROOT.parent / 'EDB')).resolve())
            inventory = discover(DEFAULT_DATABASE, DEFAULT_LEARNER, environment,
                                 binary=binary, include_registered=True)
            jobs.accept(inventory)
        mode = Path(environment['LEARNING_REQUEST_DIR']) / 'developer-mode.json'
        supervisor.run(refresh, developer_mode=lambda: developer_mode(mode))
    return 0


def start(workers, until):
    RUNTIME.mkdir(parents=True, exist_ok=True)
    RUNTIME.chmod(0o700)
    with (RUNTIME / 'cli.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        old = read_status()
        if old['state'] != 'stopped':
            print_status(old)
            return 0
        command = ['systemd-run', '--user', '--quiet', '--collect', '--unit=' + UNIT,
                   '--property=Restart=no', '--property=KillMode=mixed',
                   '--property=TimeoutStopSec=infinity', '--working-directory=' + str(ROOT),
                   # A user service does not otherwise inherit the invoking
                   # shell's configuration. Let systemd-run copy values by name
                   # so database credentials never appear in command arguments.
                   *['--setenv=' + key for key in sorted(os.environ)
                     if key in SERVICE_ENV or key.startswith('EDB_')],
                   *([] if 'PATH' in os.environ else ['--setenv=PATH=' + os.defpath]),
                   sys.executable, '-u', str(Path(__file__).resolve()), '--_serve', '-w', str(workers)]
        if until is not None:
            command += ['-u', str(until)]
        launched = time.time()
        result = subprocess.run(command, capture_output=True, text=True, timeout=15)
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or 'Cannot start the generator user service')
        # Wait only for the parent handshake, not inventory or an agent turn.
        for _ in range(50):
            value = read_status()
            if value.get('started_at', 0) >= launched:
                print_status(value)
                return 0
            time.sleep(.1)
        raise RuntimeError('Generator has not reported startup. Check journalctl --user -u ' + UNIT)


def positive_integer(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError('workers must be positive')
    return number


def percentage(value):
    number = float(value)
    if not math.isfinite(number) or not 0 <= number <= 100:
        raise argparse.ArgumentTypeError('until must be a remaining percentage from 0 to 100')
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, add_help=False,
        epilog='Example: uv run gen -w 6 -u 25. Cutoffs drain active turns; they are not a hard spending cap.')
    parser.add_argument('-h', '--h', '--help', action='help', help='show this help')
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument('-k', '--k', '--stop', dest='stop', action='store_true', help='stop new turns; let active turns finish')
    actions.add_argument('-s', '--s', '--status', dest='status', action='store_true', help='show status without polling quota')
    parser.add_argument('-w', '--w', '--workers', dest='workers', type=positive_integer, default=None, help='maximum agent workers (default: 6)')
    parser.add_argument('-u', '--u', '--until', dest='until', type=percentage, help='stop at this percent quota remaining')
    parser.add_argument('--_serve', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if (args.stop or args.status) and (args.workers is not None or args.until is not None):
        parser.error('-w and -u apply only when starting a run')
    try:
        if args._serve:
            return run_daemon(args.workers or 6, args.until)
        if args.status:
            print_status(live_status())
            return 0
        if args.stop:
            print_status(live_status(stop=True))
            return 0
        return start(args.workers or 6, args.until)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print('gen: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
