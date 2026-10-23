"""Independent strict regression: nonzero exit exposes the demonstrated cue.
Run on prospective candidate files as well as the runner batch; never modifies input.
"""
import argparse,json,pathlib,sys
sys.dont_write_bytecode=True
from audit import load,probes,module,check_math,ROOT,JOB
p=argparse.ArgumentParser();p.add_argument('--candidate-records',type=pathlib.Path);p.add_argument('--package',type=pathlib.Path,default=JOB/'workspace');p.add_argument('--output',type=pathlib.Path,default=ROOT/'regression-results.json');a=p.parse_args()
failures=[]
if a.candidate_records:
 records=load(a.candidate_records)
else:
 m=module(a.package/'17592186064206.py')
 records=[m.generate(seed=912,template='q-15707',parameters=v) for v in [[2,1,7],[3,1,7]]]
 # This canonical example is a required capability; no hard-coded template ID is required for its repair.
 outcomes=[]
 for template in m.PROFILES:
  try:
   r=m.generate(seed=912,template=template,parameters=[3,5,2]);ok=check_math(r)['passed'];outcomes.append({'template':template,'passed':ok})
  except Exception as e:outcomes.append({'template':template,'passed':False,'error':f'{type(e).__name__}: {e}'})
 if not any(x['passed'] for x in outcomes):failures.append({'defect':'canonical positive nonunit slope unsupported','parameters':[3,5,2],'attempts':outcomes})
results=probes(records)
for r in results:
 # Two fixed/candidate instances establish the retained recurring counterexample;
 # proof for the entire original construction is separately in pedagogical-variation.json.
 if r['total']>=2 and r['correct']==r['total']:failures.append({'defect':'bank-only cue answers every sampled member of recognizable subgroup','probe':r})
report={'command':sys.argv,'records':records,'probes':results,'failures':failures,'passed':not failures}
a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'failures':len(failures),'report':str(a.output)}));sys.exit(bool(failures))
