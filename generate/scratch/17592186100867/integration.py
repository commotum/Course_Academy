import json,sys,subprocess
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from serve_graph_explorer import database_environment
from inventory_jobs import save
KP=17592186100867
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
NATIVE=max((p for p in (ROOT/'.local/graph-explorer').glob('learning-*') if p.is_file() and p.stat().st_mode&0o111),key=lambda p:p.stat().st_mtime)
QUERY=(HERE/'reference/source-query.edn').read_text()
def inventory(path):
 r=subprocess.run([str(NATIVE),'math',LEARNER,ENV['EDB_ENDPOINT']],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok'];save(path,x['data']);return x['data']
def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
if __name__=='__main__':
 inv=inventory(HERE/'reference/initial-inventory.json');b=inv['basis'];kp=read_kp(HERE/'reference/initial',b)
 (HERE/'reference/source.json').write_text(json.dumps({'basis':b,'lineage':inv['lineage'],'record':kp},default=str,indent=2)+'\n')
 print(json.dumps({'basis':b,'lineage':inv['lineage'],'jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'generator':kp.get(':knowledge-point/question-generator'),'title':kp[':knowledge-point/title']}))
 for q in kp[':knowledge-point/questions']:
  print(q[':question/math-academy-id'],q.get(':question/difficulty'),q[':question/problem'], 'fields',[(f[':answer-field/key'],f[':answer-field/type'],f.get(':answer-field/correct',{}).get(':answer/value')) for f in q[':question/answer-fields']])

# Exact current learner pool through the existing application predicates.
def pool_inventory(path):
 import tempfile
 inv=inventory(path)
 with tempfile.TemporaryDirectory(prefix='matrix-column-inventory-') as temporary:
  snap=Path(temporary)/'snapshot.json'
  r=subprocess.run([str(NATIVE),'math',LEARNER,ENV['EDB_ENDPOINT']],input='{"action":"export-test-snapshot"}',env={**ENV,'LEARNING_SNAPSHOT_PATH':str(snap)},capture_output=True,text=True,check=True,timeout=55)
  assert json.loads(r.stdout)['ok']
  counts=path.with_name(path.stem+'-counts.json')
  subprocess.run([str(HERE/'inspect-inventory'),str(snap),str(counts)],check=True,timeout=55)
 result=json.loads(counts.read_text());assert result['basis']==inv['basis']==DB.basis()
 return inv,result
