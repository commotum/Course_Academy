"""KP-scoped, additive, serialized durable replenishment and exact receipt recovery."""
import fcntl,hashlib,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
H=Path(__file__).resolve().parent;ROOT=H.parents[2];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from capture.scripts.database.preview import preview_executable
from db_support import DB,KP,PATTERN,dumps,loads,kw
import validate as v
g=v.g
from inventory_jobs import save
from serve_graph_explorer import build_learning,database_environment
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';SOURCE=':application/ca-engine'
SCRIPT=str(H.with_suffix('.py').relative_to(ROOT));LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'4b43b94d0a1e03c0eb4089f0c6a6881bf04fcd6762b6649fef63f220244b2fca'
OUT=H/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):
 if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
 if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
 return str(x) if isinstance(x,uuid.UUID) else x

def inventory(native,path):
 r=subprocess.run([str(native),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE
 save(path,x['data']);return x['data']
def read(path,b):return DB.query('[:find (pull ?k '+PATTERN+') :in $ ?k :where [?k :knowledge-point/id _]]',[KP],path,'kp',b)[0][0]
def counts(kp,path,b):
 shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',b,history=True)}
 reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',b)}
 blocked={v.fingerprint(q) for q in kp[':knowledge-point/questions'] if q[':db/id'] in shown|reserved}
 blocked.add(v.fingerprint(kp[':knowledge-point/canonical-example']))
 avail={'moderate':set(),'hard':set()};bad=[];engine=[]
 for q in kp[':knowledge-point/questions']:
  level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
  if level not in avail or q[':db/id'] in shown|reserved:continue
  try:
   nq=v.normalized(q);v.check_question(nq);key=v.fingerprint(q)
   # Source notation/choice IDs are checked through the actual learner grader too.
   r={'knowledge_point':{'title':kp[':knowledge-point/title']},'question':nq,'generation':{'template':'existing-source'}}
   engine.append(v.engine_item(str(q[':question/id']),r))
   if key not in blocked:avail[level].add(key)
  except (AssertionError,ValueError,TypeError,KeyError) as e:bad.append({'id':str(q[':question/id']),'reason':str(e)})
 save(path/'existing-grading-input.json',engine)
 subprocess.run([str(H/'check-engine'),str(path/'existing-grading-input.json'),str(path/'existing-grading-report.json')],check=True)
 # Assign a task appearing in multiple bands to moderate, retaining source facts.
 overlap=avail['moderate']&avail['hard'];avail['hard']-=overlap
 result={'basis':b,'available':{k:len(z) for k,z in avail.items()},'excluded_cross_band_duplicate_tasks':sorted(overlap),'shown_or_reserved':sorted(shown|reserved),'invalid_or_incomplete':bad}
 save(path/'available-counts.json',result);return result

def transaction(records,kp):
 forms=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:assert str(gen[':question-generator/id'])==g.GENERATOR_ID and gen[':question-generator/script']==SCRIPT
 else:forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(g.GENERATOR_ID),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def datoms(report,path,source):
 attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':answer/id',':answer/type',':answer/value',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':question-generator/id',':question-generator/script'}
 for e,a,value,t,s,added in report[':edb/tx-data']:
  assert added and s==source,'Unexpected retraction or source'
  name=attrs[a]
  if e==KP:assert name in {':knowledge-point/questions',':knowledge-point/question-generator'}
  elif name!=':db/txInstant':assert e in new and name in allowed,'Out-of-scope datom'

def verify(report,path,intent):
 assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
 b=report[':edb/db-after-t'];datoms(report,path/'datom-verification',intent['source_eid'])
 before=loads((path/'before.edn').read_text());after=read(path/'readback',b)
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in after[':knowledge-point/questions']}
 assert all(canonical(q)==canonical(now[e]) for e,q in old.items())
 omit={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert canonical({k:z for k,z in before.items() if k not in omit})==canonical({k:z for k,z in after.items() if k not in omit})
 gen=after[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==g.GENERATOR_ID and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
 byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
  assert canonical(v.normalized(q))==canonical(r['question']);v.check(r)
 assert not transaction([],after)
 c=counts(after,path/'readback',b)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'available':c['available'],'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'no_retractions':True,'only_requested_kp_additive_content':True,'source':SOURCE,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
 save(path/'verification.json',result);return result

def finish(path,verified,inv):
 shortage={k:max(0,5-c) for k,c in verified['available'].items()}
 result={'outcome':'finite-limit' if any(shortage.values()) else 'generated','knowledgePoint':KP,'requested_stage':'classify','generator_path':SCRIPT,'generator_id':g.GENERATOR_ID,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':['moderate','hard'],'available_after':verified['available'],'shortage_remaining':shortage,'unsupported_levels':{'easy':{'status':'unsupported','rolling_target':5,'available_validated':0,'shortage_explicit':5,'evidence':'No easy source evidence; classification.md and capability.json'}},'unsupported_levels_filled':False,'capability':json.loads((H/'capability.json').read_text()),'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [H/'validation.json',H/'classification.md',H/'template-extraction.md',H/'bank-extraction.json',H/'capability.json',path/'preparation.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'verification.json',path/'inventory-after.json']],'note':'Existing distinct validated reserves meet supported quotas; generator registration resolves requested classification. No seed/bank/order-only duplicates inserted. Easy remains explicitly unsupported.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
 validation=json.loads((H/'validation.json').read_text());assert validation['passed'] and all(sha(ROOT/p)==s for p,s in validation['files'].items())
 native=build_learning(ROOT.parent/'EDB');preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(report,path,intent);finish(path,verified,inventory(native,path/'inventory-after.json'));return
  inv=inventory(native,OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b and LINEAGE in DB.command('status')
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read(path/'locked-source',b)
  assert str(kp[':knowledge-point/id'])==g.KP_UUID
  captured=loads((H/'source.edn').read_text());current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
  assert all(canonical(q)==canonical(current[q[':db/id']]) for q in captured[':knowledge-point/questions']),'Source evidence changed'
  assert canonical(captured[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
  (path/'before.edn').write_text(dumps(kp)+'\n')
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
  orphan=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(g.GENERATOR_ID)],path,'generator-identity',b)
  assert not orphan or len(orphan)==1 and orphan[0][0][':question-generator/script']==SCRIPT
  c=counts(kp,path,b);needed={k:max(0,5-z) for k,z in c['available'].items()}
  for job in inv['jobs']:
   if job['knowledgePoint']==KP and job['difficulty'] in needed:needed[job['difficulty']]=max(needed[job['difficulty']],job['missing'])
  supplied=json.loads(JOB.with_suffix('.generated').read_text()) if JOB.with_suffix('.generated').exists() else {}
  instances=supplied.get('instances',[])
  if isinstance(instances,dict):instances=[instances]
  for r in instances:v.check(r)
  used={v.fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(v.fingerprint(kp[':knowledge-point/canonical-example']))
  records=[];candidate_report=[]
  for level in ['moderate','hard']:
   # Execute the frozen script for finite candidates after the locked inventory recheck.
   cap=json.loads((H/'capability.json').read_text())['bounded_distinct_tasks'][level]
   command=[sys.executable,str(H.with_suffix('.py')),'--difficulty',level,'--count',str(cap),'--seed',str(int(JOB.name[:8],16)),'--format','json']
   proc=subprocess.run(command,capture_output=True,text=True,check=True);candidates=json.loads(proc.stdout)
   save(path/('generator-execution-'+level+'.json'),{'command':command,'instances':candidates})
   for r in instances+candidates:
    if r['question'][':question/difficulty']!=':question.difficulty/'+level:continue
    if needed[level]==0:break
    v.check(r);key=r['generation']['mathematical_key']
    if key not in used:records.append(r);used.add(key);needed[level]-=1
   candidate_report.append({'level':level,'generator_distinct_capability':cap,'remaining':needed[level]})
  for kind,ids in [('question',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
   assert len(ids)==len(set(ids))
   if ids:assert not DB.query('[:find ?e :in $ [?id ...] :where [?e :'+kind+'/id ?id]]',[ids],path,'identity-'+kind,b)
  save(path/'generated.json',records);save(path/'grading-input.json',[v.engine_item(str(i),r) for i,r in enumerate(records)])
  subprocess.run([str(H/'check-engine'),str(path/'grading-input.json'),str(path/'grading-report.json')],check=True)
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_evidence_unchanged':True,'available_before':c,'needed':needed,'new_questions':len(records),'candidate_capabilities':candidate_report,'supplied_generated_file_exists':JOB.with_suffix('.generated').exists(),'supplied_instances_validated':len(instances),'generator_version':g.VERSION,'generator_sha256':sha(H.with_suffix('.py')),'asset_hashes':[],'validation_sha256':sha(H/'validation.json')})
  forms=transaction(records,kp)
  if not forms:finish(path,{'basis_after':b,'new_questions':0,'available':c['available']},inv);return
  txpath=path/'transaction.edn';exact=dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(exact);f.flush();os.fsync(f.fileno())
  pr=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  (path/'preview.edn').write_text(pr.stdout);report=loads(pr.stdout);assert report[':edb/committed'] is False and report[':edb/db-before-t']==b
  datoms(report,path/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','lineage':LINEAGE,'endpoint':DB.args.endpoint,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'sha256':sha(txpath),'exact_edn':exact,'request_key':'inverse-secant-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'generator_id':g.GENERATOR_ID,'generator_path':SCRIPT,'generator_sha256':sha(H.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()}
  save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(report,path,intent);finish(path,verified,inventory(native,path/'inventory-after.json'))
if __name__=='__main__':main()
