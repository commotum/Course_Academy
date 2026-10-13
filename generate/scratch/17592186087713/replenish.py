"""Scoped, additive inventory replenishment using the configured EDB integration.

Holds application api.lock from fresh inventory through durable submission and
exact-basis readback. Retains requests/receipts and recovers before new intent.
"""
import copy, fcntl, hashlib, importlib.util, json, os, pathlib, subprocess, sys, threading, uuid
from types import SimpleNamespace
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import kw,dumps,loads
from inventory_jobs import save
from serve_graph_explorer import database_environment
from capture.scripts.database.preview import preview_executable
from validate_checkbox import g,validate,v
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
SOURCE=':application/ca-engine';LINEAGE=g.SOURCE['lineage']
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'1cda4bf6c4f95b69eb4b027196aa26f56ecbd9aa103f950af7ccdb1eb9ee2db5'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint='/tmp/edb-math/writer.sock'))
NATIVE=max((p for p in (ROOT/'.local/graph-explorer').glob('learning-*') if p.is_file()),key=lambda p:p.stat().st_mtime)
PATTERN='''[* {:knowledge-point/question-generator [*]}
 {[:knowledge-point/questions :limit nil] [* {:question/difficulty [:db/ident]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {[:answer-field/choices :limit nil] [* {:answer/type [:db/ident]}]}]}]}]'''
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok'];x=x['data'];assert x['lineage']==LINEAGE;save(path,x);return x

def read_kp(path,basis):
 return DB.query('[:find (pull ?kp '+PATTERN+') :in $ ?kp :where [?kp :knowledge-point/id _]]',[KP],path,'kp',basis)[0][0]

def fingerprint(q):
 target,arrays=v.parse_prompt(q[':question/problem'])
 return g.digest({'criterion':'ordered-row-column-dimensions','target':list(target),'candidate_dimensions':sorted(list(a[1]) for a in arrays)})

def normalize(q):
 def answer(a):return {':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']}
 return {':question/id':str(q[':question/id']),':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/answer-fields':sorted([{':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([answer(a) for a in f[':answer-field/choices']],key=lambda a:a[':answer/value'])} for f in q[':question/answer-fields']],key=lambda f:f[':answer-field/key'])}

def ordered(q):
 q=copy.deepcopy(q);q[':question/answer-fields']=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])
 for f in q[':question/answer-fields']:f[':answer-field/choices']=sorted(f[':answer-field/choices'],key=lambda a:a[':answer/value'])
 return q

def transaction(records,kp,gid):
 forms=[]
 for rec in records:
  q=rec['question'];qt=q[':question/id'];fields=[]
  for f in q[':question/answer-fields']:
   ft=f[':answer-field/id'];fields.append(ft);answers=[]
   for a in f[':answer-field/choices']:
    at=a[':answer/id'];answers.append(at)
    forms.append({kw('db/id'):at,kw('answer/id'):uuid.UUID(at),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):ft,kw('answer-field/id'):uuid.UUID(ft),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):answers,kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):qt,kw('question/id'):uuid.UUID(qt),kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/answer-fields'):fields,kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator');script=str(HERE.with_suffix('.py').relative_to(ROOT))
 if gen is None:
  forms.append({kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):script})
  forms.append([kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator'])
 elif gen.get(':question-generator/script')!=script:
  raise ValueError('Registered script differs; preserve existing registration for reconciliation')
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records],kw('db/ensure'):kw('knowledge-point/validate')})
 return forms

