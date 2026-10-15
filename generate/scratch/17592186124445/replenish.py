"""Scoped inventory preparation, additive EDB commit, and exact-basis verification."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
import sympy as S
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment,build_learning
from capture.scripts.database.preview import preview_executable
spec=importlib.util.spec_from_file_location('gradient_validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.ID;SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'b9f37e6ee72ed133d69e3ae35806a323bdc5bf0019ff9ff68df05fe1442a3f20'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
QUERY='''[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/questions [* {:question/difficulty [:db/id :db/ident]} {:knowledge-point/_canonical-example [:db/id]} {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/correct [* {:answer/type [:db/ident]}]} {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]} {:knowledge-point/canonical-example [*]}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'''
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] (or-join [?q ?l] (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]) (and [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
SAFE={'easy':['shifted_log'],'moderate':['quadratic','coupled','logquad'],'hard':['entropy']}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read_kp(p,b):return DB.query(QUERY,[KP],p,'kp',b)[0][0]
def inventory(p):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(p,x['data']);return x['data']
def normalize(q):
 q=copy.deepcopy(q)
 for k in list(q):
  if k not in (':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):del q[k]
 q[':question/id']=str(q[':question/id'])
 if isinstance(q[':question/difficulty'],dict):q[':question/difficulty']=str(q[':question/difficulty'][':db/ident'])
 for f in q[':question/answer-fields']:
  f.pop(':db/id',None);f[':answer-field/id']=str(f[':answer-field/id'])
  if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=str(f[':answer-field/type'][':db/ident'])
  if isinstance(f[':answer-field/correct'],dict):f[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
  for a in f[':answer-field/choices']:
   a.pop(':db/id',None);a[':answer/id']=str(a[':answer/id'])
   if isinstance(a[':answer/type'],dict):a[':answer/type']=str(a[':answer/type'][':db/ident'])
  f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
 q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key']);return q

def expression(q):
 text=q[':question/problem'];m=re.search(r'\$[fgh]\(x,\s*y(?:,\s*z)?\)\s*=\s*(.*?)\$',text);assert m,text
 return v.math(m[1].rstrip(',.'))
def signature(q):
 e=expression(q);vs=(v.x,v.y,v.z) if v.z in e.free_symbols else (v.x,v.y)
 ds=[S.simplify(S.diff(e,t)) for t in vs]
 # Normalize common nonzero numeric scale; omit seed, UUID, answer order, difficulty.
 coeff=next(d.as_coeff_Mul()[0] for d in ds if d!=0)
 return g.digest({'gradient':[str(S.simplify(d/coeff)) for d in ds],'interval':re.findall(r'0\\le y<.*?\$',q[':question/problem'])})

def native_item(q,label):
 q=normalize(q);checks=[]
 for i,f in enumerate(q[':question/answer-fields']):
  for a in f[':answer-field/choices']:
   checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Current practice field native grading'})
 return {'label':label,'record':{'question':q,'knowledge_point':{'title':g.KP[':knowledge-point/title']}},'checks':checks}
def native(items,p):
 save(p/'native-input.json',items);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(p/'native-input.json'),str(p/'native-report.json')],check=True)
 assert json.loads((p/'native-report.json').read_text())['documented_unresolved_checks']==0

def validate_source(q):
 e=expression(q);vs=(v.x,v.y,v.z) if v.z in e.free_symbols else (v.x,v.y);ds=[S.diff(e,t) for t in vs]
 mid=q.get(':question/math-academy-id')
 if mid=='q-128517':roots={(S.Integer(1),S.Integer(0)),(S.Integer(0),S.pi/2)}
 elif mid=='q-71470':
  # exp(t)>0: x exp(x)=0 => x=0 => y=0; z(z+2)=0.
  assert S.simplify(e-v.x*v.y*S.exp(v.x)-v.z**2*S.exp(v.z))==0
  roots={(S.Integer(0),S.Integer(0),S.Integer(0)),(S.Integer(0),S.Integer(0),S.Integer(-2))}
 else:
  sol=S.solve(ds,vs,dict=True);roots=set()
  for r in sol:
   assert set(r)==set(vs)
   point=tuple(S.simplify(r[t]) for t in vs)
   if all(t.is_real is not False for t in point) and all(S.simplify(d.subs(r))==0 for d in ds):roots.add(point)
 assert roots,(mid,ds)
 fields=q[':question/answer-fields']
 if str(fields[0][':answer-field/type'][':db/ident'])==':answer-field.type/checkbox':
  for f in fields:
   key=f[':answer-field/key'];candidate=re.search(r'\*\*'+key+r'\.\*\* \$(.*?)\$',q[':question/problem']);assert candidate,(mid,key)
   point=next(iter(v.points(candidate[1])))
   assert (f[':answer-field/correct'][':answer/value']=='true')==(point in roots),(mid,key)
 else:
  f=fields[0];assert v.points(f[':answer-field/correct'][':answer/value'])==roots,(mid,roots)
  assert sum(v.points(a[':answer/value'])==roots for a in f[':answer-field/choices'])==1
 assert q.get(':question/worked-solution')
 return {'db_id':q[':db/id'],'source_id':mid,'roots':[list(map(str,p)) for p in sorted(roots,key=str)],'fields':[{'key':f[':answer-field/key'],'type':str(f[':answer-field/type'][':db/ident']),'choice_count':len(f[':answer-field/choices'])} for f in fields],'plots':'none','difficulty':str(q[':question/difficulty'][':db/ident'])}

def counts(p,kp,b):
 used={r[0] for r in DB.query(USAGE,[KP,LEARNER],p,'unavailable',b)}
 used.update(r[0] for r in DB.query(USAGE,[KP,LEARNER],p,'historically-unavailable',b,history=True))
 available={l:[] for l in g.LEVELS};reports=[];items=[]
 for q in kp[':knowledge-point/questions']:
  report=validate_source(q);reports.append(report);items.append(native_item(q,str(q[':question/id'])))
  if q[':db/id'] not in used and not q.get(':knowledge-point/_canonical-example'):
   level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
   if level in available:available[level].append(signature(q))
 native(items,p)
 c={'basis':b,'levels':{l:len(set(xs)) for l,xs in available.items()},'excluded_shown_or_reserved':sorted(used),'source_checks':reports}
 save(p/'available-counts.json',c);return c

def validate_instance(r):
 assert r['knowledge_point']['db_id']==KP and r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
 level=r['question'][':question/difficulty'].split('/')[-1];assert r['generation']['template'] in SAFE[level]
 v.check(r)
 replay=g.generate(level,r['generation']['seed'],r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
 assert r==replay
 return r

def transaction(records,kp,gid):
 forms=[]
 for rec in records:
  q=rec['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 if kp.get(':knowledge-point/question-generator') is None:
  forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def check_report(report,p,source):
 attrs={e:str(a) for e,a in DB.attributes(p,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,val,tx,s,added in report[':edb/tx-data']:
  assert s==source and added,'Unexpected attribution or retraction'
  name=attrs[a]
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,(e,name)

def verify(p,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,p/'receipt-check',intent['source_eid']);kp=read_kp(p/'readback',report[':edb/db-after-t']);before=loads((p/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items())
 assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records)
 byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  validate_instance(r);q=byid[r['question'][':question/id']];assert normalize(q)==normalize(r['question']);assert ':question/math-academy-id' not in q
 c=counts(p/'readback',kp,report[':edb/db-after-t']);assert all(n>=5 for n in c['levels'].values()),c['levels']
 assert not transaction([],kp,intent['generator_id'])
 verified={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'original_questions_preserved':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'repeat_preparation_content_changes':0,'generator_registration_verified':True,'available_after':c['levels']}
 save(p/'verification.json',verified);return verified

def finish(p,verified):
 inv=inventory(p/'inventory-after.json');remaining=[j for j in inv['jobs'] if j['knowledgePoint']==KP]
 assert not remaining,remaining
 result={'outcome':'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':json.loads((p/'commit-intent.json').read_text())['generator_id'],'verified_commit_basis':verified['basis_after'],'lineage':LINEAGE,'new_questions':verified['new_questions'],'supported_levels':list(g.LEVELS),'available_by_level':verified['available_after'],'shortage_remaining':{l:max(0,5-n) for l,n in verified['available_after'].items()},'unsupported_levels_filled':False,'remaining_jobs':remaining,'bounded_scope':'Existing validated radio generator; four later checkbox migrations and two later source templates retained unchanged. This run uses unchanged radio families only. No unsupported difficulty is claimed filled.','evidence':[str(x.relative_to(ROOT)) for x in (p/'verification.json',p/'commit-intent.json',p/'commit.edn',p/'transaction.edn',p/'preview.edn',p/'preparation.json',p/'readback/native-report.json',p/'inventory-after.json',HERE/'validation.json',OUT/'source-replay.json')]}
 save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
 global NATIVE
 NATIVE=build_learning(ROOT.parent/'EDB')
 validation=json.loads((HERE/'validation.json').read_text());assert validation['passed']
 assert sha(HERE.with_suffix('.py'))==validation['generator_sha256'] and sha(HERE/'validate.py')==validation['validator_sha256']
 assert sha(ROOT/'generate/runs/current/check-engine')==validation['native_engine_sha256']
 replay=[]
 for f in g.FAMILIES:
  level=next(l for l,fs in g.LEVELS.items() if f in fs);r=v.check(g.generate(level,17,f,parameters=g.ORIGINAL[f],profile='raw_'+f));q=r['question'];old=g.TEMPLATES[f]
  assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
  assert sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':question/answer-fields'][0][':answer-field/choices'])
  replay.append({'template':f,'complete_bank_matched':5,'prompt_and_solution_exact':True})
 save(OUT/'source-replay.json',{'source_basis':1356,'sources':replay,'generator_sha256':sha(HERE.with_suffix('.py'))})
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);print('api.lock held; reading fresh inventory and basis',flush=True)
  for p in sorted(OUT.glob('basis-*')):
   if (p/'commit-intent.json').exists():
    intent=json.loads((p/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
    assert intent['exact_edn']==(p/'transaction.edn').read_text() and intent['sha256']==sha(p/'transaction.edn')
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    report=DB._commit(intent,p/'transaction.edn',p);finish(p,verify(p,intent,report));return
  inv=inventory(OUT/'inventory-under-lock.json');b=inv['basis'];assert DB.basis()==b
  p=OUT/f'basis-{b}';p.mkdir(exist_ok=True);kp=read_kp(p,b);assert str(kp[':knowledge-point/id'])==g.KP[':knowledge-point/id'];(p/'before.edn').write_text(dumps(kp)+'\n')
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'contributor',b);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');byscript=DB.query('[:find (pull ?e [*]) :in $ ?script :where [?e :question-generator/script ?script]]',[SCRIPT],p,'generator-by-script',b);assert len(byscript)<=1
  gid=str(gen[':question-generator/id']) if gen else str(byscript[0][0][':question-generator/id']) if byscript else str(uuid.uuid5(g.NS,'question-generator:'+str(KP)))
  if gen:assert gen[':question-generator/script']==SCRIPT
  byid=DB.query('[:find (pull ?e [*]) :in $ ?id :where [?e :question-generator/id ?id]]',[uuid.UUID(gid)],p,'generator-by-id',b);assert len(byid)<=1
  if byid:assert byid[0][0][':question-generator/script']==SCRIPT
  current=counts(p,kp,b);needed={l:max(0,5-n) for l,n in current['levels'].items()};used={signature(q) for q in kp[':knowledge-point/questions']};used.add(signature(kp[':knowledge-point/canonical-example']))
  suppliedpath=JOB.with_suffix('.generated');supplied=json.loads(suppliedpath.read_text()) if suppliedpath.exists() else {};eligible=[]
  for r in supplied.get('instances',[]):eligible.append(validate_instance(r))
  save(p/'supplied-status.json',{'exists':suppliedpath.exists(),'validated_instances':len(eligible),'generator_error':supplied.get('generatorError')})
  records=[];added={l:0 for l in g.LEVELS}
  # Execute the validated CLI after the captured inventory read. Every instance is replayed and independently checked below.
  candidates=list(eligible)
  for l,n in needed.items():
   if n:
    run=subprocess.run([sys.executable,str(HERE.with_suffix('.py')),'--difficulty',l,'--count',str(max(20,n*3)),'--seed',str(int(JOB.name[:8],16)),'--format','json'],capture_output=True,text=True,check=True)
    (p/f'cli-{l}.json').write_text(run.stdout);candidates.extend(json.loads(run.stdout))
  for r in candidates:
   l=r['question'][':question/difficulty'].split('/')[-1]
   if added[l]>=needed[l] or r['generation']['template'] not in SAFE[l]:continue
   validate_instance(r);fp=signature(r['question'])
   if fp in used:continue
   records.append(r);used.add(fp);added[l]+=1
  assert added==needed,('Bounded generator could not fill requested inventory',needed,added)
  save(p/'generated.json',records);(p/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
  native([v.native(str(i),r) for i,r in enumerate(records+eligible)],p/'generated-grading')
  for attr,values in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
   if values:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(i) for i in values]],p/'identity-check',attr.replace('/','-'),b)
  save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'available_before':current['levels'],'needed':needed,'new_by_level':added,'source':SOURCE,'generator_id':gid,'generator_sha256':sha(HERE.with_suffix('.py')),'deduplication':'Normalized exact gradient and interval; excludes canonical/source/served content, seed, UUID, choice order and overall scaling','asset_hashes':[],'validated_scope':SAFE,'capability_exceptions':['Two new hard templates and four checkbox presentations are current source evidence, preserved, independently keyed and natively graded; generation of those layouts is outside this frozen radio version. All difficulty levels have validated same-KP templates.']})
  forms=transaction(records,kp,gid);assert forms
  txpath=p/'transaction.edn';tx=dumps(forms)+'\n'
  with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
  run=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
  (p/'preview.edn').write_text(run.stdout);pr=loads(run.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'gradient-zero-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(p/'commit-intent.json',intent);report=DB._commit(intent,txpath,p);finish(p,verify(p,intent,report))
if __name__=='__main__':main()
