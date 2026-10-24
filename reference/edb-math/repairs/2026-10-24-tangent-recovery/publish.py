"""Complete the reviewed manual repair with the normal guarded publisher.

No additional author/reviewer process is permitted. A queued worker may instead
win the KP lock and complete the same durable pipeline normally.
"""
from pathlib import Path
import fcntl
import json
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_pipeline import Pipeline, read
from generator_publish import Publisher
from inventory_jobs import InventoryJobs, save
from serve_graph_explorer import database_environment
from install import DIRECTORY, JOB, JOBS, KP, PACKAGE


def completed_review_only(role, context, directory):
    assert role == 'review', 'Manual publication cannot launch an author'
    directory = Path(directory)
    assert read(directory / 'review-binding.json') == context['review_binding']
    assert read(directory / 'review-provenance.json')['reviewer'] == '/root/tangent_independent_review'
    return read(directory / 'result.json')


def main():
    environment = database_environment('math')
    publisher = Publisher.from_environment(environment=environment)
    with (JOBS / f'kp-{KP}.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        state = read(DIRECTORY / 'job.json')
        assert state['package_hash'] == PACKAGE
        assert state['stage'] in ('validate', 'prepare', 'push', 'verified')
        pipeline = Pipeline(DIRECTORY, state['request'], publisher,
                            environment=environment, session=completed_review_only)
        result = pipeline.run()
        assert result['stage'] == 'verified' and result['approval_recorded']
        outcome = {'outcome': 'generated', 'evidence': str(DIRECTORY / 'job.json'),
                   'generator': result['registration'], 'publication': result['publication'],
                   'needs_repair': False, 'difficulty': result['effective_difficulty'],
                   'package': None, 'reason': None}
        if read(JOB).get('cycle') == 2:
            save(JOB.with_suffix('.result'), outcome)
            InventoryJobs(ROOT, JOBS, read(JOB)['learner'], environment).finish(
                JOB, {'state': 'awaiting-verification', 'completedAt': time.time(),
                      'error': None, 'exitCode': 0, 'outcome': outcome}, cycle=2)
        status = publisher.client.status()
        kp = publisher.read_kp(KP, HERE / 'live-readback', status['basis'])
        # The normal publication filter assigns canonical content identities.
        # Read back its accepted records, not the generator's provisional IDs.
        wanted = {q['question'][':question/id'] for q in read(DIRECTORY / 'publication/preparation.json')['records']}
        actual = {str(q[':question/id']) for q in kp[':knowledge-point/questions']}
        assert wanted <= actual
        assert kp[':knowledge-point/question-generator'][':question-generator/script'] == result['registration']
        approval = read(pipeline.approval_path())
        assert approval['bands']['moderate']['review_policy_version'] == 4
        verification = {'passed': True, 'kp': KP, 'package_hash': PACKAGE,
                        'publication': result['publication'], 'readback_basis': status['basis'],
                        'exact_question_ids_present': sorted(wanted),
                        'registration': result['registration'], 'approval_policy': 4,
                        'additional_author_or_review_processes': 0,
                        'completion': 'Normal pipeline publication from the independently reviewed manual repair'}
        save(HERE / 'publication-verification.json', verification)
        print(json.dumps(verification, indent=2))


if __name__ == '__main__':
    main()
