import json,threading
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient,QUESTION_PULL
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DB=EDBClient(Config(),threading.Event());BASIS=json.loads((HERE/'identity.json').read_text())['basis']
def query(name,text,args):
 rows=DB.query(text,args,HERE/'evidence',name,BASIS);(HERE/(name+'.json')).write_text(json.dumps(rows,indent=2,default=str)+'\n');return rows
if __name__=='__main__':
 q=query('questions','''[:find (pull ?q '''+QUESTION_PULL+''') :in $ ?topic :where [?topic :topic/knowledge-points ?kp] (or-join [?kp ?q] [?kp :knowledge-point/questions ?q] [?kp :knowledge-point/canonical-example ?q])]''',[17592186050208])
 topic=query('topic','[:find (pull ?t [* {:topic/knowledge-points [* {:knowledge-point/question-generator [*]}]}]) :in $ ?t :where [?t :topic/id _]]',[17592186050208])
 print('QUESTIONS',len(q))
 for [question] in q:
  print('\nQUESTION',question[':db/id'],question.get(':question/math-academy-id','generated'))
  print(question[':question/problem']);print(question.get(':question/worked-solution',''))
  for f in question.get(':question/answer-fields',[]):
   print('CHOICES',[a.get(':answer/value') for a in f.get(':answer-field/choices',[])])
 print('\nGENERATORS',[(kp[':db/id'],kp.get(':knowledge-point/question-generator')) for kp in topic[0][0][':topic/knowledge-points']])
