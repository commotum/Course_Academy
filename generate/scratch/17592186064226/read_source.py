import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from serve_graph_explorer import database_environment
from edn import dumps
ENV=database_environment('math');db=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
x=json.loads(subprocess.run([str(ROOT/'.local/graph-explorer/learning-80371ed6e5f3669c'),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',ENV['EDB_ENDPOINT']],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True).stdout)['data']
(HERE/'reference/inventory-before.json').write_text(json.dumps(x,indent=2))
b=x['basis'];rows=db.query((HERE/'reference/source-query.edn').read_text(),[17592186064226],HERE/'reference','source',b)
(HERE/'source.json').write_text(json.dumps({'basis':b,'lineage':x['lineage'],'kp':rows[0][0]},default=str,indent=2))
print(json.dumps({'basis':b,'jobs':[j for j in x['jobs'] if j['knowledgePoint']==17592186064226],'kp':rows[0][0]},default=str,indent=2))
