"""Scoped tall-ellipse inventory preparation and locked durable submission."""
import argparse, copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
H=Path(__file__).resolve().parent
ROOT=H.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database, QUESTION_PULL
from edn import dumps, loads, kw
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('ellipse_validation',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID
LEVELS=g.SUPPORTED_LEVELS
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE=g.PROVENANCE['lineage']
SOURCE=':application/ca-engine'
SCRIPT=str(H.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'89bbb335e4e0408e67e0c8e3f82abc900e4597b427867e70eb6aa655e4cfb333'
OUT=H/'reference/replenishment'
LOCK=ROOT/'.local/learning/requests/math/api.lock'
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-80371ed6e5f3669c'
ENGINE=ROOT/'generate/runs/current/check-engine'
QUERY='''[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example Q} {[:knowledge-point/questions :limit nil] Q}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'''.replace('Q',QUESTION_PULL)
USAGE='''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,ENV['EDB_ENDPOINT']],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def canonical(x):
 if isinstance(x,dict):return {str(k):canonical(y) for k,y in x.items()}
 if isinstance(x,(list,tuple,set)):return sorted((canonical(y) for y in x),key=lambda y:json.dumps(y,sort_keys=True))
 if isinstance(x,uuid.UUID):return str(x)
 return x

def normalized(q):
 z={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
 z[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);z[':question/answer-fields']=[]
 for f in q[':question/answer-fields']:
  z[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
 return canonical(z)

def task_key(q):
 f=q[':question/answer-fields'][0];a=f.get(':answer-field/correct')
 if not a:
  sid=q.get(':question/math-academy-id');assert sid in g.SOURCE_GEOMETRY
  return tuple(str(g.rat(n)**2) for n in g.SOURCE_GEOMETRY[sid])
 if isinstance(a,dict):value=a[':answer/value']
 else:value=next(x[':answer/value'] for x in f[':answer-field/choices'] if str(x[':answer/id'])==a[1])
 e=v.residual(value) if '=' in value else v.parse(value)-1
 e=e/(-e.subs({v.X:0,v.Y:0}));return tuple(str(1/e.coeff(s,2)) for s in (v.X,v.Y))

def counts(kp,path,basis):
 unavailable={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'usage',basis)}
 rows={l:[] for l in LEVELS};excluded=[]
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example') or not q.get(':question/difficulty') or not q.get(':question/worked-solution') or not all(f.get(':answer-field/correct') for f in q.get(':question/answer-fields',[])):
   excluded.append(str(q[':question/id']));continue
  level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
  assert level in LEVELS
  rows[level].append(q)
 c={'basis':basis,'levels':{l:{'distinct_available_tasks':len({task_key(q) for q in qs}),'question_ids':[str(q[':question/id']) for q in qs]} for l,qs in rows.items()},'excluded_incomplete_unrated_shown_or_reserved':excluded,'unavailable_entities':sorted(unavailable)}
 save(path/'counts.json',c);return c

def transaction(records,kp,gid):
 forms=[]
 for rec in records:
  q=rec['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen is None:
  forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def check_report(report,path,source):
 attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,value,tx,s,added in report[':edb/tx-data']:
  assert s==source and added,'Unexpected attribution or retraction'
  name=attrs[a]
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,name

def validate_record(r):
 assert r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
 v.displayed_math(r)
 replay=g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=r['generation']['seed'],template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
 assert canonical(replay)==canonical(r),'Deterministic replay mismatch'

def publish(r):
 r=copy.deepcopy(r);q=r['question'];asset=r['generation']['plot'];local=Path(asset['path']);digest=sha(local);relative=ImageLibrary().put_file(local,expected_sha256=digest)
 q[':question/problem']=q[':question/problem'].replace(str(local),relative)
 assert sha(Path('/media/jake/SSD/EDB/math')/relative)==digest
 r['generation']['published_asset']={'relative':relative,'sha256':digest,'local':str(local)}
 return r

def validate_published(r):
 z=copy.deepcopy(r);asset=z['generation'].pop('published_asset');z['question'][':question/problem']=z['question'][':question/problem'].replace(asset['relative'],asset['local']);validate_record(z)
 assert sha(Path('/media/jake/SSD/EDB/math')/asset['relative'])==asset['sha256']

def prepare():
 inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
 path=OUT/f'basis-{basis}';path.mkdir(exist_ok=True)
 assert not (path/'commit-intent.json').exists(),'Recover saved intent first'
 kp=read(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
 assert canonical(kp)==canonical(g.SOURCE['record']),'Source changed since revalidation; reclassify'
 (path/'before.edn').write_text(dumps(kp)+'\n')
 c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
 gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
 source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
 supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
 assert isinstance(instances,list)
 for r in instances:validate_record(r)
 save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
 used={task_key(q) for q in kp[':knowledge-point/questions']};records=[];added={l:0 for l in LEVELS};raw=[]
 for l in LEVELS:
  seed=0
  while added[l]<needed[l] and seed<1000:
   candidates=[r for r in instances if r['question'][':question/difficulty'].endswith('/'+l)] if seed==0 else []
   candidates.append(g.generate(l,seed=seed));seed+=1
   for r in candidates:
    key=task_key(r['question'])
    if key in used or added[l]>=needed[l]:continue
    validate_record(r);used.add(key);raw.append(r);records.append(publish(r));added[l]+=1
 save(path/'raw-generated.json',raw);save(path/'generated.json',records)
 ids=[uuid.UUID(i) for r in records for f in r['question'][':question/answer-fields'] for i in [r['question'][':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]]
 if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identities',basis),'Identity exists; reconcile'
 save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':v.checks(r)} for r in records])
 subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
 forms=transaction(records,kp,gid);tx=dumps(forms)+'\n';(path/'transaction.edn').write_text(tx)
 prep={'basis':basis,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(H.with_suffix('.py')),'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len(raw),'remaining':{l:max(0,needed[l]-added[l]) for l in LEVELS},'asset_hashes':[r['generation']['published_asset'] for r in records],'exact_source_records_unchanged':22,'transaction_sha256':sha(path/'transaction.edn'),'forms':len(forms)}
 save(path/'preparation.json',prep);print(json.dumps({'prepared':str(path),'needed':needed,'new':added,'basis':basis}),flush=True);return path

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_report(report,path/'receipt-check',intent['source_eid'])
 basis=report[':edb/db-after-t'];kp=read(path/'readback',basis);before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items())
 omit={':knowledge-point/questions',':knowledge-point/question-generator'};assert {k:x for k,x in before.items() if k not in omit}=={k:x for k,x in kp.items() if k not in omit}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()};assert len(now)==len(old)+len(records)
 for r in records:
  validate_published(r);q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q;assert normalized(q)==canonical(r['question'])
 assert not transaction([],kp,intent['generator_id'])
 result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':counts(kp,path/'readback',basis)}
 save(path/'verification.json',result);return result

def finish(path,verified,inv):
 prep=json.loads((path/'preparation.json').read_text());c=verified['available_counts_after'];remaining={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':prep['generator_id'],'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'difficulty_evidence':{'easy':'observed integer radii','moderate':'observed half-unit radii','hard':'validated authored same-method third/quarter arithmetic extension; no observed hard source'},'available_counts_before':prep['available_counts'],'available_counts_after':c,'shortage_remaining':remaining,'capability_exceptions':[{'question':'q-7605','reason':'Unrated source missing worked solution and correct reference; malformed lower intercept label; preserved and excluded'}],'finite_domain_tasks':{l:len(g.domain(l)) for l in LEVELS},'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source':SOURCE,'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'preparation.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'inventory-after.json',path/'native-report.json',H/'validation.json',H/'classification.md',H/'template-extraction.md',H/'difficulty-review.md']]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({'outcome':result['outcome'],'basis':result['verified_commit_basis'],'new_questions':result['new_questions'],'shortage_remaining':remaining}),flush=True)

def commit(path):
 prep=json.loads((path/'preparation.json').read_text());txpath=path/'transaction.edn';assert sha(txpath)==prep['transaction_sha256'];assert sha(H.with_suffix('.py'))==prep['generator_sha256']
 for r in json.loads((path/'generated.json').read_text()):validate_published(r)
 intentpath=path/'commit-intent.json'
 if intentpath.exists():
  intent=json.loads(intentpath.read_text());assert intent['lineage']==LINEAGE and intent['exact_edn']==txpath.read_text() and intent['sha256']==sha(txpath)
  assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
 else:
  inv=inventory(path/'inventory-precommit.json');assert inv['basis']==prep['basis']==DB.basis(),'Stale preparation; reprepare'
  kp=read(path/'precommit',prep['basis']);assert kp==loads((path/'before.edn').read_text())
  assert counts(kp,path/'precommit',prep['basis'])==prep['available_counts']
  preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
  assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==prep['basis'];check_report(pr,path/'preview-check',prep['source_eid']);assert DB.basis()==prep['basis']
  intent={**prep,'database':'math','endpoint':DB.args.endpoint,'expected_basis':prep['basis'],'request_key':f'tall-ellipse-inventory-{KP}-{prep["basis"]}-{sha(txpath)}','sha256':sha(txpath),'exact_edn':txpath.read_text(),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK),'question_uuids':[r['question'][':question/id'] for r in json.loads((path/'generated.json').read_text())]}
  with txpath.open('r') as f:os.fsync(f.fileno())
  save(intentpath,intent)
 report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,verified,inventory(path/'inventory-after.json'))

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--commit',type=Path);args=parser.parse_args()
 assert json.loads((H/'validation.json').read_text())['passed']
 with LOCK.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  pending=[p.parent for p in OUT.glob('basis-*/commit-intent.json') if not (p.parent/'verification.json').exists()]
  if pending:assert len(pending)==1;commit(pending[0]);return
  if args.commit:commit(args.commit.resolve())
  else:prepare()
if __name__=='__main__':main()
