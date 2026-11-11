"""Prepare the separately reviewed 14-job infrastructure recovery; never apply."""
import collections
import io
import json
from pathlib import Path
import sys
import tarfile
import time

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
import generator_quota_recovery as R
from generator_lifecycle import agent_running
from inventory_jobs import save

AUDIT = Path(__file__).resolve().parent
INVENTORY = ROOT / '.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
HEALTH = ROOT / 'reference/edb-math/audits/2026-11-11-generator-resume-readiness/inventory-health.json'
OUTPUT = AUDIT / 'supplemental-recovery'
QUOTA = {
    '30e50ba96eda7f5a02926acb7783d71c153d5add94fe9855109862dd9c11d880',
    '6da8d8d4268273b824a2f43141390ac8542fe4fdb43ad8c739aa225ada6a994c',
    '7d060354efbf84a1c244d882e9782a5997771b47f61d38dd0401eafb3d4ca2d4',
    '8e9083510ea812323b58092a1ea8509689cf741cce3ca7237e42fe4813bf930c',
    'bac2828d65e550c31e4597ec24dcbe121203ec25714119b9cf3b8c5c7be641eb',
    'cc3394d19a09b6b15547dff0fdc6b4b0d63ad29790bec3b6b3ed3c33613705fb',
    'd9cac9d4940f1a6e31287ca9056ab4d475aac79479c7b74d2ccb2653177e5274',
    'fc4b9804ba065314db2120b1a6e84ad37baa46e4fe053555f5b54fea2e5d9fdc',
}
SCHEMA = {
    '81b6c4bdfe47b0aa62c342d5abb593e761078e664ae3dc2d2f227df30fe5821f',
    'af356abc043071b692ac2111094979c0c9f5d71f626112771e121b93ae0f0269',
    'b9f37e6ee72ed133d69e3ae35806a323bdc5bf0019ff9ff68df05fe1442a3f20',
}
CAPACITY = '77b9385ee1a060f948338f66ad2bd4f175a25b05c48f9e85ab8fdb62a2b0ad4a'
STALE = '7e624f9de3799a28b6de38a3ff34b13a8368f0d1a88f69302b4ab8a1d176da81'
ASSET = '69c1a76d039d3c5357e9412b1921848cbb2c7a2f7f10d5a7436dfb4ff1bb056e'


def failed_turns(data, kind):
    terminals, work_items, active = [], 0, False
    for line in data.splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if row.get('type') == 'turn.started':
            assert not active
            active = True
        elif row.get('type') in {'turn.failed', 'turn.completed'}:
            assert active
            active = False
            assert row['type'] == 'turn.failed'
            message = row.get('error', {}).get('message', '')
            if kind == 'quota':
                assert R.quota_message(row['error'])
            elif kind == 'schema':
                assert 'invalid_json_schema' in message and "$ref cannot have keywords {'description'}" in message
            else:
                assert message == 'Selected model is at capacity. Please try a different model.'
            terminals.append(row)
        elif row.get('type') in {'item.started', 'item.completed'}:
            work_items += 1
    assert not active
    # Providers can reject a continuation or final structured response after
    # useful work. Preserve that work; the terminal failure is infrastructure.
    return len(terminals)


def root_failures(log, directory):
    result = []
    for line in log.splitlines():
        if line == 'TypeError: Object of type UUID is not JSON serializable':
            result.append('uuid')
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and row.get('directory') == str(directory) and row.get('error'):
            result.append(row['error'])
    return result


