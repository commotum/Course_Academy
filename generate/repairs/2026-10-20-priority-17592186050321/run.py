"""User-requested full generator priority run for one blocked study topic."""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_cohort import CohortSession, CapacityUnavailable
from generator_pipeline import Pipeline, read
from generator_publish import Publisher
from inventory_jobs import save
from generator_services import start_cohort

TOPIC = 17592186050321
KPS = [17592186184153, 17592186184154, 17592186184155]
COHORT = ROOT / 'generate/repairs/2026-10-20-early-cohort'
SERVICE = 'course-academy-generator-cohort-20261020.service'
TOKEN = 'priority-topic-17592186050321-repair'


def resume_cohort():
    marker = COHORT / 'stop-after-current'
    if not marker.exists() or marker.read_text().strip() != TOKEN:
        return {'resumed': False, 'reason': 'Pause marker changed; preserve operator decision'}
    marker.unlink()
    for _ in range(20):
        state = subprocess.run(['systemctl', '--user', 'is-active', SERVICE], capture_output=True, text=True).stdout.strip()
        if state != 'deactivating':
            break
        time.sleep(1)
    if state in {'active', 'activating'}:
        return {'resumed': True, 'reason': 'Existing cohort worker continues'}
    result = start_cohort(COHORT)
    return {'resumed': result.returncode == 0, 'exit_code': result.returncode, 'detail': result.stderr.strip()}


def main():
    with (HERE / 'worker.lock').open('a') as worker:
        fcntl.flock(worker, fcntl.LOCK_EX)
        marker = COHORT / 'stop-after-current'
        if marker.exists() and marker.read_text().strip() != TOKEN:
            raise RuntimeError('A different operator already paused the cohort')
        marker.write_text(TOKEN + '\n')
        status = {'topic': TOPIC, 'pid': os.getpid(), 'started': time.time(), 'jobs': {}, 'state': 'running'}
        save(HERE / 'status.json', status)
        try:
            publisher = Publisher.from_environment()
            learner = read(COHORT / 'cohort.json')['learner']
            locks = ROOT / '.local/learning/inventory' / publisher.config.database / learner
            for kp in KPS:
                status.update(active_kp=kp)
                save(HERE / 'status.json', status)
                with (locks / f'kp-{kp}.lock').open('a') as kp_lock:
                    fcntl.flock(kp_lock, fcntl.LOCK_EX)
                    directory = HERE / 'jobs' / str(kp)
                    request = {'kp': kp, 'difficulty': 'unclassified', 'count': 5,
                               'existing_entrypoint': None, 'job_kind': 'build'}
                    pipeline = Pipeline(directory, request, publisher, environment=publisher.client.environment,
                                        session=CohortSession(ROOT, publisher.client.environment))
                    pipeline.max_attempts = pipeline.state.get('manual_repair_max_attempts', 3)
                    pipeline.inherited_lock_fds = (worker.fileno(), kp_lock.fileno())
                    result = pipeline.run('push')
                    while result['stage'] in {'repair', 'report-repair'}:
                        status['jobs'][str(kp)] = {'stage': 'repair', 'error': result.get('error'),
                            'repair_cycle': result.get('repair_cycle', 0), 'evidence': str(pipeline.path)}
                        save(HERE / 'status.json', status)
                        result = pipeline.run('push')
                    status['jobs'][str(kp)] = {'stage': result['stage'], 'registration': result.get('registration'),
                                              'error': result.get('error'), 'evidence': str(pipeline.path)}
                    save(HERE / 'status.json', status)
                    print(json.dumps({'kp': kp, **status['jobs'][str(kp)]}), flush=True)
            with urllib.request.urlopen(f'http://127.0.0.1:8765/api/topic-study-availability?topicId={TOPIC}') as response:
                status['study_availability'] = json.load(response)
            status['state'] = 'verified' if (status['study_availability'].get('available') and
                all(j['stage'] == 'verified' for j in status['jobs'].values())) else 'needs_repair'
        except CapacityUnavailable as error:
            status.update(state='capacity_blocked', error=str(error))
        except Exception as error:
            status.update(state='failed', error=str(error))
        finally:
            status.update(completed=time.time(), active_kp=None)
            status['cohort_resume'] = resume_cohort() if status['state'] == 'verified' else {
                'resumed': False, 'reason': 'Urgent topic remains incomplete; preserve its priority and workspace.'}
            save(HERE / 'status.json', status)
            print(json.dumps(status), flush=True)
        return 0 if status['state'] == 'verified' else 78 if status['state'] == 'capacity_blocked' else 1


if __name__ == '__main__':
    sys.exit(main())
