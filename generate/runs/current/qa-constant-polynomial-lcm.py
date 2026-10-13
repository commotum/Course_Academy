"""Root independent integer-polynomial LCM and full printed method bank/stage checks."""
import importlib.util,json,re,math
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186152116;D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_lcm_scalar',P/'ode-scalar-parser.py');g=module('root_lcm_gen',D.with_suffix('.py'));x=p.x
C=dict(records=0,actual_constant_multiple_inputs=0,choices=0,whole_method_banks=0,exact_solution_equalities=0,actual_multiple_lists=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,raw_missing_assessments=0)
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
 q=r['question'];parts=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem'],re.S);a,b=[scalar(v.rstrip('.')) for v in parts[:2]];assert a.free_symbols==b.free_symbols=={x};assert not s.cancel(a/b).free_symbols
 A,B=s.Poly(a,x,domain=s.ZZ),s.Poly(b,x,domain=s.ZZ);ac,bc=int(A.content()),int(B.content());F=A.primitive()[1].as_expr()*s.sign(A.LC());G=B.primitive()[1].as_expr()*s.sign(B.LC());same(F,G);wanted=lcm(a,b);same(wanted,math.lcm(ac,bc)*F);f=q[':question/answer-fields'][0];vals=[scalar(v[':answer/value']) for v in f.get(':answer-field/choices',[])];assert len(set(vals))==len(vals)
 if ':answer-field/correct' in f:
  good=[i for i,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1]];assert len(good)==1;same(vals[good[0]],wanted);assert sum(v==wanted for v in vals)==1
  level=q[':question/difficulty'].split('/')[-1];profile=r['generation']['profile']
  if level=='hard':
   z=s.Poly(F,x,domain=s.ZZ);assert z.degree()==2 and len(z.terms())==3 and z.content()==1 and 2<=z.LC()<=4 and 1<=abs(z.nth(1))<=9 and 1<=abs(z.nth(0))<=9
   assert min(A.LC(),B.LC())<0 and 2<=ac<=18 and 2<=bc<=18 and ac%bc and bc%ac and math.gcd(ac,bc)>1 and math.lcm(ac,bc)<=120
  elif level=='easy':assert math.gcd(ac,bc)==1 and 2<=ac<=9 and 2<=bc<=9 and math.lcm(ac,bc)<=72
  elif level=='moderate':assert math.gcd(ac,bc)>1 and math.lcm(ac,bc)<=120
  if f[':answer-field/type'].endswith('/radio') and profile in ('method_bank','content_bank'):
   if level=='hard':bank=[wanted,math.gcd(ac,bc)*F,ac*bc*F,F,math.lcm(ac,bc)*F**2]
   else:bank=[wanted,(ac+bc)*F,math.lcm(ac,bc)*F**2,s.Integer(math.lcm(ac,bc)),math.gcd(ac,bc)*F]
   assert set(vals)=={s.expand(z) for z in bank};C['whole_method_banks']+=1
  sol=q[':question/worked-solution'];spans=[a or b for a,b in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S)];eqs=[]
  for span in spans:
   for segment in span.split(r'\qquad'):
    if '=' in segment:
     sides=[expr(z) for z in segment.strip().strip(',').split('=')]
     for v in sides[1:]:same(v,sides[0]);C['exact_solution_equalities']+=1
     eqs.append(segment)
  assert len(eqs)==(5 if level=='hard' else 3)
  for num,listed in re.findall(r'- Multiples of \$(\d+):\$ \$([^$]+)\$',sol):
   n=int(num);items=[int(z) for z in re.findall(r'\d+',listed)];assert n in (ac,bc) and items==sorted(set(items)) and all(z%n==0 for z in items) and math.lcm(ac,bc) in items;C['actual_multiple_lists']+=1
 else:assert ':question/difficulty' not in q and ':question/worked-solution' not in q;C['raw_missing_assessments']+=1
 C['records']+=1;C['actual_constant_multiple_inputs']+=1;C['choices']+=len(vals);return q
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
