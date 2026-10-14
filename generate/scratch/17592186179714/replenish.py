#!/usr/bin/env python3
"""Scoped additive EDB publication, locked from current inventory through readback."""
import copy,fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from serve_graph_explorer import database_environment
from inventory_jobs import save
from database import Database,QUESTION_PULL
from edn import dumps,loads,kw
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(D.with_suffix('.py'),'gradient');qa=load(D/'validate.py','gradient_qa')
KP=17592186179714;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';SOURCE=':application/ca-engine';LINEAGE=g.RAW['lineage'];LEVELS=('easy','moderate')
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'15797887233751629a8705b33a80e394587e1a0c93df4f4821e14069fbff98f5'
SCRIPT=str(D.with_suffix('.py').relative_to(ROOT));OUT=D/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
ENV=database_environment('math');DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
NATIVE=max((ROOT/'.local/graph-explorer').glob('learning-*'),key=lambda p:p.stat().st_mtime_ns)
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def plain(v):return json.loads(json.dumps(v,default=str))
def inventory(p):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']
def read(p,b):return DB.query(QUERY,[KP],p,'kp',b)[0][0]
def normalize(q):
 return {':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':sorted([{':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])} for f in q[':question/answer-fields']],key=lambda f:f[':answer-field/key'])}
def ordered(q):
 q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
 for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
 return q
def fp(q):
 f,vs=qa.prompt(q);level=q[':question/difficulty'];level=str(level[':db/ident']) if isinstance(level,dict) else level
 if f.func==qa.s.log:
  coeffs=qa.s.Poly(f.args[0],*vs).coeffs();div=qa.s.igcd(*coeffs);f=qa.s.log(qa.s.expand(f.args[0]/div))
 return g.digest({'function':qa.s.srepr(f),'variables':list(map(str,vs)),'level':level})
def scoped(kp,b,seen):
 entities={};enums={}
 def enum(v):
  name=str(v[':db/ident']).lstrip(':')
  if name not in enums:
   eid=len(enums)+1;enums[name]=eid;entities[str(eid)]={'db/ident':name}
  return enums[name]
 for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
  r={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[]};entities[str(q[':db/id'])]=r
  if ':question/difficulty' in q:r['question/difficulty']=enum(q[':question/difficulty'])
  for f in q.get(':question/answer-fields',[]):
   r['question/answer-fields'].append(f[':db/id']);field={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]};entities[str(f[':db/id'])]=field
   if ':answer-field/correct'in f:field['answer-field/correct']=f[':answer-field/correct'][':db/id']
   for a in f.get(':answer-field/choices',[]):entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
 entities[str(KP)]={'knowledge-point/id':str(kp[':knowledge-point/id']),'knowledge-point/title':kp[':knowledge-point/title'],'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
 return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}
def counts(kp,b,p):
 p.mkdir(parents=True,exist_ok=True)
 shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
 reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
 seen={r[0] for r in shown+reserved};save(p/'scoped.json',scoped(kp,b,seen))
 subprocess.run([str(D/'check-pool'),str(p/'scoped.json'),str(p/'native-pool.json')],check=True,text=True,capture_output=True,timeout=55)
 pool=json.loads((p/'native-pool.json').read_text());ids={q for xs in pool['available_ids_by_level'].values() for q in xs}
 known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
 excluded=[];records=[];levels={l:set() for l in LEVELS}
 for q in kp[':knowledge-point/questions']:
  mid=q.get(':question/math-academy-id')
  if mid=='q-122399' or mid=='q-122601':excluded.append({'source':mid,'reason':'incomplete/unrated' if mid=='q-122399' else 'inconsistent worked solution'});continue
  if q[':db/id'] not in ids:continue
  if mid:
   name=next(t for t,v in g.TEMPLATES.items() if v[1]==mid);r=g.replay(name)
   # Source banks and solutions were validated independently; require unchanged evidence.
   assert plain(q)==next(o for o in g.KP[':knowledge-point/questions'] if o[':question/math-academy-id']==mid)
   r['question']=normalize(q)
  else:
   r=known[str(q[':question/id'])];assert normalize(q)==ordered(r['question']);qa.check_record(r)
  records.append(r);l=str(q[':question/difficulty'][':db/ident']).split('/')[-1];levels[l].add(fp(q))
 qa.native(records,p/'grading')
 result={'basis':b,'distinct_available':{l:len(v) for l,v in levels.items()},'excluded':excluded,'shown_or_reserved':sorted(seen),'native_pool':pool,'valid_question_ids':[r['question'][':question/id'] for r in records],'deduplication':'normalized mathematical function; logarithm positive common coefficient scale, seed, UUID and choice order ignored'}
 save(p/'counts.json',result);return result
def transaction(records,kp,gid):
 forms=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 else:forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms
def check_report(report,p,source):
 attrs=dict(DB.attributes(p,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,v,t,contributor,added in report[':edb/tx-data']:
  assert contributor==source and added,'Unexpected attribution/retraction'
  name=str(attrs[a])
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,name
def select(kp,needed,p):
 used={fp(q) for q in kp[':knowledge-point/questions'] if ':question/difficulty' in q}
 rows=[];supplied=JOB.with_suffix('.generated')
 if supplied.exists():
  x=json.loads(supplied.read_text());rows=x.get('instances',[]);rows=[rows] if isinstance(rows,dict) else rows
  for r in rows:qa.check_record(r)
 save(p/'supplied-status.json',{'exists':supplied.exists(),'validated_instances':len(rows)})
 selected=[]
 for l in LEVELS:
  if needed[l]==0:continue
  run=subprocess.run([sys.executable,str(D.with_suffix('.py')),'--difficulty',l,'--seed',str(int(JOB.name[:8],16)),'--count','20','--format','json'],check=True,text=True,capture_output=True,timeout=55)
  candidates=json.loads(run.stdout);save(p/('cli-'+l+'.json'),candidates)
  n=0
  for r in rows+candidates:
   if n==needed[l]:break
   if r['question'][':question/difficulty']!=':question.difficulty/'+l:continue
   qa.check_record(r);sig=fp(r['question'])
   if sig in used:continue
   used.add(sig);selected.append(r);n+=1
 ids=[uuid.UUID(uid) for r in selected for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
 if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',DB.basis())
 save(p/'generated.json',selected);qa.native(selected,p/'selected-grading')
 save(p/'mathematics-validation.json',{'passed':True,'instances':[qa.check_record(r) for r in selected],'distinct_tasks':len(selected),'all_choices_and_solution_stages_checked':True})
 (p/'generated.md').write_text('\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']+'\n\n'+json.dumps(r['question'][':question/answer-fields'],indent=2) for r in selected))
 return selected
def verify(p,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,p/'receipt-check',intent['source_eid']);b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']};assert all(now[e]==q for e,q in old.items())
 ignored={':knowledge-point/questions',':knowledge-point/question-generator'};assert {k:v for k,v in before.items() if k not in ignored}=={k:v for k,v in kp.items() if k not in ignored}
 assert str(kp[':knowledge-point/question-generator'][':question-generator/id'])==intent['generator_id'];assert kp[':knowledge-point/question-generator'][':question-generator/script']==SCRIPT
 rows=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(rows);byid={str(q[':question/id']):q for q in now.values()}
 for r in rows:assert normalize(byid[r['question'][':question/id']])==ordered(r['question']);qa.check_record(r)
 qa.native(rows,p/'readback-grading');assert not transaction([],kp,intent['generator_id']);c=counts(kp,b,p/'verified-inventory')
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(rows),'preexisting_questions_unchanged':len(old),'canonical_example_unchanged':True,'learner_and_engine_history_unchanged':True,'only_scoped_additions':True,'configured_application_contributor_verified':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c};save(p/'verification.json',result);return result
def finish(p,gid,verified,inv):
 counts=verified['available_counts_after']['distinct_available'];remaining={l:max(0,5-counts[l]) for l in LEVELS};remaining['hard']=5
 result={'outcome':'finite-limit' if any(remaining[l] for l in LEVELS) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':{'hard':'No source-backed hard template; bounded capability exception in capabilities.json'},'shortage_remaining':remaining,'available_distinct':counts,'unsupported_levels_filled':False,'excluded_source_questions':['q-122399','q-122601'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'application_contributor':SOURCE,'source_questions_and_learner_history_preserved':True,'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'mathematics-validation.json',p/'selected-grading/report.json',p/'inventory-after.json',D/'capabilities.json',D/'classification.md',D/'template-extraction.md',D/'validation.json',D/'source-bank-replay.json'] if f.exists()]}
 save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2))
