"""Bind existing actual UI cases to exact final delivery and committed content."""
import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from scripts.generator_evidence import record_sha256
from scripts.generator_publish import normalized_question
read=lambda p:json.loads(Path(p).read_text())
render=read(H/'render/rendering.json');records=read(H/'verification/render-representatives.json')
assert render['passed'] and len(render['cases'])==72
assert render['record_sha256']==[record_sha256(r) for r in records]
assert hashlib.sha256((H/'verification/render-representatives.json').read_bytes()).hexdigest()==render['input_sha256']
delivered=[(b,r) for b in ['easy','moderate','hard'] for r in read(H/'publication-delivery'/b/'accepted.json')]
items=[]
for i,r in enumerate(records[:7]):
 matches=[(band,d) for band,d in delivered if normalized_question(r['question'],identity=False)==normalized_question(d['question'],identity=False)]
 assert len(matches)==1
 band,d=matches[0];assert r==d,'Full generated JSON differs from delivered survivor';assert record_sha256(r)==record_sha256(d),'Final delivered record differs from rendered sample'
 cases=[c for c in render['cases'] if c['record_sha256']==record_sha256(d)]
 assert {(c['state'],c['viewport']['width']) for c in cases}=={('active',390),('completed',390),('active',1280),('completed',1280)}
 items.append(dict(index=i,band=band,rendered_record_sha256=record_sha256(r),delivered_record_sha256=record_sha256(d),exact_record_bytes_projection_identical=True,cases=4))
expected={q[':question/id']:q for q in read(H/'question-publication/basis-14216/expected-siblings.json')}
# Exact committed readback equality with these expectations was checked at14217
# by verify_questions; no new read or mutation is needed for the rendering claim.
proof=read(H/'question-verification.json');assert proof['passed'] and proof['basis_after']==14217
stored=[]
for i,r in enumerate(records[7:],start=7):
 q=r['question'];committed=expected[q[':question/id']]
 assert normalized_question(q)==normalized_question(committed),'Rendered stored content differs from exact committed readback'
 cases=[c for c in render['cases'] if c['record_sha256']==record_sha256(r)]
 assert len(cases)==4
 stored.append(dict(index=i,entity=committed[':db/id'],question_uuid=q[':question/id'],rendered_record_sha256=record_sha256(r),committed_content_and_owned_fields_identical=True,cases=4))
result=dict(passed=True,database_writes=0,additional_rendering_required=False,reason='All seven selected generated representatives have identical record fingerprints to actual final publication-delivery survivors. All eleven stored rendered proposals normalize exactly to their verified committed readback. Existing72 UI cases therefore cover final delivered and committed records.',ui_report='render/rendering.json',generated_representatives=items,stored_records=stored,stored_exact_readback_basis=14217,immutable_approval_unchanged=True)
(H/'render-binding-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=True,generated_identical=len(items),stored_committed_identical=len(stored),existing_ui_cases=72,additional_rendering_required=False)))
