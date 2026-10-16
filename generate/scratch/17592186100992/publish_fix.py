"""Publish the validated structural fix through the shared guarded EDB writer."""
import hashlib
import json
from pathlib import Path
import sys

H = Path(__file__).resolve().parent
ROOT = H.parents[2]
sys.path.insert(0, str(ROOT))
from scripts.generator_packages import publish_package, package_digest
from scripts.generator_publish import Publisher
from capture.scripts.database.client import StaleBasis
import validate as validator


def read(path):
    return json.loads(path.read_text())


def main():
    evidence = H / 'structural-fix'
    validation = read(evidence / 'validation.json')
    assert validation['passed']
    for name, digest in validation['sha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
    assert read(evidence / 'render/rendering.json')['passed']
    package_check = read(evidence / 'package-validation.json')
    assert package_check['passed']
    candidate = evidence / 'package'
    manifest = read(candidate / 'package.json')
    assert package_digest(candidate, manifest['entrypoint'], manifest['files'], dependencies=manifest['dependencies']) == package_check['sha256']
    assert (candidate / 'generator.py').read_bytes() == H.with_suffix('.py').read_bytes()
    records = read(evidence / 'batch.json')
    assert len(records) == 6
    for record in records:
        validator.check(record)
    publisher = Publisher.from_environment()
    # Existing pending publications must be recovered before any new preparation.
    for directory in sorted((evidence / 'publication').glob('attempt-*')):
        if (directory / 'preparation.json').exists() and not (directory / 'stale.json').exists():
            try:
                result = publisher.publish(directory)
            except StaleBasis:
                (directory / 'stale.json').write_text('{"confirmed_stale_basis":true}\n')
            else:
                print(json.dumps(result)); return
    source = publisher.extract_source(validator.g.KP_ID, evidence / 'current-source')
    original = next(q for q in source['material']['kp'][':knowledge-point/questions'] if q[':question/math-academy-id'] == 'q-13536')
    replay = validator.g.generate(parameters=validator.g.ORIGINAL, template=0, roles='ABC')['question']
    assert original[':question/problem'].splitlines()[0] == replay[':question/problem'].splitlines()[0]
    assert validator.parameters(original[':question/problem']) == validator.g.ORIGINAL
    assert original[':question/worked-solution'] == replay[':question/worked-solution']
    expected = sorted(a[':answer/value'] for a in replay[':question/answer-fields'][0][':answer-field/choices'])
    for field in original[':question/answer-fields']:
        assert sorted(a[':answer/value'] for a in field[':answer-field/choices']) == expected
    package = publish_package(candidate, manifest['entrypoint'], manifest['files'], publisher.config.math_root,
                              dependencies=manifest['dependencies'], expected_digest=package_check['sha256'])
    for attempt in range(10):
        directory = evidence / 'publication' / ('attempt-' + str(attempt))
        if directory.exists():
            continue
        publisher.prepare(validator.g.KP_ID, records, package.reference, package.digest, directory,
                          source_snapshot=source, assets_directory=candidate)
        try:
            result = publisher.publish(directory)
        except StaleBasis:
            (directory / 'stale.json').write_text('{"confirmed_stale_basis":true}\n')
            continue
        print(json.dumps(result)); return
    raise RuntimeError('Repeated concurrent writes; retry the same publication command')


if __name__ == '__main__':
    main()
