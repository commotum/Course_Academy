"""KP-scoped additive replenishment, exact durable requests and verified readback."""
import copy,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));import validate as v;g=v.g
sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import database_environment,image_path
from inventory_jobs import save
sys.path.insert(0,str(ROOT));from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from database import Database,QUESTION_PULL
from edn import dumps,loads,kw
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
LEVELS=('easy','moderate','hard');SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'62b9e0c9acf705dfb1925f3a82c285ea8075494707f832359c88666877bd7c73'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
MATH=Path(DB.env['EDB_MATH_ROOT'])
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7';POOL=HERE/'reference/native/check-pool'
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

def signature(obj):
 if isinstance(obj,dict):return {k:signature(v) for k,v in obj.items() if k!=':db/id' and '/_' not in k}
 if isinstance(obj,(tuple,list,set)):return sorted((signature(x) for x in obj),key=lambda x:json.dumps(x,sort_keys=True))
 return str(obj) if isinstance(obj,uuid.UUID) else obj

def source_refresh(kp,p):
 old={q[':db/id']:q for q in g.KP[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
 changes=[]
 for e,q in old.items():
  oldq=copy.deepcopy(q);newq=copy.deepcopy(now[e])
  if oldq.get(':question/worked-solution')!=newq.get(':question/worked-solution'):
   def normalized_solution(text):
    text=re.sub(r'!\[\]\([^)]+\)', '[IMAGE]',text)
    text=text.replace(r'\left', '').replace(r'\right.', '').replace(r'\{','{').replace(r'\}','}').replace('&','')
    return re.sub(r'\s+','',text)
   assert normalized_solution(oldq[':question/worked-solution'])==normalized_solution(newq[':question/worked-solution']),(e,'solution mathematical content changed')
   changes.append({'source_id':e,'change':'preexisting coordinate system TeX repairs; xy2 additionally has two replaced diagram assets and visible set delimiters','old_solution_sha256':hashlib.sha256(q[':question/worked-solution'].encode()).hexdigest(),'current_solution_sha256':hashlib.sha256(now[e][':question/worked-solution'].encode()).hexdigest()})
   oldq.pop(':question/worked-solution');newq.pop(':question/worked-solution')
  assert g.presentation(oldq[':question/problem'])==g.presentation(newq[':question/problem']),(e,'prompt changed')
  oldq.pop(':question/problem');newq.pop(':question/problem')
  assert signature(oldq)==signature(newq),('Frozen source changed',e)
 save(p/'preexisting-source-repairs.json',changes)
 assert signature(g.KP[':knowledge-point/canonical-example'])==signature(kp[':knowledge-point/canonical-example'])
 extra=set(now)-set(old);assert extra=={17592186436974},'Unexpected new source evidence requires classification'
 save(p/'source-refresh.json',{'basis':DB.basis(),'frozen_basis':g.SOURCE['basis'],'unchanged_frozen_questions':len(old),'new_source_ids':sorted(extra),'new_family':'bilinear density 2xy; full disk centered below the origin; radio/5 choices; moderate; two solution plots, moderate plot requirement','new_family_generation':'Classified and mathematically validated for inventory; existing frozen generator retains its nine source template families. No claim of new-family replay fidelity.','canonical_unchanged':True})

CASES={c['source_id']:c for c in json.loads((HERE/'source-cases.json').read_text())}
def source_record(q):
 e=q[':db/id']
 if e in CASES:
  c=CASES[e];r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='observed');v.check(r)
  assert signature(q[':question/answer-fields'][0][':answer-field/choices'])==signature(next(z for z in g.KP[':knowledge-point/questions'] if z[':db/id']==e)[':question/answer-fields'][0][':answer-field/choices'])
  if ':question/difficulty' in q:
   assert normalize(q)[':question/answer-fields'][0][':answer-field/correct'][1] in [str(a[':answer/id']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
  # Native grading operates on original identities and bank for rated complete records.
  if ':question/difficulty' in q:return {'knowledge_point':r['knowledge_point'],'question':normalize(q),'generation':r['generation']}
  return r
 assert e==17592186436974
 r={'knowledge_point':{'db_id':KP,'id':g.KP[':knowledge-point/id'],'title':g.KP[':knowledge-point/title']},'question':normalize(q),'generation':{'template':'bilinear-current-source'}}
 f=r['question'][':question/answer-fields'][0];expected=(g.sp.Integer(0),-6*g.sp.sin(g.t),g.r**3*g.sp.sin(2*g.t),g.sp.pi,2*g.sp.pi)
 matches=[];decoded=[]
 for a in f[':answer-field/choices']:
  z=v.parse_integral(a[':answer/value']);decoded.append(z)
  if all(v.same_expr(x,y) for x,y in zip(z,expected)):matches.append(a[':answer/id'])
 assert matches==[f[':answer-field/correct'][1]] and len(set(tuple(map(str,z)) for z in decoded))==5
 # Read the actual rendered Cartesian region and transformed final row.
 assert q[':question/problem']==r'If $D=\{(x,y)\,:\,{x}^{2}+(y+3)^{2}\le 9\},$ then ${∬}_{D}2xy\,\text{d}A=$'
 sol=q[':question/worked-solution'];last=re.findall(r'\$\$(.*?)\$\$',sol,re.S)[-1].split('\\\\')[-1].replace('\\end{aligned}','').lstrip(' & =').rstrip('. ')
 assert all(v.same_expr(x,y) for x,y in zip(v.parse_integral(last),expected))
 assert v.same_expr((2*g.x*g.y).subs({g.x:g.r*g.sp.cos(g.t),g.y:g.r*g.sp.sin(g.t)},simultaneous=True)*g.r,expected[2])
 return r

def fp(q):
 f=q[':question/answer-fields'][0];corr=f[':answer-field/correct'];cid=str(corr[':answer/id']) if isinstance(corr,dict) else corr[1]
 value=next(a[':answer/value'] for a in f[':answer-field/choices'] if str(a[':answer/id'])==cid)
 lo,up,density,start,end=v.parse_integral(value)
 canonical=[lo,up,g.sp.expand_trig(density),g.sp.Mod(start,2*g.sp.pi),end-start]
 return g.hashof([str(g.sp.simplify(z)) for z in canonical])

def local_record(r):
 r=copy.deepcopy(r)
 for f in OUT.glob('basis-*/assets.json'):
  assets=json.loads(f.read_text())
  for source,a in assets.items():
   target=MATH/a['path'];assert sha(target)==a['sha256']
   for key in (':question/problem',':question/worked-solution'):
    r['question'][key]=r['question'][key].replace(a['path'],source)
 return r

def validate(r):
 r=local_record(r);m=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
 assert level in LEVELS and r['knowledge_point']=={'db_id':KP,'id':g.KP[':knowledge-point/id'],'title':g.KP[':knowledge-point/title']}
 replay=g.generate(level,seed=m['seed'],template=m['template'],parameters=m['parameters'],profile=m['profile'])
 assert ordered(replay['question'])==ordered(r['question']) and replay['generation']==m
 v.check(r);return fp(r['question'])

def counts(kp,b,p):
 p.mkdir(parents=True,exist_ok=True)
 shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
 reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
 seen={x[0] for x in shown+reserved};save(p/'scoped.json',scoped(kp,b,seen))
 subprocess.run([str(POOL),str(p/'scoped.json'),str(p/'native-pool.json')],text=True,capture_output=True,check=True,timeout=55)
 pool=json.loads((p/'native-pool.json').read_text());ids={x for xs in pool['available_ids_by_level'].values() for x in xs}
 levels={l:set() for l in LEVELS};records=[];excluded=[]
 known={r['question'][':question/id']:r for f in OUT.glob('basis-*/generated-published.json') for r in json.loads(f.read_text())}
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] not in ids:
   excluded.append({'db_id':q[':db/id'],'reason':'native pool: unrated, incomplete, shown or reserved'});continue
  if ':question/math-academy-id' in q:r=source_record(q)
  else:
   r=known[str(q[':question/id'])];assert normalize(q)==ordered(r['question']);validate(r)
  l=r['question'][':question/difficulty'].split('/')[-1];levels[l].add(fp(r['question']));records.append(r)
 native(records,p/'actual-grading')
 result={'basis':b,'distinct_available':{l:len(xs) for l,xs in levels.items()},'validated_question_ids':[r['question'][':question/id'] for r in records],'excluded':excluded,'native_pool':pool,'deduplication':'exact decoded correct setup: radial bounds, pointwise density, angular start modulo 2pi and angular width; excludes identity, seed, order and bank'}
 save(p/'counts.json',result);return result

def select(kp,needed,p):
 supplied=JOB.with_suffix('.generated');data=json.loads(supplied.read_text()) if supplied.exists() else {};instances=data.get('instances',[]) if isinstance(data,dict) else data
 if isinstance(instances,dict):instances=[instances]
 for r in instances:validate(r)
 save(p/'supplied-status.json',{'exists':supplied.exists(),'validated_instances':len(instances)})
 used=set()
 for q in kp[':knowledge-point/questions']:
  if ':question/math-academy-id' in q:used.add(fp(source_record(q)['question']))
  else:used.add(fp(normalize(q)))
 records=[];added={l:0 for l in LEVELS}
 for l in LEVELS:
  names=['constant_right','constant_left','constant_above','constant_below'] if l=='easy' else [n for n,c in g.TEMPLATES.items() if c['level']==l]
  # Interleave families before changing radii; no replacement by seed/order.
  candidates=list(instances)
  for radius in ([2,3,4,5,1] if l=='easy' else ['3/2','5/2','7/2','9/2','1/2','1','2','3','4','5']):
   for name in names:
    if added[l]>=needed[l]:break
    r=g.generate(l,seed=17592186129275,template=name,parameters={'a':str(radius)})
    candidates.append(r)
   if len(candidates)>=110:break
  for r in candidates:
   if added[l]>=needed[l]:break
   if r['question'][':question/difficulty']!=':question.difficulty/'+l:continue
   key=fp(r['question'])
   if key in used:continue
   validate(r);records.append(r);used.add(key);added[l]+=1
 save(p/'generated.json',records);native(records,p/'selected-grading')
 images=ImageLibrary(MATH,p);published=copy.deepcopy(records)
 for r in published:
  for k in (':question/problem',':question/worked-solution'):r['question'][k]=images.text(r['question'][k])
 for source,a in images.saved.items():
  assert sha(MATH/a['path'])==a['sha256'] and image_path(a['path'],MATH)==(MATH/a['path']).resolve()
 save(p/'assets.json',images.saved);save(p/'generated-published.json',published)
 return published,added

def verify(p,intent,report):
 assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis'];check_report(report,p/'receipt-check',intent['source_eid'])
 b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items())
 exclude={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in kp.items() if k not in exclude}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((p/'generated-published.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);validate(r)
 assert not transaction([],kp,intent['generator_id'])
 after=counts(kp,b,p/'readback')
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'scoped_additive_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':after,'asset_bytes_and_app_route_verified':True}
 save(p/'verification.json',result);return result

def finish(p,gid,verified,inv):
 c=verified['available_counts_after'];remaining={l:max(0,5-c['distinct_available'][l]) for l in LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'unsupported_levels':[],'available_distinct':c['distinct_available'],'shortage_remaining':remaining,'finite_domain':{'easy':20,'moderate':30,'hard':60},'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source_status':'Ten originals and learner history preserved; two incomplete unrated source questions remain excluded. New bilinear source family checked separately; frozen generator retains nine source families.','evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'generated.json',p/'generated-published.json',p/'assets.json',p/'source-refresh.json',p/'inventory-after.json',p/'supplied-status.json',HERE/'validation.json',HERE/'freeze.json',HERE/'reference/replenishment/classification-addendum.md'] if f.exists()]}
 if any(remaining.values()):result['capability_exception']={'bounded_domain_exhausted':True,'remaining_by_level':remaining,'reason':'All finite tasks with distinct decoded polar setups exhausted; seed, identity and choice order do not increase capacity.'}
 save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result)
 print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','available_distinct','shortage_remaining','remaining_jobs')}),flush=True)

def main(inspect=False):
 freeze=json.loads((HERE/'freeze.json').read_text());assert all(sha(ROOT/f)==h for f,h in freeze['files'].items()),'Frozen generator package changed'
 val=json.loads((HERE/'validation.json').read_text());assert val['status']=='pass' and val['matched_choices']==val['total_choices']==45
 if inspect:
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];kp=read(OUT/'inspect',b);source_refresh(kp,OUT/'inspect');c=counts(kp,b,OUT/'inspect');print(json.dumps({'basis':b,'available':c['distinct_available'],'excluded':c['excluded']},indent=2));return
 preview=preview_executable(SimpleNamespace(math_root=MATH,repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
  for p in sorted(OUT.glob('basis-*')):
   if not (p/'commit-intent.json').exists():continue
   intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
   assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
   verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p));finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b);source_refresh(kp,p)
  (p/'before.edn').write_text(dumps(kp)+'\n');source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'question-generator'))
  existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
  if existing:
   assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT;gid=str(existing[0][0][':question-generator/id'])
  save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
  c=counts(kp,b,p/'current-inventory');needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS};print(json.dumps({'basis':b,'available':c['distinct_available'],'missing':needed}),flush=True)
  records,new=select(kp,needed,p)
  ids=[uuid.UUID(uid) for r in records for uid in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
  if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],p,'generated-identities',b)
  save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'available_counts':c,'missing_by_level':needed,'new_by_level':new,'assets':json.loads((p/'assets.json').read_text()),'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True,'frozen_package_hashes_verified':True,'finite_shortages':{l:needed[l]-new[l] for l in LEVELS if needed[l]>new[l]}})
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
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'polar-offset-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(p/'commit-intent.json',intent)
  verified=verify(p,intent,DB._commit(intent,txpath,p));finish(p,gid,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main('--inspect' in sys.argv)
