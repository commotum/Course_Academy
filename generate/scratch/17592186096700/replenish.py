"""Requested-KP-only additive commit, serialized with the application."""
import copy,fcntl,hashlib,importlib.util,json,os,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from db_support import DB,KP,read,dumps,loads,kw,plain
sys.path.insert(0,str(ROOT/'scripts'))
from serve_graph_explorer import database_environment
from inventory_jobs import save
spec=importlib.util.spec_from_file_location('kp_validation',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';SOURCE=':application/ca-engine'
SCRIPT=str(H.with_suffix('.py').relative_to(ROOT));OUT=H/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'e808a46bfef7dbcab773af3612bcc704949a9b6f88eefafa581f532879f895de'
LOCK=ROOT/'.local/learning/requests/math/api.lock'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):
 if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
 if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
 return str(x) if isinstance(x,uuid.UUID) else x
def inventory(native,path):
 p=subprocess.run([str(native),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=55)
 r=json.loads(p.stdout);assert r['ok'];x=r['data'];assert x['lineage']==LINEAGE;save(path,x);return x
LEVELS=("easy","moderate","hard")
NATIVE=Path((H/"reference/native-path.txt").read_text())
def source_shape(x):
 if isinstance(x,dict):return {str(k):source_shape(z) for k,z in x.items() if not (':db/ident' in x and str(k)==':db/id')}
 if isinstance(x,(list,tuple)):return sorted([source_shape(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
 return str(x) if isinstance(x,uuid.UUID) else x
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''
def tx(records,kp):
 forms=[]
 for r in records:
  q=r['question']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
   forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
  forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
 gen=kp.get(':knowledge-point/question-generator')
 if gen:
  assert str(gen[':question-generator/id'])==g.GENERATOR_ID and gen[':question-generator/script']==SCRIPT
 else:
  forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(g.GENERATOR_ID),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
 if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
 if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
 return forms

def report_checks(report,path,source):
 attrs={eid:str(a) for eid,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
 allowed={':answer/id',':answer/type',':answer/value',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':question-generator/id',':question-generator/script'}
 for e,a,value,t,s,added in report[':edb/tx-data']:
  assert added and s==source, 'Unexpected retraction or attribution'
  name=attrs[a]
  if e==KP:assert name in {':knowledge-point/questions',':knowledge-point/question-generator'}
  elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected non-scoped datom'

def normalized(q):
 x={k:str(q[k]) if k==':question/id' else q[k] for k in [':question/id',':question/problem',':question/worked-solution']};x[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);x[':question/answer-fields']=[]
 for f in q[':question/answer-fields']:
  x[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])]})
 return canonical(x)

def source_keys():
 return {g.task_key(c['template'],g.normalize_parameters('moderate',c['template'],c['parameters'],True)) for c in g.SOURCE_CASES}

def known_records():
 records={}
 for file in [OUT/'drafts.json',*OUT.glob('basis-*/selected-raw.json')]:
  if file.exists():
   records.update({r['question'][':question/id']:r for r in json.loads(file.read_text())})
 return records

def published_question(raw,path=None):
 from capture.scripts.database.images import ImageLibrary
 import copy
 library=ImageLibrary(Path('/media/jake/SSD/EDB/math'),path or OUT)
 record=copy.deepcopy(raw)
 for attr in (':question/problem',':question/worked-solution'):
  record['question'][attr]=library.text(record['question'][attr])
 return record,library.saved

def counts(kp,path,basis):
 shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
 reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
 known=known_records();out={l:set() for l in LEVELS};unknown=[]
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] in shown|reserved:continue
  level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
  if level not in out:continue
  record=known.get(str(q[':question/id']))
  if record is None:unknown.append(str(q[':question/id']));continue
  pub,_=published_question(record,path)
  assert normalized(q)==canonical(pub['question']),'Known validated content changed'
  out[level].add(record['generation']['mathematical_fingerprint'])
 result={'basis':basis,'distinct_available':{l:len(x) for l,x in out.items()},'shown_or_reserved':sorted(shown|reserved),'unrecognized_rated_questions_excluded':unknown}
 save(path/'available-counts.json',result);return result

