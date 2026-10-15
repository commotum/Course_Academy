#!/usr/bin/env python3
"""Fail on independent displayed mathematics, fidelity, native grading or shape errors."""
import hashlib, importlib.util, json, re, subprocess, sys, uuid
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
T=g.T
def group(s,i):
 assert s[i]=='{';depth=1;j=i+1
 while depth:
  depth+=(s[j]=='{')-(s[j]=='}');j+=1
 return s[i+1:j-1],j
def convert(s):
 s=s.replace('π',r'\pi').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
 s=re.sub(re.escape('\\operatorname')+r'\{(sin|cos|tan)\}',r'\1',s)
 for token,name in ((r'\sin','sin'),(r'\cos','cos'),(r'\tan','tan')):s=s.replace(token,name)
 s=re.sub(r'(sin|cos|tan)t',r'\1(t)',s)
 for cmd in (r'\frac',r'\dfrac',r'\sqrt'):
  while cmd in s:
   start=s.index(cmd);i=start+len(cmd);a,i=group(s,i)
   if cmd.endswith('sqrt'):replacement='sqrt('+convert(a)+')'
   else:b,i=group(s,i);replacement='(('+convert(a)+')/('+convert(b)+'))'
   s=s[:start]+replacement+s[i:]
 s=s.replace(r'\pi','pi').replace('{','(').replace('}',')').replace('^','**').replace('[','(').replace(']',')')
 s=re.sub(r'(?<![A-Za-z])e(?![A-Za-z])','E',s)
 return s
