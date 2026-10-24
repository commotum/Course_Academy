"""Refresh repaired source evidence and requeue the original bounded build."""
from pathlib import Path
import fcntl
import json
import shutil
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_pipeline import Pipeline, digest, read
from generator_publish import Publisher
from inventory_jobs import save
from serve_graph_explorer import database_environment

KEY = '6977c1131f954380f9bbe5b01782da280c84a1ae190330120b4a71157f4d9fa9'
JOBS = ROOT / '.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
JOB = JOBS / (KEY + '.json')
DIRECTORY = JOB.with_suffix('.pipeline') / '2'
KP = 17592186092285


def main():
    verified = read(HERE / 'verification.json')
    assert verified['committed'] and verified['exact_readback']
    assert read(HERE / 'live-grading.json')['passed']
    with (JOBS / f'kp-{KP}.lock').open('a') as kp_lock, (DIRECTORY / 'worker.lock').open('a') as worker_lock:
        fcntl.flock(kp_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(worker_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        outer = read(JOB)
        assert outer['state'] == 'blocked' and outer['cycle'] == 2
        assert not (DIRECTORY / 'publication/request.json').exists()
        state = read(DIRECTORY / 'job.json')
        assert state['stage'] == 'blocked'
        archive = DIRECTORY / 'recovery-mixture-source-6396'
        archive.mkdir(exist_ok=False)
        shutil.copytree(DIRECTORY / 'source', archive / 'source')
        shutil.copy2(DIRECTORY / 'job.json', archive / 'job.json')
        shutil.copy2(JOB, archive / 'inventory-job.json')
        env = database_environment('math')
        pub = Publisher.from_environment(environment=env)
        fresh = pub.extract_source(KP, DIRECTORY / 'source')
        q = next(q for q in fresh['material']['kp'][':knowledge-point/questions'] if q[':db/id'] == 17592186092502)
        field, = q[':question/answer-fields']
        assert field[':answer-field/correct'][':answer/value'] == '$3.2$ tons and $4.8$ tons'
        assert q[':question/worked-solution'] == (HERE / 'solution.md').read_text().strip()
        pipeline = Pipeline(DIRECTORY, state['request'], pub, environment=env)
        pipeline.persist(source_hash=digest(fresh),
                         inventory_hash=digest(read(DIRECTORY / 'source/inventory.json')),
                         review=None, review_binding=None, review_policy_version=None,
                         approval_recorded=False, report_repair_directory=None,
                         review_report_error=None, review_report_result_file=None)
        reason = ('Corrected original q-10628 at EDB basis 6396: ordered mixture amounts, missing answer key, '
                  'and worked solution. All five choices verified with the native and live preview graders; '
                  'rendering passed. Archived old capture and refreshed source/inventory. Preserve candidate '
                  'package and samples; require fresh independent review against repaired source.')
        pipeline.resume_blocked(reason)
        pipeline.persist(error=None)
        pipeline.verify_approval_inputs()
        with (JOBS / 'jobs.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            current = read(JOB)
            assert current['state'] == 'blocked' and current['cycle'] == 2
            save(JOB, {**current, 'state': 'pending', 'retryAt': 0, 'error': None,
                       'outcome': {}, 'completedAt': 0,
                       'manualRecovery': {'at': time.time(), 'reason': reason, 'evidence': str(HERE)}})
        report = {'kp': KP, 'cycle': 2, 'stage': pipeline.state['stage'], 'state': 'pending',
                  'source_basis': fresh['basis'], 'source_hash': pipeline.state['source_hash'],
                  'package_preserved': pipeline.state['package_hash'] == state['package_hash'],
                  'batch_preserved': pipeline.state['batch_hash'] == state['batch_hash'],
                  'requeued_through_existing_six_worker_limit': True}
        save(HERE / 'resume-verification.json', report)
        print(json.dumps(report))


if __name__ == '__main__':
    main()