def drafts():
 # One current native read precedes new generation; no durable EDB writes here.
 inv=inventory(NATIVE,OUT/'inventory-before-generation.json');assert DB.basis()==inv['basis']
 kp=read(inv['basis'],'before-generation');current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
 captured=json.loads((H/'source.json').read_text())['record']
 assert all(source_shape(q)==source_shape(plain(current[q[':db/id']])) for q in captured[':knowledge-point/questions'])
 val=json.loads((H/'validation.json').read_text());assert val['status']=='passed' and val['native_unresolved']==0 and all(sha(ROOT/p)==d for p,d in val['sha256'].items())
 available=counts(kp,OUT/'initial-counts',inv['basis'])['distinct_available'];needed={l:max(0,5-available[l]) for l in LEVELS}
 used=source_keys();used.update(r['generation']['mathematical_fingerprint'] for r in known_records().values() if r['question'][':question/id'] in {str(q[':question/id']) for q in current.values()})
 supplied_file=JOB.with_suffix('.generated');supplied=json.loads(supplied_file.read_text()) if supplied_file.exists() else {}
 instances=supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
 if isinstance(instances,dict):instances=[instances]
 assert isinstance(instances,list)
 records=[];rejected=[]
 if instances:
  # Every supplied instance is validated, including those excluded as duplicates.
  v.validate_records(instances,OUT/'supplied-validation')
 for r in instances:
  level=r['question'].get(':question/difficulty','').split('/')[-1];key=r['generation']['mathematical_fingerprint']
  if not r['generation']['eligible_for_learning'] or level not in LEVELS:rejected.append({'id':r['question'][':question/id'],'reason':'Evidence-only or unsupported'});continue
  if needed[level] and key not in used:records.append(r);used.add(key);needed[level]-=1
  else:rejected.append({'id':r['question'][':question/id'],'reason':'Duplicate or sufficient reserve'})
 # Execute the validated public generator; bounded seeds only discover new maths.
 for level in LEVELS:
  for offset in range(200):
   if not needed[level]:break
   template=g.TEMPLATES[0] if level=='easy' else g.TEMPLATES[offset%2]
   r=g.generate(level,421096700+offset,template=template);key=r['generation']['mathematical_fingerprint']
   if key in used:continue
   records.append(r);used.add(key);needed[level]-=1
 save(OUT/'drafts.json',records)
 if records:v.validate_records(records,OUT/'draft-validation')
 save(OUT/'supplied-status.json',{'exists':supplied_file.exists(),'instances_validated':len(instances),'excluded':rejected})
 save(H/'capabilities.json',{'generator_id':g.GENERATOR_ID,'script':SCRIPT,'version':g.VERSION,'supported_levels':list(LEVELS),'unsupported_levels':[],'exceptions':[{'level':l,'shortage':n,'reason':'Bounded 200-seed search exhausted distinct supported tasks'} for l,n in needed.items() if n],'sampling':'Finite documented domains. No seed, ID, order, translation, scale, D4 rotation/reflection or bank padding. Current source questions remain unrated.','remaining_after_draft_search':needed})
 print('Validated distinct drafts:',{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},flush=True)

def verify(report,path,intent):
 assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
 b=report[':edb/db-after-t'];report_checks(report,path/'receipt-check',intent['source_eid'])
 before=loads((path/'before.edn').read_text());after=DB.query('[:find (pull ?k '+__import__('db_support').PATTERN+') :in $ ?k :where [?k :knowledge-point/id _]]',[KP],path/'readback','kp',b)[0][0]
 old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in after[':knowledge-point/questions']}
 assert all(canonical(q)==canonical(now[e]) for e,q in old.items()),'Existing source question changed'
 excluded={':knowledge-point/questions',':knowledge-point/question-generator'}
 assert canonical({k:z for k,z in before.items() if k not in excluded})==canonical({k:z for k,z in after.items() if k not in excluded})
 gen=after[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalized(q)==canonical(r['question'])
 for asset in json.loads((path/'asset-manifest.json').read_text()).values():assert sha(Path('/media/jake/SSD/EDB/math')/asset['path'])==asset['sha256']
 assert not tx([],after),'Repeat preparation must be content no-op'
 c=counts(after,path/'readback',b)
 result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},'distinct_available_after':c['distinct_available'],'unchanged_source_questions':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'no_retractions':True,'only_requested_kp_additive_content':True,'source':SOURCE,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
 save(path/'verification.json',result);return result

def finish(path,verified,inv):
 remaining={l:max(0,5-verified['distinct_available_after'][l]) for l in LEVELS}
 caps=json.loads((H/'capabilities.json').read_text())
 result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':g.GENERATOR_ID,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'by_level':verified['by_level'],'supported_levels':list(LEVELS),'available_after':verified['distinct_available_after'],'shortage_remaining':remaining,'capability_exceptions':caps['exceptions'],'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [H/'validation.json',H/'source-replay.json',H/'classification.md',H/'template-extraction.md',H/'capabilities.json',OUT/'draft-validation/native-report.json',OUT/'draft-validation/math-report.json',path/'preparation.json',path/'asset-manifest.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json']],'note':'Current source checkbox format replayed. Easy/moderate/hard ratings are authored workload assignments. Legacy unrated originals and learner history preserved; a remaining unclassified trigger refers to retained unrated originals.'}
 save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps(result,indent=2),flush=True)

