"""Independent rendered-matrix checks, complete source-bank replay and native grading."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('leading_entries', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, default=str) + '\n')


def inspect(rec):
    """Read displayed prompt/key/solution independently of generation metadata."""
    q = rec['question']
    prompt = q[':question/problem']
    row_numbers = [int(n)-1 for n in re.findall(r'\$(\d)\$(?:st|nd|rd|th)', prompt.split('rows')[0])]
    raw = re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', prompt, re.S)[1]
    matrix = [[int(x) for x in line.split('&')] for line in raw.split('\\\\')]
    assert len(matrix) == 4 and all(len(row) == 4 for row in matrix)
    assert len(row_numbers) in (2, 3) and len(set(row_numbers)) == len(row_numbers)
    locations, numbers = [], []
    for row in row_numbers:
        nonzero = [(j, x) for j, x in enumerate(matrix[row]) if x != 0]
        assert nonzero
        locations.append(nonzero[0][0]); numbers.append(nonzero[0][1])
    answer = sum(numbers)
    fields = q[':question/answer-fields']
    assert len(fields) == 1
    f = fields[0]
    assert f[':answer-field/key'] == 'selection' and f[':answer-field/type'] == ':answer-field.type/radio'
    assert len(f[':answer-field/choices']) == 5
    values = [int(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(set(values)) == 5
    assert all(a[':answer/type'] == ':answer.type/math' for a in f[':answer-field/choices'])
    correct = [a for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1]]
    assert len(correct) == 1 and int(correct[0][':answer/value']) == answer
    assert q[':question/difficulty'] == ':question.difficulty/easy'
    solution = q[':question/worked-solution']
    clause = re.search(r'Therefore, the leading entries of the (.*?) rows of\s+\$A\$ are (.*?), respectively\.', solution, re.S)
    assert clause
    solution_rows = [int(n)-1 for n in re.findall(r'\$(\d)\$(?:st|nd|rd|th)', clause[1])]
    solution_values = [int(v) for v in re.findall(r'\$(-?\d+)\$', clause[2])]
    assert solution_rows == row_numbers and solution_values == numbers
    solution_matrix = re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', solution, re.S)[1]
    assert re.sub(r'\s+', '', solution_matrix) == re.sub(r'\s+', '', raw)
    equation = re.search(r'So, the answer is \$(.*?)\.\$', solution)[1]
    lhs, rhs = equation.split('=')
    # Independent arithmetic parse restricted to signed integers, + and parentheses.
    assert re.fullmatch(r'[0-9+()\-]+', lhs) and int(rhs) == answer
    terms = [int(x) for x in re.findall(r'-?\d+', lhs)]
    assert terms == numbers and sum(terms) == answer
    return {'rows': row_numbers, 'leading_columns': locations, 'leading_values': numbers, 'answer': answer}


def engine_entry(label, rec):
    f = rec['question'][':question/answer-fields'][0]
    return {'label': label, 'record': rec, 'checks': [
        {'submitted_answer_id': a[':answer/id'],
         'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected',
         'purpose': 'Actual learner radio grader; all five displayed choices'} for a in f[':answer-field/choices']]}


def normalized(q):
    def enum(v):
        return v[':db/ident'] if isinstance(v, dict) else v
    out = {k: str(q[k]) for k in (':question/id', ':question/problem', ':question/worked-solution')}
    out[':question/difficulty'] = enum(q[':question/difficulty'])
    out[':question/answer-fields'] = []
    for f in q[':question/answer-fields']:
        correct = f[':answer-field/correct']
        out[':question/answer-fields'].append({':answer-field/id': str(f[':answer-field/id']),
            ':answer-field/key': f[':answer-field/key'], ':answer-field/type': enum(f[':answer-field/type']),
            ':answer-field/correct': [':answer/id', str(correct[':answer/id'])] if isinstance(correct, dict) else correct,
            ':answer-field/choices': sorted([{':answer/id': str(a[':answer/id']), ':answer/type': enum(a[':answer/type']),
                ':answer/value': a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a: a[':answer/value'])})
    return out


def main():
    comparisons, engine, extraction, review = [], [], [], []
    selected = set(); column_coverage = set(); row_coverage = {2: set(), 3: set()}
    for name, case in sorted(g.CASES.items()):
        original = case['source']
        r = g.generate('easy', template=case['template'], parameters=case['parameters'], profile=name, replay=True)
        assert r['question'][':question/problem'] == original[':question/problem']
        sf = original[':question/answer-fields'][0]
        bank = sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
        new = sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
        assert bank == new
        inspect(r)
        if ':answer-field/correct' in sf:
            assert int(sf[':answer-field/correct'][':answer/value']) == case['answer']
        if ':question/worked-solution' in original:
            assert r['question'][':question/worked-solution'] == original[':question/worked-solution']
            inspect({'question': normalized(original)})
        comparisons.append({'source_id': name, 'template': case['template'], 'bank_profile': name,
            'complete_bank': True, 'matched_values': 5, 'matched_distractors': 4,
            'prompt_exact': True, 'solution_exact': ':question/worked-solution' in original,
            'original_key_available': ':answer-field/correct' in sf,
            'missing_key_repair': None if ':answer-field/correct' in sf else str(case['answer'])})
        extraction.append({'source_id': name, 'source_db_id': original[':db/id'],
            'difficulty': original.get(':question/difficulty', 'unrated; inferred easy for replay only'),
            'parameters': case['parameters'], 'template': case['template'], 'bank_profile': name,
            'correct': case['answer'], 'choice_mapping': [{'source_answer': a[':answer/id'],
                'field': sf[':answer-field/id'], 'value': a[':answer/value'],
                'recipe': 'S + (' + str(int(a[':answer/value'])-case['answer']) + ')',
                'interpretation': 'correct sum' if int(a[':answer/value']) == case['answer'] else 'unresolved observed numeric offset',
                'reproduces_complete_value': True} for a in sf[':answer-field/choices']]})
        engine.append(engine_entry('source/' + name, r))
        for seed in range(40):
            variant = g.generate('easy', seed, template=case['template'], profile=name)
            assert variant == g.generate('easy', seed, template=case['template'], profile=name)
            data = inspect(variant)
            selected.add(variant['generation']['bank_profile'])
            column_coverage.update(data['leading_columns'])
            row_coverage[len(data['rows'])].add(tuple(data['rows']))
            engine.append(engine_entry(name + '/seed/' + str(seed), variant))
            if seed == 7:
                review.append({'source_id': name, 'original': original, 'variant': variant})
    # Hold every matrix value fixed while changing each eligible target subset.
    fixed = [[-3, 5, 1, 2], [0, 4, 5, 0], [0, -6, 0, 5], [0, 0, 2, -3]]
    target_checks = []
    for n in (2, 3):
        profile = next(k for k, c in g.CASES.items() if len(c['parameters']['rows']) == n)
        for rows in itertools.combinations(range(4), n):
            r = g.generate(parameters={'matrix': fixed, 'rows': list(rows)}, profile=profile)
            data = inspect(r)
            assert data['answer'] == sum(next(x for x in fixed[row] if x) for row in rows)
            target_checks.append(data)
            engine.append(engine_entry('changed-target/' + str(rows), r))
    # Every row/leading-column boundary, both signs and full integer bounds.
    boundaries = 0
    for col in range(4):
        for sign in (-1, 1):
            matrix = [[0]*col + [sign*(9-i)] + [0]*(3-col) for i in range(4)]
            for n in (2, 3):
                profile = next(k for k, c in g.CASES.items() if len(c['parameters']['rows']) == n)
                r = g.generate(parameters={'matrix': matrix, 'rows': list(range(n))}, profile=profile)
                inspect(r); boundaries += 1
                engine.append(engine_entry('boundary/' + str((col, sign, n)), r))
    invalid = 0
    for kwargs in ({'level': 'moderate'}, {'level': 'hard'}, {'parameters': {'matrix': [[0]*4]*4, 'rows': [0, 1]}},
                   {'parameters': {'matrix': fixed, 'rows': [0, 0]}}, {'template': 'sum_4_rows'}):
        try:
            g.generate(**kwargs)
        except ValueError:
            invalid += 1
        else:
            raise AssertionError('Invalid input accepted')
    assert invalid == 5 and selected == set(g.CASES) and column_coverage == set(range(4))
    assert all(row_coverage[n] == set(itertools.combinations(range(4), n)) for n in (2, 3))
    # A seed or option order never creates semantic novelty; unqueried rows ignored.
    p = {'matrix': fixed, 'rows': [0, 1]}
    modified = json.loads(json.dumps(p)); modified['matrix'][3][3] = 9
    assert g.task_fingerprint(p) == g.task_fingerprint(modified)
    save(HERE/'engine-input.json', engine)
    binary = ROOT/'generate/runs/current/check-engine'
    subprocess.run([str(binary), str(HERE/'engine-input.json'), str(HERE/'engine.json')], check=True)
    native = json.loads((HERE/'engine.json').read_text())
    assert native['accepted_checks'] == len(engine) and native['rejected_checks'] == 4*len(engine)
    assert native['documented_unresolved_checks'] == 0
    save(HERE/'extraction.json', extraction)
    save(HERE/'source-fidelity.json', comparisons)
    save(HERE/'review.json', review)
    (HERE/'review.md').write_text('\n\n---\n\n'.join('Source '+x['source_id']+'\n\n'+
        x['original'][':question/problem']+'\n\nOriginal bank: '+', '.join(a[':answer/value'] for a in x['original'][':question/answer-fields'][0][':answer-field/choices'])+
        '\n\nGenerated variant\n\n'+g.markdown(x['variant']) for x in review))
    save(HERE/'validation.json', {'status': 'pass', 'source_basis': g.SOURCE['basis'], 'lineage': g.LINEAGE,
        'source_practice': len(comparisons), 'complete_banks_matched': len(comparisons),
        'source_values_matched': 5*len(comparisons), 'source_distractors_matched': 4*len(comparisons),
        'missing_or_extra_options': [], 'observed_correct_designations_matched': sum(c['original_key_available'] for c in comparisons),
        'unrated_missing_key_solution_sources': ['q-42362', 'q-42363'],
        'normal_samples': 40*len(comparisons), 'selected_bank_profiles': sorted(selected),
        'row_subset_coverage': {str(n): sorted(v) for n, v in row_coverage.items()},
        'leading_column_coverage': sorted(column_coverage), 'fixed_matrix_changed_targets': target_checks,
        'boundary_cases': boundaries, 'invalid_inputs_rejected': invalid,
        'grader': {'entry_point': native['entry_point'], 'accepted': native['accepted_checks'],
                   'rejected': native['rejected_checks'], 'unresolved': 0,
                   'binary_sha256': hashlib.sha256(binary.read_bytes()).hexdigest()},
        'fidelity_limits': ['Two unrated records have no original key or solution; these are inferred/authored only for replay and never revised in EDB.',
            'Choice-bank numeric offsets reproduce every source option; cognitive interpretations remain unresolved.',
            'Normal translated choice banks and expanded row/leading-column slots are declared same-method generalizations.',
            'No moderate or hard source family; unsupported bands remain explicit.']})
    print(json.dumps({'status': 'pass', 'complete_source_banks': len(comparisons), 'native_records': len(engine)}))


if __name__ == '__main__':
    main()
