import copy,json,os,subprocess,sys
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import validate_generated_record
H=Path(__file__).resolve().parent;ds={r['kp']:r for r in json.loads((H/'generator-candidates.json').read_text())};wide=ds[17592186087839];samples=json.loads((H/'staged-generator-samples.json').read_text())+json.loads((H/'separation-staged-samples.json').read_text())+json.loads((H/'relocation-samples.json').read_text());env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str((H/'wide-final-assets').resolve()),'MPLCONFIGDIR':str((H/'mpl-cache').resolve())}
for level,t in [('easy','integer_radio'),('easy','integer_blank'),('moderate','decimal_x_radio'),('moderate','decimal_y_radio'),('moderate','fraction_blank'),('moderate','decimal_both_radio')]:
 p=subprocess.run([sys.executable,str(Path(wide['directory'])/wide['entrypoint']),'--difficulty',level,'--template',t,'--seed','912235','--count','1','--format','json'],env=env,capture_output=True,text=True,check=True);samples.extend({'kp':wide['kp'],'level':level,'record':r,'kind':'staged-successor'}for r in json.loads(p.stdout))
checks=[];fields=[]
for i,s in enumerate(samples):
 r=copy.deepcopy(s['record']);validate_generated_record(r);q=r['question'];label=str(s['kp'])+'/'+str(i);tests=[]
 for attr in [':question/problem',':question/worked-solution']:fields.append({'entity':label,'attribute':attr,'value':q[attr]})
 for j,f in enumerate(q[':question/answer-fields']):
  cid=f[':answer-field/correct'][1];right=next(a for a in f[':answer-field/choices']if a[':answer/id']==cid)
  for a in f[':answer-field/choices']:fields.append({'entity':label,'attribute':'answer/value','value':a[':answer/value'],'bare_math':a[':answer/type']==':answer.type/math'})
  if f[':answer-field/type']==':answer-field.type/blank':tests.extend([{'field_index':j,'submitted':right[':answer/value'],'expected':'accepted'},{'field_index':j,'submitted':'987654321','expected':'rejected'}])
  else:tests.extend({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==cid else'rejected'}for a in f[':answer-field/choices'])
 checks.append({'label':label,'record':r,'checks':tests})
(H/'final-stage-samples.json').write_text(json.dumps(samples,indent=2));(H/'final-stage-grading-input.json').write_text(json.dumps(checks,indent=2));(H/'final-stage-render-input.json').write_text(json.dumps(fields,indent=2));subprocess.run([str(H.parent/'check-engine'),str(H/'final-stage-grading-input.json'),str(H/'final-stage-grading.json')],check=True);print('finalstage records',len(samples),'fields',len(fields))
