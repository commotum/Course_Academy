import sys,json,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).parent
sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import database_environment
sys.path.insert(0,str(ROOT/'scripts/question_capture'));from database import Database
D=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']));D.env=database_environment('math')
r=subprocess.run([str(ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',D.args.endpoint],input='{"action":"inventory"}',env=D.env,text=True,capture_output=True,check=True);inv=json.loads(r.stdout)['data'];(HERE/'reference/initial/inventory.json').write_text(json.dumps(inv,indent=2));b=inv['basis']
k=D.query((HERE/'reference/source-query.edn').read_text(),[17592186100894],HERE/'reference/initial','kp',b)[0][0]
(HERE/'source.json').write_text(json.dumps({'database':'math','basis':b,'lineage':inv['lineage'],'record':k},indent=2,default=str))
print('basis',b,'generator',k.get(':knowledge-point/question-generator'))
print('jobs',[j for j in inv['jobs'] if j['knowledgePoint']==17592186100894])
for q in k[':knowledge-point/questions']:
 print('\n',q.get(':question/math-academy-id'),q.get(':question/difficulty'),q[':question/problem'],q.get(':question/worked-solution','MISSING'))
 for f in q[':question/answer-fields']:print(f[':answer-field/key'],f[':answer-field/type'],[(a[':answer/value'],a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')) for a in f[':answer-field/choices']])
