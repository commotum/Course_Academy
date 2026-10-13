"""Root independent integer-polynomial LCM and full printed method bank/stage checks."""
import importlib.util,json,re,math
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186152117;D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_lcm_scalar',P/'ode-scalar-parser.py');g=module('root_lcm_gen',D.with_suffix('.py'));x=p.x
C=dict(records=0,actual_polynomial_input_pairs=0,choices=0,whole_method_banks=0,exact_solution_equalities=0,actual_multiple_lists=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,raw_missing_assessments=0)
def scalar(z):
 z=z.strip().rstrip('.,:').replace(r'\,','');z=re.sub(r'\\[A-Za-z]+|[wyzt]',lambda m:'x' if len(m[0])==1 else m[0],z);return s.expand(p.scalar(z))
def lcm(a,b):
 if not (a.free_symbols|b.free_symbols):assert a.is_Integer and b.is_Integer;return s.Integer(math.lcm(abs(int(a)),abs(int(b))))
 a,b=s.Poly(a,x,domain=s.ZZ),s.Poly(b,x,domain=s.ZZ);v=a.lcm(b);return s.expand(v.as_expr()*s.sign(v.LC()))
def split(z):
 depth=0;out=[];start=0
 for i,c in enumerate(z):
  if c=='(':depth+=1
  if c==')':depth-=1
  if c==',' and depth==0:out.append(z[start:i]);start=i+1
 return out+[z[start:]]
def expr(z):
 z=z.strip().rstrip('.,:').replace(r'\,','')
 if z.startswith(r'\text{LCM}'):
  body=z[len(r'\text{LCM}'):];assert body[0]=='(' and body[-1]==')';a,b=split(body[1:-1]);return lcm(scalar(a),scalar(b))
 return scalar(z)
def same(a,b):assert s.expand(a-b)==0,(a,b)
def check(r):
 q=r['question'];parts=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem'],re.S);a,b=[scalar(v.rstrip('.')) for v in parts[:2]];assert a.free_symbols==b.free_symbols=={x}
 A,B=s.Poly(a,x,domain=s.ZZ),s.Poly(b,x,domain=s.ZZ);ac,bc=int(A.content()),int(B.content());n,m=A.degree(),B.degree();h=A.nth(n-1)/(A.LC()*n);hh=B.nth(m-1)/(B.LC()*m);assert A.LC()>0 and B.LC()>0 and h==hh and h.is_Integer and 1<=abs(h)<=9 and n!=m;F=x+h;same(a,ac*F**n);same(b,bc*F**m);wanted=lcm(a,b);N=max(n,m);same(wanted,math.lcm(ac,bc)*F**N);f=q[':question/answer-fields'][0];vals=[scalar(v[':answer/value']) for v in f.get(':answer-field/choices',[])];assert len(set(vals))==len(vals)
 if ':answer-field/correct' in f:
  good=[i for i,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1]];assert len(good)==1;same(vals[good[0]],wanted);assert sum(v==wanted for v in vals)==1
  level=q[':question/difficulty'].split('/')[-1];profile=r['generation']['profile']
  assert math.lcm(ac,bc)<=120
  if level=='easy':assert 2<=ac<=9 and 2<=bc<=9 and math.gcd(ac,bc)==1 and 2<=N<=5 and min(n,m)>=1
  elif level=='moderate':assert 2<=ac<=18 and 2<=bc<=18 and math.gcd(ac,bc)>1 and max(ac,bc)>=9 and 4<=N<=5 and min(n,m)>=2
  else:assert 8<=ac<=24 and 8<=bc<=24 and math.gcd(ac,bc)>1 and ac%bc and bc%ac and 6<=N<=9 and min(n,m)>=3
  bank_profile=r['generation']['bank_profile']
  if f[':answer-field/type'].endswith('/radio'):
   if bank_profile=='method_bank':bank=[wanted,math.lcm(ac,bc)*F**min(n,m),math.lcm(ac,bc)*F**(n+m),math.gcd(ac,bc)*F**N,s.Integer(math.lcm(ac,bc))]
   elif bank_profile=='retain_inputs':bank=[wanted,math.lcm(ac,bc)*F**(n+m),ac*F**N,bc*F**N,bc*F**m]
   elif bank_profile=='product_power':bank=[wanted,math.lcm(ac,bc)*F**(n+m),ac*bc*F**(n+m),math.lcm(ac,bc)*F**(2*N),ac*bc*F**N]
   else:raise AssertionError(bank_profile)
   assert set(vals)=={s.expand(z) for z in bank};C['whole_method_banks']+=1
  sol=q[':question/worked-solution'];spans=[a or b for a,b in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S)];eqs=[]
  for span in spans:
   for segment in span.split(r'\qquad'):
    if '=' in segment:
     sides=[expr(z) for z in segment.strip().strip(',').split('=')]
     for v in sides[1:]:same(v,sides[0]);C['exact_solution_equalities']+=1
     eqs.append(segment)
  assert len(eqs)==3
  actual_max=re.search(r'which is \$(.*?)\$',sol);assert actual_max is not None and scalar(actual_max[1])==N
  for num,listed in re.findall(r'- Multiples of \$(\d+):\$ \$([^$]+)\$',sol):
   n=int(num);items=[int(z) for z in re.findall(r'\d+',listed)];assert n in (ac,bc) and items==sorted(set(items)) and all(z%n==0 for z in items) and math.lcm(ac,bc) in items;C['actual_multiple_lists']+=1
 else:assert ':question/difficulty' not in q and ':question/worked-solution' not in q;C['raw_missing_assessments']+=1
 C['records']+=1;C['actual_polynomial_input_pairs']+=1;C['choices']+=len(vals);return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case.get('level',case.get('difficulty')),template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile'))));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_prompts']+=1;C['source_solutions']+=int(':question/worked-solution' in old)
 of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f.get(':answer-field/choices',[]))==sorted(z[':answer/value'] for z in of.get(':answer-field/choices',[]));C['source_values']+=len(of.get(':answer-field/choices',[]));C['source_banks']+=int(':answer-field/choices' in of)
 if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
review=json.loads((D/'review.json').read_text());review=review if isinstance(review,list) else [r for v in review.values() for r in v]
for item in review:check(item.get('record',item))
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for t,policy in g.TEMPLATES.items():
 for level in policy['levels']:
  for seed in range(35):check(g.generate(level,seed+780,template=t))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
