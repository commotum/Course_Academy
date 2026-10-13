import json,subprocess,sys
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps
from serve_graph_explorer import database_environment
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-80371ed6e5f3669c'),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=90)
inv=json.loads(r.stdout)['data'];(HERE/'reference/inventory-initial.json').write_text(json.dumps(inv,indent=2))
b=inv['basis'];kp=DB.query((HERE/'reference/source-query.edn').read_text(),[17592186064283],HERE/'reference','source',b)[0][0]
(HERE/'source.json').write_text(json.dumps({'basis':b,'lineage':inv['lineage'],'record':kp},indent=2,default=str)+'\n')
print(json.dumps({'basis':b,'lineage':inv['lineage'],'jobs':[j for j in inv['jobs'] if j['knowledgePoint']==17592186064283],'generator':kp.get(':knowledge-point/question-generator'),'questions':len(kp.get(':knowledge-point/questions',[]))},indent=2,default=str))
