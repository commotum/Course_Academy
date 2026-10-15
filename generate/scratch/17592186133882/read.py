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
b=DB.basis(); rows=DB.query((D/'source-query.edn').read_text(),[17592186133882],D,'source',b)
(D/'source.json').write_text(json.dumps({'basis':b,'record':rows[0][0]},default=str,indent=2))
q=rows[0][0]; print(b,q[':knowledge-point/title'],q[':knowledge-point/id'],q.get(':knowledge-point/question-generator'))
for x in q.get(':knowledge-point/questions',[])+[q.get(':knowledge-point/canonical-example',{})]:
 print(x.get(':question/math-academy-id'),x.get(':question/difficulty'),x.get(':question/problem')); print('SOLUTION',x.get(':question/worked-solution'));print('FIELDS',dumps(x.get(':question/answer-fields',[])))
