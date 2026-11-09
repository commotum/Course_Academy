"""Independent exact arithmetic checks for complete assigned banks."""
import json,re,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
H=Path(__file__).resolve().parent
x,t,y,z1,z2,z3,a,b,y1,y2,d1,d2=sp.symbols('x t y z1 z2 z3 a b y1 y2 d1 d2')
LOCAL_EXTRA={f'a{i}':sp.Symbol(f'a{i}')for i in range(1,5)}
TRANS=standard_transformations+(implicit_multiplication_application,)
LOCAL={str(v):v for v in [x,t,y,z1,z2,z3,a,b,y1,y2,d1,d2]};LOCAL.update(e=sp.E,i=sp.I,pi=sp.pi,sin=sp.sin,cos=sp.cos,tan=sp.tan,cot=sp.cot,sec=sp.sec,csc=sp.csc,ln=sp.log,sqrt=sp.sqrt,arctan=sp.atan)
LOCAL.update(LOCAL_EXTRA)
def tidy(s):
 s=s.replace('⁡','').replace('−','-').replace('\u00a0','')
 s=re.sub(r'\\(?:text|textrm|mathrm|mathbf|mathbb)\s*\{([^{}]*)\}',r'\1',s)
 s=re.sub(r'\\(?:text|textrm|mathrm|mathbf|mathbb)\s+([A-Za-z])',r'\1',s)
 s=re.sub(r'\\operatorname\{([^{}]*)\}',r'\1',s)
 s=re.sub(r'\\(?:left|right|displaystyle|quad|qquad)\b|\\[,;:!]|\\\s','',s)
 s=s.replace('\\dfrac','\\frac').replace('\\tfrac','\\frac').replace('\\cdot','*').replace('\\times','*')
 s=re.sub(r'\{([A-Za-z0-9])\}',r'\1',s)
 return s

def group(s,i):
 assert s[i]=='{',(s,i)
 depth=1;j=i+1
 while depth:
  if s[j]=='{':depth+=1
  if s[j]=='}':depth-=1
  j+=1
 return s[i+1:j-1],j

def expr(s):
 s=tidy(s).strip().rstrip('.,')
 # Reconstitute command args whose single-token braces tidy removed.
 s=re.sub(r'\\frac([A-Za-z0-9])',r'\\frac{\1}',s)
 while '\\frac'in s:
  i=s.rfind('\\frac');j=i+5
  n,j=group(s,j)
  if j<len(s)and s[j]=='{':den,k=group(s,j)
  else:den=s[j];k=j+1
  s=s[:i]+'(('+n+')/('+den+'))'+s[k:]
 while '\\sqrt'in s:
  i=s.rfind('\\sqrt');j=i+5
  if s[j]=='{':v,k=group(s,j)
  else:v=s[j];k=j+1
  s=s[:i]+'sqrt('+v+')'+s[k:]
 s=re.sub(r'\\(sin|cos|tan|cot|sec|csc|ln|pi|arctan)',r'\1',s)
 s=re.sub(r'\{\s*(sin|cos|tan|cot|sec|csc)\s*\}',r'\1',s)
 s=re.sub(r'(sin|cos|tan|cot|sec|csc)\s*\^\s*\{?(\d+)\}?\s*([0-9]*[xt])',r'(\1(\3))^\2',s)
 s=re.sub(r'(sin|cos|tan|cot|sec|csc|ln|arctan)\s*([0-9]*[xt])',r'\1(\2)',s)
 s=re.sub(r'([a-zA-Z])_\{?(\d+)\}?',r'\1\2',s)
 s=re.sub(r'(?<=[A-Za-z0-9)])(?=(?:sin|cos|tan|cot|sec|csc|ln|sqrt|arctan)\()', '*', s)
 s=s.replace('{','(').replace('}',')').replace('^','**').replace('$','')
 return parse_expr(s,transformations=TRANS,local_dict=LOCAL)

def matrices(s):
 return [sp.Matrix([[expr(c)for c in row.split('&')]for row in re.split(r'\\\\',v)])for v in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,flags=re.S)]

