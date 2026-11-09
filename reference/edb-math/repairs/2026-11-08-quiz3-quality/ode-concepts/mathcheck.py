import json,re,sys
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
H=Path(__file__).resolve().parent
x,t,A,B,C,Y,Z,D,U,V=S.symbols('x t A B C Y Z D U V',real=True)
loc={str(v):v for v in [x,t,A,B,C,Y,Z,D,U,V]};loc.update(e=S.E,pi=S.pi,sin=S.sin,cos=S.cos,tan=S.tan,cot=S.cot,sec=S.sec,csc=S.csc,ln=S.log,log=S.log,sqrt=S.sqrt,arctan=S.atan,arcsin=S.asin,Q=S.Function('Q'),W=S.Function('W'))
def expr(s):
 s=s.replace('\u2061','').replace('π',r'\pi').replace('−','-');s=re.sub(r'\\(?:operatorname|mathrm|textrm|text)\s*\{\s*([^{}]+?)\s*\}',r'\1 ',s)
 s=re.sub(r'\\(?:left|right|displaystyle)\b|\\[,;!]|\\(?:quad|qquad)', '',s);s=s.replace(r'\cdot','*').replace(r'\times','*')
 s=re.sub(r'\{([yYuU])\}',r'\1',s)
 for c,a in [('y',Y),('u',U)]:
  s=re.sub(c+r'\^\{(?:″|\'\'|\\prime\s*\\prime|\\doubleprime)\}',str(D if c=='y'else V),s)
  s=re.sub(c+r'\^\{(?:′|\'|\\prime)\}','Z' if c=='y'else 'V1',s)
 s=s.replace('YDER','Z').replace('UDER','V1')
 s=re.sub(r"y\s*'\s*'",'D',s);s=re.sub(r"y\s*'",'Z',s)
 s=s.replace("y''",'D').replace("y'",'Z').replace("u''",'V').replace("u'",'V1')
 s=s.replace(r'\frac{dy}{dx}','Z')
 s=re.sub(r'\\(?:dfrac|frac)\{d\s*y\}\{d\s*x\}', 'Z', s)
 # balanced LaTex fractions -> explicit parenthesized division
 def group(v,i):
  if v[i]!='{':return v[i],i+1
  depth=1;j=i+1
  while depth:
   if v[j]=='{':depth+=1
   elif v[j]=='}':depth-=1
   j+=1
  return v[i+1:j-1],j
 while (m:=re.search(r'\\(?:dfrac|frac|tfrac)\s*',s)):
  aa,j=group(s,m.end());bb,k=group(s,j);s=s[:m.start()]+'(('+aa+')/('+bb+'))'+s[k:]
 s=s.replace(r'\sqrt', 'sqrt').replace(r'\pi','pi')
 s=re.sub(r'\\(sin|cos|tan|cot|csc|sec|ln|log|exp|arctan)\b',r'\1 ',s)
 s=s.replace('{','(').replace('}',')').replace('^','**')
 s=re.sub(r'(?<![A-Za-z])([yu])(?![A-Za-z])',lambda m:'Y'if m[1]=='y'else'U',s)
 # powered functions have conventional scope, e.g. sin^2 x
 s=re.sub(r'\((sin|cos|tan|cot|csc|sec|ln)\s*\)\*\*\(([^()]+)\)\s*\(?([xt])\)?',r'\1(\3)**(\2)',s)
 return parse_expr(s,local_dict={**loc,'V1':S.Symbol('V1')},transformations=standard_transformations+(implicit_multiplication_application,))
def mathparts(p):return [s[2:-2].strip()if s.startswith('$$')else s[1:-1].strip()for s in re.findall(r'\$\$.*?\$\$|\$(?!\$).*?\$',p,re.S)]
def equation(p):
 for s in mathparts(p):
  if not ('='in s and ('″'in s or '′'in s or "y'"in s or r'\frac{\text{d}y}'in s)):continue
  s=s.split(r'\qquad')[0].split(r'\,')[0].split(',')[0].strip().rstrip('.')
  a,b=s.split('=',1)
  return expr(a)-expr(b)
 raise ValueError('No equation')
def residual(eq,f,var):return S.simplify(S.trigsimp(eq.subs({D:S.diff(f,var,2),Z:S.diff(f,var),Y:f})))
if __name__=='__main__':
 for s in [r'{y}^{″}+\frac{2x}{{x}^{2}+1}{y}^{′}+Q(x)y=0',r'A{e}^{-6x}-5',r'\operatorname{sin}⁡3x',r'{\sin }^{2}⁡x']:
  try:print(s,expr(s.split('=')[0]))
  except Exception as e:print(e)
