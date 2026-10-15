"""Root principal inverse-function grammar and independently read substitutions."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('root_inverse_elem',Path(__file__).with_name('elementary-integral-readback.py'));P=importlib.util.module_from_spec(z);z.loader.exec_module(P)
x,u,C=P.x,P.u,P.C

def group(t,i):
 while i<len(t)and t[i].isspace():i+=1
 assert t[i]in'({';opening=t[i];closing=')'if opening=='('else'}';depth=1;j=i+1
 while depth:
  assert j<len(t);depth+=(t[j]==opening)-(t[j]==closing);j+=1
 return t[i+1:j-1],j

def scalar(raw):
 t=raw.strip().rstrip('.,?').replace('⁡','').replace('\xa0',' ').replace(r'\left','').replace(r'\right','').replace(r'\dfrac',r'\frac').replace(r'\text{ }','')
 t=re.sub(r'\\(?:text|operatorname)\{(arcsec|arcsin|arctan)\s*\}',lambda m:'\\'+m[1]+' ',t)
 t=re.sub(r'(?<![A-Za-z\\])(arcsec|arcsin|arctan)',lambda m:'\\'+m[1]+' ',t)
 # Principal arcsec(z)=acos(1/z); retain the literal function-square layout.
 while(m:=re.search(r'\\arcsec\s*',t)):
  i=m.end();power=None
  if t[i]=='^':
   i+=1
   if t[i]=='{':power,i=group(t,i)
   else:power=t[i];i+=1
  while i<len(t)and t[i].isspace():i+=1
  if t[i]in'({':arg,end=group(t,i)
  else:
   mm=re.match(r'(?:\d+)?[xu]',t[i:]);assert mm,('unsupported bare arcsec arg',t);arg=mm[0];end=i+mm.end()
  replacement=r'\arccos(\frac{1}{('+arg+')})'+('^{'+power+'}'if power else'');t=t[:m.start()]+replacement+t[end:]
 return P.scalar(t)

def eq(a,b):
 d=s.expand(a-b)
 if d==0:return True
 return s.simplify(d)==0

def signature(value):
 atoms=value.atoms(s.asin,s.atan,s.acos);assert len(atoms)==1,value;atom=next(iter(atoms));rest=s.expand(value-C);assert value.coeff(C)==1;power=2 if rest.has(atom**2)else 1;amplitude=s.cancel(rest/atom**power);assert not amplitude.has(x,u)
 if atom.func==s.acos:
  direct=s.cancel(atom.args[0]/x)
  if not direct.has(x,u):
   k=direct;kind='arcsin'if power==1 else'arccos_square'
   if power==1:amplitude=-amplitude
  else:k=s.cancel(1/atom.args[0]/x);kind='arcsec'
 else:k=s.cancel(atom.args[0]/x);kind='arcsin'if atom.func==s.asin else'arctan'
 if k.has(x,u):return('nonlinear_'+kind,power,s.simplify(amplitude),atom.args[0])
 assert k.is_positive is True,('inverse signature',value,atom,k);return(kind,power,s.simplify(amplitude),s.simplify(k))

def measure_text(text):
 # Move a numerator differential outside its exact balanced fraction, including
 # nested radical denominators; ordinary du/dx derivative operators stay intact.
 cursor=0
 while(m:=re.search(r'\\frac\{',text[cursor:])):
  start=cursor+m.start();num,end=group(text,cursor+m.end()-1);den,end=group(text,end);match=re.search(P.DIFF,num)
  if match and not num[match.end():].strip()and not re.fullmatch(P.DIFF,den):
   prefix=num[:match.start()].replace(r'\,','').strip();replacement=r'\frac{'+(prefix or'1')+'}{'+den+'}'+match[0];text=text[:start]+replacement+text[end:];cursor=start+len(replacement)
  else:cursor=end
 return P.fraction_measure(text)

def side(raw,var=x,inner=None):
 text=measure_text(raw.replace('&','').strip().rstrip('.,'));formal=[]
 while r'\int'in text:
  at=text.index(r'\int');body,iv,match=P.integrand(text[at:]);symbol=P.P.locals_[('i','j','k')[len(formal)]];formal.append((symbol,body,iv));text=text[:at]+'('+str(symbol)+')'+text[at+match.end():]
 value=scalar(text);rest=value;actual=s.Integer(0);ops=[]
 for symbol,body,iv in formal:
  coeff=s.expand(value).coeff(symbol);assert not coeff.has(var,u,*[t for t,_,_ in formal]);rest-=coeff*symbol
  if iv==var:effective=body
  else:assert iv==u and inner is not None;effective=body.subs(u,inner)*s.diff(inner,var)
  actual+=coeff*effective;ops.append((body,iv,coeff))
 rest=s.expand(rest);assert not rest.has(*[t for t,_,_ in formal]);rest=rest.subs(u,inner)if inner is not None else rest;return actual+s.diff(rest,var),ops

def check(q):
 F,var=P.prompt(measure_text(q[':question/problem']));assert var==x;sol=q[':question/worked-solution'];sub=re.search(r'\$u=(.*?)\$',sol);assert sub;U=scalar(sub[1]);k=s.diff(U,x);assert k.is_positive is True and not k.has(x)and eq(U,k*x)
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);N=dict(differentials=0,formal_inputs=0,primitive_stages=0,basic_formulas=0,values=0,pairs=0)
 for block in blocks:
  block=measure_text(block)
  if r'\frac{\text{d}u}{\text{d}x}'in block:
   a,b=re.split(r'⟹|⇒|\\(?:Longrightarrow|Rightarrow|implies)',block);assert eq(scalar(a.split('=',1)[1].replace(r'\,','').replace(r'\quad','')),k)
   def differential(raw):
    raw=raw.strip().rstrip('.,').replace(r'\quad','').replace(r'\,','');mm=re.fullmatch(r'(.*?)'+P.DIFF,raw);assert mm,('actual inverse differential',raw);coef=scalar(mm[1])if mm[1].strip()else s.Integer(1);return coef*(k if mm[2]=='u'else 1)
   left,right=b.split('=',1);assert eq(differential(left),differential(right));N['differentials']+=2;continue
  if r'\int'not in block:continue
  basic=r'\begin{aligned}'not in block and P.integrand(block)[1]==u
  text=re.sub(r'\\(?:begin|end)\{aligned\}','',block)
  for row in text.split(r'\\'):
   for part in row.replace('&','').split('='):
    if not part.strip():continue
    if basic:
     value,ops=side(part,u);target=1/(1+u*u)if'arctan'in block else 1/s.sqrt(1-u*u)
    else:value,ops=side(part,x,U);target=F
    assert eq(value,target),('actual inverse integral/primitive stage',part,value,target)
    N['formal_inputs']+=len(ops);N['primitive_stages']+=not bool(ops);N['basic_formulas']+=bool(basic)
 f=q[':question/answer-fields'][0];values=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];signatures=[signature(v)for v in values];assert len(values)==5 and len(set(signatures))==5
 # Source tasks have a real primitive at x=0; arcsec alternatives fail that
 # domain contract. asin/atan derivatives are compared as complete functions.
 flags=[sig[0]!='arcsec'and sig[1]==1 and eq(s.diff(v,x),F)for v,sig in zip(values,signatures)];assert[a[':answer/id']for a,ok in zip(f[':answer-field/choices'],flags)if ok]==[f[':answer-field/correct'][1]];N['values']+=5;N['pairs']+=10
 assert N['differentials']==2 and N['formal_inputs']>=3 and N['primitive_stages']>=2
 return F,N,signatures
