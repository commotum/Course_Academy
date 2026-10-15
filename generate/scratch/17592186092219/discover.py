from pathlib import Path
import sys,json,subprocess
from types import SimpleNamespace
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from serve_graph_explorer import database_environment
from inventory_jobs import save
from edn import dumps
D=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
P=H/'reference/initial'
b=D.basis();status=D.command('status');(P/'status.txt').write_text(status)
q=D.query((H/'reference/source-query.edn').read_text(),[17592186092219],P,'kp',b)[0][0]
save(P/'source.json',{'database':'math','basis':b,'record':json.loads(json.dumps(q,default=str))})
native=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7'
r=subprocess.run([str(native),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',D.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),text=True,capture_output=True,check=True)
x=json.loads(r.stdout);assert x['ok'];save(P/'inventory.json',x['data'])
print(json.dumps({'status':status,'title':q[':knowledge-point/title'],'questions':len(q[':knowledge-point/questions']),'generator':q.get(':knowledge-point/question-generator'),'jobs':[j for j in x['data']['jobs'] if j['knowledgePoint']==17592186092219],'inventory_basis':x['data']['basis']},default=str,indent=2))
