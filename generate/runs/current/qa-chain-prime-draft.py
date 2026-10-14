"""Root verifies displayed composites, formal prime inputs, chain factors and banks."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096843;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);sys.modules[n]=m;z.loader.exec_module(m);return m
G=mod('root_prime_generator',D.with_suffix('.py'));P=mod('root_prime_scalar',R/'ode-scalar-parser.py');F=mod('root_prime_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D);x,u=P.x,P.u
C=dict(records=0,composite_givens=0,bindings=0,formal_derivative_inputs=0,derivative_rows=0,chain_rule_factors=0,final_derivatives=0,blank_fragments=0,values=0,pairs=0,whole_banks=0,domains=0)
def clean(t):
 t=t.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace('{)}',')');t=re.sub(r'\{g\}', 'g',t);t=t.replace('g(x)','u')
 while r'\sqrt[' in t:
  m=re.search(r'\\sqrt\[(\d+)\]\{',t);assert m;start=m.end()-1;depth=1;end=start
  while depth:
   end+=1;assert end<len(t);depth+=(t[end]=='{')-(t[end]=='}')
  t=t[:m.start()]+'('+t[start+1:end]+r')^{\frac{1}{'+m[1]+'}}'+t[end+1:]
 return t.replace('g','u')
def scalar(t):return P.scalar(clean(t))
def eq(a,b):
 return s.simplify(s.powdenest(a,force=True)-s.powdenest(b,force=True))==0
def formal(t,var):
 t=clean(t);assert t.endswith('^{′}'),t;t=t[:-4]
 if t.startswith('{(') and t.endswith(')}'):t=t[1:-1]
 assert t.startswith('(') and t.endswith(')'),t;v=scalar(t[1:-1]);C['formal_derivative_inputs']+=1;return v,s.diff(v,var)
def check(r,raw=False):
 q,m=r['question'],r['generation'];t=m['template'];prompt=q[':question/problem'];fmatch=re.search(r'\$f\(x\)\s*=\s*(.*?)\$',prompt);assert fmatch;fun=scalar(fmatch[1]);df=s.diff(fun,x);C['composite_givens']+=1
 sol=q.get(':question/worked-solution')
 if sol:
  defs=re.search(r'Let \$g\(x\)=(.*?)\$ and \$f\(g\(x\)\)=(.*?)\$',sol);assert defs;inner,outer=map(scalar,defs.groups());assert eq(fun,outer.subs(u,inner));C['bindings']+=2
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==2;rows=[b.strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r'\\') for b in blocks];assert list(map(len,rows))==[2,3]
  for i,row in enumerate(rows[0]):
   lhs,form,value=row.replace('&','').strip().split('=');assert lhs.strip()==(r'{f}^{′}(g(x))' if i==0 else r'{g}^{′}(x)')
   v,d=formal(form,u if i==0 else x);assert eq(v,outer if i==0 else inner) and eq(scalar(value),d);C['derivative_rows']+=1
  lhs,right=rows[1][0].replace('&','').split('=');assert lhs.strip()==r'{f}^{′}(x)' and right.strip()==r'{f}^{′}(g(x))\cdot {g}^{′}(x)'
  lhs,right=rows[1][1].replace('&','').split('=');assert not lhs.strip() and right.count(r'\cdot')==1
  od,id=map(scalar,right.split(r'\cdot'));assert eq(od,s.diff(outer,u)) and eq(id,s.diff(inner,x));C['chain_rule_factors']+=2
  assert eq((od*id).subs(u,inner),df);lhs,right=rows[1][2].replace('&','').split('=');assert not lhs.strip() and eq(scalar(right),df);C['final_derivatives']+=1
 else:
  # Only two unrated originals have no worked solution; given functions still read.
  assert raw and t in ('q-11414','q-48850')
 vals=[scalar(v[':answer/value']) for v in q[':question/answer-fields'][0][':answer-field/choices']];field=q[':question/answer-fields'][0]
 if t=='q-342875':answer=s.diff(x**5-m['parameters']['c']*x**4,x)
 elif t=='q-342891':answer=-s.diff(2*x**4-x**2+m['parameters']['c'],x)/2
 else:answer=df
 if field[':answer-field/type']==':answer-field.type/blank':
  assert len(vals)==1 and '{{field-1}}' in prompt
  expression=prompt.split('\n\n',1)[1].replace('$','').replace('{{field-1}}',field[':answer-field/choices'][0][':answer/value']);lhs,rhs=expression.split('=');assert eq(scalar(rhs),df)
  if not raw:assert lhs.strip()==r'{f}^{′}(x)'
  assert eq(vals[0],answer);C['blank_fragments']+=1
 else:
  assert len(vals)==5 and sum(eq(v,answer) for v in vals)==1
  for a,b in itertools.combinations(vals,2):assert not eq(a,b);C['pairs']+=1
 if ':answer-field/correct' in field:assert eq(next(v for v,a in zip(vals,field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1]),answer)
 if not raw:
  if t=='authored-square':a,b=m['parameters']['a'],m['parameters']['b'];assert fun==(a*x+b)**2;expected=[df,2*(a*x+b),a*(a*x+b)**2,2*a*(a*x+b)**2,2*a*(a*x-b)]
  elif t=='q-107293':inner=3*x+m['parameters']['b'];expected=[df,5*inner**4,3*inner**5,3*inner**4,15*inner**5]
  elif t=='q-11414':c=m['parameters']['c'];inner=3*x**5-c*x**2;id=s.diff(inner,x);expected=[df,3*(5*x**5-2*c*x)*inner**2,-2*c*id*inner**2,3*id*inner**3,3*(5*x**4-2*c*x)*inner**2]
  elif t=='q-48850':c=m['parameters']['c'];inner=2*x**2+c*x;id=s.diff(inner,x);expected=[df,id/inner**s.Rational(3,2),-id/(2*inner**s.Rational(3,2)),-id/inner**s.Rational(2,3),-2*id/inner**s.Rational(3,2)]
  elif t=='q-71954':b=m['parameters']['b'];inner=8*x+b;expected=[32*(16*x+b)**3,16*inner**3,16*(16*x+b)**3,8*inner**3,df]
  elif t=='q-71956':b=m['parameters']['b'];inner=b-5*x;expected=[-15*(b+5*x)**2,-15*inner**3,15*(b+5*x)**2,15*inner**2,df]
  else:expected=[answer]
  assert all(sum(eq(v,e) for v in vals)==1 for e in expected);C['whole_banks']+=1
  domain=m['domain'];assert domain['real_x'];restriction=domain['restriction']
  if t in ('q-342883','q-48850'):
   assert restriction.endswith('>0');assert eq(scalar(restriction[:-2]),inner);assert all(float(inner.subs(x,n))>0 for n in (4,5,6))
  elif t=='q-342891':assert 'c-1/8>0' in restriction and m['parameters']['c']>=1
  else:assert restriction=='all real x'
  C['domains']+=1
 C['values']+=len(vals);C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for t,l in G.LEVELS.items():
 params=G.parameters_for(t)
 for p in (params[0],params[len(params)//2],params[-1]):check(G.generate(l,template=t,parameters=p))
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile']),True)
result=dict(status='passed',source=fidelity,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
