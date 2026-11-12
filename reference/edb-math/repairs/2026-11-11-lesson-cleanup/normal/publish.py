"""Preserve approval history; publish reviewed exact normal survivors durably."""
import json,sys,hashlib,copy,shutil
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from cleanup import p,KPS,LOCK,read,save
from generator_publish import file_lock,digest,StaleBasis,jsonable
from generator_pipeline import source_identity
from scripts.generator_approval import make_approval,approved_band
from scripts.generator_review import REVIEW_POLICY_VERSION
from scripts.generator_evidence import batch_sha256
from scripts.generator_refill import validate_survivors
from scripts.generator_refill_plan import load_refill_plan,validate_refill_plan
from scripts.generator_packages import verify_package,publish_package
COMMON=H.parent/'publication.lock'
review=read(H/'review/final-review.json');assert review['verdict']=='accepted';assert read(H/'validation.json')['passed'];assert read(H/'render/rendering.json')['passed']
for kp in KPS:
 D=H/str(kp);assert review['package_hashes'][str(kp)]==read(D/'reviewed-package.json')['package_sha256']
 assert review['source_file_hashes'][str(kp)]==hashlib.sha256((D/'source/source.json').read_bytes()).hexdigest()
 for band in ['easy','moderate','hard']:
  key=f'{kp}/{band}';assert review['verification_batch_hashes'][key]==batch_sha256(read(D/'verification'/f'{band}.json'))
  assert review['publish_batch_hashes'][key]==batch_sha256(read(D/'publish'/f'{band}.json'))
  assert len(read(D/'publish'/f'{band}.json'))==5

