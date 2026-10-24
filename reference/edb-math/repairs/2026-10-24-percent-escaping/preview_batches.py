"""Validate exact final payloads through native EDB speculation; no commits."""
import hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection
db=connection()
for b in json.loads((H/'batches.json').read_text()):
 folder=H/b['name'];payload=folder/'transaction.edn';assert hashlib.sha256(payload.read_bytes()).hexdigest()==b['sha256']
 subprocess.run([str(R/'.local/edb/mathml-tables-runtime/preview'),str(payload),str(folder/'fields.json'),str(folder/'preview-check.json')],env=db.env,check=True)
 proof=json.loads((folder/'preview-check.json').read_text());proof['sha256']=b['sha256'];(folder/'preview-check.json').write_text(json.dumps(proof,indent=2)+'\n')
