"""Freeze all owned bytes; never changes the registered numeric generator/tree."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
baseline=json.loads((H/'registered-baseline.json').read_text())['files']
paths=[ROOT/'generate/scratch/17592186064226.py']+sorted((ROOT/'generate/scratch/17592186064226').rglob('*'))
assert [{'path':str(p.relative_to(ROOT)),'size':p.stat().st_size,'sha256':sha(p)}for p in paths if p.is_file()]==baseline
source=ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186064226.json';assert sha(source)==sha(H/'source.json')
files=[H.with_suffix('.py')]+[p for p in sorted(H.rglob('*'))if p.is_file()and p.name!='freeze.json']
ledger=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)}for p in files]
manifest={'scope':'External owned draft.py and every owned tree file except freeze.json (self-reference excluded).','generator_sha256':sha(H.with_suffix('.py')),'source_basis':2275,'source_snapshot_sha256':sha(source),'registered_baseline_verified':True,'files':ledger,'tree_content_sha256':hashlib.sha256(json.dumps(ledger,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
(H/'freeze.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({k:manifest[k]for k in ['generator_sha256','tree_content_sha256','registered_baseline_verified']},indent=2))
