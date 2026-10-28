import copy,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=Path.cwd();D=json.loads((H/'snapshot.json').read_text());idents=dict(json.loads((H/'idents.json').read_text()));keys={r['field']:r['answer']for r in json.loads((H/'missing-key-completions.json').read_text())};P=json.loads((H/'proposals.json').read_text())+json.loads((H/'completion-solutions.json').read_text());pd={(p['entity'],p['attribute']):p['after']for p in P};out=[];skipped=[];owned=[]
for oq in D['questions']:
 q=copy.deepcopy(oq);checks=[]
 for a in ['question/problem','question/worked-solution']:
  if (q[':db/id'],a)in pd:q[':'+a]=pd[q[':db/id'],a]
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  bank={a[':db/id']:a for a in f.get(':answer-field/choices',[])};right=f.get(':answer-field/correct',{}).get(':db/id')or keys.get(f[':db/id']);ft=idents[f[':answer-field/type'][':db/id']];f[':answer-field/type']=ft
  for a in bank.values():a[':answer/type']=idents[a[':answer/type'][':db/id']]
  if not right:skipped.append({'question':q[':db/id'],'field':f[':db/id'],'reason':'no correct link'});continue
  assert right in bank,(q[':db/id'],right,bank);a=bank[right];owned.append(f[':db/id']);f[':answer-field/correct']=[':answer/id',a[':answer/id']]
  if ft in (':answer-field.type/radio',':answer-field.type/select',':answer-field.type/checkbox'):
   checks.extend({'field_index':i,'submitted_answer_id':a2[':answer/id'],'expected':'accepted'if a2[':db/id']==right else'rejected','purpose':'Existing choice identity checked with canonical owned key'}for a2 in bank.values())
  elif ft==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Exact canonical accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect scalar rejected'}])
 if checks:out.append({'label':str(q[':db/id']),'record':{'question':q,'knowledge_point':{'title':'Linear algebra audit'},'generation':{'template':'source-formatting-audit'}},'checks':checks})
(H/'grading-input.json').write_text(json.dumps(out,indent=2));subprocess.run([str(R/'.local/edb/html-table-repair/check-engine'),str(H/'grading-input.json'),str(H/'grading.json')],check=True);(H/'key-ownership-validation.json').write_text(json.dumps({'fields_with_owned_correct_keys':len(owned),'skipped':skipped},indent=2));print('questions',len(out),'fields',len(owned),'skipped',len(skipped))
