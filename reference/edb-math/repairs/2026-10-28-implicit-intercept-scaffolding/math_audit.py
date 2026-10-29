import json,re,sys,collections,hashlib,subprocess,importlib.util,random
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
REPO=Path(__file__).resolve().parents[9] if False else Path('/home/jake/Developer/Course_Academy')
E=Path(__file__).resolve().parent; W=E/'package'; PY=REPO/'.venv/bin/python'
sys.path.insert(0,str(W));import generator as g
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
def inspect(r):
 q=r['question'];p=q[':question/problem'];sol=q[':question/worked-solution']
 eq=re.search(r'curve has equation \$(.*?)\$',p)[1];l,rhs=eq.split('=');F=algebra(l)-algebra(rhs)
 pt=pair(re.search(r'line at \$(.*?)\$',p)[1]);axis=re.search(r'meets the \$([xy])\$-axis',p)[1];normal='**normal**' in p
 sub=dict(zip((x,y),pt));gx=s.diff(F,x).subs(sub);gy=s.diff(F,y).subs(sub)
 assert F.subs(sub)==0 and gx!=0 and gy!=0
 mt=-gx/gy;m=-1/mt if normal else mt
 ans=(s.cancel(pt[0]-pt[1]/m),s.Integer(0)) if axis=='x' else (s.Integer(0),s.cancel(pt[1]-m*pt[0]))
 assert ans==key(r),(ans,key(r),p)
 final=re.search(r'Therefore \$[PQ]=(.*?)\$\.',sol)[1];assert pair(final)==ans
 drow=re.search(r'\\begin\{aligned\}\n(.*?)&=0',sol,re.S)[1].replace(r'\frac{dy}{dx}','J')
 assert s.cancel(algebra(drow).subs(J,-s.diff(F,x)/s.diff(F,y)))==0
 last=re.findall(r'\n([xy])&=([^\n]+)\n\\end\{aligned\}',sol)[-1];assert algebra(last[1])==ans[0 if last[0]=='x' else 1]
 for f in q[':question/answer-fields']:
  vals=[pair(a[':answer/value']) for a in f[':answer-field/choices']] if f[':answer-field/type'].endswith('/radio') else []
  if vals:assert len(set(vals))==5 and vals.count(ans)==1
 shape='product' if F.coeff(x*y) else ('parabola' if not F.coeff(y,2) else ('translated' if F.coeff(x,1).subs(y,0)!=0 or F.coeff(y,1).subs(x,0)!=0 else ('circle' if F.coeff(x,2)==F.coeff(y,2) else 'ellipse/hyperbola')))
 return {'axis':axis,'normal':normal,'shape':shape,'point':list(map(str,pt)),'F':str(F),'slope':str(m),'answer':list(map(str,ans)),'final_expression':final}
def probes(rs,label):
 groups=collections.defaultdict(list)
 for r in rs:
  fs=r['question'][':question/answer-fields'];w=inspect(r)
  if not fs[0][':answer-field/type'].endswith('/radio'):continue
  for subgroup in ['all',w['axis'],w['shape']+'-'+w['axis']]:groups[subgroup].append((r,w))
 out=[]
 for group,items in groups.items():
  counts=collections.Counter();positions=collections.Counter();ranks=collections.Counter();pair_contains=0
  for r,w in items:
   f=r['question'][':question/answer-fields'][0];axis=w['axis'];vals=[pair(a[':answer/value'])[0 if axis=='x' else 1] for a in f[':answer-field/choices']];i=vals.index(key(r)[0 if axis=='x' else 1]);positions[i]+=1;ranks[sorted(vals).index(vals[i])]+=1
   for j in range(5):counts['position-'+str(j)]+=int(i==j);counts['rank-'+str(j)]+=int(sorted(vals).index(vals[i])==j)
   for name,fn in [('min_abs',lambda v:abs(v)),('max_abs',lambda v:-abs(v)),('min_den',lambda v:s.denom(v)),('max_den',lambda v:-s.denom(v))]:
    scores=list(map(fn,vals));wins=[j for j,z in enumerate(scores) if z==min(scores)];counts[name]+=int(wins==[i])
   paired=[j for j,z in enumerate(vals) if z!=0 and -z in vals];pair_contains+=int(len(paired)==2 and i in paired)
   # Bank-only strategy: choose the positive member of the unique opposite pair; no target/keys consulted.
   wins=[j for j in paired if vals[j]>0] if len(paired)==2 else [];counts['positive_opposite']+=int(wins==[i])
   wins=[j for j in paired if vals[j]<0] if len(paired)==2 else [];counts['negative_opposite']+=int(wins==[i])
   for sign in [-1,1]:
    wins=[j for j,z in enumerate(vals) if s.sign(z)==sign];counts['unique_sign_'+str(sign)]+=int(wins==[i])
  out.append({'set':label,'group':group,'total':len(items),'counts':dict(counts),'positions':dict(positions),'ranks':dict(ranks),'unique_opposite_contains':pair_contains})
 return out
