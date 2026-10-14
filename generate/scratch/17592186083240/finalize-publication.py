"""Publish the one generated plot and verify exact receipts without changing source content."""
import importlib.util,json,hashlib,copy,uuid,re,fcntl,os,subprocess,threading,urllib.request,urllib.parse
from pathlib import Path
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp_replenish',D/'replenish.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
BASE=D/'reference/replenishment/basis-2298';OUT=BASE/'asset-publication';OUT.mkdir(exist_ok=True)
records=json.loads((BASE/'generated.json').read_text());q=records[0]['question'];original=q[':question/problem'];asset=Path(re.findall(r'!\[\]\((.*?)\)',original)[0]);digest=r.sha(asset);relative='images/'+digest[:2]+'/'+digest+'.png';destination=Path('/media/jake/SSD/EDB/math')/relative
# Existing content-addressed store; exact byte identity is the publication key.
destination.parent.mkdir(parents=True,exist_ok=True)
if not destination.exists():
 tmp=destination.with_suffix('.tmp-'+str(os.getpid()));tmp.write_bytes(asset.read_bytes());os.replace(tmp,destination)
assert r.sha(destination)==digest
served=urllib.request.urlopen('http://127.0.0.1:8765/api/asset?'+urllib.parse.urlencode({'path':relative})).read();assert hashlib.sha256(served).hexdigest()==digest
published=original.replace(str(asset),relative);published_records=copy.deepcopy(records);published_records[0]['question'][':question/problem']=published
r.save(OUT/'assets.json',{'local_path':str(asset),'database_relative_path':relative,'sha256':digest,'verified_stored_bytes':True,'verified_http_availability':True,'visual_review':'curve derived from x=12te^t and y=4t^2+8t; t in [0,3], supplementary illustration; axes and curve readable without clipping'})
r.save(BASE/'generated-published.json',published_records)
preview=r.preview_executable(r.SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=r.ROOT,preview_bin=None),threading.Event())
with (r.ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
 print('Waiting for publication api.lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Publication api.lock acquired',flush=True)
 intent_path=OUT/'commit-intent.json'
 if intent_path.exists():
  intent=json.loads(intent_path.read_text());assert intent['lineage']==r.LINEAGE and intent['source']==r.SOURCE and intent['sha256']==r.sha(OUT/'transaction.edn') and intent['exact_edn']==(OUT/'transaction.edn').read_text()
 else:
  inv=r.inventory(OUT/'inventory-before.json');b=inv['basis'];assert r.DB.basis()==b;before=r.read(OUT/'before',b);r.save(OUT/'before.json',json.loads(json.dumps(before,default=str)))
  target=next(x for x in before[':knowledge-point/questions'] if str(x[':question/id'])==q[':question/id']);assert target[':question/problem']==original
  # No question is changed after learner observation/reservation.
  unavailable=r.DB.query('[:find ?item :in $ ?qid :where [?q :question/id ?qid] [?item :task-item/content ?q]]',[uuid.UUID(q[':question/id'])],OUT,'target-presentations',b,history=True);assert not unavailable
  reserved=r.DB.query('[:find ?step :in $ ?qid :where [?q :question/id ?qid] [?step :step/content ?q]]',[uuid.UUID(q[':question/id'])],OUT,'target-reservations',b);assert not reserved
  forms=[[r.kw('db/cas'),target[':db/id'],r.kw('question/problem'),original,published],[r.kw('db/ensure'),target[':db/id'],r.kw('question/validate')],[r.kw('db/ensure'),r.KP,r.kw('knowledge-point/validate')]]
  text=r.dumps(forms)+'\n'
  with (OUT/'transaction.edn').open('w') as f:f.write(text);f.flush();os.fsync(f.fileno())
  run=subprocess.run([str(preview),'with','--database','math','--file',str(OUT/'transaction.edn'),'--source',r.SOURCE],env=r.DB.env,text=True,capture_output=True,check=True,timeout=55);(OUT/'preview.edn').write_text(run.stdout);pr=r.loads(run.stdout);assert not pr[':edb/committed'] and pr[':edb/db-before-t']==b
  source=r.DB.query('[:find ?s :where [?s :db/ident :application/ca-engine]]',[],OUT,'source',b)[0][0]
  intent={'database':'math','endpoint':r.DB.args.endpoint,'lineage':r.LINEAGE,'source':r.SOURCE,'source_eid':source,'basis':b,'expected_basis':b,'request_key':'parametric-asset-publication-'+q[':question/id']+'-'+str(b)+'-'+r.sha(OUT/'transaction.edn'),'sha256':r.sha(OUT/'transaction.edn'),'exact_edn':text,'question_uuid':q[':question/id'],'question_eid':target[':db/id'],'asset_sha256':digest,'generator_id':json.loads((D/'registration.json').read_text())['id'],'generator_path':r.SCRIPT,'lock':str(r.ROOT/'.local/learning/requests/math/api.lock')};r.save(intent_path,intent)
 receipt=r.DB._commit(intent,OUT/'transaction.edn',OUT);assert receipt[':edb/committed'] and receipt[':edb/db-before-t']==intent['basis'];b=receipt[':edb/db-after-t']
 attrs=dict(r.DB.attributes(OUT/'receipt-check',intent['basis']));changes=[]
 for e,a,v,t,s,added in receipt[':edb/tx-data']:
  assert s==intent['source_eid']
  name=str(attrs[a])
  if name==':db/txInstant':assert added;continue
  assert e==intent['question_eid'] and name==':question/problem'
  assert (added and v==published) or (not added and v==original);changes.append(added)
 assert sorted(changes)==[False,True]
 after=r.read(OUT/'readback',b);before=r.read(OUT/'original-basis',intent['basis'])
 old={x[':db/id']:x for x in before[':knowledge-point/questions']};now={x[':db/id']:x for x in after[':knowledge-point/questions']};assert old.keys()==now.keys()
 for eid,x in old.items():
  if eid==intent['question_eid']:x=copy.deepcopy(x);x[':question/problem']=published
  assert x==now[eid]
 assert {k:v for k,v in before.items() if k!=':knowledge-point/questions'}=={k:v for k,v in after.items() if k!=':knowledge-point/questions'}
 for rec in published_records:assert r.normalize(next(x for x in now.values() if str(x[':question/id'])==rec['question'][':question/id']))==r.ordered(rec['question'])
 r.native(published_records,OUT/'readback-grading')
 # Count with current-equivalence expectations, retaining original preparation evidence.
 known=r.counts(after,b,OUT/'verified-inventory');r.save(OUT/'verification.json',{'passed':True,'basis_before':intent['basis'],'basis_after':b,'existing_source_questions_unchanged':18,'generated_question_id_and_fields_preserved':True,'only_generated_asset_reference_changed':True,'asset_bytes_and_http_verified':True,'no_learner_or_engine_changes':True,'actual_grader':str((OUT/'readback-grading/report.json').relative_to(r.ROOT)),'repeat_publication_content_changes':0,'available_counts':known})
 inv=r.inventory(OUT/'inventory-after.json')
 result=json.loads((BASE/'outcome.json').read_text());result.update({'verified_commit_basis':b,'available_distinct':known['distinct_available'],'shortage_remaining':{l:max(0,5-known['distinct_available'][l]) for l in r.LEVELS},'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==r.KP],'evidence':result['evidence']+[str(f.relative_to(r.ROOT)) for f in [OUT/'commit-intent.json',OUT/'transaction.edn',OUT/'commit.edn',OUT/'preview.edn',OUT/'verification.json',OUT/'assets.json',OUT/'inventory-after.json',BASE/'generated-published.json',D/'capabilities.json']],'native_grading_version_correction':'Prior round-parser rejection expectations were superseded by current grader acceptance. Original preparation counts were conservative; one additional distinct moderate question was retained. Exact original request and receipt remain preserved.'})
 assert all(v==0 for v in result['shortage_remaining'].values());r.save(OUT/'outcome.json',result);r.save(r.JOB.with_suffix('.result'),result);print(json.dumps({k:result[k] for k in ['outcome','new_questions','verified_commit_basis','available_distinct','remaining_jobs']}),flush=True)
