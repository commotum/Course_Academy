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
spec=importlib.util.spec_from_file_location('normal_validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP;LEVELS=('easy','moderate','hard');LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.CAP['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'afe18ff2cc03b33d5771d21ccc945a4f6c42410f493b90aa39d4f602c5866cfd'
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

def role(q):
 text=q[':question/problem']
 return 'x_intercept' if 'crosses the $x$-axis' in text else 'y_intercept' if 'crosses the $y$-axis' in text else 'normal'

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()

def task(q):
 z=v.read_prompt(q[':question/problem'].replace(r'\dfrac',r'\frac'))
 if z['xt'].is_polynomial(v.T) and z['yt'].is_polynomial(v.T):
  implicit=s.Poly(s.resultant(v.X-z['xt'],v.Y-z['yt'],v.T),v.X,v.Y).monic().as_expr()
  return digest([s.srepr(implicit),s.srepr(z['xp']),s.srepr(z['yp']),role(q)])
 return digest([s.srepr(s.simplify(z[k])) for k in ('xt','yt','u')]+[role(q)])

def fixtures(r):
 item=v.engine_item(r['question'][':question/id'],r)
 assert item is not None,'Every field must have a key'
 for check in item['checks']:
  if 'equivalent coordinate' in check['purpose']:
   check['expected']='accepted'
   check['purpose']='independently unreduced equivalent entry; current learner grader'
 return item

def native(records,p):
 p.mkdir(parents=True,exist_ok=True);save(p/'input.json',[fixtures(r) for r in records])
 result=subprocess.run([str(GRADER),str(p/'input.json'),str(p/'report.json')],capture_output=True,text=True,timeout=55)
 (p/'run.log').write_text(result.stdout+result.stderr)
 if result.returncode:raise ValueError('Actual learner grading failed: '+result.stderr.strip())
 return json.loads((p/'report.json').read_text())

def source_check(q):
 """Read the actual prompt, complete bank and every displayed solution chain."""
 z=v.read_prompt(q[':question/problem']);solution=q[':question/worked-solution'];v.formatting(solution)
 request=role(q);rhs=s.expand(z['mn']*(v.X-z['xp'])+z['yp'])
 for f in q[':question/answer-fields']:
  values=[];flags=[];ci=f[':answer-field/correct'][1]
  for a in f[':answer-field/choices']:
   val=a[':answer/value']
   if f[':answer-field/type'].endswith('/radio'):
    obj=v.relation(val) if request=='normal' else v.pair(val)
    eq=v.line_eq(obj,z['line']) if request=='normal' else all(v.same(a,b) for a,b in zip(obj,(0,z['yi']) if request=='y_intercept' else (z['xi'],0)))
   else:
    obj=v.math(val);correct=rhs if request=='normal' else (z['xi'] if request=='x_intercept' else 0) if f[':answer-field/key']=='field-1' else (0 if request=='x_intercept' else z['yi']);eq=v.same(obj,correct)
   flags.append(eq);assert eq==(a[':answer/id']==ci),'Source answer designation differs from independent mathematics';values.append(obj)
  assert sum(flags)==1,'Missing or multiple correct values'
  for i,a in enumerate(values):
   for b in values[:i]:assert not (all(v.same(x,y) for x,y in zip(a,b)) if isinstance(a,tuple) else v.line_eq(a,b) if request=='normal' and f[':answer-field/type'].endswith('/radio') else v.same(a,b)),'Equivalent duplicate choices'
 blocks=v.blocks(solution);derivatives=next(b for b in blocks if '{x}^{′}(t)=' in b or "x'(t)=" in b)
 parts=re.split(r',\\(?:,|quad|qquad)\s*',derivatives);assert len(parts)==2
 for part,key in zip(parts,['dx','dy']):assert v.same(v.math(part.split('=',1)[1]),z[key]),'Printed derivative wrong'
 groups=[b.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0] for b in blocks if r'\begin{aligned}' in b];checked=0
 for i,body in enumerate(groups):
  rows=body.split(r'\\')
  if i==0:
   for row,key in zip(rows,['xp','yp']):
    for fragment in row.replace('&','').split('=')[1:]:assert v.same(v.math(fragment),z[key]),'Coordinate chain wrong';checked+=1
  elif r'\frac{dy}{dx} &' in body:
   for row in rows[1:]:
    for fragment in row.replace('&','').split('=')[1:]:assert v.same(v.math(fragment),z['dy']/z['dx']),'Derivative ratio wrong';checked+=1
  elif body.lstrip().startswith('m'):
   for row in rows:
    for fragment in row.split('&',1)[-1].split('=')[1:]:
     if '|' not in fragment:assert v.same(v.math(fragment),z['m']),'Slope chain wrong';checked+=1
  else:
   for row in rows:
    eq=v.relation(row.replace('&',''));assert v.line_eq(eq,z['line']) or (request!='normal' and v.line_eq(eq,v.Y-z['yi'] if request=='y_intercept' else v.X-z['xi'])),'Line/intercept chain wrong';checked+=1
 normal=next(b for b in blocks if ('{m}_{n}' in b or 'm_n =' in b) and '=' in b)
 assert r'-\frac{1}{m}' in normal
 for fragment in normal.split('=')[2:]:assert v.same(v.math(fragment),z['mn'])
 return {'x':str(z['xt']),'y':str(z['yt']),'parameter':str(z['u']),'point':[str(z['xp']),str(z['yp'])],'slope':str(z['m']),'y_intercept':str(z['yi']),'verified_solution_fragments':checked}

