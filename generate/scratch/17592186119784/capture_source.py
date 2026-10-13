import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from serve_graph_explorer import database_environment,build_learning
from database import Database
from edn import dumps
HERE=Path(__file__).resolve().parent
OUT=HERE/'reference/initial'
db=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
native=build_learning(ROOT.parent/'EDB')
r=subprocess.run([str(native),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',db.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True)
inv=json.loads(r.stdout)['data'];(OUT/'inventory.json').write_text(json.dumps(inv,indent=2))
b=inv['basis'];kp=db.query((HERE/'reference/source-query.edn').read_text(),[17592186119784],OUT,'source',b)[0][0]
(OUT/'source.json').write_text(json.dumps({'basis':b,'lineage':inv['lineage'],'record':kp},indent=2,default=str))
print(json.dumps({'basis':b,'lineage':inv['lineage'],'jobs':[j for j in inv['jobs'] if j['knowledgePoint']==17592186119784],'kp':kp},indent=2,default=str))
