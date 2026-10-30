import sys,json,uuid,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
HERE=Path(__file__).resolve().parent
BASIS=11863; TOPIC=17592186049485
db=Publisher.from_environment(source=':agent/codex').client
status=db.status(); assert status['lineage']=='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1',status
(HERE/'status.json').write_text(json.dumps(status,indent=2))
def query(q,inputs,name):return db.query(q,inputs,HERE,name,basis=BASIS)
A='[:db/id :answer/id {:answer/type [:db/ident]} :answer/value :answer/feedback]'
AF='[:db/id :answer-field/id :answer-field/key {:answer-field/type [:db/ident]} {[:answer-field/choices :limit nil] '+A+'} {[:answer-field/correct :limit nil] '+A+'}]'
Q='[:db/id :question/id :question/math-academy-id :question/retired :question/requires-calculator {:question/difficulty [:db/ident]} :question/problem :question/worked-solution {[:question/answer-fields :limit nil] '+AF+'}]'
KP='[:db/id :knowledge-point/id :knowledge-point/title :knowledge-point/math-academy-id {:knowledge-point/canonical-example '+Q+'} {[:knowledge-point/questions :limit nil] '+Q+'} {:knowledge-point/question-generator [:db/id :question-generator/id :question-generator/script]}]'
T='[:db/id :topic/id :topic/title :topic/math-academy-id {[:topic/knowledge-points :limit nil] [:db/id]}]'
topic=query('[:find (pull ?e '+T+') :in $ ?e :where [?e :topic/id _]]',[TOPIC],'topic')[0][0]
kps=query('[:find (pull ?e '+KP+') :in $ [?e ...] :where [?e :knowledge-point/id _]]',[[p[':db/id'] for p in topic[':topic/knowledge-points']]],'kps')
CONTENT='[:db/id :tutorial/id :tutorial/title :tutorial/math-academy-id :tutorial/content :question/id :knowledge-point/id :multistep/id :assigned-problem/id]'
ACT='[:db/id :activity/id :activity/title {:activity/type [:db/ident]} {:activity/first-step [:db/id]} {[:activity/steps :limit nil] [:db/id :step/id :step/math-academy-id {:step/next [:db/id]} {:step/content '+CONTENT+'}]}]'
activities=query('[:find (pull ?e '+ACT+') :in $ ?topic :where [?e :activity/scope ?topic]]',[TOPIC],'activities')
snapshot={'basis':BASIS,'topic':topic,'kps':[r[0] for r in kps],'activities':[r[0] for r in activities]}
questions={q[':db/id']:q for kp in snapshot['kps'] for q in [kp.get(':knowledge-point/canonical-example'),*kp.get(':knowledge-point/questions',[])] if q}
extra_ids=[s[':step/content'][':db/id'] for a in snapshot['activities'] for s in a.get(':activity/steps',[]) if ':question/id' in s.get(':step/content',{}) and s[':step/content'][':db/id'] not in questions]
if extra_ids:
 for r in query('[:find (pull ?e '+Q+') :in $ [?e ...] :where [?e :question/id _]]',[extra_ids],'step-questions'):questions[r[0][':db/id']]=r[0]
snapshot['questions']=list(questions.values())
(HERE/'snapshot.json').write_text(json.dumps(jsonable(snapshot),indent=2,ensure_ascii=False)+'\n')
fields={}
math_answers=set()
def walk(obj,path='snapshot'):
 if isinstance(obj,dict):
  eid=obj.get(':db/id')
  if str(obj.get(':answer/type',{}).get(':db/ident'))==':answer.type/math':math_answers.add(eid)
  for k,v in obj.items():
   if isinstance(v,str):
    key=(eid,k,v);fields.setdefault(key,{'entity':eid,'attribute':k[1:],'value':v,'paths':[]})['paths'].append(path)
   elif isinstance(v,(dict,list)):walk(v,path+'/'+k)
 elif isinstance(obj,list):
  for i,v in enumerate(obj):walk(v,path+'/'+str(i))
walk(snapshot)
inventory=list(fields.values())
for f in inventory:
 f['bare_math']=f['attribute']=='answer/value' and f['entity'] in math_answers
 f['has_math']=f['bare_math'] or bool(re.search(r'\$|\\\(|\\\[',f['value']))
(HERE/'field-inventory.json').write_text(json.dumps(jsonable(inventory),indent=2,ensure_ascii=False)+'\n')
render=[f for f in inventory if f['has_math'] or f['attribute'] in ('tutorial/content','question/problem','question/worked-solution','answer/value','answer/feedback')]
(HERE/'render-input.json').write_text(json.dumps(jsonable(render),indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'basis':BASIS,'kps':len(kps),'activities':len(activities),'questions':len(questions),'fields':len(inventory),'render_fields':len(render)},indent=2))
