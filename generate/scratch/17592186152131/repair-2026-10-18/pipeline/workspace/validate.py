#!/usr/bin/env python3
"""Author checks independent of generator arithmetic; no database access.

Baseline checks; current review-repair coverage is in repair_checks.py.
Usage: python validate.py build
       python validate.py delivered evidence/delivery/accepted.json
"""
import collections
from fractions import Fraction
import itertools
import json
import math
import os
from pathlib import Path
import re
import sys

import generator as g

ROOT = Path(__file__).resolve().parent
E = ROOT / os.environ.get('COURSE_ACADEMY_VALIDATION_EVIDENCE_DIR', 'evidence')


def save(name, data):
    (E / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def parse(tex):
    # Independent reader for complete served answer objects.
    m = re.fullmatch(r'\{?(\d+(?:\.\d+)?)\}?\^\{(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)\}', tex)
    if m:
        b, p, q = m.groups()
        return Fraction(b), Fraction(p) / Fraction(q)
    m = re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}', tex)
    if m:
        return Fraction(int(m[1]), int(m[2])), Fraction(1)
    return Fraction(tex), Fraction(1)


def equal(a, b):
    # For positive bases, raising both to the LCM gives an exact rational test.
    (x, p), (y, q) = a, b
    d = math.lcm(p.denominator, q.denominator)
    return x ** int(p * d) == y ** int(q * d)


def inspect(record):
    q = record['question']
    problem = q[':question/problem']
    m = re.search(r'\\sqrt(?:\[(\d+)\])?\{(\d+(?:\.\d+)?)\}', problem)
    assert m, problem
    n, x = int(m[1] or 2), Fraction(m[2])
    f = q[':question/answer-fields'][0]
    choices = f[':answer-field/choices']
    correct_id = f[':answer-field/correct'][1]
    answers = [parse(c[':answer/value']) for c in choices]
    truth = (x, Fraction(1, n))
    matches = [i for i, a in enumerate(answers) if equal(a, truth)]
    assert len(matches) == 1, (problem, matches)
    index = matches[0]
    assert choices[index][':answer/id'] == correct_id
    assert all(not equal(a, b) for a, b in itertools.combinations(answers, 2))
    assert len(answers) == 5
    solution = q[':question/worked-solution']
    assert f'$x={m[2]},$' in solution and f'$n={n}.$' in solution
    final = solution.split('$$')[-2].strip().split('=')[-1]
    assert equal(parse(final), truth)
    numeric = [float(b) ** float(p) for b, p in answers]
    unit = [i for i, c in enumerate(choices) if re.search(r'\^\{1/', c[':answer/value'])]
    expected_unit = 4 if record['generation']['profile'] in ('square-index-confusion', 'indexed-grid') else 2
    assert len(unit) == expected_unit  # Numerator 1 alone must not solve the record.
    unit_bases = {i: answers[i][0] for i in unit}
    return {'x': str(x), 'n': n, 'key': choices[index][':answer/value'], 'position': index,
            'rank': sorted(range(5), key=lambda i: numeric[i]).index(index) + 1,
            'correct': index, 'min_unit_base': min(unit, key=unit_bases.get),
            'max_unit_base': max(unit, key=unit_bases.get),
            'decimal': '.' in m[2], 'case': 'x<n' if x<n else ('x=n' if x==n else 'x>n')}


def coverage(records):
    groups = collections.defaultdict(list)
    semantic = set()
    for record in records:
        a = inspect(record)
        name = record['generation']['template']
        groups[name].append(a)
        semantic.add((a['x'], a['n']))
    result = {'records': len(records), 'semantic_instances': len(semantic), 'groups': {}}
    for name, rows in groups.items():
        total = len(rows)
        cue = lambda key: {'successes': sum(r[key] == r['correct'] for r in rows), 'attempts': total}
        subgroup = {}
        for label, pred in [('integer', lambda r:not r['decimal']), ('decimal', lambda r:r['decimal'])]:
            subset = [r for r in rows if pred(r)]
            if subset:
                subgroup[label] = {'count': len(subset), 'cases': dict(collections.Counter(r['case'] for r in subset)),
                   'larger_unit_base_successes': sum(r['max_unit_base']==r['correct'] for r in subset)}
        result['groups'][name] = {
            'count': total, 'cases': dict(collections.Counter(r['case'] for r in rows)),
            'positions': dict(collections.Counter(r['position'] for r in rows)),
            'numeric_ranks': dict(collections.Counter(r['rank'] for r in rows)),
            'best_fixed_position': max(collections.Counter(r['position'] for r in rows).values()),
            'best_fixed_numeric_rank': max(collections.Counter(r['rank'] for r in rows).values()),
            'choose_smaller_unit_fraction_base': cue('min_unit_base'),
            'choose_larger_unit_fraction_base': cue('max_unit_base'),
            'numerator_one_candidates_per_record': 4 if name == 'square-equation' else 2, 'blind_radio_baseline': 0.2,
            'subgroups': subgroup}
        assert set(r['case'] for r in rows) == ({'x<n','x=n','x>n'} if name == 'square-equation' else {'x<n','x>n'})
        assert len(set(r['position'] for r in rows)) == 5
        assert len(set(r['rank'] for r in rows)) >= 2
        assert all(sum(r[k]==r['correct'] for r in rows) < total for k in ('min_unit_base','max_unit_base'))
        if name == 'square-equation':
            decimals = [r for r in rows if r['decimal']]
            assert {r['case'] for r in decimals} == {'x<n','x>n'}
    return result


