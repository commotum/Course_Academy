"""Scoped additive replenishment; exact request recovery and locked readback."""
import copy,fcntl,hashlib,importlib.util,json,os,re,subprocess,sys,threading,uuid
from pathlib import Path
from fractions import Fraction
from types import SimpleNamespace
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
s=importlib.util.spec_from_file_location('current_validation',HERE/'validate_replenishment.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));OUT=HERE/'reference/replenishment'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'2a298cbbba7dd1c78a6ee5f514324383e7f3afe62c89a01d1b703300e69a1722'
ENV=database_environment('math');DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
NATIVE=Path((OUT/'native-path.txt').read_text())
QUERY=(OUT/'source-query.edn').read_text()
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):
 if isinstance(x,dict):return {str(k):canon(v) for k,v in x.items() if str(k) not in (':knowledge-point/_questions',':knowledge-point/_canonical-example')}
 if isinstance(x,(tuple,list)):return sorted((canon(v) for v in x),key=lambda y:json.dumps(y,sort_keys=True))
 if isinstance(x,uuid.UUID):return str(x)
 return x

def coefficient(q):
 text=q[':question/problem'].replace(' ','');m=re.search(r'\\(?:d?frac)\{(\d+)\}\{(\d*)x\}',text);assert m,text
 return str(Fraction(int(m[1]),int(m[2] or 1)))
def normalize(q):
 out={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
 out[':question/difficulty']=q[':question/difficulty'][':db/ident'];out[':question/answer-fields']=[]
 for f in q[':question/answer-fields']:
  out[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
 return canon(out)
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=120)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def read(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def counts(kp,path,basis):
 unavailable={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'usage',basis)};pools={l:[] for l in g.SUPPORTED_LEVELS};excluded=[]
 for q in kp[':knowledge-point/questions']:
  fs=q[':question/answer-fields'];level=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]
  if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example') or level not in pools or not fs or len({f[':answer-field/key'] for f in fs})!=len(fs) or any(not f.get(':answer-field/correct') for f in fs):excluded.append(q[':db/id']);continue
  pools[level].append(q)
 result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({coefficient(q) for q in qs}),'question_ids':[str(q[':question/id']) for q in qs]} for l,qs in pools.items()},'excluded':excluded,'excluded_shown_reserved':sorted(unavailable),'hard':{'available':0,'supported':False,'nominal_shortage':5}}
 save(path/'available-counts.json',result);return result

def forms(records,kp,gid):
 tx=[]
 for rec in records:
  q=rec['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:tx.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   tx.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  tx.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen is None:tx.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 if records:tx.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if tx:tx.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return tx

def report_check(report,path,source):
 attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':answer/id',':answer/type',':answer/value',':question-generator/id',':question-generator/script'}
 for e,a,value,tx,s,added in report[':edb/tx-data']:
  assert s==source and added,'Unexpected contributor or retraction'
  name=attrs[a]
  if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert e in new and name in allowed,(e,name)

def verify(path,intent,receipt):
 assert receipt[':edb/committed'] is True and receipt[':edb/db-before-t']==intent['basis']
 report_check(receipt,path/'receipt-check',intent['source_eid']);basis=receipt[':edb/db-after-t']
 before=loads((path/'before.edn').read_text());after=read(path/'readback',basis)
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in after[':knowledge-point/questions']};assert all(now[e]==q for e,q in old.items())
 assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in after.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
 byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==canon(r['question']);v.independent(r)
 for asset in json.loads((path/'asset-hashes.json').read_text()):assert sha(Path(ENV['EDB_MATH_ROOT'])/asset['path'])==asset['sha256']
 assert not forms([],after,intent['generator_id'])
 c=counts(after,path/'readback',basis)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'unchanged_source_questions':len(old),'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_changes':0,'available_counts_after':c}
 save(path/'verification.json',result);return result

def finish(path,intent,verified,inv):
 c=verified['available_counts_after'];remaining={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in g.SUPPORTED_LEVELS}
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'lineage':LINEAGE,'supported_levels':list(g.SUPPORTED_LEVELS),'available_counts_after':{l:c['levels'][l]['distinct_available_tasks'] for l in g.SUPPORTED_LEVELS},'shortage_remaining_supported':remaining,'unsupported_levels':['hard'],'unsupported_nominal_shortage':{'hard':5},'unsupported_levels_filled':False,'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'native-validation.json',path/'asset-hashes.json',path/'inventory-after.json',OUT/'validation.json',HERE/'capabilities.json',HERE/'source-refresh.json') if p.exists()]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result),flush=True)

