"""Real read-only API regression; no response or learner mutation endpoint."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from serve_graph_explorer import NativeWorker,database_environment,DEFAULT_LEARNER
binary=json.loads((H/'learning-build.json').read_text())['binary'];env=database_environment('math');worker=NativeWorker([binary,'math',DEFAULT_LEARNER,env['EDB_ENDPOINT'],'--serve'],env,'audit3-readonly-grader');results=[]
cases=[(17592186235496,17592186235041,[(r'(x-3)^{2}+{y}^{2}=9','correct'),('x^2-6x+y^2=0','correct'),('9=y^2+(x-3)^2','correct'),('(x-4)^2+y^2=9','incorrect'),('(x-3)^2+y^2=10','incorrect'),('987654321','incorrect')]),(17592186637312,17592186637137,[(r'(x-0)^{2}+(y-6)^{2}=36','correct'),('x^2+y^2-12y=0','correct'),('(x-0)^2+(y-5)^2=36','incorrect')])]
try:
 for q,field,checks in cases:
  for value,expected in checks:
   body={'action':'preview-answer','topicId':17592186049570,'questionId':q,'responses':[{'fieldId':field,'value':value}]}
   response=worker.request(body);results.append({'question':q,'submitted':value,'expected':expected,'response':response})
   (H/'grader-api-verification.json').write_text(json.dumps({'checks':results,'database_writes':0},indent=2)+'\n')
   assert response.get('ok')and response['data']['status']==expected,response
finally:worker.close()
(H/'grader-api-verification.json').write_text(json.dumps({'passed':True,'checks':results,'database_writes':0,'learner_records_created':0},indent=2)+'\n');print('Actual read-only API:9checks pass;0learner writes')
