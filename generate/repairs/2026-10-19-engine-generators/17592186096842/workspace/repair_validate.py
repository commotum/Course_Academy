"""Affected checks for feedback author 2; no publication or database access.

Run with the job Python from the workspace. Earlier evidence is retained.
The grading blocker is an expected TEST FAILURE, not a passing unresolved test.
"""
import collections
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import sympy as sp
import generator as g
from validate import independent, grading, key, field, coverage
from validation_math import displayed, equal

E = Path('evidence/repair-2')
E.mkdir(parents=True, exist_ok=True)
REPO = Path('/home/jake/Developer/Course_Academy')
ENGINE = REPO / 'generate/runs/current/check-engine'
COMMANDS = []


def save(name, data):
    (E / name).write_text(json.dumps(data, indent=2, default=str) + '\n')


def run(args, name, expected=0):
    COMMANDS.append([str(a) for a in args])
    result = subprocess.run(args, capture_output=True, text=True)
    save(name, {'command': [str(a) for a in args], 'exit_code': result.returncode,
                'stdout': result.stdout, 'stderr': result.stderr})
    assert result.returncode == expected, (name, result.stderr[:500])
    return result


def nearest_cubic(records):
    report = collections.defaultdict(lambda: {'attempts': 0, 'success_mass': 0})
    for r in records:
        if r['generation']['template'] != 'slope_sum_radio':
            continue
        p = r['generation']['parameters']
        cubic = 3*p['k']*p['t']**2
        choices = field(r)[':answer-field/choices']
        errors = [abs(displayed(a[':answer/value'])-cubic) for a in choices]
        best = min(errors)
        winners = [i for i, v in enumerate(errors) if v == best]
        correct = choices.index(key(r))
        for group in ['all', 'a_sign=' + str(sp.sign(p['a'])),
                      'k_sign=' + str(sp.sign(p['k']))]:
            report[group]['attempts'] += 1
            report[group]['success_mass'] += 1/len(winners) if correct in winners else 0
    return dict(report)


def selection(records):
    # Same within-band SHA256 draw as question_selection.rs, synthetic IDs.
    pool = sorted(records, key=lambda r: r['question'][':question/id'])
    result = []
    for i in range(len(pool)):
        digest = hashlib.sha256(('course-academy/question-selection/v1/repair-' + str(i)).encode()).digest()
        uniform = (int.from_bytes(digest[8:16], 'big') >> 11)/2**53
        result.append(pool[math.floor(uniform*len(pool))])
    return result


