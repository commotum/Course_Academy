import json,urllib.request,copy,concurrent.futures,time
from pathlib import Path
H=Path(__file__).resolve().parent;cases=[]
for d in sorted(H.glob('175*')):
 for q in json.loads((d/'questions-committed.json').read_text()):
  fs=q.get(':question/answer-fields',[])
  if not fs:continue
  base=[]
  for f in fs:
   a=f[':answer-field/correct'];typ=f[':answer-field/type'][':db/ident'];base.append({'fieldId':f[':db/id'],**({'value':a[':answer/value']}if typ.endswith('/blank')else{'choiceId':a[':db/id']})})
  cases.append({'topic':int(d.name),'question':q[':db/id'],'mid':q[':question/math-academy-id'],'responses':base,'expected':'correct','kind':'correct full response'})
  for i,f in enumerate(fs):
   typ=f[':answer-field/type'][':db/ident']
   if typ.endswith('/blank'):
    alt={'fieldId':f[':db/id'],'value':'1234567'};rs=copy.deepcopy(base);rs[i]=alt;cases.append({'topic':int(d.name),'question':q[':db/id'],'mid':q[':question/math-academy-id'],'responses':rs,'expected':'incorrect','kind':'wrong blank'})
   else:
    for a in f[':answer-field/choices']:
     if a[':db/id']==f[':answer-field/correct'][':db/id']:continue
     rs=copy.deepcopy(base);rs[i]={'fieldId':f[':db/id'],'choiceId':a[':db/id']};cases.append({'topic':int(d.name),'question':q[':db/id'],'mid':q[':question/math-academy-id'],'responses':rs,'expected':'incorrect','kind':'single-field alternative'})
cases.append({'topic':17592186049370,'question':17592186229647,'mid':'q-332773','responses':[{'fieldId':17592186228106,'value':'2-4e^{-3x}'}],'expected':'correct','kind':'equivalent blank'})
(H/'grading-cases.json').write_text(json.dumps(cases,indent=2));results=[]
def run(c):
 p={'topicId':c['topic'],'questionId':c['question'],'responses':c['responses']}
 try:
  data=json.loads(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765/api/preview-answer',data=json.dumps(p).encode(),headers={'Content-Type':'application/json'}),timeout=90).read())
  return{**c,'actual':data.get('status'),'basis':data.get('basis'),'preview':data.get('preview'),'passed':data.get('status')==c['expected'],'field_grades':[{'id':f.get('id'),'grade':f.get('grade')}for f in data.get('fields',[])]}
 except Exception as e:return{**c,'passed':False,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:
 for r in ex.map(run,cases):
  results.append(r)
  if len(results)%100==0:print('graded',len(results),'of',len(cases),flush=True)
(H/'grading-checks.json').write_text(json.dumps(results,indent=2));summary={'checks':len(results),'passed':sum(r['passed']for r in results),'failures':[r for r in results if not r['passed']],'database_writes':0};(H/'grading-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