def check_report(report,path,source_eid):
 attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 for e,a,value,tx,source,added in report[':edb/tx-data']:
  name=attrs[a];assert source==source_eid and added,'Unexpected source or retraction'
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name==':db/txInstant':pass
  else:
   assert e in new and name in {':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'},name

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,path/'readback',intent['source_eid']);after=report[':edb/db-after-t'];kp=read_kp(path/'readback',after)
 before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items()),'Original source question changed'
 assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'];assert gen[':question-generator/script']==intent['generator_path']
 records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
 assert len(now)==len(old)+len(records)
 for rec in records:
  q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
  assert normalize(q)==ordered(rec['question']);assert fingerprint(q)==rec['generation']['mathematical_task_fingerprint'];validate(rec)
 assert not transaction([],kp,intent['generator_id']), 'Registration replan is not a no-op'
 result={'passed':True,'basis_before':intent['basis'],'basis_after':after,'new_questions':len(records),'source':SOURCE,'unchanged_source_questions':len(old),'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'exact_question_field_answer_readback':True}
 save(path/'verification.json',result);return result

def main():
 cv=json.loads((HERE/'reference/checkbox-validation.json').read_text());assert cv['passed'] and cv['generator_sha256']==sha(HERE.with_suffix('.py'))
 preview=preview_executable(SimpleNamespace(math_root=pathlib.Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  # Recover any retained exact submission before computing fresh intent.
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn')
    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report)
    inv=inventory(path/'inventory-after.json');finish(path,intent,verified,inv);return
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
  kp=read_kp(path,b);(path/'before.edn').write_text(dumps(kp)+'\n');assert str(kp[':knowledge-point/id'])==g.KP_UUID
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_ID
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1;source_eid=source[0][0]
  jobs={j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP and j['difficulty']!='unclassified'}
  represented={q[':question/difficulty'][':db/ident'].rsplit('/',1)[-1] for q in kp[':knowledge-point/questions'] if ':question/difficulty' in q}
  needed={level:jobs[level]['missing'] if level in jobs else 0 if level in represented else 5 for level in ('easy','moderate','hard')}
  used={fingerprint(q) for q in kp[':knowledge-point/questions']};records=[];exceptions=[]
  generated_path=JOB.with_suffix('.generated')
  saved=json.loads(generated_path.read_text()) if generated_path.exists() else {};supplied=saved.get('instances',[]);save(path/'supplied-status.json',{'exists':generated_path.exists(),'supplied_instances':len(supplied)})
  for level,count in needed.items():
   accepted=[]
   for rec in supplied:
    if rec['generation']['level']==level and len(accepted)<count:
     validate(rec);fp=rec['generation']['mathematical_task_fingerprint']
     if fp not in used:used.add(fp);accepted.append(rec)
   for seed in range(10000):
    if len(accepted)>=count:break
    rec=g.generate(level,seed);fp=rec['generation']['mathematical_task_fingerprint']
    if fp not in used:validate(rec);used.add(fp);accepted.append(rec)
   records.extend(accepted)
   if len(accepted)<count:exceptions.append({'level':level,'required':count,'generated':len(accepted),'shortage':count-len(accepted),'finite_catalog':cv['finite_catalog'][level],'bounded_search_seeds':10000})
  save(path/'generated.json',records)
  checks=[{'label':rec['question'][':question/id'],'record':rec,'checks':validate(rec)} for rec in records];save(path/'native-input.json',checks)
  subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
  forms=transaction(records,kp,gid);assert forms,'No content or registration changes'
  tx=dumps(forms)+'\n';txpath=path/'transaction.edn'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
  (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,path/'preview-check',source_eid)
  assert DB.basis()==b,'Basis advanced under application lock; preparation must be refreshed'
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source_eid,'basis':b,'expected_basis':b,'request_key':'matrix-description-replenish-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':str(HERE.with_suffix('.py').relative_to(ROOT)),'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'needed':needed,'capability_exceptions':exceptions,'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent)
  report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
  invafter=inventory(path/'inventory-after.json');finish(path,intent,verified,invafter)

def finish(path,intent,verified,inv):
 remaining=[j for j in inv['jobs'] if j['knowledgePoint']==KP]
 result={'outcome':'finite-limit' if intent['capability_exceptions'] else 'generated','knowledgePoint':KP,'generator':intent['generator_path'],'generator_path':intent['generator_path'],'generator_id':intent['generator_id'],'verified_commit_basis':verified['basis_after'],'basis_before':intent['basis'],'lineage':LINEAGE,'new_questions':verified['new_questions'],'by_level':intent['needed'],'source':SOURCE,'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'native-report.json',HERE/'reference/checkbox-validation.json',HERE/'validation.json')],'inventory_recheck_basis':inv['basis'],'remaining_shortages':remaining,'capability_exceptions':intent['capability_exceptions'],'finite_catalog':{'easy':12,'moderate':1920,'hard':25},'distinctness':'Ordered target dimensions and unordered candidate shape multiset; excludes entry, label, choice-order and seed changes.'}
 save(JOB.with_suffix('.result'),result);save(path/'outcome.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':main()
