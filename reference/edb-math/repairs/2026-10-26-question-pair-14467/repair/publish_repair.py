"""Publish the verified sampler repair through the normal guarded publisher."""
import fcntl
import json
from pathlib import Path
import sys
import time

D = Path(__file__).resolve().parent
R = next(p for p in D.parents if (p / 'scripts/generator_pipeline.py').is_file())
sys.path.insert(0, str(R / 'scripts'))
from generator_pipeline import Pipeline, read
from generator_packages import publish_package
from generator_publish import Publisher, StaleBasis
from inventory_jobs import save

KP = 17592186087687
JOBS = R / '.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
with (JOBS / f'kp-{KP}.lock').open('a') as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    publisher = Publisher.from_environment(database='math')
    state = read(D / 'job.json')
    pipeline = Pipeline(D, state['request'], publisher, environment=publisher.client.environment)
    pipeline.verify_approval_inputs()
    pipeline.validate_approved_review()
    workspace, manifest = pipeline.manifest()
    package = publish_package(workspace, manifest['entrypoint'], manifest['files'], pipeline.math_root,
        dependencies=manifest['dependencies'], expected_digest=state['package_hash'])
    source = read(D / 'source/source.json')
    original = read(D / 'repair-context.json')['original_registration']
    directory = D / 'publication'
    for attempt in range(3):
        if not (directory / 'request.json').exists() and not (directory / 'verification.json').exists():
            publisher.prepare(KP, read(D / 'samples.json'), package.reference, package.digest,
                directory, source_snapshot=source, assets_directory=state['assets_directory'],
                expected_registered_generator=original)
        try:
            receipt = publisher.publish(directory)
        except StaleBasis:
            if attempt == 2:
                raise
            continue
        break
    pipeline.persist(stage='verified', publication=receipt, registration=package.reference,
                     publication_package_hash=package.digest, publication_batch_hash=state['batch_hash'],
                     completed=time.time(), error=None, needs_repair=False)
    pipeline.record_approval()
    pipeline.persist(approval_recorded=True)
    live = publisher.client.status()
    rows = publisher.client.query(
        '[:find ?script :in $ ?kp :where [?kp :knowledge-point/question-generator ?g] [?g :question-generator/script ?script]]',
        [KP], D / 'live-readback', 'registration', live['basis'])
    assert rows == [[package.reference]], rows
    result = {'passed': True, 'kp': KP, 'registration': package.reference,
              'verified_bands': pipeline.state['verified_bands'], 'publication': receipt,
              'live_basis': live['basis'], 'registered_package_verified': True,
              'sampler_checks': read(D / 'sampler-regression.json'),
              'rendered_final_questions': 15}
    save(D / 'completion.json', result)
    print(json.dumps({key: value for key, value in result.items() if key != 'sampler_checks'}, indent=2))