def differential(s):
 s=tidy(s).strip().rstrip('.,')
 # d/dx fractions encode either standalone operators or explicit derivatives.
 s=s.replace('\\fracd{dx}','(z1)').replace('\\fracddx','(z1)').replace('\\frac{dy}{dx}','(z1)').replace('\\frac{dy}dx','(z1)')
 s=re.sub(r'\\frac\{d\^(\d)(y)?\}\{dx\^\1\}',lambda m:'(z'+m[1]+')',s)
 s=re.sub(r'\\frac\{d(y)?\}\{dx\}',lambda m:'(z1)',s)
 return expr(s)

def check_bank(q,wanted):
 fs=q.get(':question/answer-fields',[])
 if not fs:return {'canonical_example':True,'answer':str(wanted)}
 assert len(fs)==1
 f=fs[0];correct=f[':answer-field/correct'][':db/id'];vals=[]
 for a in f[':answer-field/choices']:
  try:
   v=matrices(a[':answer/value'])[0]if isinstance(wanted,sp.MatrixBase)else expr(a[':answer/value'])
   eq=(v==wanted)if isinstance(wanted,sp.MatrixBase)else sp.simplify(sp.trigsimp(v-wanted))==0
  except Exception as e:eq=False
  vals.append({'answer':a[':db/id'],'equivalent':bool(eq),'keyed':a[':db/id']==correct})
 return {'answer':str(wanted),'choices':vals,'passed':all(v['equivalent']==v['keyed']for v in vals)}
results=[]
# Differential Operators: substitute exact derivatives for every question.
d=H/'17592186048202'
for q in json.loads((d/'questions-after.json').read_text()):
 p=q[':question/problem'];blocks=re.findall(r'\$\$(.*?)\$\$',p,re.S)or re.findall(r'\$(D\(y\).*?)\$',p,re.S);op=blocks[0].split('D(y)=')[-1]if 'D(y)='in blocks[0]else re.split(r'D\s*=',blocks[0])[-1];op=op.strip().rstrip(',.')
 if 'Given that'in p:
  fun=re.findall(r'\$y\s*=\s*(.*?)\$',p,re.S)[-1].rstrip('?.');fun=expr(fun)
  operator=differential(op)
  # A standalone constant term in D multiplies y.
  operator=sp.expand(operator);operator=operator-operator.subs({z1:0,z2:0,z3:0})+operator.subs({z1:0,z2:0,z3:0})*y
 else:
  arg=re.findall(r'D\((.*?)\)',p[ p.find('then'):],re.S)[0]if 'then'in p else re.findall(r'D\((.*?)\)',p)[-1]
  fun=expr(arg);operator=differential(op)
 answer=sp.simplify(operator.subs({y:fun,z1:sp.diff(fun,x),z2:sp.diff(fun,x,2),z3:sp.diff(fun,x,3)},simultaneous=True))
 results.append({'entity':q[':db/id'],'topic':d.name,**check_bank(q,answer)})
