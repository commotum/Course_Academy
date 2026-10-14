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
import importlib.util
sys.path.insert(0,str(HERE))
spec=importlib.util.spec_from_file_location('scalar_validation',HERE/'validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
g=v.g;s=v.s
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'07faa2c36082ac8bf24a2f73eccfb3c05eea8768624a576264b4f89b90a208ea'
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
def fingerprint_data(F,x,y,lo,hi):
 # Conservative collision rule: identical scalar pullback integrals are one
 # task even when curve orientation, bank, source profile or identity differs.
 T=v.T;X=v.X;Y=v.Y
 speed=s.sqrt(s.factor(s.trigsimp(s.diff(x,T)**2+s.diff(y,T)**2)))
 if float(lo)>=0:speed=speed.xreplace({s.Abs(T):T,s.Abs(T+1):T+1})
 integrand=s.trigsimp(s.expand(F.subs({X:x,Y:y})*speed))
 return g.digest([s.srepr(integrand),str(lo),str(hi)])
def fingerprint(q):
 if str(q[':question/id'])==str(g.REC[':knowledge-point/canonical-example'][':question/id']):
  return fingerprint_data(v.X*v.Y,3*v.T,4*v.T,s.Integer(0),s.Integer(1))
 return fingerprint_data(*(v.source_prompt(q) if ':question/math-academy-id' in q else v.prompt(q)))
def check(rec):
 assert rec['knowledge_point']['db_id']==KP and rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
 family=rec['generation']['template'];level=rec['question'][':question/difficulty'].split('/')[-1]
 assert rec['generation']['bank_profile']=='method_'+family and g.TEMPLATES[family]==level
 g.validate_parameters(family,rec['generation']['parameters'])
 v.contract(rec);v.mathcheck(rec)
 # Exact replay establishes metadata and prompt/solution/bank consistency.
 replay=g.generate(level,rec['generation']['seed'],template=family,parameters=rec['generation']['parameters'])
 assert comparable(replay['question'])==comparable(rec['question'])
 return fingerprint(rec['question'])
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
 assert not transaction([],kp,intent['generator_id'])
 for a in json.loads((path/'preparation.json').read_text())['assets']:assert sha(Path('/media/jake/SSD/EDB/math')/a['database_path'])==a['sha256']
 result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'new_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
 save(path/'verification.json',result);return result

def finish(path,intent,verified,inv):
 prep=json.loads((path/'preparation.json').read_text());remaining=[j for j in inv['jobs'] if j['knowledgePoint']==KP]
 result={'outcome':'finite-limit' if any(prep['remaining_shortage'].values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'verified_commit_basis':verified['basis_after'],'lineage':LINEAGE,'new_questions':verified['new_questions'],'new_by_level':verified['new_by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'capability_exceptions':[],'remaining_shortage':prep['remaining_shortage'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':remaining,'source_exclusions':['q-40258 and q-41160 remain unrated with missing original keys and solutions; unchanged and excluded from usable inventory. Raw historical bank profiles remain evidence-only.'],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'inventory-after.json',path/'preparation.json',path/'native-report.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'reference/freeze.json')]}
 if any(prep['remaining_shortage'].values()):result['capability_exceptions']=[{'kind':'bounded-sampling-limit','attempt_limit':1000,'remaining':prep['remaining_shortage']}]
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
 print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_by_level','remaining_jobs')}),flush=True)

def main():
 freeze=json.loads((HERE/'reference/freeze.json').read_text());assert all(sha(ROOT/p)==h for p,h in freeze['hashes'].items())
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
  expected=g.REC;source_questions={str(q[':question/id']):q for q in kp[':knowledge-point/questions']}
  assert all(comparable(q)==comparable(source_questions[str(q[':question/id'])]) for q in expected[':knowledge-point/questions']),'Source changed; reclassify'
  assert comparable(kp[':knowledge-point/canonical-example'])==comparable(expected[':knowledge-point/canonical-example'])
  sources=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(sources)==1
  gen=kp.get(':knowledge-point/question-generator');registration=DB.query('[:find (pull ?g [*]) :in $ ?p :where [?g :question-generator/script ?p]]',[SCRIPT],path,'generator-by-script',b)
  assert len(registration)<=1
  gid=str(gen[':question-generator/id']) if gen else str(registration[0][0][':question-generator/id']) if registration else str(uuid.uuid5(uuid.UUID(g.REC[':knowledge-point/id']),'question-generator'))
  jobs={j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP}
  # Native inventory omits unobserved hard; the validated authored extension
  # opens its five-item reserve without counting unrated historical questions.
  counts={l:jobs[l]['available'] if l in jobs else (0 if not any(q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/'+l for q in kp[':knowledge-point/questions']) else 5) for l in LEVELS}
  needed={l:max(0,5-counts[l]) for l in LEVELS}
  used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
  if isinstance(instances,dict):instances=[instances]
  assert isinstance(instances,list)
  records=[];selected={l:0 for l in LEVELS}
  for r in instances:
   fp=check(r);level=r['question'][':question/difficulty'].split('/')[-1]
   if fp not in used and selected[level]<needed[level]:records.append(copy.deepcopy(r));used.add(fp);selected[level]+=1
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
  for level in LEVELS:
   for offset in range(1000):
    if selected[level]>=needed[level]:break
    r=g.generate(level,seed=133830014+offset,template=[f for f,l in g.TEMPLATES.items() if l==level][offset%sum(l==level for l in g.TEMPLATES.values())]);fp=check(r)
    if fp not in used:records.append(r);used.add(fp);selected[level]+=1
  remaining={l:needed[l]-selected[l] for l in LEVELS}
  for attr,ids in (
   ('question/id',[r['question'][':question/id'] for r in records]),
   ('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),
   ('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])):
   assert len(ids)==len(set(ids))
   if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(i) for i in ids]],path,'identity-'+attr.split('/')[0],b)
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
  (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
  save(path/'generated.json',records);save(path/'native-input.json',[native(r) for r in records])
  subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_counts':counts,'needed':needed,'selected':selected,'remaining_shortage':remaining,'assets':assets,'source_evidence_unchanged':True,'distinctness':'Printed geometry independently derives the scalar pullback integrand and bounds. Identical pullback integrals collapse even across orientation, bank, profile, seed or identity. All source tasks and canonical example excluded.','validation_sha256':sha(HERE/'validation.json')})
  if '--prepare-only' in sys.argv:
   print(json.dumps({'prepared_basis':b,'selected':selected,'path':str(path)}),flush=True);return
  forms=transaction(records,kp,gid);assert forms,'No content or registration changes required'
  txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
  with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
  (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
  check_report(pr,path/'preview-check',sources[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':ENV['EDB_ENDPOINT'],'lineage':LINEAGE,'source':SOURCE,'source_eid':sources[0][0],'basis':b,'expected_basis':b,'request_key':'scalar-ds-evaluation-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,intent,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
