"""Verify unchanged runtime/evidence and eight independently parsed instances."""
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'checks'))
import test_role_exchange as regression


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    handoff = read(ROOT / 'evidence/review-installation-handoff.json')
    for artifact in handoff['files']:
        assert digest(ROOT / artifact['source']) == artifact['sha256'], artifact['source']
    for name, expected in handoff['runtime_sha256'].items():
        assert digest(ROOT / name) == expected, name
    assert digest(ROOT.parent / 'source/source.json') == read(
        ROOT / 'evidence/source-and-inventory-results.json')['source_sha256']
    generator = regression.module(ROOT / '17592186229165.py')
    records = [generator.generate('easy', seed=i) for i in range(901, 906)]
    records += [generator.generate('moderate', seed=901)]
    records += [generator.generate('hard', template='two_nonresonant', seed=i)
                for i in (901, 902)]
    assert records == read(ROOT / 'evidence/small-regression.json')
    for record in records:
        regression.V.validate_record(record, record['question'][':question/difficulty'].split('/')[-1])
    print(json.dumps({'status': 'passed', 'runtime_unchanged': handoff['runtime_sha256'],
                      'source_unchanged': True, 'handoff_artifacts_verified': len(handoff['files']),
                      'small_unaffected_math_sample_passed': len(records)}))


if __name__ == '__main__':
    main()
