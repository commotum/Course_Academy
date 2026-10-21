"""Executable retained-finding regressions using independently parsed visible math.

No services or database writes. Evidence is written under workspace/evidence.
Run with the job Python from any directory.
"""
import sys
sys.dont_write_bytecode = True
import importlib.util
import json
import re
from pathlib import Path
import sympy as S

ROOT = Path(__file__).resolve().parent.parent / 'workspace'
E = Path(__file__).resolve().parent / 'author-check'
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location('candidate', ROOT / '17592186105746.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
x, y = S.symbols('x y')

def save(name, value):
    E.mkdir(exist_ok=True)
    (E / name).write_text(json.dumps(value, indent=2, default=str) + '\n')

def expr(value):
    value = value.strip().rstrip('.,').replace('&', '').replace(' ', '').replace(r'\,', '')
    value = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', value)
    value = re.sub(r'(\d|\))(?=[xy])', r'\1*', value)
    return S.sympify(value, locals={'x': x, 'y': y})

def equations(q):
    body = re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', q[':question/problem'], re.S)[1]
    rows = []
    for row in body.split(r'\\'):
        lhs, rhs = row.split('=')
        z = expr(lhs)
        rows.append([z.coeff(x), z.coeff(y), expr(rhs)])
    return S.Matrix(rows)

def matrices(text):
    pattern = r'\\begin\{(bmatrix|array)\}(?:\{[c|]+\})?(.*?)\\end\{\1\}'
    return [S.Matrix([[expr(v) for v in row.split('&')] for row in m[2].split(r'\\')])
            for m in re.finditer(pattern, text, re.S)]

def bank(r):
    return [a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]

def answer_signature(value):
    if value == 'No solution': return ('none',)
    m = matrices(value)
    assert len(m) == 2 and m[0] == S.Matrix([x, y]) and m[1].shape == (2, 1)
    return tuple(S.expand(v) for v in m[1])

def correct_value(r):
    f = r['question'][':question/answer-fields'][0]
    return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1])

def independent(r):
    q = r['question']; a = equations(q)
    meta = r['generation']
    # Published records may have canonical publisher-owned IDs; compare replay
    # only on authored records (delivered IDs are intentionally replaced).
    replay = g.generate(q[':question/difficulty'].split('/')[-1], meta['seed'], meta['template'], meta['parameters'])
    assert bank(r) == bank(replay)
    assert q[':question/problem'] == replay['question'][':question/problem']
    assert q[':question/worked-solution'] == replay['question'][':question/worked-solution']
    assert a.shape == (2, 3) and a[:, :2].rank() == 1 and a[0, 0] != 0
    consistent = a.rank() == a[:, :2].rank()
    f = q[':question/answer-fields'][0]
    assert len(q[':question/answer-fields']) == 1 and f[':answer-field/key'] == 'selection'
    assert f[':answer-field/type'] == ':answer-field.type/radio' and len(bank(r)) == 5
    signatures = [answer_signature(v) for v in bank(r)]
    assert len(set(signatures)) == 5, ('duplicate choices', r['generation'])
    valid = []
    for i, sig in enumerate(signatures):
        if sig == ('none',): ok = not consistent
        else:
            # Must be the full free-parameter family, not a single point that
            # merely satisfies a row for one value of the parameter.
            ok = consistent and sig[1] == y and all(S.expand(v) == 0 for v in a[:, :2] * S.Matrix(sig) - a[:, 2])
        if ok: valid.append(i)
    assert len(valid) == 1, ('not unique', r['generation'], valid)
    assert f[':answer-field/choices'][valid[0]][':answer/id'] == f[':answer-field/correct'][1]
    sol = q[':question/worked-solution']
    mats = [m for m in matrices(sol) if m.shape == (2, 3)]
    assert mats and mats[0] == a, ('initial matrix', r['generation'])
    previous = a
    for m in mats[1:]:
        normalized = previous.copy(); normalized[0, :] = previous[0, :] / previous[0, 0]
        eliminated = previous.copy(); eliminated[1, :] -= previous[1, 0] / previous[0, 0] * previous[0, :]
        assert m == previous or m == normalized or m == eliminated, ('invalid row step', r['generation'])
        previous = m
    assert previous[0, 0] == 1 and previous[1, 0] == previous[1, 1] == 0
    expected_x = S.expand((a[0, 2] - a[0, 1] * y) / a[0, 0])
    residual = S.simplify(a[1, 2] - a[1, 0] * a[0, 2] / a[0, 0])
    assert previous[1, 2] == residual
    # Read the displayed reduced systems without relying on generation metadata.
    scalar_systems = 0
    for body in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', sol, re.S):
        if r'\begin{' in body or ':=' in body: continue
        for row in body.split(r'\\'):
            lhs, rhs = row.split('='); lhs, rhs = expr(lhs), expr(rhs)
            if lhs.has(x): assert S.expand(S.solve(lhs - rhs, x)[0] - expected_x) == 0
            elif lhs == y: assert rhs == y
            else: assert lhs == 0 and rhs == residual
        scalar_systems += 1
    assert scalar_systems >= 1
    if consistent:
        vv = [m for m in matrices(sol) if m.shape == (2, 1)]
        assert vv and vv[-1] == S.Matrix([expected_x, y])
        assert 'basic variable' in sol and 'free variable' in sol and 'arbitrary number' in sol
    else:
        assert 'no solution' in sol and 'false statement' in sol
        contradictions = re.findall(r'(?<![\w])0(?:x\+0y)?=([^,$]+)', sol)
        assert contradictions and all(expr(v) == residual for v in contradictions)
    return {'question_id': q[':question/id'], 'template': r['generation']['template'],
            'matrix': a.tolist(), 'consistent': bool(consistent), 'valid_index': valid[0], 'passed': True}

