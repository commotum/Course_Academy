"""Publish only this KP; application api.lock spans recheck, commit and readback."""
import copy,fcntl,hashlib,itertools,json,os,re,subprocess,sys,threading,uuid
from pathlib import Path
from types import SimpleNamespace
from integration import *
import validate as v
g=v.g
from image_library import ImageLibrary
from capture.scripts.database.preview import preview_executable
OUT=D/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'ce483e11766e49c76d4c41ffd677ce167c050f5e5416dc4d7285d9515c87e270'
SOURCE_FP={
'q-125380':'segment-perpendicular','q-150018':'segment-perpendicular',
'q-125500':'["moderate","circle",1,0]','q-125504':'["moderate","circle",1,0]',
'q-125501':'["moderate","circle",2,0]','q-125502':'["moderate","ellipse",2,0]',
'q-125381':'["easy","circle",2,-1]','q-125499':'["easy","circle",3,1]',
'q-125507':'["easy","ellipse",2,-1]','q-125497':'["easy","ellipse",2,1]',
'q-125688':'rising-general-curve-opposing','q-125687':'upward-parabola-opposing','q-150013':'downward-parabola-assisting'}
def known_records():return {r['question'][':question/id']:r for path in OUT.glob('basis-*/generated.json') for r in json.loads(path.read_text())}
def task(q,known):
 mid=q.get(':question/math-academy-id')
 if mid:return SOURCE_FP[mid]
 return known[str(q[':question/id'])]['generation']['mathematical_fingerprint']
def counts(kp,b,p):
 p.mkdir(parents=True,exist_ok=True)
 shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],p,'ever-shown',b,history=True)
 reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],p,'reserved',b)
 seen={r[0] for r in shown+reserved};save(p/'scoped.json',scoped(kp,b,seen))
 subprocess.run([str(D/'reference/native/check-pool'),str(p/'scoped.json'),str(p/'native-pool.json')],check=True,capture_output=True,text=True,timeout=55)
 pool=json.loads((p/'native-pool.json').read_text());ids={e for xs in pool['available_ids_by_level'].values() for e in xs};known=known_records();tasks={l:set() for l in LEVELS};records=[];groups={}
 for q in kp[':knowledge-point/questions']:
  if q[':db/id'] not in ids:continue
  mid=q.get(':question/math-academy-id');level=str(q[':question/difficulty'][':db/ident']).split('/')[-1];assert level in LEVELS
  if mid:
   r=g.replay(mid);assert plain(q)==g.SOURCES[mid];r['question']=normalize(q)
  else:
   r=known[str(q[':question/id'])];assert normalize(q)==ordered(r['question']);v.check_record(r)
  fp=task(q,known);tasks[level].add(fp);groups.setdefault(fp,[]).append(str(q[':question/id']));records.append(r)
 v.native(records,p/'grading')
 result={'basis':b,'distinct_available':{l:len(xs) for l,xs in tasks.items()},'raw_available':{l:len(pool['available_ids_by_level'].get(l,[])) for l in LEVELS},'equivalence_groups':groups,'native_pool':pool,'shown_or_reserved':sorted(seen),'unsupported':{'hard':{'available':0,'target':5,'shortage':5,'filled':False}},'deduplication':'ellipse kind and arc sweep; easy work alignment; general source curve classes; segment rotations collapsed. Seed, uniform scale, circular rotations, noncircular aspect ratio, profile, layout, identities and choice order cannot create tasks.'};save(p/'counts.json',result);return result

def verify(p,intent,report):
 assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis'];check_report(report,p/'receipt-check',intent['source_eid'])
 b=report[':edb/db-after-t'];kp=read(p/'readback',b);before=loads((p/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']};assert all(now[e]==q for e,q in old.items())
 excluded={':knowledge-point/questions',':knowledge-point/question-generator'};assert {k:z for k,z in before.items() if k not in excluded}=={k:z for k,z in kp.items() if k not in excluded}
 records=json.loads((p/'generated.json').read_text());assert len(now)==len(old)+len(records);byid={str(q[':question/id']):q for q in now.values()}
 for r in records:
  q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q and normalize(q)==ordered(r['question']);v.check_record(r)
 gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
 assert not transaction([],kp,intent['generator_id'])
 for a in json.loads((p/'asset-manifest.json').read_text()):assert sha(Path('/media/jake/SSD/EDB/math')/a['database_path'])==a['sha256']
 after=counts(kp,b,p/'readback');result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),'unchanged_source_questions':len(old),'canonical_unchanged':True,'learner_history_unchanged':True,'only_scoped_additive_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':after};save(p/'verification.json',result);return result

