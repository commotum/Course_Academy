"""Independent printed-record witnesses for the three retained findings.

Run with the job Python from any cwd. Writes evidence only; never runtime files.
"""
import collections
import json
import pathlib
import sys

sys.dont_write_bytecode = True
from printed_math import g, s, k, x, y, equations, parse, printed_check

W = pathlib.Path(__file__).resolve().parent.parent
E = W / 'evidence'
SOURCE = W.parent / 'source/source.json'

def write(name, data):
    E.mkdir(exist_ok=True)
    (E / name).write_text(json.dumps(data, indent=2, default=str) + '\n')

def field(r):
    return r['question'][':question/answer-fields'][0]

def value(a):
    return parse(a[':answer/value'].split('=', 1)[1])

def root(r):
    rr = equations(r['question'][':question/problem'])
    A, b = s.linear_eq_to_matrix(rr, [x, y])
    roots = s.solve(A.det(), k)
    assert len(roots) == 1
    return roots[0]

def probes(records):
    groups = collections.defaultdict(list)
    for r in records:
        rr = equations(r['question'][':question/problem'])
        A, _ = s.linear_eq_to_matrix(rr, [x, y])
        # Infer recognizable family and sign entirely from the displayed data.
        target = 'dependent' if 'consistent dependent' in r['question'][':question/problem'] else 'inconsistent'
        if target == 'inconsistent':
            form = ('scaled' if abs(s.diff(A[1, 1], k)) != 1 else 'unit') + ('_shift' if A[1, 1].subs(k, 0) else '_bare')
            level = r['question'][':question/difficulty'].split('/')[-1]
            group = level + ':' + form
        else:
            form = ('negative' if s.diff(A[1, 1], k) < 0 else 'fractional' if (A[1, 0] / A[0, 0]).q != 1 and A[1, 0] != 1 else 'swap')
            group = 'hard:' + form
        sign = 'same_sign' if A[1, 0] * A[0, 1] / A[0, 0] > 0 else 'opposite_sign'
        f = field(r); choices = f[':answer-field/choices']; correct = f[':answer-field/correct'][1]
        ordered = sorted(choices, key=value)
        rank = next(j for j, a in enumerate(ordered) if a[':answer/id'] == correct)
        pos = next(j for j, a in enumerate(choices) if a[':answer/id'] == correct)
        predicted = (max if sign == 'same_sign' else min)(choices, key=value)
        for name in [group, group + ':' + sign]:
            groups[name].append((rank, pos, predicted[':answer/id'] == correct, str(root(r))))
    result = {}
    for name, rows in groups.items():
        ranks = collections.Counter(z[0] for z in rows); positions = collections.Counter(z[1] for z in rows)
        result[name] = dict(total=len(rows), numeric_ranks=dict(ranks), display_positions=dict(positions), sign_extremum_successes=sum(z[2] for z in rows), distinct_roots=len({z[3] for z in rows}), fixed_rank_best=max(ranks.values()), fixed_position_best=max(positions.values()), blind_baseline=0.2)
    return result

