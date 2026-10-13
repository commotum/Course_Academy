import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps
from serve_graph_explorer import database_environment
from inventory_jobs import save
D=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint='/tmp/edb-math/writer.sock'))
b=D.basis();q=D.query((HERE/'reference/source-query.edn').read_text(),[17592186059862],HERE/'reference','source',b)[0][0]
save(HERE/'reference/source.json',json.loads(json.dumps(q,default=str)));save(HERE/'reference/basis.json',{'basis':b,'status':D.command('status')})
r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-80371ed6e5f3669c'),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',D.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=90)
x=json.loads(r.stdout);assert x['ok'];save(HERE/'reference/inventory-initial.json',x['data'])
print(json.dumps({'basis':b,'title':q[':knowledge-point/title'],'uuid':q[':knowledge-point/id'],'generator':q.get(':knowledge-point/question-generator'),'jobs':[j for j in x['data']['jobs'] if j['knowledgePoint']==17592186059862],'source_count':len(q.get(':knowledge-point/questions',[]))},default=str))
