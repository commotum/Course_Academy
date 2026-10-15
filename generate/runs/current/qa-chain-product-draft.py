"""Root actual product equations and source-derived whole option banks."""
import sys,json,re,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096845;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_cp_gen',D.with_suffix('.py'));P=load('root_cp_math',R/'chain-combination-readback.py');F=load('root_cp_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D);x,a=P.x,P.a
N=dict(records=0,bindings=0,equation_rows=0,formal_rows=0,values=0,pairs=0,banks=0,blanks=0,domains=0)
def check(r):
 q,m=r['question'],r['generation'];t=m['template'];p=m['parameters'];fun,var,at=P.givens(q[':question/problem']);assert var==x and at is None
 rows,formal=P.stages(q[':question/worked-solution'],fun,var,at);N['equation_rows']+=rows;N['formal_rows']+=formal;N['bindings']+=2;df=s.diff(fun,x)
 f=q[':question/answer-fields'][0];vals=[P.scalar(v[':answer/value']) for v in f[':answer-field/choices']];answer=df
 if t in ('q-343332','q-343333','q-343354'):
  P.blank(q[':question/problem'],f[':answer-field/choices'][0][':answer/value'],fun,x,None);N['blanks']+=1
  factor=s.exp(x) if t=='q-343332' else s.exp(p['k']*x);answer=s.cancel(df/factor);expected=[answer]
 elif t=='q-11824':
  k=p['k'];E=s.exp(k*x);expected=[(k*x+1)*E,df,(x+1)*E,k*x*E,k*(x+1)*E]
 elif t=='q-2392':
  k=p['k'];E=a**(k*x);T=s.tan(x);S=s.sec(x)**2;expected=[df,E*(S+k*T),E*S+k*T,k*E*(S+s.log(a)*T),k*S+k*E*T]
 elif t=='q-9942':
  k,b=p['k'],p['b'];S=s.sin(k*x+b);C=s.cos(k*x+b);expected=[2*x*x*S+k*x*C,2*x*S+x*x*C,2*S+k*x*x*C,df,k*x*S+2*x*x*C]
 elif t=='q-2401':
  c=p['c'];S=s.sin(x);C=s.cos(x);expected=[(s.Rational(c,4)*x*C+s.Rational(c,2)*x*S)/S,s.Rational(c,2)*x*x*s.sqrt(S)-s.Rational(c,4)*x*s.sqrt(S),(s.Rational(c,2)*x*x*S-2*c*x*S)/s.sqrt(S),df,-s.Rational(c,2)*x*x*s.sqrt(C)+2*c*x*s.sqrt(S)]
 elif t=='q-11599':
  k,b=p['k'],p['b'];Z=k*x*x+b;expected=[(6*k*x**4+b*x*x)*Z**2,(6*k*x**4+3*b*x*x)*Z**2,(9*k*x**4+3*b*x*x)*Z**3,df,(3*b*x**4+6*k*x*x)*Z**2]
 else:raise AssertionError(t)
 assert len(vals)==len(expected) and all(sum(P.eq(v,e) for v in vals)==1 for e in expected),(t,vals,expected)
 assert sum(P.eq(v,answer) for v in vals)==1
 correct=next(v for v,z in zip(vals,f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1]);assert P.eq(correct,answer)
 for v,w in itertools.combinations(vals,2):assert not P.eq(v,w);N['pairs']+=1
 restriction=m['domains']
 if t=='q-343333':assert restriction=='x>0'
 elif t=='q-2392':assert 'a>0' in restriction and 'cos(x)!=0' in restriction
 elif t=='q-2401':assert 'sin(x)>0' in restriction and 'cos(x)>0' in restriction
 else:assert restriction=='real x'
 N['values']+=len(vals);N['banks']+=1;N['domains']+=1;N['records']+=1
for r in json.load(open(R/f'qa/{K}-sampled.json')):check(r)
for t,l in G.LEVELS.items():
 ps=G.parameter_domain(t)
 for p in (ps[0],ps[len(ps)//2],ps[-1]):check(G.generate(l,template=t,parameters=p))
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
