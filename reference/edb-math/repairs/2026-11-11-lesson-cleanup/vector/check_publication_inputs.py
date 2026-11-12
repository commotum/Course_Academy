"""Preserve the double-localization failure and check exact runner input/output."""
import copy,json,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from scripts.generator_publish import prepare_records,content_fingerprint
from scripts.generator_evidence import batch_sha256

def read(p):return json.loads(Path(p).read_text())
def save(p,x):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
for kp in [17592186096652,17592186096653,17592186096701,17592186235285]:
 d=H/str(kp);inv=read(d/'capture-after-retirement/inventory.json');fingerprints=set(inv['fingerprints']);kpuuid=read(d/'capture-after-retirement/kp.json')[':knowledge-point/id'];witness=[]
 with tempfile.TemporaryDirectory(prefix='vector-publisher-inputs-') as temp:
  for band in ['easy','moderate','hard']:
   original=d/'verification'/band;raw_batch=read(original/'records.json');expected=read(d/'publish'/band/'delivery/accepted.json');initial=read(original/'delivery-postretirement/accepted.json');mapping=read(d/'publish'/band/'ui-coverage.json')['records'];assert len(raw_batch)==len(initial);assert [initial[x['source_index']] for x in mapping]==expected;raw=[raw_batch[x['source_index']] for x in mapping]
   actual,duplicates=prepare_records(raw,kp,kpuuid,fingerprints,Path(temp),original/'assets');assert actual==expected
   # Preserve the concrete reason double processing was rejected. Never patch
   # or strip these manifests to make record identities look unchanged.
   second,_=prepare_records(expected,kp,kpuuid,fingerprints,Path(temp),Path(temp));assert [r['question'] for r in second]==[r['question'] for r in expected];assert [r['generation'] for r in second]==[r['generation'] for r in expected]
   assert second!=expected
   differences=[dict(index=i,first_assets=before['assets'],second_assets=after['assets']) for i,(before,after) in enumerate(zip(expected,second)) if before!=after]
   save(d/'publish'/band/'publisher-input-witness.json',dict(passed=True,raw_input_batch_sha256=batch_sha256(raw),actual_prepared_batch_sha256=batch_sha256(actual),reviewed_batch_sha256=batch_sha256(expected),exact_reviewed_output=True,double_localization_changes_manifest_source_keys_only=True,retained_double_localization_differences=differences,duplicates=duplicates))
   fingerprints.update(content_fingerprint(r['question']) for r in actual);witness.append(dict(band=band,records=len(actual),exact_prepared_equals_reviewed=True))
 save(d/'publisher-input-verification.json',dict(passed=True,bands=witness,repair='Submit original raw generator inputs once; bind exact Publisher prepared survivor output to accepted review. No record metadata stripped or fabricated.'))
 print(kp,'exact single-localization output equals all reviewed survivors',flush=True)
