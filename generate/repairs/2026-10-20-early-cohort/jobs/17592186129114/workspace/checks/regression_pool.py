"""Finding d72e0c903f2371587a3b: current pools, delivery, exact C counterexample."""
from copy import deepcopy
from common import *

old = load(E / 'original-delivered-batch.json')
assert [examine(r)['subset'] for r in old] == ['ABC', 'BC', 'BC', 'AC', 'AC']
original_probe = subprocess.run([sys.executable, str(ROOT / 'checks/batch_role_probe.py'),
                                str(E / 'original-delivered-batch.json'),
                                str(E / 'original-role-probe.json')], capture_output=True, text=True)
assert original_probe.returncode == 1, 'The historical strict failing witness must remain reproducible'
report = {'finding': 'd72e0c903f2371587a3b', 'historical_probe_exit': 1, 'batches': []}
all_records = []
for seed in (924724049, 0, 802139, 920113):
    stats = {}
    records = g.batch('easy', 5, seed, stats=stats)
    assert records == g.batch('easy', 5, seed)
    before = coverage(records)
    accepted = delivery(records, f'batch-{seed}')
    assert len(accepted) == 5, 'Investigate inventory removals rather than passing a reduced batch'
    after = coverage(accepted)
    run([sys.executable, ROOT / 'checks/batch_role_probe.py',
         E / f'batch-{seed}/accepted.json', E / f'batch-{seed}-roles.json'])
    report['batches'].append({'seed': seed, 'stats': stats, 'before': before, 'after': after})
    all_records += accepted

# Exact reported instance is still source-supported; rebuild it with CURRENT code.
old_cf = load(E / 'original-c-counterfactual-records.json')
base = old_cf[0]
p = deepcopy(base['generation']['parameters'])
p.pop('cases', None)
before = g.generate('easy', 924724049, profile='q-129214', parameters=p)
assert p['matrices'][2] == [[-2,-2,-2,-1],[0,3,-5,5],[0,0,0,7]]
p['matrices'][2][1][0] = 1
after = g.generate('easy', 924724049, profile='q-129214', parameters=p)
p['matrices'][2][1][0] = 0
p['matrices'][2][0][3] = 8  # Irrelevant trailing value; does not change a leading entry.
irrelevant = g.generate('easy', 924724049, profile='q-129214', parameters=p)
cf = [before, after, irrelevant]
assert [examine(r)['subset'] for r in cf] == ['ABC', 'AB', 'ABC']
assert 'c_{21}=1' in after['question'][':question/worked-solution']
assert 'in the same column as' in after['question'][':question/worked-solution']
save(E / 'counterfactual-records.json', cf)
report['counterfactual'] = {'change': 'C[2,1] 0 -> 1', 'subsets': ['ABC', 'AB', 'ABC'],
                            'irrelevant_change': 'C[1,4] -1 -> 8 preserves response'}
grader(all_records + cf, 'repair')
save(E / 'repair-regression-results.json', report)
print(json.dumps({'passed': True, 'historical_failure_reproduced': True,
                  'current_delivered_batches': len(report['batches']), 'native_checks': 6*(len(all_records)+len(cf))}))
