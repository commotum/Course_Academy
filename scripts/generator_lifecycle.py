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


def begin_launch(path, execution, environment):
    """Serialize launch admission with controlled stop, before spending budget."""
    path = Path(path).resolve()
    execution = {**execution, 'launch_id': os.urandom(16).hex()}
    owner_name = environment.get(OWNER_ENV)
    if not owner_name:
        save(path, execution)
        return execution
    owner = Path(owner_name).resolve()
    with locked(owner):
        identity = read(owner / 'owner.json')
        if not path.parent.is_relative_to(Path(identity['pipeline'])):
            raise ValueError('Agent session is outside its owning pipeline')
        if (owner / 'stopped.json').exists():
            raise ControlledServiceStop()
        execution.update(service_owner=str(owner), owner_id=identity['owner_id'])
        identity['sessions'][str(path.parent)] = execution['launch_id']
        save(owner / 'owner.json', identity)
        save(path, execution)
        return execution


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
            if (directory / 'result.json').exists():
                continue
            try:
                execution = read(directory / 'execution.json')
            except (OSError, ValueError):
                continue
            if (execution.get('status') == 'running'
                    and execution.get('owner_id') == identity['owner_id']
                    and execution.get('launch_id') == launch_id):
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
    if not owner_name or execution.get('status') != 'running' or (path.parent / 'result.json').exists():
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
