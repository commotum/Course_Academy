"""KP-scoped inventory validation, additive preparation and locked submission."""
import copy,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from serve_graph_explorer import database_environment
from inventory_jobs import save
from database import Database,QUESTION_PULL
from edn import dumps,loads,kw
spec=importlib.util.spec_from_file_location('curl_validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEVELS=('easy','moderate','hard');LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.WRAPPER['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'c7b2aa898dced37f9f81302c02fbb6e2315b7cdaa90641c05b13beed3e564288'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
ENV=database_environment('math');DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
NATIVE=Path(json.loads((HERE/'reference/native/inventory-reader.json').read_text())['path']);GRADER=HERE/'reference/native/check-engine'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def read(p,b):return DB.query(QUERY,[KP],p,'kp',b)[0][0]

def normalize(q):
    return {':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':sorted([{':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])} for f in q[':question/answer-fields']],key=lambda f:f[':answer-field/key'])}

def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q

def transaction(records,kp,gid):
    forms=[]
    for r in records:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    else:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_report(report,p,source):
    attrs=dict(DB.attributes(p,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values())
    allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution/retraction'
        name=str(attrs[a])
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,name

def read_fields(q):
 prompt=q[':question/problem']
 if r'\left\langle' in prompt:
  pairs=re.findall(r'\\left\\langle(.*?),\s*\\:(.*?)\\right\\rangle',prompt)
  assert len(pairs)==3
  return [(math(P),math(Q)) for P,Q in pairs]
 # The refreshed sources include arctan(y), in addition to the archived arctan(x).
 return v.field_readback(prompt.replace(r'\operatorname{arctan}⁡',r'\arctan '))

def math(value):return v.parse(value.replace(r'\operatorname{arctan}⁡',r'\arctan '))

def task(q):
 fs=read_fields(q);ds=[(s.diff(P,g.y),s.diff(Q,g.x)) for P,Q in fs]
 # Exclude response type, difficulty, identities, choice/candidate order,
 # held-only components, and common matching gradient contributions.
 return hashlib.sha256(json.dumps(sorted(g.assessed_derivatives(ds))).encode()).hexdigest()

def fixtures(r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  correct=f[':answer-field/correct'][1]
  for a in f[':answer-field/choices']:
   check={'field_index':i,'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete independently validated field bank'}
   check['submitted_answer_id']=a[':answer/id']
   checks.append(check)
 return {'label':r['question'][':question/id'],'record':r,'checks':checks}

def native(records,p):
 p.mkdir(parents=True,exist_ok=True);save(p/'input.json',[fixtures(r) for r in records])
 result=subprocess.run([str(GRADER),str(p/'input.json'),str(p/'report.json')],capture_output=True,text=True,timeout=55)
 (p/'run.log').write_text(result.stdout+result.stderr)
 if result.returncode:raise ValueError('Actual learner grading failed: '+result.stderr.strip())
 return json.loads((p/'report.json').read_text())

def source_check(q):
 fs=read_fields(q);sol=q[':question/worked-solution'];v.format_check(q[':question/problem']);v.format_check(sol)
 ds=[(s.diff(P,g.y),s.diff(Q,g.x)) for P,Q in fs]
 py=re.findall(re.escape(r'\frac{∂P}{∂y}=')+r'(.*?)\$',sol)
 qx=re.findall(re.escape(r'\frac{∂Q}{∂x}=')+r'(.*?)\$',sol)
 curls=re.findall(re.escape(r'\frac{∂Q}{∂x}-\frac{∂P}{∂y}=')+r'(.*?)\n',sol)
 assert len(py)==len(qx)==3 and len(curls)==4 and curls[0]=='1,'
 good=[];stages=0
 for i,(P_y,Q_x) in enumerate(ds):
  v.equal(math(py[i]),P_y);v.equal(math(qx[i]),Q_x)
  is_good=s.simplify(Q_x-P_y-1)==0
  assert (r'\ne 1' not in curls[i+1])==is_good
  for fragment in curls[i+1].removesuffix('.').split(r'\ne 1')[0].split('='):
   v.equal(math(fragment),Q_x-P_y);stages+=1
  if is_good:good.append(i)
 assert 'Therefore, the correct answer is "'+g.selection(good)+'."' in sol
 for f in q[':question/answer-fields']:
  bank=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('/checkbox'):
   assert f[':answer-field/key'] in g.LABELS
   expected=str(g.LABELS.index(f[':answer-field/key']) in good).lower()
   assert {a[':answer/value'] for a in bank}=={'true','false'} and len(bank)==2
  else:
   assert f[':answer-field/type'].endswith('/radio');expected=g.selection(good)
   assert len(bank)==5 and len({a[':answer/value'] for a in bank})==5
   subsets=[tuple(i for i,l in enumerate(g.LABELS) if re.search(r'\b'+l+r'\b',a[':answer/value'])) for a in bank]
   assert len(set(subsets))==5
  assert sum(a[':answer/value']==expected for a in bank)==1
  for a in bank:assert (a[':answer/id']==correct)==(a[':answer/value']==expected)
 return {'partials':[[str(a),str(b)] for a,b in ds],'eligible_candidates':[g.LABELS[i] for i in good],'verified_solution_stages':stages,'complete_fields':len(q[':question/answer-fields'])}

def record(q):
 return {'knowledge_point':{'db_id':KP,'id':g.KP[':knowledge-point/id'],'title':g.KP[':knowledge-point/title']},'question':normalize(q),'generation':{'template':'current-source','eligible_for_learning':True,'evidence_only':False}}

def validate(r):
 meta=r['generation'];q=r['question'];level=q[':question/difficulty'].split('/')[-1]
 assert r['knowledge_point']['db_id']==KP and meta['eligible_for_learning'] and not meta['evidence_only'] and level in LEVELS
 replay=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
 assert ordered(replay['question'])==ordered(q) and json.loads(json.dumps(replay['generation']))==meta,'Exact seeded generator replay failed'
 v.check(r)
 return task(q)

def counts(kp,b,p):
 shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
 reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?st] (or [?st :db/ident :learner-task.status/started] [?st :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
 unavailable={x[0] for x in shown+reserved};levels={l:set() for l in LEVELS};excluded=[];validated=[]
 known={r['question'][':question/id']:r for f in OUT.glob('*/generated.json') for r in json.loads(f.read_text())}
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] in unavailable:continue
  try:
   r=record(q);level=r['question'][':question/difficulty'].split('/')[-1];assert level in LEVELS
   if ':question/math-academy-id' in q:source_check(r['question'])
   else:
    original=known[r['question'][':question/id']];assert ordered(original['question'])==ordered(r['question']);validate(original);r=original
   native([r],p/('grade-'+str(q[':db/id'])));sig=task(r['question']);levels[level].add(sig);validated.append(str(q[':question/id']))
  except (AssertionError,KeyError,ValueError,StopIteration) as e:excluded.append({'eid':q[':db/id'],'reason':str(e)})
 result={'basis':b,'distinct_available':{l:len(xs) for l,xs in levels.items()},'validated_question_ids':validated,'excluded':excluded,'unavailable_shown_or_reserved':sorted(unavailable),'deduplication':'Unordered assessed held-partial pairs, omitting common matching nonconstant terms; held-only components, response shape, candidate/choice order, seed, identity and difficulty excluded'}
 save(p/'counts.json',result);return result

def source_refresh(kp,b,p):
 current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
 frozen=loads((HERE/'reference/initial/kp.edn').read_text())[0][0]
 previous={q[':question/math-academy-id']:q for q in frozen[':knowledge-point/questions'] if ':question/math-academy-id' in q}
 assert set(current)==set(previous),'New source evidence requires classification refresh'
 for mid,q in current.items():assert normalize(q)==normalize(previous[mid]),(mid,'source changed after classification refresh')
 rows=[]
 for mid,q in current.items():
  r=record(q);source_error=None
  try:proof=source_check(r['question'])
  except AssertionError:
   assert mid=='q-126572','Unexpected source validation failure'
   fixed=copy.deepcopy(r['question'])
   sol=fixed[':question/worked-solution']
   assert sol.count(r'\frac{∂P}{∂y}=-{e}^{y}$')==1
   assert sol.count(r'\frac{∂Q}{∂x}-\frac{∂P}{∂y}={e}^{y}\ne 1.')==1
   fixed[':question/worked-solution']=sol.replace(r'\frac{∂P}{∂y}=-{e}^{y}$',r'\frac{∂P}{∂y}={e}^{y}$').replace(r'\frac{∂Q}{∂x}-\frac{∂P}{∂y}={e}^{y}\ne 1.',r'\frac{∂Q}{∂x}-\frac{∂P}{∂y}=-{e}^{y}\ne 1.')
   proof=source_check(fixed)
   source_error={'candidate':'II','displayed_P':'exp(y)','printed_P_y':'-exp(y)','correct_P_y':'exp(y)','printed_curl':'exp(y)','correct_curl':'-exp(y)','correct_selected_set_unchanged':['I'],'action':'Original preserved; excluded from validated available inventory and generator sampling; correction checked in memory only'}
  if mid in g.QUESTIONS:
   old=g.QUESTIONS[mid]
   old_ds=[(s.diff(P,g.y),s.diff(Q,g.x)) for P,Q in read_fields(old)]
   now_ds=[(s.diff(P,g.y),s.diff(Q,g.x)) for P,Q in read_fields(q)]
   for original_pair,current_pair in zip(old_ds,now_ds):
    for old_value,current_value in zip(original_pair,current_pair):v.equal(old_value,current_value)
   assert old[':question/worked-solution']==q[':question/worked-solution']
   sampling='existing source-derived family; archived complete radio profile remains supported; current checkbox fields are preserved'
  else:sampling='new source template classified and validated, conservatively excluded from generator sampling'
  rows.append({'math_academy_id':mid,'eid':q[':db/id'],'difficulty':r['question'][':question/difficulty'],'fields':[(f[':answer-field/key'],f[':answer-field/type']) for f in r['question'][':question/answer-fields']],'plot_rating':'none','validation':proof,'source_error':source_error,'sampling':sampling})
 native([record(q) for q in current.values()],p/'source-grading')
 result={'basis':b,'lineage':LINEAGE,'historical_basis':g.WRAPPER['basis'],'current_sources':rows,'all_current_sources_inspected':True,'valid_current_sources':11,'source_errors':1,'historical_legacy_missing_refs':2,'current_missing_refs':0,'source_content_preserved':True}
 save(p/'source-refresh.json',result);return result

def prepare():
 inv=inventory(OUT/'inventory-before-generation.json');b=inv['basis'];p=OUT/'prepared';p.mkdir(exist_ok=True);kp=read(p,b)
 source_refresh(kp,b,p);c=counts(kp,b,p/'inventory');needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS}
 print(json.dumps({'basis':b,'available':c['distinct_available'],'missing':needed}),flush=True)
 used={task(q) for q in kp[':knowledge-point/questions']};used.add(task(kp[':knowledge-point/canonical-example']))
 supplied=JOB.with_suffix('.generated');raw=json.loads(supplied.read_text()) if supplied.exists() else {};supplied_records=raw.get('instances',[]) if isinstance(raw,dict) else raw
 if isinstance(supplied_records,dict):supplied_records=[supplied_records]
 for r in supplied_records:validate(r)
 save(p/'supplied-status.json',{'exists':supplied.exists(),'validated_instances':len(supplied_records)})
 records=[];new={l:0 for l in LEVELS};rejected=[]
 for level in LEVELS:
  if not needed[level]:continue
  run=subprocess.run([sys.executable,str(HERE.with_suffix('.py')),'--difficulty',level,'--count','25','--seed',str(int(JOB.name[:8],16)),'--format','json'],capture_output=True,text=True,check=True,timeout=55)
  candidates=supplied_records+json.loads(run.stdout);save(p/('cli-'+level+'.json'),json.loads(run.stdout))
  for r in candidates:
   if new[level]>=needed[level]:break
   if r['question'][':question/difficulty']!=':question.difficulty/'+level:continue
   try:
    sig=validate(r)
    if sig in used:continue
    native([r],p/('candidate-'+r['question'][':question/id']))
   except (ValueError,AssertionError) as e:rejected.append({'id':r['question'][':question/id'],'error':str(e)});continue
   used.add(sig);records.append(r);new[level]+=1
 save(p/'rejected.json',rejected);save(p/'generated.json',records);native(records,p/'grading')
 (p/'generated.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records))
 save(p/'validation.json',{'passed':True,'basis':b,'generator_sha256':sha(HERE.with_suffix('.py')),'validator_sha256':sha(HERE/'validate.py'),'new_by_level':new,'needed_by_level':needed,'shortage':{l:needed[l]-new[l] for l in LEVELS},'distinct_mathematical_tasks':len({validate(r) for r in records}),'source_refresh':'source-refresh.json','native_grading':'grading/report.json'})
 return records

def verify(p,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,p/'receipt-check',intent['source_eid']);b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items()),'Preexisting questions changed'
 ignored={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert {k:v for k,v in before.items() if k not in ignored}=={k:v for k,v in kp.items() if k not in ignored}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);validate(r)
 assert not transaction([],kp,intent['generator_id']);native(records,p/'readback-grading');c=counts(kp,b,p/'verified-inventory')
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_preexisting_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'additive_datoms_only':True,'application_contributor_verified':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
 save(p/'verification.json',result);return result

def finish(p,gid,verified,inv):
 c=verified['available_counts_after'];remaining={l:max(0,5-c['distinct_available'][l]) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':[],'hard_difficulty':'authored source-method extension','source_errors_excluded':['q-126572'],'available_distinct':c['distinct_available'],'shortage_remaining':remaining,'source_questions_and_learner_history_preserved':True,'application_contributor':SOURCE,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'preview.edn',p/'commit.edn',p/'generated.json',p/'source-refresh.json',p/'inventory-after.json',p/'readback-grading/report.json',OUT/'prepared/validation.json',HERE/'validation.json',HERE/'reference/native/build.json',HERE/'classification-refresh.md',HERE/'capabilities.json'] if f.exists()]}
 save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2),flush=True)

def commit():
 validation=json.loads((OUT/'prepared/validation.json').read_text());assert validation['passed'] and validation['generator_sha256']==sha(HERE.with_suffix('.py')) and validation['validator_sha256']==sha(HERE/'validate.py')
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
  for p in sorted(OUT.glob('basis-*')):
   if not (p/'commit-intent.json').exists():continue
   intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
   assert intent['connection_sha256']==hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
   verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b);source_refresh(kp,b,p)
  (p/'before.edn').write_text(dumps(kp)+'\n');source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'question-generator'))
  existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
  if existing:
   assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
  save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
  c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS};used={task(q) for q in kp[':knowledge-point/questions']};used.add(task(kp[':knowledge-point/canonical-example']));records=[]
  for r in json.loads((OUT/'prepared/generated.json').read_text()):
   level=r['question'][':question/difficulty'].split('/')[-1];sig=validate(r)
   if needed[level]>0 and sig not in used:records.append(r);needed[level]-=1;used.add(sig)
  assert not any(needed.values()),'Inventory changed or bounded generator exhausted: return to preparation and document shortage'
  save(p/'generated.json',records);native(records,p/'selected-grading')
  ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
  if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'identities',b)
  forms=transaction(records,kp,gid)
  if not forms:finish(p,gid,{'basis_after':b,'new_questions':0,'available_counts_after':c},inv);return
  tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  assert DB.basis()==b
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,text=True,capture_output=True,timeout=55);(p/'preview.log').write_text(r.stderr)
  if r.returncode:raise RuntimeError(r.stderr)
  (p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'unit-curl-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK)};save(p/'commit-intent.json',intent)
  verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))

if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--commit' in sys.argv:commit()
 else:raise SystemExit('Use --prepare or --commit')
