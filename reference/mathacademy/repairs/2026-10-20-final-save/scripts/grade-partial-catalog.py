import json,urllib.request,threading
from pathlib import Path
from scripts.config import Config
from scripts.database.client import EDBClient,QUESTION_PULL
from scripts.storage import read_json,atomic_json
root=Path('reference/mathacademy/repairs/2026-10-20-final-save/partials/grading');root.mkdir(exist_ok=True)
ids=[x['question_id']for x in read_json(root.parent/'source-judgments.json')['judgments']]
c=EDBClient(Config(),threading.Event());basis=c.basis()
rows=c.query('[:find (pull ?q '+QUESTION_PULL+') ?t :in $ [?id ...] :where [?q :question/math-academy-id ?id] [?kp :knowledge-point/questions ?q] [?t :topic/knowledge-points ?kp]]',[ids],root,'questions',basis)
assert len(rows)==11
results=[]
for q,t in rows:
 f,=q[':question/answer-fields'];correct=f[':answer-field/correct'][':db/id'];wrong=next(a[':db/id']for a in f[':answer-field/choices']if a[':db/id']!=correct)
 for answer,expected in [(correct,'correct'),(wrong,'incorrect')]:
  body={'topicId':t,'questionId':q[':db/id'],'responses':[{'fieldId':f[':db/id'],'choiceId':answer}]}
  req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(body).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'})
  d=json.load(urllib.request.urlopen(req,timeout=60));assert d['status']==expected,(q[':question/math-academy-id'],d)
  name=q[':question/math-academy-id']+'-'+expected
  atomic_json(root/(name+'.json'),{'request':body,'response':d})
  results.append({'question_id':q[':question/math-academy-id'],'expected':expected,'actual':d['status'],'basis':d['basis']})
atomic_json(root/'verification.json',{'status':'pass','checks':22,'questions':11,'read_only_preview':True,'learner_attempts_created':0,'results':results});print('11 questions passed 22 actual read-only grader checks')
