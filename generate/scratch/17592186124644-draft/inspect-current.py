import sys,json,importlib.util,subprocess
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import database_environment
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from database import Database,QUESTION_PULL
from edn import dumps
P=D/'reference/replenishment/initial';P.mkdir(parents=True,exist_ok=True)
env=database_environment('math');db=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=env['EDB_ENDPOINT']));db.env=env
b=db.basis();query='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
kp=db.query(query,[17592186124644],P,'kp',b)[0][0]
(P/'before.edn').write_text(dumps(kp)+'\n')
print(json.dumps({'basis':b,'title':kp[':knowledge-point/title'],'id':str(kp[':knowledge-point/id']),'generator':kp.get(':knowledge-point/question-generator'),'practice_count':len(kp[':knowledge-point/questions']),'questions':[{'id':q[':db/id'],'source':q.get(':question/math-academy-id'),'level':str(q.get(':question/difficulty'))} for q in kp[':knowledge-point/questions']]},default=str))
r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-64e7aa312fccadb0'),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',env['EDB_ENDPOINT']],input='{"action":"inventory"}',env=env,capture_output=True,text=True,check=True,timeout=55)
x=json.loads(r.stdout);(P/'inventory.json').write_text(json.dumps(x,indent=2));print(json.dumps({'ok':x['ok'],'basis':x.get('data',{}).get('basis'),'jobs':[j for j in x.get('data',{}).get('jobs',[]) if j['knowledgePoint']==17592186124644]}))
