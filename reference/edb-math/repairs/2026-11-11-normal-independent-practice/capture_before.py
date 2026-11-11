import sys,json
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from generator_publish import Publisher,jsonable,QUESTION_PULL
p=Publisher.from_environment(source=':agent/codex');status=p.client.status();basis=status['basis']
def save(name,value):(H/(name+'.json')).write_text(json.dumps(jsonable(value),indent=2)+'\n')
save('status',status)
source=p.extract_source(17592186092240,H/'source',basis=basis)
kp=p.read_kp(17592186092240,H/'inventory',basis);inventory=p.save_inventory(17592186092240,kp,status,basis,H/'inventory')
qs=kp[':knowledge-point/questions'];ids=[q[':db/id'] for q in qs]
save('siblings',qs)
save('prompt-provenance',p.client.query('[:find ?q ?p ?tx (pull ?s [:db/id :db/ident]) (pull ?tx [:db/txInstant]) :in $ [?q ...] :where [?q :question/problem ?p ?tx ?s]]',[ids],H,'prompt-provenance',basis))
save('task-items',p.client.query('[:find (pull ?i [*]) :in $ [?q ...] :where [?i :task-item/content ?q]]',[ids],H,'task-items',basis))
for q in qs:print(q[':db/id'],q.get(':question/math-academy-id','authored'),q[':question/difficulty'],repr(q[':question/problem']))
