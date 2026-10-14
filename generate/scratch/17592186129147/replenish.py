"""Scoped graph-selection replenishment via existing EDB integration."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.RECORD[':db/id'];SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));LINEAGE=g.WRAPPER['lineage'];LEVELS=('easy','moderate','hard');SOURCE=':application/ca-engine';LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'c20c74963f5051c4878102541c6fa24dace855200526835a610070ab80c81477'
OUT=HERE/'reference/replenishment';DB=Database(SimpleNamespace(database='math',edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),endpoint=database_environment('math')['EDB_ENDPOINT']))
QUERY=(HERE/'reference/initial/source-query.edn').read_text()
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l] (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
 (and [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
HISTORY='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q _ _ true] [?kp :knowledge-point/questions ?q]]'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def normalize(q):
 q=json.loads(json.dumps(q,default=str));q={k:q[k] for k in (':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields')}
 if isinstance(q[':question/difficulty'],dict):q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:
  for k in list(f):
   if k not in (':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/correct',':answer-field/choices'):del f[k]
  if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  if isinstance(f[':answer-field/correct'],dict):f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  f[':answer-field/choices']=sorted([{':answer/id':a[':answer/id'],':answer/type':a[':answer/type'][':db/ident'] if isinstance(a[':answer/type'],dict) else a[':answer/type'],':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])
 q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key']);return q

def fingerprint(q):
 q=copy.deepcopy(q);q[':question/problem']=re.sub(r'\$y\s*=\s*', '$y=',q[':question/problem']);return g.fingerprint(v.poly_signature(v.displayed({'question':q})))
def canonical(x):
 if isinstance(x,dict):return {str(k):canonical(y) for k,y in x.items() if not (str(k)==':db/id' and ':db/ident' in x)}
 if isinstance(x,(list,tuple,set)):return sorted([canonical(y) for y in x],key=lambda z:json.dumps(z,sort_keys=True))
 return str(x) if isinstance(x,uuid.UUID) else x

def inventory(path):
 binary=(HERE/'reference/initial/native-path.txt').read_text().strip()
 result=subprocess.run([binary,'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,text=True,capture_output=True,check=True,timeout=55)
 r=json.loads(result.stdout);assert r['ok'];r=r['data'];assert r['lineage']==LINEAGE;save(path,r);return r

def read(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def native(records,path):
 checks=[]
 for r in records:
  f=r['question'][':question/answer-fields'][0]
  checks.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual radio grader: each choice'} for a in f[':answer-field/choices']]})
 save(path/'native-input.json',checks)
 if checks:
  subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True,capture_output=True)
  assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0

def counts(kp,path,basis):
 unavailable={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'shown-reserved',basis)}|{r[0] for r in DB.query(HISTORY,[KP,LEARNER],path,'historical-presentations',basis,history=True)}
 pools={l:{} for l in LEVELS};records=[]
 for q in kp[':knowledge-point/questions']:
  n=normalize(q);level=n[':question/difficulty'].split('/')[-1];fp=fingerprint(n)
  assert len(n[':question/answer-fields'])==1 and n[':question/answer-fields'][0][':answer-field/type']==':answer-field.type/radio'
  if q[':db/id'] not in unavailable:pools[level][fp]=str(q[':question/id'])
  records.append({'knowledge_point':{'db_id':KP,'id':g.RECORD[':knowledge-point/id'],'title':g.RECORD[':knowledge-point/title']},'question':n})
 native(records,path)
 result={'basis':basis,'available':{l:len(p) for l,p in pools.items()},'question_ids':{l:list(p.values()) for l,p in pools.items()},'shown_reserved_or_historically_shown':sorted(unavailable)};save(path/'counts.json',result);return result

def forms(records,kp,gid):
 tx=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:tx.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   tx.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/correct'):f[':answer-field/correct'][1],kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('db/ensure'):kw('answer-field/validate')})
  tx.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 else:tx.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:tx.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if tx:tx.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return tx

def check_report(report,path,source):
 attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values());allowed={':question/'+s for s in ('id','problem','worked-solution','difficulty','answer-fields')}|{':answer-field/'+s for s in ('id','key','type','choices','correct')}|{':answer/'+s for s in ('id','type','value')}|{':question-generator/id',':question-generator/script'}
 for e,a,val,t,s,added in report[':edb/tx-data']:
  assert added and s==source,'Unexpected retraction or attribution';name=attrs[a]
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected change '+name

def verify(path,intent,report):
 assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis'];check_report(report,path/'receipt-check',intent['source_eid'])
 kp=read(path/'readback',report[':edb/db-after-t']);before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(canonical(now[e])==canonical(q) for e,q in old.items());omit={':knowledge-point/questions',':knowledge-point/question-generator'};assert canonical({k:x for k,x in before.items() if k not in omit})==canonical({k:x for k,x in kp.items() if k not in omit})
 records=json.loads((path/'generated.json').read_text());raw=json.loads((path/'validated-raw.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in raw:v.check(r)
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==normalize(r['question'])
  for ref in re.findall(r'!\[\]\(([^)]+)\)',q[':question/problem']):assert ImageLibrary().reference(ref)==ref
 assert not forms([],kp,intent['generator_id'])
 c=counts(kp,path/'readback',report[':edb/db-after-t']);result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in LEVELS},'source_questions_preserved':len(old),'canonical_example_preserved':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'application_contributor_verified':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'counts_after':c};save(path/'verification.json',result);return result

def finish(path,intent,verified):
 inv=inventory(path/'inventory-after.json');assert DB.basis()==inv['basis'];c=counts(read(path/'post-inventory',inv['basis']),path/'post-inventory',inv['basis']);remaining={l:max(0,5-c['available'][l]) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'topic':17592186050601,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level':c['available'],'shortage_remaining':remaining,'finite_variant_limits':{'easy':72,'moderate':672,'hard':336},'capability_exceptions':[],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source':SOURCE,'evidence':[str(p.relative_to(ROOT)) for p in (HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'current-validation.json',path/'preparation.json',path/'verification.json',path/'generated.json',path/'native-report.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'inventory-after.json')]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2),flush=True)

def prepare():
 """Recheck inventory before generating; generation and human visual QA precede commit."""
 OUT.mkdir(parents=True,exist_ok=True);inv=inventory(OUT/'inventory-before-generation.json');basis=inv['basis'];kp=read(OUT/'initial',basis);c=counts(kp,OUT/'initial',basis)
 current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q};assert set(current)==set(g.SOURCES)
 for t,q in g.SOURCES.items():assert normalize(current[t])==normalize(q),'Source requires reclassification'
 assert canonical(kp[':knowledge-point/canonical-example'])==canonical(g.RECORD[':knowledge-point/canonical-example'])
 needed={l:max(0,5-c['available'][l]) for l in LEVELS};used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']));raw=[];added={l:0 for l in LEVELS}
 supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
 if isinstance(instances,dict):instances=[instances]
 def consider(r):
  v.check(r);d=r['generation'];assert not d['raw_evidence_profile'];l=r['question'][':question/difficulty'].split('/')[-1];assert fingerprint(r['question'])==d['mathematical_fingerprint']
  replay=g.generate(l,d['seed'],parameters=d['parameters'],profile=d['bank_profile']);assert normalize(replay['question'])==normalize(r['question'])
  fp=fingerprint(r['question'])
  if added[l]<needed[l] and fp not in used:raw.append(r);used.add(fp);added[l]+=1
 for r in instances:consider(r)
 for l in LEVELS:
  for seed in range(100,1500):
   if added[l]>=needed[l]:break
   consider(g.generate(l,seed))
 save(OUT/'supplied-validation.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')});save(OUT/'validated-candidates.json',raw);native(raw,OUT)
 save(OUT/'candidate-validation.json',{'passed':True,'generation_basis':basis,'needed':needed,'added':added,'unproduced':{l:needed[l]-added[l] for l in LEVELS},'distinct_mathematical_tasks':len({fingerprint(r['question']) for r in raw}),'generator_sha256':sha(HERE.with_suffix('.py')),'validation_sha256':sha(HERE/'validation.json')});print(json.dumps({'basis':basis,'available':c['available'],'added':added,'assets':[r['generation']['plot']['prompt'] for r in raw]},indent=2))

def commit():
 validation=json.loads((HERE/'current-validation.json').read_text());assert validation['passed'] and validation['generator_sha256']==sha(HERE.with_suffix('.py'));assert validation['visual_review_passed']
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text();assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest();assert inventory(path/'recovery-inventory.json')['lineage']==LINEAGE;report=DB._commit(intent,path/'transaction.edn',path);finish(path,intent,verify(path,intent,report));return
  inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b;path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read(path,b);(path/'before.edn').write_text(dumps(kp)+'\n');current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q};assert set(current)==set(g.SOURCES)
  for t,q in g.SOURCES.items():assert normalize(current[t])==normalize(q)
  assert canonical(kp[':knowledge-point/canonical-example'])==canonical(g.RECORD[':knowledge-point/canonical-example']);c=counts(kp,path,b);needed={l:max(0,5-c['available'][l]) for l in LEVELS};added={l:0 for l in LEVELS};raw=[];used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
  for r in json.loads((OUT/'validated-candidates.json').read_text()):
   v.check(r);l=r['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(r['question'])
   if added[l]<needed[l] and fp not in used:raw.append(r);used.add(fp);added[l]+=1
  assert all(added[l]==needed[l] for l in LEVELS),'Inventory changed; return to preparation'
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
  registered=DB.query('[:find (pull ?g [*]) :in $ ?p :where [?g :question-generator/script ?p]]',[SCRIPT],path,'generator-by-path',b);assert len(registered)<=1;gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else str(uuid.uuid5(uuid.UUID(g.RECORD[':knowledge-point/id']),'question-generator'));collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b);assert not collision or collision[0][0][':question-generator/script']==SCRIPT
  records=copy.deepcopy(raw);assets=[];library=ImageLibrary()
  for r in records:
   plot=r['generation']['plot'];ref=library.put_file(plot['prompt'],expected_sha256=sha(Path(plot['prompt'])));assert library.reference(ref)==ref;r['question'][':question/problem']=r['question'][':question/problem'].replace(plot['prompt'],ref);assets.append({'local':plot['prompt'],'relative':ref,'sha256':sha(Path(plot['prompt']))})
  save(path/'validated-raw.json',raw);save(path/'generated.json',records);native(records,path)
  ids=[uuid.UUID(x) for r in records for x in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
  if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identities',b),'Identity reconciliation required'
  save(path/'preparation.json',{'basis':b,'original_job_basis':2188,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_sha256':sha(HERE.with_suffix('.py')),'counts_before':c,'needed':needed,'added':added,'assets':assets,'source_stability_verified':True,'distinctness':'ordered root coordinates, simple/even/odd-multiple categories, leading sign; seed, identity, coefficient magnitude, choice order and bank profile excluded'})
  txpath=path/'transaction.edn';text=dumps(forms(records,kp,gid))+'\n'
  with txpath.open('w') as f:f.write(text);f.flush();os.fsync(f.fileno())
  pr=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55);(path/'preview.edn').write_text(pr.stdout);report=loads(pr.stdout);assert not report[':edb/committed'] and report[':edb/db-before-t']==b;check_report(report,path/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'factored-polynomial-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':text,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);finish(path,intent,verify(path,intent,report))
if __name__=='__main__':prepare() if '--prepare' in sys.argv else commit()