def main():
 validation=json.loads((D/'validation.json').read_text());assert validation['passed'];assert all(sha(ROOT/f)==h for f,h in validation['file_hashes'].items())
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
  for p in sorted(OUT.glob('basis-*')):
   if not (p/'commit-intent.json').exists():continue
   intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text();assert intent['connection_sha256']==hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
   verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b)
  for old in g.KP[':knowledge-point/questions']:assert plain(next(q for q in kp[':knowledge-point/questions'] if q[':db/id']==old[':db/id']))==old,'Source evidence changed'
  assert {str(q[':question/math-academy-id']) for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}==set(g.SOURCES),'New source evidence requires classification'
  (p/'before.edn').write_text(dumps(kp)+'\n');src=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(src)==1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(g.NS,'question-generator'))
  existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
  if existing:assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
  save(D/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
  c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS};print(json.dumps({'basis':b,'validated_available':c['distinct_available'],'missing_supported':needed}),flush=True)
  records=select(kp,needed,p);save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_version':g.VERSION,'generator_sha256':sha(D.with_suffix('.py')),'available_before':c,'missing_supported':needed,'new_questions':len(records),'assets':[],'validation_specs':['question/validate','answer-field/validate','answer/validate','knowledge-point/validate'],'source_unchanged':True})
  forms=transaction(records,kp,gid)
  if not forms:
   verified={'passed':True,'basis_after':b,'new_questions':0,'available_counts_after':c};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
  tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  assert DB.basis()==b,'Basis changed during preparation'
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,text=True,capture_output=True,timeout=55);(p/'preview.log').write_text(r.stderr)
  if r.returncode:raise RuntimeError(r.stderr)
  (p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',src[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':src[0][0],'basis':b,'expected_basis':b,'request_key':'gradient-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(D.with_suffix('.py')),'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(p/'commit-intent.json',intent)
  verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()
