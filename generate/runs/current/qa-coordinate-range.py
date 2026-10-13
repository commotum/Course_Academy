"""Parent reads actual formulas, full coordinate sets and displayed arguments."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
from sympy.calculus.util import continuous_domain
R=Path(__file__).resolve().parent;K=17592186087722;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_coordinate_range',D.with_suffix('.py'));p=module('parent_range_parser',R/'vector-math-parser.py')
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def inner(raw):return raw[2:-2] if raw.startswith('$$') else raw[1:-1]
def math(raw):return p.scalar(raw.strip().rstrip('.,'))
def equal(a,b):return s.simplify(a-b)==0
def relation(raw):return re.split(r'(\\leq(?![A-Za-z])|\\geq(?![A-Za-z])|\\le(?![A-Za-z])|\\ge(?![A-Za-z])|[<>=])',raw)
def objects(prompt):
 body=next(inner(m[0]) for m in MATH.finditer(prompt) if re.search(r'x\s*=',m[0]) and re.search(r'y\s*=',m[0]))
 body=body.replace(r'\,','').replace(r'\quad','').strip().rstrip('.,')
 match=re.fullmatch(r'x\s*=\s*(.*?),\s*y\s*=\s*(.*?),\s*t(.*)',body,re.S);assert match,body
 xt,yt,domain=match.groups();F={'x':math(xt),'y':math(yt)}
 if r'\in' in domain or '∈' in domain:J=s.S.Reals
 else:
  parts=relation('t'+domain);assert len(parts)==3 and parts[0].strip()=='t';op=parts[1];bound=math(parts[2])
  J=s.Interval(bound,s.oo,left_open=op=='>') if op in ('>',r'\ge',r'\geq') else s.Interval(-s.oo,bound,right_open=op=='<')
 for expression in F.values():J=J.intersect(continuous_domain(expression,p.t,s.S.Reals))
 return F,J
def image(expression,domain):
 # Independent endpoint/critical-point calculation, rather than generator's function_range.
 if not expression.has(p.t):return s.FiniteSet(expression)
 assert isinstance(domain,s.Interval) or domain==s.S.Reals
 lo,hi=domain.inf,domain.sup;left_open=domain.left_open if isinstance(domain,s.Interval) else True;right_open=domain.right_open if isinstance(domain,s.Interval) else True
 derivative=s.diff(expression,p.t);roots=s.solveset(derivative,p.t,domain=domain)
 assert isinstance(roots,s.FiniteSet) or roots==s.S.EmptySet,(expression,roots)
 candidates=[(s.limit(expression,p.t,lo,dir='+'),not left_open),(s.limit(expression,p.t,hi,dir='-'),not right_open)]
 candidates += [(s.simplify(expression.subs(p.t,z)),True) for z in roots]
 assert all(not v.has(s.zoo,s.nan) for v,_ in candidates)
 low=s.Min(*[v for v,_ in candidates]);high=s.Max(*[v for v,_ in candidates])
 return s.Interval(low,high,left_open=not any(v==low and attained for v,attained in candidates),right_open=not any(v==high and attained for v,attained in candidates))
def sets(raw):
 result={}
 for part in raw.replace(r'\,','').split(','):
  part=part.strip()
  if r'\in\mathbb{R}' in part:result[part[0]]=s.S.Reals;continue
  bits=relation(part)
  if len(bits)==3:
   variable,op,value=bits;variable=variable.strip();assert variable in ('x','y'),(raw,bits);value=math(value)
   result[variable]=s.FiniteSet(value) if op=='=' else s.Interval(value,s.oo,left_open=op=='>') if op in ('>',r'\ge',r'\geq') else s.Interval(-s.oo,value,right_open=op=='<')
  else:
   assert len(bits)==5 and bits[2].strip() in ('x','y');result[bits[2].strip()]=s.Interval(math(bits[0]),math(bits[4]),left_open=bits[1]=='<',right_open=bits[3]=='<')
 return result
counts=dict(source_prompts=0,source_radio_banks=0,source_values=0,source_designations=0,source_solution_layouts=0,printed_instances=0,coordinate_images=0,solution_equations=0,solution_inequalities=0)
def check(r):
 q=r['question'];F,J=objects(q[':question/problem']);expected={v:image(f,J) for v,f in F.items()};level=q[':question/difficulty'].split('/')[-1]
 if level=='easy':assert s.degree(F['x'],p.t)==1 and abs(F['x'].coeff(p.t)) in (1,2,3)
 if level=='hard':
  for expr in F.values():assert s.degree(expr,p.t)==2 and expr.coeff(p.t,2) in (-2,-1,1,2) and expr.coeff(p.t) in (-6,-4,-2,2,4,6)
 for field in q[':question/answer-fields']:
  if field[':answer-field/type'].endswith('/radio'):
   bank=[sets(a[':answer/value']) for a in field[':answer-field/choices']];assert len(bank)==5 and len({str(b) for b in bank})==5
   hit=[a[':answer/id'] for a,b in zip(field[':answer-field/choices'],bank) if b=={v:expected[v] for v in b}];assert hit==[field[':answer-field/correct'][1]]
  else:
   idx=int(field[':answer-field/key'][-1]);variable='x' if idx<=2 else 'y';I=expected[variable];lower=I.sup==s.oo;boundary=I.inf if lower else I.sup;closed=not (I.left_open if lower else I.right_open)
   value=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
   if idx%2:assert value.strip()==('\\ge' if closed and lower else '\\le' if closed else '>' if lower else '<')
   else:assert equal(math(value),boundary)
 for block in MATH.finditer(q[':question/worked-solution']):
  body=inner(block[0]).strip().rstrip('.,')
  if r'\begin{aligned}' in body:
   text=body.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0];axis=None;raw_stages=[]
   for row in text.split(r'\\'):
    lhs,rhs=row.split('=',1)
    if lhs.replace('&','').strip():axis=lhs.replace('&','').strip()
    assert axis in F and equal(math(rhs),F[axis]),row;counts['solution_equations']+=1;raw_stages.append(rhs)
   assert len(raw_stages)==len(set(raw_stages)),'Collapsed displayed square-completion stages'
   continue
  if not re.search(r'\\(?:le|ge)|[<>=]',body):continue
  for clause in re.split(r' and |,\\,',body):
   bits=relation(clause);assert len(bits)%2==1
   for lhs,op,rhs in zip(bits[::2],bits[1::2],bits[2::2]):
    lhs=lhs.strip();rhs=rhs.strip();coordinates={v for v in ('x','y') if re.search(r'(?<![A-Za-z\\])'+v+r'(?![A-Za-z])',lhs+' '+rhs)}
    if lhs=='t' and op=='=':
     value=math(rhs);assert value in (J.inf,J.sup) or any(s.simplify(s.diff(f,p.t).subs(p.t,value))==0 for f in F.values());continue
    assert len(coordinates)<=1,(body,coordinates)
    axis=next(iter(coordinates),None)
    def operand(raw):
     if raw in F:return F[raw]
     evaluation=re.fullmatch(r'([xy])\((.*)\)',raw)
     return F[evaluation[1]].subs(p.t,math(evaluation[2])) if evaluation else math(raw)
    a=operand(lhs);b=operand(rhs)
    if op=='=':assert equal(a,b),(body,F,a,b,axis);counts['solution_equations']+=1
    else:
     delta=a-b;I=image(delta,J) if delta.has(p.t) else s.FiniteSet(delta)
     if op in ('>',r'\ge',r'\geq'):assert I.inf>=0 and (op!='>' or 0 not in I),(body,I)
     else:assert I.sup<=0 and (op!='<' or 0 not in I),(body,I)
     counts['solution_inequalities']+=1
 counts['printed_instances']+=1;counts['coordinate_images']+=2
 return expected
raw=json.loads((R/'sources'/f'{K}.json').read_text());old={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=old[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(r);assert r['question'][':question/problem']==q[':question/problem'];counts['source_prompts']+=1
 nf={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}
 for f in q.get(':question/answer-fields',[]):
  n=nf['selection'] if f[':answer-field/type'][':db/ident'].endswith('/radio') else nf[f[':answer-field/key']]
  assert f[':answer-field/type'][':db/ident']==n[':answer-field/type']
  if n[':answer-field/type'].endswith('/radio'):
   source=sorted(str(sets(a[':answer/value'])) for a in f[':answer-field/choices']);generated=sorted(str(sets(a[':answer/value'])) for a in n[':answer-field/choices']);assert source==generated;counts['source_radio_banks']+=1
  else:assert [a[':answer/value'].strip() for a in f[':answer-field/choices']]==[a[':answer/value'].strip() for a in n[':answer-field/choices']]
  counts['source_values']+=len(f[':answer-field/choices'])
  if ':answer-field/correct' in f:
   value=next(a[':answer/value'] for a in n[':answer-field/choices'] if a[':answer/id']==n[':answer-field/correct'][1]);assert value.strip()==f[':answer-field/correct'][':answer/value'].strip();counts['source_designations']+=1
 if ':question/worked-solution' in q:assert r['question'][':question/worked-solution']==q[':question/worked-solution'];counts['source_solution_layouts']+=1
for r in json.loads((D/'review.json').read_text()):check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