def audit():
 results=[]
 for d in sorted(H.glob('175*')):
  for q in json.loads((d/'questions.json').read_text()):
   mid=q[':question/math-academy-id'];r={'topic':d.name,'entity':q[':db/id'],'mid':mid,'checks':[]}
   p=q[':question/problem'];fs=q.get(':question/answer-fields',[])
   try:
    if d.name.endswith('49370'):
     eq=equation(p);hom='Find the complementary solution'in p
     if hom:eq=eq-eq.subs({Y:0,Z:0,D:0})
     for f in fs:
      for a in f.get(':answer-field/choices',[]):
       v=expr(a[':answer/value'].split('=')[-1]);res=residual(eq,v,x);ok=res==0
       if 'initial value problem'in p:
        ic=re.search(r'y\(0\)\s*=\s*([^$\n]+)',p)
        if ic:
         vv=ic[1].split(r'\,')[0].rstrip('.');ok=ok and S.simplify(v.subs(x,0)-expr(vv))==0
       r['checks'].append({'field':f[':db/id'],'answer':a[':db/id'],'valid':ok,'residual':str(res),'linked':a[':db/id']==f.get(':answer-field/correct',{}).get(':db/id')})
    elif d.name.endswith('50895'):
     eq=equation(p);P=S.simplify(eq.coeff(Z)/eq.coeff(D));r['P']=str(P)
     for f in fs:
      key=f[':answer-field/key']
      for a in f.get(':answer-field/choices',[]):
       if a[':answer/type'][':db/ident']!=':answer.type/math':continue
       try:
        v=expr(a[':answer/value']);
        if key=='field-1'and('Which differential equation'in p):ok=S.simplify(v+P*S.Function('W')(x))==0
        elif key=='field-1'and'Select the correct options'in p:ok=S.simplify(v+P)==0
        elif key=='field-2':ok=S.simplify(S.diff(v,x)+P*v)==0
        else:continue
        r['checks'].append({'field':f[':db/id'],'answer':a[':db/id'],'valid':ok,'linked':a[':db/id']==f.get(':answer-field/correct',{}).get(':db/id')})
       except Exception as e:r.setdefault('choice_errors',[]).append([a[':db/id'],str(e)])
    elif d.name.endswith('49102'):
     eq=equation(p);var=t if '(t)'in p else x
     yp=next(s for s in mathparts(p)if re.search(r'y\}?_?\{?1',s))
     f1=expr(yp.split('=')[1].rstrip('.'));r['given_residual']=str(residual(eq,f1,var))
     reduced=S.expand(eq.coeff(D)*(V*f1+2*S.Symbol('V1')*S.diff(f1,var)+U*S.diff(f1,var,2))+eq.coeff(Z)*(S.Symbol('V1')*f1+U*S.diff(f1,var))+eq.coeff(Y)*U*f1)
     for f in fs:
      for a in f.get(':answer-field/choices',[]):
       val=a[':answer/value'];rhs=val.split('=')[-1]if '='in val and 'u'in val else val.split('=')[-1]
       if 'equations must be satisfied'in p or 'equation must be satisfied'in p:
        aa,bb=val.split('=');v=expr(aa)-expr(bb);rat=S.simplify(reduced/v);ok=not bool(rat.free_symbols&{U,V,S.Symbol('V1')})
       else:
        v=expr(rhs);res=residual(eq,v,var);w=S.simplify(f1*S.diff(v,var)-v*S.diff(f1,var));ok=res==0 and w!=0
       r['checks'].append({'field':f[':db/id'],'answer':a[':db/id'],'valid':ok,'linked':a[':db/id']==f.get(':answer-field/correct',{}).get(':db/id')})
    else:continue
   except Exception as e:r['error']=str(e)
   results.append(r)
 (H/'mathematical-checks-before.json').write_text(json.dumps(results,indent=2,default=str))
 print(json.dumps({'records':len(results),'errors':[{k:v for k,v in r.items()if k!='checks'}for r in results if 'error'in r],'wrong':[r for r in results if any(c['linked']and not c['valid']for c in r['checks'])]},indent=2))

if __name__=='__main__':audit()
