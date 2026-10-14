"""Root parses displayed ODE RHSs and every scaling/witness equality."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186087888;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
P=module('root_hom_scalar',R/'ode-scalar-parser.py');G=module('root_hom_generator',D.with_suffix('.py'));F=module('root_hom_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
X,Y,T=s.symbols('x y t',positive=True)
def scalar(t,f=None):
 t=t.strip().rstrip('.,');t=re.sub(r'\\text\{\s*\}','',t)
 functions=re.findall(r'f\(([^()]*)\)',t)
 if functions:
  assert len(functions)==1 and f is not None
  a,b=map(scalar,functions[0].split(','));value=f.subs({X:a,Y:b},simultaneous=True);t=re.sub(r'f\([^()]*\)','v',t)
  return P.scalar(t).subs({P.x:X,P.y:Y,P.t:T,P.v:value},simultaneous=True)
 return P.scalar(t).subs({P.x:X,P.y:Y,P.t:T},simultaneous=True)
def zero(t):return s.cancel(s.expand_log(t,force=False))==0
def spans(t):return re.findall(r'\$\$.*?\$\$|\$[^$]+\$',t,re.S)
C=dict(records=0,displayed_functions=0,criterion_euler_tests=0,criterion_scaling_tests=0,whole_equation_pairs=0,function_definitions=0,operative_scaling_sides=0,numerical_witness_sides=0,degree_claims=0)
records=json.loads((R/f'qa/{K}-sampled.json').read_text())
for row in json.loads((D/'review.json').read_text()):
 r=row.get('record',row)
 if 'question' in r and not r['generation'].get('evidence_only') and r['generation'].get('profile')!='raw':records.append(r)
for r in records:
 q,meta=r['question'],r['generation'];sol=q[':question/worked-solution'];is_not='NOT' in q[':question/problem'];fs=q[':question/answer-fields'];assert len(fs)==1
 field=fs[0];bank=[scalar(a[':answer/value'].split('=',1)[1]) for a in field[':answer-field/choices']];truth=[]
 for value in bank:
  euler=zero(X*s.diff(value,X)+Y*s.diff(value,Y));scaling=zero(value.subs({X:T*X,Y:T*Y},simultaneous=True)-value);assert euler==scaling;truth.append(euler!=is_not);C['criterion_euler_tests']+=1;C['criterion_scaling_tests']+=1
 for a,b in itertools.combinations(bank,2):assert not zero(a-b);C['whole_equation_pairs']+=1
 assert sum(truth)==1;chosen=truth.index(True);assert field[':answer-field/choices'][chosen][':answer/id']==field[':answer-field/correct'][1];f=bank[chosen];C['displayed_functions']+=5
 assert '**Method 1**' in sol and '**Method 2**' in sol
 for span in spans(sol):
  text=span.strip('$').strip()
  if text.startswith('f(x,y)='):
   for part in text.split('=')[1:]:assert zero(scalar(part,f)-f);C['function_definitions']+=1
  elif text.startswith(r'\frac{\text{d}y}{\text{d}x}='):assert zero(scalar(text.split('=',1)[1],f)-f);C['function_definitions']+=1
 blocks=re.findall(r'\$\$\s*\\begin\{aligned\}(.*?)\\end\{aligned\}\s*\$\$',sol,re.S)
 witness=re.search(r'For \$x=(\d+)\$, \$y=(\d+)\$ and \$t=(\d+)\$',sol)
 if witness:
  assert len(blocks)==2;u,v,t=map(s.Integer,witness.groups());expected=[f.subs({X:t*u,Y:t*v}),f.subs({X:u,Y:v})];assert not zero(expected[0]-expected[1])
  for block,value in zip(blocks,expected):
   rows=block.split(chr(92)*2)
   for index,row in enumerate(rows):
    pieces=row.replace('&','').split('=');parts=pieces[1:]
    if index==0:assert pieces[0].strip() in ('f(tx,ty)','f(x,y)')
    else:assert not pieces[0].strip()
    for part in parts:assert zero(scalar(part,f)-value),(meta['template'],part,value);C['numerical_witness_sides']+=1
  numerator,denominator=s.fraction(s.cancel(f));assert s.Poly(numerator,X,Y).total_degree()==2 and {sum(mon) for mon,_ in s.Poly(numerator,X,Y).terms()}=={0,2};assert {sum(mon) for mon,_ in s.Poly(denominator,X,Y).terms()}=={2};assert s.Poly(s.gcd(numerator,denominator),X,Y).total_degree()==0;C['degree_claims']+=2
 else:
  assert len(blocks)==1;expected=f.subs({X:T*X,Y:T*Y},simultaneous=True)
  for index,row in enumerate(blocks[0].split(chr(92)*2)):
   pieces=row.replace('&','').split('=')
   if index==0:assert pieces[0].strip()=='f(tx,ty)'
   else:assert not pieces[0].strip()
   for part in pieces[1:]:assert zero(scalar(part,f)-expected),(meta['template'],part,expected);C['operative_scaling_sides']+=1
 C['records']+=1
result={'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0}
(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
