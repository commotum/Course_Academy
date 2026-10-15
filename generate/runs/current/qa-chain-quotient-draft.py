"""Root quotient operands, full solution equalities, fragments and option banks."""
import sys,json,re,hashlib,importlib.util,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096844;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_cq_gen',D.with_suffix('.py'));P=load('root_cq_math',R/'chain-combination-readback.py');F=load('root_cq_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D);x=P.x
N=dict(records=0,bindings=0,equation_rows=0,formal_rows=0,values=0,pairs=0,banks=0,blanks=0,domains=0,targets=0,time_functions=0)
def check(r):
 q,m=r['question'],r['generation'];t=m['template'];p=m['parameters'];fun,var,at=P.givens(q[':question/problem']);rows,formal=P.stages(q[':question/worked-solution'],fun,var,at,True);N['equation_rows']+=rows;N['formal_rows']+=formal;N['bindings']+=2;df=s.diff(fun,var);answer=df.subs(var,at) if at is not None else df
 f=q[':question/answer-fields'][0];vals=[P.scalar(v[':answer/value']) for v in f[':answer-field/choices']];a,b,c=p.get('a'),p.get('b'),p.get('c')
 if f[':answer-field/type'].endswith('/blank'):
  P.blank(q[':question/problem'],f[':answer-field/choices'][0][':answer/value'],fun,var,at);N['blanks']+=1
  if t=='q-313362':answer=s.factor(df*(3*x+c)**3)
  elif t=='q-313365':answer=s.factor(df*(x+b)**2)
  elif t=='q-313371':answer=s.factor(df*x*s.exp(a*x))
  elif t=='q-344143':answer=s.factor(df*(x-2)**2/s.exp(a*x*x))
  elif t=='authored-affine-square':answer=s.factor(df*x*x)
  expected=[answer]
 elif t=='q-11973':expected=[6*x/(3*x+c)**3,x/(3*x+c)**4,df,2*x/(3*x+c)**4,c*x/(3*x+c)**4]
 elif t=='q-2396':
  T=s.tan(7*x+b);S=s.sec(7*x+b)**2;expected=[df,(7*S-T)/(16*x*x),(x*S+T)/(4*x*x),(7*x*S-T)/(16*x*x),(S-T)/(4*x*x)]
 elif t=='q-11978':
  Dn=(x*x+a*a)**2;expected=[(a-x)**2/Dn,2*(x+a)/Dn,df,2*(a-x)/Dn,(a-2*x*x)/Dn]
 elif t=='q-2403':
  L=s.log(x);expected=[(x-a*s.sqrt(L))/(a*a*x*x*L),(s.Rational(a,2)-a*L)/s.sqrt(L),(1+a*s.sqrt(L))/(a*x*x*s.sqrt(L)),df,(L-a)/s.sqrt(L)]
 else:raise AssertionError(t)
 assert len(vals)==len(expected) and all(sum(P.eq(v,e) for v in vals)==1 for e in expected),(t,vals,expected)
 assert sum(P.eq(v,answer) for v in vals)==1 and P.eq(next(v for v,z in zip(vals,f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1]),answer)
 for v,w in itertools.combinations(vals,2):assert not P.eq(v,w);N['pairs']+=1
 domain=m['domain'];den=P.definitions(q[':question/worked-solution'],var);v=list(den.values())[1]
 if t=='q-2396':assert 'cos(7*x' in domain['restriction'] and 'x != 0' in domain['restriction']
 elif t=='q-2403':assert domain['restriction']=='x>1'
 elif t=='q-132975':assert domain['restriction']=='t>0' and var==P.t;N['time_functions']+=1
 elif t=='q-313371':assert domain['restriction']=='x>0'
 elif t=='q-11978':assert domain['restriction']=='all real x'
 else:
  assert 'denominator nonzero' in domain['restriction']
  assert {s.simplify(P.scalar(z)) for z in domain['denominator_zeroes']}==set(s.solve(v,var))
 if at is not None:assert s.simplify(v.subs(var,at))!=0;N['targets']+=1
 N['values']+=len(vals);N['banks']+=1;N['domains']+=1;N['records']+=1
for r in json.load(open(R/f'qa/{K}-sampled.json')):check(r)
for t,l in G.LEVELS.items():
 if t in G.EXCLUDED:continue
 ps=G.parameters_for(t)
 for p in (ps[0],ps[len(ps)//2],ps[-1]):check(G.generate(l,template=t,parameters=p))
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
