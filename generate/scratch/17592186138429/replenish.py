"""Scoped replenishment, native preview, retained exact intent and basis readback."""
import argparse,copy,fcntl,hashlib,importlib.util,json,os,re,shutil,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('current_validation',HERE/'validate-current.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE=g.SOURCE['lineage'];SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT));JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'1b4ecede142a53921b113d1ca886ddd3d429f12f8ebabf1587f5bc8e46bc3d79'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-0ee7e7bd24d378f7'
QUERY=(HERE/'reference/initial/source-query.edn').read_text()
LOCK=ROOT/'.local/learning/requests/math/api.lock'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;save(path,x['data']);return x['data']
def read_kp(path,b):return DB.query(QUERY,[KP],path,'kp',b)[0][0]
def ordered(q):
 q=copy.deepcopy(q);q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
 for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
 return q
def normalize(q):
 result={k:str(q[k]) if k==':question/id' else q[k] for k in (':question/id',':question/problem',':question/worked-solution')};result[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);result[':question/answer-fields']=[]
 for f in q[':question/answer-fields']:
  result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]})
 return ordered(result)
def fingerprint(name,p):
 # Exclude grid/window/profile entirely, so a shifted label scale cannot create
 # a new question about the same context and plotted exact line expressions.
 import sympy as sp
 return g.digest({'context':name,'lines':[[str(sp.Rational(p[k+'0'])),str(sp.Rational(p[k+'1']))] for k in ('a','b')],'response':'horizontal coordinate'})
def used_tasks(kp):
 source=json.loads((HERE/'source-current.json').read_text())['record'];mapping={'q-45165':'cars','q-59886':'trucks','q-102519':'planes','q-237989':'tanks','e-13130':'pools'};used=set()
 params={**g.SOURCE_PARAMETERS,**v.e.PARAMS};known={}
 for path in OUT.glob('basis-*/generated.json'):
  for r in json.loads(path.read_text()):known[r['question'][':question/id']]=r
 for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
  mid=q.get(':question/math-academy-id')
  if mid in mapping:used.add(fingerprint(mapping[mid],params[mapping[mid]]))
  elif str(q[':question/id']) in known:
   r=known[str(q[':question/id'])];used.add(fingerprint(r['generation']['template'],r['generation']['parameters']))
  else:raise ValueError('Unrecognized current question; reconcile its actual graph before selection')
 return used

def publish(r):
 r=copy.deepcopy(r);assets=[]
 for role,asset in r['generation']['plot_assets'].items():
  src=Path(asset['path']);digest=sha(src);ref=f'images/{digest[:2]}/{digest}.png';dest=Path('/media/jake/SSD/EDB/math')/ref;dest.parent.mkdir(parents=True,exist_ok=True)
  if dest.exists():assert sha(dest)==digest
  else:
   temp=dest.with_suffix('.tmp-'+str(os.getpid()));shutil.copyfile(src,temp);os.replace(temp,dest)
  assert sha(dest)==digest and dest.read_bytes().startswith(b'\x89PNG')
  for key in (':question/problem',':question/worked-solution'):r['question'][key]=r['question'][key].replace('![]('+asset['reference']+')','![]('+ref+')')
  assets.append({'role':role,'source':str(src.relative_to(ROOT)),'reference':ref,'sha256':digest,'bytes':dest.stat().st_size})
 r['generation']['published_assets']=assets
 return r

def transaction(records,kp,gid):
 forms=[]
 for r in records:
  q=r['question']
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
 for entity,attr,value,tx,contributor,added in report[':edb/tx-data']:
  assert contributor==source and added,'Unexpected retraction or source'
  name=attrs[attr]
  if entity==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
  elif name!=':db/txInstant':assert entity in new and name in allowed,(entity,name)

