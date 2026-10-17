"""Read-only fixed-basis inventory of multipart descendants and active routes."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import Tagged, kw, loads

HERE = Path(__file__).resolve().parent
FLAGGED = [17592186514433, 17592186235429, 17592186514464]
TASK_PULL = '''[:db/id :learner-task/id {:learner-task/status [:db/ident]}
 {[:learner/_activity :limit nil] [:db/id]}
 {:learner-task/activity [:db/id :activity/title {:activity/type [:db/ident]}
 :activity/first-step {[:activity/steps :limit nil] [:db/id :step/next {:step/content [:db/id :knowledge-point/id :question/id :multistep/id]}]}]}
 {[:learner-task/items :limit nil] [:db/id :task-item/content :task-item/next {:task-item/status [:db/ident]}]}]'''

def main():
    db = Publisher.from_environment(source=':agent/gpt-6.1-sol-high').client
    identity = db.status(); basis = int(sys.argv[1]) if len(sys.argv)>1 else identity['basis']; identity['basis']=basis
    directory = HERE / str(basis); directory.mkdir(exist_ok=True)
    def read(name, query, inputs=None):
        saved = directory / (name+'.edn')
        if saved.exists(): return loads(saved.read_text())
        return db.query(query, inputs or [], directory, name, basis)
    specs = {
        'multipart-parents': ('[:find (pull ?m [:db/id {[:multistep/steps :limit nil] [:db/id :step/content]}]) :where [?m :multistep/id _]]', []),
        'wrapper-edges': ('[:find ?w ?c :where [?w :assigned-problem/content ?c]]', []),
        'open-tasks': ('[:find (pull ?t '+TASK_PULL+') :in $ [?state ...] [?kind ...] :where [?t :learner-task/status ?status] [?status :db/ident ?state] [?t :learner-task/activity ?a] [?a :activity/type ?type] [?type :db/ident ?kind]]', [[kw('learner-task.status/'+v) for v in ['started','paused','locked','unlocked']], [kw('activity.type/'+v) for v in ['lesson','review','assessment']]])
    }
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = {name: pool.submit(read, name, *args) for name,args in specs.items()}
        data = {name: future.result() for name,future in jobs.items()}
    data['multipart-edges'] = [(m[':db/id'], st[':db/id'], st[':step/content'][':db/id']) for [m] in data['multipart-parents'] for st in m.get(':multistep/steps',[])]
    children = {}
    for m, st, c in data['multipart-edges']: children.setdefault(m,set()).add(c)
    for w,c in data['wrapper-edges']: children.setdefault(w,set()).add(c)
    roots = {m for m,st,c in data['multipart-edges']}
    descendants = set(); pending = [c for m in roots for c in children.get(m, [])]
    while pending:
        node = pending.pop()
        if node in descendants: continue
        descendants.add(node); pending.extend(children.get(node, []))
    membership_rows=[]
    nodes=sorted(descendants)
    if '--memberships' in sys.argv:
        for offset in range(0,len(nodes),25):
            rows=read('descendant-kp-pulls-'+str(offset), '[:find (pull ?q [:db/id {[:knowledge-point/_questions :limit nil] [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]', [nodes[offset:offset+25]])
            membership_rows.extend((kp[':db/id'],q[':db/id']) for [q] in rows for kp in q.get(':knowledge-point/_questions',[]))
    memberships = sorted((kp,q) for kp,q in membership_rows)
    leaf_ids = sorted({q for kp,q in memberships})
    def eid(value): return value.get(':db/id') if isinstance(value,dict) else value
    task_results = []
    for [task] in data['open-tasks']:
        activity = task[':learner-task/activity']
        steps = {step[':db/id']:step for step in activity.get(':activity/steps', [])}
        current = eid(activity.get(':activity/first-step')); route=[]; visited=set()
        while current in steps and current not in visited:
            visited.add(current); step=steps[current]; route.append(eid(step[':step/content'])); current=eid(step.get(':step/next'))
        items = task.get(':learner-task/items', [])
        presented = {eid(i.get(':task-item/content')) for i in items}
        future = [q for q in route if q in descendants and q not in presented]
        task_results.append({'task_id':task[':db/id'],'status':str(task[':learner-task/status'][':db/ident']), 'activity_id':activity[':db/id'], 'activity_type':str(activity[':activity/type'][':db/ident']), 'title':activity.get(':activity/title'), 'route':route, 'future_multipart_questions':future, 'presented_multipart_questions':sorted(presented & descendants), 'presented_count':len(items), 'learner_ids':[eid(v) for v in task.get(':learner/_activity',[])]})
    summary = {**identity, 'multipart_parent_count':len(roots), 'multipart_descendant_count':len(descendants), 'multipart_kp_question_count':len(leaf_ids), 'multipart_kp_membership_count':len(memberships), 'affected_kp_count':len({kp for kp,q in memberships}), 'multipart_kp_memberships':[{'kp':kp,'question':q} for kp,q in memberships], 'flagged':[{'question':q,'is_multipart':q in descendants,'kp_ids':[kp for kp,v in memberships if v==q]} for q in FLAGGED], 'open_task_count':len(task_results), 'tasks_with_future_multipart':[t for t in task_results if t['future_multipart_questions']], 'started_paused_tasks':[t for t in task_results if t['status'].rsplit('/',1)[-1] in ['started','paused']]}
    if '--memberships' not in sys.argv:
        for key in ['multipart_kp_question_count','multipart_kp_membership_count','affected_kp_count','multipart_kp_memberships']:summary.pop(key)
        for record in summary['flagged']:record.pop('kp_ids')
        summary['membership_count_note']='Optional global KP membership counts were not completed; route conclusions use the complete multipart descendant graph.'
    (directory/'tasks.json').write_text(json.dumps(task_results,indent=2,default=str)+'\n')
    (directory/'summary.json').write_text(json.dumps(summary,indent=2,default=str)+'\n')
    (HERE/'latest.txt').write_text(str(directory.relative_to(ROOT))+'\n')
    compact={key:value for key,value in summary.items() if key != 'multipart_kp_memberships'}
    print(json.dumps(compact,indent=2,default=str))

if __name__ == '__main__': main()
