import json,re,sys,collections
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import algebra
from algebra import matrices,scalar
from question_capture.math_format import ENV,environment,cells,MATH
S=json.loads((H/'current.json').read_text());qs={q[':db/id']:q for q in S['questions']};topic={q:t for t,k,q in S['links']};lambda_=sp.Symbol('lambda')
def simplify(v):return v.applyfunc(sp.simplify)if isinstance(v,sp.MatrixBase)else sp.simplify(v)
def expr(t,cofactor_base=None):
 t=t.replace('λ',r'\lambda').replace('−','-');local={'ell':lambda_};ms=matrices(t)
 for ii,m in reversed(list(enumerate(ms))):
  letter='Z'+chr(65+ii);a=m['matrix'];a=a.subs(algebra.symbols['l'],lambda_);val=a.det()if m['environment']=='vmatrix'else a
  left=t[:m['start']];right=t[m['end']:]
  if re.search(r'\\left\|\s*\{?\s*$',left):val=a.det()
  local[letter]=val;t=t[:m['start']]+'('+letter+')'+t[m['end']:]
 t=re.sub(r'\{C\}_\{(\d)(\d)\}|C_\{(\d)(\d)\}',lambda m:str(cofactor_base.cofactor(int(m[1]or m[3])-1,int(m[2]or m[4])-1))if cofactor_base is not None else'UNSUPPORTED',t)
 t=re.sub(r'\\color(?:\[[^]]*\])?\{[^{}]*\}','',t);t=re.sub(r'\\(?:hspace|vspace)\{[^{}]*\}','',t);t=re.sub(r'\\(?:text|textrm|mathrm)\{[\s\u00a0]*\}','',t)
 def group(pos):
  while pos<len(t)and t[pos].isspace():pos+=1
  if t[pos]!='{':return t[pos],pos+1
  d=1;e=pos+1
  while d:d+=(t[e]=='{')-(t[e]=='}');e+=1
  return t[pos+1:e-1],e
 while(m:=re.search(r'\\(?:dfrac|tfrac|frac)',t)):
  a,e=group(m.end());b,e=group(e);t=t[:m.start()]+'('+a+')/('+b+')'+t[e:]
 t=re.sub(r'\\(?:displaystyle|textstyle|left|right|quad|qquad|mathbf|mathit|mathrm|textrm)\b','',t);t=re.sub(r'\\[,;! ]','',t);t=t.replace(r'\cdot','*').replace(r'\times','*').replace(r'\lambda','ell').replace(r'\sqrt','sqrt').replace('^','**').replace('{','(').replace('}',')');t=re.sub(r'\bdet\b','det',t);t=t.strip().rstrip('.,:;');t=t.replace('[','(').replace(']',')').replace('|','');t=re.sub(r'\s+','',t)
 assert re.fullmatch(r'[\dA-Za-z+*/().-]+',t),t
 value=simplify(parse_expr(t,local_dict=local,transformations=standard_transformations+(implicit_multiplication_application,)))
 assert value.free_symbols<={lambda_,sp.Symbol('k')},str(value)
 return value
def chain_checks(q):
 sol=q.get(':question/worked-solution','');results=[];bad=[];unparsed=[]
 for block in MATH.finditer(sol):
  tex=block[0];offset=2 if tex.startswith('$$')else 1;tex=tex[offset:-offset]
  if r'\sim'in tex or '∼'in tex:continue
  aligned=re.search(r'\\begin\{aligned\}',tex)
  if aligned:
   span=environment(tex,aligned.start());rows=[''.join(r)for r in cells(tex[span[0]:span[1]])];base=None;expect=None
   for row in rows:
    if ':='in row or '='not in row:continue
    parts=row.split('=')
    if parts[0].strip():
     mm=matrices(parts[0]);base=mm[0]['matrix']if mm else None
     try:expect=expr(parts[0],base)
     except Exception:expect=None
    for part in parts[1:]:
     try:
      v=expr(part,base)
      if v==0 and expect is not None and expect.free_symbols:continue
      if expect is not None:
       ok=simplify(v-expect)==(sp.zeros(*expect.shape)if isinstance(expect,sp.MatrixBase)else 0);r={'question':q[':db/id'],'row':row,'expected':str(expect),'actual':str(v),'ok':ok};results.append(r)
       if not ok:bad.append(r)
      else:expect=v
     except Exception as e:unparsed.append({'row':row,'part':part,'error':str(e)})
  elif '='in tex:
   parts=tex.split('=');expect=None
   for part in parts:
    try:
     v=expr(part)
     if v==0 and expect is not None and expect.free_symbols:continue
     if expect is not None:
      ok=simplify(v-expect)==(sp.zeros(*expect.shape)if isinstance(expect,sp.MatrixBase)else 0);r={'question':q[':db/id'],'row':tex,'expected':str(expect),'actual':str(v),'ok':ok};results.append(r)
      if not ok:bad.append(r)
     else:expect=v
    except Exception:expect=None
 return results,bad,unparsed
if __name__=='__main__':
 checks=[];bad=[];unparsed=[]
 for q in S['questions']:
  a,b,c=chain_checks(q);checks+=a;bad+=b;unparsed.extend({'question':q[':db/id'],**r}for r in c)
 (H/'equality-audit.json').write_text(json.dumps({'checks':checks,'failures':bad,'unparsed':unparsed},indent=2)+'\n');print('Checks',len(checks),'failures',len(bad),'unparsed',len(unparsed));print('\n'.join(str(r)for r in bad))
