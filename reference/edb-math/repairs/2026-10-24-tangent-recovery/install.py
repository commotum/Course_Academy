"""Install the independently reviewed tangent repair through the ordinary pipeline.

This is a one-shot recovery, not a retry policy. It preserves the old workspace
and findings, verifies the real review's exact inputs, then queues normal
publication within the existing worker limit. No approval is synthesized here.
"""
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
from generator_review import validate_review
from inventory_jobs import save
from serve_graph_explorer import database_environment

KP = 17592186059664
KEY = 'cea5ef8806843ed0b2bb5238a66a67bd04433f91f5a991d967ed98734da9438d'
PACKAGE = 'e7b15035bab20db925c7ca95b4898285773fae170428ca83c375a3bf94a3bd8e'
JOBS = ROOT / '.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
JOB = JOBS / (KEY + '.json')
DIRECTORY = JOB.with_suffix('.pipeline') / '2'


def main():
    review_root = HERE / 'independent-review'
    report = read(review_root / 'result.json')
    validate_review(report, review_root)
    assert report['verdict'] == 'accepted', 'Independent acceptance is required'
    reviewed = read(review_root / 'reviewed-inputs.json')['binding']
    assert reviewed['package_hash'] == PACKAGE
    assert reviewed['source_hash'] == digest(read(HERE / 'fresh-source/source.json'))
    assert reviewed['inventory_hash'] == digest(read(HERE / 'fresh-source/inventory.json'))
    assert reviewed['batch_hash'] == digest(read(HERE / 'evidence/requested.json'))
    with (JOBS / f'kp-{KP}.lock').open('a') as kp_lock, (DIRECTORY / 'worker.lock').open('a') as worker_lock:
        fcntl.flock(kp_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(worker_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        outer = read(JOB)
        state = read(DIRECTORY / 'job.json')
        assert outer['state'] == 'blocked' and outer['cycle'] == 2
        assert state['stage'] == 'blocked' and state['request']['kp'] == KP
        assert not (DIRECTORY / 'publication/request.json').exists()
        archive = DIRECTORY / 'recovery-tangent-paired-banks'
        archive.mkdir(exist_ok=False)
        for name in ('source', 'workspace'):
            shutil.copytree(DIRECTORY / name, archive / name)
        for name in ('job.json', 'samples.json', 'repair-history.json', 'runtime-dependencies.json', 'repair-preflight.json'):
            if not (DIRECTORY / name).exists():
                continue
            shutil.copy2(DIRECTORY / name, archive / name)
        shutil.copy2(JOB, archive / 'inventory-job.json')

        evidence = None
        evidence_created = False
        try:
            shutil.copytree(HERE / 'package', DIRECTORY / 'workspace', dirs_exist_ok=True)
            shutil.copytree(HERE / 'workspace-regressions', DIRECTORY / 'workspace', dirs_exist_ok=True)
            shutil.copytree(HERE / 'fresh-source', DIRECTORY / 'source', dirs_exist_ok=True)
            environment = database_environment('math')
            publisher = Publisher.from_environment(environment=environment)
            pipeline = Pipeline(DIRECTORY, state['request'], publisher, environment=environment)
            reason = (
                'Installed independently reviewed symmetric tangent answer banks. Retained negative controls '
                'reproduce both historical interval-only and bank-only shape defects; the new executable '
                'checks cover both before and after delivery. The combined exact-family-plus-bounds '
                'criterion is explicitly documented as impossible for the source family, with original '
                'source-bank controls. Old workspace and findings archived intact. Real independent '
                'review is imported only on exact package, batch, source, inventory and engine hash match.'
            )
            pipeline.resume_blocked(reason)
            pipeline.persist(stage='sample', manifest='package.json', author_running=False, error=None,
                             source_hash=reviewed['source_hash'], inventory_hash=reviewed['inventory_hash'],
                             review=None, review_binding=None, review_policy_version=None,
                             approval_recorded=False, report_repair_directory=None,
                             review_report_error=None, review_report_result_file=None)
            assert pipeline.candidate_hash() == PACKAGE
            pipeline.check_repair_regressions()
            pipeline.sample()
            pipeline.persist(stage='validate', package_hash=PACKAGE)
            assert pipeline.review_binding() == reviewed, 'Independent review does not cover these exact inputs'
            pipeline.verify_approval_inputs()
            evidence = pipeline.review_directory()
            assert not evidence.exists(), 'Never overwrite an existing review'
            evidence_created = True
            shutil.copytree(review_root, evidence)
            save(evidence / 'review-binding.json', reviewed)
            save(evidence / 'review-provenance.json', {
                'kind': 'independent-collaborator-review',
                'reviewer': '/root/tangent_independent_review',
                'original_evidence': str(review_root),
                'result_digest': digest(report), 'binding': reviewed,
                'imported_at': time.time(),
                'note': 'Actual independent review; not a synthetic CodexSession execution.'})
            validate_review(read(evidence / 'result.json'), evidence)
        except BaseException as error:
            # Locks are still held and the outer job has not been requeued.
            # Restore the blocked state and its evidence if preflight/import fails.
            for name in ('source', 'workspace'):
                shutil.rmtree(DIRECTORY / name)
                shutil.copytree(archive / name, DIRECTORY / name)
            for name in ('job.json', 'samples.json', 'repair-history.json', 'runtime-dependencies.json', 'repair-preflight.json'):
                if (archive / name).exists():
                    shutil.copy2(archive / name, DIRECTORY / name)
                else:
                    (DIRECTORY / name).unlink(missing_ok=True)
            if evidence_created and evidence is not None and evidence.exists():
                shutil.rmtree(evidence)
            failed_archive = archive.with_name(archive.name + '-failed-' + str(time.time_ns()))
            archive.rename(failed_archive)
            save(HERE / 'installation-failure.json', {
                'error': str(error), 'archive': str(failed_archive),
                'outer_job_requeued': False, 'original_blocked_state_restored': True})
            raise
        with (JOBS / 'jobs.lock').open('a') as jobs_lock:
            fcntl.flock(jobs_lock, fcntl.LOCK_EX)
            current = read(JOB)
            assert current['state'] == 'blocked' and current['cycle'] == 2
            save(JOB, {**current, 'state': 'pending', 'retryAt': 0, 'completedAt': 0,
                       'error': None, 'outcome': {},
                       'manualRecovery': {'at': time.time(), 'reason': reason, 'evidence': str(HERE)}})
        result = {'kp': KP, 'stage': pipeline.state['stage'], 'cycle': 2,
                  'package_hash': PACKAGE, 'review': str(evidence),
                  'source_basis': read(DIRECTORY / 'source/source.json')['basis'],
                  'exact_review_binding': reviewed,
                  'retained_regressions_passed': True,
                  'requeued_through_existing_worker_limit': True}
        save(HERE / 'install-verification.json', result)
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
