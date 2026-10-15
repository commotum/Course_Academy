from pathlib import Path
import sys,json,subprocess
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from serve_graph_explorer import database_environment,build_learning
from inventory_jobs import save
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
KP=17592186184172
QUERY=(HERE/'reference/source-query.edn').read_text()
if __name__=='__main__':
 b=DB.basis();q=DB.query(QUERY,[KP],HERE/'reference/initial','kp',b)[0][0]
 save(HERE/'source.json',{'basis':b,'record':json.loads(json.dumps(q,default=str))})
 binary=build_learning(ROOT.parent/'EDB')
 r=subprocess.run([str(binary),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True)
 x=json.loads(r.stdout);assert x['ok'];save(HERE/'reference/inventory-before.json',x['data'])
 print(json.dumps({'basis':b,'record':q,'inventory_basis':x['data']['basis'],'jobs':[j for j in x['data']['jobs'] if j['knowledgePoint']==KP]},default=str,indent=2))
