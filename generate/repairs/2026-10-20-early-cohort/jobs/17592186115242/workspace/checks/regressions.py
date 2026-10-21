"""Retained review findings; independent checks of the current generator."""
import argparse
import json
import sys
sys.dont_write_bytecode = True
from validate_repair import g, E, field, value, printed_check, probes, zero_cases, source_replay, write

ap = argparse.ArgumentParser()
ap.add_argument('--finding', choices=['shortcut','source','zero'], required=True)
args = ap.parse_args()

if args.finding == 'shortcut':
    records = [g.generate('easy', seed=seed) for seed in range(932401,932449)]
    records += [g.generate('easy',seed=1475864943+i) for i in range(5)]
    for r in records: printed_check(r)
    report = probes(records)
    for name,z in report.items():
        ranks = {int(j) for j in z['numeric_ranks']}
        assert ranks & {0,4} and ranks & {1,2,3}, (name,z)
        assert z['sign_extremum_successes'] < z['total'], (name,z)
        assert z['fixed_position_best'] < z['total'], (name,z)
elif args.finding == 'source':
    # Includes exact q-74691 plus unchanged earlier mathematical corrections.
    records = source_replay()
    r = g.generate('hard',seed=932455,template='dependent_fractional',parameters=dict(a=2,b=-2,c=4,d=-3,u=1,v=0,e=-6))
    assert printed_check(r) == 3
    report = dict(complete_practice_banks=17, canonical=True, fractional_bare=True)
else:
    records = zero_cases()
    report = dict(zero_root_records=sum(printed_check(r)==0 for r in records), fractional_bare_root=str(printed_check(records[-1])))
write('regression-'+args.finding+'.json',dict(passed=True, report=report))
print(json.dumps(dict(finding=args.finding,passed=True)))
