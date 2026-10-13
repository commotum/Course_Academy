"""Root reads actual rate models, times, all arithmetic stages and banks."""
import importlib.util,json,re,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186064154;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_rate_scalar',R/'ode-scalar-parser.py');g=module('root_rate_generator',D.with_suffix('.py'));s=p.s
C=dict(instances=0,displayed_values=0,arithmetic_stages=0,source_questions=0,source_banks=0,source_values=0,source_existing_refs=0,source_missing_refs=0,source_exact_prompts=0,source_normalized_solutions=0)
def spans(text):return [a or b for a,b in re.findall(r'\$\$([\s\S]*?)\$\$|\$([^$]*)\$',text)]
def scalar(raw):return p.scalar(raw.replace(r'\dfrac',r'\frac').replace('E','e'))
def rounded(v,d):
 if d is None:return s.simplify(v)
 z=s.N(v,80)*10**d;return (s.floor(z+s.Rational(1,2)) if z>=0 else -s.floor(-z+s.Rational(1,2)))/s.Integer(10)**d

def check(r):
 q=r['question'];prompt=q[':question/problem'];worked=q[':question/worked-solution'];models={};var=None
 for body in spans(prompt):
  m=re.fullmatch(r"([A-Za-z])('?)(\(t\)|\(x\))\s*=\s*(.*?)[,.]?",body)
  if m:models[m[1]+m[2]]=scalar(m[4]);var=p.t if m[3]=='(t)' else p.x
 assert models,prompt
 if '24-hour time' in prompt:
  clock=re.search(r'24-hour time \$(\d+)\\text\{:\}(\d+)\$',prompt);start=re.search(r'at \$(\d+)\\text\{:\}(\d+)\$ am',prompt)
  point=s.Rational(int(clock[1])*60+int(clock[2])-int(start[1])*60-int(start[2]),60);assert point.q==2 and point<=15
 elif 'week $' in prompt:point=scalar(re.search(r'week \$([^$?]+)\?',prompt)[1]);assert point>0 and s.sqrt(point).is_Integer
 elif 'since' in prompt and len(re.findall(r'\$(\d{4})[.?]?\$',prompt))>=2:
  dates=re.findall(r'\$(\d{4})[.?]?\$',prompt);point=s.Integer(dates[-1])-s.Integer(dates[0])
 else:
  matches=re.findall(r'(?:after|construction|pool) \$([^$]+)\$ (?:hours|microseconds|days|minutes)',prompt)
  assert matches,prompt;point=scalar(matches[-1])
 assert point>0
 evaluated={name:s.simplify(expr.subs(var,point)) for name,expr in models.items()};assert all(z>0 for z in evaluated.values()),evaluated
 if len(models)==1:result=next(iter(evaluated.values()))
 else:
  assert set(models) in ({'B','D'},{'F','L'},{'O','C'}),models
  first,second=({'B','D'}==set(models) and ('B','D')) or ({'F','L'}==set(models) and ('F','L')) or ('O','C');result=s.simplify(evaluated[first]-evaluated[second])
 digits=3 if 'three decimal places' in prompt else 0 if 'nearest integer' in prompt else None;want=rounded(result,digits)
 # Check all stated time substitutions, including prose before the aligned block.
 for body in spans(worked):
  for n in re.findall(r'(?:t|x)\s*=\s*([0-9]+(?:\.[0-9]+)?)',body):assert scalar(n)==point,(body,point)
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',worked,re.S)[1];rows=block.split(chr(92)*2)
 label,initial_rhs=rows[0].split('&',1)
 def eval_labels(raw):
  for name,expr in sorted(models.items(),key=lambda z:-len(z[0])):
   base=name.rstrip("'");pattern=r'\{?'+base+r'\}?(?:\^\{[\x27′]\}|\x27)?\(([^()]*)\)'
   def replace(m):
    v=scalar(m[1]);assert v in (point,var),(raw,v,point);return '('+str(evaluated[name])+')'
   raw=re.sub(pattern,replace,raw)
  return scalar(raw)
 assert s.simplify(eval_labels(label)-result)==0,(label,result)
 for row in [initial_rhs]+[z.split('&')[-1] for z in rows[1:]]:
  row=row.strip();approx=row.startswith('≈') or row.startswith(r'\approx');row=re.sub(r'^(?:=|≈|\\approx)\s*','',row);v=scalar(row)
  assert s.simplify(v-(want if approx else result))==0,(row,v,result,want)
  C['arithmetic_stages']+=1
 if '24-hour time' in prompt:
  sine=next(expr for name,expr in models.items() if name=='C');trig=list(sine.atoms(s.sin));assert len(trig)==1 and abs(trig[0].subs(var,point))==1
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];values=[scalar(a[':answer/value'].split('$')[1]) if '$' in a[':answer/value'] else scalar(a[':answer/value']) for a in choices]
 assert len(set(str(s.simplify(v)) for v in values))==len(values)
 for a,v in zip(choices,values):assert (s.simplify(v-want)==0)==(a[':answer/id']==f[':answer-field/correct'][1]),(a,v,want)
 if r['generation']['profile']=='authored_operations':
  if len(models)==1:
   # Coefficient is read from the model, not generation metadata.
   expr=next(iter(models.values()));coefficient=expr.subs(var,0);raw=[result,2*result,result/2,coefficient,coefficient*point];assert all(v>=0 for v in values)
  else:raw=[result,evaluated[first]+evaluated[second],-result,evaluated[first],-evaluated[second]]
  assert sorted(str(s.simplify(z)) for z in values)==sorted(str(rounded(z,digits)) for z in raw)
 C['instances']+=1;C['displayed_values']+=len(values);return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def norm(text):return re.sub(r'\s+','',text).replace('≈',r'\approx')
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));C['source_questions']+=1
 if q[':question/problem']==old[':question/problem']:C['source_exact_prompts']+=1
 else:assert case['template'].startswith('stock') or not old.get(':question/answer-fields')
 if old.get(':question/worked-solution'):assert norm(q[':question/worked-solution'])==norm(old[':question/worked-solution']);C['source_normalized_solutions']+=1
 for of,nf in zip(old.get(':question/answer-fields',[]),q[':question/answer-fields']):
  assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in nf[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=len(of[':answer-field/choices'])
  if of.get(':answer-field/correct'):
   actual=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert actual==of[':answer-field/correct'][':answer/value'];C['source_existing_refs']+=1
  else:C['source_missing_refs']+=1
 if not old.get(':question/answer-fields'):C['source_missing_refs']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
# Additional explicit source calendar transfer; prove complete prose changes too.
case=next(z for z in json.loads((D/'source-cases.json').read_text()) if z['template']=='krill');params=dict(case['parameters']);params.update(year=2004,target=2014);check(g.generate(case['level'],template='krill',parameters=params))
C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
