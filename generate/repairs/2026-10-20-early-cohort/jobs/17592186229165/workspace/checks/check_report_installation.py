"""Regression 645672a4cd3f9bf609ca: installed, scoped evidence for current code.

Never writes outside the workspace or changes runtime files. The inherited
accepted result is a review candidate, not an approval issued by this author.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/home/jake/Developer/Course_Academy')
INSTALLED = ROOT / 'evidence/corrected-review'
OUT = ROOT / 'evidence/report-repair'


def read(path):
    return json.loads(path.read_text())


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    contract = module('review_contract', REPO / 'scripts/generator_review.py')
    regression = module('role_regression', ROOT / 'checks/test_role_exchange.py')
    g = regression.module(ROOT / '17592186229165.py')
    provenance = read(OUT / 'provenance.json')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-root', type=Path,
                        default=Path(provenance['origin']).parent,
                        help='Required installed report root; defaults to the destination in the retained finding')
    args = parser.parse_args()
    runtime_before = {p: digest(ROOT / p) for p in provenance['runtime_sha256']}
    assert runtime_before == provenance['runtime_sha256'], 'Runtime changed since report correction'

    # Fail if installation is absent or stale; do not repair the test's input.
    result = read(INSTALLED / 'review-result.json')
    assert result == read(INSTALLED / 'corrected-accepted-result.json')
    contract.validate_review(result, INSTALLED)
    pv = read(INSTALLED / 'pedagogical-variation.json')
    original_pv = read(OUT / 'original-pedagogical-variation.json')
    original_result = read(OUT / 'original-review-result.json')

    # Reproduce the actual prior contract error without attempting the prohibited
    # external installation. All referenced files are local byte copies.
    with tempfile.TemporaryDirectory(dir=OUT, prefix='original-contract-') as td:
        baseline = Path(td) / 'evidence'
        shutil.copytree(INSTALLED, baseline)
        (baseline / 'pedagogical-variation.json').write_text(json.dumps(original_pv))
        try:
            contract.validate_review(original_result, baseline)
        except ValueError as error:
            original_error = str(error)
        else:
            raise AssertionError('Original report must reproduce the reported failure')
    assert original_error == 'decision_variation has an unresolved decision shortcut', original_error

    # Exercise the actual atomic installation operation at the authorized root.
    # Preserve bytes; a read-only destination must cause this regression to fail.
    report_path = INSTALLED / 'pedagogical-variation.json'
    prior_hash = digest(report_path)
    with tempfile.NamedTemporaryFile(dir=INSTALLED, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(report_path.read_bytes())
    try:
        os.replace(temporary, report_path)
    finally:
        temporary.unlink(missing_ok=True)
    assert digest(report_path) == prior_hash
    contract.validate_review(result, INSTALLED)

    # The shared schema tool is not a runtime dependency of this package.
    schema_command = ['python3', '-c',
        'import json,jsonschema,sys; jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2])))',
        str(report_path), str(REPO / 'generate/pipeline/pedagogical-variation.schema.json')]
    schema = subprocess.run(schema_command, capture_output=True, text=True)
    (OUT / 'schema.log').write_text(schema.stdout + schema.stderr)
    assert schema.returncode == 0, schema.stderr

    historical = read(INSTALLED / 'contract-repair/historical-inventory-shortcut.json')
    defects = [p for p in original_pv['shortcut_probes'] if p['disposition'] == 'defect']
    assert len(defects) == 1 and historical['probe'] == defects[0]
    assert historical['probe']['correct'] == historical['probe']['total'] == 5
    assert historical['resolved_in_stored_inventory'] is False
    assert pv['shortcut_probes'] == [p for p in original_pv['shortcut_probes'] if p['disposition'] != 'defect']
    affected = read(INSTALLED / 'affected-inventory.json')['affected_questions']
    local_affected = read(ROOT / 'affected-inventory.json')['affected_questions']
    assert len(affected) == 4
    assert {(a['question_id'], a['entity_id']) for a in affected} == {(a['question_id'], a['entity_id']) for a in local_affected}
    stored = read(INSTALLED / 'generated-records.json')
    assert stored == read(ROOT / 'evidence/generated-records.json')

    # Replay visible-record evidence against the CURRENT entrypoint. A copied
    # successful report cannot pass when its record content has become stale.
    replay_count = 0
    for name in ['hard-controlled-records.json', 'counterfactual-records.json',
                 'runner-batch.json', 'generated-records.json']:
        for old in read(INSTALLED / name):
            level = old['question'][':question/difficulty'].split('/')[-1]
            meta = old['generation']
            current = g.generate(level, seed=meta['seed'], template=meta['template'],
                                 parameters=meta['parameters'], profile=meta['bank_profile'])
            assert current == old, (name, meta)
            regression.V.validate_record(current, level)
            replay_count += 1
    controlled = read(INSTALLED / 'hard-controlled-records.json')[:3]
    assert [regression.audit(r) for r in controlled] == [0, 1, 1]
    from math_parser import scalar, equal
    answer = lambda r: scalar(r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])
    assert equal(answer(controlled[0]), answer(controlled[1]))
    assert not equal(answer(controlled[0]), answer(controlled[2]))

    seeds = read(INSTALLED / 'controlled-results.json')['fresh_seeds']
    sampled = [g.generate('hard', template='mixed', seed=seed) for seed in seeds]
    captured = read(INSTALLED / 'hard-samples.json')
    for r in sampled:
        assert r in captured, 'Installed evidence does not describe current sampling'
    observed = regression.coverage(sampled)
    assert set(observed['positions']) == {'1', '2'}
    # Independently read displayed rates to check every inherited conditional
    # shortcut count, rather than trusting role labels in generation metadata.
    for probe in pv['shortcut_probes']:
        if not probe['subgroup'].startswith('fresh mixed '):
            continue
        group = probe['subgroup'].removeprefix('fresh mixed ')
        counts = observed['positions'] if group == 'all_fresh_mixed' else observed['cue_groups'][group]
        assert set(counts) == {'1', '2'}, (group, counts)
        assert probe['correct'] == counts['1'] and probe['total'] == sum(counts.values())
        assert abs(probe['baseline'] - max(counts.values()) / sum(counts.values())) < 1e-12

    assert runtime_before == {p: digest(ROOT / p) for p in runtime_before}
    output = {
        'finding': '645672a4cd3f9bf609ca', 'status': 'staged_validation_passed',
        'prior_contract_error_reproduced': original_error,
        'original_external_installation': 'Not retried: outside authorized workspace; saved EROFS evidence retained',
        'installed_root': 'evidence/corrected-review',
        'actual_contract_after_atomic_installation': 'passed', 'schema': 'passed',
        'runtime_unchanged': runtime_before,
        'visible_records_replayed_against_current_generator': replay_count,
        'current_sampler_visible_positions': observed['positions'],
        'all_current_conditional_probe_counts_recomputed': True,
        'historical_probe_preserved_verbatim': True,
        'affected_inventory_uuids_preserved': [a['question_id'] for a in affected],
        'schema_command': schema_command,
        'scope': 'Workspace installation verified. Prior review candidate retained; fresh independent review required. No external evidence-root write, database change, or publication.'
    }
    (OUT / 'staged-validation.json').write_text(json.dumps(output, indent=2) + '\n')
    # Do not conceal the retained installation failure by substituting a writable
    # directory. Default execution must stay red until the REQUIRED destination
    # is corrected by an authorized runner. An explicit local root tests only
    # the staged handoff, and is not used in repair-regressions.json.
    required = args.evidence_root.resolve()
    output['required_evidence_root'] = str(required)
    try:
        installed_result = read(required / 'review-result.json')
        contract.validate_review(installed_result, required)
        assert installed_result == result, 'Required report differs from the saved corrected candidate'
        assert read(required / 'pedagogical-variation.json') == pv, 'Required variation evidence is stale'
    except (OSError, ValueError, AssertionError) as error:
        output['status'] = 'blocked'
        output['required_destination_error'] = str(error)
        (OUT / 'results.json').write_text(json.dumps(output, indent=2) + '\n')
        raise AssertionError('Required external report remains uncorrected; staged validation alone does not close the finding: ' + str(error)) from error
    output['status'] = 'passed'
    (OUT / 'results.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({k: output[k] for k in ['status', 'installed_root', 'visible_records_replayed_against_current_generator', 'current_sampler_visible_positions', 'historical_probe_preserved_verbatim']}))


if __name__ == '__main__':
    main()
