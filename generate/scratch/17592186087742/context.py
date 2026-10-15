import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from serve_graph_explorer import database_environment
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));DB.env=database_environment('math')
KP=17592186087742;LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
QUERY=(ROOT/'generate/scratch/17592186105908/reference/initial/source-query.edn').read_text()
def plain(v):
 if isinstance(v,dict):return {str(k):plain(x)for k,x in v.items()}
 if isinstance(v,(list,tuple,set)):return [plain(x)for x in v]
 if isinstance(v,(str,int,float,bool))or v is None:return v
 return str(v)
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(plain(v),indent=2,ensure_ascii=False)+'\n')
def inventory(p):
 r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-17e1b9defebc55b9'),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=90);x=json.loads(r.stdout);assert x['ok'];save(p,x['data']);return x['data']
if __name__=='__main__':
 inv=inventory(HERE/'reference/inventory-initial.json');b=inv['basis'];kp=DB.query(QUERY,[KP],HERE/'reference/initial','kp',b)[0][0];save(HERE/'source.json',{'database':'math','basis':b,'lineage':inv['lineage'],'record':kp});print('basis',b,'generator',kp.get(':knowledge-point/question-generator'));print('jobs',[j for j in inv['jobs']if j['knowledgePoint']==KP])
 for q in kp[':knowledge-point/questions']:
  print(q.get(':question/math-academy-id'),q.get(':question/difficulty'),'problem',q[':question/problem']);print('solution',q.get(':question/worked-solution'))
  for f in q.get(':question/answer-fields',[]):print('field',f[':answer-field/key'],'correct',f.get(':answer-field/correct',{}).get(':answer/value'),'choices',[a[':answer/value']for a in f[':answer-field/choices']])
