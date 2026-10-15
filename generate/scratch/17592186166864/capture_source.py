import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]; HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from serve_graph_explorer import database_environment
from inventory_jobs import save
from edn import dumps
E=database_environment('math')
db=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=E['EDB_ENDPOINT']))
basis=db.basis();kp=db.query((HERE/'reference/source-query.edn').read_text(),[17592186166864],HERE/'reference','source',basis)[0][0]
save(HERE/'source.json',json.loads(json.dumps(kp,default=str)))
save(HERE/'reference/capture.json',{'basis':basis})
print('basis',basis);print(json.dumps(kp,default=str,indent=2))
