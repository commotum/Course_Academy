"""Scoped additive inventory replenishment through the configured EDB integration."""
import copy, fcntl, hashlib, json, os, re, subprocess, sys, threading, types, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
from image_library import ImageLibrary
# Reuse the existing independent rendered-mathematics validator without rerunning
# its package-wide test harness when validating each prepared instance.
v=types.ModuleType('instance_validation');v.__file__=str(HERE/'validate.py')
exec(compile((HERE/'validate.py').read_text().split('\ncases=[g.source_case')[0],v.__file__,'exec'),v.__dict__)
g=v.g;s=g.s
KP=g.KP[':db/id'];LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'8f3bd3989d0fc354fc46f08d782dfd922dab158797a595ca4bca88acd4bf23f9'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
NATIVE=max((p for p in (ROOT/'.local/graph-explorer').glob('learning-*') if p.is_file() and p.stat().st_mode&0o111),key=lambda p:p.stat().st_mtime)
QUERY=(HERE/'reference/source-query.edn').read_text()
LEVELS=('easy','moderate','hard')

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,ENV['EDB_ENDPOINT']],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE
 save(path,x['data']);return x['data']
def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def comparable(o):
 if isinstance(o,dict):
  if ':db/ident' in o:return {':db/ident':str(o[':db/ident'])}
  return {str(k):comparable(z) for k,z in o.items() if str(k) not in (':knowledge-point/_questions',':knowledge-point/_canonical-example')}
 if isinstance(o,list):return sorted([comparable(z) for z in o],key=lambda z:json.dumps(z,sort_keys=True))
 return o if o is None or isinstance(o,(str,int,float,bool)) else str(o)
def fingerprint_data(curve,density,a,b,fragment):
 ft=s.simplify(density.subs({g.X:curve,g.Y:g.T}))
 speed=s.sqrt(s.diff(curve,g.T)**2+1)
 # Bounds do not change a missing-integrand task; collapse those duplicates.
 values=[ft] if fragment else [s.simplify(ft*speed),s.sympify(a),s.sympify(b)]
 return hashlib.sha256(json.dumps([s.srepr(z) for z in values]).encode()).hexdigest()
def fingerprint(q):
 mid=q.get(':question/math-academy-id')
 if mid in {x[':question/math-academy-id'] for x in g.QS}:
  i=next(i for i,x in enumerate(g.QS) if x[':question/math-academy-id']==mid)
  _,level,curve,density,a,b,bank,ci,_=g.OBS[i]
  return fingerprint_data(curve,density,a,b,not isinstance(bank[ci],tuple))
 if str(q[':question/id'])==str(g.KP[':knowledge-point/canonical-example'][':question/id']):
  return fingerprint_data(g.T**2,g.X/g.Y,1,3,False)
 prompt=q[':question/problem'];equation=re.search(r'(?:line|curve) \$(.*?)\$',prompt).group(1)
 left,right=equation.split('=',1);curve=s.solve(s.Eq(v.parse(left),v.parse(right)),g.X)[0].subs(g.Y,g.T)
 density=v.parse(re.search(r'\\int_C (.*?)\\,\\mathrm\{d\}s',prompt).group(1))
 pts=re.findall(r'points \$\((.*?),(.*?)\)\$ and \$\((.*?),(.*?)\)\$',prompt)[0]
 return fingerprint_data(curve,density,v.parse(pts[1]),v.parse(pts[3]),r'\boxed{}' in prompt)
def check(rec):
 assert rec['knowledge_point']['db_id']==KP and rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
 assert rec['generation']['bank_profile']=='authored_operations'
 v.mathcheck(rec)
 replay=g.generate(rec['question'][':question/difficulty'].split('/')[-1],rec['generation']['seed'],rec['generation']['template'],parameters=rec['generation']['parameters'],profile=rec['generation']['bank_profile'])
 assert comparable(rec['question'])==comparable(replay['question'])
 return fingerprint(rec['question'])
