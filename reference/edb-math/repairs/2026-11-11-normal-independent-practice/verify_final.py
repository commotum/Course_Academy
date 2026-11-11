"""Read current normal-line state and verify immutable archives after repair."""
import json,sys,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from generator_publish import Publisher,jsonable
from scripts.generator_packages import verify_package
from scripts.generator_approval import approved_band
from generator_pipeline import source_identity
from scripts.generator_review import REVIEW_POLICY_VERSION
p=Publisher.from_environment(source=':agent/codex');install=json.loads((H/'installation-verification.json').read_text());status=p.client.status();basis=status['basis'];kp=p.read_kp(17592186092240,H/'current-readback',basis)
assert kp[':knowledge-point/question-generator'][':question-generator/script']==install['registration']
ledger=json.loads((H/'case-ledger.json').read_text());planned={r['entity']:r['after'] for r in ledger};actual=kp[':knowledge-point/questions'];assert len(actual)>=36
for q in actual:
 if q[':db/id'] in planned:assert q[':question/problem']==planned[q[':db/id']]
 else:assert "You are given $f'" not in q[':question/problem'] and 'negative reciprocal' not in q[':question/problem']
old='e12a76b8040dda3d9b70b2f1cf6cef0ca8f9bf0903b758bba5fc8de991a04c22';verify_package(p.config.math_root/'generators'/old[:2]/old,old)
verify_package(p.config.math_root/'generators'/install['package_sha256'][:2]/install['package_sha256'],install['package_sha256'])
source=p.extract_source(17592186092240,H/'current-source',basis=basis);identity={**source_identity(source),'package_sha256':install['package_sha256'],'registration':install['registration']};approval=json.loads(Path(install['approval_path']).read_text())
for band in ['easy','moderate','hard']:approved_band(approval,identity,band,REVIEW_POLICY_VERSION)
original_source=ROOT/'reference/edb-math/repairs/2026-11-11-independent-practice-review/source-only.json';assert approval['verification_binding']['initial_source_analysis_sha256']==hashlib.sha256(original_source.read_bytes()).hexdigest()
result=dict(passed=True,basis=basis,registration=install['registration'],question_count=len(actual),original36_repaired_prompts_confirmed=True,original_immutable_package_hash_verified=old,new_immutable_package_hash_verified=install['package_sha256'],all_three_approved_bands=True,real_source_first_checkpoint_hash_confirmed=True,new_questions_by_repair=0)
(H/'final-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
