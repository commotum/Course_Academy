"""Independent actual prompt/solution/bank reader; never imports the generator.

No parameter metadata is used to decide mathematical validity. New plots are
read from PNG pixels (axes, grid spacing, red marker centers), not plot sidecars.
"""
import hashlib,json,re
from fractions import Fraction
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x=s.Symbol('x');TRANS=standard_transformations+(implicit_multiplication_application,)
def scalar(t):
 t=t.strip().rstrip('.').replace(r'\,','').replace('✓','').replace(r'\times','').strip()
 t=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',t)
 assert re.fullmatch(r'[\dx+*/().\-\s]+',t),('unsupported scalar',t)
 return parse_expr(t,local_dict={'x':x},transformations=TRANS)
def equation(prompt):
 m=re.search(r'\$y\s*=\s*([^$?]+)',prompt);assert m,prompt
 return s.expand(scalar(m[1]))
def coordinates(solution):
 first=solution.split('\n\n',1)[0];pairs=re.findall(r'([ABC])=?\((-?\d+),(-?\d+)\)',first)
 assert len(pairs)==3 and {a for a,_,_ in pairs}==set('ABC'),('summary coordinates',first)
 return {a:(int(b),int(c))for a,b,c in pairs}
def subset(value):
 labels=re.findall(r'\$([ABC])\$',value);assert labels and len(labels)==len(set(labels)),value
 assert re.sub(r'\$[ABC]\$|\band\b|\bonly\b|\s','',value)=='',value
 return frozenset(labels)
def fingerprint(q):
 e=equation(q[':question/problem']);points=coordinates(q[':question/worked-solution'])
 task={'equation':[str(Fraction(str(e.coeff(x)))),str(Fraction(str(e.subs(x,0))))],'points':sorted([list(v)for v in points.values()]),'task':'identify all supplied points satisfying line'}
 return hashlib.sha256(json.dumps(task,sort_keys=True).encode()).hexdigest()