USAGE_QUERY='''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
def counts(kp,path,basis):
 unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
 known={}
 for saved in OUT.glob('basis-*/generated.json'):
  for r in json.loads(saved.read_text()):known[r['question'][':question/id']]=r
 native_items=[];rows={l:[] for l in LEVELS};excluded=[]
 for q in kp[':knowledge-point/questions']:
  level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
  if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example') or level not in LEVELS or not q.get(':question/worked-solution') or not all(f.get(':answer-field/correct') for f in q[':question/answer-fields']):
   excluded.append(str(q[':question/id']));continue
  mid=q.get(':question/math-academy-id')
  if mid:
   i=next(i for i,x in enumerate(g.QS) if x[':question/math-academy-id']==mid)
   r=g.generate(level,template=g.OBS[i][0],parameters={'density_scale':1},profile='observed_raw');v.mathcheck(r)
  else:
   r=known.get(str(q[':question/id']))
   if r is None:excluded.append(str(q[':question/id']));continue
   assert normalize(q)==comparable(r['question']);check(r)
  native_items.append(native(r));rows[level].append(q)
 save(path/'pool-native-input.json',native_items)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'pool-native-input.json'),str(path/'pool-native-report.json')],check=True)
 result={'basis':basis,'levels':{l:len({fingerprint(q) for q in qs}) for l,qs in rows.items()},'unavailable_entities':sorted(unavailable),'excluded_question_ids':excluded,'available_ids':{l:[str(q[':question/id']) for q in qs] for l,qs in rows.items()}}
 save(path/'counts.json',result);return result
def native(rec):
 f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete field-owned radio bank'} for a in f[':answer-field/choices']]}
def transaction(records,kp,gid):
 forms=[]
 for rec in records:
  q=rec['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen is None:forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def check_report(report,path,source):
 attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,value,tx,contributor,added in report[':edb/tx-data']:
  assert contributor==source and added,'Unexpected retraction or contributor'
  name=attrs[a]
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,name

def normalize(q):
 q=comparable(q);out={k:q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
 out[':question/difficulty']=q[':question/difficulty'][':db/ident'];out[':question/answer-fields']=[]
 for f in q[':question/answer-fields']:
  out[':question/answer-fields'].append({':answer-field/id':f[':answer-field/id'],':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/correct':[':answer/id',f[':answer-field/correct'][':answer/id']],':answer-field/choices':[{':answer/id':a[':answer/id'],':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
 return comparable(out)
def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 check_report(report,path/'receipt-check',intent['source_eid'])
 kp=read_kp(path/'readback',report[':edb/db-after-t']);before=loads((path/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(now[e]==q for e,q in old.items())
 excluded=(':knowledge-point/questions',':knowledge-point/question-generator')
 assert {k:z for k,z in before.items() if k not in excluded}=={k:z for k,z in kp.items() if k not in excluded}
 records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
 assert len(now)==len(old)+len(records)
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
  assert normalize(q)==comparable(r['question']);check(r)
 c=counts(kp,path/'readback',report[':edb/db-after-t'])
 prep=json.loads((path/'preparation.json').read_text())
 assert all(c['levels'][l]>=prep['available_counts']['levels'][l]+prep['selected'][l] for l in LEVELS)
 assert not transaction([],kp,intent['generator_id'])
 for a in json.loads((path/'preparation.json').read_text())['assets']:assert sha(Path('/media/jake/SSD/EDB/math')/a['database_path'])==a['sha256']
 result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'new_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
 save(path/'verification.json',result);return result

def finish(path,intent,verified,inv):
 prep=json.loads((path/'preparation.json').read_text());remaining=[j for j in inv['jobs'] if j['knowledgePoint']==KP]
 result={'outcome':'finite-limit' if any(prep['remaining_shortage'].values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'verified_commit_basis':verified['basis_after'],'lineage':LINEAGE,'new_questions':verified['new_questions'],'new_by_level':verified['new_by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'capability_exceptions':[],'remaining_shortage':prep['remaining_shortage'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':remaining,'source_exclusions':['q-122139 and q-122446 remain unrated and lack keys and solutions; unchanged and excluded from usable inventory. Historical bank replay remains evidence-only.'],'available_counts_before':prep['available_counts'],'available_counts_after':verified['available_counts_after'],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'inventory-after.json',path/'preparation.json',path/'native-report.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'freeze.json')]}
 if any(prep['remaining_shortage'].values()):result['capability_exceptions']=[{'kind':'bounded-sampling-limit','attempt_limit':1000,'remaining':prep['remaining_shortage']}]
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
 print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_by_level','remaining_jobs')}),flush=True)

def main():
 freeze=json.loads((HERE/'freeze.json').read_text());assert all(sha(ROOT/p)==h for p,h in freeze['files'].items())
 assert json.loads((HERE/'validation.json').read_text())['status']=='passed'
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn')
    assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent,verified,inventory(path/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path,b);(path/'before.edn').write_text(dumps(kp)+'\n')
  expected=g.SOURCE['record'];source_questions={str(q[':question/id']):q for q in kp[':knowledge-point/questions']}
  assert all(comparable(q)==comparable(source_questions[str(q[':question/id'])]) for q in expected[':knowledge-point/questions']),'Source changed; reclassify'
  assert comparable(kp[':knowledge-point/canonical-example'])==comparable(expected[':knowledge-point/canonical-example'])
  sources=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(sources)==1
  gen=kp.get(':knowledge-point/question-generator');registration=DB.query('[:find (pull ?g [*]) :in $ ?p :where [?g :question-generator/script ?p]]',[SCRIPT],path,'generator-by-script',b)
  assert len(registration)<=1
  gid=str(gen[':question-generator/id']) if gen else str(registration[0][0][':question-generator/id']) if registration else str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'question-generator'))
  current=counts(kp,path,b);available=current['levels']
  needed={l:max(0,5-available[l]) for l in LEVELS}
  used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
  if isinstance(instances,dict):instances=[instances]
  assert isinstance(instances,list)
  records=[];selected={l:0 for l in LEVELS}
  for r in instances:
   fp=check(r);level=r['question'][':question/difficulty'].split('/')[-1]
   if fp not in used and selected[level]<needed[level]:records.append(copy.deepcopy(r));used.add(fp);selected[level]+=1
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
  sampling_errors=[]
  templates={'easy':['authored_line_monomial','authored_affine','authored_line'],'moderate':['authored_log','authored_scaled_log','authored_reciprocal','authored_power'],'hard':['authored_shifted_power']}
  for level in LEVELS:
   for offset in range(1000):
    if selected[level]>=needed[level]:break
    try:r=g.generate(level,seed=2281945288+offset,template=templates[level][offset%len(templates[level])])
    except ValueError as error:
     sampling_errors.append({'level':level,'seed':2281945288+offset,'reason':str(error)});continue
    fp=check(r)
    if fp not in used:records.append(r);used.add(fp);selected[level]+=1
  remaining={l:needed[l]-selected[l] for l in LEVELS}
  save(path/'sampling-exceptions.json',sampling_errors)
  ids=[uuid.UUID(r['question'][':question/id']) for r in records]+[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]+[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]
  if ids:assert not DB.query('[:find ?q ?id :in $ [?id ...] :where (or-join [?q ?id] [?q :question/id ?id] [?q :answer-field/id ?id] [?q :answer/id ?id])]',[ids],path,'generated-identities',b)
  registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
  assert not registered or registered[0][0][':question-generator/script']==SCRIPT
  assets=[];library=ImageLibrary(Path('/media/jake/SSD/EDB/math'))
  save(path/'local-generated.json',records)
  for r in records:
   for key in (':question/problem',':question/worked-solution'):
    for asset in re.findall(r'!\[.*?\]\((.*?)\)',r['question'][key]):
     local=Path(asset) if Path(asset).is_absolute() else ROOT/asset;data=local.read_bytes();relative=library.put_bytes(data);assert (library.math_root/relative).read_bytes()==data
     r['question'][key]=r['question'][key].replace(asset,relative);assets.append({'local_path':asset,'database_path':relative,'sha256':hashlib.sha256(data).hexdigest()})
   check(r)
  save(path/'generated.json',records);save(path/'native-input.json',[native(r) for r in records])
  subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_counts':current,'needed':needed,'selected':selected,'remaining_shortage':remaining,'assets':assets,'source_evidence_unchanged':True,'distinctness':'Simplified requested expression; complete integrals include bounds. Fragment questions ignore bounds. Seed, identity and option order are excluded. Canonical example excluded.','validation_sha256':sha(HERE/'validation.json')})
  if '--prepare-only' in sys.argv:
   print(json.dumps({'prepared_basis':b,'selected':selected,'path':str(path)}),flush=True);return
  forms=transaction(records,kp,gid);assert forms,'No content or registration changes required'
  txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
  with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
  (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
  check_report(pr,path/'preview-check',sources[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':ENV['EDB_ENDPOINT'],'lineage':LINEAGE,'source':SOURCE,'source_eid':sources[0][0],'basis':b,'expected_basis':b,'request_key':'function-y-setup-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,intent,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
