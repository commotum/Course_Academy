#!/usr/bin/env python3
"""Scoped replenishment using existing EDB integration and application lock."""
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(HERE),str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
import validate as v
from database import Database,StaleBasis
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
g=v.g
KP=g.KP_ID
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'f2e815cfe1ebd33fe0c92dd0d69ec67e511d21a22228d0bd4cdb4ad9dda1897e'
OUT=HERE/'reference/replenishment'
LOCK=ROOT/'.local/learning/requests/math/api.lock'
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
QUERY=(HERE/'reference/source-query.edn').read_text()
# Reuse the application's existing deployed native reader, without application edits.
NATIVE=max((p for p in (ROOT/'.local/graph-explorer').glob('learning-*') if p.is_file() and p.suffix==''),key=lambda p:p.stat().st_mtime_ns)
USAGE_QUERY='''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,ENV['EDB_ENDPOINT']],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE
 save(path,x['data']);return x['data']

def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]

def normalize(q):
 result={key:str(q[key]) if key==':question/id' else q[key] for key in (':question/id',':question/problem',':question/worked-solution')}
 result[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
 result[':question/answer-fields']=[]
 for f in q[':question/answer-fields']:
  result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
 return v.ordered(result)

def source_check(q):
 assert str(q.get(':question/difficulty',{}).get(':db/ident'))==':question.difficulty/easy','Unrated or unsupported source'
 f=v.function(q[':question/problem']);correct=v.sp.cancel(v.sp.diff(f,v.X))
 n=normalize(q);assert len(n[':question/answer-fields'])==1
 field=n[':question/answer-fields'][0]
 values=[v.parse(a[':answer/value']) for a in field[':answer-field/choices']]
 assert sum(v.equal(z,correct) for z in values)==1
 assert all(not v.equal(z,y) for i,z in enumerate(values) for y in values[:i])
 assert next(a[':answer/id'] for a,z in zip(field[':answer-field/choices'],values) if v.equal(z,correct))==field[':answer-field/correct'][1]
 assert n[':question/worked-solution']
 return n

def counts(path,kp,basis):
 unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
 unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
 rows=[];excluded=[];native=[]
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):
   excluded.append({'id':str(q[':question/id']),'reason':'Previously presented or reserved'});continue
  try:
   n=source_check(q)
   rec={'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':n,'generation':{'template':q.get(':question/math-academy-id','persisted-generated')}}
   native.append({'label':n[':question/id'],'record':rec,'checks':v.checks(rec)})
   rows.append({'id':n[':question/id'],'fingerprint':v.fingerprint(n)})
  except (AssertionError,KeyError,ValueError,StopIteration) as error:
   excluded.append({'id':str(q[':question/id']),'source_id':q.get(':question/math-academy-id'),'reason':str(error) or type(error).__name__})
 save(path/'available-native-input.json',native)
 if native:
  subprocess.run([str(HERE/'check-engine'),str(path/'available-native-input.json'),str(path/'available-native-report.json')],check=True)
  assert json.loads((path/'available-native-report.json').read_text())['documented_unresolved_checks']==0
 result={'basis':basis,'easy':len({r['fingerprint'] for r in rows}),'validated_available':rows,'excluded':excluded,'historically_shown_or_reserved':sorted(unavailable),'minimum':5,'unsupported':{'moderate':{'filled':False,'shortage':5},'hard':{'filled':False,'shortage':5}}}
 save(path/'available-counts.json',result);return result

def transaction(records,kp):
 forms=[]
 for rec in records:
  q=rec['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:
  assert str(gen[':question-generator/id'])==g.GENERATOR_ID and gen[':question-generator/script']==SCRIPT,'Existing registered identity must be reconciled, never replaced'
 else:
  forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(g.GENERATOR_ID),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def check_report(report,path,source):
 names=dict(DB.attributes(path,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,value,tx,s,added in report[':edb/tx-data']:
  assert s==source and added,'Unexpected retraction or contributor'
  name=str(names[a])
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected entity or attribute'

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,path/'receipt-check',intent['source_eid'])
 before=loads((path/'before.edn').read_text());after=read_kp(path/'readback',report[':edb/db-after-t'])
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in after[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items()),'Original source mutation'
 assert {k:z for k,z in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:z for k,z in after.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
 byid={str(q[':question/id']):q for q in now.values()}
 for rec in records:
  q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
  assert normalize(q)==v.ordered(rec['question']);v.validate(rec)
 gen=after[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==g.GENERATOR_ID and gen[':question-generator/script']==SCRIPT
 assert not transaction([],after),'Repeat preparation would change registration'
 available=counts(path/'readback',after,report[':edb/db-after-t'])
 verification={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'all_original_questions_unchanged':len(old),'canonical_example_unchanged':True,'only_scoped_additive_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts':available}
 save(path/'verification.json',verification);return verification

def finish(path,verification,inv):
 counts_after=verification['available_counts'];caps=json.loads((HERE/'capabilities.json').read_text())
 result={'outcome':'finite-limit' if counts_after['easy']<5 else 'unsupported','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':g.GENERATOR_ID,'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'unsupported_levels_filled':False,'capability_exceptions':caps['exceptions'],'shortage_remaining':{'easy':max(0,5-counts_after['easy']),'moderate':5,'hard':5},'available_counts_after':counts_after,'verified_commit_basis':verification['basis_after'],'new_questions':verification['new_questions'],'lineage':LINEAGE,'inventory_recheck_basis':inv['basis'],'remaining_native_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',path/'available-counts.json',path/'readback/available-native-report.json',HERE/'validation.json',HERE/'source-replay.json',HERE/'capabilities.json',HERE/'engine-build.json') if p.exists()],'note':'Easy inventory validated and sufficient; registration committed if absent. Moderate and hard remain unfilled bounded capability exceptions. Original questions, canonical example and learner history preserved. No new content made solely to satisfy an unclassified trigger.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
 print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}))

def prepare_and_commit(preview):
 inv=inventory(OUT/'inventory-current.json');basis=inv['basis'];assert DB.basis()==basis
 path=OUT/('basis-'+str(basis));path.mkdir(parents=True,exist_ok=True)
 kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
 (path/'before.edn').write_text(dumps(kp)+'\n')
 # Exact original snapshot is immutable. Sort many-valued Pull rows, including
 # answer banks, before comparing representation-independent evidence.
 def canon(x):
  if isinstance(x,dict):return {str(k):canon(z) for k,z in x.items()}
  if isinstance(x,list):return sorted((canon(z) for z in x),key=lambda z:json.dumps(z,sort_keys=True))
  if isinstance(x,uuid.UUID):return str(x)
  return x
 source=loads((HERE/'reference/source.edn').read_text())[0][0]
 original={q[':db/id']:q for q in source[':knowledge-point/questions']}
 current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(canon(current[e])==canon(q) for e,q in original.items()),'New source evidence requires reclassification'
 assert canon(source[':knowledge-point/canonical-example'])==canon(kp[':knowledge-point/canonical-example'])
 available=counts(path,kp,basis);needed=max(0,5-available['easy'])
 supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
 instances=supplied.get('instances',[])
 if isinstance(instances,dict):instances=instances.get('instances',[instances])
 for rec in instances:v.validate(rec)
 save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
 used={g.generate('easy',0,mid,parameters=t['parameters'])['generation']['math_fingerprint'] for mid,t in g.TEMPLATES.items()}
 for q in current.values():
  try:used.add(v.fingerprint(q))
  except (ValueError,KeyError):pass
 records=[]
 # Execute the validated generator after current inventory, even if only
 # registration is needed; retain local previews without needless imports.
 previews=g.batch('easy',max(2,needed),int(JOB.name[:8],16))
 for rec in instances+previews:
  v.validate(rec);fp=rec['generation']['math_fingerprint']
  if len(records)<needed and fp not in used:records.append(rec);used.add(fp)
 for i in range(1000):
  if len(records)>=needed:break
  rec=g.generate('easy',int(JOB.name[:8],16)+i);v.validate(rec)
  fp=rec['generation']['math_fingerprint']
  if fp not in used:records.append(rec);used.add(fp)
 for kind in ('question','answer-field','answer'):
  ids=[item[':'+kind+'/id'] for rec in records for item in ([rec['question']] if kind=='question' else rec['question'][':question/answer-fields'] if kind=='answer-field' else [a for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]
  assert len(ids)==len(set(ids))
  if ids:assert not DB.query('[:find ?e :in $ [?id ...] :where [?e :'+kind+'/id ?id]]',[list(map(uuid.UUID,ids))],path,'identity-'+kind,basis)
 save(path/'previews.json',previews);save(path/'generated.json',records)
 native=[{'label':str(i),'record':r,'checks':v.checks(r)} for i,r in enumerate(instances+previews+records)]
 save(path/'native-input.json',native)
 subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
 save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':available,'missing_easy':needed,'new_questions':len(records),'local_previews':len(previews),'source_evidence_unchanged':True,'assets':[],'unsupported_shortages':{'moderate':5,'hard':5}})
 forms=transaction(records,kp)
 if not forms:
  verification={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts':available}
  save(path/'verification.json',verification);finish(path,verification,inv);return
 source_rows=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source_rows)==1
 txpath=path/'transaction.edn';text=dumps(forms)+'\n'
 with txpath.open('w') as f:f.write(text);f.flush();os.fsync(f.fileno())
 r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
 (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
 assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis
 check_report(pr,path/'preview-check',source_rows[0][0]);assert DB.basis()==basis
 intent={'database':'math','endpoint':ENV['EDB_ENDPOINT'],'lineage':LINEAGE,'source':SOURCE,'source_eid':source_rows[0][0],'basis':basis,'expected_basis':basis,'request_key':'polynomial-quotient-17592186096620-'+str(basis)+'-'+sha(txpath),'sha256':sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':text,'generator_id':g.GENERATOR_ID,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
 save(path/'commit-intent.json',intent)
 report=DB._commit(intent,txpath,path);verification=verify(path,intent,report)
 finish(path,verification,inventory(path/'inventory-after.json'))

def main():
 validation=json.loads((HERE/'validation.json').read_text());assert validation['passed']
 freeze=json.loads((HERE/'freeze.json').read_text());assert all(sha(ROOT/path)==digest for path,digest in freeze['files'].items())
 preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
 OUT.mkdir(parents=True,exist_ok=True)
 with LOCK.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  # Resolve identical saved requests before reading/replanning a fresh intent.
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text())
    assert intent['database']=='math' and intent['endpoint']==ENV['EDB_ENDPOINT'] and intent['lineage']==LINEAGE and intent['source']==SOURCE
    assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    inventory(OUT/'inventory-recovery.json')
    report=DB._commit(intent,path/'transaction.edn',path);verification=verify(path,intent,report)
    finish(path,verification,inventory(path/'inventory-after.json'));return
  for attempt in range(3):
   try:prepare_and_commit(preview);return
   except StaleBasis:
    if attempt==2:raise

if __name__=='__main__':main()