engine_paths=list((ROOT/'engine/rust').rglob('*.rs'))+[ROOT/'generate/runs/current/check-engine'];engine_hash=digest({str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in engine_paths})
results=[]
for kp in KPS:
 D=H/str(kp);source=read(D/'source/source.json');package=read(D/'reviewed-package.json');package_hash=package['package_sha256'];script=package['registration'];P=(D/'package') if (D/'package').exists() else p.config.math_root/Path(script).parent;manifest=package['manifest']
 with file_lock(LOCK/f'kp-{kp}.lock'):
  with file_lock(COMMON):
   pending_dirs=list((D/'registration').glob('*/request.json'))+list((D/'publication').glob('*/*/request.json'))
   for pending in pending_dirs:
    try:p.publish(pending.parent)
    except StaleBasis:pass
   installed=publish_package(P,manifest['entrypoint'],manifest['files'],p.config.math_root,dependencies=manifest['dependencies'],expected_digest=package_hash);verify_package(installed.directory,package_hash)
   fresh=p.extract_source(kp,D/'source-before-publication');assert source_identity(fresh)==source_identity(source)
   current_script=fresh['registered_generator'][':question-generator/script'];assert current_script in [source['registered_generator'][':question-generator/script'],script]
   identity={**source_identity(source),'package_sha256':package_hash,'registration':script}
   # Exact pending registration requests always recover before new preparations.
   pending=list((D/'registration').glob('*/request.json'));assert len(pending)<=1
   registration=None
   if pending:registration=p.publish(pending[0].parent)
   for attempt in range(1,6):
    if registration:break
    R=D/'registration'/str(attempt)
    try:
     if not (R/'preparation.json').exists():p.prepare(kp,[],script,package_hash,R,source_snapshot=source,expected_registered_generator=current_script)
     registration=p.publish(R)
    except StaleBasis:continue
   assert registration and registration['passed']
   # Publisher's truthful no-change registration result lacks a separate boolean;
   # bind the actual current identity readback explicitly without inventing a tx.
   basis=registration['basis_after'];current=p.read_kp(kp,D/'registration-readback',basis)
   assert current[':knowledge-point/question-generator'][':question-generator/script']==script
   receipt={**registration,'generator_registration_verified':True,'registration_readback_basis':basis,'actual_registration':jsonable(current[':knowledge-point/question-generator'])}
   batches={};reports={}
   for band in ['easy','moderate','hard']:
    rows=read(D/'verification'/f'{band}.json');batches[band]=dict(batch_hash=batch_sha256(rows),assets={},seed=202611113,count=len(rows));reports[band]=dict(status='passed',batch_sha256=batches[band]['batch_hash'],evidence_paths=[str(H/'review/final-review.json'),str(H/'validation.json'),str(H/'independent-native-report.json'),str(H/'render/rendering.json'),str(D/'independent'/f'{band}.json'),str(D/'delivery'/band/'delivery.json'),str(D/'delivery'/band/'native/result.json')])
   plan,plan_binding=load_refill_plan(P,manifest)
   if kp!=17592186092240:validate_refill_plan(P,manifest,[dict(id=i) for i in plan_binding['finding_ids']],D/'review')
   else:validate_refill_plan(P,manifest,[dict(id=i) for i in plan_binding['finding_ids']],ROOT/'reference/edb-math/repairs/2026-11-11-normal-independent-practice/review')
   binding=dict(policy_version=REVIEW_POLICY_VERSION,package_hash=package_hash,source_hash=digest(source),inventory_hash=digest(read(D/'inventory/inventory.json')),engine_hash=engine_hash,assets={},batch_hash=batches['easy']['batch_hash'],effective_difficulty='easy',initial_source_analysis_sha256=hashlib.sha256((H/'review/source-only.json').read_bytes()).hexdigest(),independent_review_sha256=hashlib.sha256((H/'review/final-review.json').read_bytes()).hexdigest(),verification_batches=batches,refill_plan=plan_binding)
   approval_review={**review,'band_verification':reports};save(D/'approval-review.json',approval_review)
   approval=make_approval(identity,approval_review,binding,str(D/'approval-review.json'),receipt,None,REVIEW_POLICY_VERSION)
   A=p.config.math_root/'generators/approvals'/package_hash/f'{kp}.json'
   if A.exists():
    old=read(A)
    if old!=approval:
     backup=D/'prior-approval'/f"{digest(old)}.json";save(backup,old)
     # Preserve an adjacent archive before replacing the active pointer file.
     archive=A.parent/'history'/str(kp)/f"{digest(old)}.json";save(archive,old)
   save(A,approval)
   for band in batches:approved_band(read(A),identity,band,REVIEW_POLICY_VERSION)
   save(D/'approval.json',approval)
  # Every band keeps its own recoverable Publisher outbox; accepted final objects
  # are native graded before submit and fresh source checked inside preparation.
  publications=[]
  for band in ['easy','moderate','hard']:
   with file_lock(COMMON):
    bandroot=D/'publication'/band;pending=list(bandroot.glob('*/request.json'));assert len(pending)<=1
    result=p.publish(pending[0].parent) if pending else None
    for attempt in range(1,6):
     if result:break
     R=bandroot/str(attempt)
     def validator(rows,inventory,out):
      assert len(rows)==5 and batch_sha256(rows)==review['publish_batch_hashes'][f'{kp}/{band}'],'Exact approved five-survivor publication batch changed'
      return validate_survivors(rows,inventory,out,root=P,manifest=manifest,band=band,python=sys.executable,repo_root=ROOT,environment=p.client.environment,expected_plan=plan_binding)
     try:
      if not (R/'preparation.json').exists():p.prepare(kp,read(D/'publish'/f'{band}.json'),script,package_hash,R,source_snapshot=source,expected_registered_generator=script,records_validator=validator)
      result=p.publish(R)
     except StaleBasis:continue
    assert result and result['passed'] and result['new_questions']==5,(kp,band,result)
    publications.append(dict(band=band,**result));save(D/'publication-results.json',publications)
  results.append(dict(kp=kp,package_sha256=package_hash,new_questions=sum(r['new_questions'] for r in publications),publications=publications,approval_path=str(A),source_identity=identity));save(H/'publication-results.json',dict(passed=len(results)==3,new_questions=sum(r['new_questions'] for r in results),results=results));print(kp,'published15fresh',flush=True)
