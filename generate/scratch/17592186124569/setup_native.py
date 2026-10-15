from pathlib import Path
import sys,json,subprocess
sys.path.insert(0,str(Path.cwd()))
from capture.scripts.database.preview import _library
sys.path[:0]=['scripts','scripts/question_capture']
from serve_graph_explorer import database_environment,build_learning
from types import SimpleNamespace
root=Path.cwd();p=root/'generate/scratch/17592186124569/reference/native';p.mkdir(parents=True,exist_ok=True)
lib=_library(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math')))
reader=build_learning(lib.parents[3])
(p/'inventory-reader.json').write_text(json.dumps({'path':str(reader),'edb_library':str(lib)}))
r=subprocess.run([str(reader),'math','59d5cf13-351c-4114-be19-4c3bb64ee051','/tmp/edb-math/writer.sock'],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True)
x=json.loads(r.stdout);assert x['ok'];(p.parent/'initial/inventory.json').write_text(json.dumps(x['data'],indent=2));print('inventory basis',x['data']['basis']);print([j for j in x['data']['jobs'] if j['knowledgePoint']==17592186124569])
