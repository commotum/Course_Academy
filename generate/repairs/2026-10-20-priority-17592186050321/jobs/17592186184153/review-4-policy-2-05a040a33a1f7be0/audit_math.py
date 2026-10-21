import re
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
V={v:S.Symbol(v,positive=True) for v in ('x','y','t')};V['C']=S.Symbol('C')
TRANS=standard_transformations+(implicit_multiplication_application,)
def tex(src):
 text=src.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\!','').strip().rstrip('.')
 pos=0
 def group():
  nonlocal pos
  while pos<len(text) and text[pos].isspace():pos+=1
  if text[pos]=='{':pos+=1;return walk('}')
  c=text[pos];pos+=1;return c
 def walk(stop=None):
  nonlocal pos
  out=''
  while pos<len(text):
   if stop and text[pos]==stop:pos+=1;return out
   if text.startswith(r'\frac',pos) or text.startswith(r'\dfrac',pos):
    pos+=5 if text.startswith(r'\frac',pos) else 6
    a=group();b=group();out+=f'(({a})/({b}))'
   elif text.startswith(r'\sqrt',pos):
    pos+=5;d='2'
    if text[pos]=='[':end=text.index(']',pos);d=text[pos+1:end];pos=end+1
    a=group();out+=f'(({a})**(1/({d})))'
   elif text[pos]=='{':out+='('+group()+')'
   elif text[pos]=='^':pos+=1;out+='**'+('('+group()+')')
   else:out+=text[pos];pos+=1
  assert stop is None,(text,stop)
  return out
 return parse_expr(walk(),local_dict=V,transformations=TRANS)
def equal(a,b):return S.expand(S.powdenest(a-b,force=True))==0 or S.simplify(a-b)==0
def field(r):return r['question'][':question/answer-fields'][0]
def answer(r):
 f=field(r);return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def extract(r):
 p=r['question'][':question/problem']
 if "Given $y'(t)=" in p:return tex(re.search(r"Given \$y'\(t\)=(.*?)\$",p)[1]),'t'
 if 'Find the integral of $' in p:
  raw=re.search(r'of \$(.*?)\$',p)[1];return tex(raw),re.search(r'for \$([xyt])>0',p)[1]
 raw=re.search(r'\\left\((.*?)\\right\)',p)[1];v=re.search(r'\\mathrm\{d\}([xyt])',p)[1];return tex(raw),v

def verify(r):
 integrand,v=extract(r);x=V[v];f=field(r);values=[tex(a[':answer/value']) for a in f[':answer-field/choices']]
 qualifies=[equal(S.diff(a,x),integrand) for a in values]
 assert sum(qualifies)==1
 assert qualifies[next(j for j,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==answer(r)[':answer/id'])]
 assert len(set(map(str,values)))==len(values)
 sol=r['question'][':question/worked-solution'];rows=sol.split('&=')
 final=tex(rows[-1].split(r'\end')[0]);rule=tex(rows[-2].split(r'\\')[0])
 assert equal(S.diff(final,x),integrand) and equal(rule,final)
 assert equal(final,tex(answer(r)[':answer/value'])+(V['C'] if f[':answer-field/type'].endswith('/blank') else 0))
 if f[':answer-field/type'].endswith('/blank'):assert '+\\,C' in r['question'][':question/problem'] and not values[0].has(V['C'])
 else:assert len(values)==5 and all(a.has(V['C']) for a in values)
 return {'id':r['question'][':question/id'],'integrand':str(integrand),'correct':answer(r)[':answer/value'],'variable':v,'passes':True}