def grader_cases(records, prefix):
    output = []
    for i, record in enumerate(records):
        a = inspect(record)
        field = record['question'][':question/answer-fields'][0]
        output.append({'label': f'{prefix}-{i}', 'record': record, 'checks': [
           {'submitted_answer_id': c[':answer/id'],
            'expected': 'accepted' if j==a['correct'] else 'rejected',
            'purpose': 'independent exact rational-power check of every authored choice'}
           for j,c in enumerate(field[':answer-field/choices'])]})
    return output


def source_checks():
    sources = json.loads((ROOT/'source_cases.json').read_text())
    replay = g.source_replay()
    summary = []
    for original, record in zip(sources['questions'], replay):
        a = inspect(record)
        assert record['question'][':question/problem'] == original[':question/problem']
        source_choices = original[':question/answer-fields'][0][':answer-field/choices']
        generated = record['question'][':question/answer-fields'][0][':answer-field/choices']
        matches = [[i for i,c in enumerate(generated) if equal(parse(c[':answer/value']),parse(s[':answer/value']))]
                   for s in source_choices]
        assert all(len(m)==1 for m in matches) and len({m[0] for m in matches})==5
        correct = original[':question/answer-fields'][0].get(':answer-field/correct')
        if correct:
            assert equal(parse(correct[':answer/value']), parse(a['key']))
        original_solution = original.get(':question/worked-solution')
        if original_solution:
            assert record['question'][':question/worked-solution'] == g.normalize_prose(original_solution)
        summary.append({'source_id':original[':question/id'], 'source_ma_id':original[':question/math-academy-id'],
            'choices_matched':5, 'distractors_matched':4,'prompt_exact':True,
            'solution_exact_normalized':True if original_solution else None,
            'source_difficulty':original.get(':question/difficulty'),
            'inferred_missing_key':not bool(correct)})
    canonical = sources['canonical']
    c = g.generate(4, 5, 'indexed-equation')
    assert equal(parse(inspect(c)['key']),parse('4^{1/5}'))
    assert 'x = 4' in canonical[':question/worked-solution'] and 'n = 5' in canonical[':question/worked-solution']
    save('source-replay-records.json', replay)
    save('source-replay.json', {'banks':summary, 'complete_banks_matched':3,'choices_matched':15,
         'distractors_matched':12,'canonical_id':canonical[':question/id'],
         'canonical_conversion_verified':True,'canonical_field_bank':'none supplied'})
    return replay


def controlled():
    sets = [
        ('swap-roles', g.generate(3,7,'indexed-equation',order_seed=91),g.generate(7,3,'indexed-equation',order_seed=91)),
        ('change-index',g.generate(6,3,'indexed-what',order_seed=92),g.generate(6,7,'indexed-what',order_seed=92)),
        ('change-base',g.generate(5,4,'indexed-what',order_seed=92),g.generate(8,4,'indexed-what',order_seed=92)),
        ('square-relevant-base',g.generate('1.5',2,'square-equation',order_seed=93),g.generate('3.5',2,'square-equation',order_seed=93)),
        ('irrelevant-order',g.generate(6,5,'indexed-equation',order_seed=1),g.generate(6,5,'indexed-equation',order_seed=2))]
    report=[]; records=[]; checks=[]
    for label, before, after in sets:
        a,b = inspect(before),inspect(after)
        preservation = label=='irrelevant-order'
        assert equal(parse(a['key']),parse(b['key'])) == preservation
        if preservation:
            assert before['question'][':question/id']==after['question'][':question/id']
            assert before['question'][':question/worked-solution']==after['question'][':question/worked-solution']
        else:
            assert before['question'][':question/problem']!=after['question'][':question/problem']
            assert before['question'][':question/worked-solution']!=after['question'][':question/worked-solution']
        if label=='swap-roles':
            # The previous key is now the role-swapped distractor, not merely a different UUID.
            f=after['question'][':question/answer-fields'][0]
            old=[c for c in f[':answer-field/choices'] if equal(parse(c[':answer/value']),parse(a['key']))]
            assert len(old)==1 and old[0][':answer/id'] != f[':answer-field/correct'][1]
            checks.append({'label':'swapped-old-key-now-rejected','record':after,
                           'checks':[{'submitted_answer_id':old[0][':answer/id'],'expected':'rejected','purpose':'controlled role swap rejects former key'}]})
        report.append({'case':label,'before':a,'after':b,'response_preserved':preservation})
        records.extend([before,after])
    save('counterfactuals.json',report)
    save('counterfactual-records.json',records)
    return records, checks


