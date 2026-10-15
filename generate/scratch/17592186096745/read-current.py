import sys,json,subprocess
from pathlib import Path
sys.path.insert(0,'scripts')
from serve_graph_explorer import build_learning,database_environment
h=Path('generate/scratch/17592186096745')
b=build_learning(Path('/home/jake/Developer/EDB'))
(h/'native-runtime.json').write_text(json.dumps({'binary':str(b)},indent=2)+'\n')
r=subprocess.run([str(b),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',database_environment('math')['EDB_ENDPOINT']],input='{"action":"inventory"}',text=True,env=database_environment('math'),capture_output=True,check=True)
d=json.loads(r.stdout);(h/'reference/inventory-before-generation.json').write_text(json.dumps(d,indent=2)+'\n');print(d['ok'],d.get('error'));print('basis',d.get('data',{}).get('basis'));print([j for j in d.get('data',{}).get('jobs',[]) if j['knowledgePoint']==17592186096745])
