"""Frozen independent displayed-TeX parser. No generator import or symbolic helpers."""
import re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
X=sp.Symbol('x',real=True);Y=sp.Symbol('y',real=True)
def convert(text):
 text=text.replace('\\\\','\\').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\!','')
 def group(st,i):
  assert st[i]=='{',(st,i);depth=1;j=i+1
  while depth:
   if st[j]=='{':depth+=1
   if st[j]=='}':depth-=1
   j+=1
  return st[i+1:j-1],j
 def cv(st):
  out='';i=0
  while i<len(st):
   if st.startswith(r'\frac',i) or st.startswith(r'\dfrac',i):
    i+=len(r'\dfrac') if st.startswith(r'\dfrac',i) else len(r'\frac');a,i=group(st,i);b,i=group(st,i);out+='(('+cv(a)+')/('+cv(b)+'))'
   elif st.startswith(r'\sqrt',i):
    i+=5;n='2'
    if st[i]=='[':j=st.index(']',i);n=st[i+1:j];i=j+1
    a,i=group(st,i);out+='(('+cv(a)+')**(1/('+n+')))'
   elif st[i]=='{':a,i=group(st,i);out+='('+cv(a)+')'
   elif st[i]=='^':out+='**';i+=1
   else:out+=st[i];i+=1
  return out
 return cv(text)
def formal(text):
 text=text.strip().rstrip('.,').replace('&','')
 text=re.sub(r'\\(?:d?frac)\{\\(?:text|mathrm)\{d\}\}\{\\(?:text|mathrm)\{d\}x\}','D',text)
 text=re.sub(r"\{?f\}?\s*\^\{[′']\}",'Fp',text)
 text=re.sub(r"f'",'Fp',text)
 text=re.sub(r"\{?m\}?\s*\^\{[′']\}",'N',text)
 text=text.replace("m'",'N');text=re.sub(r'\bm\b','M',text)
 return text

def expression(text,f=None,m=None,n=None):
 text=formal(text);d=sp.diff(f,X) if f is not None else None
 env={'x':X,'y':Y,'M':sp.Symbol('M') if m is None else m,'N':sp.Symbol('N') if n is None else n,'D':lambda e:sp.diff(e,X),'Fp':lambda a:d.subs(X,a)}
 return parse_expr(convert(text),local_dict=env,transformations=standard_transformations+(implicit_multiplication_application,))
def equality(a,b,domain='real x'):
 delta=a-b
 if domain=='x>0':delta=delta.subs(X,sp.Symbol('positive',positive=True))
 assert sp.simplify(delta)==0,(a,b,domain,sp.simplify(delta))
def actual(q):
 pr=q[':question/problem'];mt=re.search(r'\$(?:f\(x\)|y)\s*=\s*(.*?)\$',pr);assert mt,'No actual function'
 f=expression(mt[1]);pt=re.search(r'at the point \$\((.*?)\)',pr);assert pt
 px,yp=map(expression,pt[1].split(','));equality(f.subs(X,px),yp)
 if any(power.exp.is_Rational and power.exp.q!=1 and power.has(X) for power in f.atoms(sp.Pow)):assert px>0;domain='x>0'
 elif sp.denom(sp.cancel(f)).has(X):assert px!=0;domain='x!=0'
 else:domain='real x'
 if domain=='x>0':
  positive=sp.Symbol('positive',positive=True);f=sp.simplify(f.subs(X,positive)).subs(positive,X)
 m=sp.simplify(sp.diff(f,X).subs(X,px));assert m!=0 and m.is_finite
 n=-1/m;b=sp.simplify(yp-n*px);axis=re.search(r'intersects the \$([xy])\$-axis',pr)[1];a=sp.simplify(-b/n) if axis=='x' else b
 return f,px,yp,m,n,b,a,axis,domain

