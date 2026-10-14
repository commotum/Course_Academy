"""Recheck finite catalog under application lock; register, retain, verify."""
import copy,fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import kw,dumps,loads
from inventory_jobs import save
from serve_graph_explorer import database_environment
s=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'67b069bbd9563ed889b84fad1c133a9906d07c384e74023ea1a47e29d17d4360'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-77cf2bd638861f3b';QUERY=(HERE/'reference/source-query.edn').read_text()
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):
 if isinstance(x,dict):return {str(k):canonical(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return sorted([canonical(v) for v in x],key=lambda v:json.dumps(v,sort_keys=True))
 return str(x) if isinstance(x,uuid.UUID) else x

def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def read_kp(path,basis):return DB.query(QUERY,[[KP]],path,'kp',basis)[0][0]
def counts(kp,path,basis):
 shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
 reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
 available=set();excluded=[];records=[];available_ids=[]
 for q in kp[':knowledge-point/questions']:
  t=q.get(':question/math-academy-id');assert t in g.QUESTIONS
  rec=g.replay_source(t);assert g.normalize(q)==rec['question'];v.check(rec);records.append(rec)
  if t not in g.TEMPLATES:excluded.append({'id':q[':db/id'],'reason':'unrated; preserved and excluded'});continue
  if q[':db/id'] in shown|reserved:continue
  available.add(g.fingerprint(t));available_ids.append(q[':db/id'])
 v.grade(records,path/'inventory-grading')
 result={'basis':basis,'distinct_available':{'easy':len(available),'moderate':0,'hard':0},'available_easy_source_ids':available_ids,'shown_ids':sorted(shown),'reserved_ids':sorted(reserved),'excluded':excluded,'canonical_example_excluded':True,'validated_source_questions':len(records)}
 save(path/'available-counts.json',result);return result

def forms(kp,gid):
 gen=kp.get(':knowledge-point/question-generator')
 if gen:
  assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
  return []
 out=[{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator'],[kw('db/ensure'),KP,kw('knowledge-point/validate')]]
 for q in kp[':knowledge-point/questions']:
  out.append([kw('db/ensure'),q[':db/id'],kw('question/validate')])
  for f in q[':question/answer-fields']:
   out.append([kw('db/ensure'),f[':db/id'],kw('answer-field/validate')])
   for a in f[':answer-field/choices']:out.append([kw('db/ensure'),a[':db/id'],kw('answer/validate')])
 return out

def check_report(report,path,source_eid):
 attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 for e,a,value,tx,src,added in report[':edb/tx-data']:
  assert added and src==source_eid,'unexpected retraction or contributor'
  name=attrs[a]
  if e==KP:assert name==':knowledge-point/question-generator'
  elif name!=':db/txInstant':assert e in new and name in (':question-generator/id',':question-generator/script')

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,path/'receipt-check',intent['source_eid']);after=report[':edb/db-after-t']
 kp=read_kp(path/'readback',after);before=loads((path/'before.edn').read_text())
 assert canonical({k:v for k,v in before.items() if k!=':knowledge-point/question-generator'})==canonical({k:v for k,v in kp.items() if k!=':knowledge-point/question-generator'})
 assert not forms(kp,intent['generator_id'])
 stock=counts(kp,path/'readback',after)
 verification={'passed':True,'basis_before':intent['basis'],'basis_after':after,'new_questions':0,'source_questions_unchanged':len(kp[':knowledge-point/questions']),'canonical_example_unchanged':True,'learner_history_unchanged':True,'only_additive_generator_registration_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_after':stock}
 save(path/'verification.json',verification);return verification

def finish(path,gid,verified,inv):
 stock=counts(read_kp(path/'current-inventory',inv['basis']),path/'current-inventory',inv['basis'])
 caps=json.loads((HERE/'capabilities.json').read_text())
 result={'outcome':'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'generator_registered':True,'lineage':LINEAGE,'verified_commit_basis':verified.get('basis_after'),'inventory_recheck_basis':inv['basis'],'new_questions':0,'new_questions_by_level':{'easy':0,'moderate':0,'hard':0},'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'unsupported_levels_filled':False,'available_by_level':stock['distinct_available'],'shortage_by_level':{l:max(0,5-stock['distinct_available'][l]) for l in ('easy','moderate','hard')},'finite_catalog_tasks':10,'additional_distinct_tasks':0,'capability_exceptions':caps['capability_exceptions'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (HERE/'validation.json',HERE/'freeze.json',HERE/'capabilities.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',path/'generated.json',path/'preparation.json',path/'transaction.edn',path/'commit-intent.json',path/'preview.edn',path/'commit.edn',path/'verification.json',path/'inventory-after.json',path/'current-inventory/available-counts.json') if p.exists()],'note':'Finite easy catalog already exists in the bank. No cosmetic copies were committed. Current checkbox response shapes preserved. Moderate/hard remain unsupported by this bounded package; they are not claimed impossible for the KP.'}
 save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_by_level','generator_id')}))

def main():
 validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='passed' and validation['script_sha256']==sha(HERE.with_suffix('.py'))
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
    assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn') and intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert b==DB.basis() and LINEAGE in DB.command('status')
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b)
  assert canonical({k:v for k,v in kp.items() if k!=':knowledge-point/question-generator'})==canonical(g.SOURCE['record']),'source facts changed; reclassify'
  (path/'before.edn').write_text(dumps(kp)+'\n');stock=counts(kp,path,b)
  reg=kp.get(':knowledge-point/question-generator');gid=str(reg[':question-generator/id']) if reg else g.GENERATOR_ID
  identities=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
  assert not identities or (reg and identities[0][0][':db/id']==reg[':db/id'])
  contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
  supplied=JOB.with_suffix('.generated');instances=json.loads(supplied.read_text()).get('instances',[]) if supplied.exists() else []
  if isinstance(instances,dict):instances=[instances]
  for rec in instances:v.check(rec)
  # Execute only after the locked current-inventory read. Exhaust the finite domain.
  proc=subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty','easy','--count','1000','--seed','20261014','--format','json'],capture_output=True,text=True,check=True)
  candidates=json.loads(proc.stdout);save(path/'candidates.json',candidates)
  used={g.fingerprint(q[':question/math-academy-id']) for q in kp[':knowledge-point/questions']}
  for rec in candidates:v.check(rec)
  new=[r for r in candidates if r['generation']['mathematical_fingerprint'] not in used];assert not new,'finite catalog assumption requires new preparation'
  save(path/'generated.json',[])
  assets=[{'reference':ref,'sha256':Path(ref).stem,'reused':True,'stored_bytes_verified':True} for ref in validation['plots']['existing_assets_verified']]
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'available_before':stock,'candidate_tasks':len(candidates),'duplicates_excluded':len(candidates),'new_questions':0,'supplied_generated_exists':supplied.exists(),'supplied_instances_validated':len(instances),'asset_hashes':assets,'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['capability_exceptions']})
  save(HERE/'freeze.json',{'generator_id':gid,'generator_path':SCRIPT,'version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'validation':str((HERE/'validation.json').relative_to(ROOT)),'source_basis':g.SOURCE['basis'],'rechecked_basis':b,'support':['easy'],'finite_catalog_tasks':10})
  txforms=forms(kp,gid)
  if not txforms:
   verified={'passed':True,'basis_after':None,'no_change_basis':b,'new_questions':0};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
  tx=dumps(txforms)+'\n';txpath=path/'transaction.edn'
  with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
  pr=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  (path/'preview.edn').write_text(pr.stdout);report=loads(pr.stdout);assert report[':edb/committed'] is False and report[':edb/db-before-t']==b
  check_report(report,path/'preview-check',contributor[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'neighborhood-finite-register-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent);receipt=DB._commit(intent,txpath,path);verified=verify(path,intent,receipt);finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
