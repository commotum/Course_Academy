import sys,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from serve_graph_explorer import database_environment,build_learning
from inventory_jobs import save
exe=build_learning(ROOT.parent/'EDB')
r=subprocess.run([str(exe),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',database_environment('math')['EDB_ENDPOINT']],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True)
x=json.loads(r.stdout);assert x['ok'];save(HERE/'inventory-initial.json',x['data']);save(HERE/'runtime.json',{'native':str(exe)})
print(json.dumps({'basis':x['data']['basis'],'lineage':x['data']['lineage'],'jobs':[j for j in x['data']['jobs'] if j['knowledgePoint']==17592186096621]},indent=2))
