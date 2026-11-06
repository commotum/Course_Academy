from pathlib import Path
import json,sys,subprocess,hashlib,shutil
R=Path('/home/jake/Developer/Course_Academy');H=R/'reference/edb-math/imports/oregon-state/2026-11-06-341-prq12';sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection
for name in ['prepare.py','source-inventory.json','qa.py']:
 shutil.copy2(Path('/tmp/ingest-prq12')/name,H/name)
db=connection();payload=H/'transaction.edn';digest=hashlib.sha256(payload.read_bytes()).hexdigest()
run=subprocess.run([str(R/'.local/edb/f26-missing-2026-10-21/preview'),str(payload)],env=db.env,check=True,capture_output=True,text=True,timeout=120)
(H/'preview.log').write_text(run.stdout+run.stderr);(H/'native-preview-verification.json').write_text(json.dumps({'passed':True,'committed':False,'sha256':digest,'basis':int((H/'preview-basis.txt').read_text()),'output':run.stdout},indent=2)+'\n')
entities=json.loads((H/'entities.json').read_text());records={x[':db/id']:x for x in entities};q=next(x for x in entities if ':question/id'in x and x[':question/answer-fields'] and records[x[':question/answer-fields'][0]][':answer-field/type'].endswith('/radio'));f=records[q[':question/answer-fields'][0]];choices=[{':answer/id':records[aid][':answer/id']['$uuid'],':answer/type':records[aid][':answer/type'],':answer/value':records[aid][':answer/value']}for aid in f[':answer-field/choices']]
field={':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',f[':answer-field/correct']]}
checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct']else'rejected','purpose':'Correct True choice'if a[':answer/id']==f[':answer-field/correct']else'Incorrect False choice'}for a in choices]
fixture=[{'label':'canvas-59459059','record':{'question':{':question/problem':q[':question/problem'],':question/answer-fields':[field]},'knowledge_point':{'title':'Equal null space and image'},'generation':{'template':'imported-assignment'}},'checks':checks}]
(H/'grading-input.json').write_text(json.dumps(fixture));r=subprocess.run([str(R/'generate/runs/current/check-engine'),str(H/'grading-input.json'),str(H/'grading-verification.json')],capture_output=True,text=True,check=True);g=json.loads((H/'grading-verification.json').read_text());assert g['passed'] and g['accepted_checks']==g['rejected_checks']==1;g['source_sha256']=digest;(H/'grading-verification.json').write_text(json.dumps(g,indent=2)+'\n')
print(run.stdout.strip());print(r.stdout.strip());print('Native written field preserved without automatic grading.')
