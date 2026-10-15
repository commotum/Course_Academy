import json,sys,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from serve_graph_explorer import database_environment,build_learning
HERE=Path(__file__).parent
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
DB.env=ENV
KP=17592186172100
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
def save(path,value):path.write_text(json.dumps(value,indent=2,default=str)+'\n')
def inventory():
 binary=build_learning(ROOT.parent/'EDB')
 r=subprocess.run([str(binary),'math',LEARNER,ENV['EDB_ENDPOINT']],input='{"action":"inventory"}',env=ENV,text=True,capture_output=True,check=True)
 v=json.loads(r.stdout);assert v['ok'];return v['data']
if __name__=='__main__':
 inv=inventory();save(HERE/'reference/inventory-before.json',inv)
 basis=inv['basis'];kp=DB.query((HERE/'reference/source-query.edn').read_text(),[KP],HERE/'reference/read-before','source',basis)[0][0]
 save(HERE/'source.json',{'database':'math','basis':basis,'lineage':inv['lineage'],'record':kp})
 print(json.dumps({'basis':basis,'lineage':inv['lineage'],'generator':kp.get(':knowledge-point/question-generator'),'jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'sources':[(q[':question/math-academy-id'],q[':question/difficulty'],q[':question/problem'],[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]) for q in kp[':knowledge-point/questions']]},indent=2))
