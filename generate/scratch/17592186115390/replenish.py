"""Scoped inventory generation and basis-guarded additive commit for KP 17592186115390."""
import copy, fcntl, hashlib, importlib.util, json, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database, StaleBasis
from edn import kw,dumps,loads
from inventory_jobs import save
from serve_graph_explorer import database_environment,build_learning
spec=importlib.util.spec_from_file_location('kp_validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
spec=importlib.util.spec_from_file_location('scoped_commit_helpers',ROOT/'generate/scratch/17592186133881/commit_helpers.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
KP=g.KP_ID;TOPIC=17592186048233;LEVELS=('easy','moderate','hard');LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
SOURCE=':application/ca-engine';SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'3601cd5cb57d806b4cbd6bbdf087469f985930809ee8611d5e1e27ac301649ef'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
S=json.loads((HERE/'source.json').read_text());LINEAGE=S['lineage']
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
h.DB=DB;h.KP=KP;h.SCRIPT=SCRIPT
QUERY=(ROOT/'generate/scratch/17592186133876/reference/source-query.edn').read_text()
ENGINE=HERE/'check-current-engine';POOL=HERE/'check-current-pool'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def legacy_matrix(value):
 """Bounded notation normalization for the current source's bmatrix repair."""
 if isinstance(value,str):return value.replace(r'\begin{bmatrix}',r'[\begin{aligned}').replace(r'\end{bmatrix}',r'\end{aligned}]')
 if isinstance(value,dict):return {k:legacy_matrix(x) for k,x in value.items()}
 if isinstance(value,list):return [legacy_matrix(x) for x in value]
 return value
def read_kp(path,b):return DB.query(QUERY,[KP],path,'kp',b)[0][0]
def build_native():
 deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps'
 libs={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')}
 harnesses={ENGINE:ROOT/'generate/runs/current/check-engine.rs',POOL:ROOT/'generate/scratch/17592186110754/check-pool.rs'}
 for exe,src in harnesses.items():
  cmd=['rustc','--edition=2024','-O',str(src)]
  for name,p in libs.items():cmd+=['--extern',name+'='+str(p)]
  subprocess.run(cmd+['-L','dependency='+str(deps),'-L','dependency='+str(edb),'-o',str(exe)],check=True)
 save(OUT/'native-build.json',{'libraries':{str(p):sha(p) for p in libs.values()},'harnesses':{str(p.relative_to(ROOT)):sha(p) for p in harnesses.values()},'executables':{str(p.relative_to(ROOT)):sha(p) for p in harnesses}})
def native(records,path):
 path.mkdir(parents=True,exist_ok=True);items=[]
 for r in records:
  f=r['question'][':question/answer-fields'][0]
  items.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete bank choice grading'} for a in f[':answer-field/choices']]})
 save(path/'native-input.json',items);subprocess.run([str(ENGINE),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
 assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0

def printed_data(q,name):
 prompt=legacy_matrix(q[':question/problem']);layout=g.BASES[name][4] if name in g.BASES else 'basis'
 if layout=='basis':
  # Read both compact generated and spaced source aligned equations.
  raws=re.findall(r'&\s*=\s*(.*?)(?= \\\\|\\end\{aligned\})',prompt,re.S)
  fs=[v.basis(x) for x in raws]
 else:fs=[g.vector(x) for x in v.vectors(prompt)]
 target=re.search(r'\$([^$]+)\$',prompt)[1].replace(r'\mathbf','').replace('^{′}','').replace("'",'')
 pairs=re.findall(r'([+-]?\s*\d*)\s*([fgh])\(t\)',target)
 assert len(pairs)==len(fs),(name,pairs,fs)
 cs=[]
 for s,n in pairs:
  s=s.replace(' ','');cs.append(-1 if s=='-' else 1 if s in ('','+') else int(s))
 pointmatch=re.search(r'at \$t\s*=\s*([+-]?\d+)',prompt);point=int(pointmatch[1]) if pointmatch else None
 return fs,cs,point

def fingerprint(q,name):
 fs,cs,point=printed_data(q,name)
 # Conservatively collapse equivalent combined givens, all banks, seeds and order.
 combined=g.total(fs,cs)
 return hashlib.sha256(json.dumps({'combined':[g.sp.srepr(g.sp.simplify(x)) for x in combined],'point':point},sort_keys=True).encode()).hexdigest()
def validate(r):
 assert r['knowledge_point']['db_id']==KP and r['knowledge_point']['id']==g.KP_UUID
 m=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1];assert level in LEVELS
 stages=v.mathcheck(r)
 replay=g.generate(level,m['seed'],m['template'],parameters=m['parameters'],profile=m['bank_profile'])
 assert h.ordered(replay['question'])==h.ordered(r['question'])
 assert replay['generation']==m,'Metadata does not match deterministic replay'
 return fingerprint(r['question'],m['template'])
def retained():
 return {r['question'][':question/id']:r for file in OUT.glob('basis-*/generated.json') for r in json.loads(file.read_text())}
def inventory(binary,path):
 x=subprocess.run([str(binary),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
 result=json.loads(x.stdout);assert result['ok'] and result['data']['lineage']==LINEAGE
 save(path,result['data']);return result['data']
def counts(kp,b,path):
 path.mkdir(parents=True,exist_ok=True)
 shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],path,'ever-shown',b,history=True)
 reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?s] (or [?s :db/ident :learner-task.status/started] [?s :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],path,'reserved',b)
 seen={r[0] for r in shown+reserved};entities={str(i+1):{'db/ident':name} for i,name in enumerate(('question.difficulty/easy','question.difficulty/moderate','question.difficulty/hard','answer-field.type/radio','answer.type/math'))}
 enum=lambda x:str(x[':db/ident']).lstrip(':')
 for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
  entities[str(q[':db/id'])]={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[f[':db/id'] for f in q.get(':question/answer-fields',[])]}
  if ':question/difficulty' in q:entities[str(q[':db/id'])]['question/difficulty']=enum(q[':question/difficulty'])
  for f in q.get(':question/answer-fields',[]):
   d={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f[':answer-field/choices']]}
   if ':answer-field/correct' in f:d['answer-field/correct']=f[':answer-field/correct'][':db/id']
   entities[str(f[':db/id'])]=d
   for a in f[':answer-field/choices']:entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
 entities[str(KP)]={'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id'],'knowledge-point/title':kp[':knowledge-point/title']}
 save(path/'snapshot.json',{'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)})
 subprocess.run([str(POOL),str(path/'snapshot.json'),str(path/'pool.json')],check=True,capture_output=True)
 pool=json.loads((path/'pool.json').read_text());known=retained();byid={q[':db/id']:q for q in kp[':knowledge-point/questions']};keys={l:set() for l in LEVELS};exclusions=[];records=[]
 for level,ids in pool['available_ids_by_level'].items():
  for eid in ids:
   q=byid[eid];sid=q.get(':question/math-academy-id')
   try:
    if sid in g.DATA:
     r=g.generate(level,template=sid,parameters={'scales':[1,1,1]},profile=sid);r['question']=legacy_matrix(h.normalize(q))
     v.mathcheck(r);key=fingerprint(q,sid)
    else:
     r=known[str(q[':question/id'])];assert h.normalize(q)==h.ordered(r['question']);key=validate(r)
    keys[level].add(key);records.append(r)
   except (AssertionError,ValueError,KeyError) as error:exclusions.append({'entity':eid,'source':sid,'reason':'Source is unrated/incomplete or has invalid math/domain/solution; preserved and excluded: '+str(error)[:300]})
 native(records,path/'available-grading')
 result={'basis':b,'distinct_available':{l:len(keys[l]) for l in LEVELS},'remaining_shortage':{l:max(0,5-len(keys[l])) for l in LEVELS},'native_pool':pool,'mathematical_exclusions':exclusions,'ever_shown':sorted({r[0] for r in shown}),'reserved':sorted({r[0] for r in reserved}),'distinctness':'exact simplified combined supplied vector and evaluation point; seed, identity, choice order and bank ignored'}
 save(path/'validated-counts.json',result);return result

def verify(path,intent,receipt):
 assert receipt[':edb/committed'] is True and receipt[':edb/db-before-t']==intent['basis'];h.check_report(receipt,path/'receipt-check',intent['source_eid'])
 b=receipt[':edb/db-after-t'];kp=read_kp(path/'readback',b);before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items());omit={':knowledge-point/questions',':knowledge-point/question-generator'};assert {k:x for k,x in before.items() if k not in omit}=={k:x for k,x in kp.items() if k not in omit}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:assert h.normalize(byid[r['question'][':question/id']])==h.ordered(r['question']);validate(r)
 native(records,path/'readback-grading');assert h.transaction([],kp,intent['generator_id'])==[]
 c=counts(kp,b,path/'readback-inventory');result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'new_by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in LEVELS},'source_questions_preserved':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'additive_scoped_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c};save(path/'verification.json',result);return result

def finish(path,gid,verified,binary):
 inv=inventory(binary,path/'inventory-after.json');kp=read_kp(path/'latest',inv['basis']);c=counts(kp,inv['basis'],path/'latest-inventory');prep=json.loads((path/'preparation.json').read_text())
 result={'outcome':'finite-limit' if any(c['remaining_shortage'].values()) else 'generated','knowledgePoint':KP,'topic':TOPIC,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'verified_commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'new_by_level':verified['new_by_level'],'supported_levels':list(LEVELS),'observed_levels':['easy','moderate'],'authored_levels':['hard'],'unsupported_levels':[],'unsupported_levels_filled':False,'available_counts_before':prep['available_counts']['distinct_available'],'available_counts_after':c['distinct_available'],'remaining_shortage':c['remaining_shortage'],'capability_exceptions':prep['capability_exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source_questions_and_learner_history_preserved':True,'evidence':[str(p.relative_to(ROOT)) for p in [HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'validation.json',HERE/'registration.json',OUT/'native-build.json',OUT/'current-engine-replay.json',path/'generated.json',path/'generated.md',path/'preparation.json',path/'native-report.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json',path/'latest-inventory/validated-counts.json'] if p.exists()],'note':'Existing validated generator reused; hard is an explicitly authored canonical mixed-function workload. Malformed and unrated source questions remain unchanged and excluded. Only distinct exact mathematical tasks counted. Exact basis-guarded request and receipt verified under application api.lock.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
 assert json.loads((HERE/'validation.json').read_text())['status']=='pass';assert json.loads((HERE/'validation.json').read_text())['generator_sha256']==sha(HERE.with_suffix('.py'))
 build_native();subprocess.run([str(ENGINE),str(HERE/'engine-input.json'),str(OUT/'current-engine-replay.json')],check=True)
 binary=build_learning(ROOT.parent/'EDB');preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Acquired application api.lock',flush=True)
  for path in sorted(OUT.glob('basis-*')):
   if not (path/'commit-intent.json').exists():continue
   intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint and intent['sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text();assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
   finish(path,intent['generator_id'],verify(path,intent,DB._commit(intent,path/'transaction.edn',path)),binary);return
  inv=inventory(binary,OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b;path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID;(path/'before.edn').write_text(dumps(kp)+'\n')
  current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
  for old in S['record'][':knowledge-point/questions']:assert h.source_shape(legacy_matrix(current[old[':db/id']]),old)==h.canonical(old),'Source changed beyond equivalent matrix notation; reclassification required'
  save(path/'source-delta.json',{'historical_basis':S['basis'],'current_basis':b,'current_source_read':'before.edn','only_difference':'q-128458 column vectors use bmatrix instead of bracketed aligned; exact recursive source comparison passes after bounded notation normalization','mathematical_source_facts_preserved':True})
  assert h.source_shape(kp[':knowledge-point/canonical-example'],S['record'][':knowledge-point/canonical-example'])==h.canonical(S['record'][':knowledge-point/canonical-example'])
  contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
  gen=kp.get(':knowledge-point/question-generator');byscript=DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-script',b);assert len(byscript)<=1
  registration=HERE/'registration.json';saved=json.loads(registration.read_text())['id'] if registration.exists() else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'));gid=str(gen[':question-generator/id']) if gen else str(byscript[0][1]) if byscript else saved
  matched=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-id',b);assert not matched or len(matched)==1 and matched[0][0][':question-generator/script']==SCRIPT
  save(registration,{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or byscript or registration.exists()),'generator_sha256':sha(HERE.with_suffix('.py'))})
  c=counts(kp,b,path/'current-inventory');needed=c['remaining_shortage'];print(json.dumps({'basis':b,'validated_available':c['distinct_available'],'needed':needed}),flush=True)
  known=retained();used=set()
  for q in kp[':knowledge-point/questions']:
   name=q.get(':question/math-academy-id') or known[str(q[':question/id'])]['generation']['template'];used.add(fingerprint(q,name))
  used.add(fingerprint(kp[':knowledge-point/canonical-example'],'canonical-mixed'))
  for sid,level in g.TEMPLATES.items():
   if sid in g.DATA:used.add(fingerprint(g.generate(level,template=sid,parameters={'scales':[1,1,1]},profile=sid)['question'],sid))
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied;instances=[instances] if isinstance(instances,dict) else instances
  records=[];checked=[];added={l:0 for l in LEVELS};attempts={l:0 for l in LEVELS}
  def consider(r):
   key=validate(r);checked.append(r);level=r['question'][':question/difficulty'].split('/')[-1];attempts[level]+=1
   if added[level]<needed[level] and key not in used:used.add(key);records.append(r);added[level]+=1
  for r in instances:consider(r)
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError') if isinstance(supplied,dict) else None})
  previews=json.loads(subprocess.run([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--count','5','--seed',str(int(JOB.name[:8],16)),'--format','json'],text=True,capture_output=True,check=True,timeout=55).stdout)
  for r in previews:consider(r)
  for level in LEVELS:
   for i in range(256):
    if added[level]>=needed[level]:break
    consider(g.generate(level,seed=int(JOB.name[:8],16)+5+i))
  exceptions=[{'level':l,'requested':needed[l],'produced':added[l],'remaining':needed[l]-added[l],'filled':False,'reason':'Bounded 261 seeded candidates exhausted; documented bounded domain only, not proof of global exhaustion.'} for l in LEVELS if added[l]<needed[l]]
  ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]];assert len(ids)==len(set(ids))
  if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identities',b),'Existing identity collision requires reconciliation'
  save(path/'generated.json',records);save(path/'validated-previews.json',previews);(path/'generated.md').write_text('\n\n---\n\n'.join(map(g.markdown,records))+'\n');native(checked,path)
  save(path/'preparation.json',{'basis':b,'original_job_basis':1831,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'sampling_attempts':attempts,'capability_exceptions':exceptions,'assets':[],'generator_sha256':sha(HERE.with_suffix('.py')),'all_selected_instances_mathematically_validated':True,'all_selected_instances_actual_grader_validated':True,'source_basis':S['basis'],'source_evidence_unchanged':True})
  forms=h.transaction(records,kp,gid)
  if not forms:
   verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'new_by_level':added,'available_counts_after':c};save(path/'verification.json',verified);finish(path,gid,verified,binary);return
  txpath=path/'transaction.edn';txpath.write_text(dumps(forms)+'\n');r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;h.check_report(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'vector-sum-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':txpath.read_text(),'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)};save(path/'commit-intent.json',intent)
  finish(path,gid,verify(path,intent,DB._commit(intent,txpath,path)),binary)
if __name__=='__main__':main()