def main():
    # Same captured source used by the runner, not the generator's partial old snapshot.
    source_path = ROOT.parent / 'source/source.json'
    if not source_path.exists():
        raise AssertionError('Runner-supplied source capture is required for source replay regression')
    source = json.loads(source_path.read_text())['material']['kp'][':knowledge-point/questions']
    replays = []; records = []; report = []; pairs = []
    from math_format import normalize_prose, normalize_tex
    for old in source:
        sid = old[':question/math-academy-id']; level = old[':question/difficulty'][':db/ident'].split('/')[-1]
        r = g.generate(level, 7331, sid, {'rhs_scale': 1}); independent(r)
        q = r['question']; of = old[':question/answer-fields'][0]
        assert q[':question/problem'] == normalize_prose(old[':question/problem'])
        assert sorted(bank(r)) == sorted(normalize_tex(a[':answer/value']) if a[':answer/type'][':db/ident'].endswith('/math') else a[':answer/value'] for a in of[':answer-field/choices'])
        assert correct_value(r) == normalize_tex(of[':answer-field/correct'][':answer/value'])
        expected = old[':question/worked-solution']
        if sid == 'q-42159': expected = expected.replace(r'1 & 7 & 4 \\ 6 & 42 & -24', r'1 & 7 & 4 \\ 6 & 42 & 24')
        if sid == 'q-130924': expected = expected.replace(r'-3 & 10 & 6', r'-3 & 12 & 6')
        # Presentation conversion only: construct expected explicit augmentation
        # independently of the generator's corresponding normalization helper.
        def augmented(m):
            body = m[1]
            return r'\left[\begin{array}{cc|c}' + body + r'\end{array}\right]' if len(body.split(r'\\')[0].split('&')) == 3 else m[0]
        expected = re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', augmented, expected, flags=re.S)
        assert re.sub(r'\s+', '', q[':question/worked-solution']) == re.sub(r'\s+', '', normalize_prose(expected)), sid
        replays.append({'source_id': old[':question/id'], 'profile': sid, 'prompt': True, 'complete_mathematical_bank': True, 'correct_value': True, 'corrected_solution': True})
        records.append(r)
        # Every source coefficient signature, signed and zero intercepts; the
        # relevant evidence alone switches consistency and leaves the bank fixed.
        for c in [-8, 0, 8]:
            rr = [g.generate(level, 7331, sid, {'intercept': c, 'residual': delta}) for delta in [0, -6 if c < 0 else 6]]
            aa, bb = [equations(v['question']) for v in rr]
            assert aa[:, :2] == bb[:, :2] and aa[0, :] == bb[0, :]
            assert bank(rr[0]) == bank(rr[1])
            assert correct_value(rr[0]) != correct_value(rr[1])
            checks = [independent(v) for v in rr]
            assert [v['consistent'] for v in checks] == [True, False]
            assert rr[0]['question'][':question/worked-solution'] != rr[1]['question'][':question/worked-solution']
            report.extend(checks); records.extend(rr)
            pairs.append({'profile': sid, 'intercept': c, 'records': [v['question'][':question/id'] for v in rr], 'bank_unchanged': True, 'decisive_RHS_only_changed': True})
        # Exercise the default role sampler, not only forced parameter paths.
        normal = [g.generate(level, seed, sid) for seed in [0, 1]]
        assert {independent(v)['consistent'] for v in normal} == {False, True}
        scaled = [g.generate(level, seed, sid, {'rhs_scale': 2}) for seed in [0, 1]]
        assert {independent(v)['consistent'] for v in scaled} == {False, True}
        records.extend(normal + scaled)
    # Exact counterexample retained, then the newly available controlled pair.
    old = g.generate('easy', 7331, 'q-42157', {'rhs_scale': 2, 'second_rhs': -20})
    assert equations(old['question']) == S.Matrix([[1, -6, 4], [-4, 24, -20]])
    # Retain the review's exact eight-scale cue probe as well. Non-original
    # scales must not freeze the decision, even with the seed held constant.
    scale_probe = [g.generate('easy', 7331, 'q-42157', {'rhs_scale': t}) for t in [-4,-3,-2,-1,1,2,3,4]]
    assert {independent(v)['consistent'] for v in scale_probe} == {False, True}
    records.extend(scale_probe)
    exact = [g.generate('easy', 7331, 'q-42157', {'rhs_scale': 1, 'second_rhs': v}) for v in [-10, -8]]
    assert [equations(v['question']) for v in exact] == [S.Matrix([[1, -6, 2], [-4, 24, -10]]), S.Matrix([[1, -6, 2], [-4, 24, -8]])]
    assert bank(exact[0]) == bank(exact[1]) and correct_value(exact[0]) == 'No solution'
    assert answer_signature(correct_value(exact[1])) == (2 + 6*y, y)
    irrelevant = g.generate('easy', 7331, 'q-42157', {'intercept': 2, 'residual': 3})
    assert correct_value(irrelevant) == correct_value(exact[0])
    assert sorted(bank(irrelevant)) == sorted(bank(exact[0]))
    records.extend([old, *exact, irrelevant])
    # A few legacy scales verify the completed scaling/matrix typo repairs survive.
    for sid, t in [('q-42159', -4), ('q-130924', 4), ('q-20964', -4)]:
        level = 'moderate' if sid == 'q-130924' else 'easy'
        records.append(g.generate(level, 7331, sid, {'rhs_scale': t}))
    all_checks = [independent(r) for r in records]
    # Complete native-grader cases derive their expectation from parsed math.
    inputs = []
    for i, (r, check) in enumerate(zip(records, all_checks)):
        choices = r['question'][':question/answer-fields'][0][':answer-field/choices']
        inputs.append({'label': f'independent {i} {check["template"]}', 'record': r, 'checks': [
            {'submitted_answer_id': option[':answer/id'], 'expected': 'accepted' if j == check['valid_index'] else 'rejected', 'purpose': 'independently solved complete bank'}
            for j, option in enumerate(choices)]})
    save('source-replay.json', {'passed': True, 'cases': replays})
    save('regression-records.json', records)
    save('math-results.json', all_checks)
    save('counterfactual-results.json', {'passed': True, 'pairs': pairs, 'exact_pair': [v['question'][':question/id'] for v in exact], 'irrelevant_residual_preserves_no_solution': True})
    save('grader-input.json', inputs)
    easy = [r for r in records[17:] if r['question'][':question/difficulty'].endswith('/easy')]
    # Use only the controlled-grid records (not the interleaved replays/defaults)
    # for exact paired cue comparisons after the publisher's filters.
    controlled = [g.generate('easy', 7331, old[':question/math-academy-id'], {'intercept': c, 'residual': delta})
        for old in source if old[':question/difficulty'][':db/ident'].endswith('/easy')
        for c in [-8, 0, 8] for delta in [0, -6 if c < 0 else 6]]
    save('delivery-input.json', controlled)
    save('render-input.json', [exact[0], exact[1], g.generate('easy', 7331, 'q-20964', {'rhs_scale': 1}), g.generate('easy', 7331, 'q-20783', {'intercept': 0, 'residual': 0}), g.generate('moderate', 7331, 'q-130924', {'intercept': -8, 'residual': -6})])
    save('repair-regression-results.json', {'passed': True, 'findings': ['5bda1794e02541c06117', 'a8a813a755862016dfa8'], 'source_cases': len(replays), 'controlled_pairs': len(pairs), 'independent_records': len(all_checks), 'default_sampler_outcomes_per_profile': 'both', 'scaled_sampler_outcomes_per_profile': 'both', 'original_review_eight_scale_probe': 'passed', 'metadata_mathematical_replay': True, 'native_grader_checks_prepared': len(inputs)*5})
    print(json.dumps({'passed': True, 'source_cases': len(replays), 'controlled_pairs': len(pairs), 'independent_records': len(all_checks)}))

if __name__ == '__main__': main()
