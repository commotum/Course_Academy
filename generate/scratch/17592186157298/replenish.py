"""Scoped additive preparation/commit; serialize with the application through readback."""
import copy, fcntl, hashlib, importlib.util, json, os, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('validator',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP;SOURCE=':application/ca-engine';LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'ceb828f8b064144748de68fb6aa717b3f5efa559cad1300daab4f4c707184799'
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-9793bad6fcb9390e';QUERY=(HERE/'reference/initial/source-query.edn').read_text()
LOCK=ROOT/'.local/learning/requests/math/api.lock'
SHOWN='[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?task] [?task :learner-task/items ?item] [?item :task-item/content ?q]]'
RESERVED='[:find ?q :in $ ?kp ?learner [?state ...] :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?task] [?task :learner-task/status ?status] [?status :db/ident ?state] [?task :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'
EXCLUDED={'q-161100':'Solution diagram labels squared radius as 1 instead of 2','q-161101':'Zero denominator in intermediate worked step','q-83975':'Wrong angular density in intermediate worked step','q-85062':'Inconsistent signed diagram label'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),text=True,capture_output=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok']and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def read(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def canonical(z):
 if isinstance(z,dict):return {str(k):canonical(v)for k,v in z.items()}
 if isinstance(z,(tuple,list)):return sorted([canonical(v)for v in z],key=lambda v:json.dumps(v,sort_keys=True))
 return str(z)if isinstance(z,uuid.UUID)else z

def as_record(q):
 q=copy.deepcopy(q);fs=[]
 for f in q[':question/answer-fields']:
  fs.append({':answer-field/id':str(f[':answer-field/id']),':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/key':f[':answer-field/key'],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']}for a in f[':answer-field/choices']]})
 return {'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':{':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':fs},'generation':{'template':q.get(':question/math-academy-id','persisted'),'profile':'current-source'}}
def retained():
 return {r['question'][':question/id']:r for p in OUT.glob('basis-*/generated.json')for r in json.loads(p.read_text())}
def counts(kp,path,basis):
 path.mkdir(parents=True,exist_ok=True);unavailable={row[0]for row in DB.query(SHOWN,[KP,LEARNER],path,'shown',basis)}
 unavailable.update(row[0]for row in DB.query(RESERVED,[KP,LEARNER,[kw('learner-task.status/started'),kw('learner-task.status/paused')]],path,'reserved',basis))
 existing=retained();good=[];excluded=[];fixtures=[];seen=set()
 for q in kp.get(':knowledge-point/questions',[]):
  if q[':db/id']in unavailable:excluded.append({'id':str(q[':question/id']),'reason':'shown or reserved'});continue
  sid=q.get(':question/math-academy-id');qid=str(q[':question/id'])
  if sid in EXCLUDED:excluded.append({'id':qid,'source_id':sid,'reason':EXCLUDED[sid]});continue
  if sid in g.ORIGINALS:
   assert canonical(q)==canonical(g.ORIGINALS[sid]),'Source changed: reclassify'
   r=as_record(q);f=r['question'][':question/answer-fields'][0];assert len(f[':answer-field/choices'])==5
   # Source answer/domain correctness established by full-bank replay.
   fp=v.signature(sid,1)
  elif qid in existing:
   rec=existing[qid];original=copy.deepcopy(rec);original['generation'].pop('published_assets',None);v.check(original);r=as_record(q)
   expected=copy.deepcopy(rec['question'])
   for role,asset in rec['generation'].get('published_assets',{}).items():
    for k in (':question/problem',':question/worked-solution'):expected[k]=expected[k].replace(rec['generation']['assets'][role],asset)
   assert canonical(r['question'])==canonical(expected)
   fp=v.signature(rec['generation']['template'],rec['generation']['parameters']['scale'])
  else:excluded.append({'id':qid,'reason':'No retained mathematical validation'});continue
  if fp in seen:excluded.append({'id':qid,'reason':'Duplicate mathematical task'});continue
  seen.add(fp);good.append(qid);fixtures.append(v.native(r,qid))
 save(path/'grading-input.json',fixtures);subprocess.run([str(HERE/'check-engine'),str(path/'grading-input.json'),str(path/'grading-report.json')],check=True)
 result={'basis':basis,'available':{'easy':0,'moderate':len(good),'hard':0},'distinct_available_question_ids':good,'excluded':excluded,'shown_or_reserved':sorted(unavailable),'validated_by_actual_learner_grader':True};save(path/'counts.json',result);return result

def publish(rec,path):
 q=copy.deepcopy(rec['question']);assets={};manifest=[]
 for role,ref in rec['generation']['assets'].items():
  src=ROOT/ref;h=sha(src);relative='images/'+h[:2]+'/'+h+'.png';dest=Path(database_environment('math')['EDB_MATH_ROOT'])/relative;dest.parent.mkdir(parents=True,exist_ok=True)
  if not dest.exists():
   with dest.open('xb')as f:f.write(src.read_bytes());f.flush();os.fsync(f.fileno())
  assert sha(dest)==h
  assets[role]=relative;manifest.append({'role':role,'local':ref,'database_path':relative,'sha256':h,'verified':True})
  for key in (':question/problem',':question/worked-solution'):q[key]=q[key].replace(ref,relative)
 rec['generation']['published_assets']=assets
 save(path/('assets-'+q[':question/id']+'.json'),manifest)
 return q

def transaction(records,kp,gid,path):
 forms=[]
 for rec in records:
  q=publish(rec,path)
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id']for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id']for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:
  assert str(gen[':question-generator/id'])==gid
  if gen.get(':question-generator/script')!=SCRIPT:forms.append([kw('db/add'),gen[':db/id'],kw('question-generator/script'),SCRIPT])
 else:forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id']for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def check_report(report,path,source):
 attrs={e:str(a)for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,value,tx,s,added in report[':edb/tx-data']:
  name=attrs[a];assert s==source and added,'Unexpected attribution or retraction'
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed

def verify(path,intent,report):
 assert report[':edb/committed']is True and report[':edb/db-before-t']==intent['basis'];check_report(report,path/'receipt-check',intent['source_eid']);basis=report[':edb/db-after-t'];kp=read(path/'readback',basis);before=loads((path/'before.edn').read_text())
 old={str(q[':question/id']):q for q in before[':knowledge-point/questions']};now={str(q[':question/id']):q for q in kp[':knowledge-point/questions']}
 assert all(canonical(q)==canonical(now[qid])for qid,q in old.items()),'Source questions changed'
 assert canonical({k:v for k,v in before.items()if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:v for k,v in kp.items()if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id']and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
 for rec in records:
  q=now[rec['question'][':question/id']];assert ':question/math-academy-id'not in q
  exp=copy.deepcopy(rec['question'])
  for role,ref in rec['generation']['published_assets'].items():
   assert sha(Path(database_environment('math')['EDB_MATH_ROOT'])/ref)==ref.split('/')[-1].split('.')[0]
   for k in (':question/problem',':question/worked-solution'):exp[k]=exp[k].replace(rec['generation']['assets'][role],ref)
  assert canonical(as_record(q)['question'])==canonical(exp)
 c=counts(kp,path/'readback-counts',basis)
 assert not transaction([],kp,intent['generator_id'],path)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_existing_questions':len(old),'learner_history_unchanged':True,'only_scoped_additive_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c};save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
 c=verified['available_counts_after'];remaining={l:max(0,5-c['available'][l])for l in ('easy','moderate','hard')}
 result={'outcome':'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':['moderate'],'unsupported_levels':['easy','hard'],'unsupported_levels_filled':False,'available_counts_after':c,'shortage_remaining':remaining,'capability_exceptions':json.loads((HERE/'validation.json').read_text())['capability_exceptions'],'finite_new_variant_limit':121,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs']if j['knowledgePoint']==KP],'note':'Moderate reserve is validated against current inventory. Easy and hard remain unsupported and retain explicit deficits. Existing source content and learner history are preserved. Generator registration resolves the classification trigger; it does not fill unsupported levels.','evidence':[str(p.relative_to(ROOT))for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',HERE/'validation.json',HERE/'engine-report.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md']]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k]for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def main():
 val=json.loads((HERE/'validation.json').read_text());assert val['status']=='passed'and val['generator_sha256']==sha(HERE.with_suffix('.py'))and val['validator_sha256']==sha(HERE/'validate.py')
 preview=preview_executable(SimpleNamespace(math_root=Path(database_environment('math')['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
 print('Waiting for application lock',flush=True)
 with LOCK.open('a')as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);print('Application lock acquired; rechecking current inventory',flush=True);inv=inventory(OUT/'inventory-under-lock.json');assert DB.basis()==inv['basis']
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math'and intent['endpoint']==DB.args.endpoint and intent['lineage']==inv['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn')and intent['exact_edn']==(path/'transaction.edn').read_text()and intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
  basis=inv['basis'];path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
  (path/'before.edn').write_text(dumps(kp)+'\n');source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id'])if gen else g.uid('question-generator')
  c=counts(kp,path/'counts-before',basis);needed=max(0,5-c['available']['moderate']);print('Validated availability '+str(c['available'])+'; moderate shortage '+str(needed),flush=True)
  used={v.signature(sid,1)for sid in g.DATA};known=retained();used.update(v.signature(rec['generation']['template'],rec['generation']['parameters']['scale'])for rec in known.values())
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text())if supplied_path.exists()else{};instances=supplied.get('instances',[]);assert isinstance(instances,list)
  for rec in instances:
   assert set(rec['generation']['assets'])=={'prompt','solution'},'Missing essential region diagrams'
   v.check(rec)
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')});records=[]
  for rec in instances:
   fp=v.signature(rec['generation']['template'],rec['generation']['parameters']['scale'])
   if len(records)<needed and fp not in used:records.append(rec);used.add(fp)
  for scale in range(2,13):
   for sid in g.DATA:
    if len(records)>=needed:break
    fp=v.signature(sid,scale)
    if fp in used:continue
    rec=g.generate('moderate',int(JOB.name[:8],16),sid,scale);v.check(rec);records.append(rec);used.add(fp)
  save(path/'generated.json',records)
  ids=[uuid.UUID(a)for rec in records for a in [rec['question'][':question/id']]+[f[':answer-field/id']for f in rec['question'][':question/answer-fields']]+[a[':answer/id']for f in rec['question'][':question/answer-fields']for a in f[':answer-field/choices']]]
  if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-collisions',basis)
  save(path/'grading-input.json',[v.native(rec,rec['question'][':question/id'])for rec in records]);subprocess.run([str(HERE/'check-engine'),str(path/'grading-input.json'),str(path/'grading-report.json')],check=True)
  forms=transaction(records,kp,gid,path);save(path/'generated.json',records);save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'available_counts':c,'supported_shortage':needed,'new_questions':len(records),'remaining_supported_shortage':needed-len(records),'capability_exceptions':val['capability_exceptions'],'generator_sha256':sha(HERE.with_suffix('.py')),'source_history_unchanged':True,'parameters':[rec['generation']for rec in records]})
  if not forms:
   verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
  txpath=path/'transaction.edn';text=dumps(forms)+'\n'
  with txpath.open('w')as f:f.write(text);f.flush();os.fsync(f.fileno())
  fresh=inventory(path/'inventory-precommit.json');assert fresh['basis']==basis and fresh['lineage']==LINEAGE and DB.basis()==basis
  result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,check=True,timeout=90);(path/'preview.edn').write_text(result.stdout);pr=loads(result.stdout);assert pr[':edb/committed']is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'polar-cap-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':text,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id']for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
  save(path/'commit-intent.json',intent);print('Submitting saved exact request at basis '+str(basis),flush=True);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
