"""Root independently reads actual three-polynomial LCM tasks and all solution stages."""
import importlib.util,json,re,math,itertools
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186152119;D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_triple_scalar',P/'ode-scalar-parser.py');g=module('root_triple_gen',D.with_suffix('.py'));x,y=p.x,p.y
C=dict(records=0,actual_polynomial_triples=0,choices=0,whole_banks=0,solution_equalities=0,prose_maxima=0,numeric_multiple_lists=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,raw_missing_assessments=0,normal_typo_repairs=0)
def scalar(z,L):
 z=z.strip().rstrip('.,:').replace(r'\,','');z=re.sub(r'\\[A-Za-z]+|[xyuv]',lambda m:str(L[m[0]]) if len(m[0])==1 else m[0],z);return s.expand(p.scalar(z))
def split(z):
 dep=0;start=0;out=[]
 for i,c in enumerate(z):
  dep+=(c=='(')-(c==')')
  if c==',' and dep==0:out.append(z[start:i]);start=i+1
 return out+[z[start:]]
def lcm(vals):
 if not set().union(*(a.free_symbols for a in vals)):return s.Integer(math.lcm(*(abs(int(a)) for a in vals)))
 z=s.Poly(vals[0],x,y,domain=s.ZZ)
 for a in vals[1:]:z=z.lcm(s.Poly(a,x,y,domain=s.ZZ))
 return s.expand(z.as_expr()*s.sign(z.LC()))
def expr(z,L):
 z=z.strip().rstrip('.,:').replace(r'\,','')
 if z.startswith(r'\text{LCM}'):
  body=z[len(r'\text{LCM}'):];assert body[0]=='(' and body[-1]==')';return lcm([scalar(v,L) for v in split(body[1:-1])])
 return scalar(z,L)