def read(s):
 return parse_expr(convert(s.strip().rstrip('.,')),local_dict={'t':T,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'pi':sp.pi,'E':sp.E},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def eq(a,b):return sp.simplify(a-b)==0
def requested(record):
 q=record['question'];prompt=q[':question/problem'];m=re.search(r'x\s*=\s*(.*?),\s*(?:\\,)?y\s*=\s*(.*?),',prompt,re.S);assert m,prompt
 x,y=map(read,m.groups());return x,y,sp.diff(x,T),sp.diff(y,T)
def displayed_domain(record):
 prompt=record['question'][':question/problem']
 m=re.search(r'x\s*=\s*(.*?),\s*(?:\\,)?y\s*=\s*(.*?),',prompt,re.S)
 tail=prompt[m.end():].split('$$')[0].split('$')[0].strip().replace(r'\,','').rstrip('.')
 if '∞' in tail or r'\infty' in tail:
  assert '-' in tail and tail.count('∞')+tail.count(r'\infty')==2
  return sp.S.Reals
 match=re.fullmatch(r'(.*?)'+re.escape(r'\le')+r'\s*t\s*('+re.escape(r'\le')+r'|<)\s*(.*)',tail)
 assert match,tail
 lo,op,hi=match.groups();return sp.Interval(read(lo),read(hi),right_open=op=='<')
def mathcheck(record):
 q=record['question'];meta=record['generation'];template=meta['template'];p=g.guards(template,meta['parameters']);x,y,dx,dy=requested(record)
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==17592186083278
 expected_fields=2 if template in ('polynomial_two','spiral_cos','spiral_sin','paired_cubics') or (template=='circle_vertical' and meta['profile']=='raw') else 1
 assert len(q[':question/answer-fields'])==expected_fields
 expected_kind=':answer-field.type/'+('blank' if template in ('polynomial_two','spiral_cos','spiral_sin','paired_cubics') else 'radio')
 assert all(f[':answer-field/type']==expected_kind for f in q[':question/answer-fields'])
 keys=[f[':answer-field/key'] for f in q[':question/answer-fields']]
 assert len(set(keys))==len(keys) or (template=='circle_vertical' and meta['profile']=='raw')
 roots=[g.e(z) for z in meta['roots']];orientation='vertical' if 'is vertical' in q[':question/problem'] else 'horizontal';assert orientation==meta['orientation']
 target=dy if orientation=='horizontal' else dx;other=dx if orientation=='horizontal' else dy
 assert all(eq(target.subs(T,z),0) and not eq(other.subs(T,z),0) for z in roots)
 domain=displayed_domain(record);assert domain==g.mathematics(template,p)[-1]
 # Independent completeness: solve the displayed derivative, restricting the displayed domain.
 if target.has(sp.sin,sp.cos):
  if template.startswith('circle'):
   expected=sp.solveset(target,T,domain=domain)
   assert expected==sp.FiniteSet(*roots),(expected,roots)
  else:
   # sin +/- cos with nonzero exp/scale; enumerate an independently derived quarter-angle grid.
   expected=[j*sp.pi/4 for j in range(9) if eq(target.subs(T,j*sp.pi/4),0) and not eq(other.subs(T,j*sp.pi/4),0)]
   assert sp.FiniteSet(*roots)==sp.FiniteSet(*expected)
   periodic=sp.expand_trig(sp.simplify(target/sp.exp(T)))
   assert sp.simplify(periodic-(sp.expand(periodic).coeff(sp.sin(T))*sp.sin(T)+sp.expand(periodic).coeff(sp.cos(T))*sp.cos(T)))==0
 else:
  expected=sp.solveset(target,T,domain=domain)
  assert expected==sp.FiniteSet(*roots),(expected,roots)
 # Read every field's actual displayed values, not UUID correctness alone.
 for f in q[':question/answer-fields']:
  uuid.UUID(f[':answer-field/id']);kind=f[':answer-field/type'];choices=f[':answer-field/choices']
  assert len({a[':answer/id'] for a in choices})==len(choices)
  parsed=[]
  for a in choices:
   uuid.UUID(a[':answer/id'])
   if kind.endswith('/blank'):obj=[read(a[':answer/value'])]
   elif a[':answer/type'].endswith('/text'):obj=[read(v) for v in re.findall(r'\$t\s*=\s*(.*?)\$',a[':answer/value'])]
   else:obj=[read(a[':answer/value'].split('=')[1])]
   assert obj
   parsed.append(sp.FiniteSet(*obj))
  assert len(set(parsed))==len(parsed)
  if ':answer-field/correct' in f:
   selected=next(i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1])
   if kind.endswith('/blank'):assert parsed[selected]==sp.FiniteSet(roots[int(f[':answer-field/key'].split('-')[-1])-1])
   else:assert parsed[selected]==sp.FiniteSet(*roots) and sum(v==sp.FiniteSet(*roots) for v in parsed)==1
  if kind.endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 solution=q.get(':question/worked-solution')
 if solution:
  bs=g.blocks(solution)
  assert len(bs)==(4 if len(roots)==2 or template=='line_cubic' else 3)
  # First formal slope block and complete derivative block are mandatory.
  assert 'm=' in bs[0] and ('frac' in bs[0])
  parts=bs[1].split(r'\,') if r'\,' in bs[1] else bs[1].split(r'\qquad')
  assert len(parts)==2
  assert eq(read(parts[0].split('=')[1]),dx)
  assert eq(read(parts[1].split('=')[1]),dy)
  rows=bs[2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\')
  # Ensure the factor/trig-solving operative chain cannot disappear while equal final values survive.
  required=6 if template.startswith('spiral') else 3 if template in ('polynomial_two','paired_cubics','line_cubic') else 1
  assert len(rows)==required,(template,rows)
  for ri,row in enumerate(rows):
   row=row.replace('&','').strip().rstrip('.')
   if '⟹' in row:
    left,final=row.split('⟹');assert eq(read(left.split('=')[0]),target);listed=[read(z) for z in final.split('=')[1].split(',')];assert sp.FiniteSet(*listed)==sp.FiniteSet(*roots)
   elif row.split('=')[0].strip()=='t':
    listed=[read(z) for z in row.split('=')[1].split(',')];assert sp.FiniteSet(*listed)==sp.FiniteSet(*roots)
   else:
    left,right=row.split('=');lhs=read(left);rhs=read(right)
    assert all(eq((lhs-rhs).subs(T,z),0) for z in roots)
    if ri==0:assert eq(lhs,target)
    if ri==1 and template in ('polynomial_two','paired_cubics','line_cubic'):assert eq(lhs,target)
  if len(bs)==4:
   rows=bs[3].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==len(roots)
   for row,z in zip(rows,roots):
    row=row.replace('&','').strip().rstrip(',');parts=row.split('=');arg=re.search(r'\((.*?)\)',parts[0]).group(1);assert eq(read(arg),z)
    values=[read(part.split(r'\ne')[0]) for part in parts[1:]]
    assert all(eq(v,other.subs(T,z)) for v in values),(template,row,values,other.subs(T,z))
    assert all(not eq(v,0) for v in values)
  else:
   note=re.search(r'Note that \$\{([xy])\}\^\{′\}\((.*?)\)=(.*?)'+re.escape(r'\ne')+r' 0\.\$',solution)
   assert note,solution
   letter,arg,val=note.groups();assert eq(read(arg),roots[0]);assert eq(read(val),(dx if letter=='x' else dy).subs(T,roots[0])) and not eq(read(val),0)
  conclusion=solution[solution.index('Therefore'):] if 'Therefore' in solution else solution[solution.index('which confirms'):]
  vals=[read(v) for v in re.findall(r'\$t\s*=\s*(.*?)\$',conclusion)]
  assert sp.FiniteSet(*vals)==sp.FiniteSet(*roots)
 for text in [q[':question/problem'],solution or '']+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
  assert text.count('$')%2==0
  depth=0
  for c in text:
   depth+=(c=='{')-(c=='}');assert depth>=0
  assert depth==0
  assert '--' not in text and '+-' not in text
 return roots

