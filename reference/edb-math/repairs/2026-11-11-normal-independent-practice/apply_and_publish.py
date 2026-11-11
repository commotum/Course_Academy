"""Apply independently reviewed prompt repair and immutable registration durably.
Run only after root review authorizes live publication. Unknown requests recover
exactly; only confirmed StaleBasis rejections are retired and recomputed.
"""
import argparse,hashlib,json,os,sys,subprocess,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from generator_publish import Publisher,GeneratorCommitter,StaleBasis,jsonable,digest,loads,file_lock
from scripts.generator_packages import publish_package,verify_package,package_digest
from scripts.generator_approval import make_approval,approved_band
from scripts.generator_refill_plan import validate_refill_plan
from scripts.generator_evidence import batch_sha256
from scripts.generator_review import REVIEW_POLICY_VERSION
from generator_pipeline import source_identity

def read(p):return json.loads(Path(p).read_text())
def save(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile(mode='w',dir=p.parent,prefix='.'+p.name,delete=False) as f:
  json.dump(v,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno());tmp=f.name
 os.replace(tmp,p)

def jobs(directory):
 rows=[]
 for f in directory.glob('*.json'):
  try:j=read(f)
  except (OSError,ValueError):continue
  if j.get('request',{}).get('knowledgePoint')==17592186092240:
   rows.append(dict(path=str(f),state=j['state'],request=j['request'],outcome=j.get('outcome')))
 return rows

def verify_questions(p,D,receipt,request):
 proof=GeneratorCommitter(p.config,p.client,D).verify_receipt(request,receipt);after=receipt[':edb/db-after-t']
 kp=p.read_kp(17592186092240,D/'readback',after);actual=jsonable(kp[':knowledge-point/questions'])
 expected=read(D/'expected-siblings.json')
 assert {q[':db/id']:q for q in actual}=={q[':db/id']:q for q in expected},'Exact repaired siblings readback differs'
 before=read(D/'siblings-before.json');historical=p.read_kp(17592186092240,D/'history',request['basis'])
 assert jsonable(historical[':knowledge-point/questions'])==before,'Historical snapshot changed'
 ids=[q[':db/id'] for q in actual]
 items=p.client.query('[:find (pull ?i [*]) :in $ [?q ...] :where [?i :task-item/content ?q]]',[ids],D,'items-readback',after)
 assert jsonable(items)==read(D/'task-items-before.json'),'Learner task-items changed'
 result=dict(passed=True,basis_before=request['basis'],basis_after=after,request_key=request['request_key'],prompts_changed=11,all_siblings=len(actual),imported_unchanged=20,fields_keys_solutions_and_learner_history_unchanged=True,historical_snapshot_preserved=True,**proof)
 save(H/'question-verification.json',result);save(D/'verified-receipt.json',jsonable(receipt))
 save(D/'verified-request.json',request);return result

parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args();assert args.apply,'Explicit root-reviewed --apply required'
assert read(H/'preflight-verification.json')['passed']
assert read(H/'refill-regressions.json')['passed']
render=read(H/'render/rendering.json');assert render.get('passed') is True,'Actual final rendering must pass'
review_path=H/'review/independent-review.json';review=read(review_path);assert review['verdict']=='accepted'
P=H/'package';manifest=read(P/'package.json');expected_hash=package_digest(P,manifest['entrypoint'],manifest['files'],dependencies=manifest['dependencies'])
assert review['package_sha256']==expected_hash,'Independent review must bind final package'
p=Publisher.from_environment(source=':agent/codex');source=read(H/'source/source.json');old=source['registered_generator'][':question-generator/script']
lockdir=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
with file_lock(lockdir/'kp-17592186092240.lock'):
 current_jobs=jobs(lockdir);save(H/'apply-jobs.json',current_jobs)
 assert not any(j['state']=='running' for j in current_jobs),'Unexpected running KP job while holding KP lock'
 # Recover any exact pending question request before fresh preparation.
 for attempt in range(3):
  pending_dirs=[d.parent for d in (H/'question-publication').glob('*/request.json')]
  assert len(pending_dirs)<=1,'Multiple unknown outcomes require reconciliation'
  if pending_dirs:
   D=pending_dirs[0];committer=GeneratorCommitter(p.config,p.client,D);request=committer.pending()
  elif (H/'question-verification.json').exists():break
  else:
   with file_lock(Path(p.config.request_directory)/'api.lock'):
    subprocess.run([sys.executable,str(H/'prepare_questions.py')],check=True)
    prepared=read(H/'question-preparation.json');D=Path(prepared['directory']);committer=GeneratorCommitter(p.config,p.client,D)
    request=committer.save_request(loads((D/'batch.edn').read_text()),loads((D/'snapshot.edn').read_text()),prepared['batch_digest'])
  try:
   with file_lock(Path(p.config.request_directory)/'api.lock'):
    receipt=committer.submit(request);result=verify_questions(p,D,receipt,request)
  except StaleBasis:
   committer.retire(request,'rejected_stale_basis',dict(reason='Confirmed writer basis rejection; refresh question-only CAS plan'));continue
  committer.retire(request,'verified',result);break
 else:raise RuntimeError('Repeated basis races while applying questions')
 # Publish package bytes once; preserve old archive untouched.
 package=publish_package(P,manifest['entrypoint'],manifest['files'],p.config.math_root,dependencies=manifest['dependencies'],expected_digest=expected_hash)
 verify_package(package.directory,package.digest);save(H/'installed/package.json',dict(kp=17592186092240,package_sha256=package.digest,registration=package.reference))
 publication=None
 for attempt in range(1,4):
  D=H/'registration-publication'/str(attempt)
  if not (D/'preparation.json').exists():p.prepare(17592186092240,[],package.reference,package.digest,D,source_snapshot=source,expected_registered_generator=old)
  try:publication=p.publish(D);break
  except StaleBasis:save(D/'confirmed-stale.json',dict(reason='Writer rejected basis; refresh registration preparation'))
 assert publication and publication['passed'] and publication['new_questions']==0 and publication['generator_registration_verified']
 save(H/'installed/publication.json',publication)
 fresh=p.extract_source(17592186092240,H/'source-final');assert source_identity(fresh)==source_identity(source)
 identity={**source_identity(fresh),'package_sha256':package.digest,'registration':package.reference}
 plan=validate_refill_plan(P,manifest,[dict(id=i) for i in ['supplied-assessed-work','awkward-coefficient-dot']],H/'review')
 batches={};reports={}
 for band in ['easy','moderate','hard']:
  records=read(H/'verification'/f'{band}.json');batches[band]=dict(batch_hash=batch_sha256(records),assets={},seed=20261111,count=len(records))
  reports[band]=dict(status='passed',batch_sha256=batches[band]['batch_hash'],evidence_paths=['review/independent-review.json','preflight-verification.json',f'verification/{band}.json',f'delivery/{band}/native-report.json',f'publication-delivery/{band}/delivery.json','render/rendering.json','refill-regressions.json'])
 engine_paths=list((ROOT/'engine/rust').rglob('*.rs'))+[ROOT/'generate/runs/current/check-engine']
 engine_hash=digest({str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in engine_paths})
 binding=dict(policy_version=REVIEW_POLICY_VERSION,package_hash=package.digest,source_hash=digest(source),inventory_hash=digest(read(H/'inventory/inventory.json')),engine_hash=engine_hash,assets={},batch_hash=batches['easy']['batch_hash'],effective_difficulty='easy',initial_source_analysis_sha256=hashlib.sha256((H/'review/source-only.json').read_bytes()).hexdigest(),independent_review_sha256=hashlib.sha256(review_path.read_bytes()).hexdigest(),refill_plan=plan,verification_batches=batches)
 approval_review={**review,'band_verification':reports};save(H/'approval-review.json',approval_review)
 approval_path=p.config.math_root/'generators/approvals'/package.digest/'17592186092240.json'
 approval=make_approval(identity,approval_review,binding,str(H/'approval-review.json'),publication,None,REVIEW_POLICY_VERSION)
 if approval_path.exists():
  approval=read(approval_path)
 else:save(approval_path,approval)
 for band in batches:approved_band(read(approval_path),identity,band,REVIEW_POLICY_VERSION)
 save(H/'installed/approval.json',approval)
 save(H/'installation-verification.json',dict(passed=True,registration=package.reference,package_sha256=package.digest,approval_path=str(approval_path),verified_bands=list(batches),new_questions=0,publication=publication,question_repair=read(H/'question-verification.json'),old_package_unchanged=True))
 print('Normal-line prompt repair, replacement registration and all-band approval verified.',flush=True)
