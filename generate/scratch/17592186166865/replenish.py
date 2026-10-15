"""Requested circle-KP only; additive EDB commit with api.lock and exact receipts."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import build_learning,database_environment
spec=importlib.util.spec_from_file_location('circle_validation',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(H.with_suffix('.py').relative_to(ROOT));OUT=H/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'6d772219705ab759d0f2c76258c8f3fc6ac72646e4c69d4bc73a686127390fcd'
LOCK=ROOT/'.local/learning/requests/math/api.lock';LEVELS=('easy','moderate','hard')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
QUERY=(OUT/'kp-query.edn').read_text()
GENERATOR_ID=str(uuid.uuid5(uuid.UUID(g.R[':knowledge-point/id']),'question-generator'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def plain(x):
 if isinstance(x,dict):return {str(k):plain(z) for k,z in x.items()}
 if isinstance(x,(tuple,list)):return [plain(z) for z in x]
 return str(x) if isinstance(x,uuid.UUID) else x
def inventory(native,path):
 p=subprocess.run([str(native),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=55)
 r=json.loads(p.stdout);assert r['ok'];x=r['data'];assert x['lineage']==LINEAGE;save(path,x);return x

def source_recheck(kp):
 def subset(a,b):
  if isinstance(a,dict):return all(k in b and subset(z,b[k]) for k,z in a.items())
  if isinstance(a,list):return len(a)==len(b) and all(any(subset(z,w) for w in b) for z in a)
  return a==b
 current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
 for old in g.R[':knowledge-point/questions']:
  assert subset(old,plain(current[old[':question/math-academy-id']])),'Changed original source requires classification'
 assert subset(g.R[':knowledge-point/canonical-example'],plain(kp[':knowledge-point/canonical-example']))
 assert set(current)<=set(g.GEOMETRY)|{'q-131253'},'New source requires classification'
 if 'q-131253' in current:
  initial=loads((OUT/'initial-kp.edn').read_text())[0][0]
  expected=next(q for q in initial[':knowledge-point/questions'] if q.get(':question/math-academy-id')=='q-131253')
  assert canonical(current['q-131253'])==canonical(expected)
 return True

def geometry(q):
 sid=q.get(':question/math-academy-id')
 if sid in g.GEOMETRY:return tuple(map(str,g.GEOMETRY[sid]))
 if sid=='q-131253':return None
 # Read geometry independently from the rendered worked solution's circle equation.
 worked=q.get(':question/worked-solution','');m=re.search(r'\$\$\n(.*?)\n\$\$',worked,re.S)
 if not m:return None
 equation=m[1].replace(r'\,','').split('⟹')[-1];lhs,rhs=map(v.scalar,equation.split('='));F=v.s.expand(lhs-rhs)
 h=-F.coeff(v.x,1)/2;k=-F.coeff(v.y,1)/2;r=v.s.sqrt(h*h+k*k-F.subs({v.x:0,v.y:0}))
 assert v.s.simplify(F-((v.x-h)**2+(v.y-k)**2-r*r))==0 and r>0
 return tuple(map(str,(h,k,r)))
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''
def counts(kp,path,basis):
 shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
 reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
 out={l:set() for l in LEVELS};excluded=[]
 for q in kp[':knowledge-point/questions']:
  sid=q.get(':question/math-academy-id');key=geometry(q)
  if key is None:excluded.append({'id':str(q[':question/id']),'source':sid,'reason':'Missing graph/context; separate point-evaluation template'});continue
  if q[':db/id'] in shown|reserved:continue
  fields=q.get(':question/answer-fields',[])
  if not q.get(':question/worked-solution') or not fields or not all(f.get(':answer-field/correct',{}).get(':answer/id') in {a[':answer/id'] for a in f.get(':answer-field/choices',[])} for f in fields):continue
  level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
  if level in out:out[level].add(key)
 result={'basis':basis,'distinct_available':{l:len(z) for l,z in out.items()},'shown_or_reserved':sorted(shown|reserved),'excluded_templates':excluded};save(path/'available-counts.json',result);return result

def check(r):
 assert r['knowledge_point']['db_id']==KP and r['knowledge_point']['id']==g.R[':knowledge-point/id']
 assert r['generation']['eligible_for_learning'] and r['generation']['bank_profile']=='method'
 p=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
 replay=g.generate(level,p['seed'],parameters=p['parameters'],profile=p['bank_profile'])
 expected=copy.deepcopy(replay['question']);local=p['plot'];actual=r['question'][':question/problem']
 if actual!=expected[':question/problem']:
  relative=re.search(r'!\[\]\((images/[^)]+)\)',actual)[1]
  assert (Path('/media/jake/SSD/EDB/math')/relative).read_bytes()==Path(local).read_bytes()
  expected[':question/problem']=expected[':question/problem'].replace(local,relative)
 assert canonical(expected)==canonical(r['question'])
 good=v.check(r);assert geometry(r['question'])==tuple(p['parameters'][k] for k in ('h','k','r'));return good

def publish(records):
 library=ImageLibrary(Path('/media/jake/SSD/EDB/math'));assets=[]
 for rec in records:
  local=rec['generation']['plot'];data=Path(local).read_bytes();relative=library.put_bytes(data)
  assert (library.math_root/relative).read_bytes()==data
  rec['question'][':question/problem']=rec['question'][':question/problem'].replace(local,relative)
  assets.append({'role':'prompt','local_path':local,'database_path':relative,'sha256':hashlib.sha256(data).hexdigest()})
 return assets

def canonical(x):
 if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
 if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
 return str(x) if isinstance(x,uuid.UUID) else x


def tx(records,kp):
 forms=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:
  assert str(gen[':question-generator/id'])==GENERATOR_ID and gen[':question-generator/script']==SCRIPT
 else:
  forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(GENERATOR_ID),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms


def report_checks(report,path,source):
 attrs={eid:str(a) for eid,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':answer/id',':answer/type',':answer/value',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':question-generator/id',':question-generator/script'}
 for e,a,value,t,s,added in report[':edb/tx-data']:
  assert added and s==source, 'Unexpected retraction or attribution'
  name=attrs[a]
  if e==KP:assert name in {':knowledge-point/questions',':knowledge-point/question-generator'}
  elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected non-scoped datom'


def normalized(q):
 x={k:str(q[k]) if k==':question/id' else q[k] for k in [':question/id',':question/problem',':question/worked-solution']};x[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);x[':question/answer-fields']=[]
 for f in q[':question/answer-fields']:
  x[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])]})
 return canonical(x)


def verify(report,path,intent):
 assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
 b=report[':edb/db-after-t'];report_checks(report,path/'receipt-check',intent['source_eid'])
 before=loads((path/'before.edn').read_text());after=DB.query(QUERY,[KP],path/'readback','kp',b)[0][0]
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in after[':knowledge-point/questions']}
 assert all(canonical(q)==canonical(now[e]) for e,q in old.items())
 exclude={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert canonical({k:z for k,z in before.items() if k not in exclude})==canonical({k:z for k,z in after.items() if k not in exclude})
 gen=after[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
  assert normalized(q)==canonical(r['question']);check(r)
 assert len({geometry(r['question']) for r in records})==len(records)
 assert not tx([],after),'Repeated preparation must be a content no-op'
 c=counts(after,path/'readback',b)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'distinct_available_after':c['distinct_available'],'unchanged_existing_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'no_retractions':True,'only_requested_kp_additive_content':True,'source':SOURCE,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
 save(path/'verification.json',result);return result

def finish(path,verified,inv):
 remaining={l:max(0,5-verified['distinct_available_after'][l]) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':GENERATOR_ID,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_by_level':verified['by_level'],'supported_levels':list(LEVELS),'available_after':verified['distinct_available_after'],'shortage_remaining':remaining,'unsupported_levels_filled':False,'capability_exceptions':json.loads((H/'capability.json').read_text()),'inventory_recheck_basis':inv['basis'],'remaining_native_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [H/'validation.json',H/'classification.md',H/'template-extraction.md',H/'capability.json',path/'preparation.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json']],'note':'All original source questions, the canonical example and learner history are preserved. The contextual blank source remains excluded from independent usable inventory. Hard is an authored fractional-center extension; easy circle/radius diversity is distinct from derivative diversity.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2),flush=True)

def main():
 global GENERATOR_ID
 assert json.loads((H/'validation.json').read_text())['passed']
 frozen=json.loads((H/'freeze.json').read_text())['files'];assert sha(H.with_suffix('.py'))==frozen[SCRIPT]
 native=build_learning(ROOT.parent/'EDB')
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());GENERATOR_ID=intent['generator_id']
    assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(report,path,intent);finish(path,verified,inventory(native,path/'inventory-after.json'));return
  inv=inventory(native,OUT/'inventory-locked.json');b=inv['basis'];assert DB.basis()==b and LINEAGE in DB.command('status')
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
  kp=DB.query(QUERY,[KP],path,'kp',b)[0][0];source_recheck(kp);(path/'before.edn').write_text(dumps(kp)+'\n')
  reg=kp.get(':knowledge-point/question-generator')
  if reg:
   GENERATOR_ID=str(reg[':question-generator/id']);assert reg[':question-generator/script']==SCRIPT
  save(H/'generator-registration.json',{'id':GENERATOR_ID,'script':SCRIPT,'knowledge_point':KP,'version':g.VERSION,'generator_sha256':sha(H.with_suffix('.py'))})
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
  c=counts(kp,path,b);needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS}
  used={geometry(q) for q in kp[':knowledge-point/questions']};records=[];supplied_status=[]
  supplied=json.loads(JOB.with_suffix('.generated').read_text()) if JOB.with_suffix('.generated').exists() else {}
  instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
  for r in instances:
   check(r);l=r['question'][':question/difficulty'].split('/')[-1];key=geometry(r['question'])
   status='accepted' if needed[l]>0 and key not in used else 'duplicate-or-no-current-shortage'
   supplied_status.append({'id':r['question'][':question/id'],'status':status})
   if status=='accepted':records.append(r);used.add(key);needed[l]-=1
  # Deterministic traversal of bounded parameters: no identity/profile/choice-order inflation.
  domains={'easy':({'h':0,'k':0,'r':str(r)} for r in g.EASY_RADII),'moderate':({'h':h,'k':k,'r':r} for h,k,r in [(2,1,2),(-2,3,3),(3,-1,2),(-1,-3,3),(0,3,2),(3,0,2)]+[(h,k,r) for h in range(-4,5) for k in range(-4,5) if h or k for r in g.MOD_RADII]),'hard':({'h':str(h),'k':str(k),'r':'3/2'} for h in g.HARD_CENTERS for k in g.HARD_CENTERS)}
  for l in LEVELS:
   for p in domains[l]:
    if needed[l]==0:break
    key=tuple(str(g.sp.sympify(p[k])) for k in ('h','k','r'))
    if key in used:continue
    r=g.generate(l,seed=1846674,parameters=p);check(r)
    records.append(r);used.add(key);needed[l]-=1
  save(path/'generated-local.json',records)
  assets=publish(records)
  save(path/'generated.json',records);(path/'review.md').write_text('\n\n'.join(g.markdown(r) for r in records)+'\n')
  native_items=[]
  for r in records:
   good=check(r);native_items.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==good else 'rejected','purpose':'full generated radio bank'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]})
  save(path/'native-input.json',native_items)
  subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
  native_report=json.loads((path/'native-report.json').read_text());assert native_report['documented_unresolved_checks']==0
  for attr,key,ids in [('question/id','q',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field/id','f',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer/id','a',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
   if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[ids],path,'identity-'+key,b),'Existing identity requires reuse/reconciliation'
  gid=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(GENERATOR_ID)],path,'generator-identity',b);assert not gid or len(gid)==1 and gid[0][0][':question-generator/script']==SCRIPT
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_evidence_unchanged':True,'available_before':c,'new_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'new_questions':len(records),'shortage_remaining':needed,'supplied_generated_file_exists':JOB.with_suffix('.generated').exists(),'supplied_status':supplied_status,'distinct_circle_tasks':len({geometry(r['question']) for r in records}),'distinct_derivatives_by_level':{l:len({r['generation']['derivative_fingerprint'] for r in records if r['question'][':question/difficulty'].endswith('/'+l)}) for l in LEVELS},'generator_version':g.VERSION,'generator_sha256':sha(H.with_suffix('.py')),'validator_sha256':sha(H/'validate.py'),'validation_sha256':sha(H/'validation.json'),'native_engine_sha256':sha(ROOT/'generate/runs/current/check-engine'),'asset_hashes':assets,'lock':str(LOCK)})
  forms=tx(records,kp);assert forms,'No content changes required'
  txpath=path/'transaction.edn';text=dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(text);f.flush();os.fsync(f.fileno())
  result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  (path/'preview.edn').write_text(result.stdout);pr=loads(result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;report_checks(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','lineage':LINEAGE,'endpoint':DB.args.endpoint,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'sha256':sha(txpath),'exact_edn':text,'request_key':'circle-slope-replenish-'+str(b)+'-'+sha(txpath),'generator_id':GENERATOR_ID,'generator_path':SCRIPT,'generator_sha256':sha(H.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()}
  save(path/'commit-intent.json',intent)
  report=DB._commit(intent,txpath,path);verified=verify(report,path,intent);finish(path,verified,inventory(native,path/'inventory-after.json'))
if __name__=='__main__':main()
