"""Parent parses actual coordinate formulas, table cells and complete scalar banks."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186087717;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_parametric_table',D.with_suffix('.py'));p=module('parent_table_parser',R/'vector-math-parser.py');MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def inner(raw):return raw[2:-2] if raw.startswith('$$') else raw[1:-1]
def math(raw):return p.scalar(raw.strip().rstrip('.,'))
def equal(a,b):return s.simplify(s.trigsimp(a-b))==0
def cells(row):return [z.strip() for z in row.split('|')[1:-1]]
def tables(text):return [cells(row) for row in text.splitlines() if row.startswith('|')]
def objects(prompt):
 body=next(inner(m[0]) for m in MATH.finditer(prompt) if re.search(r'x\s*=',m[0])).replace(r'\,','')
 match=re.search(r'x\s*=\s*(.*?),\s*y\s*=\s*(.*?),',body,re.S);assert match,(prompt,body)
 functions={name:math(value) for name,value in zip(('x','y'),match.groups())};grid=tables(prompt);times=[math(z.strip('$')) for z in grid[0][1:]];return functions,times,grid
counts=dict(source_radio_banks=0,source_values=0,source_designations=0,source_prompt_math=0,shared_source_solution_layouts=0,source_solution_repairs=0,printed_instances=0,prompt_numeric_cells=0,solution_numeric_cells=0,solution_equality_stages=0)
def combo(raw,values):
 assert re.fullmatch(r'[abc+\-\s]+',raw);return s.sympify(raw,locals=values)
def check(r):
 q=r['question'];F,ts,grid=objects(q[':question/problem']);targets={}
 for axis,row in zip(('x','y'),grid[2:4]):
  assert len(row)-1==len(ts)
  for time,raw in zip(ts,row[1:]):
   expected=s.simplify(F[axis].subs(p.t,time));assert not expected.has(s.zoo,s.oo,s.nan)
   if raw.startswith('{{'):targets[raw[2:-2]]=expected
   elif raw.strip('$') in ('a','b','c'):targets[raw.strip('$')]=expected
   else:assert equal(math(raw.strip('$')),expected);counts['prompt_numeric_cells']+=1
 level=q[':question/difficulty'].split('/')[-1]
 if level in ('moderate','hard'):
  degree=2 if level=='moderate' else 3
  for expression in F.values():
   poly=s.Poly(expression,p.t);assert len(poly.terms())==3 and poly.degree()==degree
   assert poly.nth(degree) in [s.Rational(a,4) for a in (-5,-3,-1,1,3,5)]
   assert poly.nth(degree-1) in [s.Rational(a,3) for a in (-4,-2,-1,1,2,4)]
   assert poly.nth(0) in list(range(-6,0))+list(range(1,7))
   if level=='hard':assert poly.nth(1)==0
   assert all(not poly.eval(time).is_integer for time in (2,3,4))
  blank_times=[time for row in grid[2:4] for time,cell in zip(ts,row[1:]) if cell.startswith('{{')];assert sorted(blank_times)==[2,3,4]
 request=re.search(r'Find the value of \$(.*?)\$',q[':question/problem']);combined=combo(request[1].rstrip('.'),targets) if request else None
 for f in q[':question/answer-fields']:
  expected=combined if request else targets[f[':answer-field/key']];vals=[math(a[':answer/value']) for a in f[':answer-field/choices']]
  assert all(not equal(a,b) for n,a in enumerate(vals) for b in vals[:n])
  assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if equal(v,expected)]==[f[':answer-field/correct'][1]]
 sol=q[':question/worked-solution']
 for row in tables(sol):
  if row[0] not in ('$x$','$y$'):continue
  axis=row[0].strip('$');assert len(row)-1==len(ts)
  for time,value in zip(ts,row[1:]):assert equal(math(value.strip('$')),F[axis].subs(p.t,time));counts['solution_numeric_cells']+=1
 for m in MATH.finditer(sol):
  text=inner(m[0]).strip().rstrip('.,')
  if '=' not in text or '\\le' in text:continue
  lhs,*rhs=text.split('=');lhs=lhs.strip()
  if lhs=='t':continue
  if lhs in ('x','y'):assert equal(math(rhs[0]),F[lhs]);continue
  if lhs in ('a','b','c'):expected=targets[lhs]
  elif re.fullmatch(r'[xy]\(-?\d+\)',lhs):expected=F[lhs[0]].subs(p.t,s.Integer(lhs[2:-1]))
  elif request:expected=combo(lhs,targets)
  else:raise AssertionError(('Unknown parent stage',text))
  for raw in rhs:assert equal(math(raw),expected),(r['generation']['template'],text);counts['solution_equality_stages']+=1
 counts['printed_instances']+=1;return F,ts
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=qs[c['source_id']];r=g.generate('easy',template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);F,ts=check(r);oF,ots,_=objects(old[':question/problem']);assert ts==ots and all(equal(F[name],oF[name]) for name in F);counts['source_prompt_math']+=1
 new={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}
 for sf in old.get(':question/answer-fields',[]):
  nf=new[sf[':answer-field/key']];assert sf[':answer-field/type'][':db/ident']==nf[':answer-field/type'];remaining=[math(a[':answer/value']) for a in nf[':answer-field/choices']]
  for a in sf[':answer-field/choices']:
   matches=[n for n,v in enumerate(remaining) if equal(math(a[':answer/value']),v)];assert len(matches)==1;remaining.pop(matches[0]);counts['source_values']+=1
  assert not remaining
  if sf[':answer-field/type'][':db/ident'].endswith('/radio'):counts['source_radio_banks']+=1
  if ':answer-field/correct' in sf:
   selected=next(math(a[':answer/value']) for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert equal(selected,math(sf[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
 if ':question/worked-solution' in old:
  expected=old[':question/worked-solution']
  for a,b in g.REPAIRS.get(c['source_id'],[]):expected=expected.replace(a,b)
  assert re.sub(r'\s+','',expected)==re.sub(r'\s+','',r['question'][':question/worked-solution']);counts['shared_source_solution_layouts']+=1
  if c['source_id'] in g.REPAIRS:counts['source_solution_repairs']+=1
for r in json.loads((D/'review.json').read_text()):check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
