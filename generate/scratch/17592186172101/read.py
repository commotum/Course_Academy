import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from serve_graph_explorer import database_environment
from inventory_jobs import save
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
DB.env=database_environment('math')
if __name__=='__main__':
 b=DB.basis();q=DB.query((HERE/'reference/source-query.edn').read_text(),[17592186172101],HERE/'reference/initial','kp',b)[0][0]
 save(HERE/'source.json',{'basis':b,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','record':json.loads(json.dumps(q,default=str))})
 print(json.dumps(q,default=str,indent=2))
 r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True)
 inv=json.loads(r.stdout)['data'];save(HERE/'reference/initial/inventory.json',inv);print('JOBS',json.dumps([j for j in inv['jobs'] if j['knowledgePoint']==17592186172101]))
