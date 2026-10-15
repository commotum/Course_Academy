import sys,json,importlib.util,subprocess
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from serve_graph_explorer import database_environment
from database import Database
ENV=database_environment('math');DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
src=json.loads((HERE/'source.json').read_text());b=src['basis'];kp=src['record'];out=HERE/'reference/initial'
query='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l] (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
 (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/unlocked] [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?s] [?s :step/content ?q]))]'''
(HERE/'reference/usage-query.edn').write_text(query)
seen={r[0] for history in [False,True] for r in DB.query(query,[17592186179672,'59d5cf13-351c-4114-be19-4c3bb64ee051'],out,'usage-'+str(history),b,history)}
print('Seen/reserved:',seen)
for q in kp[':knowledge-point/questions']:
 print(q[':question/math-academy-id'],q[':db/id'] in seen)
(HERE/'reference/initial/usage.json').write_text(json.dumps(sorted(seen)))
