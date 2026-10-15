"""Additive KP-only registration/replenishment using the application's EDB path."""
import fcntl,hashlib,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from capture.scripts.database.preview import preview_executable
from context import ROOT,HERE,DB,ENV,KP,LEARNER,inventory
from validate import g,check_question,engine_checks,normalized
from edn import dumps,loads,kw
from database import StaleBasis
from inventory_jobs import save
SOURCE=':application/ca-engine'
LINEAGE=g.SOURCE['lineage']
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'8111a0b6c90e48c15aa9b31f4018fab8b15f52df9fdc3a6e2857fdf5b5280340'
LOCK=ROOT/'.local/learning/requests/math/api.lock'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
LEVELS=('easy','moderate','hard')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read_kp(path,basis):return DB.query((HERE/'reference/source-query.edn').read_text(),[KP],path,'kp',basis)[0][0]
def canonical(v):
 if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items() if str(k)!=':db/id'}
 if isinstance(v,(list,tuple)):return sorted([canonical(x) for x in v],key=lambda x:json.dumps(x,sort_keys=True))
 return str(v) if isinstance(v,uuid.UUID) else v

def native(records,path):
 save(path/'native-input.json',[{'label':str(q[':question/id']),'record':{'question':normalized(q),'knowledge_point':{'title':g.TITLE},'generation':{'template':'live-validated'}},'checks':engine_checks(q)} for q in records])
 subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True,timeout=55)
 report=json.loads((path/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
 return report

def counts(kp,basis,path):
 query=(HERE/'reference/usage-query.edn').read_text()
 used={r[0] for r in DB.query(query,[KP,LEARNER],path,'usage',basis)}
 used.update(r[0] for r in DB.query(query,[KP,LEARNER],path,'historical-usage',basis,history=True))
 pools={l:set() for l in LEVELS};excluded=[];valid=[]
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] in used:excluded.append({'question':q[':db/id'],'reason':'presented/reserved including retained history'});continue
  try:result=check_question(q)
  except (AssertionError,KeyError,ValueError,IndexError) as e:
   excluded.append({'question':q[':db/id'],'reason':'failed independent source/displayed mathematics check: '+str(e)});continue
  pools[result['level']].add(result['signature']);valid.append(q)
 native(valid,path)
 result={'basis':basis,'available_by_level':{l:len(pools[l]) for l in LEVELS},'unavailable_including_history':sorted(used),'excluded':excluded,'canonical_excluded':True,'distinctness':'expanded divergence and moderate rectangle bounds; disregard identity/seed/order and nonassessed easy geometry'}
 save(path/'available-counts.json',result)
 return result

def forms(records,kp,gid):
 tx=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    tx.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   tx.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  tx.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:
  assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
 else:
  tx.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:tx.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if tx:tx.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return tx

def datom_audit(report,path,source_eid):
 attrs=dict(DB.attributes(path,report[':edb/db-before-t']));new=set(report[':edb/tempids'].values());allowed={':question/'+s for s in ('id','problem','worked-solution','difficulty','answer-fields')}|{':answer-field/'+s for s in ('id','key','type','choices','correct')}|{':answer/'+s for s in ('id','type','value')}|{':question-generator/id',':question-generator/script'}
 for e,a,v,tx,s,added in report[':edb/tx-data']:
  assert s==source_eid and added,'Unexpected source or retraction'
  name=str(attrs[a])
  if e==KP:assert name in (':knowledge-point/question-generator',':knowledge-point/questions')
  elif name!=':db/txInstant':assert e in new and name in allowed
 return {'datoms':len(report[':edb/tx-data']),'all_additive':True,'requested_kp_and_new_content_only':True,'learner_history_untouched':True,'source_attribution':SOURCE}

def finish(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
 assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
 audit=datom_audit(report,path/'datom-audit',intent['source_eid']);after=report[':edb/db-after-t']
 kp=read_kp(path/'readback',after);before=loads((path/'before.edn').read_text())
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 assert all(canonical(now[e])==canonical(q) for e,q in old.items())
 omit={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert canonical({k:v for k,v in kp.items() if k not in omit})==canonical({k:v for k,v in before.items() if k not in omit})
 records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  assert canonical(normalized(byid[r['question'][':question/id']]))==canonical(normalized(r['question']))
  check_question(byid[r['question'][':question/id']],True)
 assert len(now)==len(old)+len(records)
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 assert not forms([],kp,intent['generator_id'])
 available=counts(kp,after,path/'readback')
 verification={'passed':True,'basis_before':intent['basis'],'basis_after':after,'generator_registration_verified':True,'source_questions_unchanged':len(old),'canonical_example_unchanged':True,'audit':audit,'repeat_preparation_content_changes':0,'new_questions':len(records),'available_counts':available}
 save(path/'verification.json',verification)
 inv=inventory();assert inv['lineage']==LINEAGE;save(path/'inventory-after.json',inv)
 supported_shortages={l:max(0,5-available['available_by_level'][l]) for l in g.LEVELS}
 result={'outcome':'finite-limit' if any(supported_shortages.values()) else 'generated','knowledgePoint':KP,'topic':17592186050694,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'lineage':LINEAGE,'preparation_basis':intent['basis'],'verified_commit_basis':after,'new_questions':len(records),'reason':'Current inventory is already sufficient in supported bands; validated generator registered without duplicating source questions.' if not records else 'Validated distinct replenishment and generator registration committed.','supported_levels':list(g.LEVELS),'unsupported_levels':['hard'],'unsupported_levels_filled':False,'available_by_level':available['available_by_level'],'shortage_remaining':{**supported_shortages,'hard':5},'capability_exceptions':json.loads((HERE/'capabilities.json').read_text())['exceptions'],'finite_limits':json.loads((HERE/'capabilities.json').read_text())['finite_limits'],'source_questions_and_learner_history_preserved':True,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'preview.edn',path/'commit.edn',path/'generated.json',path/'preparation.json',path/'inventory-after.json',HERE/'validation.json',HERE/'source-replay.json',HERE/'template-components.json',HERE/'asset-verification.json',HERE/'capabilities.json',HERE/'freeze.json')]}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
 print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','available_by_level','shortage_remaining')},indent=2),flush=True)
 return result

def prepare(preview):
 inv=inventory();assert inv['lineage']==LINEAGE;save(OUT/'inventory-under-lock.json',inv)
 # Exact retained requests precede new preparation. A committed receipt is reused.
 for p in sorted(OUT.glob('basis-*')):
  if (p/'commit-intent.json').exists():
   intent=json.loads((p/'commit-intent.json').read_text())
   assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
   assert intent['exact_edn']==(p/'transaction.edn').read_text() and intent['sha256']==sha(p/'transaction.edn')
   assert intent['generator_sha256']==sha(HERE.with_suffix('.py'))
   assert intent['connection_sha256']==hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
   return finish(p,intent,DB._commit(intent,p/'transaction.edn',p))
 basis=inv['basis'];assert DB.basis()==basis
 path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True)
 kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
 (path/'before.edn').write_text(dumps(kp)+'\n')
 current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
 assert all(canonical(current[sid])==canonical(q) for sid,q in g.SOURCES.items()),'Source evidence changed; reclassify'
 assert canonical(kp[':knowledge-point/canonical-example'])==canonical(g.SOURCE['record'][':knowledge-point/canonical-example'])
 contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(contributor)==1
 gen=kp.get(':knowledge-point/question-generator')
 registered=DB.query('[:find (pull ?g [*]) :in $ ?path :where [?g :question-generator/script ?path]]',[SCRIPT],path,'generator-by-path',basis);assert len(registered)<=1
 identity_file=HERE/'generator-id.json';identity=json.loads(identity_file.read_text()) if identity_file.exists() else {}
 gid=str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else identity.get('id',g.GENERATOR_UUID)
 assert not identity or identity['id']==gid
 save(identity_file,{'id':gid,'script':SCRIPT,'knowledge_point':KP})
 collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',basis)
 assert not collision or collision[0][0][':question-generator/script']==SCRIPT
 available=counts(kp,basis,path)
 needed={l:max(0,5-available['available_by_level'][l]) for l in g.LEVELS};added={l:0 for l in g.LEVELS}
 used={check_question(q)['signature'] for q in kp[':knowledge-point/questions']}
 # Canonical repeated-integral task is excluded too, using its known components
 # P=7x²y^6+x³, Q=-2xy^7+4x²y, bounds [-1,1]x[-3,0].
 used.add(g.digest(['moderate','7*x**2',[-1,1,-3,0]]))
 records=[]
 def consider(r):
  assert r['knowledge_point']['db_id']==KP and r['knowledge_point']['id']==g.KP_UUID
  meta=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1];assert level in g.LEVELS
  replay=g.generate(level,meta['seed'],meta['template'],meta['parameters'],meta['profile'])
  assert normalized(r['question'])==normalized(replay['question'])
  signature=check_question(r['question'],True)['signature'];assert signature==meta['mathematical_fingerprint']
  if added[level]<needed[level] and signature not in used:records.append(r);used.add(signature);added[level]+=1
 supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
 instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
 assert isinstance(instances,list)
 for r in instances:consider(r)
 seed=int(JOB.name[:8],16)
 for level in g.LEVELS:
  candidates=g.catalog(level);g.random.Random(seed).shuffle(candidates)
  for sid,s in candidates:
   if added[level]>=needed[level]:break
   consider(g.generate(level,seed,sid,{'scale':s}))
 save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generatorError':supplied.get('generatorError')})
 save(path/'generated.json',records);native([r['question'] for r in records],path/'selected') if records else None
 for attr,values in [('question/id',[r['question'][':question/id'] for r in records]),('answer-field/id',[f[':answer-field/id'] for r in records for f in r['question'][':question/answer-fields']]),('answer/id',[a[':answer/id'] for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
  if values:
   assert len(values)==len(set(values))
   assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[[uuid.UUID(s) for s in values]],path/'identity-check',attr.replace('/','-'),basis)
 tx=forms(records,kp,gid)
 save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_version':g.VERSION,'needed':needed,'new_by_level':added,'current_inventory':available,'original_job':json.loads(JOB.with_suffix('.json').read_text()),'source_comparison':'all ten complete source questions and canonical unchanged','asset_hashes':json.loads((HERE/'asset-verification.json').read_text()),'remaining_supported_shortages':{l:needed[l]-added[l] for l in g.LEVELS}})
 assert tx,'Already registered; recover the original receipt instead of writing an empty transaction'
 txpath=path/'transaction.edn';text=dumps(tx)+'\n'
 with txpath.open('w') as stream:stream.write(text);stream.flush();os.fsync(stream.fileno())
 result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,capture_output=True,text=True,check=True,timeout=55)
 (path/'preview.edn').write_text(result.stdout);report=loads(result.stdout);assert report[':edb/committed'] is False
 if report[':edb/db-before-t']!=basis or DB.basis()!=basis:raise StaleBasis('Confirmed basis changed before submission')
 datom_audit(report,path/'preview-audit',contributor[0][0])
 intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':basis,'expected_basis':basis,'request_key':'kp-flux-generator-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':text,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK)}
 save(path/'commit-intent.json',intent)
 return finish(path,intent,DB._commit(intent,txpath,path))

def main():
 assert json.loads((HERE/'validation.json').read_text())['pass']
 freeze=json.loads((HERE/'freeze.json').read_text())
 for rel,digest in freeze['artifacts'].items():assert sha(ROOT/rel)==digest,'Frozen artifact changed: '+rel
 # Build and check runtime before acquiring the application writer lock.
 from serve_graph_explorer import build_learning
 build_learning(ROOT.parent/'EDB')
 libs=json.loads((HERE/'validation.json').read_text())['native_build']
 assert all(sha(ROOT/v['path'])==v['sha256'] for v in libs.values()),'Native application changed; repeat validation'
 preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock held: fresh inventory, basis, preview, submit and exact readback',flush=True)
  for attempt in range(3):
   try:return prepare(preview)
   except StaleBasis:
    if attempt==2:raise
    print('Confirmed stale-basis rejection; preparing against a fresh captured inventory',flush=True)
if __name__=='__main__':main()
