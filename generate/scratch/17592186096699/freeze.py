"""Finalize only after every validation/document producer has exited."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
H=Path(__file__).resolve().parent
# Metadata-only alias migration for records emitted by the completed full audit;
# it changes neither learner content, UUIDs, math fingerprints nor grader inputs.
def aliases(x):
 if isinstance(x,dict):
  if 'generation' in x and 'math_fingerprint' in x['generation']:
   x['generation']['mathematical_fingerprint']=x['generation']['math_fingerprint']
  for v in x.values():aliases(v)
 elif isinstance(x,list):
  for v in x:aliases(v)
for name in ('review.json','engine-input.json'):
 p=H/name;value=json.loads(p.read_text());aliases(value);p.write_text(json.dumps(value,indent=2)+'\n')
report=json.loads((H/'validation.json').read_text());assert report['status']=='pass'
producer_paths=[H.with_suffix('.py'),H/'validate.py',H/'build_docs.py',H/'notation_audit.py',Path(__file__).resolve()]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
manifest={'frozen_at':datetime.now(timezone.utc).isoformat(),'producers_stopped':True,'producer_hashes':{str(p):sha(p) for p in producer_paths},'artifact_hashes':{str(p):sha(p) for p in sorted(H.iterdir()) if p.is_file() and p.name!='frozen-manifest.json'},'native_engine_sha256':sha(Path('generate/runs/current/check-engine')),'native_engine_source_sha256':sha(Path('generate/runs/current/check-engine.rs')),'final_counts':report}
(H/'frozen-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'generator_sha256':manifest['producer_hashes'][str(H.with_suffix('.py'))],'manifest':str(H/'frozen-manifest.json'),'counts':report},indent=2))
