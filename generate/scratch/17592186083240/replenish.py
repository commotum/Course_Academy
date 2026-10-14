"""KP-scoped additive inventory replenishment using the configured EDB integration."""
import copy,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import database_environment
from inventory_jobs import save
sys.path.insert(0,str(ROOT));from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from database import Database,QUESTION_PULL
from edn import dumps,loads,kw
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load(HERE.with_suffix('.py'),'parametric_generator')
qa=load(ROOT/'generate/runs/current/qa-parametric-derivative.py','independent_parametric_qa')
KP=17592186083240;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.RAW['lineage'];SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'10050d51eb09fa790401412e9c267c7c7ca9bcaed98699db69be91905baab74b'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
NATIVE=ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e';POOL=HERE/'reference/native/check-pool'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(p):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']
def read(p,b):return DB.query(QUERY,[KP],p,'kp',b)[0][0]
def normalize(q):
    return {':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':sorted([{':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])} for f in q[':question/answer-fields']],key=lambda f:f[':answer-field/key'])}

def ordered(q):
    q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    return q

def scoped(kp,b,seen):
    entities={};enums={}
    def enum(value):
        name=str(value[':db/ident']).lstrip(':')
        if name not in enums:
            e=len(enums)+1;enums[name]=e;entities[str(e)]={'db/ident':name}
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

def fp(q):
 x,y,domain=qa.curve(q[':question/problem']);m=re.search(r'where \$t=(.*?)\.\$',q[':question/problem']);point=qa.math(m[1]) if m else None
 level=str(q[':question/difficulty'][':db/ident']) if isinstance(q[':question/difficulty'],dict) else q[':question/difficulty']
 # Remove incidental whitespace/punctuation in a domain; retain interval/branch.
 domain=re.sub(r'\s+','',domain).rstrip(',')
 return g.mathematical_fingerprint(x,y,point,domain,level.split('/')[-1])

def fixtures(records):
 result=[]
 for rec in records:
  checks=[]
  for i,f in enumerate(rec['question'][':question/answer-fields']):
   correct=f[':answer-field/correct'][1]
   if f[':answer-field/type'].endswith('/radio'):
    checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'independently verified complete bank'} for a in f[':answer-field/choices'])
   else:
    value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
    checks.extend([{'field_index':i,'submitted':value,'expected':'accepted','purpose':'canonical exact answer'},{'field_index':i,'submitted':'('+value+')','expected':'accepted','purpose':'equivalent grouped exact expression through current learner grader'},{'field_index':i,'submitted':'('+value+')+1','expected':'rejected','purpose':'incorrect derivative'}])
  result.append({'label':rec['question'][':question/id'],'record':rec,'checks':checks})
 return result

def native(records,p):
 p.mkdir(parents=True,exist_ok=True);save(p/'input.json',fixtures(records))
 r=subprocess.run([str(HERE/'reference/native/check-engine'),str(p/'input.json'),str(p/'report.json')],text=True,capture_output=True,timeout=55)
 (p/'run.log').write_text(r.stdout+r.stderr)
 if r.returncode:raise RuntimeError(r.stderr)
 return json.loads((p/'report.json').read_text())

def local_record(rec):
 rec=copy.deepcopy(rec)
 for assetfile in OUT.glob('basis-*/asset-publication/assets.json'):
  asset=json.loads(assetfile.read_text());relative=asset['database_relative_path']
  if relative in rec['question'][':question/problem']:
   assert sha(Path('/media/jake/SSD/EDB/math')/relative)==asset['sha256'] and sha(Path(asset['local_path']))==asset['sha256']
   rec['question'][':question/problem']=rec['question'][':question/problem'].replace(relative,asset['local_path'])
 return rec

def validate(rec):
 rec=local_record(rec)
 meta=rec['generation'];q=rec['question'];l=q[':question/difficulty'].split('/')[-1]
 assert l in LEVELS and meta['eligible_for_learning'] and not meta['evidence_only']
 assert rec['knowledge_point']['db_id']==KP
 replay=g.generate(l,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
 assert ordered(replay['question'])==ordered(q) and replay['generation']==meta
 old=g.QUESTIONS.get(str(g.TEMPLATES[meta['template']].get('source_id')))
 qa.check(rec,old)
 return fp(q)

def source_record(q):
 r={'knowledge_point':{'db_id':KP,'id':g.KP[':knowledge-point/id'],'title':g.KP[':knowledge-point/title']},'question':normalize(q),'generation':{'template':'current-source'}}
 x,y,_=qa.curve(q[':question/problem']);point=re.search(r'where \$t=(.*?)\.\$',q[':question/problem']);answer=qa.s.simplify(qa.s.diff(y,qa.t)/qa.s.diff(x,qa.t))
 if point:answer=qa.s.simplify(answer.subs(qa.t,qa.math(point[1])))
 for f in r['question'][':question/answer-fields']:
  vals=[qa.math(a[':answer/value'].split('=',1)[-1]) for a in f[':answer-field/choices']]
  assert all(not qa.equal(a,b) for a,b in qa.itertools.combinations(vals,2))
  assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if qa.equal(v,answer)]==[f[':answer-field/correct'][1]]
 return r

def counts(kp,b,p):
 p.mkdir(parents=True,exist_ok=True)
 shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
 reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
 seen={x[0] for x in shown+reserved};save(p/'scoped.json',scoped(kp,b,seen))
 subprocess.run([str(POOL),str(p/'scoped.json'),str(p/'native-pool.json')],text=True,capture_output=True,check=True,timeout=55)
 pool=json.loads((p/'native-pool.json').read_text());ids={q for xs in pool['available_ids_by_level'].values() for q in xs}
 levels={l:set() for l in LEVELS};validated=[];excluded=[];known={r['question'][':question/id']:r for f in sorted(OUT.glob('basis-*/generated*.json'),key=lambda f:f.name=='generated-published.json') for r in json.loads(f.read_text())}
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] not in ids:continue
  try:
   if ':question/math-academy-id' in q:r=source_record(q)
   else:
    r=known[str(q[':question/id'])];assert ordered(local_record({'question':normalize(q)})['question'])==ordered(local_record(r)['question']);validate(r)
   native([r],p/('grading-'+str(q[':db/id'])))
   level=str(q[':question/difficulty'][':db/ident']).split('/')[-1];levels[level].add(fp(q));validated.append(str(q[':question/id']))
  except (AssertionError,RuntimeError,ValueError) as e:excluded.append({'question_id':str(q[':question/id']),'reason':str(e)})
 result={'basis':b,'distinct_available':{l:len(v) for l,v in levels.items()},'validated_question_ids':validated,'excluded':excluded,'shown_or_reserved':sorted(seen),'native_pool':pool,'deduplication':'normalized actual coordinate functions, relative amplitude, domain, supplied parameter and difficulty; seed, bank, common positive scaling and choice order excluded'}
 save(p/'counts.json',result);return result

if __name__=='__main__' and '--inspect' in sys.argv:
 inv=inventory(OUT/'inventory-before.json');b=inv['basis'];kp=read(OUT/'initial',b)
 c=counts(kp,b,OUT/'initial');print(json.dumps({'basis':b,'counts':c['distinct_available'],'excluded':c['excluded'],'remaining_jobs':[x for x in inv['jobs'] if x['knowledgePoint']==KP]},indent=2))

def source_refresh(kp,p):
 current={str(q[':db/id']):q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
 assert set(current)==set(g.QUESTIONS),'New source coverage requires reclassification'
 changes=[]
 for eid,old in g.QUESTIONS.items():
  q=current[eid]
  for key in [':question/problem',':question/worked-solution',':question/math-academy-id']:
   assert q[key]==old[key],(eid,key,'source mathematical content changed')
  assert q[':question/difficulty'][':db/ident']==old[':question/difficulty'][':db/ident']
  a=normalize(q);raw=copy.deepcopy(old);raw[':question/answer-fields']=[f for f in raw[':question/answer-fields'] if ':answer-field/correct' in f];b=normalize(raw)
  assert a==b,(eid,'source bank changed')
  if len(old[':question/answer-fields'])!=len(q[':question/answer-fields']):changes.append({'source':eid,'math_academy_id':q[':question/math-academy-id'],'change':'legacy duplicate field without correct reference removed before this replenishment; valid field unchanged','old_field_count':len(old[':question/answer-fields']),'current_field_count':len(q[':question/answer-fields'])})
 save(p/'source-refresh.json',{'basis':DB.basis(),'frozen_basis':g.RAW['basis'],'source_questions':18,'all_prompt_solution_difficulty_and_complete_valid_banks_unchanged':True,'legacy_repairs':changes,'current_complete_banks':18,'frozen_banks_retained_as_evidence':19})

def select(kp,needed,p):
 used=set()
 for q in kp[':knowledge-point/questions']:
  try:used.add(fp(q))
  except (AssertionError,ValueError):pass
 # Canonical circle has no compatible source formatting; its normalized method
 # has unit-amplitude cos/sin coordinates, unlike authored hard rule pairs.
 try:used.add(fp(kp[':knowledge-point/canonical-example']))
 except (AssertionError,ValueError):pass
 supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};supplied_rows=supplied.get('instances',[])
 if isinstance(supplied_rows,dict):supplied_rows=[supplied_rows]
 for r in supplied_rows:validate(r)
 save(p/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(supplied_rows),'generator_error':supplied.get('generatorError')})
 selected=[];new={l:0 for l in LEVELS};rejected=[]
 for l in LEVELS:
  if not needed[l]:continue
  run=subprocess.run([sys.executable,str(HERE.with_suffix('.py')),'--difficulty',l,'--count','30','--seed',str(int(JOB.name[:8],16)),'--format','json'],text=True,capture_output=True,check=True,timeout=55)
  candidates=supplied_rows+json.loads(run.stdout);save(p/('cli-'+l+'.json'),json.loads(run.stdout))
  # Both validated hard rule backbones must be demonstrated when available.
  if l=='hard':candidates.sort(key=lambda r:0 if r['generation']['template']=='product_pair' else 1)
  family_counts={}
  for r in candidates:
   if new[l]>=needed[l]:break
   if r['question'][':question/difficulty']!=':question.difficulty/'+l:continue
   f=r['generation']['template']
   if l=='hard' and family_counts.get(f,0)>=3:continue
   try:
    sig=validate(r)
    if sig in used:continue
    native([r],p/('candidate-grading-'+r['question'][':question/id']))
   except (AssertionError,RuntimeError,ValueError) as e:
    rejected.append({'level':l,'template':f,'parameters':r['generation']['parameters'],'reason':str(e)});continue
   used.add(sig);selected.append(r);new[l]+=1;family_counts[f]=family_counts.get(f,0)+1
 save(p/'rejected-candidates.json',rejected)
 ids=[uuid.UUID(uid) for r in selected for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
 if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',DB.basis())
 save(p/'generated.json',selected)
 (p/'generated.md').write_text('\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']+'\n\n'+json.dumps(r['question'][':question/answer-fields'],indent=2) for r in selected))
 native(selected,p/'selected-grading');save(p/'mathematics-validation.json',{'passed':True,'independent_coordinate_derivatives_solution_stages_and_complete_banks':qa.C,'distinct_new_mathematical_tasks':len(selected),'generator_replay_verified':True,'seed_option_order_and_common_scaling_ignored_for_deduplication':True})
 return selected,new

