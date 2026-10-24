"""Credit only exact agent launches interrupted by their owning UI service."""
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import time

from inventory_jobs import save

OWNER_ENV = 'COURSE_ACADEMY_GENERATOR_SERVICE_OWNER'
INTERRUPTED_EXIT = 75


class ControlledServiceStop(SystemExit):
    def __init__(self):
        super().__init__(INTERRUPTED_EXIT)


def read(path):
    return json.loads(Path(path).read_text())


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def completed_result(directory):
    try:
        read(Path(directory) / 'result.json')
        return True
    except (OSError, ValueError):
        return False


@contextmanager
def locked(owner):
    with (Path(owner) / 'owner.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def create_owner(job, cycle):
    job = Path(job).resolve()
    pipeline = job.with_suffix('.pipeline') / str(cycle)
    identity = os.urandom(16).hex()
    owner = pipeline / 'service-interruptions' / identity
    owner.mkdir(parents=True)
    save(owner / 'owner.json', {'format': 1, 'owner_id': identity,
         'job': str(job), 'cycle': cycle, 'pipeline': str(pipeline),
         'created': time.time(), 'sessions': {}})
    return owner


def process_identity(pid):
    """Linux PID/start-time identity distinguishes exited agents and PID reuse."""
    try:
        fields = Path(f'/proc/{int(pid)}/stat').read_text().rsplit(')', 1)[1].split()
        return {'pid': int(pid), 'start_ticks': fields[19], 'state': fields[0]}
    except (OSError, TypeError, ValueError, IndexError):
        return None


def agent_running(execution):
    expected = execution.get('agent_process')
    if expected is None:
        return False
    observed = process_identity(expected['pid'])
    return bool(observed and observed['start_ticks'] == expected['start_ticks']
                and observed['state'] not in {'Z', 'X'})


def begin_launch(path, execution, environment, spawn):
    """Serialize launch admission with controlled stop, before spending budget."""
    path = Path(path).resolve()
    execution.update(launch_id=os.urandom(16).hex())
    execution.pop('agent_process', None)
    owner_name = environment.get(OWNER_ENV)
    def start(owner=None):
        if owner is not None:
            identity = read(owner / 'owner.json')
            if not path.parent.is_relative_to(Path(identity['pipeline'])):
                raise ValueError('Agent session is outside its owning pipeline')
            if (owner / 'stopped.json').exists():
                raise ControlledServiceStop()
            execution.update(service_owner=str(owner), owner_id=identity['owner_id'])
            identity['sessions'][str(path.parent)] = execution['launch_id']
            save(owner / 'owner.json', identity)
        save(path, execution)
        process = spawn()
        observed = process_identity(process.pid)
        if observed:
            execution['agent_process'] = {k: observed[k] for k in ('pid', 'start_ticks')}
        else:
            execution.pop('agent_process', None)
        save(path, execution)
        return execution, process
    if not owner_name:
        execution.pop('service_owner', None)
        execution.pop('owner_id', None)
        return start()
    with locked(Path(owner_name).resolve()):
        return start(Path(owner_name).resolve())


def finish_launch(path, execution):
    owner = execution.get('service_owner')
    if owner:
        with locked(owner):
            save(path, execution)
    else:
        save(path, execution)


def mark_stopped(owner):
    """Record shutdown evidence without rewriting concurrently owned execution."""
    owner = Path(owner)
    with locked(owner):
        if (owner / 'stopped.json').exists():
            return read(owner / 'stopped.json')
        identity = read(owner / 'owner.json')
        sessions = []
        for directory, launch_id in identity['sessions'].items():
            directory = Path(directory)
            if completed_result(directory):
                continue
            try:
                execution = read(directory / 'execution.json')
            except (OSError, ValueError):
                continue
            if (execution.get('status') == 'running'
                    and execution.get('owner_id') == identity['owner_id']
                    and execution.get('launch_id') == launch_id
                    and agent_running(execution)):
                sessions.append({'directory': str(directory), 'launch_id': launch_id,
                                 'launches': execution['launches'],
                                 'execution_hash': fingerprint(execution)})
        marker = {'format': 1, 'owner_id': identity['owner_id'],
                  'pipeline': identity['pipeline'], 'job': identity['job'],
                  'cycle': identity['cycle'], 'reason': 'controlled-service-stop',
                  'at': time.time(), 'sessions': sessions}
        save(owner / 'stopped.json', marker)
        return marker


def stopped(owner):
    return (Path(owner) / 'stopped.json').exists()


def credit_interruption(path, execution, default_limit):
    """A marked running launch gets one replacement; actual failures never do."""
    path = Path(path).resolve()
    owner_name = execution.get('service_owner')
    if not owner_name or execution.get('status') != 'running' or completed_result(path.parent):
        return execution
    owner = Path(owner_name)
    if not (owner / 'stopped.json').is_file():
        return execution
    with locked(owner):
        marker = read(owner / 'stopped.json')
        identity = read(owner / 'owner.json')
        if (marker.get('reason') != 'controlled-service-stop'
                or marker.get('owner_id') != execution.get('owner_id')
                or marker.get('owner_id') != identity.get('owner_id')
                or marker.get('pipeline') != identity.get('pipeline')
                or not path.parent.is_relative_to(Path(identity['pipeline']))):
            return execution
        launch_id = execution.get('launch_id')
        credits = execution.get('controlled_interruptions', [])
        if any(row.get('launch_id') == launch_id for row in credits):
            return execution
        witness = next((row for row in marker['sessions']
                        if row['directory'] == str(path.parent) and row['launch_id'] == launch_id
                        and row['launches'] == execution['launches']
                        and row['execution_hash'] == fingerprint(execution)), None)
        if witness is None:
            return execution
        execution = {**execution,
                     'launch_limit': execution.get('launch_limit', default_limit) + 1,
                     'controlled_interruptions': [*credits, {**witness, 'marker': str(owner / 'stopped.json'),
                                                           'credited_at': time.time()}]}
        save(path, execution)
        return execution
