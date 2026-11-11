from pathlib import Path
import json,hashlib,sys,subprocess,shutil
R=Path('/home/jake/Developer/Course_Academy');H=R/'reference/edb-math/imports/oregon-state/2026-11-11-341-whw6';T=Path('/tmp/ingest-whw6');sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection

db=connection();p=H/'transaction.edn';digest=hashlib.sha256(p.read_bytes()).hexdigest()
run=subprocess.run([str(R/'.local/edb/f26-missing-2026-10-21/preview'),str(p)],env=db.env,capture_output=True,text=True,check=True,timeout=120);(H/'preview.log').write_text(run.stdout+run.stderr);(H/'native-preview-verification.json').write_text(json.dumps({'passed':True,'committed':False,'sha256':digest,'basis':int((H/'preview-basis.txt').read_text()),'output':run.stdout},indent=2)+'\n')
entities=json.loads((H/'entities.json').read_text());byid={r[':db/id']:r for r in entities};cases=[]
for q in entities:
 if ':question/id'not in q:continue
 fields=[];checks=[]
 for i,fid in enumerate(q[':question/answer-fields']):
  f=byid[fid];choices=[{':answer/id':byid[aid][':answer/id']['$uuid'],':answer/type':byid[aid][':answer/type'],':answer/value':byid[aid][':answer/value']}for aid in f[':answer-field/choices']]
  correct=f[':answer-field/correct'];fields.append({':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]})
  if f[':answer-field/type'].endswith('/free'):continue
  if f[':answer-field/type'].endswith('/checkbox'):
   for a in choices:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected','purpose':'Correct membership'if a[':answer/id']==correct else'Incorrect membership'})
  else:
   answer=byid[correct][':answer/value']
   wrong=r'\sqrt{x^4+3}'if answer.startswith('-\\sqrt')else r'e^x'if answer==r'e^{-x}'else'0'
   checks.extend([{'field_index':i,'submitted':answer,'expected':'accepted','purpose':'Canonical symbolic answer'},{'field_index':i,'submitted':wrong,'expected':'rejected','purpose':'Incorrect sign, factor, or omitted solution terms'}])
 if checks:cases.append({'label':q[':db/id'],'record':{'question':{':question/problem':q[':question/problem'],':question/answer-fields':fields},'knowledge_point':{'title':'MTH 256 E1 and E2'},'generation':{'template':'imported-assignment'}},'checks':checks})
(H/'grading-input.json').write_text(json.dumps(cases));run2=subprocess.run([str(R/'generate/runs/current/check-engine'),str(H/'grading-input.json'),str(H/'grading-verification.json')],check=True,capture_output=True,text=True,timeout=120);g=json.loads((H/'grading-verification.json').read_text());assert g['passed']and g['accepted_checks']==g['rejected_checks']==8;g['source_sha256']=digest;(H/'grading-verification.json').write_text(json.dumps(g,indent=2)+'\n')
print(run.stdout.strip());print(run2.stdout.strip());print('Nine native free-response fields remain ungraded with authored references.')
