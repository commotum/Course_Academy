"""Root printed two-term integrals, real log families, all banks and C↔K equality."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ID=17592186064208;D=R.parents[2]/f'generate/scratch/{ID}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_combined_rational_gen',D.with_suffix('.py'));P=load('root_combined_rational_math',R/'elementary-integral-readback.py');B=load('root_combined_groups',R/'direct-derivative-readback.py');x,C=P.x,P.C;K=s.Symbol('root_positive_K',positive=True);k=P.P.locals_['k']
def scalar(t):
 t=re.sub(r'\\text\{\s*\}', '',t)
 return P.scalar(re.sub(r'(?<![A-Za-z\\])K(?![A-Za-z])','k',t)).subs(k,K)
def normalize(expr):
 expr=s.expand_log(expr)
 sub={}
 for node in expr.atoms(s.log):
  arg=node.args[0]
  if arg.func==s.Abs:
   numerator,denominator=s.fraction(s.cancel(arg.args[0]));z=s.Integer(0)
   for poly,sign in[(numerator,1),(denominator,-1)]:
    coef,fac=s.factor_list(poly,x);z+=sign*s.log(s.Abs(coef))
    for f,n in fac:
     assert s.degree(f,x)==1;a=f.coeff(x);root=-f.subs(x,0)/a;z+=sign*n*(s.log(s.Abs(a))+s.Function('root_logabs')(x-root))
   sub[node]=z
  else:assert not arg.has(x),('unqualified real log domain',node)
 return s.expand(s.expand_log(expr.xreplace(sub)))
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{ID}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};N=dict(raw_records=0,source_banks=0,source_values=0,source_keys=0,source_solutions=0,records=0,formal_integrals=0,primitive_stages=0,constant_family_equalities=0,values=0,pairs=0,connected_real_components=0);tasks={l:set()for l in G.LEVELS}
def check(r,sid=None):
 q,m=r['question'],r['generation'];F,var=P.prompt(q[':question/problem']);assert var==x;block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution']);assert len(block)==1;rows=[v.strip()for v in block[0].split(r'\\')];assert len(rows)==4
 left,right=rows[0].replace('&','').split('=');value,ops=P.side(left);assert len(ops)==1 and s.cancel(value-F)==0;N['formal_integrals']+=1;value,ops=P.side(right);assert len(ops)==2 and s.cancel(value-F)==0;N['formal_integrals']+=2
 denominators=[s.denom(z[0])for z in ops];assert all(s.Poly(z,x).degree()==1 for z in denominators);poles=sorted({root for z in denominators for root in s.solve(z,x)});assert len(poles)==2 and list(map(str,poles))==m['domain']['excluded_poles'];N['connected_real_components']+=3;assert m['domain']['K'].startswith('positive arbitrary')
 a=s.Poly(denominators[0],x).coeff_monomial(x);assert a!=0;primitive=[]
 for row in rows[1:]:
  expr=scalar(row.replace('&','').strip().removeprefix('='));assert s.cancel(P.derivative(s.expand_log(expr),x)-F)==0;N['primitive_stages']+=1;primitive.append(expr)
 for expr in primitive[1:]:assert s.simplify(normalize(expr)-normalize(primitive[0].subs(C,s.log(K)/a)))==0,('actual C/K rewrite',rows,expr);N['constant_family_equalities']+=1
 f=q[':question/answer-fields'][0];values=[scalar(z[':answer/value'])for z in f[':answer-field/choices']];derivatives=[s.cancel(P.derivative(s.expand_log(z),x))for z in values];assert len(values)==5;assert[z[':answer/id']for z,d in zip(f[':answer-field/choices'],derivatives)if s.cancel(d-F)==0]==[f[':answer-field/correct'][1]]
 for i,d in enumerate(derivatives):
  for v in derivatives[:i]:assert s.cancel(d-v)!=0;N['pairs']+=1
 if sid:
  o=olds[sid];of=o.get(':question/answer-fields',[None])[0]
  if of:
   old=[normalize(scalar(z[':answer/value']))for z in of[':answer-field/choices']];new=[normalize(v)for v in values];assert len(old)==len(new)and all(sum(s.simplify(v-w)==0 for w in new)==1 for v in old);N['source_banks']+=1;N['source_values']+=len(old)
   if ':answer-field/correct'in of:assert s.cancel(P.derivative(s.expand_log(scalar(of[':answer-field/correct'][':answer/value'])),x)-F)==0;N['source_keys']+=1
  if ':question/worked-solution'in o:assert q[':question/worked-solution']==G.fmt.normalize_prose(o[':question/worked-solution']);N['source_solutions']+=1
 N['records']+=1;N['values']+=len(values);tasks[q[':question/difficulty'].split('/')[-1]].add(str(s.cancel(F)))
for sid,o in olds.items():
 assert G.source_case(sid)['raw']==o;N['raw_records']+=1;c=next(c for c in json.load(open(D/'source-cases.json'))if c['source_id']==sid);check(c['record'],sid)
for r in json.load(open(D/'previews.json')):check(r)
for l in G.LEVELS:
 for seed in range(18):check(G.generate(l,seed))
for bad in(True,1.1,'1'):
 for fn in(lambda:G.generate('easy',seed=bad),lambda:G.batch('easy',bad),lambda:G.batch('easy',1,bad)):
  try:fn()
  except ValueError:pass
  else:raise AssertionError('invalid integer')
result=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,sampled_actual_integrands={l:len(t)for l,t in tasks.items()},constant_and_domain_proof='Printed C=ln(K)/a substitution verified for every primitive equality, K>0 and a nonzero: bijective arbitrary constant family. Factorized log absolute identities valid on all three real components excluding both printed poles, no forced sign simplification.',scope='Observed hard complete reciprocal-linear banks; missing E/M are explicit same two-term general-formula/single-log families, unit versus small integer inner slopes. No additional substitutions or nonlinear denominator skills.',database_writes=0);(R/f'qa/{ID}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
