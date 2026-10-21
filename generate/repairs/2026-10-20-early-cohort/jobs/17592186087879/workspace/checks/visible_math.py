import re
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
x=s.Symbol('x',positive=True);y=s.Symbol('y');D=s.Symbol('D')
def clean(t):
 return t.replace('\\\\frac','\\frac').replace('\\\\operatorname','\\operatorname').replace('\\u2061','').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\quad','').replace(r'\!','')
def group(t,i):
 while t[i].isspace():i+=1
 assert t[i]=='{',(t,i)
 j=i+1;d=1;k=j
 while d:
  if t[k]=='{':d+=1
  if t[k]=='}':d-=1
  k+=1
 return t[j:k-1],k
def expr(t):
 t=clean(t).strip().rstrip('.').replace(r'\dfrac',r'\frac')
 t=re.sub(r'\\operatorname\{(sin|cos|ln)\}',r'\\\1',t)
 while r'\frac' in t:
  i=t.index(r'\frac');a,j=group(t,i+5);b,k=group(t,j);t=t[:i]+'(('+str(expr(a))+')/('+str(expr(b))+'))'+t[k:]
 for a,b in [(r'\cdot','*'),(r'\pi','pi'),(r'\sin',' sin '),(r'\cos',' cos '),(r'\ln',' log ')]:t=t.replace(a,b)
 t=t.replace('{','(').replace('}',')')
 return parse_expr(t,local_dict={'x':x,'y':y,'D':D,'e':s.E,'pi':s.pi,'sin':s.sin,'cos':s.cos,'log':s.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def eq(a,b):return s.simplify(a-b)==0
def promptdata(r):
 t=clean(r['question'][':question/problem']);blocks=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$',t,re.S)
 t=next(a or b for a,b in blocks if 'dy' in a+b or r'\text{d}y' in a+b)
 t=re.sub(r'\\frac\{\\text\{d\}y\}\{\\text\{d\}x\}|\\frac\{dy\}\{dx\}','D',t)
 initial=re.search(r'y\((.*?)\)\s*=\s*(-?\d+)',t);assert initial,t
 point=expr(initial[1]);h=expr(initial[2]);ode=t[:initial.start()].replace('x>0','').rstrip(' ,');lhs,rhs=ode.split('=',1);lhs=expr(lhs);a=s.expand(lhs).coeff(D)
 return s.simplify(lhs.coeff(y)/a),s.simplify(expr(rhs)/a),point,h

def mathcheck(r):
 try:
  p,q,t,h=promptdata(r);fields=r['question'][':question/answer-fields'];checks=[]
  for fi,f in enumerate(fields):
   vals=[expr(a[':answer/value']) for a in f[':answer-field/choices']];cid=f[':answer-field/correct'][1];correct=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==cid)
   valid=[(eq(s.diff(v,x),p*v) and v!=0) if fi==0 else (eq(s.diff(v,x)+p*v,q) and eq(v.subs(x,t),h)) for v in vals]
   checks.append({'field':fi,'valid_indices': [i for i,v in enumerate(valid) if v],'key_index':correct,'key_valid':valid[correct],'exactly_one':sum(valid)==1})
  final=re.findall(r'\$\$\s*y\s*=(.*?)\$\$',r['question'][':question/worked-solution'],re.S)
  final_ok=None
  if final:
   v=expr(final[-1]); final_ok=eq(s.diff(v,x)+p*v,q) and eq(v.subs(x,t),h)
  return {'id':r['question'][':question/id'],'template':r['generation']['template'],'parameters':r['generation']['parameters'],'displayed':{'P':str(p),'Q':str(q),'t':str(t),'h':str(h)},'fields':checks,'final_solution_valid':final_ok,'passed':all(c['key_valid'] and c['exactly_one'] for c in checks) and final_ok is not False}
 except Exception as e:return {'id':r['question'][':question/id'],'template':r['generation']['template'],'error':repr(e),'passed':False}

