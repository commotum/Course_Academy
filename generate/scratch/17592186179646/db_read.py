import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT))
from capture.scripts.storage import atomic_json,atomic_text
sys.path[:0]=[str(ROOT),str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from serve_graph_explorer import database_environment
from edn import dumps,loads,kw
from capture.scripts.storage import atomic_json,atomic_text
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
KP=17592186179646;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1';SOURCE=':application/ca-engine'
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7';OUT=ROOT/'reference/generated'/str(KP)
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,text=True,capture_output=True,check=True,timeout=55)
 x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE;atomic_json(path,x['data']);return x['data']
def read(path,b):
 r=DB.query((HERE/'source-query.edn').read_text(),[KP],path,'kp',b);assert len(r)==1;return r[0][0]
def plain(x):
 if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
 if isinstance(x,list):return [plain(v) for v in x]
 if hasattr(x,'hex'):return str(x)
 return x
if __name__=='__main__':
 inv=inventory(OUT/'initial-inventory.json');b=inv['basis'];r=read(OUT/'initial',b);atomic_json(HERE/'source.json',{'database':'math','basis':b,'lineage':LINEAGE,'record':plain(r)})
 print(json.dumps({'basis':b,'generator':plain(r.get(':knowledge-point/question-generator')),'jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'questions':len(r[':knowledge-point/questions'])}))
 for q in r[':knowledge-point/questions']:
  fs=q.get(':question/answer-fields',[]);print(q[':db/id'],q.get(':question/math-academy-id'),q.get(':question/difficulty'),q.get(':question/problem'),[[a[':answer/value'] for a in f[':answer-field/choices']] for f in fs], [f.get(':answer-field/correct',{}).get(':answer/value') for f in fs])
