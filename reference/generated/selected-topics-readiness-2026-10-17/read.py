from pathlib import Path
import json,sys,threading
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient
HERE=ROOT/'reference/generated/selected-topics-readiness-2026-10-17'
TOPICS=[17592186048115,17592186048150,17592186048189,17592186048191,17592186048245,17592186048332,17592186048403,17592186048470,17592186048489,17592186048528,17592186048557,17592186048569,17592186048697,17592186048777,17592186048813,17592186048842,17592186049053,17592186049119,17592186049131,17592186049146,17592186049195,17592186049332,17592186049380,17592186049406,17592186049443,17592186049481,17592186049486,17592186049774,17592186049879,17592186049930,17592186050101,17592186050245,17592186050271,17592186050283,17592186050375,17592186050409,17592186050420,17592186050473,17592186050489,17592186050542,17592186050571,17592186050608,17592186050628,17592186050649,17592186050771,17592186050783,17592186050789,17592186050898,17592186050902,17592186050905,17592186050985,17592186051059,17592186051084]
if __name__=='__main__':
 db=EDBClient(Config(capture_only=True),threading.Event()); identity=db.status()
 payload={**identity,'learner':17592186045416,'topics':TOPICS};(HERE/'input.json').write_text(json.dumps(payload,indent=2)+'\n')
 rows=db.query('[:find (pull ?t [:db/id :topic/title {:topic/knowledge-points [:db/id :knowledge-point/title :knowledge-point/questions]}]) :in $ [?t ...] :where [?t :topic/id _]]',[TOPICS],HERE,'topic-bank-sizes',identity['basis'])
 results=[]
 for row in rows:
  t=row[0];kps=t.get(':topic/knowledge-points',[])
  results.append({'topic':t[':db/id'],'title':t.get(':topic/title'),'kps':len(kps),'question_members':sum(len(k.get(':knowledge-point/questions',[])) for k in kps)})
 (HERE/'bank-sizes.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps({'basis':identity['basis'],'topics':len(results),'kps':sum(t['kps'] for t in results),'question_members':sum(t['question_members'] for t in results),'max_questions_per_topic':max(t['question_members'] for t in results)}))
