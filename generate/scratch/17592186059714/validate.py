"""Rendered prompt/solution mathematics, complete bank replay, native grading."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('vector_generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

def expression(text):
    # Restricted exact parser for the emitted integer/radical values, independent
    # of generator math. Reject unsupported notation instead of guessing.
    text = text.replace(' ', '').replace(r'\cdot', '*')
    m = re.fullmatch(r'(-?\d*)\\sqrt\{(\d+)\}', text)
    if m:
        return sp.Integer(m[1] or 1) * sp.sqrt(sp.Integer(m[2]))
    if re.fullmatch(r'-?\d+', text):
        return sp.Integer(text)
    raise ValueError('Unexpected exact value: ' + text)

def parse_question(q):
    m = re.search(r'⟨\s*(-?\s*\d+)\s*,\s*(-?\s*\d+)\s*⟩', q[':question/problem'])
    if m is None:
        m = re.search(r'\\langle\s*(-?\s*\d+)\s*,\s*(-?\s*\d+)\s*\\rangle', q[':question/problem'])
    assert m, 'Vector not readable from prompt'
    x, y = [int(t.replace(' ', '')) for t in m.groups()]
    return x, y

def fingerprint(q):
    x, y = parse_question(q)
    return g.fingerprint_squared(x*x + y*y)

def solution_check(q):
    x, y = parse_question(q)
    correct = sp.sqrt(sp.Integer(x*x+y*y))
    assert q.get(':question/worked-solution') and len(q.get(':question/answer-fields', [])) == 1
    solution = q[':question/worked-solution']
    # Independently check every numeric displayed line, including signed squares.
    lines = solution.splitlines()
    numeric = [t for t in lines if t.startswith('&=')]
    assert 3 <= len(numeric) <= 4
    assert re.fullmatch(r'&= \\sqrt\{\((-?\d+)\)\^\{2\} \+ \((-?\d+)\)\^\{2\}\}(?: \\\\)?', numeric[0])
    coords = re.findall(r'\((-?\d+)\)\^\{2\}', numeric[0])
    assert list(map(int, coords)) == [x, y]
    squares = re.search(r'\\sqrt\{(\d+) \+ (\d+)\}', numeric[1])
    assert squares and list(map(int, squares.groups())) == [x*x, y*y]
    summed = re.search(r'\\sqrt\{(\d+)\}', numeric[2])
    assert summed and int(summed[1]) == x*x+y*y
    last = numeric[-1].removeprefix('&= ').removesuffix(' \\\\')
    assert sp.simplify(expression(last)-correct) == 0
    f = q[':question/answer-fields'][0]
    assert f[':answer-field/key'] == 'selection'
    ft = f[':answer-field/type']
    assert ft == ':answer-field.type/radio' or ft[':db/ident'] == ':answer-field.type/radio'
    choices = f[':answer-field/choices']
    assert len(choices) == 5 and len({str(c[':answer/id']) for c in choices}) == 5
    vals = [expression(c[':answer/value']) for c in choices]
    assert all(v.is_real and v.is_positive for v in vals)
    assert len(set(vals)) == 5
    designation = f[':answer-field/correct']
    cid = str(designation[':answer/id'] if isinstance(designation, dict) else designation[1])
    assert [str(c[':answer/id']) for c, v in zip(choices, vals) if sp.simplify(v-correct) == 0] == [cid]
    for c in choices:
        at = c[':answer/type']
        assert at == ':answer.type/math' or at[':db/ident'] == ':answer.type/math'
    return correct

def independent(rec):
    solution_check(rec['question'])
    meta = rec['generation']
    assert rec['knowledge_point']['id'] == g.KP_UUID
    assert rec['question'][':question/difficulty'] == ':question.difficulty/easy'
    assert meta['parameter_fingerprint'] == fingerprint(rec['question'])
    assert rec == g.generate_profile(meta['template'], meta['parameters']['scale'], meta['seed'])
    return True

def checks(rec):
    solution_check(rec['question'])
    f = rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id': a[':answer/id'],
             'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected',
             'purpose': 'Every option in the complete bank'} for a in f[':answer-field/choices']]

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')

def main():
    preview, replay = [], []
    for mid in g.SPECS:
        original = g.ROWS[mid]
        rec = g.generate_profile(mid, 1)
        independent(rec)
        source_bank = original[':question/answer-fields'][0][':answer-field/choices']
        bank = rec['question'][':question/answer-fields'][0][':answer-field/choices']
        assert {expression(a[':answer/value']) for a in source_bank} == {expression(a[':answer/value']) for a in bank}
        assert {a[':answer/value'] for a in source_bank} == {a[':answer/value'] for a in bank}
        assert rec['question'][':question/problem'] == original[':question/problem']
        assert rec['question'][':question/requires-calculator'] == original[':question/requires-calculator']
        replay.append({'source': mid, 'bank_values_matched': 5, 'bank_values_total': 5,
            'distractors_matched': 4, 'complete_bank': True, 'prompt_exact': True,
            'value_notation_exact': True, 'missing_or_extra_options': [],
            'correct_designation': 'Absent in source; independently derived and checked',
            'solution_fidelity': 'Source solution absent; authored using canonical/rated easy solution sequence',
            'difficulty': 'Unrated source; easy authored using rated neighboring evidence'})
        for s in g.SCALES_BY_PROFILE[mid]:
            r = g.generate_profile(mid, s, 923)
            independent(r)
            assert g.generate_profile(mid, s, 17)['question'] == r['question']
            preview.append(r)
    # Independent verification of all available solution-only sources; their
    # unknown response formats remain excluded, with no invented original key.
    support = []
    for mid in ('q-18047', 'q-18048'):
        q = g.ROWS[mid]
        x, y = parse_question(q)
        final = re.findall(r'&\s*=\s*([^&]*?)\\end\{aligned\}', q[':question/worked-solution'])[0].strip().rstrip('.')
        assert expression(final) == sp.sqrt(x*x+y*y)
        support.append({'source': mid, 'solution_correct': True, 'answer_shape': 'missing; not generated or counted as gradable'})
    assert g.batch('easy', 0, 0) == []
    assert g.batch('easy', 100, 1) == g.batch('easy', 100, 1)
    catalog = g.batch('easy', 100, 1)
    assert len(catalog) == len({fingerprint(r['question']) for r in preview}) == 9
    for level in ('moderate', 'hard'):
        try:
            g.batch(level, 5, 0)
        except ValueError:
            pass
        else:
            raise AssertionError('Unsupported level silently generated')
    for mid, s in [('q-1325', 0), ('q-1325', -1), ('q-18046', 4)]:
        try:
            g.generate_profile(mid, s)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid bound accepted')
    # Changed rendered answer/solution/key must fail mathematical validation.
    import copy
    for part in ('answer', 'solution', 'key'):
        broken = copy.deepcopy(preview[0])
        if part == 'answer':
            f = broken['question'][':question/answer-fields'][0]
            next(a for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1])[':answer/value'] = '999'
        elif part == 'solution':
            broken['question'][':question/worked-solution'] = broken['question'][':question/worked-solution'].replace(r'\sqrt{17}', '999')
        else:
            f = broken['question'][':question/answer-fields'][0]
            f[':answer-field/correct'][1] = f[':answer-field/choices'][0][':answer/id']
        try:
            solution_check(broken['question'])
        except (AssertionError, ValueError):
            pass
        else:
            raise AssertionError('Bad ' + part + ' accepted')
    native = [{'label': r['question'][':question/id'], 'record': r, 'checks': checks(r)} for r in preview]
    save('reference/native-input.json', native)
    subprocess.run([str(HERE / 'check-engine'), str(HERE / 'reference/native-input.json'), str(HERE / 'reference/native-report.json')], check=True)
    report = json.loads((HERE / 'reference/native-report.json').read_text())
    assert report['documented_unresolved_checks'] == 0
    build = json.loads((HERE / 'reference/grader-build.json').read_text())
    for name, value in build['engine_sources'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == value
    result = {'status': 'pass', 'source_basis': g.SOURCE['basis'], 'lineage': g.SOURCE['lineage'],
        'source_replay': replay, 'solution_only_evidence': support,
        'complete_banks': 2, 'matched_options': 10, 'matched_distractors': 8,
        'source_original_correct_designations': 0, 'authored_correct_designations_verified': 2,
        'generated_validated': len(preview), 'distinct_tasks': len(catalog),
        'native_grader': 'course_academy_engine::learning::grade_field',
        'native_checks': report['accepted_checks'] + report['rejected_checks'],
        'hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [HERE.with_suffix('.py'), HERE / 'validate.py', HERE / 'source.json', HERE / 'check-engine', HERE / 'reference/grader-build.json', HERE / 'templates.json', HERE / 'capabilities.json', HERE / 'classification.md', HERE / 'template-extraction.md']}}
    save('validation.json', result)
    save('preview.json', preview)
    save('review.json', {'originals': list(g.ROWS.values()), 'generated': preview})
    review = ['# Original and variant review', '', 'Raw originals are retained in source.json. Original ratings, keys, and solutions remain absent where absent. See extraction for authored completions.']
    for mid in g.SPECS:
        q = g.ROWS[mid]
        review += ['', '## Original ' + mid, '', q[':question/problem'], '',
            '\n'.join('- $' + a[':answer/value'] + '$' for a in q[':question/answer-fields'][0][':answer-field/choices'])]
        for s in (1, 2, max(g.SCALES_BY_PROFILE[mid])):
            r = g.generate_profile(mid, s)
            review += ['', '### Scale ' + str(s), '', r['question'][':question/problem'], '',
                '\n'.join('- $' + a[':answer/value'] + '$' for a in r['question'][':question/answer-fields'][0][':answer-field/choices']),
                '', r['question'][':question/worked-solution']]
    (HERE / 'review.md').write_text('\n'.join(review) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'complete_banks', 'matched_options', 'generated_validated', 'distinct_tasks', 'native_checks')}))

if __name__ == '__main__':
    main()
