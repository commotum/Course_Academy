#!/usr/bin/env python3
"""Regression a2f26476abafae793e46: test current visible banks, not metadata."""
import collections
import json
import pathlib
import re
import sys
sys.dont_write_bytecode = True
ROOT = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import generator as g
from retained_predictor import predict


def field(r):
    return r['question'][':question/answer-fields'][0]


def visible(r):
    """Infer the ODE and candidates solely from learner-visible strings."""
    prompt = r['question'][':question/problem']
    m = re.search(r'=\\frac\{(-?\d*)(x\^3|x)\+(y\^3|2y|y)\}\{(xy\^2|x)\}', prompt)
    assert m, prompt
    a = int(m[1]) if m[1] not in ('', '-') else (-1 if m[1] else 1)
    family = 'cube_root' if m[2] == 'x^3' else 'affine' if m[3] == '2y' else 'linear_log'
    choices = field(r)[':answer-field/choices']
    coefficients = []
    for choice in choices:
        tex = choice[':answer/value']
        if family == 'cube_root':
            match = re.fullmatch(r'y=x\\sqrt\[3\]\{(-?\d+)\\ln\|x\|\+C\}', tex)
            assert match, tex
            # Differentiating y^3/x^3=b ln|x|+C gives y'=y/x+(b/3)x²/y².
            assert int(match[1]) % 3 == 0
            implied_a = int(match[1]) // 3
        elif family == 'affine':
            match = re.fullmatch(r'y=Cx\^2([+-])(\d*)x', tex)
            assert match, tex
            b = int(match[2] or 1) * (1 if match[1] == '+' else -1)
            # y=Cx²+bx gives y'-2y/x=-b.
            implied_a = -b
        else:
            match = re.fullmatch(r'y=(-?\d*)x\\ln\|x\|\+Cx', tex)
            assert match, tex
            implied_a = int(match[1]) if match[1] not in ('', '-') else (-1 if match[1] else 1)
            # y=bx ln|x|+Cx gives y'-y/x=b on either nonzero x interval.
        coefficients.append(implied_a)
    assert len(coefficients) == len(set(coefficients)) == 5
    assert coefficients.count(a) == 1
    expected = choices[coefficients.index(a)]
    assert field(r)[':answer-field/correct'][1] == expected[':answer/id']
    solution = r['question'][':question/worked-solution'].replace('&', '')
    assert expected[':answer/value'] in solution
    return family, a, coefficients


def probes(records):
    by_family = collections.defaultdict(list)
    for r in records:
        family, a, cs = visible(r)
        f = field(r); bank = f[':answer-field/choices']; key = f[':answer-field/correct'][1]
        for name, aid in [('retained review predictor', predict(f)[1]),
                          ('first', bank[0][':answer/id']), ('last', bank[-1][':answer/id']),
                          ('smallest magnitude', bank[min(range(5), key=lambda i:abs(cs[i]))][':answer/id']),
                          ('largest magnitude', bank[max(range(5), key=lambda i:abs(cs[i]))][':answer/id']),
                          ('smallest signed coefficient', bank[cs.index(min(cs))][':answer/id']),
                          ('largest signed coefficient', bank[cs.index(max(cs))][':answer/id']),
                          ('shortest string', min(bank, key=lambda z:len(z[':answer/value']))[':answer/id']),
                          ('longest string', max(bank, key=lambda z:len(z[':answer/value']))[':answer/id']),
                          ('smallest UUID', min(bank, key=lambda z:z[':answer/id'])[':answer/id']),
                          ('largest UUID', max(bank, key=lambda z:z[':answer/id'])[':answer/id'])]:
            by_family[family, name].append((aid is not None, aid == key))
    return [{'family':t,'strategy':p,'attempts':sum(v[0] for v in vs),'correct':sum(v[1] for v in vs),'total':len(vs),'baseline':0.2} for (t,p),vs in by_family.items()]


def main():
    out = pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
    # Retain the exact latest counterexample and its signed counterfactual.
    exact = [g.generate('cube_root', a, seed=826033) for a in (2,-2)]
    assert all(predict(field(r))[1] is None for r in exact)
    census = [g.generate(t,a,826031) for t in ('cube_root','affine','linear_log') for a in (*range(-9,0),*range(1,10))]
    assert all(predict(field(r))[1] is None for r in census)
    # Identical visible bank, all five legitimate correct assignments, same presentation seed.
    controlled = []
    groups = []
    for t in ('cube_root','affine','linear_log'):
        rs = [g.generate(t,a,826033,bank_index=7) for a in (-2,-1,1,2,3)]
        banks = [[c[':answer/value'] for c in field(r)[':answer-field/choices']] for r in rs]
        assert all(b == banks[0] for b in banks)
        keyed_positions = []
        for r in rs:
            _, a, cs = visible(r)
            keyed_positions.append(cs.index(a))
            visible_after = json.loads(json.dumps(r))
            field(visible_after)[':answer-field/choices'].reverse()
            assert visible(visible_after)[:2] == visible(r)[:2]
            assert field(visible_after)[':answer-field/correct'] == field(r)[':answer-field/correct']
        assert set(keyed_positions) == set(range(5))
        # Every rank/shape/string/position-only probe must actually fail on four of five.
        rows = probes(rs)
        for z in rows:
            if z['strategy'] not in ('retained review predictor','smallest UUID','largest UUID'):
                assert z['correct'] == 1, z
            else:
                assert z['correct'] < z['total'], z
        groups.append({'family':t,'prompt_coefficients':[-2,-1,1,2,3],'same_visible_bank':True,'correct_positions':keyed_positions,'probes':rows})
        controlled.extend(rs)
    normal = g.generate_batch('easy',18,826031)
    all_records = census + controlled + exact + normal
    for r in all_records: visible(r)
    rows = probes(census)
    assert not any(z['correct'] == z['total'] for z in rows)
    for name, data in [('census-records',census),('controlled-records',controlled),('normal-records',normal),('exact-counterexamples',exact)]:
        (out/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
    report = {'finding':'a2f26476abafae793e46','passed':True,'exact_latest_case':"generate('cube_root',2,seed=826033)",'old_predictor_census':{'accepted_predictions':0,'total':54},'math_witness':'Visible prompt coefficient and candidate directional derivatives; no generation metadata used to infer correct answers.','census_probes':rows,'controlled_groups':groups,'normal_counts':dict(collections.Counter(visible(r)[0] for r in normal)),'source_replay':'Original complete banks tested separately; not part of normal easy generation.'}
    (out/'shortcut-regression.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'passed':True,'census':54,'controlled':15,'exact':2,'normal':18,'retained_shortcut_predictions':0}))

if __name__ == '__main__': main()
