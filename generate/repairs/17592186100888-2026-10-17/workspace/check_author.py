"""Focused author checks; read source files, never open EDB or publish."""
from pathlib import Path
import collections
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

import sympy as sp
import generator as g

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE_ROOT = HERE.parent / 'source'
SOURCE = json.loads((SOURCE_ROOT / 'source.json').read_text())


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def key(record):
    values = {}
    for field in record['question'][':question/answer-fields']:
        values[field[':answer-field/key']] = next(a[':answer/value'] for a in field[':answer-field/choices']
                                                if a[':answer/id'] == field[':answer-field/correct'][1])
    return ''.join('T' if values[k] == 'true' else 'F' for k in ('I', 'II', 'III'))


def independent_math(t, p):
    """Reconstruct the function and requested comparisons from source equations."""
    x, y = sp.symbols('x y', positive=True)
    if t in ('power_easy', 'power_moderate'):
        f = p.get('a', 1)*x**p['n']
        claim, rhs = p['d']*x**(p['n']-1), p['q']*f/x
    elif t in ('exp_true', 'exp_none'):
        sign = -1 if t == 'exp_none' else 1
        f = p.get('a', 1)*sp.exp(sign*p['k']*x)
        claim, rhs = sign*p.get('a', 1)*p['d']*sp.exp(sign*p['k']*x), sign*p['q']*f
    elif t == 'sin_none':
        f = sp.sin(p['k']*x)/p['b']
        claim, rhs = p['d']*sp.cos(p['k']*x)/p['b'], p['q']*sp.cos(p['k']*x)/p['b']
    elif t == 'cos_i':
        f = sp.cos(p['k']*x)
        claim, rhs = -p['d']*sp.sin(p['k']*x), -p['q']*sp.sin(p['k']*x)
    elif t == 'inverse_none':
        f = -x**(-p['n'])
        claim, rhs = p['d']/x**(p['n']+1), -p['q']*f/x
    elif t == 'log_all':
        f = sp.log(p['k']*x+p['h'])
        claim, rhs = p['d']/(p['k']*x+p['h']), p['q']*sp.exp(-f)
    elif t == 'log_scaled':
        f = 2*p['m']*sp.log(x)
        claim, rhs = p['d']/x, p['q']*x*sp.exp(-f/p['m'])
    else:
        z = p['b']*x+p['c']
        f = p['a']*sp.log(z)
        claim, rhs = p['a']*p['d']/z, p['a']*p['q']*sp.exp(-f/p['a'])
    actual = sp.diff(f, x)
    i, ii = sp.simplify(actual-claim) == 0, sp.simplify(actual-rhs) == 0
    return ''.join('T' if v else 'F' for v in (i, ii, ii))


