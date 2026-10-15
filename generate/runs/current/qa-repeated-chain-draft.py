"""Root actual three-function bindings, every formal chain factor and whole banks."""
import sys,json,re,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096742;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_mc_gen',D.with_suffix('.py'));P=load('root_mc_math',R/'chain-combination-readback.py');F=load('root_mc_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D);x,u,v=P.x,P.u,P.v
N=dict(records=0,bindings=0,derivative_rows=0,formal_operators=0,chain_rows=0,evaluation_rows=0,values=0,pairs=0,banks=0,blanks=0,domains=0)
def clean(t):return P.clean(t)
def val(text,defs,fun,label,at):
 text=clean(text)
 def fraction(m):
  name,var=m[1],m[2];assert name in (label,'u','v')
  if var=='u':assert name==label;result=s.diff(defs[label],u)
  elif var=='v':assert name=='u';result=s.diff(defs['u'],v)
  else:
   assert var=='x';f=fun if name==label else defs['u'].subs(v,defs['v']) if name=='u' else defs['v'];result=s.diff(f,x)
  N['formal_operators']+=1;return '('+s.latex(result).replace(r'\log',r'\ln')+')'
 text=re.sub(r'\\frac\{\\mathrm\{d\}([fyhuv])\}\{\\mathrm\{d\}([xuv])\}',fraction,text)
 def named(m):
  arg=P.scalar(m[1]);assert arg==x or at is not None and P.eq(arg,at),(arg,at)
  return '('+s.latex(s.diff(fun,x).subs(x,arg)).replace(r'\log',r'\ln')+')'
 text=re.sub(label+r"(?:\^\{\x27\}|\x27)\((.*?)\)",named,text)
 return P.scalar(text).subs(u,defs['u']).subs(v,defs['v'])
def check(r):
 q,m=r['question'],r['generation'];tid=m['template'];p=m['parameters'];prompt=clean(q[':question/problem']);given=re.search(r'\$([fyh])(?:\(x\))?\s*=\s*(.*?)\$',prompt);assert given;label=given[1];fun=P.scalar(given[2]);point=re.search(label+r"(?:\^\{\x27\}|\x27)\(([^x][^)]*)\)",prompt);at=P.scalar(point[1]) if point else None
 sol=clean(q[':question/worked-solution']);blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);head=blocks[0]
 defs={n:P.scalar(e.strip().strip(',')) for n,e in re.findall(r'([fyhuv])\s*=\s*(.*?)(?=\s*,?\s*[fyhuv]\s*=|$)',head,re.S)};assert set(defs)=={label,'u','v'},defs
 assert defs[label].free_symbols<={u} and defs['u'].free_symbols<={v} and defs['v'].free_symbols<={x}
 assert P.eq(defs[label].subs(u,defs['u']).subs(v,defs['v']),fun);N['bindings']+=3;df=s.diff(fun,x)
 body=blocks[1]
 parts=re.split(r',(?=\s*\\frac)',body)
 assert len(parts)==3
 for equation,(name,var) in zip(parts,((label,'u'),('u','v'),('v','x'))):
  lhs,rhs=equation.split('=');assert lhs.strip()==r'\frac{\mathrm{d}'+name+r'}{\mathrm{d}'+var+'}';assert P.eq(val(lhs,defs,fun,label,at),val(rhs,defs,fun,label,at));N['derivative_rows']+=1
 for bi,block in enumerate(blocks[2:]):
  for row in block.split(r'\\'):
   parts=row.replace('&','').strip().split('=');parts=[z for z in parts if z.strip()];wanted=df if bi==0 else df.subs(x,at)
   actual=[val(z,defs,fun,label,at) for z in parts];assert all(P.eq(z,wanted) for z in actual),(tid,row,actual,wanted)
   N['chain_rows' if bi==0 else 'evaluation_rows']+=1
 field=q[':question/answer-fields'][0];vals=[P.scalar(z[':answer/value']) for z in field[':answer-field/choices']];answer=df.subs(x,at) if at is not None else df
 a,b=p.get('a'),p.get('b');z=defs['v']
 if tid=='q-48569':expected=[df,-3*a*s.cos(x)**2*s.sin(x),-3*s.sin(z)**2,3*a*s.sin(z)**2*s.cos(z),3*s.cos(z)**2*s.sin(z)]
 elif tid=='q-48570':expected=[df,3*s.sin(z)**2*s.cos(z),3*a*s.sin(x)**2*s.cos(x),3*a*s.sin(z)*s.cos(z),3*s.sin(x)*s.cos(x)]
 elif tid=='q-2397':expected=[df,3*x*s.sin(z)**2*s.cos(z)**2,2*a*x*s.sin(z)**2*s.cos(z)**2,2*a*x*s.sin(z)**2*s.cos(z),6*a*x*s.sin(z)**3*s.cos(z)**3]
 elif tid=='q-31352':expected=[df,-s.csc((x+b)**2)**2,2*x*s.csc((x+b)**2)**2,-2*(x+b)*s.csc(x+b),4*(x+b)]
 elif tid=='q-31361':expected=[answer,a*s.cot(b)**3*s.sec(b)**2,-4*s.cot(b)**2*s.csc(b)**2,4*a*s.cot(b)*s.sec(b)**2,-4*s.cot(b)**3*s.csc(b)**2]
 elif tid=='q-28655':expected=[answer,-1,-a,a,1]
 elif tid=='q-312907':answer=-24*a*x*x;expected=[answer];P.blank(q[':question/problem'],field[':answer-field/choices'][0][':answer/value'],fun,x,at);N['blanks']+=1
 elif tid=='q-342927':answer=-s.sin(z);expected=[answer];P.blank(q[':question/problem'],field[':answer-field/choices'][0][':answer/value'],fun,x,at);N['blanks']+=1
 else:raise AssertionError(tid)
 assert len(vals)==len(expected) and all(sum(P.eq(v,e) for v in vals)==1 for e in expected),(tid,vals,expected)
 assert sum(P.eq(v,answer) for v in vals)==1 and P.eq(next(v for v,z in zip(vals,field[':answer-field/choices']) if z[':answer/id']==field[':answer-field/correct'][1]),answer)
 for a1,b1 in itertools.combinations(vals,2):assert not P.eq(a1,b1);N['pairs']+=1
 domain=m['domain'];assert domain['real_x'] and domain['radians']
 if tid=='q-342927':assert '\\cos(' in domain['restriction'] and domain['restriction'].endswith(')>0') and 1<=b<=24
 elif tid=='q-28655':assert domain['restriction']==r'\cos(x)>0' and p=={'a':5}
 elif tid in ('q-31352','q-31361'):assert domain['restriction'].endswith(r'\notin\pi\mathbb{Z}')
 else:assert domain['restriction']=='all real x'
 N['values']+=len(vals);N['banks']+=1;N['domains']+=1;N['records']+=1
if __name__=='__main__':
 for r in json.load(open(R/f'qa/{K}-sampled.json')):check(r)
 for tid,l in G.DIFFICULTIES.items():
  if tid in G.RAW_ONLY:continue
  ps=[{'a':5}] if tid=='q-28655' else G.parameters_for(tid)
  for p in (ps[0],ps[len(ps)//2],ps[-1]):check(G.generate(l,template=tid,parameters=p,profile='source-compatibility' if tid=='q-28655' else None))
 result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
