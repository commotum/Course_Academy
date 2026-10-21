"""Capture the affected bank and learner records at one immutable basis."""
from pathlib import Path
import sys, json
sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.client import QUESTION_PULL
HERE = Path(__file__).resolve().parent
db = Publisher.from_environment(source=':application/ca-engine').client
b = db.basis()
out = HERE / f'snapshot-{b}'
out.mkdir(exist_ok=True)
def read(name, query, args):
    rows = db.query(query, args, out, name, b)
    (out/(name+'.json')).write_text(json.dumps(rows, indent=2, default=str)+'\n')
    return rows
kp = read('kp', '[:find (pull ?k [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {:knowledge-point/questions '+QUESTION_PULL+'}]) :in $ ?k :where [?k :knowledge-point/id _]]', [17592186129115])[0][0]
items = read('items', '[:find (pull ?i [* {:task-item/status [:db/id :db/ident]} {:task-item/responses [*]} {:learner-task/_items [:db/id]}]) :in $ [?q ...] :where [?i :task-item/content ?q]]', [[q[':db/id'] for q in kp[':knowledge-point/questions']]])
def many(v):
    return [v] if isinstance(v, dict) else v
tasks = sorted({t[':db/id'] for [i] in items for t in many(i.get(':learner-task/_items', []))})
read('tasks', '[:find (pull ?t [* {:learner-task/status [:db/id :db/ident]} {:learner-task/activity [* {:activity/type [:db/id :db/ident]} {:activity/scope [:db/id :topic/title]}]} {:learner-task/items [* {:task-item/status [:db/id :db/ident]} {:task-item/responses [*]} {:task-item/content [:db/id :question/id :question/problem {:knowledge-point/_questions [:db/id :knowledge-point/title]}]}]} {:learner/_activity [:db/id :learner/id]}]) :in $ [?t ...] :where [?t :learner-task/id _]]', [tasks])
read('learner', '[:find (pull ?l [* {:learner/performance [*]} {[:learner/knowledge-profile :limit nil] [* {:progress/topic [:db/id :topic/title]}]} {:learner/activity [:db/id :learner-task/priority :learner-task/remediation-for {:learner-task/status [:db/id :db/ident]} {:learner-task/activity [:db/id :activity/title {:activity/type [:db/id :db/ident]} {:activity/scope [:db/id :topic/title]}]}]}]) :in $ ?l :where [?l :learner/id _]]', [17592186045416])
(HERE/'snapshot-path.txt').write_text(str(out.relative_to(ROOT)))
print(json.dumps({'basis': b, 'questions':len(kp[':knowledge-point/questions']), 'items':len(items),'tasks':tasks}))
