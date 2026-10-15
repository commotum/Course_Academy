"""KP-scoped additive preparation and locked exact-request publication."""
from pathlib import Path
import fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database,QUESTION_PULL
from edn import dumps,loads,kw
from serve_graph_explorer import database_environment
sp=importlib.util.spec_from_file_location('gradient_validation',HERE/'validate.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);g=v.g
save=v.save;sha=v.sha;KP=g.KP;SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));SOURCE=':application/ca-engine';LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage']
LOCK=ROOT/'.local/learning/requests/math/api.lock';JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'b62a4105a918e78ec4822840a28f839568c7463993b56a60d78c3fdff7dfc16d';OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
ENV=database_environment('math');DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
NATIVE=Path(json.loads((HERE/'reference/native/inventory-reader.json').read_text())['path'])
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
def inventory(p):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=55);x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']
def read(p,b):return DB.query(QUERY,[KP],p,'kp',b)[0][0]
def refresh(kp,p):
 original=g.SOURCE['record'];old={q[':question/math-academy-id']:q for q in original[':knowledge-point/questions']};current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id'in q}
 assert old==json.loads(json.dumps(current,default=str)) and original[':knowledge-point/canonical-example']==json.loads(json.dumps(kp[':knowledge-point/canonical-example'],default=str)),'Source evidence changed: reclassify before publication'
 report,_=v.source_evidence(json.loads(json.dumps(kp,default=str)));save(p/'source-refresh.json',{'passed':True,'source_banks':report,'unchanged_source_questions':len(old)})
def counts(kp,b,p):
 shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
 tasks=DB.query('[:find (pull ?l [{[:learner/activity :limit nil] [:db/id {:learner-task/status [:db/ident]}]}]) :in $ ?learner :where [?l :learner/id ?learner]]',[LEARNER],p,'reservation-tasks',b)
 active=[a[':db/id'] for row in tasks for a in row[0].get(':learner/activity',[]) if a.get(':learner-task/status',{}).get(':db/ident') in (':learner-task.status/started',':learner-task.status/paused')]
 held=DB.query('[:find (pull ?t [{:learner-task/activity [{[:activity/steps :limit nil] [{:step/content [:db/id]}]}]}]) :in $ [?t ...] :where [?t :learner-task/status _]]',[active],p,'reserved',b) if active else []
 members={q[':db/id'] for q in kp[':knowledge-point/questions']}
 reserved=[[s[':step/content'][':db/id']] for row in held for s in row[0].get(':learner-task/activity',{}).get(':activity/steps',[]) if s.get(':step/content',{}).get(':db/id') in members]
 unavailable={r[0] for r in shown+reserved};used=set();available=[];excluded=[];records=[];known={r['question'][':question/id']:r for r in json.loads((HERE/'reference/all-validated.json').read_text())}
 for q in kp[':knowledge-point/questions']:
  name=q.get(':question/math-academy-id');reason=None
  if q[':db/id'] in unavailable:reason='previously presented or reserved'
  elif name in g.EXCLUDED:reason=g.EXCLUDED[name]
  elif name=='q-168602':reason='Standalone source lacks vector-field premise; new generated version supplies it'
  elif name in g.CASES:
   r={'knowledge_point':{'db_id':KP,'title':g.TITLE},'question':v.normalize(q),'generation':{'template':name}}
   P,Q=v.prompt(q[':question/problem']);v.check_bank(r['question'],P,Q)
  else:
   r=known.get(str(q[':question/id']));assert r is not None,'Unknown generated question: revalidate explicitly'
   assert v.ordered(v.normalize(q))==v.ordered(r['question']);v.check(r)
  if reason:excluded.append({'id':q[':db/id'],'source':name,'reason':reason});continue
  sig=v.task(r['question'])
  if sig in used:excluded.append({'id':q[':db/id'],'reason':'duplicate mathematical vector field'});continue
  used.add(sig);available.append(str(q[':question/id']));records.append(r)
 v.native(records,p/'grading')
 c={'basis':b,'distinct_available':{'easy':len(available),'moderate':0,'hard':0},'available_question_uuids':available,'excluded':excluded,'ever_shown':[r[0] for r in shown],'reserved':[r[0] for r in reserved],'canonical_excluded':True};save(p/'counts.json',c);return c

def forms(records,kp,gid):
 tx=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:tx.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   tx.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  tx.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:
  assert str(gen[':question-generator/id'])==gid
  if gen.get(':question-generator/script')!=SCRIPT:tx.append([kw('db/add'),gen[':db/id'],kw('question-generator/script'),SCRIPT])
 else:tx.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:tx.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if tx:tx.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return tx

def pick(kp,c,all_records):
 used=set()
 for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
  try:
   if q.get(':question/math-academy-id')=='q-168602':
    P,Q=v.prompt(q[':question/worked-solution']);used.add(g.digest([g.s.srepr(g.s.simplify(P)),g.s.srepr(g.s.simplify(Q))]))
   else:used.add(v.task(q))
  except (AssertionError,ValueError):pass # Missing standalone premise is recorded/excluded above.
 needed=max(0,5-c['distinct_available']['easy']);selected=[]
 if not needed:return [],0
 for r in all_records:
  sig=v.check(r)['task']
  if len(selected)<needed and sig not in used:selected.append(r);used.add(sig)
 return selected,needed-len(selected)