def record(q):
 return {'knowledge_point':{'db_id':KP,'id':g.SOURCE[':knowledge-point/id'],'title':g.SOURCE[':knowledge-point/title']},'question':normalize(q),'generation':{'template':'current-source','eligible_for_learning':True,'evidence_only':False}}

def validate(r):
 meta=r['generation'];q=r['question'];level=q[':question/difficulty'].split('/')[-1]
 assert r['knowledge_point']['db_id']==KP and meta['eligible_for_learning'] and not meta['evidence_only'] and level in LEVELS
 replay=g.generate(level,seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
 assert ordered(replay['question'])==ordered(q) and replay['generation']==meta,'Exact seeded generator replay failed'
 v.verify(r)
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
   sig=task(r['question']);levels[level].add(sig);validated.append(r)
  except (AssertionError,KeyError,ValueError,StopIteration) as e:excluded.append({'eid':q[':db/id'],'reason':str(e)})
 if validated:native(validated,p/'grading')
 result={'basis':b,'distinct_available':{l:len(xs) for l,xs in levels.items()},'validated_question_ids':[r['question'][':question/id'] for r in validated],'excluded':excluded,'unavailable_shown_or_reserved':sorted(unavailable),'deduplication':'polynomial implicit curve and assessed point, otherwise displayed coordinate functions and supplied parameter; normal/intercept role; seed, identity, reparametrization, difficulty, and bank order excluded'}
 save(p/'counts.json',result);return result

def source_refresh(kp,b,p):
 current={str(q[':db/id']):q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
 for old in g.QUESTIONS:
  eid=str(old[':db/id'])
  assert eid in current
  q=current[eid]
  for key in [':question/problem',':question/worked-solution',':question/math-academy-id']:
   assert q.get(key)==old.get(key),(eid,key,'source changed')
  assert q.get(':question/difficulty',{}).get(':db/ident')==old.get(':question/difficulty',{}).get(':db/ident')
  if ':question/difficulty' in old and all(':answer-field/correct' in f for f in old[':question/answer-fields']):assert normalize(q)==normalize(old)
 additions=[]
 for eid,q in current.items():
  if eid in {str(q[':db/id']) for q in g.QUESTIONS}:continue
  r=record(q);proof=source_check(r['question']);additions.append({'eid':int(eid),'math_academy_id':q[':question/math-academy-id'],'difficulty':r['question'][':question/difficulty'],'field_keys_and_types':[(f[':answer-field/key'],f[':answer-field/type']) for f in r['question'][':question/answer-fields']],'plot_rating':'none','mathematics':proof,'sampling':'newly observed template excluded from existing generator sampling; existing validated families are sufficient for all difficulty targets','question':r['question']})
 annotations=[{'eid':int(eid),'attribute':':question/requires-calculator','frozen':old.get(':question/requires-calculator'),'current':current[eid].get(':question/requires-calculator')} for old in g.QUESTIONS for eid in [str(old[':db/id'])] if old.get(':question/requires-calculator')!=current[eid].get(':question/requires-calculator')]
 save(p/'source-refresh.json',{'basis':b,'lineage':LINEAGE,'frozen_basis':g.CAP['basis'],'all_original_prompt_solution_banks_and_difficulty_unchanged':True,'preexisting_annotation_changes':annotations,'source_question_count':len(current),'new_sources':additions})
 return additions

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
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':[],'available_distinct':c['distinct_available'],'shortage_remaining':remaining,'source_questions_and_learner_history_preserved':True,'application_contributor':SOURCE,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'preview.edn',p/'commit.edn',p/'generated.json',p/'source-refresh.json',p/'inventory-after.json',p/'readback-grading/report.json',OUT/'prepared/validation.json',HERE/'validation.json',HERE/'reference/native/build.json',HERE/'classification-refresh.md'] if f.exists()]}
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
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.SOURCE[':knowledge-point/id']),'question-generator'))
  existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
  if existing:
   assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
  save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
  c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS};used={task(q) for q in kp[':knowledge-point/questions']};used.add(task(kp[':knowledge-point/canonical-example']));records=[]
  for r in json.loads((OUT/'prepared/generated.json').read_text()):
   level=r['question'][':question/difficulty'].split('/')[-1];sig=validate(r)
   if needed[level]>0 and sig not in used:records.append(r);needed[level]-=1;used.add(sig)
  assert not any(needed.values()),'Inventory changed: return to preparation before commit'
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
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'parametric-normal-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK)};save(p/'commit-intent.json',intent)
  verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))

if __name__=='__main__':
 if '--prepare' in sys.argv:prepare()
 elif '--commit' in sys.argv:commit()
 else:raise SystemExit('Use --prepare or --commit')
