"""Read printed question data independently of the generator's metadata."""
import copy,importlib.util,json,re,subprocess,sys,os
from decimal import Decimal,ROUND_HALF_UP,localcontext
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import prepare_records,inventory_fingerprints,validate_question
from scripts.rounded_finance_batch_policy import validate_delivery_batch,displayed_number
from scripts.question_capture.math_format import MATH

def calculate(q):
 vals=[];prompt=q[':question/problem'];places=0
 for match in MATH.finditer(prompt):
  try:vals.append(displayed_number(match[0]))
  except ValueError:pass
 with localcontext()as ctx:
  ctx.prec=50
  if 'forex'in prompt.lower():pct,C,t=vals;r=pct/100*(-1 if 'decreasing'in prompt else 1);raw=C*(-r*t).exp()
  elif 'gas price'in prompt:C,pct,t=vals;r=pct/100*(-1 if 'decreasing'in prompt else 1);raw=C*(-r*t).exp();places=2
  elif 'biology class'in prompt:initial,t,final=vals;raw=(final/initial).ln()/t*100
  elif 'koalas'in prompt:initial,pct,final=vals;raw=(final/initial).ln()/(-pct/100)
  elif 'crimes'in prompt:year,initial,pct,end=vals;raw=initial*(-pct/100*(end-year)).exp()
  elif 'plague'in prompt:initial,pct,weeks=vals;raw=initial*(-pct/100*weeks*7).exp()
  else:raise AssertionError('Unknown printed context')
  expected=raw.quantize(Decimal(1).scaleb(-places),rounding=ROUND_HALF_UP)
 return raw,places,expected

def check(row,kp):
 q=row['question'];validate_question(q);validate_delivery_batch([row],kp);raw,places,expected=calculate(q);f=q[':question/answer-fields'][0];key=f[':answer-field/correct'][1]
 matching=[a for a in f[':answer-field/choices']if displayed_number(a[':answer/value'])==expected]
 assert len(matching)==1 and matching[0][':answer/id']==key,(kp,raw,expected,q)
 return {'raw':str(raw),'places':places,'correct':str(expected),'values':[str(displayed_number(a[':answer/value']))for a in f[':answer-field/choices']]}

reports=[];grading=[];render=[];n=0
for item in json.loads((H/'capture.json').read_text())['knowledge_points']:
 kp=item['kp'];d=H/str(kp);pool=json.loads((d/'candidate-pool.json').read_text());accepted=json.loads((d/'accepted-pool.json').read_text());checks=[]
 for row in pool:check(row,kp);n+=1
 for seed in(7,37,20261026):
  rows=json.loads(subprocess.check_output([sys.executable,str(d/'package/generator.py'),'--count','30','--seed',str(seed),'--difficulty','moderate'],text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}))
  validate_delivery_batch(rows,kp)
  for r in rows:check(r,kp);n+=1
 before=json.loads((d/'before.json').read_text());fps=inventory_fingerprints(before[':knowledge-point/questions']+[before[':knowledge-point/canonical-example']]);new,dup=prepare_records(pool,kp,before[':knowledge-point/id'],fps,ROOT,d/'package');assert(len(new),dup)==((0,5)if kp==17592186059798 else(5,0))
 for i,row in enumerate(accepted):
  f=row['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1];tests=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==key else'rejected'}for a in f[':answer-field/choices']];grading.append({'label':f'{kp}:{i}','record':row,'checks':tests});checks.append(check(row,kp))
 report={'passed':True,'independently_checked_records':95,'new_questions':len(new),'duplicates':dup,'delivered':checks};(d/'generator-verification.json').write_text(json.dumps(report,indent=2)+'\n');reports.append({'kp':kp,**report});render+=accepted;print(kp,'printed mathematics and separated choices checked',flush=True)
for name,value in [('generator-verification',{'passed':True,'records_checked':n,'knowledge_points':reports}),('grader-input',grading),('render-input',render)]:(H/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
