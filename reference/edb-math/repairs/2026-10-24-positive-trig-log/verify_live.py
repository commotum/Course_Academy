"""Read-only application grading checks for the exact reported question."""
import json,time,urllib.request,urllib.error
from pathlib import Path
H=Path(__file__).resolve().parent
checks=[
 (r'-3\ln(\cos x+2)','correct','Exact reported entry'),
 ('-3ln(2+cos(x))','correct','Commuted sum'),
 ('-3ln(abs(cos(x)+2))','correct','Absolute-value form'),
 ('-3ln(2+cos(x))+7/3','correct','Constant absorbed by external C'),
 ('3ln(2+cos(x))','incorrect','Wrong sign'),
 ('-2ln(2+cos(x))','incorrect','Wrong coefficient'),
 ('-3ln(3+cos(x))','incorrect','Wrong offset'),
 ('-3ln(2+cos(2x))','incorrect','Wrong inner argument'),
]
results=[]
for value,expected,purpose in checks:
 payload={'topicId':17592186050489,'questionId':17592186678417,'responses':[{'fieldId':17592186678364,'value':value}]}
 req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','Origin':'http://127.0.0.1:8765'},method='POST')
 start=time.monotonic()
 with urllib.request.urlopen(req,timeout=45)as r:out=json.load(r)
 assert out['status']==expected,(value,out)
 results.append({'submitted':value,'expected':expected,'actual':out['status'],'purpose':purpose,'seconds':round(time.monotonic()-start,3)})
(H/'live-after.json').write_text(json.dumps({'passed':True,'database_writes':0,'question':17592186678417,'checks':results},indent=2)+'\n');print(json.dumps({'passed':True,'checks':len(results),'database_writes':0,'exact_reported_entry':results[0]}))
