"""Executable retained findings; visible equations, independent witnesses, no writes to runtime."""
import collections
import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parents[1]
OUT = W / 'evidence'
OUT.mkdir(exist_ok=True)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


g = load(W / '17592186078583.py', 'current_generator')
v = load(W / '17592186078583/validate.py', 'independent_validator')


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def field(r):
    return r['question'][':question/answer-fields'][0]


def key(f):
    k = f[':answer-field/correct']
    return k[1] if isinstance(k, list) else k[':answer/id']


def correct_value(r):
    f = field(r)
    return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == key(f))


def shortest_correct(r):
    f = field(r)
    choices = f[':answer-field/choices']
    n = min(len(a[':answer/value']) for a in choices)
    shortest = [a for a in choices if len(a[':answer/value']) == n]
    return len(shortest) == 1 and shortest[0][':answer/id'] == key(f)


def independent(r):
    # Existing source-derived checker reads prompt temperatures, actual solution
    # blocks, and each displayed equation, rather than trusting generator keys.
    v.independent(r)
    return r


def grader_case(r, label):
    q = r['question']
    ambient = int(re.findall(r'\$\{(\d+)\}\^', q[':question/problem'])[-1])
    target = -v.C * (v.U - ambient)
    return {'label': label, 'record': r, 'checks': [
        {'submitted_answer_id': a[':answer/id'],
         'expected': 'accepted' if v.sp.expand(v.rhs(a[':answer/value']) - target) == 0 else 'rejected',
         'purpose': 'Native radio grading against equation independently derived from visible ambient'}
        for a in field(r)[':answer-field/choices']]}


def cue_summary(records):
    grouped = collections.defaultdict(list)
    for r in records:
        grouped[r['generation']['template']].append(r)
    result = {}
    for template, rows in grouped.items():
        positions = collections.Counter()
        ranks = collections.defaultdict(list)
        shortest = longest = 0
        for r in rows:
            f = field(r)
            choices = f[':answer-field/choices']
            correct = next(i for i, a in enumerate(choices) if a[':answer/id'] == key(f))
            positions[correct + 1] += 1
            # Strip shared derivative LHS, TeX and whitespace; test visible RHS
            # lengths as well as exact strings from the reported counterexample.
            strings = [a[':answer/value'].split('=', 1)[1] for a in choices]
            lengths = [len(s) for s in strings]
            shortest += shortest_correct(r)
            longest += lengths.count(max(lengths)) == 1 and lengths[correct] == max(lengths)
            for rank, length in enumerate(sorted(set(lengths)), 1):
                tied = [i for i, n in enumerate(lengths) if n == length]
                ranks[rank].append((int(correct in tied), len(tied)))
        assert shortest == 0, f'{template}: shortest-choice counterexample persists'
        assert longest == 0, f'{template}: unique longest choice predicts key'
        assert len(positions) > 1, f'{template}: fixed answer position'
        # Even allowing uniform guessing within a tied length class must not
        # yield certainty. Record these probabilities, rather than count ties
        # as a failed attack and hide the remaining risk.
        rank_rates = {str(rank): sum(hit / size for hit, size in cases) / len(rows)
                      for rank, cases in ranks.items()}
        assert max(rank_rates.values()) < 1, f'{template}: length rank determines key'
        result[template] = {'records': len(rows), 'position_counts': dict(positions),
                            'unique_shortest_correct': shortest, 'unique_longest_correct': longest,
                            'length_rank_guess_success': rank_rates,
                            'ambient_values': sorted({r['generation']['parameters']['S'] for r in rows}),
                            'initial_values': sorted({r['generation']['parameters']['I'] for r in rows
                                                      if 'I' in r['generation']['parameters']}),
                            'choice_count': 5, 'uniform_guess_baseline': 0.2}
    return result


