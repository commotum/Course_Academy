import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from serve_graph_explorer import database_environment,build_learning
from inventory_jobs import save
D=HERE/'reference/initial'
env=database_environment('math')
db=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=env['EDB_ENDPOINT']))
r=subprocess.run([str(build_learning(ROOT.parent/'EDB')),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',env['EDB_ENDPOINT']],input='{"action":"inventory"}',env=env,capture_output=True,text=True,check=True)
i=json.loads(r.stdout)['data'];save(D/'inventory.json',i)
q=db.query((HERE/'reference/source-query.edn').read_text(),[17592186064178],D,'kp',i['basis'])[0][0]
save(HERE/'source.json',{'basis':i['basis'],'lineage':i['lineage'],'record':json.loads(json.dumps(q,default=str))})
print(json.dumps({'basis':i['basis'],'lineage':i['lineage'],'jobs':[j for j in i['jobs'] if j['knowledgePoint']==17592186064178],'record':q},default=str,indent=2))