def build():
    replay=source_checks() # Run original cases before expanding the finite domain.
    counterfactuals, cross=controlled()
    boundary = [g.generate(2,10,'indexed-equation'),g.generate(15,3,'indexed-what'),
        g.generate(3,2,'square-equation'),g.generate(15,2,'square-equation'),
        g.generate('1.2',2,'square-equation'),g.generate('7.5',2,'square-equation')]
    for r in boundary: inspect(r)
    bad=[(2,4,'indexed-equation'),(5,2,'indexed-what'),(0,3,'indexed-equation')]
    for x,n,t in bad:
        try:g.generate(x,n,t)
        except ValueError:pass
        else:raise AssertionError('Invalid boundary accepted')
    for difficulty in ('moderate','hard'):
        try:g.generate_batch(difficulty)
        except ValueError:pass
        else:raise AssertionError('Unsupported band accepted')
    assert g.generate_batch(seed=234,count=5)==g.generate_batch(seed=234,count=5)
    normal=[]
    for seed in range(30):
        batch=g.generate_batch(seed=seed,count=5)
        semantic=[(str(r['generation']['parameters']['x']),r['generation']['parameters']['n']) for r in batch]
        assert len(set(semantic))==5
        normal.extend(batch)
    save('seeded-records.json',normal)
    save('seeded-variation.json',coverage(normal))
    # Exact finite-domain expansion resolves possible bank collisions and coverage gaps.
    records=[g.generate(x,n,t,order_seed=10000+i,seed=20261017)
             for i,(t,x,n) in enumerate((t,x,n) for t in g.TEMPLATES for x,n in g.domain(t))]
    report=coverage(records)
    report.update({'invalid_boundaries_rejected':len(bad),'unsupported_bands_rejected':2,
        'determinism':True,'generator_rejection':'None: samples already-valid domains. Finite-domain equivalence checks found no collisions.',
        'fidelity':'three source banks; 15/15 choices and 12/12 distractors; two available solutions exact after normalization',
        'correctness':'every permitted template/domain point checked with exact independent rational powers',
        'grading':'see native-grader.json and delivered-native-grader.json',
        'variation':'Baseline only; authoritative repaired-bank probes and full configuration coverage are in repair_checks.py and evidence/repair-2.',
        'justified_conditional_cues':['The prior decimal-only shortcut defense was refuted by review and withdrawn; normal square practice now uses a two-by-two base/index bank.',
          'The key always keeps the radicand as its base and uses 1/index; this is the taught rule, not an incidental cue.',
          'Exactly one correct choice is required by radio; all five positions are eligible.'],
        'selection_limits':['No learner snapshot/history or live policy supplied. Read-only selection inspection shows filtering by band and uniform hash draw within eligible band; history may remove any item. Zero easy weight could suppress this generator entirely. No learner distribution guarantee is claimed.']})
    save('domain-records.json', records)
    save('pedagogical-variation.json',report)
    save('native-grader-input.json',grader_cases(replay+boundary+counterfactuals,'source-boundary-controlled')+cross)
    # Representative UI cases cover all forms, both relative-size cases and decimal extension.
    render=[g.generate(2,7,'indexed-what'),g.generate(9,3,'indexed-what'),
            g.generate(3,7,'indexed-equation'),g.generate(7,3,'indexed-equation'),
            g.generate(3,2,'square-equation'),g.generate(10,2,'square-equation'),
            g.generate('1.5',2,'square-equation'),g.generate('3.5',2,'square-equation')]
    save('render-records.json',render)
    print(json.dumps({'source_banks':3,'matched_choices':15,'domain_records':len(records),
                      'semantic_instances':report['semantic_instances'],'counterfactual_pairs':5,'render_records':len(render)}))


def delivered(path):
    records=json.loads(Path(path).read_text())
    report=coverage(records)
    report['coverage_comparison'] = 'Every declared template, relative-size case, all five positions, and decimal cases on both sides of 2 must survive; asserted above.'
    save('delivered-variation.json',report)
    save('delivered-native-grader-input.json',grader_cases(records,'delivered'))
    print(json.dumps({'accepted_records':len(records),'semantic_instances':report['semantic_instances'],
                      'native_checks':len(records)*5}))

if __name__=='__main__':
    E.mkdir(exist_ok=True)
    if sys.argv[1]=='build':build()
    elif sys.argv[1]=='delivered':delivered(sys.argv[2])
    else:raise SystemExit('Use build or delivered ACCEPTED.json')
