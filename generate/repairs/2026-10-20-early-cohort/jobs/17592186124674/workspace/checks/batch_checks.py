"""Build current delivered-batch grading cases and two targeted normal witnesses."""
import importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('repair',W/'checks/repair.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
extra=[c.g.generate_easy(seed=19),c.g.generate_easy(seed=31)]
assert extra[0]['generation']['template']=='source_17592186317478'
assert extra[1]['generation']['template']=='direct_model' and extra[1]['generation']['bank_kind']=='mixed'
records=json.loads((W/'evidence/delivery-batch/accepted.json').read_text())+extra
cases=[]
for r in records:
    w=c.witness(r)
    cases.append({'label':'delivered batch or targeted normal coverage witness','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==w['correct'] else 'rejected','purpose':'independent visible equilibrium/model check'} for a in c.choices(r)]})
c.save('batch-grader-input.json',cases)
c.save('normal-coverage-witness.json',extra)
c.save('normal-coverage.json',{'targeted_default_seeds':[19,31],'purpose':'The original reviewer 40-seed range misses computer context and direct mixed profile; two targeted default calls exercise them. Controlled records exercise every eligible target in both direct profiles and all source prompts.','cases':[c.witness(r) for r in extra],'all_normal_prompt_and_bank_profiles_exercised':True})
print(json.dumps({'batch_and_coverage_records':len(records),'checks':5*len(records)}))
