"""Install independently reviewed immutable revisions, approve all bands, refill.

Uses the runner's durable transport and readback. Existing entities and immutable
packages are never overwritten. Resume an exact pending request before planning
another attempt; basis conflicts are confirmed rejections, never unknown outcomes.
"""
import argparse,hashlib,json,os,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from capture.scripts.storage import atomic_json,file_lock,read_json
from capture.scripts.database.client import StaleBasis
from scripts.generator_publish import Publisher,jsonable,digest
from scripts.generator_packages import publish_package,verify_package,build_manifest,manifest_digest,check_dependencies
from scripts.generator_pipeline import source_identity
from scripts.generator_approval import make_approval,approved_band
from scripts.generator_review import REVIEW_POLICY_VERSION
from scripts.generator_evidence import batch_sha256
from scripts.generator_refill import validate_survivors
from scripts.generator_refill_plan import validate_refill_plan

BANDS=['easy','moderate','hard']
def read(p):return json.loads(Path(p).read_text())
def save(p,x):atomic_json(Path(p),jsonable(x))
def submit(p,kp,records,package,sha,base,source,assets,expected,validator=None,expected_records=None):
 expected_records=records if expected_records is None else expected_records
 for attempt in range(1,5):
  directory=base/str(attempt)
  try:
   if not (directory/'preparation.json').exists():
    prepared=p.prepare(kp,records,package.reference,sha,directory,source_snapshot=source,assets_directory=assets,expected_registered_generator=expected,records_validator=validator)
    assert len(prepared['records'])==len(expected_records),'Fresh reviewed batch no longer wholly survives dedup; refresh inventory review'
    if records:assert prepared['records']==expected_records,'Publication preparation changed actual reviewed survivor objects'
   result=p.publish(directory);assert result['passed'];return result
  except StaleBasis:
   save(directory/'confirmed-stale.json',dict(reason='Confirmed basis rejection; exact Publisher pending request retired before reprepare'))
 raise RuntimeError('Four confirmed basis conflicts; no unconfirmed new intent')

