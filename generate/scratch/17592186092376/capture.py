import json,sys,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]; HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database,QUESTION_PULL
from edn import dumps,loads
from serve_graph_explorer import database_environment
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
KP=17592186092376
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
def plain(v):
 if isinstance(v,dict):return {str(k):plain(x)for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [plain(x)for x in v]
 if isinstance(v,(str,int,float,bool))or v is None:return v
 return str(v)
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(plain(v),indent=2)+'\n')
def inventory(p):
 r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-17e1b9defebc55b9'),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok'];save(p,x['data']);return x['data']
def read(p,basis):return DB.query(QUERY,[KP],p,'kp',basis)[0][0]
if __name__=='__main__':
 p=HERE/'reference/initial';inv=inventory(p/'inventory.json');b=inv['basis'];x=read(p,b);save(HERE/'source.json',{'basis':b,'lineage':inv['lineage'],'record':x});print(b,inv['lineage']);print('KP',x[':knowledge-point/title'],'generator',x.get(':knowledge-point/question-generator'));print('job',[j for j in inv['jobs']if j['knowledgePoint']==KP]);
 for q in x[':knowledge-point/questions']:print(q[':db/id'],q.get(':question/math-academy-id'),q.get(':question/difficulty',{}).get(':db/ident'),'complete',bool(q.get(':question/worked-solution'))and all(f.get(':answer-field/correct')for f in q.get(':question/answer-fields',[])))
