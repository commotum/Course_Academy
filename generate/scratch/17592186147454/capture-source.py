import json,sys,subprocess
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]; HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from serve_graph_explorer import database_environment
from inventory_jobs import save
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']));DB.env=ENV
NATIVE=ROOT/'.local/graph-explorer/learning-ef48cfde3a25d91e'
def inventory(path):
 r=subprocess.run([str(NATIVE),'math','59d5cf13-351c-4114-be19-4c3bb64ee051',DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
 x=json.loads(r.stdout);assert x['ok'];save(path,x['data']);return x['data']
def main():
 inv=inventory(HERE/'reference/inventory-initial.json');basis=inv['basis']
 kp=DB.query((HERE/'reference/source-query.edn').read_text(),[17592186147454],HERE/'reference','source',basis)[0][0]
 save(HERE/'source.json',{'database':'math','basis':basis,'lineage':inv['lineage'],'record':json.loads(json.dumps(kp,default=str))})
 print(json.dumps({'basis':basis,'lineage':inv['lineage'],'generator':kp.get(':knowledge-point/question-generator'),'jobs':[j for j in inv['jobs'] if j['knowledgePoint']==17592186147454]},default=str))
 for q in kp[':knowledge-point/questions']:
  print('\n',q.get(':question/math-academy-id'),q.get(':question/difficulty'),q[':question/problem'])
  for f in q[':question/answer-fields']:
   print([(a[':answer/value'],a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')) for a in f[':answer-field/choices']])
if __name__=='__main__':main()
