import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps
from serve_graph_explorer import database_environment
from inventory_jobs import save
ENV=database_environment('math');DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-80371ed6e5f3669c'
def inventory(path):
 r=subprocess.run([str(NATIVE),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90);x=json.loads(r.stdout);assert x['ok'];save(path,x['data']);return x['data']
