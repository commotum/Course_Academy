import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from serve_graph_explorer import database_environment
from database import Database
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
KP=17592186133881;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
QUERY=(ROOT/'generate/scratch/17592186133876/reference/source-query.edn').read_text()
def scoped(kp,b,seen):
 entities={str(i+1):{'db/ident':name} for i,name in enumerate(('question.difficulty/easy','question.difficulty/moderate','question.difficulty/hard','answer-field.type/checkbox','answer-field.type/radio','answer.type/text'))}
 def enum(x):return str(x[':db/ident']).lstrip(':')
 for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]:
  entities[str(q[':db/id'])]={'question/id':str(q[':question/id']),'question/problem':q[':question/problem'],'question/answer-fields':[f[':db/id'] for f in q.get(':question/answer-fields',[])]}
  if ':question/difficulty' in q:entities[str(q[':db/id'])]['question/difficulty']=enum(q[':question/difficulty'])
  for f in q.get(':question/answer-fields',[]):
   entities[str(f[':db/id'])]={'answer-field/key':f[':answer-field/key'],'answer-field/type':enum(f[':answer-field/type']),'answer-field/choices':[a[':db/id'] for a in f[':answer-field/choices']],'answer-field/correct':f[':answer-field/correct'][':db/id']}
   for a in f[':answer-field/choices']:entities[str(a[':db/id'])]={'answer/type':enum(a[':answer/type']),'answer/value':a[':answer/value']}
 entities[str(KP)]={'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']],'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id'],'knowledge-point/title':kp[':knowledge-point/title']}
 return {'basis_t':b,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)}
def available(kp,b,path):
 path.mkdir(parents=True,exist_ok=True)
 shown=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]',[KP,LEARNER],path,'shown',b,history=True)
 reserved=DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?s] (or [?s :db/ident :learner-task.status/started] [?s :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]',[KP,LEARNER],path,'reserved',b)
 (path/'snapshot.json').write_text(json.dumps(scoped(kp,b,{row[0] for row in shown+reserved})))
 subprocess.run([str(ROOT/'generate/scratch/17592186110754/check-pool'),str(path/'snapshot.json'),str(path/'available.json')],check=True,capture_output=True)
 return json.load(open(path/'available.json'))
if __name__=='__main__':
 b=DB.basis();kp=DB.query(QUERY,[KP],P/'reference/current','kp',b)[0][0];print(json.dumps(available(kp,b,P/'reference/current')))