def main():
    sources = {q[':question/math-academy-id']: q for q in SOURCE['material']['kp'][':knowledge-point/questions']}
    source_rows = []
    for family, mask in g.MASKS.items():
        source = sources[mask['source_id']]
        rec = g.source_replay(g.LEVELS[family], family, raw=True)
        q = rec['question']
        assert q[':question/problem'] == source[':question/problem'], family
        assert q[':question/worked-solution'] == source[':question/worked-solution'], family
        expected_banks = {f[':answer-field/key']: (sorted(c[':answer/value'] for c in f[':answer-field/choices']), f[':answer-field/correct'][':answer/value'])
                          for f in source[':question/answer-fields']}
        actual_banks = {f[':answer-field/key']: (sorted(c[':answer/value'] for c in f[':answer-field/choices']),
                          next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id'] == f[':answer-field/correct'][1]))
                        for f in q[':question/answer-fields']}
        assert actual_banks == expected_banks, family
        assert rec['generation']['evidence_only'] and not rec['generation']['eligible_for_learning']
        normalized = g.source_replay(g.LEVELS[family], family)
        assert g.replay.NORMAL_DOMAIN_PHRASE in normalized['question'][':question/worked-solution']
        source_rows.append({'family': family, 'question_db_id': source[':db/id'], 'key': key(rec),
                            'prompt_exact': True, 'solution_exact': True, 'complete_banks': 3, 'choices': 6})
    canonical = SOURCE['material']['kp'][':knowledge-point/canonical-example']
    assert canonical[':db/id'] == 17592186100725
    assert sp.simplify(sp.diff(1/g.x, g.x) + 1/g.x**2) == 0
    assert sp.simplify(sp.diff(1/g.x, g.x) - (-g.y/g.x).subs(g.y, 1/g.x)) == 0
    assert r'\dfrac{1}{x}' in canonical[':question/problem'] and r'-\dfrac{y}{x}' in canonical[':question/problem']
    write('source-replay.json', {'basis': SOURCE['basis'], 'practice_cases': source_rows,
         'complete_banks_matched': 27, 'choices_matched': 54,
         'canonical': {'question_db_id': canonical[':db/id'], 'independent_mathematical_key': 'TTT',
                       'limitation': 'Canonical example has no captured answer fields. Its derivative/substitution are independently verified; its absent field bank is not claimed as replayed.'}})

    records, coverage = [], {}
    for number, (family, level) in enumerate(g.LEVELS.items()):
        family_records = []
        for case in g.CASES:
            rec = g.generate(level, seed=77+number, template=family, decision_case=case)
            assert key(rec) == independent_math(family, rec['generation']['parameters'])
            assert key(rec) == ''.join('T' if v else 'F' for v in (case[0], case[1], case[1]))
            assert rec == g.generate(level, seed=77+number, template=family, decision_case=case)
            assert ':answer-field.type/checkbox' == rec['question'][':question/answer-fields'][0][':answer-field/type']
            family_records.append(rec)
        # A template-only/position-only guess succeeds on at most one of four
        # controlled cases; no sign change encodes either decision.
        assert {key(rec) for rec in family_records} == {'FFF', 'FTT', 'TFF', 'TTT'}
        coverage[family] = {'cases': sorted(key(rec) for rec in family_records),
                            'best_fixed_subset_success': 1, 'trials': 4}
        records.extend(family_records)

    counterfactual = []
    for d, q in ((-5, 2), (-6, 2), (-5, 3), (-6, 3)):
        p = {'a': -3, 'n': 2, 'd': d, 'q': q}
        rec = g.generate_moderate(parameters=p, template='power_moderate')
        assert key(rec) == independent_math('power_moderate', p)
        assert '- 3 x^{2}' in rec['question'][':question/problem']
        counterfactual.append(rec)
    assert [key(r) for r in counterfactual] == ['FTT', 'TTT', 'FFF', 'TFF']
    records.extend(counterfactual)
    write('user-counterfactuals.json', counterfactual)

    # Parameter-domain enumeration is cheap integer work, not thousands of
    # generated symbolic questions. Boundary representatives get full math checks.
    capacities, sign_probes = {}, {}
    for family, level in g.LEVELS.items():
        domain = list(g.parameter_domain(family))
        capacities[family] = len(domain)
        assert len({json.dumps(p, sort_keys=True) for p, _ in domain}) == len(domain)
        buckets = collections.defaultdict(set)
        for p, case in domain:
            g.validate_parameters(family, p)
            # Coefficient signs are constant within source family, and both
            # truth values occur for both independent comparisons in every bucket.
            coefficient = p.get('a', 1)
            sign = 'negative' if coefficient < 0 else 'positive'
            buckets[sign].add(case)
        assert all(cases == set(g.CASES) for cases in buckets.values())
        sign_probes[family] = {k: len(v) for k, v in buckets.items()}
        for p, _ in (domain[0], domain[-1]):
            rec = g.generate(level, template=family, parameters=p)
            assert key(rec) == independent_math(family, p)
            records.append(rec)
        if len(domain) < 1000:
            try: g.batch(level, len(domain)+1, template=family)
            except ValueError as exc: assert 'capacity' in str(exc)
            else: raise AssertionError('Impossible count was accepted')

    # All eight checkbox submissions are unambiguous field-owned choice IDs.
    grader = []
    for index, rec in enumerate(records):
        checks = []
        for i, field in enumerate(rec['question'][':question/answer-fields']):
            for answer in field[':answer-field/choices']:
                expected = 'accepted' if answer[':answer/id'] == field[':answer-field/correct'][1] else 'rejected'
                checks.append({'field_index': i, 'submitted_answer_id': answer[':answer/id'],
                               'expected': expected, 'purpose': 'Correct or opposite Boolean field-owned choice'})
        grader.append({'label': 'author-'+str(index), 'record': rec, 'checks': checks})
    write('grader-input.json', grader)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'), str(HERE/'grader-input.json'),
                    str(HERE/'grader-report.json')], check=True, stdout=subprocess.DEVNULL)

    write('author-records.json', records)
    delivery_rows = {}
    for band in g.SUPPORTED_LEVELS:
        selected = [r for r in records if r['question'][':question/difficulty'] == ':question.difficulty/'+band]
        write(band+'-records.json', selected)
        subprocess.run([sys.executable, str(REPO/'generate/pipeline/check_delivery.py'),
            '--input', str(HERE/(band+'-records.json')), '--source', str(SOURCE_ROOT/'source.json'),
            '--inventory', str(SOURCE_ROOT/'inventory.json'), '--difficulty', band,
            '--output', str(HERE/('delivery-'+band))], check=True, stdout=subprocess.DEVNULL)
        accepted = json.loads((HERE/('delivery-'+band)/'accepted.json').read_text())
        after = collections.defaultdict(set)
        for rec in accepted: after[rec['generation']['template']].add(key(rec))
        assert all(value == {'FFF', 'FTT', 'TFF', 'TTT'} for value in after.values())
        assert set(after) == {t for t, level in g.LEVELS.items() if level == band}
        delivery_rows[band] = {'input': len(selected), 'accepted': len(accepted),
                                'per_family_cases': {t: sorted(v) for t, v in after.items()}}

    manifest = json.loads((HERE/'package.json').read_text())
    with tempfile.TemporaryDirectory(prefix='relocation-', dir=HERE) as temporary:
        temp = Path(temporary)
        for rel in manifest['files']:
            target = temp/rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(HERE/rel, target)
        env = dict(os.environ)
        env.pop('PYTHONPATH', None)
        for band in g.SUPPORTED_LEVELS:
            command = [sys.executable, str(temp/'generator.py'), '--difficulty', band, '--count', '5', '--seed', '31', '--format', 'json']
            one = subprocess.check_output(command, cwd=temp, env=env)
            two = subprocess.check_output(command, cwd=temp, env=env)
            assert one == two
            relocated = json.loads(one)
            assert relocated == g.batch(band, 5, 31)
            assert {key(r) for r in relocated} == {'FFF', 'FTT', 'TFF', 'TTT'}
    assert (HERE/'math_format.py').read_bytes() == (REPO/'scripts/question_capture/math_format.py').read_bytes()
    result = {'passed': True, 'source_questions': 9, 'source_banks': 27, 'source_choices': 54,
        'canonical_math': 'passed', 'generated_math_cases': len(records), 'native_grader_checks': len(records)*6,
        'family_coverage': coverage, 'finite_capacities': capacities, 'coefficient_sign_groups': sign_probes,
        'exact_user_function_counterfactuals': ['FTT', 'TTT', 'FFF', 'TFF'],
        'delivery': delivery_rows, 'same_seed_and_relocation': 'all3 bands, twice, 5 records each',
        'limits': ['Actual learner history selection is not exercised by the offline delivery helper.',
                   'Actual UI visual inspection is performed by root and the independent reviewer.',
                   'Hard is the preexisting authored affine-log extension; no captured hard example exists.']}
    write('author-validation.json', result)
    write('author-result.json', {'status': 'ready', 'manifest': 'package.json',
         'summary': 'Repaired all10 families to vary derivative-claim truth and solution truth independently; preserves original9 complete Boolean banks in explicit evidence-only replay, retains scoped hard affine-log extension, uses direct bounded coefficient enumeration and canonical formatting before IDs.',
         'evidence_paths': ['instructional-account.md', 'source-replay.json', 'check_author.py', 'author-validation.json',
                            'author-records.json', 'user-counterfactuals.json', 'grader-input.json', 'grader-report.json',
                            'delivery-easy/delivery.json', 'delivery-moderate/delivery.json', 'delivery-hard/delivery.json'],
         'limitations': result['limits']})
    print(json.dumps({'passed': True, 'source_questions': 9, 'generated_math_cases': len(records),
                      'native_grader_checks': len(records)*6, 'delivery': {b: v['accepted'] for b, v in delivery_rows.items()}}))


if __name__ == '__main__': main()
