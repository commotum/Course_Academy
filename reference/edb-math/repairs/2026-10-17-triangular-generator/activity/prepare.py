"""Prepare a reversible activity transaction fragment; never commit live data."""
from pathlib import Path
import json,sys,hashlib,argparse,datetime,uuid
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Cargo.toml').exists())
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(HERE))
from audit import TASK_PULL,TASKS
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps,loads,kw,Tagged
SOURCE=':agent/gpt-6.1-sol-high'
TASK=17592186413350;BAD_ITEM=17592186576280;BAD_QUESTION=17592186487475
GOOD=[17592186576278,17592186576279];LEARNER=17592186045416

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--basis',type=int);args=parser.parse_args()
 db=Publisher.from_environment(source=SOURCE).client
 identity=db.status();basis=args.basis if args.basis is not None else identity['basis'];assert basis<=identity['basis'];identity={**identity,'basis':basis};out=HERE/f'prepared-{basis}';out.mkdir(exist_ok=True)
 def read(name,q,inputs):return db.query(q,inputs,out,name,basis)
 [[task]]=read('task','[:find (pull ?t '+TASK_PULL+') :in $ ?t :where [?t :learner-task/id _]]',[TASK])
 assert task[':learner-task/status'][':db/ident']==':learner-task.status/paused'
 assert task.get(':learner-task/xp-earned',0)==0 and ':learner-task/finished-at' not in task
 assert ':learner-task/active-item' not in task
 items={i[':db/id']:i for i in task[':learner-task/items']}
 assert set(items)==set(GOOD+[BAD_ITEM])
 assert items[BAD_ITEM][':task-item/content'][':db/id']==BAD_QUESTION
 assert items[BAD_ITEM][':task-item/status'][':db/ident']==':task-item.status/correct'
 assert ':task-item/next' not in items[BAD_ITEM]
 assert items[GOOD[0]][':task-item/next'][':db/id']==GOOD[1]
 assert items[GOOD[1]][':task-item/next'][':db/id']==BAD_ITEM
 elapsed=sum(items[i][':task-item/elapsed-seconds'] for i in GOOD)
 forms=[
  [kw('db/retract'),TASK,kw('learner-task/items'),BAD_ITEM],
  [kw('db/retract'),GOOD[-1],kw('task-item/next'),BAD_ITEM],
  [kw('db/cas'),TASK,kw('learner-task/elapsed-seconds'),task[':learner-task/elapsed-seconds'],elapsed],
  [kw('db/ensure'),TASK,kw('learner-task/validate')],
 ]
 accuracy=json.loads((HERE/'accuracy/audit.json').read_text())
 assert accuracy['nativeControlMatchedEveryTransaction'] and accuracy['nativeControlEqualsCurrent']
 assert accuracy['badItem']==BAD_ITEM and accuracy['retentionEvents']==0
 # A content-only basis advance is safe, but any changed learner evidence must
 # rerun the native control/counterfactual replay rather than silently reuse it.
 [[dynamic]]=read('all-dynamic-state','[:find (pull ?l [{[:learner/knowledge-profile :limit nil] [*]} {:learner/performance [*]}]) :in $ ?l :where [?l :learner/id _]]',[LEARNER])
 def record(e):
  result={}
  for key,value in e.items():
   attr=str(key).lstrip(':')
   if attr=='db/id':continue
   if isinstance(value,dict) and set(value)=={':db/id'}:value=value[':db/id']
   elif attr in {'progress/memory-at','progress/last-direct-at'}:
    value={'$instant':round(datetime.datetime.fromisoformat(value.replace('Z','+00:00')).timestamp()*1000)}
   elif isinstance(value,uuid.UUID):value=str(value)
   result[attr]=value
  return result
 observed={str(e[':db/id']):record(e) for e in dynamic[':learner/knowledge-profile']+[dynamic[':learner/performance']]}
 expected=json.loads((HERE/'accuracy/before.json').read_text())
 assert observed==expected,'Learner profile/performance membership or state changed since native replay; rerun accuracy/preview before preparing'
 all_state_hash=hashlib.sha256(json.dumps(observed,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 corrections=loads((HERE/'accuracy/accuracy-forms.edn').read_text())
 for form in corrections:
  if str(form[2]) in {':progress/last-direct-at',':progress/memory-at'}:
   for index in range(3,len(form)):
    if form[index] is not None:form[index]=Tagged('inst',form[index])
 forms.extend(corrections)
 state_ids=sorted({f[1] for f in corrections if f[1]!=LEARNER}|set(accuracy['detachedProfiles']))
 states=read('state','[:find (pull ?e [* {[:learner/knowledge-profile :limit nil] [:db/id]}]) :in $ [?e ...] :where [?e _ _]]',[state_ids+[LEARNER]])
 byid={e[':db/id']:e for [e] in states}
 for f in corrections:
  if str(f[0])==':db/ensure':continue
  eid,attr=f[1],str(f[2]);old=byid[eid].get(attr)
  if attr==':learner/knowledge-profile':assert f[3] in [e[':db/id'] for e in old]
  elif isinstance(f[3],Tagged):assert old==f[3].value
  else:assert old==f[3],(eid,attr,old,f[3])
 groups=[['tasks',TASK_PULL,[TASK]],['items','[* {[:task-item/responses :limit nil] [*]}]',GOOD+[BAD_ITEM]],['state','[*]',state_ids],['learner','[* {[:learner/knowledge-profile :limit nil] [:db/id]}]',[LEARNER]]]
 for name,v in [('transaction-fragment.edn',forms),('native-pulls.edn',groups)]:
  content=dumps(v)+'\n';(HERE/name).write_text(content);(out/name).write_text(content)
 (HERE/'native/input.json').write_text(json.dumps({'learner':LEARNER,'tasks':[TASK],'profiles':state_ids},indent=2)+'\n')
 plan={**identity,'source':SOURCE,'task':TASK,'removed_items':[BAD_ITEM],'removed_questions':[BAD_QUESTION],'retained_items':GOOD,'affected_state_ids':state_ids,'elapsed_before':task[':learner-task/elapsed-seconds'],'elapsed_after':elapsed,'accuracy_basis':accuracy['basis'],'entire_dynamic_state_freshly_verified':True,'entire_dynamic_state_count':len(observed),'entire_dynamic_state_sha256':all_state_hash,'bad_answer_basis':accuracy['badBasis'],'accuracy_events_replayed':len(accuracy['events']),'detached_profiles':accuracy['detachedProfiles'],'fragment_sha256':hashlib.sha256((HERE/'transaction-fragment.edn').read_bytes()).hexdigest(),'notes':['No durable writes. Combine this fragment with the content retirement in one guarded transaction.','Native control replay exactly reproduces every accuracy event from the bad answer through its captured basis.','Current state was re-read and checked against every correction precondition.','Bad item, response and newly-created profile records remain archived; learner/task membership is detached.','All valid tutorial/example work, XP, retention, mastery and assessment evidence are preserved.'],'application_preview_command':[str(HERE/'native/preview'),'TRANSACTION_DIRECTORY',SOURCE,str(basis),str(HERE/'native/input.json')]}
 for p in [HERE/'fragment-plan.json',out/'fragment-plan.json']:p.write_text(json.dumps(plan,indent=2)+'\n')
 print(json.dumps(plan,indent=2))
if __name__=='__main__':main()
