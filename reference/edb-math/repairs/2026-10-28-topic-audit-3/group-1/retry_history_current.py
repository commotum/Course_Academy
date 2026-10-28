import json,sys,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
p=H/'incoming-history-proof.json';d=json.loads(p.read_text())
for row in d['results']:
 if not row['error']:continue
 e=row['target'];name='incoming-literal-retry-'+str(e)
 try:row['rows']=connection().query(f'[:find ?e ?a :where [?e ?a {e}]]',[],H,name,9837);row['previous_error']=row['error'];row['error']=None
 except subprocess.CalledProcessError as ex:row['retry_error']=ex.stderr
 p.write_text(json.dumps(d,default=str,indent=2)+'\n');print(e,row['rows'],row['error'],flush=True)