def main():
 validation=json.loads((OUT/'validation.json').read_text());assert validation['status']=='pass' and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
 preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text();assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    receipt=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,receipt);finish(path,intent,verified,inventory(path/'inventory-after.json'));return
  inv=inventory(OUT/'locked-inventory.json');basis=inv['basis'];assert DB.basis()==basis
  path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
  (path/'before.edn').write_text(dumps(kp)+'\n')
  current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
  for sid,sourceq in g.QS.items():
   cq=canon(current[sid]);sq=canon(sourceq)
   # Pull now includes db/id on difficulty; immutable semantic/source IDs are compared recursively otherwise.
   if ':db/id' not in sq[':question/difficulty']:cq[':question/difficulty'].pop(':db/id',None)
   assert cq==sq,('Source changed; reclassify',sid)
  assert set(current)==set(g.QS),'New source requires validation'
  contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(contributor)==1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
  c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in g.SUPPORTED_LEVELS}
  used={coefficient(q) for q in kp[':knowledge-point/questions']};used.add(coefficient(kp[':knowledge-point/canonical-example']));records=[];added={l:0 for l in g.SUPPORTED_LEVELS}
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);assert isinstance(instances,list)
  for r in instances:v.independent(r)
  save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
  candidates=instances+[g.generate(l,seed=seed) for l in g.SUPPORTED_LEVELS for seed in range(120)]
  for r in candidates:
   level=r['question'][':question/difficulty'].split('/')[-1];fp=coefficient(r['question'])
   if added[level]<needed[level] and fp not in used:v.independent(r);records.append(r);used.add(fp);added[level]+=1
  save(path/'raw-generated.json',records)
  library=ImageLibrary(Path(ENV['EDB_MATH_ROOT']),path);published=[]
  for r in records:
   mapping={}
   for asset in r['generation']['plot_coefficients']:
    data=(ROOT/asset).read_bytes();mapped=library.store(data,asset);assert (Path(ENV['EDB_MATH_ROOT'])/mapped).read_bytes()==data;mapping[asset]=mapped
    published.append({'original':asset,'path':mapped,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
   # Base reciprocal plot is also a worked-solution asset.
   q=r['question']
   for asset in re.findall(r'!\[\]\(([^)]+)\)',q[':question/worked-solution']):
    if asset not in mapping:
     data=(ROOT/asset).read_bytes();mapping[asset]=library.store(data,asset);published.append({'original':asset,'path':mapping[asset],'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
   for f in q[':question/answer-fields']:
    for a in f[':answer-field/choices']:a[':answer/value']=mapping[a[':answer/value']]
   for old,new in mapping.items():q[':question/worked-solution']=q[':question/worked-solution'].replace(old,new)
   z=r['generation'];z['plot_coefficients']={mapping[k]:val for k,val in z['plot_coefficients'].items()};z['correct_plot']=mapping[z['correct_plot']]
  save(path/'asset-hashes.json',published);save(path/'generated.json',records)
  ids=[uuid.UUID(x) for r in records for x in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
  if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identities',basis)
  save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':v.checks(r)} for r in records])
  subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-validation.json')],check=True)
  save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts_before':c,'needed':needed,'added':added,'mathematical_coefficients':[coefficient(r['question']) for r in records],'source_questions_unchanged':True,'validation':str(OUT/'validation.json'),'generator_sha256':sha(HERE.with_suffix('.py'))})
  tx=forms(records,kp,gid)
  if not tx:
   verified={'basis_after':basis,'new_questions':0,'available_counts_after':c};save(path/'verification.json',verified);finish(path,{'generator_id':gid},verified,inv);return
  text=dumps(tx)+'\n';txpath=path/'transaction.edn'
  with txpath.open('w') as f:f.write(text);f.flush();os.fsync(f.fileno())
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=120);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;report_check(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==basis
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':basis,'expected_basis':basis,'request_key':'reciprocal-stretch-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':text,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
  save(path/'commit-intent.json',intent);receipt=DB._commit(intent,txpath,path);verified=verify(path,intent,receipt);finish(path,intent,verified,inventory(path/'inventory-after.json'))
if __name__=='__main__':main()