def check(rec,check_plot=True):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];expr=equation(prompt);points=coordinates(sol);truth={a for a,(xx,y)in points.items()if expr.subs(x,xx)==y}
 fields=q[':question/answer-fields'];values=0
 if fields[0][':answer-field/type'].endswith('/checkbox'):
  assert len(fields)==3 and {f[':answer-field/key']for f in fields}==set('ABC')
  for f in fields:
   assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==['false','true']
   correct=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert(correct=='true')==(f[':answer-field/key']in truth)
   values+=2
  assert not re.findall(r'\\begin\{aligned\}',sol),'unrated short solution shape changed'
  # These original short solutions explicitly assert the matching label.
  assert re.search(r'Only B satisfies',sol)and truth=={'B'}
  stages=0
 else:
  assert len(fields)==1 and fields[0][':answer-field/key']=='selection'
  f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio'
  bank=[subset(a[':answer/value'])for a in f[':answer-field/choices']];assert len(bank)==5 and len(set(bank))==5
  key=next(subset(a[':answer/value'])for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert key==truth and sum(v==truth for v in bank)==1,('key',key,truth)
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==3
  intros=re.findall(r'Substituting the point \$([ABC])\((-?\d+),(-?\d+)\)\$ results in (?:a )?(true|false) statement:',sol);assert len(intros)==3,sol
  conclusions=re.findall(r'Therefore, the point \$([ABC])\$ does ((?:\*not\* |not )?)lie on the line\.',sol);assert len(conclusions)==3
  for label,block,intro,conclusion in zip('ABC',blocks,intros,conclusions):
   xx,y=points[label];ok=label in truth
   assert intro==(label,str(xx),str(y),'true'if ok else'false'),('stale target/truth',intro,points[label])
   assert conclusion[0]==label and(bool(conclusion[1])is(not ok)),('conclusion',conclusion)
   rows=[r.strip()for r in block.split(r'\\')];assert len(rows)==3,rows
   eqs=[[v.strip()for v in r.split('&')]for r in rows];assert all(len(v)==2 for v in eqs),eqs
   assert eqs[0][0]=='y'and eqs[0][1].strip().startswith('=')
   assert s.expand(scalar(eqs[0][1].strip()[1:])-expr)==0,('stage1 equation',block)
   # Check the actual substitution operand as well as its evaluated value.
   sub=re.fullmatch(r'\s*=(.*?)\((-?\d+)\)(.*)',eqs[1][1]);assert sub,eqs[1]
   assert scalar(sub[1])==expr.coeff(x)and int(sub[2])==xx and scalar(sub[3]or'0')==expr.subs(x,0),('stage2 operands',sub.groups(),xx,expr)
   assert scalar(eqs[1][0])==y and scalar(eqs[1][1].strip()[1:])==expr.subs(x,xx),('stage2 substitution',block)
   assert scalar(eqs[2][0])==y and scalar(eqs[2][1].strip()[1:])==expr.subs(x,xx),('stage3 evaluation',block)
   assert('✓'in block)==ok and(r'\times'in block)==(not ok),('stage truth mark',block)
  final=re.search(r'Finally, only points? (.*?) lie(?:s)? on the line\.',sol);assert final and frozenset(re.findall(r'\$([ABC])\$',final[1]))==truth,('final subset',sol)
  assert 'To check whether a point lies on the line, we substitute the coordinates of the point into the equation and determine whether the resulting statement is true.'in sol
  values=5;stages=9
 if check_plot:
  image=re.search(r'!\[\]\((.*?)\)',prompt)[1]
  if Path(image).is_absolute():check_png(image,points)
 return {'points':{a:list(v)for a,v in points.items()},'truth':sorted(truth),'equation':str(expr),'stages':stages,'answer_values':values,'task':fingerprint(q)}

def check_png(path,points):
 """Infer plotted coordinates directly from PNG black axes/gray grid/red pixels."""
 from PIL import Image
 import numpy as np
 im=np.array(Image.open(path).convert('RGB'));red=(im[:,:,0]>180)&(im[:,:,1]<100)&(im[:,:,2]<100);ys,xs=np.where(red);assert len(xs)>15,path
 # Three disjoint red marker components; labels use black pixels.
 pixels=set(zip(xs.tolist(),ys.tolist()));centers=[]
 while pixels:
  seed=pixels.pop();pending=[seed];component=[seed]
  while pending:
   xx,yy=pending.pop()
   for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
    v=(xx+dx,yy+dy)
    if v in pixels:pixels.remove(v);pending.append(v);component.append(v)
  if len(component)>4:centers.append(tuple(np.mean(component,axis=0)))
 assert len(centers)==3,('red components',path,centers)
 black=np.max(im,axis=2)<80;ox=int(np.argmax(black.sum(axis=0)));oy=int(np.argmax(black.sum(axis=1)))
 gray=(np.max(im,axis=2)-np.min(im,axis=2)<4)&(im[:,:,0]>170)&(im[:,:,0]<220)
 def spacing(counts):
  candidates=np.where(counts>max(35,counts.max()*.6))[0];groups=[]
  for v in candidates:
   if groups and v-groups[-1][-1]<=2:groups[-1].append(v)
   else:groups.append([v])
  centers=[sum(g)/len(g)for g in groups];diffs=np.diff(centers);assert len(diffs)>=2,(path,centers)
  estimate=float(np.median(diffs));units=np.rint(diffs/estimate);return float(sum(diffs)/sum(units))
 sx=spacing(gray.sum(axis=0));sy=spacing(gray.sum(axis=1));assert abs(sx-sy)<1,(sx,sy)
 actual=sorted(((cx-ox)/sx,(oy-cy)/sy)for cx,cy in centers);expected=sorted(points.values())
 assert all(abs(a-c)<.12 and abs(b-d)<.12 for(a,b),(c,d)in zip(actual,expected)),('plotted coordinate mismatch',path,actual,expected)
 return {'pixel_coordinates':actual,'origin_pixel':[ox,oy],'unit_pixel':[sx,sy]}