def finish(p,intent,verified,inv):
 after=verified['available_counts_after'];remaining={l:max(0,5-after['distinct_available'][l]) for l in LEVELS};remaining['hard']=5
 prep=json.loads((p/'preparation.json').read_text());result={'outcome':'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'verified_commit_basis':verified['basis_after'],'lineage':LINEAGE,'new_questions':verified['new_questions'],'new_by_level':prep['new_by_level'],'supported_levels':list(LEVELS),'unsupported_levels':['hard'],'unsupported_levels_filled':False,'shortage_remaining':remaining,'available_counts_before':prep['available_counts'],'available_counts_after':after['distinct_available'],'capability_exceptions':json.loads((D/'capabilities.json').read_text())['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(f.relative_to(ROOT)) for f in (p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'asset-manifest.json',p/'generated.json',p/'inventory-after.json',D/'validation.json',D/'classification.md',D/'template-extraction.md',D/'plot-extraction.md',D/'freeze.json')],'note':'Hard shortage is a bounded capability exception, not filled inventory. Source questions and all learner history preserved; exact request and verified receipt retained. Application api.lock held through inventory/basis recheck, submit and exact-basis readback.'};save(p/'outcome.json',result);save(JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_by_level','available_counts_after','shortage_remaining')}),flush=True)

def main():
 freeze=json.loads((D/'freeze.json').read_text());assert all(sha(ROOT/f)==h for f,h in freeze['sha256'].items());assert json.loads((D/'validation.json').read_text())['passed']
 preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
 with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
  print('Waiting for application api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Application api.lock acquired',flush=True)
  for p in sorted(OUT.glob('basis-*')):
   if not (p/'commit-intent.json').exists():continue
   intent=json.loads((p/'commit-intent.json').read_text());assert intent['lineage']==LINEAGE and intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE and intent['exact_edn']==(p/'transaction.edn').read_text() and intent['sha256']==sha(p/'transaction.edn');assert intent['connection_sha256']==hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest();inventory(p/'recovery-inventory.json');report=DB._commit(intent,p/'transaction.edn',p);verified=verify(p,intent,report);finish(p,intent,verified,inventory(p/'inventory-after.json'));return
  inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b;p=OUT/('basis-'+str(b));p.mkdir(exist_ok=True);kp=read(p,b);(p/'before.edn').write_text(dumps(kp)+'\n')
  assert all(plain(q)==g.SOURCES[q[':question/math-academy-id']] for q in kp[':knowledge-point/questions']);assert plain(kp[':knowledge-point/canonical-example'])==g.KP[':knowledge-point/canonical-example']
  source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'contributor',b);assert len(source)==1
  gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP[':knowledge-point/id']),'question-generator'))
  registered=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
  if registered:
   assert len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT;gid=str(registered[0][0][':question-generator/id'])
  save(D/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or registered)})
  current=counts(kp,b,p/'current-inventory');needed={l:max(0,5-current['distinct_available'][l]) for l in LEVELS};used={task(q,known_records()) for q in kp[':knowledge-point/questions']};used.add('canonical-perpendicular-curve')
  supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[]);instances=[instances] if isinstance(instances,dict) else instances
  for r in instances:v.check_record(r)
  save(p/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances)})
  candidates=list(instances)
  for level in LEVELS:
   if needed[level]:
    for i in range(200):
     r=g.generate(level,804742+i);fp=r['generation']['mathematical_fingerprint']
     if fp not in used:candidates.append(r);break
  records=[];selected={l:0 for l in LEVELS}
  for r in candidates:
   v.check_record(r);level=r['question'][':question/difficulty'].split('/')[-1];fp=r['generation']['mathematical_fingerprint']
   if selected[level]<needed[level] and fp not in used:records.append(copy.deepcopy(r));selected[level]+=1;used.add(fp)
  # Explicitly bounded public sampler execution; iterate remaining domain only
  # if future replenishment needs more than this invocation's first candidate.
  for level in LEVELS:
   for ab,sweep,sign in itertools.product(((1,1),(2,1)),(2,3) if level=='easy' else (1,2),(-1,1)):
    if selected[level]>=needed[level]:break
    r=g.generate(level,804742,dict(a=ab[0],b=ab[1],start=0,sweep=sweep,direction=1,force_sign=sign));v.check_record(r);fp=r['generation']['mathematical_fingerprint']
    if fp not in used:records.append(r);selected[level]+=1;used.add(fp)
  assert len({r['generation']['mathematical_fingerprint'] for r in records})==len(records)
  if records:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where [?e :question/id ?id]]',[[uuid.UUID(r['question'][':question/id']) for r in records]],p,'generated-identities',b)
  save(p/'local-generated.json',records);assets=[];library=ImageLibrary(Path('/media/jake/SSD/EDB/math'))
  for r in records:
   for key in (':question/problem',':question/worked-solution'):
    for ref in re.findall(r'!\[.*?\]\((.*?)\)',r['question'][key]):
     local=ROOT/ref;data=local.read_bytes();relative=library.put_bytes(data);assert (library.math_root/relative).read_bytes()==data;r['question'][key]=r['question'][key].replace(ref,relative);assets.append({'local_path':ref,'database_path':relative,'sha256':hashlib.sha256(data).hexdigest()})
   v.check_record(r)
  save(p/'asset-manifest.json',assets);save(p/'generated.json',records);v.native(records,p/'selected-grading')
  (p/'generated.md').write_text('\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
  save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_counts':current['distinct_available'],'needed':needed,'new_by_level':selected,'supported_shortage_remaining':{l:needed[l]-selected[l] for l in LEVELS},'hard_shortage':5,'hard_filled':False,'validation_sha256':sha(D/'validation.json'),'distinctness':current['deduplication']})
  forms=transaction(records,kp,gid)
  if not forms:raise RuntimeError('No changes; use verified recovery evidence instead')
  txpath=p/'transaction.edn';tx=dumps(forms)+'\n'
  with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
  r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,capture_output=True,text=True,check=True,timeout=55);(p/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;check_report(pr,p/'preview-check',source[0][0]);assert DB.basis()==b
  intent={'database':'math','endpoint':ENV['EDB_ENDPOINT'],'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'qualitative-work-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(D.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')};save(p/'commit-intent.json',intent)
  report=DB._commit(intent,txpath,p);verified=verify(p,intent,report);finish(p,intent,verified,inventory(p/'inventory-after.json'))
if __name__=='__main__':main()
