"""Restore misplaced completed verification records and requeue their same jobs."""
import fcntl
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_pipeline import Pipeline
from generator_publish import Publisher
from inventory_jobs import save
from serve_graph_explorer import database_environment

JOBS = ROOT / '.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
TARGETS = {17592186179670, 17592186175924, 17592186138396, 17592186124445}
REASON = 'Restore completed verification saved at a duplicated relative path; retain original session, samples, and budgets.'


def main():
    environment = database_environment('math')
    publisher = Publisher.from_environment(database='math')
    recovered = []
    for path in JOBS.glob('*.json'):
        outer = json.loads(path.read_text())
        kp = outer.get('request', {}).get('knowledgePoint')
        if kp not in TARGETS or outer.get('state') != 'blocked':
            continue
        with (JOBS / f'kp-{kp}.lock').open('a') as kp_lock:
            fcntl.flock(kp_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with (JOBS / 'jobs.lock').open('a') as jobs_lock:
                fcntl.flock(jobs_lock, fcntl.LOCK_EX)
                outer = json.loads(path.read_text())
                assert outer['state'] == 'blocked'
                assert outer['outcome']['reason']['code'] in {'review_binding_changed', 'pipeline_process_failed'}
                directory = path.with_suffix('.pipeline') / str(outer['cycle'])
                with (directory / 'worker.lock').open('a') as worker_lock:
                    fcntl.flock(worker_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    state = json.loads((directory / 'job.json').read_text())
                    assert state['stage'] in {'blocked', 'validate'} and not state.get('review')
                    assert not state.get('publication') and not (directory / 'publication/request.json').exists()
                    evidence = Path(state['active_review_directory'])
                    execution = (evidence / 'execution.json').read_bytes()
                    before_path = Path(__file__).with_name(f'{kp}-before.json')
                    assert not before_path.exists(), 'Preserve earlier recovery evidence'
                    save(before_path, {'outer': outer, 'pipeline': state})
                    pipeline = Pipeline(directory, state['request'], publisher, environment=environment)
                    assert pipeline.restore_misplaced_final_binding(evidence), 'No exact completed record to restore'
                    event = {'time': time.time(), 'reason': REASON, 'prior_error': state.get('error')}
                    if state['stage'] == 'blocked':
                        assert state['error']['code'] == 'review_binding_changed'
                        assert state['error']['resume_stage'] == 'validate'
                        pipeline.persist(stage='validate', error=None,
                            resume_events=[*state.get('resume_events', []), event])
                    assert (evidence / 'execution.json').read_bytes() == execution
                    save(path, {**outer, 'state': 'pending', 'processFailures': 0,
                        'retryAt': 0, 'error': None, 'outcome': {},
                        'recovery_events': [*outer.get('recovery_events', []), event]})
                    recovered.append({'kp': kp, 'cycle': outer['cycle'], 'job': str(path),
                        'restored_binding': str(evidence / 'final-binding.json'),
                        'session_and_budgets_unchanged': True})
    save(Path(__file__).with_name('recovery.json'), {'time': time.time(), 'recovered': recovered})
    print(json.dumps(recovered, indent=2))


if __name__ == '__main__':
    main()
