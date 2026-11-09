import json,urllib.request,concurrent.futures,copy
from pathlib import Path
H=Path(__file__).resolve().parent;jobs=[]
for d in sorted(H.glob('175*')):
 for q in json.loads((d/'questions-after.json').read_text()):
  fs=q.get(':question/answer-fields',[])
  if not fs:continue
  baseline=[{'fieldId':f[':db/id'],'choiceId':f[':answer-field/correct'][':db/id']}for f in fs]
  jobs.append({'topicId':int(d.name),'questionId':q[':db/id'],'responses':baseline,'expected':'correct'})
  for i,f in enumerate(fs):
   for a in f[':answer-field/choices']:
    if a[':db/id']==f[':answer-field/correct'][':db/id']:continue
    responses=copy.deepcopy(baseline);responses[i]['choiceId']=a[':db/id'];jobs.append({'topicId':int(d.name),'questionId':q[':db/id'],'responses':responses,'expected':'incorrect'})
def one(job):
 data={k:v for k,v in job.items()if k!='expected'}
 try:
  r=json.loads(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(data).encode(),headers={'Content-Type':'application/json'}),timeout=60).read());return {**job,'actual':r.get('status'),'basis':r.get('basis'),'passed':r.get('status')==job['expected'],'preview':r.get('preview')}
 except Exception as e:return {**job,'error':str(e),'passed':False}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(one,jobs))
(H/'grading-checks.json').write_text(json.dumps(rows,indent=2));print(json.dumps({'checks':len(rows),'questions':len({r['questionId']for r in rows}),'failures':[r for r in rows if not r['passed']],'bases':sorted({r.get('basis')for r in rows if r.get('basis')})},indent=2))
