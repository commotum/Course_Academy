"""Publish independently accepted, exactly validated refill batches durably."""
import argparse,hashlib,json,os,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts'),str(H)]
from generator_publish import Publisher,file_lock,StaleBasis,content_fingerprint,jsonable
from generator_packages import verify_package
from generator_approval import approved_band
from generator_review import REVIEW_POLICY_VERSION
from generator_pipeline import source_identity
from generator_refill import validate_survivors
from generator_evidence import batch_sha256
from independent_math import audit as math_check

def read(p):return json.loads(Path(p).read_text())
def save(p,x):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
a=argparse.ArgumentParser();a.add_argument('--apply',action='store_true',required=True);a.parse_args()
review=read(H.parent/'review/gaussian-refill-review.json');assert review['verdict']=='accepted'
assert read(H/'native-report.json')['passed'] and read(H/'render/rendering.json')['passed']
p=Publisher.from_environment(source=':agent/codex');results=[]
for kp in [17592186096672,17592186096673]:
 D=H/str(kp);source=read(D/'source/source.json');info=read(D/'package.json');ref=info['registration'];sha=info['package_sha256'];package=p.config.math_root/ref;manifest=info['manifest'];verify_package(package.parent,sha)
 assert review['package_hashes'][str(kp)]==sha
 assert review['source_file_hashes'][str(kp)]==hashlib.sha256((D/'source/source.json').read_bytes()).hexdigest()
 approval=read(p.config.math_root/'generators/approvals'/sha/(str(kp)+'.json'));identity={**source_identity(source),'package_sha256':sha,'registration':ref}
 with file_lock(ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock'):
  for band in ['easy','moderate','hard']:
   B=D/band;records=read(B/'records.json');expected=batch_sha256(records);assert len(records)==5
   # Independent review binds each exact new batch and source, not a prior sample.
   assert review['batch_hashes'][f'{kp}/{band}']==expected
   approved_band(approval,identity,band,REVIEW_POLICY_VERSION)
   def validator(actual,inventory,directory):
    assert batch_sha256(actual)==expected and len(actual)==5,'Actual delivery differs from accepted new batch'
    for row in actual:assert not math_check(row['question'],row['question'][':question/id'])['issues']
    return validate_survivors(actual,inventory,directory,root=package.parent,manifest=manifest,band=band,python=sys.executable,repo_root=ROOT,environment=dict(os.environ),expected_plan=approval['verification_binding']['refill_plan'])
   publication=None
   with file_lock(H.parent/'publication.lock'):
    for attempt in range(1,6):
     P=B/'publication'/str(attempt)
     try:
      if not (P/'preparation.json').exists():
       prepared=p.prepare(kp,records,ref,sha,P,source_snapshot=source,expected_registered_generator=ref,records_validator=validator)
       assert prepared['new_questions']==5
      publication=p.publish(P);break
     except StaleBasis:save(P/'confirmed-stale.json',{'reason':'Confirmed writer basis rejection; exact original unknown outcomes never replaced'})
   assert publication and publication['passed'] and publication['new_questions']==5
   after=p.read_kp(kp,B/'live-readback',publication['basis_after']);stored={str(q[':question/id']):q for q in after[':knowledge-point/questions']};ids=[]
   for row in records:
    q=stored[row['question'][':question/id']];assert not q.get(':question/retired');assert content_fingerprint(q)==content_fingerprint(row['question']);ids.append(q[':db/id'])
   r={'kp':kp,'band':band,'published':5,'new_question_ids':ids,'batch_hash':expected,'publication':publication};results.append(r);save(H/'publication-results.json',{'passed':len(results)==6,'results':results,'total_new':sum(x['published'] for x in results)})
print('Published and read back30 new Gaussian questions.',flush=True)
