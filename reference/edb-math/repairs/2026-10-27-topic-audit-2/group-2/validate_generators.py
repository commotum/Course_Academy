import json,copy,subprocess,re,sys,os
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];samples=json.loads((H/'generator-full-samples.json').read_text());g=next(x for x in json.loads((H/'generators.json').read_text())if x['kp']==17592186064245);staged=H/'generators'/str(g['kp'])/Path(g['path']).name;fresh=[]
info=next(x for x in json.loads((H/'generator-full-invocations.json').read_text())if x['kp']==g['kp']);env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':'/tmp/course-academy-kp17592186192790-checkdeps'}
for j in info['invocations']:
 if not j.get('passed'):continue
 p=subprocess.run([sys.executable,str(staged),'--difficulty',j['band'],'--count',str(j['records']),'--seed','271028','--format','json',*j['args']],capture_output=True,text=True,env=env,check=True)
 for record in json.loads(p.stdout):
  assert '$$'in record['question'][':question/problem'];fresh.append({'kp':g['kp'],'band':j['band'],'record':record,'kind':'staged-successor','arguments':j['args']})
samples=[x for x in samples if x['kp']!=g['kp']]+fresh
(H/'generator-final-samples.json').write_text(json.dumps(samples,indent=2)+'\n');(H/'generator-staged-samples.json').write_text(json.dumps(fresh,indent=2)+'\n');checks=[];fields=[]
for i,s in enumerate(samples):
 record=copy.deepcopy(s['record']);q=record['question'];label=str(s['kp'])+'/'+str(i);tests=[]
 fields.extend([{'entity':label,'attribute':a,'value':q[a]}for a in[':question/problem',':question/worked-solution']])
 for j,f in enumerate(q[':question/answer-fields']):
  kind=f[':answer-field/type'];kind=kind[':db/ident']if isinstance(kind,dict)else kind;f[':answer-field/type']=kind
  correct=f[':answer-field/correct'];cid=correct[':answer/id']if isinstance(correct,dict)else correct[1];f[':answer-field/correct']=[':answer/id',cid]
  right=next(a for a in f[':answer-field/choices']if a[':answer/id']==cid)
  if kind==':answer-field.type/checkbox':fields.append({'entity':label,'attribute':'answer-field/key','value':f[':answer-field/key']})
  for a in f[':answer-field/choices']:
   at=a[':answer/type'];at=at[':db/ident']if isinstance(at,dict)else at;a[':answer/type']=at;fields.append({'entity':label,'attribute':'answer/value','value':a[':answer/value'],'bare_math':at==':answer.type/math'})
  if kind==':answer-field.type/blank':tests.extend([{'field_index':j,'submitted':right[':answer/value'],'expected':'accepted','purpose':'Fresh canonical value accepted'},{'field_index':j,'submitted':'987654321','expected':'rejected','purpose':'Incorrect function/scalar rejected'}])
  else:tests.extend({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==cid else'rejected','purpose':'Complete fresh bank grading'}for a in f[':answer-field/choices'])
 checks.append({'label':label,'record':record,'checks':tests})
(H/'generator-grading-input.json').write_text(json.dumps(checks,indent=2)+'\n');(H/'generator-render-input.json').write_text(json.dumps(fields,indent=2)+'\n');subprocess.run([str(H.parent/'check-engine'),str(H/'generator-grading-input.json'),str(H/'generator-grading.json')],check=True);print('records',len(samples),'fields',len(fields),'staged',len(fresh))
