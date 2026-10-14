import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];H=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/question_capture'));sys.path.insert(0,str(ROOT/'scripts'))
from database import Database,QUESTION_PULL
from edn import dumps
from serve_graph_explorer import database_environment
D=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',D.args.endpoint],input='{"action":"inventory"}',env=D.env,capture_output=True,text=True,check=True,timeout=55)
x=json.loads(r.stdout);assert x['ok'];inv=x['data'];(H/'reference/inventory-before.json').write_text(json.dumps(inv,indent=2))
b=inv['basis'];q='[:find (pull ?k [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?k :where [?k :knowledge-point/id _]]'
r=D.query(q,[17592186119806],H/'reference','source',b);assert len(r)==1
(H/'source.json').write_text(json.dumps({'basis':b,'lineage':inv['lineage'],'record':r[0][0]},default=str,indent=2))
print(json.dumps({'basis':b,'jobs':[j for j in inv['jobs'] if j['knowledgePoint']==17592186119806],'source':r[0][0]},default=str,indent=2))
