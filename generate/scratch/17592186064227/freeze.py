"""Freeze owned numeric script/tree recursively, excluding only this manifest."""
import sys
sys.dont_write_bytecode=True
import collections,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];SCRIPT=HERE.with_suffix('.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,z):(HERE/n).write_text(json.dumps(z,indent=2,ensure_ascii=False)+'\n')
b=json.loads((HERE/'baseline.json').read_text());assert b['captured_before_generator_import']and not b['numeric_script_existed']and not b['numeric_tree_existed'];assert not b['manifest_entry']['latest_inventory']['has_generator']
for source,dest in [('sources/17592186064227.json','sources.json'),('topics/17592186050783.json','topic.json'),('lessons/17592186050783.json','lesson.json')]:assert sha(ROOT/'generate/runs/current/refresh-2026-10-14'/source)==sha(HERE/'reference'/dest)
assert sha(HERE/'source.json')==sha(HERE/'reference/sources.json')
assert sha(HERE/'check-engine')==sha(ROOT/'generate/runs/current/check-engine')
assert sha(HERE/'math_format.py')==sha(ROOT/'scripts/question_capture/math_format.py')
assert not list(HERE.rglob('__pycache__'))
save('final-preservation.json',{'passed':True,'registered_numeric_baseline':'absent before creation; no existing numeric import or mutation','basis_2275_evidence_unchanged':True,'frozen_native_runner_SHA256':sha(HERE/'check-engine'),'frozen_formatter_SHA256':sha(HERE/'math_format.py'),'baseline_SHA256':sha(HERE/'baseline.json'),'scope':'Owned numeric script and matching tree only; no root manifest, QA, shared helper, engine or DB edits'})
v=json.loads((HERE/'validation.json').read_text());v['latest_script_SHA256']=sha(SCRIPT);v['latest_validator_SHA256']=sha(HERE/'validate.py');save('validation.json',v)
manifest=HERE/'freeze-manifest.json';entries={}
for p in[SCRIPT,HERE,*sorted(HERE.rglob('*'))]:
 if p==manifest:continue
 entries[str(p.relative_to(ROOT))]={'kind':'directory'}if p.is_dir()else{'kind':'file','sha256':sha(p),'bytes':p.stat().st_size}
save('freeze-manifest.json',{'version':1,'basis':2275,'script_SHA256':sha(SCRIPT),'validator_SHA256':sha(HERE/'validate.py'),'validation_status':v['status'],'normal_native_grading_gaps':v['native_gap_count'],'excluded':[str(manifest.relative_to(ROOT))],'entries':entries})
print('Frozen',len(entries),'entries; script SHA256',sha(SCRIPT))