def prepare():
 inv=inventory(OUT/'inventory-before.json');b=inv['basis'];p=OUT/'prepared';p.mkdir(exist_ok=True);kp=read(p,b);refresh(kp,p);c=counts(kp,b,p/'current-inventory');all_records=json.loads((HERE/'reference/all-validated.json').read_text());selected,remaining=pick(kp,c,all_records)
 save(p/'generated.json',selected);save(p/'validation.json',{'passed':True,'basis':b,'lineage':LINEAGE,'counts':c,'new_questions':len(selected),'unfilled_easy':remaining,'generator_sha256':sha(HERE.with_suffix('.py')),'validator_sha256':sha(HERE/'validate.py'),'generated_sha256':sha(p/'generated.json')});print(json.dumps({'basis':b,'counts':c['distinct_available'],'new_questions':len(selected),'unfilled_easy':remaining}),flush=True)

def check_datoms(report,p,source):
 attrs=dict(DB.attributes(p,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values());allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,val,tx,src,added in report[':edb/tx-data']:
  assert src==source and added,'Unexpected attribution or retraction';name=str(attrs[a])
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,(e,name)

def verify(p,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_datoms(report,p/'receipt-check',intent['source_eid']);b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']};assert all(now[e]==q for e,q in old.items()),'Preexisting questions changed'
 ignored={':knowledge-point/questions',':knowledge-point/question-generator'};assert {k:v for k,v in before.items() if k not in ignored}=={k:v for k,v in kp.items() if k not in ignored}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 selected=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(selected);byid={str(q[':question/id']):q for q in now.values()}
 for r in selected:assert v.ordered(v.normalize(byid[r['question'][':question/id']]))==v.ordered(r['question']);v.check(r)
 assert forms([],kp,intent['generator_id'])==[];v.native(selected,p/'readback-grading');c=counts(kp,b,p/'verified-inventory')
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(selected),'unchanged_preexisting_questions':len(old),'canonical_example_unchanged':True,'source_questions_and_learner_history_preserved':True,'additive_datoms_only':True,'application_contributor_verified':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c};save(p/'verification.json',result);return result

def finish(p,intent,verified,inv):
 c=verified['available_counts_after'];cap=json.loads((HERE/'capabilities.json').read_text());result={'outcome':'generated' if c['distinct_available']['easy']>=5 else 'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'available_distinct':c['distinct_available'],'shortage_remaining':{'easy':max(0,5-c['distinct_available']['easy']),'moderate':5,'hard':5},'unsupported_levels_filled':False,'capability_exceptions':cap['exceptions'],'finite_variant_limit':cap['finite_variant_limit'],'source_questions_and_learner_history_preserved':True,'application_contributor':SOURCE,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(f.relative_to(ROOT)) for f in [HERE/'classification.md',HERE/'template-extraction.md',HERE/'capabilities.json',HERE/'validation.json',HERE/'review.md',HERE/'reference/exhaustive-grading/report.json',p/'commit-intent.json',p/'transaction.edn',p/'preview.edn',p/'commit.edn',p/'verification.json',p/'inventory-after.json',p/'verified-inventory/counts.json']], 'note':'Easy inventory has been independently validated; only any actual shortage was replenished. Moderate and hard remain explicitly unsupported. No question is counted merely because its seed or UUID differs.'};save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2),flush=True)

def commit():
 val=json.loads((HERE/'validation.json').read_text());assert val['passed'] and val['generator_sha256']==sha(HERE.with_suffix('.py')) and val['validator_sha256']==sha(HERE/'validate.py')
 prep=json.loads((OUT/'prepared/validation.json').read_text());assert prep['passed'] and prep['generator_sha256']==sha(HERE.with_suffix('.py')) and prep['generated_sha256']==sha(OUT/'prepared/generated.json')
 preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
  # Resolve original retained intent first; never assign another key to uncertain work.
  for p in sorted(OUT.glob('basis-*')):
   if not (p/'commit-intent.json').exists():continue
   intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text() and intent['connection_sha256']==hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
   report=DB._commit(intent,p/'transaction.edn',p);verified=verify(p,intent,report);finish(p,intent,verified,inventory(p/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b);refresh(kp,p);(p/'before.edn').write_text(dumps(kp)+'\n');source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
  existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
  if existing:assert len(existing)==1;gid=str(existing[0][0][':question-generator/id'])
  save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
  c=counts(kp,b,p/'current-inventory');all_records=json.loads((HERE/'reference/all-validated.json').read_text());selected,remaining=pick(kp,c,all_records);save(p/'generated.json',selected);v.native(selected,p/'selected-grading')
  ids=[uuid.UUID(uid) for r in selected for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
  if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'identities',b)
  tx=forms(selected,kp,gid);assert tx,'No changes; use retained verified outcome'
  txpath=p/'transaction.edn';text=dumps(tx)+'\n'
  with txpath.open('w') as stream:stream.write(text);stream.flush();os.fsync(stream.fileno())
  save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'new_questions':len(selected),'unfilled_easy':remaining,'counts':c,'generator_sha256':sha(HERE.with_suffix('.py')),'contributor':SOURCE,'assets':[],'lock':str(LOCK)})
  assert DB.basis()==b;r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,capture_output=True,text=True,timeout=55);(p/'preview.log').write_text(r.stderr);assert r.returncode==0,r.stderr;(p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_datoms(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'gradient-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':text,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in selected],'lock':str(LOCK)};save(p/'commit-intent.json',intent)
  with (p/'commit-intent.json').open('r') as stream:os.fsync(stream.fileno())
  verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,intent,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':
 if '--prepare'in sys.argv:prepare()
 elif '--commit'in sys.argv:commit()
 else:raise SystemExit('Use --prepare or --commit')
