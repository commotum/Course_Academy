"""Publish validated replacement packages without changing their old versions."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import uuid

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_packages import build_manifest, manifest_digest, publish_package, verify_package, check_dependencies
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import loads

HERE = Path(__file__).resolve().parent


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')


def prepare():
    publisher = Publisher.from_environment()
    capture = ROOT / (HERE / 'capture-directory.txt').read_text().strip()
    snapshot = loads((capture / 'snapshot.edn').read_text())
    records = []
    for [kp] in snapshot['scope']:
        kid = kp[':db/id']
        old = kp[':knowledge-point/question-generator']
        old_ref = old[':question-generator/script']
        old_directory = publisher.config.math_root / str(Path(old_ref).parent)
        original = verify_package(old_directory, old_directory.name)
        candidate = HERE / 'generators' / str(kid)
        evidence = HERE / 'generator-evidence' / str(kid) / 'verification.json'
        report = json.loads(evidence.read_text())
        assert report.get('status') == 'passed' or report.get('passed') is True
        assert hashlib.sha256((candidate / 'generator.py').read_bytes()).hexdigest() == report['generator_sha256']
        names = sorted(original.manifest['files'])
        for name in names:
            if name != 'generator.py':
                assert (candidate / name).read_bytes() == (old_directory / name).read_bytes()
        manifest = build_manifest(candidate, original.entrypoint, names, dependencies=original.manifest['dependencies'])
        digest = manifest_digest(manifest)
        observed = check_dependencies(manifest['dependencies'], sys.executable)
        records.append({'kp_id': kid, 'source_directory': str(candidate.relative_to(ROOT)),
                        'old_generator_eid': old[':db/id'], 'old_reference': old_ref,
                        'manifest': manifest, 'digest': digest,
                        'reference': f'generators/{digest[:2]}/{digest}/{original.entrypoint}',
                        'generator_uuid': str(uuid.uuid5(kp[':knowledge-point/id'], 'generator-package:' + digest)),
                        'verification_file': str(evidence.relative_to(ROOT)), 'observed_dependencies': observed})
    save('packages-plan.json', {'math_root': str(publisher.config.math_root), 'packages': records})
    print(json.dumps([{'kp_id': r['kp_id'], 'digest': r['digest']} for r in records]))


def publish():
    plan = json.loads((HERE / 'packages-plan.json').read_text())
    publisher = Publisher.from_environment()
    assert str(publisher.config.math_root) == plan['math_root']
    for record in plan['packages']:
        manifest = record['manifest']
        package = publish_package(ROOT / record['source_directory'], manifest['entrypoint'],
                                  manifest['files'], publisher.config.math_root,
                                  dependencies=manifest['dependencies'], expected_digest=record['digest'])
        assert package.reference == record['reference']
        old_directory = publisher.config.math_root / str(Path(record['old_reference']).parent)
        verify_package(old_directory, old_directory.name)
    save('published-packages.json', {**plan, 'all_verified': True, 'old_packages_unchanged': True})
    print(json.dumps({'packages_published': len(plan['packages']), 'old_packages_unchanged': True}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('prepare', 'publish'))
    args = parser.parse_args()
    globals()[args.action]()
