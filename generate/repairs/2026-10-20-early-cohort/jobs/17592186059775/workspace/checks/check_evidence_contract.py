"""Finding 9b8cb52352b8ca3e790e: real evidence paths and current-record binding.

Read-only with respect to runtime files and original reviews. Writes evidence only.
The bundle is staged for the runner; this check never installs outside workspace.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

W = Path(__file__).resolve().parents[1]
REPO = Path('/home/jake/Developer/Course_Academy')
JOB = W.parent


def load(p):
    return json.loads(p.read_text())


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bundle', type=Path, default=W/'evidence/contract-correction')
    parser.add_argument('--expected-evidence-root', type=Path)
    args = parser.parse_args()
    bundle = args.bundle.resolve()
    spec = importlib.util.spec_from_file_location('review_validator', REPO/'scripts/generator_review.py')
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    report = load(bundle/'result.json')
    validator.validate_review(report, bundle)
    assert report['verdict'] == 'accepted'
    variation = load(bundle/'pedagogical-variation.json')
    # Schema tooling is installed in the system Python, while runtime checks use
    # the pinned job Python. It is a validation-only dependency.
    subprocess.run(['/usr/bin/python3', '-B', '-c',
                    'import json,jsonschema,sys; '
                    'jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2])))',
                    str(bundle/'pedagogical-variation.json'),
                    str(REPO/'generate/pipeline/pedagogical-variation.schema.json')], check=True)

    # Detect a missing file, with real validator behavior, rather than trusting a
    # previous successful validation report or a copied expected status.
    with tempfile.TemporaryDirectory() as td:
        broken = Path(td)/'bundle'
        shutil.copytree(bundle, broken)
        validator.validate_review(report, broken)  # Simulated runner installation.
        (broken/'correction-provenance.json').unlink()
        try:
            validator.validate_review(report, broken)
        except ValueError as error:
            negative = str(error)
            assert negative == ('source_analysis.evidence_paths: missing, empty, '
                                'or escaping evidence: correction-provenance.json'), negative
        else:
            raise AssertionError('Missing provenance was incorrectly accepted')

    before = load(W/'evidence/evidence-contract-before.json')['runtime_hashes']
    assert all(digest(W/n) == h for n, h in before.items()), 'Reviewed runtime changed'
    source = load(JOB/'source/source.json')['material']['kp']
    originals = {q[':question/id']: q for q in source[':knowledge-point/questions']}
    source_cases = load(bundle/'source-analysis.json')['source_cases']
    for case in source_cases:
        original = originals[case['id']]
        assert case['prompt'] == original[':question/problem']
        assert case['fields'] == original[':question/answer-fields']

    # Actually invoke the current generator, then independently read visible
    # matrices, choices, solution and rank/position counterfactuals.
    sys.path.insert(0, str(W/'checks'))
    from check_batch_selection import g, contrast_bank, strict_shortcut
    current = g.batch('easy', 5, 4258185931)
    assert current == load(bundle/'correction-current-records.json'), 'Stale evidence batch'
    raw = contrast_bank(current)
    delivered = load(bundle/'delivery-batch/accepted.json')
    delivered_check = contrast_bank(delivered, delivered=True)
    assert {r['question'][':question/problem'] for r in current} == {
        r['question'][':question/problem'] for r in delivered}
    try:
        strict_shortcut(load(bundle/'previous-runner-batch.json'))
    except AssertionError as error:
        assert str(error) == 'Reported pivot/rank shortcut answers every member'
    else:
        raise AssertionError('Historical shortcut control stopped reproducing')

    # Affected records contain full question identities and archived generation
    # parameters; do not treat original source captures as generated instances.
    inventory = load(JOB/'source/inventory.json')['questions']
    stored = {q[':question/id']: q for q in inventory}
    generated = {r['question'][':question/id']: r for r in load(bundle/'generated-records.json')}
    affected = load(bundle/'affected-inventory.json')['affected_questions']
    for row in affected:
        r = generated[row['question_id']]
        q = stored[row['question_id']]
        assert r['question'][':question/problem'] == q[':question/problem']
        assert r['generation'], 'Complete generation metadata required'
        assert row['evidence_path'] == 'generated-records.json'

    plan = load(W/'evidence/contract-installation.json')
    if args.expected_evidence_root is not None:
        assert Path(plan['destination_evidence_root']).resolve() == args.expected_evidence_root.resolve(), 'Stale runner evidence destination'
    for row in plan['files']:
        path = (W/row['workspace_source']).resolve()
        assert path.is_relative_to(bundle)
        assert digest(path) == row['sha256'], row['workspace_source']
        assert path.relative_to(bundle).as_posix() == row['destination']
    assert plan['status'] == 'staged_not_installed'
    result = {'finding_id': '9b8cb52352b8ca3e790e', 'passed': True,
              'bundle_root': str(bundle.relative_to(W)),
              'real_review_validator': 'scripts/generator_review.py:validate_review',
              'missing_provenance_negative_control': negative,
              'relocated_bundle_root_validated': True,
              'current_raw': raw['pivot_shortcut'],
              'current_delivered': delivered_check['pivot_shortcut'],
              'historical_control': 'strict check fails as required (5/5)',
              'source_capture_prompts_and_fields_reconfirmed': len(source_cases),
              'affected_generated_records_bound': len(affected),
              'runtime_files_unchanged': len(before),
              'runner_installation_files': len(plan['files']),
              'runner_destination': plan['destination_evidence_root'],
              'destination_installed': False}
    (W/'evidence/evidence-contract-validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
