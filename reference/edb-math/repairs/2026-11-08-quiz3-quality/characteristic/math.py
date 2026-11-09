import re,json,sys
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
T=standard_transformations+(implicit_multiplication_application,convert_xor)
x,t=S.symbols('x t',positive=True);Y,Yp,Ypp,L,A,B,P,Q,C,D=S.symbols('y u v L A B P Q C D')
locals={str(z):z for z in [x,t,Y,Yp,Ypp,L,A,B,P,Q,C,D]};locals.update(e=S.E,i=S.I,pi=S.pi,sin=S.sin,cos=S.cos,ln=S.log,sqrt=S.sqrt)
def tex(s):
 s=s.strip().strip('.,').replace('\\\\','\\').replace('\\u2061','').replace('\u2061','').replace('λ',r'\lambda').replace('−','-')
 s=re.sub(r'\\(?:operatorname|textrm|mathrm|text)\s*\{(cos|sin|ln|i|d)\}',r'\1',s)
 s=re.sub(r'\\(?:displaystyle|left|right|quad|qquad|,|;|!|\s)', '',s)
 s=re.sub(r'\{y\}\^\{[″]\}|y\^\{″\}|y\s*\x27\x27', 'Ypp',s)
 s=re.sub(r'\{y\}\^\{[′]\}|y\^\{′\}|y\s*\x27', 'Yp',s)
 s=re.sub(r'\{c\}_\{1\}|c_\{1\}|c_1','C',s);s=re.sub(r'\{c\}_\{2\}|c_\{2\}|c_2','D',s)
 s=s.replace(r'\lambda','L').replace(r'\pi','pi').replace(r'\cdot','*').replace(r'\cos','cos').replace(r'\sin','sin').replace(r'\ln','ln')
 s=s.replace('{e}','e')
 s=s.replace('Ypp','v').replace('Yp','u').replace('Y','y')
 def arg(pos):
  while pos<len(s)and s[pos].isspace():pos+=1
  if s[pos]=='{':
   level=1;j=pos+1
   while level:level+= (s[j]=='{')-(s[j]=='}');j+=1
   return s[pos+1:j-1],j
  if s[pos]=='\\':
   m=re.match(r'\\[A-Za-z]+',s[pos:]);return m[0],pos+len(m[0])
  return s[pos],pos+1
 while True:
  m=re.search(r'\\(?:dfrac|frac|sqrt)\s*',s)
  if not m:break
  a,end=arg(m.end())
  if m[0].startswith(r'\sqrt'):replacement='sqrt('+a+')'
  else:b,end=arg(end);replacement='(('+a+')/('+b+'))'
  s=s[:m.start()]+replacement+s[end:]
 s=s.replace('{','(').replace('}',')').replace('sqrt(', ' sqrt(')
 # Bind source TeX function arguments before implicit multiplication.
 pos=0
 while True:
  m=re.search(r'(cos|sin|ln)',s[pos:])
  if not m:break
  st=pos+m.start();en=pos+m.end();j=en
  while j<len(s)and s[j].isspace():j+=1
  if j<len(s)and s[j]=='(':
   s=s[:st]+' '+s[st:];pos=en+1;continue
  k=j;depth=0
  while k<len(s):
   ch=s[k]
   if depth==0 and (ch in '+-=,\n)' or s[k:k+3]in ['cos','sin']):break
   if ch=='(':depth+=1
   if ch==')':depth-=1
   k+=1
  s=s[:st]+' '+s[st:en]+'('+s[j:k].strip()+')'+s[k:];pos=k+3
 s=s.strip().strip('.,')
 if '\\'in s or '='in s:raise ValueError(s)
 return parse_expr(s,local_dict=locals,transformations=T)
def deriv_text(s):
 # All source encodings of Leibniz derivatives.
 s=re.sub(r'\\(?:dfrac|frac)\{(?:\\(?:textrm|text|mathrm)\{d\}|d|\{\\(?:text|textrm|mathrm)\{d\}\})\^\{?2\}?\s*y\}\{(?:\\(?:textrm|text|mathrm)\{d\}|d)\s*\{?([xt])\}?\^\{?2\}?\}', 'Ypp',s)
 s=re.sub(r'\\(?:dfrac|frac)\{(?:\\(?:textrm|text|mathrm)\{d\}|d)\s*y\}\{(?:\\(?:textrm|text|mathrm)\{d\}|d)\s*[xt]\}', 'Yp',s)
 return s
base=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic')
def extract_ode(q):
 problem=deriv_text(q[':question/problem']);frags=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',problem,re.S)
 for pair in frags:
  st=next(v for v in pair if v)
  if ('Ypp'in st or '″'in st or "y''"in st)and '='in st:
   st=st.split('=')[0].strip();return tex(st)
 raise ValueError('NO ODE')
if __name__=='__main__':
 for d in base.glob('175*'):
  rows=[]
  for q in json.loads((d/'questions.json').read_text()):
   row={'eid':q[':db/id'],'mid':q[':question/math-academy-id']}
   try:row['ode']=str(extract_ode(q))
   except Exception as e:row['error']=str(e)
   rows.append(row)
  (d/'math-parse.json').write_text(json.dumps(rows,indent=2))
  print(d.name,[(r['mid'],r['error'])for r in rows if 'error'in r])
