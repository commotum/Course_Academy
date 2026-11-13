import json,sys,subprocess,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection
a=json.loads((H/'source-audit.json').read_text());es=json.loads((H/'entities.json').read_text());by={e[':db/id']:e for e in es};sha=hashlib.sha256((H/'transaction.edn').read_bytes()).hexdigest();assert sha==a['sha256']
def save(n,v):(H/n).write_text(json.dumps(v,indent=2)+'\n')
db=connection();r=subprocess.run([str(R/'.local/edb/f26-missing-2026-10-21/preview'),str(H/'transaction.edn')],env=db.env,capture_output=True,text=True,timeout=120);(H/'preview.log').write_text(r.stdout+r.stderr);assert r.returncode==0,(r.stdout,r.stderr);save('native-preview-verification.json',{'passed':True,'sha256':sha,'basis':int((H/'preview-basis.txt').read_text()),'committed':False});print(r.stdout.strip(),flush=True)
cases=[]
for e in es:
 if ':question/id'not in e:continue
 fields=[];checks=[]
 for i,fid in enumerate(e[':question/answer-fields']):
  f=by[fid];choices=[{':answer/id':by[x][':answer/id']['$uuid'],':answer/type':by[x][':answer/type'],':answer/value':by[x][':answer/value']}for x in f[':answer-field/choices']];c=by[f[':answer-field/correct']]
  fields.append({':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',c[':answer/id']['$uuid']]})
  if f[':answer-field/type'].endswith('/free'):continue
  if f[':answer-field/type'].endswith('/radio'):
   wrong=next(x for x in choices if x[':answer/id']!=c[':answer/id']['$uuid'])
   checks.extend([{'field_index':i,'submitted_answer_id':c[':answer/id']['$uuid'],'expected':'accepted','purpose':'verified reference choice'},{'field_index':i,'submitted_answer_id':wrong[':answer/id'],'expected':'rejected','purpose':'a distinct incorrect choice'}])
  else:checks.extend([{'field_index':i,'submitted':c[':answer/value'],'expected':'accepted','purpose':'independently verified exact result'},{'field_index':i,'submitted':'999','expected':'rejected','purpose':'a different incorrect numeric result'}])
 if checks:cases.append({'label':e[':db/id'],'record':{'question':{':question/problem':e[':question/problem'],':question/answer-fields':fields},'knowledge_point':{'title':'MTH 341 actual past exam'},'generation':{'template':'imported-past-exam'}},'checks':checks})
save('grading-input.json',cases);r=subprocess.run([str(R/'generate/runs/current/check-engine'),str(H/'grading-input.json'),str(H/'grading-verification.json')],capture_output=True,text=True,timeout=120);(H/'grading.log').write_text(r.stdout+r.stderr);assert r.returncode==0,(r.stdout,r.stderr);g=json.loads((H/'grading-verification.json').read_text());assert g['passed']and g['accepted_checks']==20 and g['rejected_checks']==20;g['source_sha256']=sha;save('grading-verification.json',g);print('20 correct and 20 incorrect field checks passed.')
