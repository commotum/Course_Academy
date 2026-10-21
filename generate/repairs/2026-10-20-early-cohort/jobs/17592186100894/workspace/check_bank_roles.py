"""Independent visible-bank and calculus witnesses for the conditional shortcut."""
from audit_support import *
from check_minimal import probe
from collections import defaultdict, Counter

E.mkdir(exist_ok=True)
constants = ('-pi^2', '-1', '0', '1', 'pi^2')
records = [g.generate('easy', 492800, 'q-104065', {'h': 1, 'a': a, 'c': c})
           for a in (2, 4, 6) for c in constants]

def measurements(rs):
    banks = defaultdict(list)
    for r in rs:
        # Group by complete visible bank IN ORDER, without using profile metadata.
        bank = tuple(a[':answer/value'] for a in field(r)[':answer-field/choices'])
        banks[bank].append(r)
    result = []
    for bank, group in banks.items():
        keys = Counter(correct(r) for r in group)
        assert len(bank) == len(set(bank)) == 5
        assert set(keys) == set(bank), 'Some visible bank role can never be correct'
        assert set(keys.values()) == {1}, 'Role controls must test each candidate exactly once'
        # The same whole bank admits all five correct choices. This defeats any
        # deterministic bank-only cue, including conjunctions of shape features.
        pure = [r for r in group if simplify(prompt_data(r)[1][1]/S.pi**2).is_Rational is True]
        assert len(pure) == 3 and len(set(correct(r) for r in pure)) == 3
        probes = [probe(r) for r in group]
        assert not any(p['shortcut_success'] for p in probes)
        # Shortest choice including ties: require counterexamples even within
        # the reviewer's pure-pi-squared ordinate subgroup.
        shortest = min(range(5), key=lambda i: len(bank[i]))
        shortest_success = sum(correct(r) == bank[shortest] for r in pure)
        assert shortest_success < len(pure)
        result.append({'bank': list(bank), 'records': len(group),
                       'correct_values': dict(keys), 'pure_pi_squared_records': len(pure),
                       'shortest_in_pure_subgroup_successes': shortest_success,
                       'conditional_cue_successes': sum(p['shortcut_success'] for p in probes),
                       'conditional_cue_qualifying': sum(p['qualifies'] for p in probes)})
    assert len(banks) == 3, 'Lost supported whole-bank profiles'
    return result

raw = measurements(records)
math = [math_check(r) for r in records]
assert all(m['passed'] and m['valid_choice_count'] == 1 for m in math)
# Independently parse final worked equation; stale explanations fail this check.
for r in records:
    sol = r['question'][':question/worked-solution']
    final = re.search(r'Therefore \$y=(.*?)\$\.', sol).group(1)
    assert simplify(expr(final)-explicit(r, correct(r))) == 0

prior = json.loads((JOB/'review-1-policy-2-a0e5ad288aa2c633/conditional-shortcut-records.json').read_text())
controls = [g.generate('easy', r['generation']['seed'], 'q-104065', r['generation']['parameters']) for r in prior]
assert len(controls) == 5
assert not any(probe(r)['shortcut_success'] for r in controls)
save('conditional-controls.json', controls)
save('role-records.json', records)
save('role-math.json', math)
inp = E/'role-records.json';out = E/'delivery-roles'
cmd = [sys.executable, str(ROOT/'generate/pipeline/check_delivery.py'), '--input', str(inp),
       '--source', str(JOB/'source/source.json'), '--inventory', str(JOB/'source/inventory.json'),
       '--difficulty', 'easy', '--output', str(out), '--asset-root', str(E),
       '--math-root', '/media/jake/SSD/EDB/math']
p = subprocess.run(cmd, capture_output=True, text=True)
(E/'roles-delivery-console.txt').write_text(p.stdout+p.stderr)
assert p.returncode == 0, p.stdout+p.stderr
accepted = json.loads((out/'accepted.json').read_text())
assert len(accepted) == len(records)
delivered = measurements(accepted)
# Test keys and every distractor using the native grader in one batch.
cases = []
for r in accepted+controls:
    f = field(r)
    cases.append({'label': 'role witness '+str(r['generation']['parameters']), 'record': r,
                  'checks': [{'submitted_answer_id': a[':answer/id'],
                              'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected'}
                             for a in f[':answer-field/choices']]})
save('role-grader-input.json', cases)
cmd_grade = [str(ROOT/'generate/runs/current/check-engine'), str(E/'role-grader-input.json'), str(E/'role-grader-report.json')]
p = subprocess.run(cmd_grade, capture_output=True, text=True)
(E/'role-grader-console.txt').write_text(p.stdout+p.stderr)
assert p.returncode == 0, p.stdout+p.stderr
save('role-results.json', {'raw': raw, 'delivered': delivered, 'math_records': len(math),
                         'prior_qualifying_controls_tested': len(controls),
                         'commands': [cmd, cmd_grade], 'native_checks': sum(len(c['checks']) for c in cases),
                         'claim': 'Every visible candidate becomes the unique key in the SAME bank and order; no bank-only cue solves these supported IVPs. Pure-pi-squared subgroup retains three distinct keys per bank.',
                         'limits': 'Finite catalog proof for changed trig family; other unchanged families retain prior validated scope. This does not assert that all imaginable prompt-dependent heuristics are impossible.'})
print(json.dumps({'banks': len(raw), 'roles_per_bank': 5, 'delivered': len(accepted), 'math_passed': len(math), 'prior_controls': len(controls), 'native_checks': sum(len(c['checks']) for c in cases), 'passed': True}))
