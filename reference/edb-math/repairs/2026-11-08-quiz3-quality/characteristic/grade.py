import json,urllib.request,concurrent.futures
from pathlib import Path
base=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic')
def grade(job):
 topic,q,f,a=job;body={'topicId':topic,'questionId':q[':db/id'],'responses':[{'fieldId':f[':db/id'],'choiceId':a[':db/id']}]};req=urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',json.dumps(body).encode(),headers={'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(req,timeout=45)as r:result=json.load(r)
  actual=result.get('status',result.get('result'));expected='correct'if a[':db/id']==f[':answer-field/correct'][':db/id']else'incorrect'
  return {'question':q[':db/id'],'mid':q[':question/math-academy-id'],'field':f[':db/id'],'choice':a[':db/id'],'expected':expected,'actual':actual,'passed':actual==expected,'response':result}
 except Exception as e:return {'question':q[':db/id'],'field':f[':db/id'],'choice':a[':db/id'],'error':str(e),'passed':False}
for d in sorted(base.glob('175*')):
 jobs=[(int(d.name),q,f,a)for q in json.loads((d/'questions-after.json').read_text())for f in q.get(':question/answer-fields',[])for a in f[':answer-field/choices']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(grade,jobs))
 (d/'grading-checks.json').write_text(json.dumps(rows,indent=2)+'\n');print(d.name,len(rows),'passed',sum(r['passed']for r in rows),'sample',str(rows[:1])[:300],flush=True)
