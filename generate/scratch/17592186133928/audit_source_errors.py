"""Assert actual captured error bytes; preserve raw alongside minimal repairs."""
import json
from pathlib import Path
ROOT=Path(__file__).parent
source=json.loads((ROOT/'source.json').read_text())['record'][':knowledge-point/questions']
repairs={
'q-161928':[(r'-\frac{\text{d}}{\text{d}t}(2{t}^{2}-2t)',r'+\frac{\text{d}}{\text{d}t}(2{t}^{2}-2t)','formal derivative sign'),(r'\frac{5{t}^{3}}{4}',r'\frac{5{t}^{4}}{4}','primitive power')],
'q-162316':[(r'=z\,i+x\,k',r'=z\,i+y\,k','field symbolic substitution matches prompt'),(r'-\frac{\text{d}}{\text{d}t}({t}^{3}-t)',r'+\frac{\text{d}}{\text{d}t}({t}^{3}-t)','formal derivative sign')],
'q-162889':[(r'& =\,i+',r'& =1\,i+','missing visible field coefficient'),(r'=(\,i+',r'=(1\,i+','missing visible dot-vector coefficient')],
'q-162314':[(r'-\frac{\text{d}}{\text{d}t}(-t-{t}^{2})',r'+\frac{\text{d}}{\text{d}t}(-t-{t}^{2})','formal derivative sign')],
}
records=[]
for q in source:
 sid=q[':question/math-academy-id'];solution=q.get(':question/worked-solution');fixed=solution
 operations=[]
 for old,new,reason in repairs.get(sid,[]):
  assert fixed.count(old)==1,(sid,reason,fixed.count(old))
  fixed=fixed.replace(old,new)
  operations.append({'original':old,'replacement':new,'reason':reason,'instances':1})
 records.append({'source_id':sid,'raw_solution':solution,'minimally_repaired_solution':fixed,'repairs':operations,'raw_solution_present':solution is not None,'raw_eligible_for_learning':False,'repair_is_fidelity_match':False,'opaque_bank_remains_ineligible':True})
(ROOT/'source-repairs.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
print('Source byte audit: 7 minimal edits in 4 source solutions; 6 correct raw solutions; 1 missing solution.')