def same(a,b):assert s.expand(a-b)==0,(a,b)
def check(r):
 q=r['question'];spans=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem'],re.S);raw=[]
 for z in spans:raw.extend(a.strip().rstrip('.,') for a in split(z.replace(r"\,","")) if a.strip().rstrip('.,'))
 raw=raw[:3];assert len(raw)==3
 actual=list(dict.fromkeys(re.findall('[xyuv]',re.sub(r'\\[A-Za-z]+','',','.join(raw)))));assert 1<=len(actual)<=2;L=dict(zip(actual,(x,y)));inputs=[scalar(v,L) for v in raw];wanted=lcm(inputs);coeff=[];fd=[]
 for a in inputs:
  c,fs=s.factor_list(a,x,y);assert c.is_Integer and c>=2;coeff.append(int(c));dic={}
  for f,n in fs:
   assert len(f.free_symbols)==1;v=next(iter(f.free_symbols));same(f,v+f.subs(v,0));assert f.subs(v,0).is_Integer and abs(f.subs(v,0))<=9;dic[f]=n
  fd.append(dic)
 bases=sorted(fd[0],key=str);assert all(set(a)==set(bases) for a in fd);powers=[[a[f] for f in bases] for a in fd];mx=[max(a[j] for a in powers) for j in range(len(bases))];mn=[min(a[j] for a in powers) for j in range(len(bases))];sm=[sum(a[j] for a in powers) for j in range(len(bases))];ell=math.lcm(*coeff)
 def value(c,e):return s.expand(c*s.prod(f**n for f,n in zip(bases,e)))
 same(wanted,value(ell,mx));meta=r['generation'];profile=meta['bank_profile'];f=q[':question/answer-fields'][0];vals=[scalar(v[':answer/value'],L) for v in f.get(':answer-field/choices',[])];assert len(set(vals))==len(vals)
 if ':answer-field/correct' not in f:
  assert ':answer-field/choices' not in f and ':question/difficulty' not in q and ':question/worked-solution' not in q and meta['evidence_only'] and not meta['eligible_for_learning'];C['raw_missing_assessments']+=1
 else:
  good=next(v for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1]);same(scalar(good[':answer/value'],L),wanted);assert sum(z==wanted for z in vals)==1
  level=q[':question/difficulty'].split('/')[-1];assert len(bases)==dict(easy=1,moderate=2,hard=3)[level] and max(coeff)<=(12 if level=='easy' else 20) and ell<=(60 if level=='easy' else 120)
  assert all(1<=n<=(7 if level=='moderate' else 5) for a in powers for n in a) and all(len({a[j] for a in powers})>=2 for j in range(len(bases)))
  if level=='hard':assert len(actual)==2 and all(f.subs(next(iter(f.free_symbols)),0)!=0 for f in bases) and len({next(i for i,a in enumerate(powers) if a[j]==mx[j]) for j in range(3)})==3 and all(sum(a[j]==mx[j] for a in powers)==1 for j in range(3))
  sol=q[':question/worked-solution'];maths=[a or b for a,b in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S)];eqs=[]
  for z in maths:
   if '=' in z:
    z=z.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').replace(r'\\','');vs=[expr(v,L) for v in z.split('=')]
    for v in vs[1:]:same(v,vs[0]);C['solution_equalities']+=1
    eqs.append(z)
  assert len(eqs)==3
  lists=re.findall(r'- Multiples of \$(\d+):\$ \$([^$]+)\$',sol);assert len(lists)==3
  for num,listed in lists:
   num=int(num);items=[int(v) for v in re.findall(r'\d+',listed)];assert num in coeff and items==sorted(set(items)) and all(v%num==0 for v in items) and ell in items;C['numeric_multiple_lists']+=1
  if len(bases)==1 and '- For ' not in sol:
   references=re.findall(r'we raise \$(.*?)\$ to the largest power.*?which is \$(.*?)\$',sol,re.S);assert len(references)==1;fac,power=references[0];assert scalar(fac,L)==bases[0] and scalar(power,L)==mx[0];C['prose_maxima']+=1
  else:
   maxima=re.findall(r'- For (.*?) the largest power is \$(.*?)\$',sol);assert len(maxima)==len(bases)
   for operands,maximum in maxima:
    rawvalues=[]
    for span in re.findall(r'\$(.*?)\$',operands):rawvalues.extend(v for v in split(span.replace(r'\,','')) if v.strip())
    assert len(rawvalues)==3;vs=[scalar(v,L) for v in rawvalues];hits=[j for j,factor in enumerate(bases) if all(z==s.expand(factor**powers[i][j]) for i,z in enumerate(vs))];assert len(hits)==1 and scalar(maximum,L)==mx[hits[0]];C['prose_maxima']+=1
  if f[':answer-field/type'].endswith('/radio'):
   if profile.startswith('authored-'):bank=[wanted,value(math.gcd(*coeff),mx),value(math.prod(coeff),mx),value(ell,mn),value(ell,sm)]
   else:
    # Explicit source pattern order must use actual printed variable/factor order.
    srcbases=[]
    for axis in (x,y):srcbases.extend(fac for fac in bases if axis in fac.free_symbols)
    e=[[a[fac] for fac in srcbases] for a in fd];M=[max(a[j] for a in e) for j in range(len(bases))];N=[min(a[j] for a in e) for j in range(len(bases))];S=[sum(a[j] for a in e) for j in range(len(bases))]
    def observed(c,pows):return s.expand(c*s.prod(fac**n for fac,n in zip(srcbases,pows)))
    if profile=='observed-q-76247':bank=[wanted,observed(2*ell,M),observed(ell,[2*e[1][0]]),observed(2*ell,[2*e[1][0]]),observed(max(coeff)**2,S)]
    elif profile=='observed-q-112230':part=math.lcm(coeff[0],coeff[1]);ss=[S[0],S[1]-1];bank=[wanted,observed(part,M),observed(ell+part,M),observed(ell,ss),observed(ell+part,ss)]
    elif profile=='observed-q-76475':bank=[wanted,observed(2*ell,N),observed(2*ell,M),observed(ell,S),observed(ell,N)]
    else:raise AssertionError(profile)
   assert set(vals)==set(bank);C['whole_banks']+=1
 C['records']+=1;C['actual_polynomial_triples']+=1;C['choices']+=len(vals);return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_prompts']+=1;C['source_solutions']+=int(':question/worked-solution' in old);of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f.get(':answer-field/choices',[]))==sorted(z[':answer/value'] for z in of.get(':answer-field/choices',[]));C['source_values']+=len(of.get(':answer-field/choices',[]));C['source_banks']+=int(':answer-field/choices' in of)
 if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
review=json.loads((D/'review.json').read_text());review=review if isinstance(review,list) else [r for v in review.values() for r in v]
for item in review:check(item.get('record',item))
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for name,(level,kind,n) in g.TEMPLATES.items():
 for seed in range(25):check(g.generate(level,seed+381,template=name))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