def prepare(preview):
 inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
 path=OUT/f'basis-{b}';path.mkdir(exist_ok=True);kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
 (path/'before.edn').write_text(dumps(kp)+'\n')
 evidence=json.loads((HERE/'source-current.json').read_text())['record']
 def jsonshape(x):return json.loads(json.dumps(x,default=str))
 byid={q[':db/id']:jsonshape(q) for q in kp[':knowledge-point/questions']}
 assert all(byid[q[':db/id']]==q for q in evidence[':knowledge-point/questions']),'New or changed source evidence; reclassify'
 assert jsonshape(kp[':knowledge-point/canonical-example'])==evidence[':knowledge-point/canonical-example']
 source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
 gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
 save(HERE/'generator-identity.json',{'id':gid,'script':SCRIPT,'knowledgePoint':KP})
 jobs={j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP}
 # Observed source easy availability comes from the native inventory. New
 # classified supported bands with no rated records have zero eligible stock.
 needed={level:jobs.get(level,{}).get('missing',5 if not any(q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/'+level for q in kp[':knowledge-point/questions']) else 0) for level in ('easy','moderate','hard')}
 used=used_tasks(kp);records=[];selected={level:0 for level in needed}
 supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
 if isinstance(instances,dict):instances=[instances]
 for r in instances:
  assert r['knowledge_point']['db_id']==KP;v.check(r);level=r['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(r['generation']['template'],r['generation']['parameters'])
  if selected[level]<needed[level] and fp not in used:records.append(r);used.add(fp);selected[level]+=1
 save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances)})
 for level in needed:
  for offset in range(1000):
   if selected[level]>=needed[level]:break
   template=['trucks','planes','tanks'][offset%3] if level=='easy' else None
   r=g.generate(level,36138429+offset,template=template);v.check(r);fp=fingerprint(r['generation']['template'],r['generation']['parameters'])
   if fp in used:continue
   records.append(r);used.add(fp);selected[level]+=1
 exceptions=[{'level':level,'kind':'finite-limit','requested':needed[level],'produced':selected[level],'remaining':needed[level]-selected[level],'bounded_search':1000} for level in needed if selected[level]<needed[level]]
 ids=[uuid.UUID(r['question'][':question/id']) for r in records]
 assert not ids or not DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'generated-identities',b),'Identity collision requires reconciliation'
 registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
 assert not registered or registered[0][0][':question-generator/script']==SCRIPT
 save(path/'local-generated.json',records);save(path/'native-input.json',[v.native(r) for r in records])
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
 published=[publish(r) for r in records];save(path/'generated.json',published)
 prep={'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'generator_id':gid,'missing_by_level':needed,'selected_by_level':selected,'new_questions':len(records),'source_evidence_unchanged':True,'capability_exceptions':exceptions,'asset_hashes':[asset for r in published for asset in r['generation']['published_assets']],'distinctness':'context and reduced exact line expressions; excludes source/canonical content, seed, identity, bank, order and grid/window changes'}
 save(path/'preparation.json',prep)
 forms=transaction(published,kp,gid);assert forms,'No content changes; reconcile prior verification'
 txpath=path/'transaction.edn';txpath.write_text(dumps(forms)+'\n')
 with txpath.open('rb') as f:os.fsync(f.fileno())
 r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
 assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
 print(json.dumps({'prepared_path':str(path),'basis':b,'selected':selected}),flush=True);return path

def verify(path,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];b=report[':edb/db-after-t'];check_report(report,path/'receipt-check',intent['source_eid']);kp=read_kp(path/'readback',b)
 before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']};assert all(now[e]==q for e,q in old.items())
 exclude=(':knowledge-point/questions',':knowledge-point/question-generator');assert {k:v for k,v in before.items() if k not in exclude}=={k:v for k,v in kp.items() if k not in exclude}
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());local=json.loads((path/'local-generated.json').read_text());assert len(now)==len(old)+len(records);byuuid={str(q[':question/id']):q for q in now.values()}
 for r,lr in zip(records,local):
  q=byuuid[r['question'][':question/id']];assert ':question/math-academy-id' not in q;assert normalize(q)==ordered(r['question']);v.check(lr)
  for asset in r['generation']['published_assets']:assert sha(Path('/media/jake/SSD/EDB/math')/asset['reference'])==asset['sha256']
 assert not transaction([],kp,intent['generator_id'])
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'by_level':{level:sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records) for level in ('easy','moderate','hard')},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'only_additive_scoped_content_datoms':True,'learner_history_unchanged':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'all_assets_verified':True};save(path/'verification.json',result);return result

def finish(path,intent,verified):
 inv=inventory(path/'inventory-after.json');jobs=[j for j in inv['jobs'] if j['knowledgePoint']==KP];prep=json.loads((path/'preparation.json').read_text());exceptions=prep['capability_exceptions']
 assert not jobs or exceptions,'Supported inventory shortage remains'
 result={'outcome':'finite-limit' if exceptions else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'by_level':verified['by_level'],'supported_levels':['easy','moderate','hard'],'unsupported_levels':[],'capability_exceptions':exceptions,'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':jobs,'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'transaction.edn',path/'preview.edn',path/'inventory-after.json',path/'preparation.json',path/'native-report.json',HERE/'validation.json',HERE/'current-validation.json',HERE/'current-visual-review.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'capabilities.json')],'note':'All four source practices and canonical example preserved; easy is source-supported, moderate/hard are explicitly authored graph-reading bands. No learner/history or application facts modified.'};save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2),flush=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--commit',action='store_true');args=ap.parse_args()
 validation=json.loads((HERE/'current-validation.json').read_text());assert validation['passed'];assert all(sha(ROOT/p)==digest for p,digest in validation['hashes'].items())
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['sha256']==sha(path/'transaction.edn');assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report);finish(path,intent,verified);return
  if not args.commit:prepare(preview);return
  b=DB.basis();path=OUT/f'basis-{b}'
  if not (path/'preparation.json').exists():path=prepare(preview)
  prep=json.loads((path/'preparation.json').read_text());assert prep['basis']==DB.basis()
  inv=inventory(path/'inventory-under-commit-lock.json');assert inv['basis']==prep['basis'] and inv['lineage']==LINEAGE
  visual=json.loads((HERE/'current-visual-review.json').read_text());assert visual['passed'] and visual['prepared_basis']==prep['basis']
  for asset in visual['assets']:assert sha(ROOT/asset['path'])==asset['sha256']
  # The preview is repeated at the locked current basis; original EDN is used.
  txpath=path/'transaction.edn';r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90);(path/'preview-under-commit-lock.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/db-before-t']==prep['basis'] and pr[':edb/committed'] is False;check_report(pr,path/'commit-preview-check',prep['source_eid']);assert DB.basis()==prep['basis']
  intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':prep['source_eid'],'basis':prep['basis'],'expected_basis':prep['basis'],'request_key':'word-graphs-replenish-'+str(KP)+'-'+str(prep['basis'])+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':txpath.read_text(),'generator_id':prep['generator_id'],'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in json.loads((path/'generated.json').read_text())],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
  save(path/'commit-intent.json',intent);report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,intent,verified)
if __name__=='__main__':main()
