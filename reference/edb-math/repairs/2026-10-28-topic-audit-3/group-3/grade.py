import copy,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());idents=dict(json.loads((H/'idents.json').read_text()));dups=json.loads((H/'duplicate-field-keys.json').read_text());drop={}
for g in dups:
 q=next(q for q in D['questions']if q[':db/id']==g['question']);fs=[f for f in q[':question/answer-fields']if f[':db/id']in g['fields']];complete=[f for f in fs if f.get(':answer-field/correct')];keep=max(complete,key=lambda f:f[':db/id']);drop[g['question']]={f[':db/id']for f in fs if f[':db/id']!=keep[':db/id']}
keys={r['field']:r['answer']for r in json.loads((H/'missing-key-completions.json').read_text())};out=[];skip=[]
for original in D['questions']:
 q=copy.deepcopy(original);q[':question/answer-fields']=[f for f in q.get(':question/answer-fields',[])if f[':db/id']not in drop.get(q[':db/id'],set())]
 if not q[':question/answer-fields']:continue
 checks=[];missing=False
 for i,f in enumerate(q[':question/answer-fields']):
  cid=keys.get(f[':db/id'],f.get(':answer-field/correct',{}).get(':db/id'));a=next((a for a in f[':answer-field/choices']if a[':db/id']==cid),None)
  if not a:missing=True;break
  f[':answer-field/correct']=[':answer/id',a[':answer/id']];f[':answer-field/type']=idents[f[':answer-field/type'][':db/id']]
  for choice in f[':answer-field/choices']:choice[':answer/type']=idents[choice[':answer/type'][':db/id']]
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Canonical valid expression accepted without learner writes'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Wrong scalar rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected','purpose':'Every authored bank choice dispatch'}for a in f[':answer-field/choices'])
 if missing:skip.append(q[':db/id']);continue
 out.append({'label':str(q[':db/id']),'record':{'question':q,'knowledge_point':{'title':'Group3 vectorcalculus audit'},'generation':{'template':'current-or-proposed'}},'checks':checks})
(H/'grading-input.json').write_text(json.dumps(out,indent=2));(H/'grading-coverage.json').write_text(json.dumps({'records':len(out),'checks':sum(len(r['checks'])for r in out),'skipped_missing':skip,'local_duplicate_membership_simulation':{k:sorted(v)for k,v in drop.items()}},indent=2));p=subprocess.run([str(H.parent/'check-engine'),str(H/'grading-input.json'),str(H/'grading.json')],capture_output=True,text=True);print(p.stdout);print(p.stderr);print('nativeexit',p.returncode,'questions',len(out),'checks',sum(len(r['checks'])for r in out))
