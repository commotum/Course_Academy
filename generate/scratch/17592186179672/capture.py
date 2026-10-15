import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from serve_graph_explorer import database_environment,build_learning
from database import Database
from edn import dumps
ENV=database_environment('math');DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
query=(ROOT/'generate/scratch/17592186105905/reference/replenishment/source-query.edn').read_text();(HERE/'reference/source-query.edn').write_text(query)
b=DB.basis();kp=DB.query(query,[17592186179672],HERE/'reference/initial','kp',b)[0][0]
(HERE/'source.json').write_text(json.dumps({'basis':b,'record':kp},indent=2,default=str))
native=build_learning(ROOT.parent/'EDB');(HERE/'reference/learning-executable.txt').write_text(str(native))
r=subprocess.run([str(native),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',ENV['EDB_ENDPOINT']],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=55)
x=json.loads(r.stdout);(HERE/'reference/initial/inventory.json').write_text(json.dumps(x,indent=2));print(json.dumps({'basis':b,'title':kp.get(':knowledge-point/title'),'generator':kp.get(':knowledge-point/question-generator'),'questions':len(kp.get(':knowledge-point/questions',[])),'inventory_basis':x['data']['basis'],'lineage':x['data']['lineage'],'jobs':[j for j in x['data']['jobs'] if j['knowledgePoint']==17592186179672]},indent=2,default=str))
