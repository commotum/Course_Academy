"""Evidence-bound, one-time recovery of historical quota-blocked inventory jobs.

This does not run a pipeline or grant new content budgets. It restores only the
launch capacity demonstrably consumed by the recorded quota rejection turns.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack, contextmanager
import hashlib
import io
import json
from pathlib import Path
import fcntl
import tarfile
import time

from generator_lifecycle import agent_running
from inventory_jobs import save


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return json.dumps(value, indent=2).encode()


def quota_message(value):
    if not isinstance(value, dict):
        return False
    text = str(value.get('message', '')).lower().replace('’', "'")
    return (value.get('code') in {'usage_limit_reached', 'quota_exceeded', 'insufficient_quota'}
            or "you've hit your usage limit" in text)


def quota_turns(data):
    """Count terminal rejected turns, never duplicate the accompanying error."""
    turns, active, quota, terminals, last = 0, False, 0, 0, None
    for raw in data.splitlines():
        try:
            row = json.loads(raw)
        except (ValueError, UnicodeDecodeError):
            continue
        if not isinstance(row, dict):
            continue
        kind = row.get('type')
        if kind == 'turn.started':
            if active:
                raise ValueError('Unfinished or overlapping turns in quota evidence')
            active, turns = True, turns + 1
        elif kind in {'turn.failed', 'turn.completed'}:
            if not active:
                raise ValueError('Terminal event lacks an admitted turn')
            active, terminals = False, terminals + 1
            last = kind == 'turn.failed' and quota_message(row.get('error'))
            quota += int(last)
    if active or not quota or not last or turns != terminals:
        raise ValueError('Evidence must end in a complete quota-rejected turn')
    return quota


def inside(root, path):
    result = Path(path).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError('Recovery path escapes its inventory cycle')
    return result


def plan_job(inventory, item, recovery_id, at):
    inventory = Path(inventory).resolve()
    root_path = inside(inventory, inventory / (item['key'] + '.json'))
    root_bytes = root_path.read_bytes()
    root = json.loads(root_bytes)
    if root.get('state') != 'blocked':
        raise ValueError('Manifest job is no longer blocked')
    if root['request']['knowledgePoint'] != item['kp'] or root['key'] != item['key']:
        raise ValueError('Manifest identity differs from inventory')
    cycle = root.get('cycle', 1)
    directory = root_path.with_suffix('.pipeline') / str(cycle)
    pipeline_path = directory / 'job.json'
    pipeline_bytes = pipeline_path.read_bytes()
    pipeline = json.loads(pipeline_bytes)
    error = pipeline.get('error') or {}
    cause = error.get('cause') or {}
    if (pipeline.get('stage') != 'blocked' or pipeline['request']['kp'] != item['kp']
            or error.get('code') != 'agent_session_retry_exhausted'
            or cause.get('code') != 'agent_session_retry_exhausted'
            or root.get('outcome', {}).get('reason') != error
            or cause.get('role') != item['role']):
        raise ValueError('Current blocker is not the exact audited session exhaustion')
    stage = error.get('resume_stage')
    if stage not in {'investigate', 'validate', 'generate', 'report-repair'}:
        raise ValueError('Unknown saved resume stage')
    if (directory / 'publication/request.json').exists():
        raise ValueError('Publication intent requires separate reconciliation')
    events_path = inside(directory, Path(cause['session_directory']) / 'events.jsonl')
    execution_path = inside(directory, cause.get('execution_path', events_path.parent / 'execution.json'))
    execution_bytes = execution_path.read_bytes()
    execution = json.loads(execution_bytes)
    if execution.get('status') != 'failed' or agent_running(execution):
        raise ValueError('Agent execution is not a settled failure')
    if Path(execution.get('result_directory', events_path.parent)).resolve() != events_path.parent:
        raise ValueError('Evidence is not bound to the failed execution')
    if execution.get('parent_deferrals') or execution.get('quota_recoveries'):
        raise ValueError('Execution already has rejection credits; reconcile separately')
    events = events_path.read_bytes()
    count = quota_turns(events)
    if count != item['rejected_turns'] or not 0 < count <= execution['launches']:
        raise ValueError('Quota evidence differs from the incident allowlist')
    if cause.get('launches') != execution['launches']:
        raise ValueError('Execution launch count has changed')
    # These counters track valid outputs rejected by content checks, not CLI
    # failures. Keeping them prevents quota recovery from refreshing real work.
    source_rounds = pipeline.get('source_account_rounds', {}).get(item['role'], 0)
    source_limit = pipeline.get('source_account_limits', {}).get(item['role'], 3)
    if stage == 'investigate' and source_rounds >= source_limit:
        raise ValueError('A separate source-account correction cap is exhausted')
    if pipeline.get('attempt', 0) > pipeline.get('author_attempt_limit', 3):
        raise ValueError('A separate author attempt cap is exhausted')
    if len(pipeline.get('review_sessions', [])) > pipeline.get('review_session_limit', 9):
        raise ValueError('A separate review session cap is exhausted')
    limit = execution.get('launch_limit', 3)
    if execution['launches'] != limit:
        raise ValueError('Blocked execution is not exactly at its launch limit')
    record = {'id': recovery_id, 'at': at, 'quota_rejected_turns': count,
              'events_path': str(events_path), 'events_sha256': sha(events),
              'prior_launch_limit': limit, 'new_launch_limit': limit + count,
              'resume_stage': stage}
    changes = [
        ('execution', execution_path, execution_bytes, {
            'launch_limit': limit + count, 'status': 'deferred', 'error': None,
            'quota_recoveries': [record]}),
        ('pipeline', pipeline_path, pipeline_bytes, {
            'stage': stage, 'error': None, 'updated': at, 'quota_recovery': record}),
        ('root', root_path, root_bytes, {
            'state': 'pending', 'retryAt': 0, 'error': None, 'exitCode': None,
            'outcome': {'outcome': 'paused', 'reason': {
                'code': 'quota_exhaustion_recovered', 'recovery_id': recovery_id}},
            'quota_recovery': record}),
    ]
    files, originals = [], {}
    for kind, path, original, updates in changes:
        name = item['key'] + '/' + kind + '.json'
        after = encoded({**json.loads(original), **updates})
        files.append({'kind': kind, 'path': str(path), 'backup': name,
                      'before_sha256': sha(original), 'after_sha256': sha(after), 'updates': updates})
        originals[name] = original
    return {'key': item['key'], 'kp': item['kp'], 'cycle': cycle,
            'quota_credits': count, 'resume_stage': stage, 'files': files,
            'events_path': str(events_path), 'events_sha256': sha(events)}, originals


def prepare(inventory, manifest, output):
    inventory, manifest, output = Path(inventory).resolve(), Path(manifest), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    if (output / 'plan.json').exists() or (output / 'backups.tar.gz').exists():
        raise ValueError('Use a new output directory; recovery evidence is immutable')
    manifest_bytes = manifest.read_bytes()
    entries = json.loads(manifest_bytes)
    if len({item['key'] for item in entries}) != len(entries):
        raise ValueError('Duplicate job in incident allowlist')
    recovery_id = 'quota-2026-11-11-' + sha(manifest_bytes)[:16]
    plan = {'format': 1, 'recovery_id': recovery_id, 'prepared_at': time.time(),
            'inventory': str(inventory), 'manifest_sha256': sha(manifest_bytes), 'jobs': [], 'skipped': []}
    with tarfile.open(output / 'backups.tar.gz', 'w:gz') as archive:
        for entry in entries:
            try:
                row, originals = plan_job(inventory, entry, recovery_id, plan['prepared_at'])
            except (OSError, ValueError, KeyError) as error:
                plan['skipped'].append({'key': entry['key'], 'reason': str(error)})
                continue
            plan['jobs'].append(row)
            for name, original in originals.items():
                member = tarfile.TarInfo(name)
                member.size = len(original)
                member.mode = 0o600
                archive.addfile(member, io.BytesIO(original))
    plan['backup_sha256'] = sha((output / 'backups.tar.gz').read_bytes())
    save(output / 'plan.json', plan)
    summary = {'eligible_jobs': len(plan['jobs']), 'skipped_jobs': len(plan['skipped']),
               'quota_launch_credits': sum(row['quota_credits'] for row in plan['jobs']),
               'changed_files': sum(len(row['files']) for row in plan['jobs']),
               'no_pipeline_or_database_execution': True}
    save(output / 'dry-run.json', summary)
    return summary


@contextmanager
def lock_file(path, *, wait=False):
    with Path(path).open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | (0 if wait else fcntl.LOCK_NB))
        yield


def load_plan(output):
    output = Path(output)
    plan = json.loads((output / 'plan.json').read_text())
    if sha((output / 'backups.tar.gz').read_bytes()) != plan['backup_sha256']:
        raise ValueError('Backup archive changed')
    with tarfile.open(output / 'backups.tar.gz', 'r:gz') as archive:
        originals = {member.name: archive.extractfile(member).read() for member in archive.getmembers()}
    for row in plan['jobs']:
        for spec in row['files']:
            if sha(originals[spec['backup']]) != spec['before_sha256']:
                raise ValueError('Backed-up source differs from recovery plan')
            after = encoded({**json.loads(originals[spec['backup']]), **spec['updates']})
            if sha(after) != spec['after_sha256']:
                raise ValueError('Recovery patch differs from plan')
    return plan, originals


def refreshed_inventory_root(spec, original, current_bytes):
    """Accept only inventory ranking after a completed, recorded recovery.

    The UI marks an unfinished resumable cycle ``running`` without launching it.
    Such refreshes must survive an interrupted recovery; no attempt, outcome,
    cycle, stage input, or recovery marker may differ from the applied image.
    """
    if spec['kind'] != 'root':
        return False
    current = json.loads(current_bytes)
    expected = {**json.loads(original), **spec['updates']}
    if current.get('state') not in {'pending', 'running', 'withdrawn'}:
        return False
    if {k: v for k, v in current.items() if k not in {'state', 'request'}} != {
            k: v for k, v in expected.items() if k not in {'state', 'request'}}:
        return False
    stable = ('knowledgePoint', 'stage', 'missing', 'script', 'difficulty', 'jobKind')
    return all(current['request'].get(k) == expected['request'].get(k) for k in stable)


def apply(output, daemon_lock):
    output = Path(output)
    plan, originals = load_plan(output)
    inventory = Path(plan['inventory'])
    results = []
    with lock_file(daemon_lock), lock_file(inventory / 'jobs.lock', wait=True):
        for row in plan['jobs']:
            directory = inventory / (row['key'] + '.pipeline') / str(row['cycle'])
            with ExitStack() as locks:
                locks.enter_context(lock_file(inventory / f'kp-{row["kp"]}.lock'))
                locks.enter_context(lock_file(directory / 'worker.lock'))
                if (directory / 'publication/request.json').exists():
                    raise ValueError('A publication intent appeared after planning')
                if sha(Path(row['events_path']).read_bytes()) != row['events_sha256']:
                    raise ValueError('Agent evidence changed after planning')
                # Check every member before any write. Accepting exact planned
                # after-images makes an interrupted apply safely idempotent.
                pending = []
                for spec in row['files']:
                    current_bytes = Path(spec['path']).read_bytes()
                    current = sha(current_bytes)
                    if current not in {spec['before_sha256'], spec['after_sha256']}:
                        if not refreshed_inventory_root(spec, originals[spec['backup']], current_bytes):
                            raise ValueError('Concurrent change at ' + spec['path'])
                    if current == spec['before_sha256']:
                        pending.append(spec)
                for spec in pending:
                    save(Path(spec['path']), {**json.loads(originals[spec['backup']]), **spec['updates']})
                results.append({'key': row['key'], 'written_files': len(pending)})
        # Capture exact after-image verification while admission refresh cannot
        # legitimately update an already-unblocked root job beneath the audit.
        verification = verify(output)
        if not verification['verified']:
            raise ValueError('Recovery verification failed; inspect verification.json')
    result = {'recovery_id': plan['recovery_id'], 'applied_at': time.time(),
              'jobs': len(results), 'written_files': sum(row['written_files'] for row in results),
              'quota_launch_credits': sum(row['quota_credits'] for row in plan['jobs'])}
    save(output / 'applied.json', result)
    return result


def verify(output):
    plan, originals = load_plan(output)
    failures, refreshed = [], []
    for row in plan['jobs']:
        for spec in row['files']:
            current = Path(spec['path']).read_bytes()
            if sha(current) != spec['after_sha256']:
                if refreshed_inventory_root(spec, originals[spec['backup']], current):
                    refreshed.append({'key': row['key'], 'path': spec['path'], 'sha256': sha(current),
                                      'state': json.loads(current)['state']})
                else:
                    failures.append(spec['path'])
        if sha(Path(row['events_path']).read_bytes()) != row['events_sha256']:
            failures.append(row['events_path'])
    result = {'verified_at': time.time(), 'jobs': len(plan['jobs']),
              'verified': not failures, 'failures': failures,
              'quota_launch_credits': sum(row['quota_credits'] for row in plan['jobs']),
              'other_budget_changes': 0, 'event_logs_changed': 0 if not failures else None,
              'inventory_ranking_refreshes': refreshed}
    save(Path(output) / 'verification.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['plan', 'apply', 'verify'])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--inventory', type=Path)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--daemon-lock', type=Path)
    args = parser.parse_args()
    if args.action == 'plan':
        if not args.inventory or not args.manifest:
            parser.error('plan requires --inventory and --manifest')
        result = prepare(args.inventory, args.manifest, args.output)
    elif args.action == 'apply':
        if not args.daemon_lock:
            parser.error('apply requires the stopped supervisor daemon lock')
        result = apply(args.output, args.daemon_lock)
    else:
        result = verify(args.output)
    display = {**result}
    if 'failures' in display:
        display['failures'] = len(display['failures'])
        display['inventory_ranking_refreshes'] = len(display['inventory_ranking_refreshes'])
    print(json.dumps(display, indent=2))


if __name__ == '__main__':
    main()
