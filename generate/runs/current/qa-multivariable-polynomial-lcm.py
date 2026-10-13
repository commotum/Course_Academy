"""Root derives multivariable LCM, whole banks and every actual solution stage."""
import importlib.util,json,re,math
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186152118;D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_multilcm_scalar',P/'ode-scalar-parser.py');g=module('root_multilcm_gen',D.with_suffix('.py'));x,y=p.x,p.y
C=dict(records=0,actual_polynomial_pairs=0,choices=0,whole_banks=0,solution_equalities=0,prose_maxima=0,numeric_multiple_lists=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,raw_missing_assessments=0)
def scalar(z,letters):
 z=z.strip().rstrip('.,:').replace(r'\,','');z=re.sub(r'\\[A-Za-z]+|[xyzwuv]',lambda m:str(letters[m[0]]) if len(m[0])==1 else m[0],z);return s.expand(p.scalar(z))
def lcm(a,b):
 if not (a.free_symbols|b.free_symbols):assert a.is_Integer and b.is_Integer;return s.Integer(math.lcm(abs(int(a)),abs(int(b))))
 v=s.Poly(a,x,y,domain=s.ZZ).lcm(s.Poly(b,x,y,domain=s.ZZ));return s.expand(v.as_expr()*s.sign(v.LC()))
def split(z):
 dep=0;start=0;out=[]
 for i,c in enumerate(z):
  dep+=(c=='(')-(c==')')
  if c==',' and dep==0:out.append(z[start:i]);start=i+1
 return out+[z[start:]]
def expr(z,L):
 z=z.strip().rstrip('.,:').replace(r'\,','')
 if z.startswith(r'\text{LCM}'):
  body=z[len(r'\text{LCM}'):];assert body[0]=='(' and body[-1]==')';a,b=split(body[1:-1]);return lcm(scalar(a,L),scalar(b,L))
 return scalar(z,L)
def same(a,b):assert s.expand(a-b)==0,(a,b)
def factors(v):
 c,fs=s.factor_list(v,x,y);assert c.is_Integer and c>=2 and len(fs)==2
 out={}
 for f,n in fs:
  assert len(f.free_symbols)==1;axis=next(iter(f.free_symbols));assert axis in (x,y) and axis not in out;h=f.subs(axis,0);same(f,axis+h);assert h.is_Integer and abs(h)<=9;out[axis]=(f,n,h)
 assert set(out)=={x,y};return int(c),out

def check(r):
 q=r['question'];spans=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem'],re.S);Araw,Braw=spans[:2]
 actual=list(dict.fromkeys(re.findall('[xyzwuv]',re.sub(r'\\[A-Za-z]+','',Araw+Braw))));assert len(actual)==2;L=dict(zip(actual,(x,y)));a,b=scalar(Araw,L),scalar(Braw,L);ac,af=factors(a);bc,bf=factors(b);assert ac!=bc
 for axis in (x,y):assert af[axis][0]==bf[axis][0]
 F,G=af[x][0],af[y][0];n,q0=af[x][1],af[y][1];m,s0=bf[x][1],bf[y][1];E,H=max(n,m),max(q0,s0);lo,hi=min(n,q0,m,s0),max(n,q0,m,s0);ell=math.lcm(ac,bc);wanted=lcm(a,b);same(wanted,ell*F**E*G**H);assert af[x][2] or af[y][2]
 field=q[':question/answer-fields'][0];vals=[scalar(v[':answer/value'],L) for v in field[':answer-field/choices']];assert len(set(vals))==len(vals)
 if ':answer-field/correct' in field:
  good=[i for i,z in enumerate(field[':answer-field/choices']) if z[':answer/id']==field[':answer-field/correct'][1]];assert len(good)==1;same(vals[good[0]],wanted);assert sum(z==wanted for z in vals)==1
  level=q[':question/difficulty'].split('/')[-1];profile=r['generation']['bank'];assert (n,q0)!=(m,s0)
  if level=='easy':assert max(ac,bc)<=9 and math.gcd(ac,bc)==1 and ell<=60 and hi<=5
  elif level=='moderate':assert 4<=min(ac,bc) and max(ac,bc)<=20 and max(ac,bc)>=9 and math.gcd(ac,bc)>1 and ac%bc and bc%ac and ell<=120 and 3<=hi<=6
  else:assert 12<=min(ac,bc) and max(ac,bc)<=30 and math.gcd(ac,bc)>1 and ac%bc and bc%ac and 120<ell<=180 and lo>=2 and 7<=hi<=9
  sol=q[':question/worked-solution'];maths=[a or b for a,b in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S)];eqs=[]
  for z in maths:
   if '=' in z:
    vs=[expr(v,L) for v in z.split('=')]
    for v in vs[1:]:same(v,vs[0]);C['solution_equalities']+=1
    eqs.append(z)
  assert len(eqs)==3
  for num,listed in re.findall(r'- Multiples of \$(\d+):\$ \$([^$]+)\$',sol):
   num=int(num);items=[int(v) for v in re.findall(r'\d+',listed)];assert num in (ac,bc) and items==sorted(set(items)) and all(v%num==0 for v in items) and ell in items;C['numeric_multiple_lists']+=1
  maxima=re.findall(r'- For \$(.*?)\$ and \$(.*?)\$ the largest power is \$(.*?)\$',sol);assert len(maxima)==2
  for left,right,power in maxima:
   lft,rgt=scalar(left,L),scalar(right,L);axis=next(iter(lft.free_symbols));assert lft.free_symbols==rgt.free_symbols=={axis};assert lft==s.expand(af[axis][0]**af[axis][1]) and rgt==s.expand(bf[axis][0]**bf[axis][1]);assert scalar(power,L)==max(af[axis][1],bf[axis][1]);C['prose_maxima']+=1
 else:assert ':question/difficulty' not in q and ':question/worked-solution' not in q;C['raw_missing_assessments']+=1
 profile=r['generation']['bank']
 if field[':answer-field/type'].endswith('/radio'):
  if profile=='method_bank':bank=[wanted,ell*F**min(n,m)*G**min(q0,s0),math.gcd(ac,bc)*F**E*G**H,ell*F**(n+m)*G**(q0+s0),ell*F**H*G**E]
  elif profile=='product_sum_swap':bank=[ell*F**(n+m)*G**(q0+s0),wanted,ac*bc*F**E*G**H,ac*bc*F**(n+m)*G**(q0+s0),ell*F**H*G**E]
  elif profile=='opaque_patterns':bank=[s.Rational(3,2)*ell*F**min(n,m)*G**H,ell*F**(2*n)*G**(q0+s0),wanted,ell*F**min(n,m)*G**H,s.Rational(3,2)*ell*F**min(n,m)*G**(H+1)]
  else:raise AssertionError(profile)
  assert set(vals)=={s.expand(v) for v in bank};C['whole_banks']+=1
 C['records']+=1;C['actual_polynomial_pairs']+=1;C['choices']+=len(vals);return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile'))));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_prompts']+=1;C['source_solutions']+=int(':question/worked-solution' in old)
 of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);C['source_values']+=len(of[':answer-field/choices']);C['source_banks']+=1
 if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
review=json.loads((D/'review.json').read_text());review=review if isinstance(review,list) else [r for v in review.values() for r in v]
for item in review:check(item.get('record',item))
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for t,policy in g.TEMPLATES.items():
 for level in policy['levels']:
  for seed in range(25):check(g.generate(level,seed+1270,template=t))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
