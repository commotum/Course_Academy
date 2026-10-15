import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import database_environment
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from database import Database
from edn import dumps
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
if __name__=='__main__':
 b=DB.basis();kp=DB.query((HERE/'reference/source-query.edn').read_text(),[17592186133893],HERE/'reference/initial','kp',b)[0][0]
 (HERE/'source.json').write_text(json.dumps({'basis':b,'kp':kp},indent=2,default=str)+'\n')
 r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
 inv=json.loads(r.stdout)['data'];(HERE/'reference/initial/inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
 print(json.dumps({'basis':b,'generator':kp.get(':knowledge-point/question-generator'),'questions':len(kp[':knowledge-point/questions']),'inventory_basis':inv['basis'],'jobs':[j for j in inv['jobs'] if j['knowledgePoint']==17592186133893]}))
 for q in [kp[':knowledge-point/canonical-example']]+kp[':knowledge-point/questions']:
  print('\nSOURCE',q.get(':question/math-academy-id'),q[':db/id'],q.get(':question/difficulty'))
  print(q.get(':question/problem'));print('CHOICES',[(a[':answer/value'],a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')) for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])])
