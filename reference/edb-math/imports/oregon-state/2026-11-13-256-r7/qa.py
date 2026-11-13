from pathlib import Path
import json,sys,subprocess,hashlib,shutil
R=Path('/home/jake/Developer/Course_Academy');H=R/'reference/edb-math/imports/oregon-state/2026-11-13-256-r7';sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection
def save(n,v):(H/n).write_text(json.dumps(v,indent=2)+'\n')
for name in ['prepare.py','qa.py','author.py']:shutil.copy2(Path('/tmp/rec7-review')/name,H/name)
db=connection();p=H/'transaction.edn';digest=hashlib.sha256(p.read_bytes()).hexdigest()
run=subprocess.run([str(R/'.local/edb/f26-missing-2026-10-21/preview'),str(p)],env=db.env,capture_output=True,text=True,timeout=120)
(H/'preview.log').write_text(run.stdout+run.stderr);assert run.returncode==0,(run.stdout,run.stderr);save('native-preview-verification.json',{'passed':True,'committed':False,'sha256':digest,'basis':int((H/'preview-basis.txt').read_text()),'output':run.stdout})
entities=json.loads((H/'entities.json').read_text());r={e[':db/id']:e for e in entities};cases=[];render=[]
for e in entities:
 for attr in [':tutorial/content',':question/problem',':question/worked-solution',':answer/value']:
  if attr in e:render.append({'entity':e[':db/id'],'attribute':attr,'value':e[attr],'bare_math':attr==':answer/value'and e[':answer/type']==':answer.type/math'})
 if ':question/id'not in e:continue
 f=r[e[':question/answer-fields'][0]];a=r[f[':answer-field/correct']];kind=f[':answer-field/type'];val=a[':answer/value']
 if kind.endswith('/free'):continue
 choice={':answer/id':a[':answer/id']['$uuid'],':answer/type':a[':answer/type'],':answer/value':val}
 field={':answer-field/key':f[':answer-field/key'],':answer-field/type':kind,':answer-field/choices':[choice],':answer-field/correct':[':answer/id',a[':answer/id']['$uuid']]}
 checks=[{'field_index':0,'submitted':val,'expected':'accepted','purpose':'verified canonical math answer'},{'field_index':0,'submitted':'0','expected':'rejected','purpose':'incorrect zero root, polynomial, or incomplete solution family'}]
 cases.append({'label':e[':db/id'],'record':{'question':{':question/problem':e[':question/problem'],':question/answer-fields':[field]},'knowledge_point':{'title':'MTH 256 Recitation 7'},'generation':{'template':'imported-assignment'}},'checks':checks})
save('grading-input.json',cases);save('render-input.json',render)
grun=subprocess.run([str(R/'generate/runs/current/check-engine'),str(H/'grading-input.json'),str(H/'grading-verification.json')],capture_output=True,text=True,timeout=120);(H/'grading.log').write_text(grun.stdout+grun.stderr)
g=json.loads((H/'grading-verification.json').read_text());g['source_sha256']=digest;save('grading-verification.json',g);print(run.stdout.strip());print(grun.stdout.strip());assert grun.returncode==0 and g['passed'] and g['accepted_checks']==8 and g['rejected_checks']==8,g
