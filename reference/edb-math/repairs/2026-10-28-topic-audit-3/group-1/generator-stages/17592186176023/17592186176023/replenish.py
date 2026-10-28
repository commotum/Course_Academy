"""Additive, exact-request inventory replenishment for this KP only."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database, QUESTION_PULL
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'c8a060783937bd539780dd6ab03e37fcdd20c635aae6e186e12024c20137a885'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
NATIVE=ROOT/'.local/graph-explorer/learning-6ff1a057dff4b9a2'
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
 (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
 (and [?l :learner/activity ?t] [?t :learner-task/status ?st]
 (or [?st :db/ident :learner-task.status/started] [?st :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(value):
 if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
 if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
 if isinstance(value,uuid.UUID):return str(value)
 return value
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
 obj=json.loads(r.stdout);assert obj['ok'] and obj['data']['lineage']==LINEAGE;save(path,obj['data']);return obj['data']
def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
SOURCE_PARAMETERS={name:g.anchor(name) for name in g.Q}
SOURCE_PARAMETERS.update({'q-126735':{'c':'8','s':'4','inner':'0','lo':'-1/2','hi':'0'},'q-126737':{'c':'4','s':'4','inner':'0','lo':'0','hi':'3/2'}})
EXCLUDED={'q-126736':'Worked solution changes the sign of Q in two integral rows.', 'q-126758':'Equivalent duplicate distractors and missing coefficient in worked solution.', 'q-125717':'sqrt(x) is not C1 on an open neighborhood of the stated boundary; source solution claims the usual Green theorem conditions.', 'q-126737':'sqrt(y^7+3) is nonreal at (0,-2) on the plotted boundary; worked integral also substitutes sqrt(x) for x^2.'}
CURRENT_SOURCE=OUT/'preflight/kp.edn'

def task_data(P,Q,p):
 # Nuisances, choice order, identities and difficulty labels do not create tasks.
 return g.digest([s.srepr(s.expand(P-P.subs(g.Y,0))),s.srepr(s.expand(Q-Q.subs(g.X,0))),*[str(s.sympify(p[k])) for k in ('s','inner','lo','hi')]])
def task(q):
 mid=q.get(':question/math-academy-id')
 if mid:
  P,Q=v.raw_prompt_components(q);p=g.exact(SOURCE_PARAMETERS[mid])
 else:
  P,Q=v.prompt_components(q)
  # Published paths are mapped back to immutable local geometry sidecars.
  prompt=q[':question/problem'];paths=re.findall(r'!\[\]\((.*?)\)',prompt+'\n'+q[':question/worked-solution'])
  p=None
  for path0 in paths:
   path=Path(path0)
   if path.is_absolute() and path.with_suffix('.json').exists():p=json.loads(path.with_suffix('.json').read_text());break
   for side in (HERE/'plots').glob('*.json'):
    if sha(side.with_suffix('.png'))==Path(path0).stem:p=json.loads(side.read_text());break
   if p is not None:break
  assert p is not None,'Missing geometry evidence'
 return task_data(P,Q,p)

def source_record(q,kp):
 q=copy.deepcopy(q)
 q[':question/id']=str(q[':question/id']);q[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
 for f in q[':question/answer-fields']:
  f[':answer-field/id']=str(f[':answer-field/id']);f[':answer-field/type']=str(f[':answer-field/type'][':db/ident']);f[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
  for a in f[':answer-field/choices']:a[':answer/id']=str(a[':answer/id']);a[':answer/type']=str(a[':answer/type'][':db/ident'])
 return json.loads(json.dumps({'knowledge_point':{'db_id':KP,'id':str(kp[':knowledge-point/id']),'title':kp[':knowledge-point/title']},'question':q,'generation':{'template':q[':question/math-academy-id'],'evidence_only':True}},default=str))

def check_current_sources(kp,path):
 reports=[];engine=[]
 for q in kp[':knowledge-point/questions']:
  mid=q.get(':question/math-academy-id')
  if not mid:continue
  assert mid in SOURCE_PARAMETERS,'New source evidence requires reclassification'
  P,Q=v.raw_prompt_components(q);p=g.exact(SOURCE_PARAMETERS[mid]);F=s.simplify((s.diff(Q,g.X)-s.diff(P,g.Y)).subs({g.X:g.R*s.cos(g.T),g.Y:g.R*s.sin(g.T)})*g.R)
  formal=s.simplify(s.integrate(s.integrate(F,(g.R,p['inner'],s.sqrt(p['s']))),(g.T,s.pi*p['lo'],s.pi*p['hi'])))
  f=q[':question/answer-fields'][0];vals=[v.scalar(a[':answer/value']) for a in f[':answer-field/choices']]
  flags=[s.simplify(a-formal)==0 for a in vals];assert sum(flags)==1
  hit=next(a for a,yes in zip(f[':answer-field/choices'],flags) if yes);assert hit[':answer/id']==f[':answer-field/correct'][':answer/id']
  distinct=all(s.simplify(a-b)!=0 for i,a in enumerate(vals) for b in vals[i+1:]);assert distinct or mid=='q-126758'
  rec=source_record(q,kp);engine.append({'label':mid,'record':rec,'checks':native_checks(rec)})
  reports.append({'source':mid,'db_id':q[':db/id'],'difficulty':str(q[':question/difficulty'][':db/ident']),'fields':'one selection radio / five scalar math choices','complete_bank_replayed':5,'formal_curl_integral':str(formal),'unique_bank':distinct,'eligible_for_validated_inventory':mid not in EXCLUDED,'exclusion':EXCLUDED.get(mid),'prompt_and_solution_bytes_retained':True,'choice_values':[a[':answer/value'] for a in f[':answer-field/choices']]})
 save(path/'current-source-validation.json',{'basis':DB.basis(),'sources':reports,'complete_banks':'12/12','choice_values':'60/60','notes':'Formal integration for q126737 does not validate its nonreal boundary integral. No opaque historical bank is used for new learner output.'})
 save(path/'source-native-input.json',engine)
 subprocess.run([str(HERE/'reference/native/check-engine'),str(path/'source-native-input.json'),str(path/'source-native-report.json')],check=True)
 return reports
def native_checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'entire radio bank'} for a in f[':answer-field/choices']]
def count(kp,path,basis):
 unavailable={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'usage',basis)}
 rows={l:[] for l in LEVELS};excluded=[]
 for q in kp[':knowledge-point/questions']:
  mid=q.get(':question/math-academy-id')
  if q[':db/id'] in unavailable:continue
  if mid in EXCLUDED:excluded.append({'id':str(q[':question/id']),'reason':EXCLUDED[mid]});continue
  level=str(q[':question/difficulty'][':db/ident']).split('/')[-1];assert level in rows
  assert q[':question/worked-solution'];f=q[':question/answer-fields'][0];assert len(f[':answer-field/choices'])==5 and ':answer-field/correct' in f
  rows[level].append(q)
 result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({task(q) for q in qs}),'available_question_ids':[str(q[':question/id']) for q in qs]} for l,qs in rows.items()},'excluded_shown_or_reserved':sorted(unavailable),'excluded_invalid_or_duplicate_bank':excluded}
 save(path/'available-counts.json',result);return result

def transaction(records,kp,gid):
 forms=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if not gen:
  forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def check_report(report,path,source):
 attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,value,tx,src,added in report[':edb/tx-data']:
  assert src==source and added,'Unexpected source or retraction'
  name=attrs[a]
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected existing entity or attribute'
def normalize(q):
 q=copy.deepcopy(q)
 for key in list(q):
  if key==':db/id' or key.startswith(':knowledge-point/'):q.pop(key)
 q[':question/id']=str(q[':question/id']);q[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
 for f in q[':question/answer-fields']:
  f.pop(':db/id',None);f[':answer-field/id']=str(f[':answer-field/id']);f[':answer-field/type']=str(f[':answer-field/type'][':db/ident']);f[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
  for a in f[':answer-field/choices']:
   a.pop(':db/id',None);a[':answer/id']=str(a[':answer/id']);a[':answer/type']=str(a[':answer/type'][':db/ident'])
 return canonical(q)
def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_report(report,path/'receipt-check',intent['source_eid'])
 basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis);old=loads((path/'before.edn').read_text());byid={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(canonical(byid[q[':db/id']])==canonical(q) for q in old[':knowledge-point/questions'])
 assert canonical({k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})==canonical({k:v for k,v in old.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')})
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());questions={str(q[':question/id']):q for q in byid.values()};assert len(byid)==len(old[':knowledge-point/questions'])+len(records)
 for r in records:
  q=questions[r['question'][':question/id']];assert normalize(q)==canonical(r['question']);assert ':question/math-academy-id' not in q;v.normal_check(json.loads((path/'generated-local.json').read_text())[records.index(r)])
 assert not transaction([],kp,intent['generator_id'])
 counts=count(kp,path/'readback',basis)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old[':knowledge-point/questions']),'source_and_learner_history_preserved':True,'only_scoped_additive_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':counts}
 save(path/'verification.json',result);return result

def finish(path,gid,verified,inv):
 prep=json.loads((path/'preparation.json').read_text());counts=verified['available_counts_after'];remaining={l:max(0,5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'excluded_source_defects':EXCLUDED,'supported_levels':list(LEVELS),'available_counts_before':prep['available_counts'],'available_counts_after':counts,'shortage_remaining':remaining,'unsupported_levels_filled':False,'capability_exceptions':[{'template':'q-126737','status':'unsupported_source_template','reason':EXCLUDED['q-126737'],'difficulty_band_unsupported':False},{'template':'q-126735','status':'source_only','reason':'Fourth-quadrant coefficient8 source validated; frozen generator conservatively samples existing sector bounds with coefficient<=6.'}],'finite_variant_limits':json.loads((HERE/'finite-domain.json').read_text()),'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'native-report.json',path/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'validation-freeze.json',HERE/'current-classification.md',OUT/'visual-review.json',path/'current-source-validation.json',path/'asset-hashes.json'] if p.exists()]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def main():
 freeze=json.loads((HERE/'validation-freeze.json').read_text());assert freeze['status']=='passed'
 for name,digest in freeze['hashes'].items():assert sha(ROOT/name)==digest,'Validated inputs changed'
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    verified=verify(path,intent,DB._commit(intent,path/'transaction.edn',path));finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis;path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True)
  kp=read_kp(path,basis);(path/'before.edn').write_text(dumps(kp)+'\n')
  frozen=loads(CURRENT_SOURCE.read_text())[0][0]
  assert canonical(kp)==canonical(frozen),'Scoped sources changed since preflight; reclassify'
  check_current_sources(kp,path)
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');existing=DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-identity',basis)
  gid=str(gen[':question-generator/id']) if gen else str(existing[0][1]) if existing else str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'question-generator'))
  assert len(existing)<=1
  if not gen and existing:raise ValueError('Existing unattached generator identity requires explicit reconciliation')
  counts=count(kp,path,basis);needed={l:max(0,5-counts['levels'][l]['distinct_available_tasks']) for l in LEVELS};used={task(q) for q in kp[':knowledge-point/questions']}
  # Canonical upper semicircle, quadratic radial curl3, radius2.
  used.add(task_data(-g.Y**3,g.X**3,{'s':'4','inner':'0','lo':'0','hi':'1'}))
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
  for r in instances:v.normal_check(r);assert r['generation']['eligible_for_learning'] and r['knowledge_point']['db_id']==KP
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
  records=[];added={l:0 for l in LEVELS}
  def consider(r):
   l=r['question'][':question/difficulty'].split('/')[-1];fp=task(r['question'])
   if added[l]<needed[l] and fp not in used:
    v.normal_check(r);records.append(r);used.add(fp);added[l]+=1
  for r in instances:consider(r)
  for l in LEVELS:
   for offset in range(1000):
    if added[l]>=needed[l]:break
    consider(g.generate(l,seed=int(JOB.name[:8],16)+offset))
  if any(added[l]<needed[l] for l in LEVELS):
   save(path/'capability-exception.json',{'bounded_attempts_per_level':1000,'needed':needed,'produced':added,'remaining':{l:needed[l]-added[l] for l in LEVELS},'finite_domain':json.loads((HERE/'finite-domain.json').read_text())})
  from image_library import ImageLibrary
  library=ImageLibrary();local_records=copy.deepcopy(records);asset_hashes=[]
  for rec in records:
   for key in (':question/problem',':question/worked-solution'):
    for source_path in re.findall(r'!\[\]\((.*?)\)',rec['question'][key]):
     source_path=Path(source_path);digest=sha(source_path);rel=library.put_file(source_path,expected_sha256=digest)
     assert sha(library.math_root/rel)==digest
     asset_hashes.append({'local_path':str(source_path),'reference':rel,'sha256':digest,'verified_available':True})
     rec['question'][key]=rec['question'][key].replace(str(source_path),rel)
  save(path/'generated-local.json',local_records);save(path/'asset-hashes.json',asset_hashes)
  ids=[uuid.UUID(i) for r in records for i in [r['question'][':question/id'],r['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]]
  matches=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else [];assert not matches,'Identity collision requires reconciliation'
  save(path/'generated.json',records);save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':native_checks(r)} for r in records])
  subprocess.run([str(HERE/'reference/native/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
  save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':counts,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({task(r['question']) for r in records}),'asset_hashes':asset_hashes,'source_basis':g.SOURCE['basis'],'source_evidence_unchanged':True,'generator_id':gid,'generator_path':SCRIPT})
  if '--prepare-only' in sys.argv:
   print(json.dumps({'prepared_basis':basis,'new_by_level':added,'records':len(records)}),flush=True);return
  review=json.loads((OUT/'visual-review.json').read_text());assert review['passed']
  assert set(r['question'][':question/id'] for r in records)<=set(review['reviewed_question_ids']),'New instances require visual review'
  assert set(a['sha256'] for a in asset_hashes)<=set(review['reviewed_asset_hashes']),'New assets require visual review'
  forms=transaction(records,kp,gid)
  if not forms:
   verified={'passed':True,'basis_after':basis,'new_questions':0,'available_counts_after':counts};save(path/'verification.json',verified);finish(path,gid,verified,inv);return
  txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  preview_result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
  (path/'preview.edn').write_text(preview_result.stdout);pr=loads(preview_result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'green-polar-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent);verified=verify(path,intent,DB._commit(intent,txpath,path));finish(path,gid,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
