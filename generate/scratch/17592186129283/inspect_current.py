from pathlib import Path
from types import SimpleNamespace
import sys,json
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps
from serve_graph_explorer import database_environment
HERE=Path(__file__).resolve().parent
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
QUERY='''[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example [*]} {[:knowledge-point/questions :limit nil] [* {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/correct [* {:answer/type [:db/ident]}]} {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'''
if __name__=='__main__':
 status={'basis':DB.basis(),'status':DB.command('status')};out=HERE/'reference/replenishment/initial';out.mkdir(exist_ok=True)
 kp=DB.query(QUERY,[17592186129283],out,'kp',status['basis'])[0][0]
 print(status);print('Generator:',kp.get(':knowledge-point/question-generator'))
 for q in kp[':knowledge-point/questions']:
  print(q[':db/id'],q.get(':question/math-academy-id'),q.get(':question/difficulty'),len(q.get(':question/answer-fields',[])))
