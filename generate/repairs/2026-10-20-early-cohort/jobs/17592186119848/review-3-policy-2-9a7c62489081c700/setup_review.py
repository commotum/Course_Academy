import json,shutil,hashlib
from pathlib import Path
E=Path(__file__).resolve().parent;J=E.parent;P=J/'review-2-policy-2-7a41c9f08b6c9942';W=J/'workspace'
load=lambda p:json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
files=['review_helpers.py','audit_delivery.py','check_batch_decisions.py','check_exclusive_subset.py']
for n in files:shutil.copy2(P/n,E/n)
prior=E/'prior';prior.mkdir(exist_ok=True)
reuse=['source-replay.json','source-replay-summary.json','replays.json','catalog.json','math-results.json','coverage-results.json','scope-results.json','grader-input.json','grader-results.json','inventory-review.json']
for n in reuse:shutil.copy2(P/n,prior/n)
shutil.copy2(P/'batch.json',E/'previous-batch.json');shutil.copy2(J/'samples.json',E/'batch.json')
shutil.copy2(J/'review-1-policy-2-36e1ecca399a86e2/batch.json',E/'first-failing-batch.json')
save(E/'package-before.json',{str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()})
save(E/'provenance.json',{'source_review':str(P),'source_hash':'85a2f2ac50bd80025dfc45b405bd0399cc4eac36154fba05258753379a48016a','engine_hash':'dc1e0a8583ca33c6028bc0a641128ecc8e7896742189dd42b292170c9726bad9','reused_files':{n:hashlib.sha256((prior/n).read_bytes()).hexdigest() for n in reuse},'basis':'Unchanged original source and engine per runner binding; current catalog and exact replays will be compared before reusing unaffected checks.'})
rel=E/'relocated';rel.mkdir(exist_ok=True)
for n in ['package.json']+load(W/'package.json')['files']:
 d=rel/n;d.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(W/n,d)
(rel/'checks').mkdir(exist_ok=True);(rel/'evidence').mkdir(exist_ok=True)
for n in ['validate_content.py','check_batch_decisions.py','check_exclusive_subset.py','check_runtime.py']:shutil.copy2(W/'checks'/n,rel/'checks'/n)
print('copied independent tests, reusable evidence, and isolated declared runtime')
