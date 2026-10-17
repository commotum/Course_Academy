"""Compare every eligible matrix-entry task and independently validate arithmetic."""
import copy,hashlib,importlib.util,json,sys,types
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5]
path=ROOT/'generate/scratch/17592186100873.py'
before=types.ModuleType('entry_before');before.__file__=str(path)
exec(compile((HERE/'17592186100873.before.py').read_text(),str(path),'exec'),before.__dict__)
def module(name,file):
 spec=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
new=module('entry_after',path);validation=module('entry_validation',path.with_suffix('')/'validate.py')
records=[];coverage={};changed=0
for mid in before.TEMPLATES:
 assert before.domain(mid)==new.domain(mid)
 old=before.generate('easy',template=mid,replay=True);fresh=new.generate('easy',template=mid,replay=True)
 assert old==fresh;validation.audit(fresh);records.append(fresh)
 coverage[mid]=[]
 for row,column in new.domain(mid):
  args={'level':'easy','seed':23,'template':mid,'parameters':{'row':row,'column':column}}
  old=before.generate(**args);fresh=new.generate(**args);validation.audit(fresh)
  delta=copy.deepcopy(fresh)
  for attr in (':question/problem',':question/worked-solution'):
   assert delta['question'][attr]!=old['question'][attr]
   delta['question'][attr]=old['question'][attr]
  assert delta==old
  assert before.fingerprint(old['question'])==new.fingerprint(fresh['question'])
  assert fresh==new.generate(**args)
  records.append(fresh);coverage[mid].append([row,column]);changed+=1
report=validation.native(records,HERE/'native')
report={**report,'records':len(report['records'])}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
summary={'passed':True,'knowledge_point':17592186100873,'path':str(path.relative_to(ROOT)),'before_sha256':sha(HERE/'17592186100873.before.py'),'after_sha256':sha(path),'validator_sha256':sha(path.with_suffix('')/'validate.py'),'eligible_source_profiles':len(coverage),'eligible_cells_checked':changed,'source_replays_unchanged':len(coverage),'all_non_prompt_solution_data_preserved':True,'full_matrices_selected_vectors_and_arithmetic_verified':True,'native':report,'active_registration_basis':3269,'coverage':coverage}
(HERE/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
(HERE/'render-samples.json').write_text(json.dumps([next(r for r in records if not r['generation']['evidence_only'] and r['generation']['template']==mid) for mid in coverage],indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='coverage'},indent=2))
