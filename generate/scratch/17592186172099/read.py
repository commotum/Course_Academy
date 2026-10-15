from pathlib import Path
from types import SimpleNamespace
import sys,json
R=Path(__file__).resolve().parents[3];sys.path[:0]=[str(R/'scripts'),str(R/'scripts/question_capture')]
from database import Database
from serve_graph_explorer import database_environment
P=Path(__file__).parent/'reference/initial'
db=Database(SimpleNamespace(edb_bin=str(R/'.local/edb/capture-runtime/math-edb'),database='math',endpoint='/tmp/edb-math/writer.sock'));db.env=database_environment('math')
b=db.basis();q=(P/'source-query.edn').read_text();kp=db.query(q,[17592186172099],P,'source',b)[0][0]
(P/'source.json').write_text(json.dumps({'basis':b,'kp':kp},indent=2,default=str)+'\n')
print(b);print(json.dumps(kp,indent=2,default=str))
