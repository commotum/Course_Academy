from pathlib import Path
import json,sys,subprocess,hashlib,shutil
R=Path('/home/jake/Developer/Course_Academy');H=R/'reference/edb-math/imports/oregon-state/2026-11-09-341-prq13';T=Path('/tmp/ingest-prq13');sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection
for name in ['prepare.py','source-inventory.json','qa.py']:shutil.copy2(T/name,H/name)
shutil.copy2('/tmp/author-prq13.py',H/'author.py')
db=connection();p=H/'transaction.edn';digest=hashlib.sha256(p.read_bytes()).hexdigest()
run=subprocess.run([str(R/'.local/edb/f26-missing-2026-10-21/preview'),str(p)],env=db.env,check=True,capture_output=True,text=True,timeout=120)
(H/'preview.log').write_text(run.stdout+run.stderr);(H/'native-preview-verification.json').write_text(json.dumps({'passed':True,'committed':False,'sha256':digest,'basis':int((H/'preview-basis.txt').read_text()),'output':run.stdout},indent=2)+'\n')
entities=json.loads((H/'entities.json').read_text());r={e[':db/id']:e for e in entities};cases=[]
for q in entities:
 if ':question/id'not in q:continue
 assert len(q[':question/answer-fields'])==1
 f=r[q[':question/answer-fields'][0]];assert f[':answer-field/type']==':answer-field.type/radio'
 choices=[{':answer/id':r[aid][':answer/id']['$uuid'],':answer/type':r[aid][':answer/type'],':answer/value':r[aid][':answer/value']}for aid in f[':answer-field/choices']]
 field={':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',f[':answer-field/correct']]}
 checks=[{'field_index':0,'submitted_answer_id':x[':answer/id'],'expected':'accepted'if x[':answer/id']==f[':answer-field/correct']else'rejected','purpose':'Verified intended source choice'if x[':answer/id']==f[':answer-field/correct']else'Incorrect supplied alternative'}for x in choices]
 cases.append({'label':q[':db/id'],'record':{'question':{':question/problem':q[':question/problem'],':question/answer-fields':[field]},'knowledge_point':{'title':'Eigenpair definitions and characteristic equation'},'generation':{'template':'imported-assignment'}},'checks':checks})
(H/'grading-input.json').write_text(json.dumps(cases));g_run=subprocess.run([str(R/'generate/runs/current/check-engine'),str(H/'grading-input.json'),str(H/'grading-verification.json')],capture_output=True,text=True,check=True,timeout=120);g=json.loads((H/'grading-verification.json').read_text());assert g['passed'] and g['accepted_checks']==3 and g['rejected_checks']==7;g['source_sha256']=digest;(H/'grading-verification.json').write_text(json.dumps(g,indent=2)+'\n');print(run.stdout.strip());print(g_run.stdout.strip())