def main():
 if '--drafts-only' in sys.argv:drafts();return
 val=json.loads((H/'validation.json').read_text());assert val['status']=='passed' and val['native_unresolved']==0 and all(sha(ROOT/p)==d for p,d in val['sha256'].items())
 records=json.loads((OUT/'drafts.json').read_text());native_report=json.loads((OUT/'draft-validation/native-report.json').read_text()) if records else {};assert not records or native_report['documented_unresolved_checks']==0
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with LOCK.open('a') as lock:
  print('Acquiring application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application lock acquired',flush=True)
  for path in sorted(OUT.glob('basis-*')):
   if (path/'commit-intent.json').exists():
    intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn') and intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
    report=DB._commit(intent,path/'transaction.edn',path);verified=verify(report,path,intent);finish(path,verified,inventory(NATIVE,path/'inventory-after.json'));return
  inv=inventory(NATIVE,OUT/'inventory-before-commit.json');b=inv['basis'];assert DB.basis()==b and LINEAGE in DB.command('status')
  path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read(b,'locked-source');assert str(kp[':knowledge-point/id'])==g.KP_UUID
  captured=json.loads((H/'source.json').read_text())['record'];original={q[':db/id']:q for q in captured[':knowledge-point/questions']};current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
  assert all(source_shape(q)==source_shape(plain(current[e])) for e,q in original.items()),'Source changed; reclassify'
  assert source_shape(captured[':knowledge-point/canonical-example'])==source_shape(plain(kp[':knowledge-point/canonical-example']))
  (path/'before.edn').write_text(dumps(kp)+'\n')
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
  reg=kp.get(':knowledge-point/question-generator');by_script=DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]',[SCRIPT],path,'generator-by-script',b);assert len(by_script)<=1
  existing=reg or (by_script[0][0] if by_script else None)
  if existing:assert str(existing[':question-generator/id'])==g.GENERATOR_ID and existing[':question-generator/script']==SCRIPT,'Reuse existing identity; reconcile before change'
  available=counts(kp,path,b)['distinct_available'];needed={l:max(0,5-available[l]) for l in LEVELS};used=source_keys();known=known_records()
  used.update(known[str(q[':question/id'])]['generation']['mathematical_fingerprint'] for q in current.values() if str(q[':question/id']) in known)
  selected=[]
  for r in records:
   level=r['question'][':question/difficulty'].split('/')[-1];key=r['generation']['mathematical_fingerprint']
   if needed[level] and key not in used:selected.append(r);used.add(key);needed[level]-=1
  for attr,key,ids in [('question/id','q',[uuid.UUID(r['question'][':question/id']) for r in selected]),('answer-field/id','f',[uuid.UUID(f[':answer-field/id']) for r in selected for f in r['question'][':question/answer-fields']]),('answer/id','a',[uuid.UUID(a[':answer/id']) for r in selected for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
   if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :'+attr+' ?id]]',[ids],path,'identity-'+key,b),'Existing identity requires reconciliation'
  generator_identity=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(g.GENERATOR_ID)],path,'generator-identity',b);assert not generator_identity or len(generator_identity)==1 and generator_identity[0][0][':question-generator/script']==SCRIPT
  published=[];assets={}
  for r in selected:
   pub,manifest=published_question(r,path);published.append(pub);assets.update(manifest)
  save(path/'selected-raw.json',selected);save(path/'generated.json',published);save(path/'asset-manifest.json',assets)
  save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'available_before':available,'new_questions':len(published),'supported_shortage_remaining':needed,'distinct_tasks':len({r['generation']['mathematical_fingerprint'] for r in published}),'generator_sha256':sha(H.with_suffix('.py')),'source_unchanged':True,'lock':str(LOCK),'supplied_status':json.loads((OUT/'supplied-status.json').read_text())})
  forms=tx(published,kp)
  if not forms:
   verified={'basis_after':b,'new_questions':0,'by_level':{l:0 for l in LEVELS},'distinct_available_after':available};save(path/'verification.json',dict(verified,passed=True,no_changes=True));finish(path,verified,inv);return
  txpath=path/'transaction.edn';text=dumps(forms)+'\n'
  with txpath.open('w') as stream:stream.write(text);stream.flush();os.fsync(stream.fileno())
  result=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
  (path/'preview.edn').write_text(result.stdout);pr=loads(result.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;report_checks(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','lineage':LINEAGE,'endpoint':DB.args.endpoint,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'sha256':sha(txpath),'exact_edn':text,'request_key':'parallel-diagram-checkbox-'+str(b)+'-'+sha(txpath),'generator_id':g.GENERATOR_ID,'generator_path':SCRIPT,'generator_sha256':sha(H.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in published],'lock':str(LOCK),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()}
  save(path/'commit-intent.json',intent)
  report=DB._commit(intent,txpath,path);verified=verify(report,path,intent);finish(path,verified,inventory(NATIVE,path/'inventory-after.json'))
if __name__=='__main__':main()