def verify(p,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,p/'receipt-check',intent['source_eid'])
 b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items()),'Preexisting question changed'
 ignored={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert {k:v for k,v in before.items() if k not in ignored}=={k:v for k,v in kp.items() if k not in ignored}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records)
 byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);validate(r)
 assert not transaction([],kp,intent['generator_id'])
 native(records,p/'readback-grading');after=counts(kp,b,p/'verified-inventory')
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'configured_application_contributor_verified':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':after}
 save(p/'verification.json',result);return result

def finish(p,gid,verified,inv):
 c=verified['available_counts_after'];remaining={l:max(0,5-c['distinct_available'][l]) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':[],'shortage_remaining':remaining,'available_distinct':c['distinct_available'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source_questions_and_learner_history_preserved':True,'application_contributor':SOURCE,'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'source-refresh.json',p/'generated.json',p/'mathematics-validation.json',p/'selected-grading/report.json',p/'inventory-after.json',HERE/'capabilities.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'reference/native/build.json'] if f.exists()]}
 save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','available_distinct','shortage_remaining')}),flush=True)

def main():
 v=json.loads((HERE/'validation.json').read_text());assert v['passed']
 assert all(sha(HERE.parent/f)==h for f,h in v['file_hashes'].items()),'Validated generator package changed'
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
  for p in sorted(OUT.glob('basis-*')):
   if not (p/'commit-intent.json').exists():continue
   intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
   assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
   verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b);source_refresh(kp,p)
  (p/'before.edn').write_text(dumps(kp)+'\n')
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'question-generator'))
  existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
  if existing:
   assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
  save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
  c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS};print(json.dumps({'basis':b,'available':c['distinct_available'],'missing':needed}),flush=True)
  records,new=select(kp,needed,p)
  save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'available_counts':c,'missing_by_level':needed,'new_by_level':new,'asset_hashes':[],'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True,'finite_shortages':{l:needed[l]-new[l] for l in LEVELS if needed[l]>new[l]}})
  forms=transaction(records,kp,gid)
  if not forms:
   verified={'passed':True,'basis_after':b,'new_questions':0,'available_counts_after':c};save(p/'verification.json',verified);finish(p,gid,verified,inv);return
  tx=dumps(forms)+'\n';txpath=p/'transaction.edn'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  assert DB.basis()==b,'Basis changed during preparation'
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,text=True,capture_output=True,timeout=55)
  (p/'preview.log').write_text(r.stderr)
  if r.returncode:raise RuntimeError(r.stderr)
  (p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'parametric-derivative-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(p/'commit-intent.json',intent)
  verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__' and '--inspect' not in sys.argv:
 if any(OUT.glob('basis-*/asset-publication/commit-intent.json')):
  subprocess.run([sys.executable,str(HERE/'finalize-publication.py')],check=True)
 else:main()
