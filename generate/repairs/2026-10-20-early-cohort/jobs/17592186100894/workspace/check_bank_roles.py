"""Independent visible-bank and calculus witnesses for the conditional shortcut."""
from audit_support import *
from check_minimal import probe
from collections import defaultdict, Counter

E.mkdir(exist_ok=True)
# Exercise every finite bank profile and every answer-bearing role.
records = []
for bank_id in range(15):
    exemplar = g.generate('easy', 492800, 'q-104065', {'h': 1, 'bank': bank_id})
    # Read each candidate's coefficient and constant from the visible expression.
    for option in field(exemplar)[':answer-field/choices']:
        value = explicit(exemplar, option[':answer/value'])
        poly = S.expand(value-S.log(S.sin(x-1)))
        a = poly.coeff(x, 2)
        c = simplify(poly-a*(x-1)**2)
        records.append(g.generate('easy', 492800, 'q-104065', {'h': 1, 'bank': bank_id, 'a': int(a), 'c': str(c)}))

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
        assert len(pure) in (0, 5)
        if pure: assert len(set(correct(r) for r in pure)) == 5
        probes = [probe(r) for r in group]
        assert not any(p['shortcut_success'] for p in probes)
        # Shortest choice including ties: require counterexamples even within
        # the reviewer's pure-pi-squared ordinate subgroup.
        shortest = min(range(5), key=lambda i: len(bank[i]))
        shortest_success = sum(correct(r) == bank[shortest] for r in pure)
        if pure: assert shortest_success < len(pure)
        result.append({'bank': list(bank), 'records': len(group),
                       'correct_values': dict(keys), 'pure_pi_squared_records': len(pure),
                       'shortest_in_pure_subgroup_successes': shortest_success,
                       'conditional_cue_successes': sum(p['shortcut_success'] for p in probes),
                       'conditional_cue_qualifying': sum(p['qualifies'] for p in probes)})
    assert len(banks) == 15, 'Lost supported whole-bank profiles'
    return result

raw = measurements(records)
math = [math_check(r) for r in records]
assert all(m['passed'] and m['valid_choice_count'] == 1 for m in math)
assert all(sum(c['IC'] == '0' for c in m['choices']) >= 2 for m in math), 'IC substitution alone reveals key'
# Independently parse final worked equation; stale explanations fail this check.
for r in records:
    sol = r['question'][':question/worked-solution']
    final = re.search(r'Therefore \$y=(.*?)\$\.', sol).group(1)
    assert simplify(expr(final)-explicit(r, correct(r))) == 0

prior = [(492797, -4, 2, 'pi^2'), (492800, 1, 4, '0'), (492802, 1, 4, 'pi^2'),
         (492803, 4, 6, '-pi^2'), (492805, 4, 6, '0')]
controls = [g.generate('easy', seed, 'q-104065', {'h': h, 'a': a, 'c': c}) for seed,h,a,c in prior]
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
                         'claim': 'Every visible candidate becomes the unique key in the SAME bank and order; no bank-only cue solves these supported IVPs. Every key has at least one same-IC distractor; pure-pi-squared banks retain five distinct keys.',
                         'limits': 'Finite catalog proof for changed trig family; other unchanged families retain prior validated scope. This does not assert that all imaginable prompt-dependent heuristics are impossible.'})
print(json.dumps({'banks': len(raw), 'roles_per_bank': 5, 'delivered': len(accepted), 'math_passed': len(math), 'prior_controls': len(controls), 'native_checks': sum(len(c['checks']) for c in cases), 'passed': True}))
