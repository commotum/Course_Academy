import json,re,sys,collections,argparse
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x,y,J=s.symbols('x y J')
def save(n,d): (E/n).write_text(json.dumps(d,indent=2,default=str)+'\n')
def read(p):return json.loads(Path(p).read_text())
def algebra(t):
 t=t.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\dfrac',r'\frac').replace(r'\cdot','*').strip().rstrip('.')
 while r'\frac' in t:
  new=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',lambda m:'(('+m[1]+')/('+m[2]+'))',t)
  assert new!=t,t
  t=new
 t=t.replace('^','**').replace('{','(').replace('}',')')
 assert '\\' not in t,t
 return parse_expr(t,local_dict={'x':x,'y':y,'J':J},transformations=standard_transformations+(implicit_multiplication_application,))
def pair(t):
 t=t.replace(r'\left','').replace(r'\right','').replace(r'\,','').strip().rstrip('.')
 return tuple(algebra(z) for z in t[1:-1].split(','))
def correct(f):return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def key(r):
 fs=r['question'][':question/answer-fields']
 if fs[0][':answer-field/type'].endswith('/radio'):return pair(correct(fs[0])[':answer/value'])
 return tuple(algebra(correct(next(f for f in fs if f[':answer-field/key']=='field-'+str(i)))[':answer/value']) for i in (1,2))

p=argparse.ArgumentParser();p.add_argument('--input',type=Path);args=p.parse_args()
if args.input:rs=json.loads(args.input.read_text())
else:
 import generator
 rs=generator.generate('easy',5,2936070573)
groups=collections.defaultdict(list)
for r in rs:
 q=r['question'];f=q[':question/answer-fields'][0]
 if not f[':answer-field/type'].endswith('/radio'):continue
 text=q[':question/problem'];axis=re.search(r'meets the \$([xy])\$-axis',text)[1]
 eq=re.search(r'curve has equation \$(.*?)\$',text)[1].split('=')[0];F=algebra(eq)
 shape='circle' if F.coeff(x,2)==F.coeff(y,2) else 'ellipse'
 vals=[pair(z[':answer/value'])[0 if axis=='x' else 1] for z in f[':answer-field/choices']]
 i=vals.index(key(r)[0 if axis=='x' else 1]);v=vals[i]
 actions={'position:'+str(i),'rank:'+str(sorted(vals).index(v))}
 for cue,scores in [('min-abs',[abs(z) for z in vals]),('max-abs',[-abs(z) for z in vals]),('min-den',[s.denom(z) for z in vals]),('max-den',[-s.denom(z) for z in vals])]:
  if [j for j,z in enumerate(scores) if z==min(scores)]==[i]:actions.add(cue)
 paired=[j for j,z in enumerate(vals) if z and -z in vals]
 if len(paired)==2 and i in paired:actions.add('positive-opposite' if v>0 else 'negative-opposite')
 for sign in [-1,1]:
  if [j for j,z in enumerate(vals) if s.sign(z)==sign]==[i]:actions.add('unique-sign:'+str(sign))
 for group in ['all',axis,shape+'-'+axis]:groups[group].append(actions)
fail={k:sorted(set.intersection(*v)) for k,v in groups.items() if len(v)>=2 and set.intersection(*v)}
print(json.dumps({'input':str(args.input),'failures':fail,'passed':not fail}));raise SystemExit(bool(fail))
