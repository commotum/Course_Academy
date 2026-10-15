import sys,json
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from serve_graph_explorer import database_environment
from database import Database
from edn import dumps
D=Path(__file__).resolve().parent
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
DB.env=database_environment('math')
b=DB.basis(); rows=DB.query((D/'source-query.edn').read_text(),[17592186133883],D,'source',b)
(D/'source.json').write_text(json.dumps({'basis':b,'record':rows[0][0]},default=str,indent=2))
print('basis',b,'title',rows[0][0][':knowledge-point/title'],'generator',rows[0][0].get(':knowledge-point/question-generator'))
for q in rows[0][0][':knowledge-point/questions']:
 print(q.get(':question/math-academy-id'),q.get(':question/difficulty'),q[':question/problem']);f=q[':question/answer-fields'][0];print('bank',[a[':answer/value'] for a in f[':answer-field/choices']],'correct',f[':answer-field/correct'][':answer/value'])
import subprocess
r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7'),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
x=json.loads(r.stdout);(ROOT/'reference/generated/17592186133883/initial-inventory.json').write_text(json.dumps(x,indent=2));print('inventory',x['data']['basis'],[j for j in x['data']['jobs'] if j['knowledgePoint']==17592186133883])
