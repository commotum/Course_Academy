"""Freeze this reviewed package, excluding mutable replenishment receipts."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
artifacts=[HERE.with_suffix('.py')]+[HERE/name for name in ['source.json','validate.py','replenish.py','classification.md','template-extraction.md','plot-extraction.md','source-components.json','source-fidelity.json','source-corrections.json','excluded-sources.json','plot-assets.json','capabilities.json','review.md','review.json','validation.json','reference/native/check-engine.rs','reference/native/check-engine','reference/native/check-engine.build.json','reference/native/check-pool.rs','reference/native/check-pool','reference/native/check-pool.build.json']]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='passed' and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
(HERE/'freeze.json').write_text(json.dumps({'version':'line-integral-smooth-scale-v1','source_basis':validation['source_basis'],'lineage':validation['lineage'],'sha256':{str(p.relative_to(ROOT)):sha(p) for p in artifacts}},indent=2)+'\n')
