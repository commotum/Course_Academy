"""Replay the exact latest review counterexample; exit 1 demonstrates it.

Single-seed replay deliberately stays unchanged. The repair is batch selection,
tested separately by batch_regressions.py --finding batch.
"""
import json
import sys
sys.dont_write_bytecode = True
from validate_repair import W, g, printed_check, probes

E = W/'evidence/repair-2'
E.mkdir(parents=True,exist_ok=True)
records = [g.generate('easy',seed=n) for n in [1475864945,1475864946]]
for r in records: printed_check(r)
captured = json.loads((W.parent/'samples.json').read_text())
assert records == captured[2:4]
report = probes(records)
z = report['easy:unit_bare:opposite_sign']
assert z['total'] == z['sign_extremum_successes'] == z['numeric_ranks'][0] == 2
(E/'baseline-records.json').write_text(json.dumps(records,indent=2)+'\n')
(E/'baseline-results.json').write_text(json.dumps(dict(
    strict_passed=False, exact_captured_records=True, seeds=[1475864945,1475864946],
    probes=report,command=f'{sys.executable} -B checks/reproduce_latest.py',
    interpretation='Expected exit 1: exact latest delivered subgroup remains reproducible; repaired batch selection is tested separately.'
),indent=2)+'\n')
print(json.dumps(dict(reproduced_current=2,minimum_correct=2,strict_passed=False)))
raise SystemExit(1)
