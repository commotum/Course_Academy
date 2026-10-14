import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from serve_graph_explorer import database_environment,build_learning
from edn import dumps
from inventory_jobs import save
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE=build_learning(ROOT.parent/'EDB')
def inventory(path):
 r=subprocess.run([str(NATIVE),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok'];save(path,x['data']);return x['data']
if __name__=='__main__':
 inv=inventory(HERE/'reference/initial/inventory.json');b=inv['basis'];q=(HERE/'reference/source-query.edn').read_text();kp=DB.query(q,[17592186166863],HERE/'reference/initial','kp',b)[0][0]
 save(HERE/'source.json',{'basis':b,'lineage':inv['lineage'],'record':json.loads(json.dumps(kp,default=str))});print('basis',b,'lineage',inv['lineage'],'generator',kp.get(':knowledge-point/question-generator'))
 print('KP',kp[':knowledge-point/id'],kp[':knowledge-point/title'])
 print('jobs',json.dumps([j for j in inv['jobs'] if j['knowledgePoint']==17592186166863]))
 for q in kp[':knowledge-point/questions']:
  print('\n',q[':db/id'],q.get(':question/math-academy-id'),q.get(':question/difficulty'), '\n',q[':question/problem'])
  print('fields',[(f[':answer-field/key'],f[':answer-field/type'],[(a[':answer/value']) for a in f[':answer-field/choices']],f.get(':answer-field/correct',{}).get(':answer/value')) for f in q[':question/answer-fields']])
 print('CANONICAL',kp.get(':knowledge-point/canonical-example'))
