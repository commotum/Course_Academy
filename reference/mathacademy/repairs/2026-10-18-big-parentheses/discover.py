import json, threading
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient
HERE=Path(__file__).resolve().parent
DB=EDBClient(Config(),threading.Event())
BASIS=json.loads((HERE/'identity.json').read_text())['basis']
def query(name,source,args):
 r=DB.query(source,args,HERE/'evidence',name,BASIS)
 (HERE/(name+'.json')).write_text(json.dumps(r,indent=2,default=str)+'\n')
 return r
if __name__=='__main__':
 topics=query('topics','''[:find (pull ?t [* {[:topic/knowledge-points :limit nil] [* {:knowledge-point/question-generator [*]}]}])
 :in $ ?kp :where [?t :topic/knowledge-points ?kp]]''',[17592186105744])
 print(json.dumps(topics,indent=2,default=str))
 ids=[r[0][':db/id'] for r in topics]
 lessons=query('lessons','''[:find (pull ?a [* {:activity/steps [* {:step/content [*]}]}])
 :in $ [?t ...] :where [?a :activity/scope ?t] [?a :activity/type :activity.type/lesson]]''',[ids])
 print(json.dumps(lessons,indent=2,default=str))
