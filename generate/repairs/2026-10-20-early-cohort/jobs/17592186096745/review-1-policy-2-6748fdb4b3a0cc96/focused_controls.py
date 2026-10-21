import json,sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'workspace'))
import generator as g
from review_math import check,correct_index
root=Path(__file__).resolve().parent
records=[g.generate(template=p,seed=7310951+j*104729) for p in ('q-74625','q-131634') for j in range(10)]
(root/'focused-controls.json').write_text(json.dumps(records,indent=2))
res=[check(r) for r in records]
(root/'focused-controls-math.json').write_text(json.dumps(res,indent=2,default=str))
cases=json.load(open(root/'grader-input.json'))
for r in records:
 q=r['question'];f=q[':question/answer-fields'][0];idx=correct_index(q)
 cases.append({'label':'added-profile-control:'+q[':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==idx else 'rejected','purpose':'independently computed RREF on restored source profile'} for j,a in enumerate(f[':answer-field/choices'])]})
(root/'grader-all-input.json').write_text(json.dumps(cases,indent=2))
(root/'render-extra-input.json').write_text(json.dumps([r for r in json.load(open(root/'counterfactual-records.json'))[:6] if r['review_case']!='base'],indent=2))
print(json.dumps({'controls':len(records),'math_failures':[r for r in res if r['errors']],'native_grader_records':len(cases)}))
