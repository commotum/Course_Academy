import json,sys,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]; HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps
from serve_graph_explorer import database_environment
from inventory_jobs import save
ENV=database_environment('math');DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
Q='''[* {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/correct [* {:answer/type [:db/ident]}]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/ident]}]}]}]'''
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+Q+'} {[:knowledge-point/questions :limit nil] '+Q+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
if __name__=='__main__':
 out=HERE/'reference'; b=DB.basis(); kp=DB.query(QUERY,[17592186087866],out,'source',b)[0][0]
 save(out/'source.json',{'database':'math','basis':b,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','record':json.loads(json.dumps(kp,default=str))})
 req={'database':'math','learner':'59d5cf13-351c-4114-be19-4c3bb64ee051','topics':[17592186050608],'activity_type':'lesson','after_basis':None,'lineage':None,'at':None}
 r=subprocess.run([str(ROOT/'.local/generate/find-candidates-b13a7928a9573a2f')],input=json.dumps(req),env=ENV,capture_output=True,text=True,check=True)
 save(out/'inventory-before.json',json.loads(r.stdout))
 print('Basis',b,'generator',kp.get(':knowledge-point/question-generator'))
 for q in kp[':knowledge-point/questions']:
  print('\n',q.get(':question/math-academy-id'),q[':db/id'],q.get(':question/difficulty'),q[':question/problem']);print(q[':question/worked-solution'])
  for f in q[':question/answer-fields']:
   print('FIELD',f[':answer-field/type'],f[':answer-field/key']);print('BANK',[(a[':answer/value'],a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')) for a in f[':answer-field/choices']])
 print('INVENTORY',[(k['db/id'],k['inventory']) for t in json.loads(r.stdout)['topics'] for k in t['knowledge_points'] if k['db/id']==17592186087866])
