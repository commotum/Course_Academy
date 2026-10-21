"""Strict regressions: expected to fail the reviewed package, no package writes."""
import sys,json
sys.dont_write_bytecode=True
import review as R
failures=[]
try:
 r=R.g.generate('easy',7331,'q-20964',{'rhs_scale':1})
 if R.equations(r['question']).tolist()!=[[1,-5,0],[2,-10,3]]:failures.append({'test':'zero_intercept_source_replay','reason':'Wrong original matrix'})
except ValueError as e:failures.append({'test':'zero_intercept_source_replay','source_id':'897c434c-2b3e-570b-8210-f27b51719e55','parameters':{'difficulty':'easy','seed':7331,'template':'q-20964','rhs_scale':1},'reason':str(e)})
rs=[R.g.generate('easy',7331,'q-42157',{'rhs_scale':t}) for t in [-4,-3,-2,-1,1,2,3,4]]
# A coefficient-only cue must not determine consistency. The exact absent
# counterfactual is x-6y=2, -4x+24y=-8 (consistent), rather than RHS -10.
types={R.equations(r['question'])[:,:2].rank()==R.equations(r['question']).rank() for r in rs}
if types!={False,True}:failures.append({'test':'coefficient_signature_must_not_fix_consistency','template':'q-42157','observed_types':list(types),'minimal_generated_case':{'seed':7331,'rhs_scale':2,'equations':[[1,-6,4],[-4,24,-20]],'action':'Choose No solution solely from coefficient -6; succeeds for every allowed scale.'},'required_decision_pair':{'before':[[1,-6,2],[-4,24,-10]],'after':[[1,-6,2],[-4,24,-8]],'expected':'No solution -> x=2+6y, y free'}})
R.save('targeted-regressions.json',{'command':f'{sys.executable} {R.ROOT}/targeted-regressions.py','expected_exit_on_current_package':1,'failures':failures,'passed':not failures})
print(json.dumps({'failed':len(failures),'tests':[x['test'] for x in failures]}))
sys.exit(bool(failures))
