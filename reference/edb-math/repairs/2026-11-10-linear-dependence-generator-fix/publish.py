"""Install reviewed immutable packages and register them without adding stock."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

H=Path(__file__).resolve().parent
ROOT=H.parents[3]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from scripts.generator_packages import publish_package,verify_package
from scripts.generator_publish import Publisher,digest
from generator_pipeline import source_identity
from scripts.generator_evidence import batch_sha256
from scripts.generator_approval import make_approval,approved_band
from scripts.generator_review import REVIEW_POLICY_VERSION
from scripts.generator_refill_plan import validate_refill_plan

def read(path):return json.loads(Path(path).read_text())
def save(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,prefix='.'+path.name,delete=False) as f:
        json.dump(value,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno());temporary=f.name
    os.replace(temporary,path)

assert read(H/'review/report.json')['verdict']=='accepted'
assert read(H/'review/refill-review-final.json')['verdict']=='accepted'
assert read(H/'preflight-verification.json')['passed']
assert read(H/'player-verification.json')['passed']
publisher=Publisher.from_environment(source=':agent/codex')
old=read(H.parent/'2026-11-10-linear-dependence-checkboxes/generator-follow-up.json')
engine_paths=list((ROOT/'engine/rust').rglob('*.rs'))+[ROOT/'generate/runs/current/check-engine']
engine_hash=digest({str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in engine_paths})
results=[]
for kp in [17592186119924,17592186119925]:
    root=H/'packages'/str(kp);manifest=read(root/'package.json')
    package=publish_package(root,manifest['entrypoint'],manifest['files'],publisher.config.math_root,dependencies=manifest['dependencies'])
    verify_package(package.directory,package.digest)
    installed=dict(kp=kp,package_sha256=package.digest,registration=package.reference)
    save(H/'installed'/str(kp)/'package.json',installed)
    original=next(r['registered_script'] for r in old if r['kp']==kp)
    reviewed_source=read(H/'sources'/str(kp)/'source.json')
    publication=None
    for attempt in range(1,4):
        directory=H/'publication'/str(kp)/str(attempt)
        try:
            if not (directory/'preparation.json').exists():
                publisher.prepare(kp,[],package.reference,package.digest,directory,
                    source_snapshot=reviewed_source,expected_registered_generator=original)
            publication=publisher.publish(directory)
            save(H/'installed'/str(kp)/'publication.json',publication)
            break
        except Exception as error:
            if error.__class__.__name__!='StaleBasis':raise
            # Publisher retires only a confirmed stale request. Any other
            # failure propagates with the original request files untouched.
            save(directory/'confirmed-stale.json',dict(type=type(error).__name__,reason=str(error)))
    assert publication is not None,'Repeated concurrent writes prevented registration'
    assert publication['passed'] and publication['new_questions']==0
    assert publication['generator_registration_verified']
    current_source=publisher.extract_source(kp,H/'sources-final'/str(kp))
    assert source_identity(current_source)==source_identity(reviewed_source),'Instructional source changed since review'
    identity={**source_identity(current_source),'package_sha256':package.digest,'registration':package.reference}
    findings=[dict(id=i) for i in ['subset-radio-response','redundant-none','empty-subset-support']]
    plan=validate_refill_plan(root,manifest,findings,H/'review')
    batches={}
    reports={}
    for band in ['easy','moderate','hard']:
        records=read(H/'verification'/str(kp)/(band+'.json'))
        result=read(H/'delivery'/str(kp)/band/'result.json')
        assert result['status']=='passed' and result['records']>0
        batches[band]=dict(batch_hash=batch_sha256(records),assets={},seed=20261110,count=len(records))
        reports[band]=dict(status='passed',batch_sha256=batches[band]['batch_hash'],evidence_paths=[
            'review/report.json','review/refill-review-final.json','engine-report.json','player-verification.json',
            'verification/'+str(kp)+'/'+band+'.json','delivery/'+str(kp)+'/'+band+'/result.json'])
    inventory=read(H/'delivery'/str(kp)/'inventory/inventory.json')
    binding=dict(policy_version=REVIEW_POLICY_VERSION,package_hash=package.digest,
        source_hash=digest(reviewed_source),inventory_hash=digest(inventory),engine_hash=engine_hash,
        assets={},batch_hash=batches['moderate']['batch_hash'],effective_difficulty='moderate',
        initial_source_analysis_sha256=hashlib.sha256((H/'review/source-account.md').read_bytes()).hexdigest(),
        refill_plan=plan,verification_batches=batches)
    review=dict(verdict='accepted',scope='Scoped response-format repair of an already reviewed mathematical construction.',
        independent_review='review/report.json',supplemental_independent_review='review/refill-review-final.json',
        root_checks=['native whole-question grading','actual player rendering and controls','real publication survivor validation','relocated deterministic package execution'],
        band_verification=reports)
    review_path=H/('approval-review-'+str(kp)+'.json');save(review_path,review)
    value=make_approval(identity,review,binding,str(review_path),publication,None,REVIEW_POLICY_VERSION)
    approval_path=publisher.config.math_root/'generators/approvals'/package.digest/(str(kp)+'.json')
    if approval_path.exists():
        previous=read(approval_path)
        for band in batches:approved_band(previous,identity,band,REVIEW_POLICY_VERSION)
        value=previous
    else:
        save(approval_path,value)
    for band in batches:approved_band(read(approval_path),identity,band,REVIEW_POLICY_VERSION)
    save(H/'installed'/str(kp)/'approval.json',value)
    result=dict(installed,publication=publication,approval_path=str(approval_path),verified_bands=list(batches),
        refill_plan=plan,existing_questions_unchanged=True,new_questions=0,passed=True)
    results.append(result);save(H/'installation-verification.json',dict(passed=len(results)==2,results=results))
    print(kp,'registered and approved for all three bands:',package.reference,flush=True)
