"""Root independently reads supplied rates, units and complete text option banks."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186064153;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_context_scalar',R/'ode-scalar-parser.py');g=module('root_context_generator',D.with_suffix('.py'));s=p.s
C=dict(instances=0,values=0,displayed_number_checks=0,solution_derivative_equalities=0,source_prompts=0,source_banks=0,source_values=0,source_solutions=0,source_existing_refs=0,source_missing_refs=0)
def numeric(raw):return p.scalar(raw.strip().rstrip('?.').removesuffix('m'))
def nums(text):
 result=[]
 for z in re.findall(r'\$([^$]*)\$',text):
  try:n=numeric(z)
  except (AssertionError,ValueError):continue
  if not n.free_symbols:result.append(n)
 return result
def equalities(text):
 normalized=text.replace('{','').replace('}','')
 return [(m[1],numeric(m[2]),numeric(m[3])) for m in re.finditer(r"([A-Za-z])(?:\^′|')\(([^()]*)\)\s*=\s*([^$\n]+)",normalized)]
def task(prompt):
 direct=equalities(prompt)
 if direct:assert len(direct)==1;name,t,r=direct[0]
 else:
  m=re.search(r'at \$([tv])=([^$]+)\$ is equal to \$([^$]+)\$',prompt);assert m,prompt;t=numeric(m[2]);r=numeric(m[3]);name='P' if 'lemonade' in prompt else 'V'
 assert t.is_Integer and 2<=t<=60 and r.is_Rational and r!=0
 if 'lemonade' in prompt:return name,t,r,'price','cents per liter',100
 if 'in thousands' in prompt:return name,t,r,'visitors','visitors per hour',1000
 if 'sheet of ice' in prompt:return name,t,r,'ice','squared centimeters per minute',1
 if 'cup of tea' in prompt:return name,t,r,'temperature','degrees Celsius per minute',1
 if 'school' in prompt:return name,t,r,'budget','dollars per student',1
 if 'Sam' in prompt:return name,t,r,'walking','meters per day',1
 if 'car' in prompt:return name,t,r,'car','meters per second',1
 assert 'mobile phone app' in prompt;return name,t,r,'app','users per hour',1
def eligible(text,T):
 _,t,r,context,unit,scale=T
 if re.search(r'constant|constantly|total|(?:increased|decreased) by',text):return False
 if 'at a rate of' not in text or unit not in text:return False
 if context=='price' and 'liters of lemonade are sold' not in text:return False
 if nums(text)!=[t,abs(r)*scale]:return False
 positive=bool(re.search(r'\b(?:increased|increases|increasing)\b',text));negative=bool(re.search(r'\b(?:decreased|decreases|decreasing)\b',text))
 return positive and not negative if r>0 else negative and not positive
def check(record):
 q=record['question'];T=task(q[':question/problem']);name,t,r,context,unit,scale=T;mag=abs(r)*scale;profile=record['generation']['bank_profile'];f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];assert len(choices)==5
 good=[z for z in choices if eligible(z[':answer/value'],T)];assert len(good)==1 and f[':answer-field/correct']==[':answer/id',good[0][':answer/id']]
 for z in choices:
  text=z[':answer/value'];actual=nums(text);expected=[t,mag]
  if context in ('app','car','budget') and 'constant rate' in text:expected=[t/r if context=='car' and profile=='observed' else r/t]
  elif context in ('app','car','budget') and ('increased by' in text):expected=[mag,t]
  elif context=='walking' and 'constant rate' in text:expected=[t,r/t]
  elif context=='walking' and ('walked a distance' in text or 'increased by' in text):expected=[mag,t]
  elif context=='price' and 'When the price' in text:expected=[mag,t]
  elif context=='visitors' and 'constant rate' in text:expected=[t,mag/t]
  elif context=='ice' and ('observation began' in text or 'area of the sheet is' in text and actual[0]==mag):expected=[mag,t]
  elif context=='car' and profile=='authored' and 'at a rate of' in text and actual==[t,t]:expected=[t,t];assert r!=t
  assert actual==expected,(text,actual,expected);C['displayed_number_checks']+=len(actual)
  if context=='car' and profile=='authored':assert not re.search(r'\b(?:decreased|decreases|decreasing)\b',text)
 worked=q[':question/worked-solution'];ee=equalities(worked);assert ee and all(z==(name,t,r) for z in ee),(ee,T);C['solution_derivative_equalities']+=len(ee)
 final=worked.split('*')[-2];assert eligible(final,T)
 if context=='ice' and profile=='authored':assert 'is changing $t$' in worked
 if context=='visitors' and r<0:assert 'currently' in q[':question/problem']
 if q[':question/difficulty'].endswith('/hard'):assert r<0
 else:assert r>0
 C['instances']+=1;C['values']+=5;return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=sources[c['source_id']];q=check(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']));assert q[':question/problem']==old[':question/problem'];C['source_prompts']+=1
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution'];C['source_solutions']+=1
 for of,nf in zip(old[':question/answer-fields'],q[':question/answer-fields']):
  assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in nf[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=len(of[':answer-field/choices'])
  actual=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1])
  if of.get(':answer-field/correct'):assert actual==of[':answer-field/correct'][':answer/value'];C['source_existing_refs']+=1
  else:C['source_missing_refs']+=1
for r in json.loads((D/'review.json').read_text()):check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