def source_replay():
    material = json.loads(SOURCE.read_text())['material']
    sources = material['kp'][':knowledge-point/questions']
    specs = json.loads((W / '17592186115242/recipes.json').read_text())
    report = []; records = []
    for source in sources:
        sid = source[':question/math-academy-id']; spec = specs[sid]
        rr = equations(source[':question/problem']); A, b = s.linear_eq_to_matrix(rr, [x, y])
        p = dict(a=int(A[0, 0]), b=int(A[0, 1]), c=int(b[0]), d=int(A[1, 0]), u=int(s.diff(A[1, 1], k)), v=int(A[1, 1].subs(k, 0)), e=int(b[1]))
        level = source[':question/difficulty'][':db/ident'].split('/')[-1]
        r = g.generate(level, seed=932455, profile=sid, parameters=p)
        t = printed_check(r)
        assert all(s.expand(a-b) == 0 for a, b in zip(rr, equations(r['question'][':question/problem'])))
        sf = source[':question/answer-fields'][0]; f = field(r)
        assert {value(a) for a in sf[':answer-field/choices']} == {value(a) for a in f[':answer-field/choices']}
        assert value(sf[':answer-field/correct']) == t
        assert r['generation']['bank_variant'] == 'observed'
        # Full solution wording is retained after documented mathematical and
        # presentation repairs, rather than only comparing the answer.
        raw = source[':question/worked-solution']
        if sid == 'q-74695': raw = raw.replace('x+ky=2', 'x+ky=-2').replace('x+ky &=2', 'x+ky &=-2')
        if sid == 'q-42021': raw = raw.replace('1 & 2 & -3', '1 & 2 & 3').replace('1-2y=3', 'x+2y=3').replace('1-2y &=3', 'x+2y &=3')
        if sid == 'q-74691': raw = raw.replace('2x+2y=4', '2x-2y=4').replace('$y$,.', '$y$.')
        import re
        raw = g.normalize_prose(raw)
        raw = re.sub(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', lambda m: g.matrix([[v.strip() for v in row.split('&')] for row in m[1].split(r'\\')]), raw, flags=re.S)
        # Ignore aligned-column marker placement; equations and every matrix are
        # independently checked above and by printed_check.
        def wording(z): return re.sub(r'\s+', '', g.normalize_system_braces(z)).replace('&', '')
        assert wording(raw) == wording(r['question'][':question/worked-solution']), sid
        report.append(dict(source=sid, question_id=source[':question/id'], complete_bank=True, matched_choices=5, matched_distractors=4, solution_wording=True, root=str(t)))
        records.append(r)
        # An explicitly requested observed profile also generalizes to new data.
        changed = g.generate(level, seed=102, profile=sid)
        printed_check(changed); records.append(changed)
    canonical = material['kp'][':knowledge-point/canonical-example']
    r = g.generate('moderate', seed=11, template='inconsistent_bare', parameters=dict(a=2,b=-2,c=1,d=4,u=1,v=0,e=-3))
    assert all(s.expand(a-b) == 0 for a,b in zip(equations(canonical[':question/problem']),equations(r['question'][':question/problem'])))
    assert printed_check(r) == -4
    records.append(r)
    write('source-replays.json', records)
    write('source-replay-report.json', dict(passed=True, practice_banks=len(report), choices=5*len(report), canonical_system=True, cases=report))
    return records

def zero_cases():
    cases = [
        ('moderate','inconsistent_shift',dict(a=1,b=2,c=1,d=2,u=1,v=4,e=3)),
        ('moderate','inconsistent_scaled_shift',dict(a=1,b=2,c=1,d=2,u=2,v=4,e=3)),
        ('hard','dependent_fractional',dict(a=2,b=2,c=4,d=3,u=1,v=3,e=6)),
        ('hard','dependent_negative',dict(a=1,b=2,c=1,d=-2,u=-1,v=-4,e=-2)),
    ]
    profiles = {'inconsistent_shift':'q-42059','inconsistent_scaled_shift':'q-131728','dependent_fractional':'q-131731','dependent_negative':'q-42021'}
    records = []
    for level, template, params in cases:
        for profile in [None, profiles[template]]:
            r = g.generate(level, seed=932455, template=template, parameters=params, profile=profile)
            assert printed_check(r) == 0
            records.append(r)
    # Bare hard fractional source parameters must work without a replay profile.
    r = g.generate('hard', seed=932455, template='dependent_fractional', parameters=dict(a=2,b=-2,c=4,d=-3,u=1,v=0,e=-6))
    assert printed_check(r) == 3; records.append(r)
    write('boundary-records.json', records)
    return records

def counterfactuals():
    base = dict(a=1,b=2,c=1,d=2,u=1,v=3,e=3)
    records = [g.generate('moderate', seed=713, template='inconsistent_shift', parameters=p) for p in [base,dict(base,v=1),dict(base,e=4),dict(base,v=4)]]
    roots = list(map(printed_check, records)); assert roots == [1,3,1,0]
    # Keep seed and bank profile fixed so old and new answers remain present:
    # grader must now reject k=1 where it previously accepted it.
    assert any(value(a) == 1 for a in field(records[1])[':answer-field/choices'])
    write('counterfactual-records.json',records)
    write('counterfactual-results.json',dict(passed=True, roots=roots, relevant='v=3 -> 1 -> 4 changes root 1 -> 3 -> 0', irrelevant='e=3 -> 4 preserves root 1; both residuals nonzero'))
    return records

def main():
    sources = source_replay(); boundaries = zero_cases(); cf = counterfactuals()
    sample = [g.generate('easy', seed=seed) for seed in range(932401,932449)]
    # Small regression sample for unaffected backbone families; source profiles
    # above independently exercise their original and changed parameters.
    for level in ['moderate','hard']:
        for template in g.TEMPLATES[level]:
            sample += [g.generate(level, seed=seed, template=template) for seed in range(932401,932409)]
    for r in sample: printed_check(r)
    before = probes(sample)
    easy = {n:z for n,z in before.items() if n.startswith('easy:')}
    for name, stats in easy.items():
        ranks = {int(i) for i in stats['numeric_ranks']}
        assert ranks & {0,4} and ranks & {1,2,3}, (name,stats)
        assert stats['sign_extremum_successes'] < stats['total'], (name,stats)
        assert stats['fixed_position_best'] < stats['total'], (name,stats)
    batch = g.generate_batch('easy',5,seed=1475864943)
    for r in batch: printed_check(r)
    for name,z in probes(batch).items():
        ranks={int(rank) for rank in z['numeric_ranks']}
        assert z['distinct_roots']>=2 and ranks & {0,4} and ranks & {1,2,3}, (name,z)
        assert z['sign_extremum_successes']<z['total'] and z['fixed_position_best']<z['total'], (name,z)
    write('samples.json',sample); write('batch.json',batch)
    write('easy-samples.json',[r for r in sample if r['question'][':question/difficulty']==':question.difficulty/easy'])
    write('shortcut-results.json',dict(passed=True, input=before, batch=probes(batch)))
    representatives = batch + [sources[-3],boundaries[0]] + cf
    write('render-records.json', representatives)
    # Actual grader submissions are selected from independent parsed roots,
    # not trusted generator keys. Include every option as an accept/reject case.
    grader = []
    for i,r in enumerate(sources + boundaries + cf + batch):
        t = root(r)
        grader.append(dict(label=f'independent-{i}', record=r, checks=[dict(submitted_answer_id=a[':answer/id'], expected='accepted' if value(a)==t else 'rejected', purpose='printed determinant and rank witness') for a in field(r)[':answer-field/choices']]))
    write('grader-input.json',grader)
    write('math-results.json',dict(passed=True, source_and_changed=len(sources), boundaries=len(boundaries), counterfactuals=len(cf), fresh=len(sample), batch=len(batch), semantic_instances=len({r['generation']['mathematical_fingerprint'] for r in sample}), witness='Printed prompt determinant and augmented ranks at every choice; all printed matrix transitions and corresponding equations; final answer and surviving-equation prose'))
    print(json.dumps(dict(passed=True, source_banks=17, boundaries=len(boundaries), math_records=len(sources+boundaries+cf+sample+batch), grader_records=len(grader), easy_shortcuts=easy),default=str))

if __name__ == '__main__': main()
