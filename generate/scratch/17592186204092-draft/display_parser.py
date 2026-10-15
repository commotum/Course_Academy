"""Private frozen exact parser for this linear no-solution backbone."""
import re,uuid
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
LETTERS='xyzuvwpqrkmnab';SYMBOLS={c:sp.Symbol(c) for c in LETTERS}
def expr(text):
 text=text.strip().rstrip('.')
 text=re.sub(r'\{\{(.*?)\}_\{⏟\}\}_\{[ab]\}',r'\1',text)
 text=re.sub(r'\\underbrace\{([^{}]+)\}_\{[ab]\}',r'(\1)',text)
 text=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',text)
 if not re.fullmatch(r'[0-9xyzuvwpqrkmnab+*/().\-\s]+',text):raise ValueError('unsupported exact expression: '+text)
 text=re.sub(r'([a-z])(?=[a-z])',r'\1*',text)
 return parse_expr(text,local_dict=SYMBOLS,transformations=standard_transformations+(implicit_multiplication_application,))
def prompt_parameters(problem):
 m=re.search(r'\$\$\s*(.*?)\s*\$\$',problem,re.S)
 equation=m[1] if m else re.search(r'\$([^$]*=[^$]*)\$',problem)[1]
 match=re.fullmatch(r'(-?\d*)([pqrkmn])([xyzuvw])([+-]\d+)?=(-?\d*)([xyzuvw])([+-]\d+)?',re.sub(r'\s+','',equation))
 if not match:raise ValueError('prompt equation outside backbone')
 a,k,x,b,c,y,d=match.groups()
 if x!=y:raise ValueError('different equation variables')
 def integer(v):return int(v) if v not in ('','-') else (-1 if v=='-' else 1)
 return dict(variable=x,parameter=k,a=integer(a),b=int(b or 0),c=integer(c),d=int(d or 0))
def validate_record(rec):
 q=rec['question'];meta=rec['generation'];p=prompt_parameters(q[':question/problem'])
 if p!=meta['parameters']:raise ValueError('rendered givens/metadata disagree')
 if rec['knowledge_point']['db_id']!=17592186204092:raise ValueError('KP mismatch')
 x,k=SYMBOLS[p['variable']],SYMBOLS[p['parameter']];root=sp.Rational(p['c'],p['a']);delta=(p['a']*k-p['c'])*x+p['b']-p['d']
 if not p['a'] or not p['c'] or p['b']==p['d']:raise ValueError('parameter constraints')
 if sp.expand(delta.subs(k,root)).has(x) or delta.subs(k,root)==0:raise ValueError('must be contradiction')
 if sp.expand(delta.subs(k,root+1)).coeff(x)==0:raise ValueError('neighbor must have unique solution')
 level=q[':question/difficulty'].split('/')[-1]
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if len(q[':question/answer-fields'])!=1:raise ValueError('field count')
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];correct=f[':answer-field/correct'];values=[expr(a[':answer/value']) for a in choices]
 expected=[root,sp.Rational(p['a'],p['c']),sp.Rational(p['c']-1,p['a']),sp.Rational(p['c'],p['c']-1),sp.Integer(p['c']-1)] if level=='easy' else [root]
 if values!=expected or len(set(values))!=len(values):raise ValueError('whole bank mismatch/collision')
 if correct!=[':answer/id',choices[0][':answer/id']]:raise ValueError('correct ownership')
 if f[':answer-field/type']!=':answer-field.type/'+('radio' if level=='easy' else 'blank') or f[':answer-field/key']!=('selection' if level=='easy' else 'field-1'):raise ValueError('field contract')
 if any(a[':answer/type']!=':answer.type/math' for a in choices):raise ValueError('answer type')
 if level=='easy' and p['b'] or level!='easy' and not p['b']:raise ValueError('constant workload')
 ids=[q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in choices]
 if len(set(ids))!=len(ids):raise ValueError('identity collision')
 for i in ids:uuid.UUID(i)
 if q[':question/problem'].count('{{field-1}}')!=(0 if level=='easy' else 1):raise ValueError('placeholder')
 if f'variable ${p["variable"]},$' not in q[':question/problem'] or f'where ${p["parameter"]}$ is a constant' not in q[':question/problem']:raise ValueError('target naming')
 solution=q[':question/worked-solution']
 for phrase in (f'factor ${p["variable"]}$ on the left-hand side',f'Solving this for ${p["parameter"]},$'): 
  if phrase not in solution:raise ValueError('stale target reference')
 displays=re.findall(r'\$\$\s*(.*?)\s*\$\$',solution,re.S)
 stage_count=0
 for display in displays:
  if display=='ax=b':continue
  if display.startswith(r'\begin{aligned}'):
   body=display[len(r'\begin{aligned}'): -len(r'\end{aligned}')];lines=body.split(r'\\')
  else:lines=[display]
  for line in lines:
   if '=' not in line:raise ValueError('missing equation')
   l,r=map(expr,line.replace('&','').split('='));diff=sp.expand(l-r)
   if x in diff.free_symbols:
    if sp.expand(diff-delta)!=0:raise ValueError('invalid variable equation intermediate')
   elif k in diff.free_symbols:
    if sp.solve(diff,k)!=[root]:raise ValueError('invalid parameter equation intermediate')
   else:raise ValueError('unexpected constant equation')
  stage_count+=1
 if stage_count!=(5 if level=='easy' else 6):raise ValueError('ordered solution workload')
 for key in (':question/problem',':question/worked-solution'):
  text=q[key]
  if text.count('$')%2 or text.count('{')!=text.count('}'):raise ValueError('unbalanced mathematics')
 return True
