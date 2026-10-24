"""Readmit old-policy stopped build jobs once, preserving their drafts/history."""
import argparse
import fcntl
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
from inventory_jobs import save
from generator_pipeline import PHASE_POLICY_VERSION


def recover(directory):
    rows = []
    with (directory / 'jobs.lock').open('a') as jobs_lock:
        fcntl.flock(jobs_lock, fcntl.LOCK_EX)
        for path in sorted(directory.glob('*.json')):
            outer = json.loads(path.read_text())
            if outer.get('state') not in {'blocked', 'rejected'} or outer.get('request', {}).get('jobKind', 'build') != 'build':
                continue
            job = path.with_suffix('.pipeline') / str(outer.get('cycle', 1))
            state_file = job / 'job.json'
            if not state_file.exists():
                continue
            state = json.loads(state_file.read_text())
            if state.get('phase_policy_version', 0) >= PHASE_POLICY_VERSION or state.get('stage') not in {'blocked', 'unsupported', 'failed'}:
                continue
            with (job / 'worker.lock').open('a') as worker:
                try:
                    fcntl.flock(worker, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    continue
                save(job / 'recovery/outer-before-three-phase.json', outer)
                save(path, {**outer, 'state': 'pending', 'retryAt': 0, 'processFailures': 0,
                            'error': None, 'threePhaseRecovery': {'policy': PHASE_POLICY_VERSION,
                                'time': time.time(), 'reason': 'Investigation/exemplars, nonblocking incomplete imports and repair-capable verification replace the old stop conditions.'}})
                rows.append({'key': path.stem, 'kp': state['request']['kp'],
                             'previous_stage': state['stage'], 'previous_outer_state': outer['state']})
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    rows = recover(args.directory)
    save(Path(__file__).with_name('recovered-jobs.json'), {'time': time.time(), 'jobs': rows})
    print(json.dumps({'readmitted': len(rows)}))
