#!/usr/bin/env python3
"""One-time, evidence-bound bridge to controlled generator shutdown handling.

snapshot reads live state and writes an audit bundle. apply changes only the
captured launch budgets (plus the two named historical interruption blocks),
while the service is stopped. Neither command controls the service or EDB.
"""
import argparse
import base64
from contextlib import ExitStack
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import uuid

ROOT = Path(__file__).resolve().parents[4]
INVENTORY = ROOT / '.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
SERVICE = 'course-academy.service'
LEGACY = {
    17592186059726: '9eaccc5fcb994b5d09ff9b52af27a373452db684f7f52b7f982c37dc07dd217c',
    17592186059727: '040808a30865dc53206f42f34d2f96c822bd563ad01180644ae365f9c38b8bea',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def packed(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    return {'path': str(path), 'sha256': digest(data), 'bytes': base64.b64encode(data).decode()}


def unpack(item):
    data = base64.b64decode(item['bytes'], validate=True)
    require(digest(data) == item['sha256'], 'Corrupt snapshot: ' + item['path'])
    return data


def atomic_bytes(path, data):
    path = Path(path)
    temporary = path.with_name(path.name + '.recovery-tmp')
    with temporary.open('wb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def save(path, value):
    atomic_bytes(path, (json.dumps(value, indent=2) + '\n').encode())


def service_state():
    output = subprocess.check_output(['systemctl', '--user', 'show', SERVICE,
        '-p', 'ActiveState', '-p', 'SubState', '-p', 'MainPID', '-p', 'ControlGroup', '-p', 'InvocationID'], text=True)
    return dict(line.split('=', 1) for line in output.splitlines() if '=' in line)


def process(pid):
    path = Path('/proc') / str(pid)
    try:
        fields = (path / 'stat').read_text().rsplit(')', 1)[1].split()
        return {'pid': int(pid), 'ppid': int(fields[1]), 'start_ticks': fields[19], 'state': fields[0],
                'uid': path.stat().st_uid,
                'argv': (path / 'cmdline').read_bytes().decode().rstrip('\0').split('\0'),
                'cgroups': [line.split(':', 2)[2] for line in (path / 'cgroup').read_text().splitlines()]}
    except (OSError, ValueError, IndexError):
        return None


def processes():
    return [row for name in os.listdir('/proc') if name.isdigit() and (row := process(name))]


def owned(row, service):
    group = service['ControlGroup']
    return bool(group and row['uid'] == os.getuid() and
                any(value == group or value.startswith(group + '/') for value in row['cgroups']))


def argument(argv, flag):
    return argv[argv.index(flag) + 1]


def journal(since, until=None):
    command = ['journalctl', '--user', '-u', SERVICE, '--since', since, '--no-pager', '-o', 'json']
    if until:
        command += ['--until', until]
    rows = []
    for line in subprocess.check_output(command, text=True).splitlines():
        row = json.loads(line)
        message = row.get('MESSAGE', '')
        if (any(word in message for word in ('Stopping ' + SERVICE, 'Stopped ' + SERVICE,
                                            'Started ' + SERVICE, 'Killing process '))
                or '"event": "generator_blocked"' in message):
            rows.append({'at': int(row['__REALTIME_TIMESTAMP']) / 1000000, 'message': message})
    return rows


def capture(job_path, session):
    job_path, session = Path(job_path).resolve(), Path(session).resolve()
    require(job_path.parent == INVENTORY, 'Wrong inventory root')
    job = read(job_path)
    pipeline = job_path.with_suffix('.pipeline') / str(job['cycle'])
    require(session.is_relative_to(pipeline), 'Session outside captured pipeline')
    require(not (pipeline / 'publication/request.json').exists(), 'Pending publication intent: ' + str(pipeline))
    require(not (session / 'result.json').exists(), 'Session has a completed result')
    execution = read(session / 'execution.json')
    require(execution.get('status') == 'running', 'Session is not interrupted/running')
    require(not execution.get('service_owner'), 'Protected launch must use normal lifecycle credit')
    require(type(execution.get('launches')) is int and execution['launches'] > 0, 'Invalid launch count')
    return {'job': packed(job_path), 'pipeline': packed(pipeline / 'job.json'),
            'execution': packed(session / 'execution.json'), 'session': str(session),
            'knowledge_point': job['request']['knowledgePoint'], 'cycle': job['cycle']}


def historical_proof(entry, rows):
    job = json.loads(unpack(entry['job']))
    state = json.loads(unpack(entry['pipeline']))
    execution = json.loads(unpack(entry['execution']))
    kp = entry['knowledge_point']
    require(LEGACY.get(kp) == Path(entry['job']['path']).stem, 'Historical recovery is not allowlisted')
    require(entry['cycle'] == 2 and Path(entry['session']).name == 'author-1', 'Unexpected historical attempt')
    require(job['state'] == state['stage'] == 'blocked' and state['attempt'] == 1
            and state.get('author_running') is True and state['author_attempt_limit'] == 3
            and not state.get('review_sessions'), 'Historical logical attempt changed')
    error = state.get('error', {})
    cause = error.get('cause', {})
    require(error.get('code') == cause.get('code') == 'agent_session_retry_exhausted'
            and error.get('resume_stage') == 'generate' and cause.get('role') == 'author'
            and cause.get('session_directory') == entry['session'] and cause.get('launches') == 3
            and cause.get('error') == 'Session was interrupted'
            and job.get('outcome', {}).get('reason') == error, 'Not the exact interruption-only block')
    require(execution == {'launches': 3, 'status': 'running'}, 'Historical execution changed')
    events = [json.loads(line) for line in (Path(entry['session']) / 'events.jsonl').read_text().splitlines()]
    starts = [uuid.UUID(event['thread_id']).int >> 80 for event in events if event.get('type') == 'thread.started']
    require(len(starts) == 3 and not any(event.get('type') in ('turn.completed', 'turn.failed', 'error')
                                       for event in events), 'Historical session has terminal or unexpected turns')
    starts = [value / 1000 for value in starts]
    stops = [row['at'] for row in rows if row['message'].startswith('Stopped ' + SERVICE)]
    ends = [*starts[1:], job['completedAt']]
    require(all(any(start < stop < end for stop in stops) for start, end in zip(starts, ends)),
            'No service stop between each unfinished historical launch')
    blocked = [row for row in rows if '"event": "generator_blocked"' in row['message']
               and str(kp) in row['message'] and str(Path(entry['job']['path'])) in row['message']]
    require(blocked, 'Missing journal record of this exact blocked job')
    return {'kind': 'historical-convergent-evidence', 'pid_proof_available': False,
            'thread_start_times': starts, 'service_stop_times': stops, 'block_records': blocked,
            'authorization': 'Explicitly scoped one-launch recovery of these two interruption-only blocks.'}


def snapshot(output):
    output = Path(output).resolve()
    require(not output.exists(), 'Use a new snapshot directory')
    state = service_state()
    require(state['ActiveState'] == 'active' and state['SubState'] == 'running', 'Service is not running')
    main = process(int(state['MainPID']))
    require(main and owned(main, state), 'Cannot prove service main-process ownership')
    at = time.time()
    all_processes = processes()
    entries, skipped = [], []
    for worker in all_processes:
        if not owned(worker, state) or str(ROOT / 'scripts/generator_pipeline.py') not in worker['argv']:
            continue
        if '--inventory-job' not in worker['argv']:
            continue
        children = [row for row in all_processes if row['ppid'] == worker['pid'] and owned(row, state)
                    and 'exec' in row['argv'] and '--output-last-message' in row['argv']]
        if not children:
            skipped.append({'pipeline_pid': worker['pid'], 'reason': 'No live direct Codex child; no launch credited'})
            continue
        require(len(children) == 1, 'Ambiguous live agent ownership')
        child = children[0]
        session = Path(argument(child['argv'], '--output-last-message')).resolve().parent
        entry = capture(argument(worker['argv'], '--inventory-job'), session)
        require(str(entry['cycle']) == argument(worker['argv'], '--inventory-cycle'), 'Worker cycle mismatch')
        require(json.loads(unpack(entry['job']))['state'] == 'running', 'Worker job is not running')
        for before in (worker, child):
            after = process(before['pid'])
            require(after and after['start_ticks'] == before['start_ticks'] and owned(after, state),
                    'Process changed during capture; take another snapshot')
        require(Path(entry['execution']['path']).read_bytes() == unpack(entry['execution']), 'Launch changed during capture')
        entries.append({**entry, 'kind': 'live', 'pipeline_process': worker, 'agent_process': child})
    history = journal('2026-10-24 18:16:00 UTC', '2026-10-24 18:31:00 UTC')
    for kp, key in LEGACY.items():
        entry = capture(INVENTORY / (key + '.json'), INVENTORY / (key + '.pipeline/2/author-1'))
        entries.append({**entry, 'kind': 'historical', 'proof': historical_proof(entry, history)})
    require(service_state() == state, 'Service changed during snapshot')
    output.mkdir(mode=0o700, parents=True)
    for index, entry in enumerate(entries):
        archive = output / f'entry-{index}'
        archive.mkdir()
        for name in ('events.jsonl', 'prompt.txt'):
            path = Path(entry['session']) / name
            if path.exists():
                (archive / name).write_bytes(path.read_bytes())
        entry['archive'] = str(archive)
    manifest = {'format': 1, 'created': at, 'service': state, 'main_process': main,
                'helper_sha256': digest(Path(__file__).read_bytes()), 'inventory': str(INVENTORY),
                'entries': entries, 'skipped': skipped, 'historical_journal': history}
    save(output / 'snapshot.json', manifest)
    print(json.dumps({'snapshot': str(output / 'snapshot.json'), 'live': sum(e['kind'] == 'live' for e in entries),
                      'historical': 2, 'skipped': skipped}))


def current_matches(item):
    return Path(item['path']).read_bytes() == unpack(item)


def changes_for(entry, token):
    """Plan one credit; never reset launch counts or logical author budgets."""
    execution = json.loads(unpack(entry['execution']))
    credit = {'snapshot_sha256': token, 'prior_execution_sha256': entry['execution']['sha256'],
              'launches': execution['launches'], 'credited_at': time.time(), 'kind': entry['kind']}
    execution = {**execution, 'launch_limit': execution.get('launch_limit', 3) + 1,
                 'manual_interruption_credits': [*execution.get('manual_interruption_credits', []), credit]}
    updates = [(entry['execution'], execution)]
    if entry['kind'] == 'historical':
        pipeline = json.loads(unpack(entry['pipeline']))
        job = json.loads(unpack(entry['job']))
        event = {**credit, 'prior_error': pipeline['error'], 'prior_outcome': job['outcome']}
        pipeline.update(stage='generate', error=None, updated=time.time(),
                        manual_interruption_recoveries=[*pipeline.get('manual_interruption_recoveries', []), event])
        job.update(state='running', retryAt=0, completedAt=0, error=None, outcome={},
                   manual_interruption_recoveries=[*job.get('manual_interruption_recoveries', []), event])
        updates += [(entry['pipeline'], pipeline), (entry['job'], job)]
    return [{'path': before['path'], 'before': before,
             'after': base64.b64encode((json.dumps(after, indent=2) + '\n').encode()).decode()}
            for before, after in updates]


def apply(snapshot_path):
    snapshot_path = Path(snapshot_path).resolve()
    manifest = read(snapshot_path)
    token = digest(snapshot_path.read_bytes())
    require(manifest['helper_sha256'] == digest(Path(__file__).read_bytes()), 'Helper changed; capture again')
    require(manifest['inventory'] == str(INVENTORY), 'Unexpected inventory')
    state = service_state()
    require(state['ActiveState'] == 'inactive' and state['SubState'] == 'dead' and state['MainPID'] == '0',
            'Stop the service before apply')
    require(not any(owned(row, manifest['service']) and row['state'] not in ('Z', 'X') for row in processes()),
            'A process in the captured service cgroup is still alive')
    completed = snapshot_path.parent / 'applied.json'
    require(not completed.exists(), 'This snapshot has already been applied')
    stop_rows = journal('@' + str(manifest['created']))
    require(any(row['message'].startswith('Stopped ' + SERVICE) for row in stop_rows), 'Missing post-snapshot service stop')
    with ExitStack() as stack:
        for path in [INVENTORY / 'jobs.lock', *[Path(e['pipeline']['path']).parent / 'worker.lock' for e in manifest['entries']],
                     *[INVENTORY / f'kp-{e["knowledge_point"]}.lock' for e in manifest['entries']]]:
            lock = stack.enter_context(path.open('a'))
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        plan_path = snapshot_path.parent / 'application-plan.json'
        if plan_path.exists():
            plan = read(plan_path)
            require(plan['snapshot_sha256'] == token, 'Application plan belongs to another snapshot')
        else:
            changes, skipped = [], []
            for entry in manifest['entries']:
                pipeline = Path(entry['pipeline']['path']).parent
                require(not (pipeline / 'publication/request.json').exists(), 'Publication intent appeared; do not change this job')
                if Path(entry['session'], 'result.json').exists() or not all(current_matches(entry[key]) for key in ('execution', 'pipeline')):
                    require(entry['kind'] != 'historical', 'Historical recovery changed; capture again')
                    skipped.append({'session': entry['session'], 'reason': 'Finished or changed after snapshot; no credit'})
                    continue
                if entry['kind'] == 'historical':
                    require(current_matches(entry['job']), 'Historical job changed; capture again')
                    historical_proof(entry, manifest['historical_journal'])
                else:
                    for identity in (entry['pipeline_process'], entry['agent_process']):
                        observed = process(identity['pid'])
                        require(not observed or observed['start_ticks'] != identity['start_ticks'] or observed['state'] in ('Z', 'X'),
                                'Captured process is still running')
                archive = Path(entry['archive'])
                for key in ('execution', 'pipeline', 'job'):
                    (archive / (key + '-before.json')).write_bytes(unpack(entry[key]))
                (archive / 'events-at-stop.jsonl').write_bytes(Path(entry['session'], 'events.jsonl').read_bytes())
                result = Path(entry['job']['path']).with_suffix('.result')
                if result.exists():
                    (archive / 'durable-result-before.json').write_bytes(result.read_bytes())
                changes += changes_for(entry, token)
            plan = {'snapshot_sha256': token, 'created': time.time(), 'stop_journal': stop_rows,
                    'changes': changes, 'skipped': skipped}
            save(plan_path, plan)
        # Validate the entire write set before touching any live state. A rerun
        # after an interrupted apply accepts exact already-written bytes only.
        for change in plan['changes']:
            current = Path(change['path']).read_bytes()
            require(current in (unpack(change['before']), base64.b64decode(change['after'])), 'Apply target changed: ' + change['path'])
        for change in plan['changes']:
            atomic_bytes(change['path'], base64.b64decode(change['after']))
        save(completed, {'snapshot_sha256': token, 'at': time.time(), 'files': [c['path'] for c in plan['changes']],
                         'skipped': plan['skipped']})
    print(json.dumps(read(completed), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('snapshot').add_argument('--output', type=Path, required=True)
    commands.add_parser('apply').add_argument('--snapshot', type=Path, required=True)
    args = parser.parse_args()
    snapshot(args.output) if args.command == 'snapshot' else apply(args.snapshot)
