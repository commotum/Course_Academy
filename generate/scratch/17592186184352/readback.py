"""Independently parse displayed givens, formal substitution, and every row.

No generator parameter or answer helper is used. The scalar grammar is frozen
from the parent reader. Integral evaluation uses independently recovered factors.
"""
import importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
sp=importlib.util.spec_from_file_location('definite_independent_scalar',Path(__file__).parent/'reference/scalar.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
x,u=p.x,p.u
def equal(a,b):return s.simplify(s.expand_log(a-b,force=True))==0
def clean(t):
 t=t.strip().rstrip('.,').replace(r'\displaystyle','').replace(r'\left','').replace(r'\right','').replace(r'\big','').replace(r'\,','').replace('⁡','')
 t=t.replace(r'{\int }',r'\int').replace(r'\text{d}',r'\mathrm{d}').replace(r'\textrm{d}',r'\mathrm{d}').replace(r'{|}',r'|').replace(r'\operatorname{ln}',r'\ln').replace(r'\dfrac',r'\frac')
 t=t.replace('{e}','e')
 t=re.sub(r'(?<![A-Za-z])d([xu])\s*$',lambda m:r'\mathrm{d}'+m[1],t)
 if t.endswith('dx') and r'\mathrm{d}x' not in t:t=t[:-2]+r'\mathrm{d}x'
 t=re.sub(r'\\ln\s*\|([^|]+)\|',r'ln(Abs(\1))',t)
 return t
def scalar(t):return p.scalar(clean(t))
def group(t,start):
 if t[start]!='{':return t[start],start+1
 depth=1;i=start+1
 while depth:
  depth+=(t[i]=='{')-(t[i]=='}');i+=1
 return t[start+1:i-1],i
@lru_cache(None)
def primitive(body,var):
 # Source scope: proportional derivative times exponential, or derivative/u.
 for f in body.atoms(s.exp):
  ratio=s.cancel(body/(f*s.diff(f.args[0],var)))
  if not ratio.has(var):return ratio*f
 for f in body.atoms(s.Pow):
  if not f.base.has(var) and f.exp.has(var):
   ratio=s.cancel(body/(f*s.diff(f.exp,var)))
   if not ratio.has(var):return ratio*f/s.log(f.base)
 numerator,denominator=s.fraction(s.cancel(body))
 if denominator.has(var):
  ratio=s.simplify(numerator/s.diff(denominator,var))
  if not ratio.has(var):return ratio*s.log(denominator)
 return s.integrate(body,var)
def integral_parts(t):
 t=clean(t);i=t.index(r'\int');pos=i+4
 while pos<len(t) and t[pos].isspace():pos+=1
 assert t[pos]=='_',t;lo,pos=group(t,pos+1);assert t[pos]=='^',t;hi,pos=group(t,pos+1)
 m=re.search(r'\\mathrm\{d\}([xu])',t[pos:]);assert m,t
 end=pos+m.end();body=t[pos:pos+m.start()].strip().rstrip('*').removesuffix(r'\cdot').strip()
 var=x if m[1]=='x' else u
 prefix=t[:i].strip();coeff=scalar(prefix) if prefix else s.Integer(1)
 F=scalar(body);low=scalar(lo);high=scalar(hi)
 return coeff,F,var,low,high,t[end:]
def expression(t):
 t=clean(t)
 if r'\int' in t:
  coeff,F,var,low,high,after=integral_parts(t);assert not after,t
  prim=primitive(F,var);return coeff*(prim.subs(var,high)-prim.subs(var,low))
 if '|' in t:
  before,after=t.split('|',1);before=before.strip()
  # Captured MathML sometimes has an enclosing brace around the bar prefix.
  if before.startswith('{') and before.count('{')>before.count('}'):before=before[1:]
  if before.endswith('}') and before.count('}')>before.count('{'):before=before[:-1]
  after=after.removeprefix('}')
  assert after.startswith('_'),t;lo,pos=group(after,1);assert after[pos]=='^';hi,pos=group(after,pos+1);assert not after[pos:]
  prim=scalar(before);return prim.subs(u,scalar(hi))-prim.subs(u,scalar(lo))
 return scalar(t)
def blocks(t):return [m[1] if m[1] is not None else m[2] for m in re.finditer(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$(?!\$)',t,re.S)]
def rows(solution):
 block=next(z for z in blocks(solution) if r'\begin{aligned}' in z)
 block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip()
 return [t.replace('&','').strip() for t in block.split(r'\\')]
def signatures(solution):
 result=[]
 for row in rows(solution):
  rhs=row.split('=',1)[1]
  if r'\int' in rhs:result.append('integral_'+('u' if re.search(r'\\(?:text|mathrm)\{d\}u',rhs) else 'x'))
  elif '|' in rhs:result.append('primitive_at_bounds')
  elif re.search(r'e\}?\^',rhs):result.append('exponential_endpoint_difference')
  elif '-' in rhs:result.append('endpoint_difference')
  elif '(' in rhs and '\\ln' not in rhs and '\\operatorname{ln}' not in rhs:result.append('endpoint_product')
  else:result.append('arithmetic_or_log_reduction')
 return result
def check(question,expected_signature=None):
 prompt=question[':question/problem'];solution=question[':question/worked-solution']
 for text in [prompt,solution,*[a[':answer/value'] for f in question[':question/answer-fields'] for a in f[':answer-field/choices']]]:assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
 given=next(z for z in blocks(prompt) if r'\int' in z).strip().rstrip('= .')
 coeff,F,var,low,high,after=integral_parts(given);assert var==x and not after
 correct_value=expression(given)
 substitution=scalar(re.search(r'\$u=(.*?)\.\$',solution)[1]);assert not substitution.has(u)
 form=next(z for z in blocks(solution) if r'\frac{\mathrm{d}u}' in z or r'\frac{\text{d}u}' in z)
 left,right=re.split(r'\\quad\\Longrightarrow\\quad|⟹',form,maxsplit=1)
 derivative=scalar(left.split('=',1)[1]);assert equal(derivative,s.diff(substitution,x))
 lhs,rhs=right.strip().rstrip('.').split('=',1)
 left_factor=scalar(re.sub(r'\\(?:text|mathrm)\{d\}u','',lhs)) if re.sub(r'\\(?:text|mathrm)\{d\}u','',lhs).strip() else s.Integer(1)
 right_factor=scalar(re.sub(r'\\(?:text|mathrm)\{d\}x','',rhs))
 assert equal(left_factor*derivative,right_factor)
 table=re.findall(r'^\| \$([xu])\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',solution,re.M);assert len(table)==2
 table_x=[scalar(t) for t in table[0][1:]];table_u=[scalar(t) for t in table[1][1:]]
 assert equal(table_x[0],low) and equal(table_x[1],high)
 assert all(equal(substitution.subs(x,a),b) for a,b in zip(table_x,table_u))
 stage_rows=rows(solution);assert equal(expression(stage_rows[0].split('=',1)[0]),correct_value)
 prior_body=None;count=0
 for row in stage_rows:
  rhs=row.split('=',1)[1];assert equal(expression(rhs),correct_value),(rhs,expression(rhs),correct_value)
  if r'\int' in rhs:
   c,G,w,L,H,after=integral_parts(rhs);assert not after
   if w==x:assert equal(c*G,coeff*F) and equal(L,low) and equal(H,high)
   else:
    assert equal(L,table_u[0]) and equal(H,table_u[1])
    assert equal((c*G).subs(u,substitution)*derivative,coeff*F)
   prior_body=(c*G,w)
  elif '|' in rhs:
   before=clean(rhs).split('|',1)[0];assert prior_body is not None
   derived=s.diff(scalar(before),prior_body[1])
   if derived.has(s.sign(u)):
    assert all(v>0 for v in table_u)
    derived=derived.subs(s.sign(u),1).subs(s.Abs(u),u)
   assert equal(derived,prior_body[0])
  count+=1
 f=question[':question/answer-fields'][0];values=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len({a[':answer/id'] for a in f[':answer-field/choices']})==len(values)
 for i,a in enumerate(values):assert all(not equal(a,b) for b in values[:i])
 selected=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert equal(scalar(selected[':answer/value']),correct_value)
 if f[':answer-field/type']==':answer-field.type/blank':assert '{{'+f[':answer-field/key']+'}}' in prompt
 if expected_signature is not None:assert signatures(solution)==expected_signature,(signatures(solution),expected_signature)
 return {'rows':count,'formal_derivatives':1,'differential_relations':1,'bounds':4,'bank_values':len(values)}
