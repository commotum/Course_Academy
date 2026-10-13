"""Parent independently reads printed trig formulas, intervals and inequality rows."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186087736;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_trig_range',D.with_suffix('.py'));p=module('parent_trig_range_parser',R/'vector-math-parser.py')
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def inner(raw):return raw[2:-2] if raw.startswith('$$') else raw[1:-1]
def math(raw):return p.scalar(raw.strip().rstrip('.,').replace(r'\theta','t').replace('θ','t'))
def equal(a,b):return s.simplify(a-b)==0
def objects(prompt):
 body=next(inner(m[0]) for m in MATH.finditer(prompt) if re.search(r'x\s*=',m[0]) and re.search(r'y\s*=',m[0]))
 body=body.replace(r'\,','').strip().rstrip('.,');match=re.fullmatch(r'x\s*=\s*(.*?),\s*y\s*=\s*(.*?),\s*(.*)',body,re.S);assert match,body
 x,y,domain=match.groups();assert domain.replace(' ','').replace('θ',r'\theta').replace('π',r'\pi') in (r'0\le\theta<2\pi',r'0\leq\theta<2\pi'),domain
 F={'x':math(x),'y':math(y)};parameters={}
 for v,fn in [('x',s.cos),('y',s.sin)]:
  expr=s.expand(F[v]);coefficient=expr.coeff(fn(p.t));shift=s.simplify(expr-coefficient*fn(p.t));assert not shift.has(p.t) and coefficient!=0;parameters[v]=(coefficient,shift)
 return F,parameters
def interval(expression):
 expr=s.expand(expression);a=expr.coeff(s.cos(p.t));b=expr.coeff(s.sin(p.t));h=s.simplify(expr-a*s.cos(p.t)-b*s.sin(p.t));assert not h.has(p.t)
 return s.Interval(h-s.sqrt(a*a+b*b),h+s.sqrt(a*a+b*b))
def bank(raw):
 output={}
 for clause in raw.replace(r'\,','').split(','):
  parts=re.split(r'\\leq(?![A-Za-z])|\\le(?![A-Za-z])',clause);assert len(parts)==3 and parts[1].strip() in ('x','y'),raw
  lo,axis,hi=parts;output[axis.strip()]=s.Interval(math(lo),math(hi))
 return output
counts=dict(source_prompts=0,source_radio_banks=0,source_values=0,source_designations=0,source_solutions=0,printed_instances=0,coordinate_images=0,inequality_stages=0)
def check(r):
 q=r['question'];F,parameters=objects(q[':question/problem']);images={v:interval(expr) for v,expr in F.items()}
 if q[':question/difficulty'].endswith('/hard'):
  for v,(a,h) in parameters.items():assert a<0 and s.denom(a)>1 and h!=0 and s.denom(h)>1 and s.denom(a)<=4 and s.denom(h)<=4 and abs(a)<=9 and abs(h)<=9 and not (images[v].inf.is_integer and images[v].sup.is_integer)
 for f in q[':question/answer-fields']:
  selected=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type'].endswith('/radio'):
   vals=[bank(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==5 and len({str(v) for v in vals})==5
   correct=[a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if v==images];assert correct==[f[':answer-field/correct'][1]]
  else:
   n=int(f[':answer-field/key'].split('-')[1]);v='x' if n<=3 else 'y'
   if n in (2,5):assert selected.strip()==r'\le'
   else:assert equal(math(selected),images[v].inf if n in (1,4) else images[v].sup)
 for block in MATH.finditer(q[':question/worked-solution']):
  body=inner(block[0]).strip().rstrip('.,')
  if r'\begin{aligned}' in body:rows=body.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')
  else:rows=[body]
  for row in rows:
   row=re.sub(r'\\text\{[^}]*\}','',row).replace('&','').strip().rstrip('.,');parts=re.split(r'(\\le(?![A-Za-z])|\\ge(?![A-Za-z])|[<>])',row)
   if row.replace(' ','')==r'0\le\theta<2\pi':continue
   if len(parts)==1:continue
   assert len(parts)%2==1
   for lhs,op,rhs in zip(parts[::2],parts[1::2],parts[2::2]):
    def value(z):
     z=z.strip();return F[z] if z in F else math(z)
    delta=value(lhs)-value(rhs);I=interval(delta)
    if op in (r'\le','<'):assert I.sup<=0 and (op!='<' or 0 not in I),(row,I)
    else:assert I.inf>=0 and (op!='>' or 0 not in I),(row,I)
    counts['inequality_stages']+=1
 counts['printed_instances']+=1;counts['coordinate_images']+=2
old={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=old[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(r);assert q[':question/problem']==r['question'][':question/problem'];counts['source_prompts']+=1
 nf={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}
 for f in q[':question/answer-fields']:
  n=nf['selection'] if f[':answer-field/type'][':db/ident'].endswith('/radio') else nf[f[':answer-field/key']];assert f[':answer-field/type'][':db/ident']==n[':answer-field/type']
  if n[':answer-field/type'].endswith('/radio'):
   assert sorted(str(bank(a[':answer/value'])) for a in f[':answer-field/choices'])==sorted(str(bank(a[':answer/value'])) for a in n[':answer-field/choices']);counts['source_radio_banks']+=1
  else:assert [a[':answer/value'].strip() for a in f[':answer-field/choices']]==[a[':answer/value'].strip() for a in n[':answer-field/choices']]
  counts['source_values']+=len(f[':answer-field/choices'])
  if ':answer-field/correct' in f:
   value=next(a[':answer/value'] for a in n[':answer-field/choices'] if a[':answer/id']==n[':answer-field/correct'][1]);source_value=f[':answer-field/correct'][':answer/value']
   if n[':answer-field/type'].endswith('/radio'):assert bank(value)==bank(source_value)
   else:assert value.strip()==source_value.strip()
   counts['source_designations']+=1
 if ':question/worked-solution' in q:assert q[':question/worked-solution']==r['question'][':question/worked-solution'];counts['source_solutions']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
