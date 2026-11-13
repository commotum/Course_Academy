from pathlib import Path
import json,sys,subprocess,hashlib
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection
def save(n,v):(H/n).write_text(json.dumps(v,indent=2)+'\n')
db=connection();p=H/'transaction.edn';digest=hashlib.sha256(p.read_bytes()).hexdigest()
run=subprocess.run([str(R/'.local/edb/f26-missing-2026-10-21/preview'),str(p)],env=db.env,capture_output=True,text=True,timeout=120)
(H/'preview.log').write_text(run.stdout+run.stderr);assert run.returncode==0,(run.stdout,run.stderr)
save('native-preview-verification.json',{'passed':True,'committed':False,'sha256':digest,'basis':int((H/'preview-basis.txt').read_text()),'output':run.stdout})
entities=json.loads((H/'entities.json').read_text());render=[]
qs=[e for e in entities if ':question/id'in e];fieldless=[e for e in qs if ':question/answer-fields'not in e]
assert len(fieldless)==1 and ':question/worked-solution'not in fieldless[0]
assert len(qs)==4 and len([e for e in entities if ':answer-field/type'in e])==3
assert all(e[':answer-field/type']==':answer-field.type/free'for e in entities if ':answer-field/type'in e)
for e in entities:
 for attr in [':tutorial/content',':question/problem',':question/worked-solution',':answer/value']:
  if attr in e:render.append({'entity':e[':db/id'],'attribute':attr,'value':e[attr],'bare_math':False})
save('render-input.json',render);save('grading-verification.json',{'passed':True,'source_sha256':digest,'graded_fields':0,'native_free_fields':3,'fieldless_questions':1,'scope':'Written responses and review reminder are ungraded; no learner submissions made.'})
print(run.stdout.strip());print('Graph: 4 questions, 1 fieldless reminder, 3 native free fields')