def main():
    assert not OUTPUT.exists(), 'Do not replace an already prepared recovery'
    health = json.loads(HEALTH.read_text())
    rows = {row['key']: row for row in health['other_failure_details']}
    at = time.time()
    identity = 'supplemental-infrastructure-2026-11-11'
    plan = {'format': 1, 'recovery_id': identity, 'prepared_at': at,
            'inventory': str(INVENTORY), 'jobs': [], 'skipped': []}
    originals = {}
    process_causes, launch_causes = collections.Counter(), collections.Counter()
    for key in sorted(QUOTA | SCHEMA | {CAPACITY, STALE, ASSET}):
        path = INVENTORY / (key + '.json')
        root_bytes = path.read_bytes(); root = json.loads(root_bytes)
        directory = path.with_suffix('.pipeline') / str(root['cycle'])
        state_path = directory / 'job.json'
        state_bytes = state_path.read_bytes(); state = json.loads(state_bytes)
        assert root['state'] == 'blocked'
        assert not (directory / 'publication/request.json').exists()
        assert root['request']['knowledgePoint'] == state['request']['kp']
        root_log = path.with_suffix('.log')
        log_bytes = root_log.read_bytes()
        terminal = root_failures(log_bytes.decode(), directory)
        execution_path, launches, quota_credits, process_credits = None, 0, 0, 0
        process_counts, launch_counts = {}, {}
        stage = state['stage']
        kind = ('quota' if key in QUOTA else 'schema' if key in SCHEMA else
                'capacity' if key == CAPACITY else 'stale-basis' if key == STALE else 'runtime-assets')
        record = {'id': identity, 'at': at, 'cause': kind, 'resume_stage': stage,
                  'root_log': str(root_log), 'root_log_sha256': R.sha(log_bytes)}
        changes = []
        if key in QUOTA | SCHEMA | {CAPACITY}:
            failed = [item for item in rows[key]['executions'] if item['status'] == 'failed']
            assert len(failed) == 1
            execution_path = R.inside(directory, ROOT / failed[0]['path'])
            execution_bytes = execution_path.read_bytes(); execution = json.loads(execution_bytes)
            assert execution['status'] == 'failed' and not agent_running(execution)
            assert not execution.get('quota_recoveries') and not execution.get('infrastructure_recoveries')
            session = R.inside(directory, execution.get('result_directory', execution_path.parent))
            events_path = session / 'events.jsonl'; events_bytes = events_path.read_bytes()
            launches = failed_turns(events_bytes, kind)
            assert launches == execution['launches'] == (3 if key == CAPACITY else 2)
            launch_counts[kind] = launches
            launch_causes.update(launch_counts)
            quota_credits = launches if kind == 'quota' else 0
            record.update(events_path=str(events_path), events_sha256=R.sha(events_bytes),
                          rejected_turns=launches, prior_launch_limit=execution.get('launch_limit', 3),
                          new_launch_limit=execution.get('launch_limit', 3) + launches)
            if key == CAPACITY:
                assert state['stage'] == 'blocked'
                assert state['error']['code'] == 'agent_session_retry_exhausted'
                assert state['error']['cause']['session_directory'] == str(session)
                stage = state['error']['resume_stage']
            else:
                assert root['outcome']['reason']['code'] == 'pipeline_process_failed'
                assert root['processFailures'] == 3 and state['stage'] in {'investigate', 'validate'}
                # Last two failed process results match the exact agent output
                # path whose only two turns were provider rejections.
                assert len(terminal) >= 3
                for error in terminal[-2:]:
                    assert str(session / 'result.json') in error and 'returned non-zero exit status 1' in error
                prior = terminal[-3]
                assert prior in {'uuid', 'Database advanced during preparation'}
                prior_kind = 'uuid-serialization' if prior == 'uuid' else 'stale-basis'
                process_counts = {kind: 2, prior_kind: 1}
                process_credits = 3
            changes.append(('execution', execution_path, execution_bytes, {
                'launch_limit': execution.get('launch_limit', 3) + launches,
                'status': 'deferred', 'error': None, 'infrastructure_recoveries': [record]}))
        else:
            events_path, events_bytes = root_log, log_bytes
            if key == STALE:
                assert root['outcome']['reason']['code'] == 'pipeline_process_failed'
                assert root['processFailures'] == 3 and state['stage'] == 'prepare'
                assert terminal[-2:] == ['Database advanced during preparation'] * 2
                assert 'timed out after 3600 seconds' in terminal[-3]
                process_credits, process_counts = 2, {'stale-basis': 2}
                record['preserved_failure'] = terminal[-3]
            else:
                assert state['error']['code'] == 'author_reported_limitation'
                assert 'runner asset' in state['error']['cause']['summary']
                assert state['attempt'] == 2 and state['author_attempt_limit'] == 3
                assert state['author_running'] is False
                assert list(state['progress_failures'].values()) == [1]
                stage = 'generate'
                record['reason'] = ('Runtime-relative asset resolution is now supported in sample_band; '
                                    'resume the one remaining author attempt, retaining all-band review requirements.')
        process_causes.update(process_counts)
        record.update(resume_stage=stage, launch_credits_by_cause=launch_counts,
                      process_credits_by_cause=process_counts)
        # Never adjust author/review/correction/content-failure counters. The
        # stale prepare case needs only root dispatch reopened, no phase edit.
        if key != STALE:
            changes.append(('pipeline', state_path, state_bytes, {
                'stage': stage, 'error': None, 'updated': at, 'infrastructure_recovery': record}))
        root_updates = {'state': 'pending', 'retryAt': 0, 'error': None, 'exitCode': None,
            'outcome': {'outcome': 'paused', 'reason': {'code': 'infrastructure_recovered', 'recovery_id': identity}},
            'infrastructure_recovery': record}
        if process_credits:
            root_updates['processFailures'] = root['processFailures'] - process_credits
        changes.append(('root', path, root_bytes, root_updates))
        files = []
        for name, destination, before, updates in changes:
            backup = key + '/' + name + '.json'
            originals[backup] = before
            files.append({'kind': name, 'path': str(destination), 'backup': backup,
                          'before_sha256': R.sha(before),
                          'after_sha256': R.sha(R.encoded({**json.loads(before), **updates})),
                          'updates': updates})
        plan['jobs'].append({'key': key, 'kp': state['request']['kp'], 'cycle': root['cycle'],
            'cause': kind, 'quota_credits': quota_credits, 'launch_credits': launches,
            'process_credits': process_credits, 'resume_stage': stage,
            'files': files, 'events_path': str(events_path), 'events_sha256': R.sha(events_bytes),
            'additional_evidence': [{'path': str(root_log), 'sha256': R.sha(log_bytes)}]})
    OUTPUT.mkdir()
    with tarfile.open(OUTPUT / 'backups.tar.gz', 'w:gz') as archive:
        for name, before in originals.items():
            member = tarfile.TarInfo(name); member.size = len(before); member.mode = 0o600
            archive.addfile(member, io.BytesIO(before))
    plan['backup_sha256'] = R.sha((OUTPUT / 'backups.tar.gz').read_bytes())
    save(OUTPUT / 'plan.json', plan)
    summary = {'eligible_jobs': len(plan['jobs']), 'skipped_jobs': 0,
               'launch_credits_by_cause': dict(launch_causes),
               'process_failure_credits_by_cause': dict(process_causes),
               'changed_files': len(originals), 'preserved_genuine_timeout_failures': 1,
               'runtime_asset_author_attempts_remaining': 1, 'no_generation_or_approval': True}
    save(OUTPUT / 'dry-run.json', summary)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
