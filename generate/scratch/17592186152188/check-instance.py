"""Step 7 fail-closed replay, displayed mathematics, identity, scope and grading."""
import importlib.util,json,re,hashlib,subprocess,sys
from pathlib import Path
import sympy as s
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('ellipse',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
C,S=s.symbols('C S',real=True)
def read(expr):
 expr=expr.strip().rstrip('.,').replace('&','').strip()
 for trig,token in [('cos','C'),('sin','S')]:
  expr=re.sub(r'\{'+trig+r'\}\^\{2\}⁡(?:\\theta|t)',token+'^{2}',expr)
  expr=re.sub(r'\\'+trig+r'\^2\\theta',token+'^{2}',expr)
  expr=re.sub(r'\\operatorname\{'+trig+r'\}⁡(?:\\theta|t)',token,expr)
  expr=re.sub(r'\\'+trig+r'\\theta',token,expr)
 value=g.tex_expr(expr)
 return value.subs({s.Symbol('C'):C,s.Symbol('S'):S})
def reduce(expr):return s.simplify(s.expand(expr).subs(S**2,1-C**2))
def formula_from_prompt(q):
 block=re.findall(r'\$\$(.*?)\$\$',q[':question/problem'],re.S)[0]
 if r'\frac{x}' in block:
  eqs=block.split(r',\quad ')[:2];vals=[]
  for v,eq in zip([g.X,g.Y],eqs):
   left,right=eq.split('=');vals.append(s.solve(read(left)-read(right),v)[0])
 else:
  m=re.search(r'x=(.*?),\\(?:,|quad )y=(.*?),\\(?:,|quad )0',block)
  assert m,block
  vals=[read(m.group(1)),read(m.group(2))]
 ax=vals[0].coeff(C);by=vals[1].coeff(S);h=vals[0].subs(C,0);k=vals[1].subs(S,0)
 assert ax>0 and by>0
 return vals, (g.X-h)**2/ax**2+(g.Y-k)**2/by**2

def check(record):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==g.KP_ID
 q=record['question'];f=q[':question/answer-fields'][0]
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in f[':answer-field/choices']]:
  assert text.count('$')%2==0
  depth=0
  for char in text:
   if char=='{':depth+=1
   if char=='}':depth-=1
   assert depth>=0
  assert depth==0
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 vals,expected=formula_from_prompt(q)
 p=record['generation']['parameters'];a,b,h,k=[s.sympify(p[z]) for z in ['a','b','h','k']]
 assert s.simplify(vals[0]-(a*C+h))==0 and s.simplify(vals[1]-(b*S+k))==0
 # Every printed algebraic row including formal first equations and final prose
 # conclusion must describe the actually printed parametric object.
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)
 counts=[];rows_checked=0
 for block in blocks:
  body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');rows=body.split('\\\\');counts.append(len(rows))
  for row in rows:
   sides=[read(x) for x in row.split('=')]
   for left,right in zip(sides,sides[1:]):
    assert reduce((left-right).subs({g.X:vals[0],g.Y:vals[1]}))==0,(record['generation'],row,left,right)
   rows_checked+=1
 target=g.tex_expr(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]).split('=')[0])
 assert s.simplify(target-expected)==0,(record['generation'],target,expected)
 residuals=[]
 for answer in f[':answer-field/choices']:
  # Complete equations are normalized by their constant, independently of sides.
  if '=' in answer[':answer/value']:
   lhs,rhs=answer[':answer/value'].split('=');res=g.tex_expr(lhs)-g.tex_expr(rhs)
  else:res=g.tex_expr(answer[':answer/value'])-1
  res=s.Poly(res,g.X,g.Y,extension=True);res=res.monic().as_expr();residuals.append(res)
 assert len(set(map(str,residuals)))==len(residuals)
 return {'template':record['generation']['template'],'parameters':p,'rows_checked':rows_checked,'block_row_counts':counts,'correct_displayed_math':True}

