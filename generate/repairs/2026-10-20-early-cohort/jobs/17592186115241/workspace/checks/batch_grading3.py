"""One native-grader input, including raw, delivered and controlled responses."""
import json,pathlib
E=pathlib.Path(__file__).resolve().parents[1]/'evidence';cases=[]
for name in ['grader-input.json','role-grader-input.json','rational-grader-input.json','unit-grader-input.json','post-grader-input.json','controlled-grader-input.json']:
 cases.extend(json.loads((E/name).read_text()))
for group in ('rational','unit'):
 for i,r in enumerate(json.loads((E/('delivery-'+group)/'accepted.json').read_text())):
  f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][-1]
  cases.append({'label':'delivered-'+group+'-'+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==key else 'rejected','purpose':'shared delivery bank identities'} for c in f[':answer-field/choices']]})
# Repeated raw/delivered banks still validate independently when normalization
# changes a record. Exact duplicates need only one native check.
seen=set();unique=[]
for case in cases:
 signature=json.dumps({'record':case['record'],'checks':case['checks']},sort_keys=True)
 if signature in seen:continue
 seen.add(signature);unique.append(case)
(E/'repair3-grader-input.json').write_text(json.dumps(unique,indent=2)+'\n')
print(json.dumps({'native_records':len(unique),'native_checks':sum(len(c['checks']) for c in unique)}))
