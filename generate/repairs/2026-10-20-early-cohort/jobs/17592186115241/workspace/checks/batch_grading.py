"""Batch all independently witnessed raw and delivered choices for the native grader."""
import json,pathlib
E=pathlib.Path(__file__).resolve().parents[1]/'evidence';cases=[]
for name in ['grader-input.json','role-grader-input.json','rational-grader-input.json','post-grader-input.json','controlled-grader-input.json']:
 cases.extend(json.loads((E/name).read_text()))
for i,r in enumerate(json.loads((E/'delivery-rational/accepted.json').read_text())):
 f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][-1]
 cases.append({'label':'delivered-rational-'+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==key else 'rejected','purpose':'filtered rational bank identities'} for c in f[':answer-field/choices']]})
(E/'repair2-grader-input.json').write_text(json.dumps(cases,indent=2)+'\n')
print(json.dumps({'native_records':len(cases),'native_checks':sum(len(c['checks']) for c in cases)}))
