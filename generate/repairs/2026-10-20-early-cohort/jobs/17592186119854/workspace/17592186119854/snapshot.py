import json,sys,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from serve_graph_explorer import database_environment
from database import Database
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';KP=17592186119854
if __name__=='__main__':
 p=HERE/'reference/initial';p.mkdir(parents=True,exist_ok=True)
 r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,text=True,capture_output=True,check=True,timeout=55)
 inv=json.loads(r.stdout)['data'];(p/'inventory.json').write_text(json.dumps(inv,indent=2))
 rows=DB.query((HERE/'source-query.edn').read_text(),[KP],p,'source',inv['basis'])
 source={'database':'math','basis':inv['basis'],'lineage':inv['lineage'],'record':rows[0][0]}
 (HERE/'source.json').write_text(json.dumps(source,indent=2,default=str)+'\n')
 print(json.dumps({'basis':inv['basis'],'jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'generator':source['record'].get(':knowledge-point/question-generator'),'questions':len(source['record'][':knowledge-point/questions'])}))
