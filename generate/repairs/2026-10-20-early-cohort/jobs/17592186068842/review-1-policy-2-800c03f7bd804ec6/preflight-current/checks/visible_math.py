import json,pathlib,re,copy,hashlib,collections
import sympy as S
R=pathlib.Path(__file__).resolve().parent.parent/'evidence'
read=lambda n:json.load(open(R/n))
def save(n,v):(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False))
x,y,v=S.symbols('x y v',real=True)
# A review-owned recursive TeX reader. Author parser/validator is never called here.
def group(t,pos):
 assert t[pos]=='{';depth=1;end=pos+1
 while depth:
  depth+=(t[end]=='{')-(t[end]=='}');end+=1
 return t[pos+1:end-1],end

def compile_tex(t):
 t=t.replace(r'\frac{\text{d}y}{\text{d}x}','v').replace(r'\cdot','*').replace(r'\,','').replace(r'\text{ }','').replace(r'\left','').replace(r'\right','').replace('⁡','')
 t=re.sub(r'\\operatorname\{(sin|csc)\}([0-9]*x)',lambda m:' '+m[1]+'('+m[2]+')',t).strip().rstrip('.,')
 out='';i=0
 while i<len(t):
  if t.startswith('\\frac',i):
   top,j=group(t,i+5);bot,i=group(t,j);out+='(('+compile_tex(top)+')/('+compile_tex(bot)+'))'
  elif t.startswith('\\sqrt',i):
   a,i=group(t,i+5);out+='sqrt('+compile_tex(a)+')'
  elif t[i]=='{':
   a,i=group(t,i);out+='('+compile_tex(a)+')'
  elif t[i]=='^':out+='**';i+=1
  else:out+=t[i];i+=1
 return out
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application

def expr(t):return parse_expr(compile_tex(t),local_dict={'x':x,'y':y,'v':v,'e':S.E,'sin':S.sin,'csc':S.csc,'sqrt':S.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def equation(t):
 l,r=t.split('=');return expr(l),expr(r)
def resolved(t):
 l,r=equation(t);return S.cancel((r-l.subs(v,0))/S.diff(l,v))
def same(a,b):return S.simplify(S.expand_power_exp(a-b))==0
def sep(t):
 l,r=equation(t);return S.simplify(S.diff(S.diff(l,v),x))==0 and not r.has(y,v) and l.subs(v,0)==0

def check_record(r):
 q=r['question'];prompt=re.findall(r'\$\$(.*?)\$\$',q[':question/problem'],re.S)[0];ode=resolved(prompt)
 f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];valid=[c[':answer/id'] for c in cs if sep(c[':answer/value']) and same(resolved(c[':answer/value']),ode)]
 stages=[]
 for b in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)[2:]:
  if '\\begin{aligned}' in b:
   rows=b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');lhs=None
   for row in rows:
    row=row.replace('&','').strip()
    if row.startswith('='):row=lhs+row
    else:lhs=row.split('=')[0]
    stages.append({'expression':row,'equivalent':same(resolved(row),ode)})
  else:stages.append({'expression':b.strip(),'equivalent':same(resolved(b),ode)})
 return {'id':q[':question/id'],'template':r['generation']['template'],'valid_choices':valid,'stored_key':f[':answer-field/correct'][1],'passed':valid==[f[':answer-field/correct'][1]] and all(z['equivalent'] for z in stages),'stages':stages}