def run():
    source = json.loads((W.parent / 'source/source.json').read_text())
    bank = source['material']['kp'][':knowledge-point/questions']
    raw, replay = [], []
    for q in bank:
        template = q[':question/math-academy-id']
        level = q[':question/difficulty'][':db/ident'].split('/')[-1]
        numbers = list(map(int, re.findall(r'\$\{(\d+)\}\^', q[':question/problem'])))
        p = {'S': numbers[-1], **({'I': numbers[0]} if level == 'moderate' else {})}
        r = independent(g.generate(level, 90271, template=template, profile=template, parameters=p))
        v.fidelity(q, r)
        raw.append(r)
        replay.append({'source_question_id': q[':question/id'], 'template': template,
                       'parameters': p, 'prompt_solution_complete_bank_key_match': True, 'options': 5})
    assert len(replay) == 10
    save('source-replay-records.json', raw)
    save('source-replay.json', {'banks': replay, 'matched_banks': 10, 'matched_options': 50,
                              'canonical_limit': 'Bread example has no captured answer bank.'})

    # Retain EXACT reviewer acceptance tests first; never exempt the reported seed.
    cake = independent(g.generate('easy', 90271, template='q-106877', profile='q-106877', parameters={'S': 70}))
    assert 'Fahrenheit' in cake['question'][':question/problem']
    turkey = independent(g.generate('moderate', 92601, template='q-106883'))
    assert turkey['generation']['parameters'] == {'S': 52, 'I': 179}
    assert not shortest_correct(turkey), 'Exact retained shortest-choice failure persists'

    records = []
    coverage = {}
    for level, templates in g.DEFAULT_TEMPLATES.items():
        for template in templates:
            # Focus on the changed moderate rule; small easy control sample.
            seeds = range(92601, 92609) if level == 'moderate' else range(92601, 92604)
            for seed in seeds:
                records.append(independent(g.generate(level, seed, template=template)))
            unit = g.TEMPLATES[template]['unit']
            lo, hi = (10, 40) if unit == 'C' else (50, 85)
            tested = []
            for S in (lo, hi):
                # Test both supported initial endpoints without a large sweep.
                initials = [None] if level == 'easy' else [max(g.INITIAL_BOUNDS[template][0], S + 10), g.INITIAL_BOUNDS[template][1]]
                for I in initials:
                    p = {'S': S, **({'I': I} if I is not None else {})}
                    records.append(independent(g.generate(level, 92633, template=template, parameters=p)))
                    tested.append(p)
            coverage[template] = tested
    normal_draws = [independent(g.generate_easy(seed)) for seed in range(15)]
    assert any(r['generation']['template'] == 'q-106877' for r in normal_draws), 'Cake absent from normal sampling'
    save('normal-easy-draws.json', normal_draws)
    save('samples.json', records)
    for level in g.LEVELS:
        save('samples-' + level + '.json', [r for r in records if r['question'][':question/difficulty'].endswith('/' + level)])
    save('shortcut-before-delivery.json', cue_summary(records))

    # Controlled role changes at equal seed preserve bank/profile and ordering.
    cf, cf_results = [], []
    for level, templates in g.DEFAULT_TEMPLATES.items():
        for template in templates:
            S = 22 if g.TEMPLATES[template]['unit'] == 'C' else 64
            p = {'S': S}
            if level == 'moderate':
                p['I'] = max(g.INITIAL_BOUNDS[template][0], S + 15)
            a = independent(g.generate(level, 92817, template=template, parameters=p))
            b = independent(g.generate(level, 92817, template=template, parameters={**p, 'S': S + 1}))
            assert correct_value(a) != correct_value(b)
            assert a['question'][':question/worked-solution'] != b['question'][':question/worked-solution']
            assert a['generation']['parameter_fingerprint'] != b['generation']['parameter_fingerprint']
            # Cross-response must reject, not just use two changed lookup UUIDs.
            old_expr = v.rhs(correct_value(a))
            assert v.sp.expand(old_expr - v.rhs(correct_value(b))) != 0
            result = {'template': template, 'ambient_change_updates_response_solution_task': True}
            cf.extend([a, b])
            if level == 'moderate':
                c = independent(g.generate(level, 92817, template=template, parameters={**p, 'I': p['I'] + 1}))
                assert correct_value(a) == correct_value(c)
                assert a['question'][':question/worked-solution'] == c['question'][':question/worked-solution']
                assert a['generation']['parameter_fingerprint'] == c['generation']['parameter_fingerprint']
                cf.append(c)
                result['initial_only_change_preserves_response_solution_task'] = True
            cf_results.append(result)
    save('counterfactual-records.json', cf)
    save('counterfactual-results.json', cf_results)

    # Ensure independent checks detect stale prompt, key, and solution mutations.
    for mutation in ('prompt', 'key', 'solution'):
        bad = copy.deepcopy(cf[0])
        f = field(bad)
        if mutation == 'key':
            f[':answer-field/correct'][1] = next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id'] != key(f))
        elif mutation == 'prompt':
            bad['question'][':question/problem'] = bad['question'][':question/problem'].replace('{22}', '{23}')
        else:
            bad['question'][':question/worked-solution'] = bad['question'][':question/worked-solution'].replace('-k(T-22)', '-k(T-23)')
        try:
            independent(bad)
        except AssertionError:
            pass
        else:
            raise AssertionError('Independent witness missed mutation: ' + mutation)

    rejected = []
    for level, template, p in [('easy', 'q-106877', {'S': 49}), ('easy', 'q-106877', {'S': 86}),
                               ('moderate', 'q-106883', {'S': 52, 'I': 52}), ('moderate', 'q-106934', {'S': 76, 'I': 213})]:
        try:
            g.generate(level, 0, template=template, parameters=p)
        except ValueError:
            rejected.append({'template': template, 'parameters': p})
        else:
            raise AssertionError('Invalid boundary accepted')
    save('math.json', {'passed': True, 'source_replays': len(raw), 'sample_records': len(records),
                       'counterfactual_records': len(cf), 'boundary_coverage': coverage,
                       'invalid_boundary_rejections': rejected,
                       'negative_mutations_detected': ['prompt', 'key', 'solution']})
    save('grader-input.json', [grader_case(r, f'visible-math-{i}') for i, r in enumerate(raw + records + cf)])
    batch = json.loads(subprocess.check_output([
        sys.executable, str(W / '17592186078583.py'), '--difficulty', 'easy',
        '--count', '5', '--seed', '93011', '--format', 'json'], text=True))
    for r in batch:
        independent(r)
    assert len({r['generation']['parameter_fingerprint'] for r in batch}) == 5
    save('batch.json', batch)
    # Two same-seed ambient changes demonstrate the changed evidence visually.
    cake_pair = [r for r in cf if r['generation']['template'] == 'q-106877']
    save('render-records.json', cake_pair + [turkey, next(r for r in records if r['generation']['template'] == 'q-106934')])
    save('regressions.json', {'passed': True, 'findings': ['740ca70087bb0b79e807', 'a6abccb1458850272d61'],
                              'exact_turkey_parameters': turkey['generation']['parameters'],
                              'source_banks': len(raw), 'sample_records': len(records),
                              'normal_easy_draws': len(normal_draws)})
    print(json.dumps({'passed': True, 'source_banks': len(raw), 'sample_records': len(records), 'counterfactuals': len(cf)}))


if __name__ == '__main__':
    run()
