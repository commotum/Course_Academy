"""Read every original numeric integration-stage expression, fail on unknown syntax."""
import re
from math_parser import scalar
import sympy as s

def group(text,start=0):
 assert text[start]=='{',text
 depth=0
 for i in range(start,len(text)):
  if text[i]=='{':depth+=1
  if text[i]=='}':
   depth-=1
   if depth==0:return text[start+1:i],text[i+1:]
 raise ValueError(text)
def clean(text):
 return text.replace(r'\,','').replace(r'\text{d}','').replace('dy','y').replace('dx','x').replace(r'\operatorname{ln}','\\ln').strip().rstrip('.')
def take_integral(raw):
 prefix=r'{\int }_';pos=raw.index(prefix);coeff=raw[:pos];lo,rest=group(raw[pos+len(prefix):]);assert rest[0]=='^';hi,rest=group(rest[1:]);return scalar(coeff) if coeff else s.Integer(1),scalar(lo),scalar(hi),rest

def bracket(raw,var):
 # MA groups the whole bracket in an extra pair of braces; strip that wrapper.
 pos=raw.index('[');end=raw.index(']',pos);expr=scalar(raw[pos+1:end]);prefix=raw[:pos].rstrip('{');suffix=raw[end+1:]
 if suffix.startswith('}'):suffix=suffix[1:]
 assert suffix.startswith('_'),raw
 lo,tail=group(suffix[1:]);assert tail.startswith('^');hi,tail=group(tail[1:]);lo=scalar(lo.replace(var+'=',''));hi=scalar(hi.replace(var+'=',''))
 coeff=scalar(prefix) if prefix else s.Integer(1)
 return coeff*expr,lo,hi,tail

def audit(g,src):
 k=src[':question/math-academy-id'];x,y=g.x,g.y;m=g.model(k,dict(p=1,q=1,r=1),'observed_'+k)
 prompt=src[':question/problem'];rawF=re.search('⟨(.*?)⟩',prompt,re.S).group(1);actualF=[scalar(v) for v in rawF.replace(r'\,','').split(',')];assert all(g.eq(v,w) for v,w in zip(actualF,m['F']))
 actualg=scalar(re.search(r'\$z=(.*?)\$',prompt).group(1));assert g.eq(actualg,m['g'])
 domain=re.search(r'for \$(.*?)\\le\s*x\\le\s*(.*?)\$ and \$(.*?)\\le\s*y\\le\s*(.*?)\.\$',prompt);assert domain
 assert all(g.eq(scalar(v),w) for v,w in zip(domain.groups(),m['b']))
 bs=re.findall(r'\$\$\n(.*?)\n\$\$',src[':question/worked-solution'],re.S);rows=bs[-1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
 checked=[]
 def same(a,b):assert s.simplify(a-b)==0,(k,stage,a,b)
 for stage,row in zip(g.STAGES[k],rows):
  rhs=clean(row.split(' & =',1)[1])
  if stage=='formula':continue
  if stage in ['dot','distributed','simplified']:
   prefix='{∬}_{D}(';assert rhs.startswith(prefix);expr=rhs[len(prefix):];expr=expr[:expr.rindex(')')];val=scalar(expr)
   if k=='q-161541':xp,yp=s.symbols('xp yp',positive=True);val=s.simplify(val.subs({x:xp,y:yp})).subs({xp:x,yp:y})
   same(val,m['h'])
  elif stage=='iterated':
   c,lo,hi,rest=take_integral(rhs);same(c,1);same(lo,m['b'][0]);same(hi,m['b'][1]);c,lo,hi,expr=take_integral(rest);same(c,1);same(lo,m['b'][2]);same(hi,m['b'][3]);assert expr.endswith('yx');expr=expr[:-2];assert expr.startswith('(') and expr.endswith(')');same(scalar(expr[1:-1]),m['h'])
  elif stage=='primitive_y':
   c,lo,hi,rest=take_integral(rhs);same(lo,m['b'][0]);same(hi,m['b'][1]);expr,a,b,tail=bracket(rest,'y');assert tail=='x';same(a,m['b'][2]);same(b,m['b'][3]);same(s.diff(c*expr,y),m['h'])
  elif stage in ['evaluated_y','simplified_y']:
   c,lo,hi,expr=take_integral(rhs);same(lo,m['b'][0]);same(hi,m['b'][1]);assert expr.endswith('x');expr=expr[:-1];same(c*scalar(expr),m['iy'])
  elif stage=='primitive_x':
   expr,lo,hi,tail=bracket(rhs,'x');assert not tail;same(lo,m['b'][0]);same(hi,m['b'][1]);same(s.diff(expr,x),m['iy'])
  elif stage in ['evaluated_x','answer']:same(scalar(rhs),m['answer'])
  checked.append(stage)
 return {'source_id':k,'numeric_stages_checked':checked,'total':len(checked)}
