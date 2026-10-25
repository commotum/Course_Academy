"""Validate exact final payloads through native EDB speculation; no commits."""
import hashlib,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection
db=connection()
for b in json.loads((H/'batches.json').read_text()):
 folder=H/b['name'];payload=folder/'transaction.edn';assert hashlib.sha256(payload.read_bytes()).hexdigest()==b['sha256']
 subprocess.run([str(R/'.local/edb/percent-escaping/preview'),str(payload),str(folder/'fields.json'),str(folder/'preview-check.json')],env=db.env,check=True,capture_output=True,text=True)
 proof=json.loads((folder/'preview-check.json').read_text());proof['sha256']=b['sha256'];(folder/'preview-check.json').write_text(json.dumps(proof,indent=2)+'\n')
 print('Native preview passed',b['name'],'fields',b['fields'],'T'+str(proof['db_before_t']),flush=True)