def main(kp):
 d=H/str(kp);root=d/'package';manifest=read(root/'package.json');candidate=read(d/'package-candidate.json');review=read(d/'review/report.json');source=read(d/'source/source.json')
 assert read(H/'retirement/verification.json')['passed'];assert read(d/'publication-selection.json')['passed'];assert review['verdict']=='accepted';assert read(d/'preflight-verification.json')['passed'];assert read(d/'refill-regressions.json')['passed']
 sha=manifest_digest(build_manifest(root,manifest['entrypoint'],manifest['files'],dependencies=manifest['dependencies']));assert sha==candidate['sha256']==review['package_sha256'],'Independent review bound to different bytes'
 assert hashlib.sha256((d/'source/source.json').read_bytes()).hexdigest()==review['source_file_sha256'],'Independent review bound to different source bytes'
 for band in BANDS:
  assert batch_sha256(read(d/'publish'/band/'delivery/accepted.json'))==review['publication_batch_hashes'][band],'Independent review bound to different final survivor batch'
 for band in BANDS:
  out=d/'verification'/band;assert read(out/'refill/result.json')['status']=='passed';assert read(out/'render/rendering.json')['passed'];assert read(out/'native-report.json')['passed'];assert len(read(out/'delivery-postretirement/accepted.json'))>=5
 findings=[dict(id=x) for check in read(root/'refill-review-plan.json')['checks'] for x in check['finding_ids']];plan=validate_refill_plan(root,manifest,findings,d/'review');assert plan==candidate['refill_plan'];check_dependencies(manifest['dependencies'],sys.executable)
 p=Publisher.from_environment(source=':agent/codex');old=read(d/'capture-after-retirement/kp.json')[':knowledge-point/question-generator'][':question-generator/script'];lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock'
 with file_lock(lock,blocking=False),file_lock(H.parent/'publication.lock'):
  # Content-addressed install is additive; verify an existing install rather
  # than writing into immutable files. Dependencies are unchanged pinned runtime.
  package=publish_package(root,manifest['entrypoint'],manifest['files'],p.config.math_root,dependencies=manifest['dependencies'],expected_digest=sha);verify_package(package.directory,sha)
  registration=submit(p,kp,[],package,sha,d/'registration',source,None,old)
  fresh=p.extract_source(kp,d/'source-after-registration');assert source_identity(fresh)==source_identity(source)
  identity={**source_identity(fresh),'package_sha256':sha,'registration':package.reference}
  batches={};reports={}
  for band in BANDS:
   out=d/'publish'/band;records=read(out/'delivery/accepted.json');assets={str(f.relative_to(out/'delivery/assets')):hashlib.sha256(f.read_bytes()).hexdigest() for f in (out/'delivery/assets').rglob('*') if f.is_file()}
   batches[band]=dict(batch_hash=batch_sha256(records),assets=assets,seed=20261112,count=len(records))
   reports[band]=dict(status='passed',batch_sha256=batches[band]['batch_hash'],evidence_paths=['review/report.json',f'publish/{band}/delivery/accepted.json',f'publish/{band}/delivery/delivery.json',f'publish/{band}/refill/result.json',f'publish/{band}/refill/native-report.json',f'publish/{band}/ui-coverage.json',f'verification/{band}/render/rendering.json','refill-regressions.json'])
  engine_paths=list((ROOT/'engine/rust').rglob('*.rs'))+[ROOT/'generate/runs/current/check-engine'];engine_hash=digest({str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in engine_paths})
  binding=dict(policy_version=REVIEW_POLICY_VERSION,package_hash=sha,source_hash=digest(source),inventory_hash=digest(read(d/'capture-after-retirement/inventory.json')),engine_hash=engine_hash,assets=batches['moderate']['assets'],batch_hash=batches['moderate']['batch_hash'],effective_difficulty='moderate',initial_source_analysis_sha256=hashlib.sha256((d/'review/source-checkpoint.json').read_bytes()).hexdigest(),original_source_analysis_sha256=hashlib.sha256((ROOT/'generate/reports/lesson-quality-audit-2026-11-11/vector/source-only.json').read_bytes()).hexdigest(),refill_plan=plan,verification_batches=batches)
  approval_review=dict(review,band_verification=reports,independent_review='review/report.json',independent_review_sha256=hashlib.sha256((d/'review/report.json').read_bytes()).hexdigest(),independent_source_checkpoint='review/source-checkpoint.json');reviewpath=d/'approval-review.json';save(reviewpath,approval_review)
  approval=make_approval(identity,approval_review,binding,str(reviewpath),registration,None,REVIEW_POLICY_VERSION);approvalpath=p.config.math_root/'generators/approvals'/sha/(str(kp)+'.json')
  if approvalpath.exists():
   for band in BANDS:approved_band(read(approvalpath),identity,band,REVIEW_POLICY_VERSION)
  else:save(approvalpath,approval)
  for band in BANDS:approved_band(read(approvalpath),identity,band,REVIEW_POLICY_VERSION)
  publications={}
  for band in BANDS:
   out=d/'publish'/band;records=read(out/'delivery/accepted.json')
   def validator(actual,inventory,directory):
    assert actual==records,'Only the exact independently reviewed final survivor objects may publish'
    return validate_survivors(actual,inventory,directory,root=package.directory,manifest=read(root/'package.json'),band=band,python=sys.executable,repo_root=ROOT,environment=os.environ.copy(),expected_plan=plan)
   raw_batch=read(d/'verification'/band/'records.json');original_delivery=read(d/'verification'/band/'delivery-postretirement/accepted.json');mapping=read(out/'ui-coverage.json')['records']
   assert len(raw_batch)==len(original_delivery),'Raw-to-survivor index mapping needs explicit refresh'
   assert [original_delivery[x['source_index']] for x in mapping]==records
   raw_records=[raw_batch[x['source_index']] for x in mapping]
   publications[band]=submit(p,kp,raw_records,package,sha,d/'publication'/band,source,d/'verification'/band/'assets',package.reference,validator,expected_records=records)
   assert publications[band]['new_questions']>=5
  status=p.client.status();current=jsonable(p.read_kp(kp,d/'final-readback',status['basis']));save(d/'final-readback/kp.json',current);save(d/'final-readback/status.json',status)
  baseline=read(d/'capture-after-retirement/kp.json');oldids={q[':db/id'] for q in baseline[':knowledge-point/questions']};new=[q for q in current[':knowledge-point/questions'] if q[':db/id'] not in oldids]
  assert len(new)==sum(x['new_questions'] for x in publications.values());assert all(not q.get(':question/retired') for q in new)
  final_source=p.extract_source(kp,d/'source-final',basis=status['basis']);assert source_identity(final_source)==source_identity(source)
  for band in BANDS:approved_band(read(approvalpath),{**source_identity(final_source),'package_sha256':sha,'registration':package.reference},band,REVIEW_POLICY_VERSION)
  result=dict(passed=True,kp=kp,package_sha256=sha,registration=registration,approval_path=str(approvalpath),verified_bands=BANDS,publications=publications,new_questions=len(new),new_question_entities=[dict(entity=q[':db/id'],uuid=q[':question/id'],difficulty=q[':question/difficulty']) for q in new],retired_history_preserved=True,source_identity_matches_final=True)
  save(d/'installation-verification.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('kp',type=int);ap.add_argument('--apply',action='store_true',required=True);args=ap.parse_args();main(args.kp)
