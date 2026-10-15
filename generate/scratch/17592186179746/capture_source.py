import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]; HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from serve_graph_explorer import database_environment
from edn import dumps
D=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));D.env=database_environment('math')
r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',D.args.endpoint],input='{"action":"inventory"}',env=D.env,capture_output=True,text=True,check=True)
i=json.loads(r.stdout)['data'];(HERE/'reference/inventory.json').write_text(json.dumps(i,indent=2));b=i['basis']
k=D.query((HERE/'reference/source-query.edn').read_text(),[17592186179746],HERE/'reference/initial','kp',b)[0][0]
(HERE/'source.json').write_text(json.dumps({'basis':b,'lineage':i['lineage'],'record':k},default=str,indent=2))
print(b,k[':knowledge-point/title'],k[':knowledge-point/id'],k.get(':knowledge-point/question-generator'))
for q in k[':knowledge-point/questions']:
 print(q.get(':question/math-academy-id'),q[':db/id'],q.get(':question/difficulty'),q[':question/problem'])