def validate(q,allow_missing=False):
 f,p,yp,m,n,b,a,axis,domain=actual(q);solution=q[':question/worked-solution'];bs=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S);assert len(bs)==5,'five source stages'
 # Explicit formal binding and operands, not just a final derivative value.
 first=[v.strip() for v in formal(bs[0].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')[0]).split('=')]
 assert first[0].strip()=='Fp(x)','derivative formal input must be x'
 assert first[1].lstrip().startswith('D('),'first derivative operator operand'
 firstoperand=first[1].strip()[2:-1];equality(expression(firstoperand),f,domain)
 slope=[v.strip() for v in formal(bs[1]).split('=')];assert slope[0]=='M';assert slope[1]=='Fp('+str(p)+')','actual slope evaluation input'
 reciprocal=[v.strip() for v in formal(bs[2]).split('=')];assert reciprocal[0]=='N';assert reciprocal[1].strip()==r'-\frac{1}{M}','negative reciprocal operand'
 for block_index,block in enumerate(bs):
  body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  rows=body.split(r'\\')
  # Aligned continuation rows inherit derivative/value left-hand side.
  carry=None
  for row in rows:
   pieces=[v.strip().rstrip('.,') for v in row.replace('&','').split('=')]
   if not pieces[0]:assert carry is not None;pieces[0]=carry
   else:carry=pieces[0]
   assert len(pieces)>=2,(block_index,row)
   if block_index<=2:
    if block_index==0:
     for piece in pieces[1:]:
      operand_text=formal(piece);start=0
      while 'D(' in operand_text[start:]:
       k=operand_text.index('D(',start);depth=1;j=k+2
       while depth:
        if operand_text[j]=='(':depth+=1
        elif operand_text[j]==')':depth-=1
        j+=1
       operand=expression(operand_text[k+2:j-1]);prefix=re.sub(r'(?:\\cdot|\*)\s*$','',operand_text[:k].strip()).strip()
       factor=expression(prefix) if prefix else sp.Integer(1)
       equality(factor*operand,f,domain);start=j
    values=[expression(v,f,m,n) for v in pieces]
    for val in values[1:]:equality(values[0],val,domain)
   elif block_index==3:
    if row==rows[0]:
     equality(expression(pieces[0],f,m,n),Y-yp,domain)
     equality(expression(pieces[1],f,m,n),n*(X-p),domain)
    # Every full equation must be precisely the normal line, with y coefficient1.
    vals=[expression(v,f,m,n) for v in pieces]
    for val in vals[1:]:
     residual=vals[0]-val;assert sp.diff(residual,Y)==1,'normal equation dependent variable'
     equality(residual.subs(Y,n*X+b),0,domain)
   else:
    vals=[expression(v,f,m,n) for v in pieces]
    if row==rows[0]:
     if axis=='x':equality(vals[0],n*X+b,domain);equality(vals[1],sp.Integer(0),domain)
     else:assert not vals[1].has(X);equality(vals[0],Y,domain);equality(vals[1],b,domain)
    sub={X:a,Y:0} if axis=='x' else {X:0,Y:a}
    for val in vals[1:]:equality(vals[0].subs(sub),val.subs(sub),domain)
 # Explicit axis operation and target variables are part of the rendered contract.
 assert 'setting $'+('y' if axis=='x' else 'x')+'=0$' in solution
 conclusion=re.search(r'Therefore,.*?\$\((.*?)\)\.?\$',solution,re.S);assert conclusion
 point=tuple(map(expression,conclusion[1].replace(r'\,','').split(',')));target=(a,sp.Integer(0)) if axis=='x' else (sp.Integer(0),a)
 for got,want in zip(point,target):equality(got,want,domain)
 fieldreports=[]
 for field in q.get(':question/answer-fields',[]):
  kind=field[':answer-field/type'];kind=kind if isinstance(kind,str) else kind[':db/ident'];cs=field.get(':answer-field/choices',[])
  if not cs:
   assert allow_missing;fieldreports.append({'missing':True});continue
  good=[];values=[]
  for c in cs:
   if kind.endswith('radio'):
    z=tuple(map(expression,c[':answer/value'].strip('()').split(',')));assert len(z)==2
    valid=sp.simplify(z[1]-n*z[0]-b)==0 and z[1 if axis=='x' else 0]==0
   else:
    assert kind.endswith('blank');assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
    z=expression(c[':answer/value']);index=int(field[':answer-field/key'].split('-')[-1])-1;valid=sp.simplify(z-target[index])==0
   values.append(z);good.append(bool(valid))
  assert len(set(values))==len(values),'equivalent complete bank values'
  assert sum(good)==1,'complete bank must have exactly one correct answer'
  ref=field.get(':answer-field/correct');assert ref is not None or allow_missing
  if ref:
   cid=ref[':answer/id'] if isinstance(ref,dict) else ref[1];assert cid==cs[good.index(True)][':answer/id']
  fieldreports.append({'key':field[':answer-field/key'],'options':len(cs),'correct_unique':True})
 return {'function':sp.srepr(f),'point':[str(p),str(yp)],'axis':axis,'domain':domain,'normal_slope':str(n),'intercept':str(a),'fields':fieldreports,'operative_blocks':5}
