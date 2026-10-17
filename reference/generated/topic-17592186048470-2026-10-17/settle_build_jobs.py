"""Settle only these three pending builds after bounded native verification."""
import argparse
import fcntl
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from inventory_jobs import InventoryJobs, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('readiness', type=Path)
    args = parser.parse_args()
    readiness = json.loads(args.readiness.read_text())
    assert readiness['topic'] == 17592186048470
    assert readiness['lesson_ready'] and readiness['read_scope']['global_attribute_scans'] == 0
    rows = {row['knowledgePoint']: row for row in readiness['knowledge_points']}
    results = []
    for original in json.loads((HERE / 'before-jobs.json').read_text()):
        path = ROOT / original['path']
        kp = original['request']['knowledgePoint']
        row = rows[kp]
        base = '.local/generation/decimal-grader-repair' if kp == 17592186054745 else '.local/generation'
        pipeline_path = ROOT / f'{base}/math/{kp}-auto/job.json'
        pipeline = json.loads(pipeline_path.read_text())
        assert pipeline['stage'] == 'verified' and pipeline['approval_recorded']
        assert row['available_total'] >= 5
        assert row['generator_script'] == pipeline['registration']
        with (path.parent / f'kp-{kp}.lock').open('a') as kp_lock:
            try:
                fcntl.flock(kp_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                results.append({'kp': kp, 'status': 'active-worker; unchanged'})
                continue
            with (path.parent / 'jobs.lock').open('a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                current = json.loads(path.read_text())
                assert current['lineage'] == readiness['lineage']
                assert current['request']['knowledgePoint'] == kp
                if (current.get('cycle', 1) != original.get('cycle', 1)
                        or current['state'] not in ('pending', 'awaiting-verification')
                        or InventoryJobs.recoverable(path, current)):
                    results.append({'kp': kp, 'status': current['state'] + '; unchanged'})
                    continue
                updated = {
                    **current, 'state': 'verified', 'verifiedBasis': readiness['basis'],
                    'completedAt': time.time(),
                    'outcome': {
                        'outcome': 'generated', 'evidence': str(pipeline_path),
                        'generator': pipeline['registration'],
                        'readinessEvidence': str(args.readiness.resolve()),
                        'difficulty': pipeline['effective_difficulty'],
                    },
                }
                save(path, updated)
                results.append({'kp': kp, 'status': 'verified', 'before': current, 'after': updated})
    save(HERE / 'settled-build-jobs.json', {'basis': readiness['basis'], 'jobs': results})
    print(json.dumps([{'kp': row['kp'], 'status': row['status']} for row in results]))


if __name__ == '__main__':
    main()
