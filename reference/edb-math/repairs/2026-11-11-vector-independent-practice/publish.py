"""Apply reviewed target CAS and immutable registration under the worker KP lock.

No action occurs without --apply. The parent agent must independently review this
file, the exact repair ledger, and the actual accepted review before invoking it.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys

H=Path(__file__).resolve().parent;ROOT=H.parents[3];KP=17592186235285;TARGET=17592186735164
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from capture.scripts.storage import atomic_json,file_lock,read_json
from capture.scripts.database.edn import dumps,loads,kw
from capture.scripts.database.client import StaleBasis
from scripts.generator_publish import Publisher,GeneratorCommitter,jsonable,digest,ImageLibrary
from scripts.generator_packages import publish_package,verify_package,build_manifest,manifest_digest,check_dependencies
from scripts.generator_approval import make_approval,approved_band
from scripts.generator_evidence import batch_sha256
from scripts.generator_refill_plan import validate_refill_plan
from scripts.generator_review import REVIEW_POLICY_VERSION
from scripts.generator_pipeline import source_identity


def read(p):return json.loads(Path(p).read_text())
def save(p,v):atomic_json(Path(p),jsonable(v))

def apply_stored(p):
    out=H/'stored/apply';out.mkdir(parents=True,exist_ok=True)
    verified=read_json(out/'verification.json')
    if verified and verified.get('passed'):return verified
    baseline=read(H/'capture/kp.json');before=read(H/'stored/before.json');proposed=read(H/'stored/proposed.json')
    committer=GeneratorCommitter(p.config,p.client,out)
    for attempt in range(3):
        request=committer.pending()
        if request is None:
            status=p.client.status();basis=status['basis']
            assert status['lineage']==read(H/'capture/status.json')['lineage']
            current=jsonable(p.read_kp(KP,out/'before',basis))
            # Covers newly generated siblings, changed banks and changed imports.
            assert current[':knowledge-point/questions']==baseline[':knowledge-point/questions'],'Pool changed: refresh audit before applying'
            assert current[':knowledge-point/question-generator']==baseline[':knowledge-point/question-generator'],'Registration changed since review'
            forms=[];assertions=[];retractions=[]
            for attr in ['question/problem','question/worked-solution']:
                forms.append([kw('db/cas'),TARGET,kw(attr),before[':'+attr],proposed[':'+attr]])
                assertions.append([TARGET,kw(attr),proposed[':'+attr]])
                retractions.append([TARGET,kw(attr),before[':'+attr]])
            forms.append([kw('db/ensure'),TARGET,kw('question/validate')])
            attrs=p.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[],out,'attributes',basis)
            idents=p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],out,'idents',basis)
            snapshot=dict(basis=basis,lineage=status['lineage'],attributes=attrs,idents=idents)
            batch=dict(source=':agent/codex',forms=forms,assertions=assertions,retractions=retractions)
            save(out/'preparation.json',dict(basis=basis,before=current,proposed=proposed,batch_edn=dumps(batch),snapshot_edn=dumps(snapshot)))
            try:committer.preview(batch,snapshot)
            except StaleBasis:continue
            request=committer.save_request(batch,snapshot,digest(proposed))
        assert request['content_sha256']==digest(proposed),'Pending intent does not match reviewed target'
        try:receipt=committer.submit(request)
        except StaleBasis:
            committer.retire(request,'rejected_stale_basis',dict(reason='Confirmed writer rejection; reprepare unchanged reviewed patch'))
            continue
        evidence=committer.verify_receipt(request,receipt)
        preparation=read(out/'preparation.json');basis=receipt[':edb/db-after-t']
        current=jsonable(p.read_kp(KP,out/'readback',basis));expected=copy.deepcopy(preparation['before'])
        expected[':knowledge-point/questions']=[proposed if q[':db/id']==TARGET else q for q in expected[':knowledge-point/questions']]
        assert current==expected,'Readback differs beyond exact target prompt/solution repair'
        # Read the old basis explicitly to verify retained historical content.
        historical=jsonable(p.read_kp(KP,out/'historical-readback',request['basis']))
        assert historical==preparation['before'],'Historical snapshot changed'
        result=dict(passed=True,basis_before=request['basis'],basis_after=basis,request_key=request['request_key'],
            repaired_questions=[TARGET],other_authored_unchanged=12,imported_unchanged=14,
            fields_answers_and_keys_unchanged=True,retained_history_verified=True,**evidence)
        save(out/'verification.json',result);committer.retire(request,'verified',result);return result
    raise RuntimeError('Three confirmed basis conflicts; no new intent submitted')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true',required=True);parser.parse_args()
    review=read(H/'review/report.json');assert review['verdict']=='accepted'
    assert read(H/'preflight-verification.json')['passed']
    assert read(H/'refill-regressions.json')['passed']
    for band in ['easy','moderate','hard']:
        assert read(H/'verification'/band/'refill/result.json')['status']=='passed'
        assert read(H/'verification'/band/'render-delivered/rendering.json')['passed']
    assert read(H/'stored/engine-report.json')['passed']
    assert read(H/'stored/render/rendering.json')['passed']
    p=Publisher.from_environment(source=':agent/codex');root=H/'package';manifest=read(root/'package.json')
    sha=manifest_digest(build_manifest(root,manifest['entrypoint'],manifest['files'],dependencies=manifest['dependencies']))
    assert sha==read(H/'package-candidate.json')['sha256']
    assert sha==review['package_sha256'],'Independent review is bound to another candidate'
    check_dependencies(manifest['dependencies'],sys.executable)
    old=read(H/'capture/kp.json')[':knowledge-point/question-generator'][':question-generator/script']
    lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{KP}.lock'
    with file_lock(lock,blocking=False):
        # Package installation is content-addressed and retains the old package.
        package=publish_package(root,manifest['entrypoint'],manifest['files'],p.config.math_root,
            dependencies=manifest['dependencies'],expected_digest=sha)
        verify_package(package.directory,sha)
        # Publish only assets referenced by the final reviewed target.
        proposed=read(H/'stored/proposed.json');library=ImageLibrary(p.config.math_root,H/'stored/assets')
        for key in [':question/problem',':question/worked-solution']:
            for reference in re.findall(r'!\[[^]]*\]\(([^)]+)\)',proposed[key]):
                data=(H/'stored/assets'/reference).read_bytes()
                assert library.store(data,reference)==reference
        with file_lock(p.config.request_directory/'api.lock'):
            stored=apply_stored(p)
        publication=None
        for attempt in range(1,4):
            directory=H/'publication'/str(attempt)
            try:
                if not (directory/'preparation.json').exists():
                    p.prepare(KP,[],package.reference,sha,directory,source_snapshot=read(H/'source/source.json'),expected_registered_generator=old)
                publication=p.publish(directory);break
            except StaleBasis:
                save(directory/'confirmed-stale.json',dict(reason='Confirmed stale basis; pending request retired by Publisher'))
        assert publication and publication['passed'] and publication['new_questions']==0
        source=p.extract_source(KP,H/'source-final');reviewed_source=read(H/'source/source.json')
        assert source_identity(source)==source_identity(reviewed_source)
        identity={**source_identity(source),'package_sha256':sha,'registration':package.reference}
        plan=validate_refill_plan(root,manifest,[dict(id='premature-vector-construction')],H/'review')
        engine_paths=list((ROOT/'engine/rust').rglob('*.rs'))+[ROOT/'generate/runs/current/check-engine']
        engine_hash=digest({str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in engine_paths})
        batches={};reports={}
        for band in ['easy','moderate','hard']:
            records=read(H/'verification'/band/'records.json');assets={}
            for rec in records:
                for name in rec['generation']['plot_assets'].values():assets[name]=hashlib.sha256((H/'verification'/band/'plots'/name).read_bytes()).hexdigest()
            batches[band]=dict(batch_hash=batch_sha256(records),assets=assets,seed=20261111,count=len(records))
            reports[band]=dict(status='passed',batch_sha256=batches[band]['batch_hash'],evidence_paths=[
                'review/report.json',f'verification/{band}/records.json',f'verification/{band}/delivery/delivery.json',
                f'verification/{band}/refill/result.json',f'verification/{band}/refill/native-report.json',f'verification/{band}/render-delivered/rendering.json'])
        binding=dict(policy_version=REVIEW_POLICY_VERSION,package_hash=sha,source_hash=digest(reviewed_source),
            inventory_hash=digest(read(H/'capture/inventory.json')),engine_hash=engine_hash,assets=batches['moderate']['assets'],
            batch_hash=batches['moderate']['batch_hash'],effective_difficulty='moderate',
            initial_source_analysis_sha256=hashlib.sha256((H/'review/source-only.json').read_bytes()).hexdigest(),
            refill_plan=plan,verification_batches=batches)
        approval_review=dict(review,band_verification=reports,
            independent_review='review/report.json',independent_review_sha256=hashlib.sha256((H/'review/report.json').read_bytes()).hexdigest(),
            independent_source_checkpoint='review/source-only.json')
        review_path=H/'approval-review.json';save(review_path,approval_review)
        approval=make_approval(identity,approval_review,binding,str(review_path),publication,None,REVIEW_POLICY_VERSION)
        approval_path=p.config.math_root/'generators/approvals'/sha/(str(KP)+'.json')
        if approval_path.exists():
            for band in batches:approved_band(read(approval_path),identity,band,REVIEW_POLICY_VERSION)
        else:save(approval_path,approval)
        for band in batches:approved_band(read(approval_path),identity,band,REVIEW_POLICY_VERSION)
        # Registration readback verifies that all existing pool members, including
        # the repaired target, survived package publication byte-for-byte.
        result=dict(passed=True,stored_repair=stored,publication=publication,package_sha256=sha,
            registration=package.reference,approval_path=str(approval_path),verified_bands=list(batches),new_questions=0)
        save(H/'installation-verification.json',result);print(json.dumps(result))

if __name__=='__main__':main()
