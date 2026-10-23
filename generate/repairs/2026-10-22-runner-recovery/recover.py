"""Recover the three runaway jobs after repairing the runner; no Codex launches."""
from contextlib import ExitStack
import fcntl
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_cohort import CohortPipeline, CampaignStore
from generator_pipeline import read, digest
from generator_publish import Publisher
from inventory_jobs import save

DIRECTORY = ROOT / 'generate/repairs/2026-10-20-early-cohort'
RECOVERY = Path(__file__).resolve().parent
KPS = (17592186229165, 17592186059775, 17592186115242)
REASON = ('Fixed report writable roots and routing, durable retry budgets, and runner-owned '
          'inventory repair; retained generator regressions passed before fresh independent review.')


def main():
    store = CampaignStore(DIRECTORY)
    publisher = Publisher.from_environment()
    campaign = read(DIRECTORY / 'cohort.json')
    locks = ROOT / '.local/learning/inventory' / publisher.config.database / campaign['learner']
    results = []
    with ExitStack() as stack:
        for kp in KPS:
            for path in (locks / f'kp-{kp}.lock', DIRECTORY / 'jobs' / str(kp) / 'worker.lock'):
                lock = stack.enter_context(path.open('a'))
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for kp in KPS:
            directory = DIRECTORY / 'jobs' / str(kp)
            backup = RECOVERY / str(kp)
            backup.mkdir(exist_ok=True)
            for name in ('job.json', 'repair-history.json', 'source/inventory.json', 'feedback.json'):
                target = backup / name
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists():
                    shutil.copy2(directory / name, target)
            state = read(directory / 'job.json')
            pipeline = CohortPipeline(directory, state['request'], publisher,
                                      environment=publisher.client.environment)
            if kp == 17592186115242:
                history = read(directory / 'repair-history.json')
                finding = next(row for row in history['findings'] if row['id'] == '591f580cadb749294588')
                finding['finding']['kind'] = 'inventory'
                finding['runner_ownership_migration'] = {
                    'previous_kind': 'decision_shortcut', 'time': time.time(),
                    'reason': 'The original requested change explicitly requires separate stored-inventory remediation.'}
                save(directory / 'repair-history.json', history)
            repaired = pipeline.repair_inventory(Path(state['previous_review']['directory']))
            if repaired and repaired.get('unresolved'):
                pipeline.block_inventory(repaired)
                raise RuntimeError(f'{kp}: inventory repair unresolved: {repaired["unresolved"]}')
            pipeline.check_repair_regressions()
            if kp == 17592186115242:
                command = [str(ROOT / '.venv/bin/python'), '-B', 'checks/batch_regressions.py', '--finding', 'inventory']
                completed = subprocess.run(command, cwd=directory / 'workspace',
                                           capture_output=True, text=True, timeout=180)
                (backup / 'inventory-regression.stdout').write_text(completed.stdout)
                (backup / 'inventory-regression.stderr').write_text(completed.stderr)
                if completed.returncode:
                    raise RuntimeError(f'{kp}: refreshed inventory check failed: {completed.stderr[-1000:]}')
            pipeline.sample()
            pipeline.persist(package_hash=pipeline.candidate_hash(), author_running=False,
                             approval_recorded=False)
            pipeline.block('runner_recovery_ready', {'reason': REASON}, 'validate')
            pipeline.resume_blocked(REASON)
            row = {'kp': kp, 'stage': pipeline.state['stage'], 'attempt': pipeline.state['attempt'],
                   'package_hash': pipeline.state['package_hash'],
                   'pool_repair': repaired, 'generator_regressions': 'passed',
                   'author_attempt_limit': pipeline.state['author_attempt_limit']}
            results.append(row)
            save(backup / 'recovery.json', row)
            print(json.dumps({'kp': kp, 'stage': row['stage'], 'regressions': 'passed',
                              'retired': (repaired or {}).get('retired', []),
                              'protected': (repaired or {}).get('protected', [])}), flush=True)
        with store.locked() as campaign:
            for item in campaign['items']:
                if item['kp'] in KPS:
                    item.update(state='pending', error=None, recovery_reason=REASON)
            campaign.pop('campaign_error', None)
            store.write(campaign)
        save(RECOVERY / 'recovery.json', {'time': time.time(), 'jobs': results})


if __name__ == '__main__':
    main()