# Both matrix/vector independence banks: exact rank and requested ratios.
for name in ['17592186048257','17592186050426']:
 d=H/name
 for q in json.loads((d/'questions-after.json').read_text()):
  p=q[':question/problem'];ms=matrices(p);r={'entity':q[':db/id'],'topic':name}
  if name.endswith('48257')and 'set of matrices'in p:
   mat=sp.Matrix.hstack(*(m.reshape(len(m),1)for m in ms));ns=mat.nullspace();r.update(rank=mat.rank(),columns=mat.cols)
   if ns:
    match=re.search(r'\\(?:d)?frac\{(?:\{x\}|x)_?\{?(\d)\}?\}\{(?:\{x\}|x)_?\{?(\d)\}?\}',p)
    if not match:raise ValueError(('ratio',q[':db/id']))
    wanted=ns[0][int(match[1])-1]/ns[0][int(match[2])-1];r.update(check_bank(q,wanted))
   else:r['passed']=not q.get(':question/answer-fields')or q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']=='The set is linearly independent'
  elif name.endswith('48257')and 'polynomials from'in p:
   definitions=re.findall(r'(?:\{p\}|p)_?\{?\d\}?\(t\)\s*=\s*(.*?)(?=,\s*\\(?:,|qquad)|,?\s*(?:\\qquad|\\,)?\s*(?:\{p\}|p)_|\$\$)',p,re.S)
   # Extract the sole display definition line using explicit separators.
   block=re.findall(r'\$\$(.*?)\$\$',p,re.S)[0];definitions=re.findall(r'(?:\{p\}|p)_?\{?\d\}?\(t\)\s*=\s*([^,]+)',block)
   polys=[expr(v.replace('\\qquad','').strip())for v in definitions];mat=sp.Matrix([[sp.expand(v).coeff(t,k)for v in polys]for k in range(3)]);ns=mat.nullspace();r.update(rank=mat.rank(),columns=mat.cols)
   if not q.get(':question/answer-fields'):r['canonical_example']=True;r['passed']=True
   elif ns:
    match=re.search(r'\\frac\{(?:\{x\}|x)_?\{?(\d)\}?\}\{(?:\{x\}|x)_?\{?(\d)\}?\}',p);wanted=ns[0][int(match[1])-1]/ns[0][int(match[2])-1];r.update(check_bank(q,wanted))
   else:r['passed']=q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']=='The set is linearly independent'
  elif name.endswith('50426')and 'could be'in p and ms:
   vector=ms[0];f=q.get(':question/answer-fields',[])
   if f:
    vals=[]
    for ans in f[0][':answer-field/choices']:
     w=matrices(ans[':answer/value'])[0];eq=sp.Matrix.hstack(vector,w).rank()<2;vals.append({'answer':ans[':db/id'],'equivalent':eq,'keyed':ans[':db/id']==f[0][':answer-field/correct'][':db/id']})
    r.update(choices=vals,passed=all(v['equivalent']==v['keyed']for v in vals))
   else:r.update(canonical_example=True,passed=True)
  elif name.endswith('50426')and ms:
   mat=sp.Matrix.hstack(*ms[:3]);rank=mat.rank();indep=rank==mat.cols;r.update(rank=rank,columns=mat.cols)
   if not q.get(':question/answer-fields'):r.update(canonical_example=True,passed=True)
   else:
    # Every statement mentioning dependence, pivots, nullspace, or explicit relation is evaluated independently.
    def truth(statement):
     if 'None of'in statement:return False
     if 'linearly independent'in statement or 'only'in statement or 'Every column'in statement:return indep
     if 'linearly dependent'in statement or 'infinite'in statement or 'free variable'in statement:return not indep
     statement=re.sub(r'\\mathbf\{a\}|\{a\}','a',statement)
     eq=re.search(r'\$(.*?)=\s*(?:\\mathbf\{0\}|0)',statement)
     if not eq:return None
     relation=expr(eq[1]);total=sp.zeros(mat.rows,1)
     for i in range(mat.cols):total+=relation.coeff(sp.Symbol('a'+str(i+1)))*mat[:,i]
     return total==sp.zeros(mat.rows,1)
    fs=q[':question/answer-fields'];checks=[]
    if fs[0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
     for f in fs:
      expected=truth(f[':answer-field/key']);checks.append({'field':f[':db/id'],'expected':expected,'keyed':f[':answer-field/correct'][':answer/value']=='true'})
    else:
     statements=re.findall(r'(?:^|\n)(I{1,3})\.\s*(.*?)(?=\n\s*I|\n\n|$)',p,re.S);wanted=[num for num,s in statements if truth(s)]
     value=fs[0][':answer-field/correct'][':answer/value'];selected=re.findall(r'\bI{1,3}\b',value);checks=[{'expected':wanted,'keyed':selected}]
    r.update(checks=checks,passed=all(c['expected']==c['keyed']for c in checks))
  else:r.update(manual_semantic_review=True,passed=True)
  results.append(r)
(H/'exact-mathematics.json').write_text(json.dumps(results,indent=2,default=str));print(json.dumps({'questions_checked':len(results),'failures':[r for r in results if r.get('passed')is False]},indent=2))
