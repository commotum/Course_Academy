"""Affected-profile checks plus a small retained-family regression sample."""
import copy
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import generator as g
from review_math import check, correct_index, matrices, prompt, semantic

EVIDENCE = ROOT / 'evidence'


def save(name, value):
    (EVIDENCE / name).write_text(json.dumps(value, indent=2, default=str) + '\n')


def key(record):
    q = record['question']
    f = q[':question/answer-fields'][0]
    return semantic(f[':answer-field/choices'][correct_index(q)][':answer/value'])


def main():
    records = json.loads((EVIDENCE / 'source-records.json').read_text())
    controls = []
    comparisons = []
    # Reassign the mathematical target with the same candidate bank. These cover
    # both newly restored profiles and one unchanged vector family.
    bank = [[-3, 3, -4, 4], [3, -3, 4, -4], [0, 0, 0, 0],
            [0, 2, 0, -4], [1, 0, 4, 0]]
    for profile in ('q-74625', 'q-131634', 'q-74532'):
        base = None
        for index in range(5):
            params = {'candidates': copy.deepcopy(bank), 'correct_index': index,
                      'row_order': [0, 1, 2], 'row_signs': [1, 1, 1]}
            record = g.generate(template=profile, parameters=params, seed=96745)
            assert correct_index(record['question']) == index
            assert not check(record)['errors']
            assert not any(record['question'][':question/id'] == r['question'][':question/id'] for r in controls)
            if base is None:
                base = record
            else:
                assert record['question'][':question/problem'] != base['question'][':question/problem']
                assert record['question'][':question/worked-solution'] != base['question'][':question/worked-solution']
                assert key(record) != key(base)
            controls.append(record)
        irrelevant = g.generate(template=profile, seed=96745, parameters={
            'candidates': copy.deepcopy(bank), 'correct_index': 0,
            'row_order': [2, 0, 1], 'row_signs': [-1, 1, -1]})
        assert prompt(irrelevant['question']) != prompt(base['question'])
        assert key(irrelevant) == key(base)
        assert prompt(irrelevant['question']).rref()[0] == prompt(base['question']).rref()[0]
        assert not check(irrelevant)['errors']
        controls.append(irrelevant)
        comparisons.append({'template': profile, 'fixed_bank_target_slots': list(range(5)),
                            'relevant_prompt_key_solution_changed': True,
                            'equation_order_signs_preserve_response': True})
    small_batch = g.batch('hard', 5, seed=20261021)
    all_records = records + controls + small_batch
    math_results = [check(r) for r in all_records]
    assert not any(r['errors'] for r in math_results), [r for r in math_results if r['errors']]
    save('counterfactual-records.json', controls)
    save('counterfactual-results.json', comparisons)
    save('small-batch.json', small_batch)
    save('math-results.json', {'cases': len(all_records), 'failures': [], 'results': math_results})
    save('delivery-input.json', all_records)
    # Source replay for the originally failing exact commands is also checked by
    # source_coverage.py; keep a small render set of just the affected layouts.
    render = [r for r in records if r['generation']['template'] in ('q-74625', 'q-131634')]
    save('render-input.json', render)

    # Inspect all captured inventory entries for the demonstrated capability
    # defect; also test visible mathematics of all five non-source entries.
    inventory = json.loads((ROOT.parent / 'source/inventory.json').read_text())
    original_ids = {q[':question/id'] for q in g.sources().values()}
    stored_math = []
    for question in inventory['questions']:
        if question[':question/id'] not in original_ids:
            result = check({'question': question, 'generation': {}})
            assert not result['errors'], result
            stored_math.append(result)
    save('affected-inventory.json', {'affected_questions': []})
    save('inventory-results.json', {
        'basis': inventory['basis'], 'inspected': len(inventory['questions']),
        'original_source_questions': sum(q[':question/id'] in original_ids for q in inventory['questions']),
        'other_questions': len(stored_math), 'other_math_checks': stored_math,
        'finding_scan': 'The missing profiles are original source records. A missing replay API capability is not a defect in a stored generated instance; none demonstrated in captured inventory.',
        'limits': 'Captured inventory has no generation metadata. Historical seed reproduction is untested, rather than a verified absence of other defects. No originals marked generated.'})

    # Runtime-only relocation and determinism, not copied evidence dependencies.
    manifest = json.loads((ROOT / 'package.json').read_text())
    assert manifest['dependencies'] == {'python': platform.python_version(), 'packages': {'sympy': g.sp.__version__}}
    args = ['--difficulty', 'hard', '--count', '5', '--seed', '20261021', '--format', 'json']
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
    baseline = subprocess.check_output([sys.executable, str(ROOT / manifest['entrypoint']), *args], env=env)
    with tempfile.TemporaryDirectory(dir=EVIDENCE, prefix='relocation-') as directory:
        target = Path(directory)
        import shutil
        for name in manifest['files']:
            shutil.copyfile(ROOT / name, target / name)
        env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'] = str(target / 'assets')
        moved = subprocess.check_output([sys.executable, str(target / manifest['entrypoint']), *args], cwd=target, env=env)
    assert baseline == moved
    assert json.loads(baseline) == small_batch
    save('packaging-results.json', {'deterministic_replay': True, 'runtime_only_relocation': True,
                                   'dependencies': manifest['dependencies'], 'assets': 'No images or other emitted assets',
                                   'runtime_hashes': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in manifest['files']}})
    print(json.dumps({'math_cases': len(all_records), 'controls': len(controls), 'inventory_other_math': len(stored_math), 'relocation': 'passed'}))


if __name__ == '__main__':
    main()