def main():
    replay = g.replay_sources()
    cases = json.loads(Path('data/source-cases.json').read_text())
    source_report = []
    grader = []
    for case, rec in zip(cases, replay):
        expected = independent(rec)
        original = rec['generation']['source_capture']
        assert g.normalize_prose(original[':question/problem']) == rec['question'][':question/problem']
        matches = 0
        if field(rec)[':answer-field/type'].endswith('/radio'):
            original_choices = original[':question/answer-fields'][0][':answer-field/choices']
            assert len(original_choices) == len(field(rec)[':answer-field/choices'])
            for a in original_choices:
                assert sum(equal(displayed(a[':answer/value']), displayed(b[':answer/value']))
                           for b in field(rec)[':answer-field/choices']) == 1
                matches += 1
        source_report.append({'source_id': case['source_id'], 'prompt': 'matched',
                              'independent_math_and_displayed_steps': 'passed',
                              'complete_radio_choices_matched': matches})
        grader.append(grading(rec, expected, 'source ' + case['source_id']))
    q107303 = next(r for r in replay if r['generation']['replay_source_id'] == 'q-107303')
    solution = q107303['question'][':question/worked-solution']
    assert r'\sqrt{u}={u}^{1/2}' in solution
    assert r'\frac{1}{2}{u}^{-1/2}=\frac{1}{2\sqrt{u}}' in solution
    save('source-replay.json', source_report)
    save('source-records.json', replay)

    records = []
    for name, spec in g.TEMPLATES.items():
        for seed in [1000, 1001]:
            r = g.generate(spec['level'], seed=seed, template=name)
            grader.append(grading(r, independent(r), 'small regression ' + name))
            records.append(r)

    # Original reported shortcut cohort, unchanged values/seeds and new banks.
    reviewed = []
    for i in range(20):
        a = [-8,-6,6,8][i % 4]
        t = [-4,-3,3,4][(i//4) % 4]
        root = [3,5][i % 2]
        k = [-2,-1,1,2][(i//5) % 4]
        reviewed.append(g.generate('easy', seed=958113+i, template='slope_sum_radio',
                                  parameters=dict(a=a,b=root*root-a*t,t=t,k=k), bank_role=i % 5))
    for r in reviewed:
        independent(r)
    save('reviewed-sum-records.json', reviewed)

    # Fixed other data: every eligible correct coefficient role; both signs.
    sum_controls = []
    for a in [-8, 8]:
        for k in [-2, 2]:
            for role in range(5):
                p = dict(a=a, b=9-a*(-4), t=-4, k=k)
                r = g.generate('easy', seed=17, template='slope_sum_radio',
                               parameters=p, bank_role=role)
                independent(r)
                sum_controls.append(r)
    # The old zero-total-slope rejection is now a valid five-option bank.
    zero = g.generate('easy', seed=1168, template='slope_sum_radio',
                      parameters=dict(a=-6, b=7, t=1, k=1))
    assert independent(zero) == 0
    sum_controls.append(zero)
    # Relevant changes keep cubic and point fixed; key and explanation must change.
    changed = [g.generate('easy', seed=21, template='slope_sum_radio',
                         parameters=dict(a=a, b=9+4*a, t=-4, k=-2), bank_role=2) for a in [-8, -7]]
    values = [independent(r) for r in changed]
    assert values[0] != values[1]
    for i, r in enumerate(changed):
        grader.append({'label': 'changed radical contribution rejects stale response',
                       'record': r, 'checks': [{'submitted_answer_id': a[':answer/id'],
                                                'expected': 'rejected',
                                                'purpose': 'other derivative is now a distractor'}
                                               for a in field(r)[':answer-field/choices']
                                               if equal(displayed(a[':answer/value']), values[1-i])]})
    # At least one stale response actually belongs to the changed bank.
    assert any(c['checks'] for c in grader if c['label'].startswith('changed radical'))
    sum_controls.extend(changed)
    for i, r in enumerate(sum_controls + reviewed):
        grader.append(grading(r, independent(r), 'repaired sum bank ' + str(i)))

    # Canonical plus same-method coefficient/constant counterfactuals and both shapes.
    quadratics = [g.generate('hard', template='sqrt_quadratic_blank', parameters=p)
                  for p in [dict(a=-1, b=0, c=1), dict(a=-1, b=0, c=4),
                            dict(a=2, b=0, c=-3), dict(a=2, b=-3, c=0)]]
    for i, r in enumerate(quadratics):
        grader.append(grading(r, independent(r), 'quadratic shape ' + str(i)))
    assert equal(displayed(key(quadratics[0])[':answer/value']), -g.X/sp.sqrt(1-g.X**2))
    assert not equal(independent(quadratics[0]), independent(quadratics[1]))
    sampled_quad = [g.generate('hard', seed=s, template='sqrt_quadratic_blank') for s in range(8)]
    for r in sampled_quad:
        independent(r)
    assert {r['generation']['parameters']['b'] == 0 for r in sampled_quad} == {False, True}
    records += quadratics + sampled_quad + sum_controls + reviewed
    save('records.json', records)
    save('sum-controls.json', sum_controls)

    # Original runner seed: positive power equivalent MUST be accepted, and isn't.
    runner = [g.generate('moderate', seed=4221317821+i) for i in range(5)]
    save('runner-records.json', runner)
    bad = next(r for r in runner if r['generation']['parameters'] == {'a': 2, 'b': -6}
               and field(r)[':answer-field/type'].endswith('/blank'))
    blocker = [{'label': 'required valid reciprocal fractional-power equivalent',
                'record': bad, 'checks': [{'submitted': r'-\frac{1}{(2x-6)^{3/2}}',
                                          'expected': 'accepted',
                                          'purpose': 'source-grounded equivalent; review reproduction'}]}]
    save('grading-blocker-input.json', blocker)
    run([ENGINE, E/'grading-blocker-input.json', E/'grading-blocker-report.json'],
        'grading-blocker-command.json', expected=1)

    # Separate canonical zero rejection: mathematically wrong, currently unresolved.
    save('zero-blocker-input.json', [{'label': 'canonical nonzero function rejects zero',
                                     'record': quadratics[0], 'checks': [
                                         {'submitted': '0', 'expected': 'rejected',
                                          'purpose': 'derivative is not the zero function'}]}])
    run([ENGINE, E/'zero-blocker-input.json', E/'zero-blocker-report.json'],
        'zero-blocker-command.json', expected=1)

    save('grader-input.json', grader)
    run([ENGINE, E/'grader-input.json', E/'grader-report.json'], 'grader-command.json')

    delivery = {}
    accepted = []
    for band in ['easy', 'moderate', 'hard']:
        rs = [r for r in records if r['question'][':question/difficulty'].endswith('/'+band)]
        save('input-'+band+'.json', rs)
        run([sys.executable, REPO/'generate/pipeline/check_delivery.py',
             '--input', E/('input-'+band+'.json'), '--source', '../source/source.json',
             '--inventory', '../source/inventory.json', '--difficulty', band,
             '--output', E/('delivery-'+band), '--asset-root', E/'assets',
             '--math-root', '/media/jake/SSD/EDB/math'], 'delivery-'+band+'-command.json')
        delivered = json.loads((E/('delivery-'+band)/'accepted.json').read_text())
        accepted.extend(delivered)
        delivery[band] = {'input': len(rs), 'accepted': len(delivered)}
    save('accepted-records.json', accepted)
    selected = selection([r for r in accepted if r['generation']['template']=='slope_sum_radio'])
    save('synthetic-selection.json', selected)
    before = nearest_cubic(sum_controls[:20])
    after_controls = [r for r in accepted if r['generation']['template']=='slope_sum_radio'
                      and r['generation']['parameters']['a'] in [-8,8]
                      and r['generation']['parameters']['t']==-4
                      and r['generation']['parameters']['b']==9+4*r['generation']['parameters']['a']
                      and r['generation']['seed']==17]
    assert len(after_controls) == 20
    for stage in [before, nearest_cubic(after_controls), nearest_cubic(selected)]:
        assert all(v['success_mass'] < v['attempts'] for v in stage.values())
    # Full five roles survive each fixed-data sign subgroup (no mathematical variety claim).
    roles = collections.defaultdict(set)
    for r in after_controls:
        p = r['generation']['parameters']
        roles[str((p['a'],p['k']))].add(r['generation']['bank_assignment'])
    assert all(v == set(range(5)) for v in roles.values())
    save('shortcut-results.json', {
        'fixed_other_data_before_delivery': before,
        'fixed_other_data_after_delivery': nearest_cubic(after_controls),
        'reviewed_twenty_seed_cohort': nearest_cubic(reviewed),
        'synthetic_selection': nearest_cubic(selected),
        'all_five_roles_after_delivery': {k: sorted(v) for k,v in roles.items()},
        'before': coverage(records), 'after': coverage(accepted),
        'limits': 'Selection uses synthetic entity ordering and configured within-band draw; live history, policy and database identities unavailable.'})

    # Actual delivery of the requested moderate runner-style batch.
    run([sys.executable, REPO/'generate/pipeline/check_delivery.py', '--input', E/'runner-records.json',
         '--source', '../source/source.json', '--inventory', '../source/inventory.json',
         '--difficulty', 'moderate', '--output', E/'delivery-runner',
         '--asset-root', E/'assets', '--math-root', '/media/jake/SSD/EDB/math'],
        'delivery-runner-command.json')
    survivors = json.loads((E/'delivery-runner/accepted.json').read_text())
    assert any(r['generation']['parameters']=={'a':2,'b':-6} for r in survivors)

    cli = [sys.executable, 'generator.py', '--difficulty', 'moderate', '--count', '5',
           '--seed', '4221317821', '--format', 'json']
    first = subprocess.check_output(cli)
    assert first == subprocess.check_output(cli)
    manifest = json.loads(Path('package.json').read_text())
    with tempfile.TemporaryDirectory(dir=E) as tmp:
        dest = Path(tmp).resolve()
        for filename in manifest['files']:
            (dest/filename).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(filename, dest/filename)
        relocated = subprocess.check_output([sys.executable, str(dest/'generator.py'),
                         *cli[2:]], cwd=dest)
        assert json.loads(relocated)==json.loads(first)
    save('render-records.json', [q107303, quadratics[0], quadratics[1], sum_controls[0], zero, bad])
    save('runtime-hashes.json', {f: hashlib.sha256(Path(f).read_bytes()).hexdigest()
                               for f in ['package.json']+manifest['files']})
    summary = {'source_replay': {'cases':17, 'radio_choices':40, 'status':'passed',
                               'q107303_power_stages':'restored'},
               'mathematics': {'records':len(records), 'status':'passed',
                               'canonical_quadratic':'supported', 'normal_quadratic_shapes':2},
               'sum_shortcut':'repaired; five fixed-data roles survive actual easy delivery',
               'grading':'BLOCKED: native power/radical equivalence and wrong-zero checks fail',
               'delivery':delivery, 'runner_delivered':len(survivors),
               'determinism':'passed', 'relocation':'passed',
               'semantic_instances':len({r['generation']['parameter_fingerprint'] for r in records}),
               'status':'unsupported'}
    save('summary.json', summary)
    save('commands.json', COMMANDS)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
