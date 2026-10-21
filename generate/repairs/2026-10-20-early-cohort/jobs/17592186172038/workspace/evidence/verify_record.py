"""Fail closed: displayed math, geometry, complete banks, source prose, grader."""
import concurrent.futures,importlib.util,json,math,re,subprocess,random,hashlib,tempfile,shutil
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parents[1]/'17592186172038';ROOT=HERE.parent;ASSETS=ROOT/'evidence/assets'
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def latex(s):
 s=s.strip().rstrip(',.?').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*')
 def group(s,i):
  assert s[i]=='{';depth=1;j=i+1
  while depth:
   if s[j]=='{':depth+=1
   if s[j]=='}':depth-=1
   j+=1
  return s[i+1:j-1],j
 while r'\frac' in s:
  i=s.index(r'\frac');a,j=group(s,i+5);b,k=group(s,j);s=s[:i]+f'(({latex(a)})/({latex(b)}))'+s[k:]
 s=s.replace('^','**').replace('{','(').replace('}',')')
 return parse_expr(s,local_dict={'x':g.X,'y':g.Y},transformations=standard_transformations+(implicit_multiplication_application,))

def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];m=r['generation'];f=q[':question/answer-fields'][0]
 expr=latex(q[':question/problem'].split('=',1)[1].rstrip('$?'))
 if m['bank_profile']=='authored' and m['template']=='affine_fraction':assert q[':question/problem'].split('=',1)[1].count(r'\frac')>=1
 assert sp.simplify(expr-g.eq(m['template'],m['parameters']))==0
 pts=m['parameters']['points'];s=[expr.subs({g.X:x,g.Y:y}) for x,y in pts]
 assert list(map(str,s))==m['exact_slopes']
 banks=[]
 for a in f[':answer-field/choices']:
  path=ASSETS/a[':answer/value'];assert path.exists();meta=json.loads(path.with_suffix('.json').read_text());assert meta['exact_points']==pts
  row=[]
  for (x,y),segment in zip(pts,meta['segments']):
   assert segment['center']==[float(sp.Rational(x)),float(sp.Rational(y))];end=segment['endpoints'];dx=end[1][0]-end[0][0];dy=end[1][1]-end[0][1]
   v=sp.oo if segment['slope']=='inf' else sp.Rational(segment['slope']);row.append(v)
   assert (abs(dx)<1e-12 if v==sp.oo else math.isclose(dy,float(v)*dx,abs_tol=1e-12))
   assert all(meta['bounds'][0]<px<meta['bounds'][1] and meta['bounds'][2]<py<meta['bounds'][3] for px,py in end)
  assert list(map(str,row))==m['choice_geometry'][a[':answer/value']];banks.append(tuple(row))
  if a[':answer/id']==f[':answer-field/correct'][1]:assert list(row)==s
 assert len(banks)==len(set(banks))==5 and banks.count(tuple(s))==1
 if m['bank_profile']=='authored':
  for i,row in enumerate(banks):
   for other in banks[:i]:
    distances=[]
    for a,b in zip(row,other):
     aa=math.pi/2 if a==sp.oo else math.atan(float(a));bb=math.pi/2 if b==sp.oo else math.atan(float(b));delta=abs(aa-bb);distances.append(min(delta,math.pi-delta))
    assert max(distances)>=math.radians(8)
 solution=q[':question/worked-solution'];block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S).group(1);rows=block.split(r'\\');assert len(rows)==3
 for i,row in enumerate(rows):
  coords=re.search(r'\|\}_\{\((.*?)\)\}',row);assert coords
  shown=[latex(v) for v in coords.group(1).split(',')];assert shown==list(map(sp.Rational,pts[i]))
  values=row.split('=',1)[1].split('=');assert len(values)==(3 if m['bank_profile']=='authored' and not q[':question/difficulty'].endswith('/easy') else 2)
  assert all(sp.simplify(latex(v)-s[i])==0 for v in values)
 assert q[':question/problem'].count('$')%2==0 and solution.count('$')%2==0
 for text in [q[':question/problem'],solution]:
  assert text.count('{')==text.count('}')
  assert not re.search(r'--|\+\s*-',text),text
 correctpath=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert f'![]({correctpath})' in solution
 return True

