from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
import uuid
sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps, kw
HERE=Path(__file__).parent
TASKS=[17592186489498,17592186576141]
TASK_PULL='[* {:learner-task/status [:db/id :db/ident]} {:learner-task/activity [* {:activity/type [:db/id :db/ident]} {:activity/scope [:db/id :topic/title]} {[:activity/steps :limit nil] [* {:step/content [:db/id :knowledge-point/title :knowledge-point/canonical-example :question/id :tutorial/id]}]}]} {[:learner-task/items :limit nil] [* {:task-item/status [:db/id :db/ident]} {[:task-item/responses :limit nil] [*]} {:task-item/content [:db/id :question/math-academy-id {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/title]}]}]} {[:learner/_activity :limit nil] [:db/id :learner/id]}]'
def main():
 db=Publisher.from_environment(source=':agent/gpt-6.1-sol-high').client
 ident=db.status();basis=ident['basis'];out=HERE/f'capture-{basis}';out.mkdir(exist_ok=True)
 def read(name,q,inputs):return db.query(q,inputs,out,name,basis)
 tasks=read('tasks','[:find (pull ?t '+TASK_PULL+') :in $ [?t ...] :where [?t :learner-task/id _]]',[TASKS])
 learners=sorted({l[':db/id'] for [t] in tasks for l in t[':learner/_activity']})
 topics=sorted({t[':learner-task/activity'][':activity/scope'][':db/id'] for [t] in tasks})
 specs={
 'learner':('[:find (pull ?l [* {[:learner/performance :limit nil] [*]}]) :in $ [?l ...] :where [?l :learner/id _]]',[learners]),
 'profiles':('[:find (pull ?p [*]) :in $ [?l ...] [?topic ...] :where [?l :learner/knowledge-profile ?p] [?p :progress/topic ?topic]]',[learners,topics]),
 'source':('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]',[kw('agent/gpt-6.1-sol-high')]),
 'attributes':('[:find ?a ?ident :where [?a :db/ident ?ident] [?a :db/valueType _]]',[]),
 }
 with ThreadPoolExecutor(max_workers=3) as pool:
  fs={n:pool.submit(read,n,*a) for n,a in specs.items()};data={n:f.result() for n,f in fs.items()}
 snapshot={**ident,'tasks':tasks,**data};(out/'snapshot.edn').write_text(dumps(snapshot)+'\n');(out/'snapshot.json').write_text(json.dumps(snapshot,indent=2,default=str)+'\n')
 (HERE/'capture-directory.txt').write_text(str(out.relative_to(ROOT))+'\n')
 for [task] in tasks:
  items={i[':db/id']:i for i in task.get(':learner-task/items',[])}
  successors={i[':task-item/next'][':db/id'] for i in items.values() if ':task-item/next' in i}
  first=list(set(items)-successors);assert len(first)==1
  chain=[];i=first[0]
  while i:
   v=items[i];chain.append({'item':i,'question':v[':task-item/content'][':db/id'],'kp':v[':task-item/content'].get(':knowledge-point/_questions',[]),'state':v[':task-item/status'][':db/ident'],'seconds':v.get(':task-item/elapsed-seconds'),'next':v.get(':task-item/next'),'deferred':v.get(':task-item/deferred-step')});i=v.get(':task-item/next',{}).get(':db/id')
  print(json.dumps({'task':task[':db/id'],'state':task[':learner-task/status'][':db/ident'],'title':task[':learner-task/activity'][':activity/title'],'chain':chain},indent=2,default=str))
 print(json.dumps({'basis':basis,'directory':str(out),'learners':learners,'profiles':data['profiles']},indent=2,default=str))
if __name__=='__main__':main()
