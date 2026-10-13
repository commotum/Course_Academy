"""Root independent whole-model, bank and printed-stage oracle, basis1356."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','scalar');U,K,A=p.u,p.k,p.z

def val(text,var=None):
 text=text.strip().rstrip('.,').replace(r'\,','')
 if var:text=text.replace('{'+var+'}_{0}','v').replace(var,'u')
 text=re.sub(r'(?<![A-Za-z])a(?![A-Za-z])','z',text)
 return s.expand(p.scalar(text))

def equation(text):
 text=text.strip().rstrip('.,').replace(r'\text{d}','d').replace(r'\textrm d ','d').replace(' ','')
 m=re.fullmatch(r'\\(?:d?frac)\{d([A-Za-z])\}\{dt\}=(.*)',text);assert m,text
 var=m[1];parts=m[2].split(r',\,');chain=[val(t,var) for t in parts[0].split('=')]
 assert all(s.expand(z-chain[0])==0 for z in chain),text
 initial=None
 if len(parts)>1:
  assert len(parts)==2
  z=re.fullmatch(var+r'\(0\)=(.*)',parts[1]);assert z,text;initial=val(z[1],var);assert initial.is_number or initial==p.v
 return var,chain[0],initial,len(chain)-1

def equal(x,y):return x[0]==y[0] and s.expand(x[1]-y[1])==0 and x[2]==y[2]
def recognition_good(o,cap):
 _,rhs,n,_=o
 if s.degree(rhs,U)!=1:return False
 b=rhs.coeff(U);c=rhs.subs(U,0)
 return bool(b<0 and c>0 and (n<-c/b if n is not None else -c/b==cap))

def check(r,kp,n):
 q=r['question'];gm=r['generation'];prompt=q[':question/problem'];fields=q[':question/answer-fields']
 raw=gm['profile'].startswith('observed_');assert gm['evidence_only']==raw or kp==17592186124674
 assert gm['eligible_for_learning']==(not gm['evidence_only'])
 if kp==17592186124673:
  m=re.search(r'\$y\s*<\s*([\d.]+)\$',prompt);cap=val(m[1]) if m else None
 else:
  symbol=re.search(r'\$([A-Z])\(t\)\$',prompt)[1]
  m=re.search(r'maximum[^$]*?is \$(\d+)\$',prompt);assert m,prompt;cap=s.Integer(m[1])
  rate=re.search(r'rate of increase equals \$(.*?)\$ times',prompt);rate=val(rate[1]) if rate else K
  expected=s.expand(rate*(cap-U))
 for f in fields:
  options=[equation(a[':answer/value']) for a in f[':answer-field/choices']];assert len(options)==5
  assert all(not equal(a,b) for ix,a in enumerate(options) for b in options[:ix])
  good=[ix for ix,o in enumerate(options) if recognition_good(o,cap)] if kp==17592186124673 else [ix for ix,o in enumerate(options) if o[0]==symbol and o[2] is None and s.expand(o[1]-expected)==0]
  assert len(good)==1,(prompt,options,good)
  if ':answer-field/correct' in f:assert f[':answer-field/correct'][1]==f[':answer-field/choices'][good[0]][':answer/id']
  n['choices']+=5
  if not raw:
   actual=[z[1] for z in options];goodrhs=options[good[0]][1];b=goodrhs.coeff(U);c=goodrhs.subs(U,0)
   if kp==17592186124673 and cap is not None:
    k=-b;a=cap
    bank=[-k*(U+a),a*(U+k),a*(U-k),k*(a-U),k*(U-a)] if gm['template']=='factored_equation' else [k-k*a*U,k*U-k*a,k*a-k*U,k*U**2-k*a,k*a-k*U**2]
   elif kp==17592186124674:
    initial=re.search(r'(?:initially (?:contains|has)|currently has|initially houses) \$(\d+)\$',prompt);I=int(initial[1]) if initial else None
    if rate==K:bank=[K*(cap-U),-K*(cap-U),K*U*(cap-U),K*U**2*(cap-U),-K*(cap+U)]
    elif q[':question/difficulty'].endswith('/moderate'):bank=[rate*(cap-U),cap-U,-rate*(cap-U),rate*(I-U),rate*cap-U]
    else:bank=[rate*(cap-U),(cap-U)/rate,s.numer(rate)*(cap-U),rate*cap-U,rate*(I-U)]
   else:bank=None
   # Repaired observed profiles retain full evidence bank, not authored defaults.
   if kp==17592186124674 and gm['profile'].startswith('repaired_'):bank=None
   if bank is not None:
    assert all(sum(s.expand(z-e)==0 for z in actual)==1 for e in bank),(actual,bank);n['whole_operation_banks']+=1
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
  for ix,block in enumerate(blocks):
   o=equation(block);n['printed_equalities']+=o[3]+1
   if ix==0:assert s.expand(o[1]-K*(A-U))==0
   elif kp==17592186124674:assert s.expand(o[1]-expected)==0
   else:assert any(o[0]==z[0] and s.expand(o[1]-z[1])==0 and (o[2] is None or o[2]==z[2]) for z in options),block
  if kp==17592186124673:
   for lhs,rhs in re.findall(r'\$\{[yP]\}_\{0\}=([^>$]+)>a=([^,$]+)',sol):assert val(lhs)>val(rhs)
  else:
   if not gm['profile'].startswith(('observed_','repaired_')):
    m=re.search(r'\$a=(\d+)',sol);assert m and int(m[1])==cap
    if rate!=K:assert val(re.search(r'\$k=(.*?)\$',sol)[1])==rate
 n['records']+=1

for kp in (17592186124673,17592186124674):
 D=ROOT/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'g'+str(kp));n=dict(records=0,choices=0,whole_operation_banks=0,printed_equalities=0,source_exact_banks=0,source_exact_solutions=0,changed_public_profiles=0)
 cases=json.loads((D/'source-cases.json').read_text());old={q[':question/math-academy-id']:q for q in json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions']}
 for c in cases:
  r=g.generate(c['level'],parameters=c['parameters'],profile=c['bank_profile']);check(r,kp,n);q=r['question'];o=old[c['source_id']]
  assert q[':question/problem']==o[':question/problem']
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in o)
  if ':question/worked-solution' in o:assert o[':question/worked-solution']==q[':question/worked-solution'];n['source_exact_solutions']+=1
  for sf,gf in zip(o[':question/answer-fields'],q[':question/answer-fields']):
   assert sorted(z[':answer/value'] for z in sf[':answer-field/choices'])==sorted(z[':answer/value'] for z in gf[':answer-field/choices']);n['source_exact_banks']+=1
   assert (':answer-field/correct' in sf)==(':answer-field/correct' in gf)
   if ':answer-field/correct' in sf:assert sf[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in gf[':answer-field/choices'] if z[':answer/id']==gf[':answer-field/correct'][1])
  z=g.generate(c['level'],seed=2049,profile=c['bank_profile']);check(z,kp,n);assert z['question']!=q;n['changed_public_profiles']+=1
 for l in ('easy','moderate','hard'):
  seen=set()
  for seed in range(48):
   r=g.generate(l,seed+4000);check(r,kp,n);seen.add(r['generation']['mathematical_fingerprint'])
   z=g.generate(l,seed+8000,template=r['generation']['template'],profile=r['generation']['profile'],parameters=r['generation']['parameters']);assert z['question'][':question/id']==r['question'][':question/id']
  assert len(seen)>=20,(l,len(seen));n[l+'_meaningful_sample']=len(seen)
 review=json.loads((D/'review.json').read_text())
 for r in review:check(r.get('record',r),kp,n)
 if kp==17592186124673:
  r=g.generate('hard',template='expanded_ivp',seed=19);params=r['generation']['parameters']
  good=next(i for i,o in enumerate(params['options']) if s.Rational(o['b'])<0 and s.Rational(o['initial'])<-s.Rational(o['c'])/s.Rational(o['b']))
  bad=next(i for i,o in enumerate(params['options']) if s.Rational(o['b'])<0 and i!=good);o=params['options'][bad];o['initial']=str(-s.Rational(o['c'])/s.Rational(o['b']))
  try:g.generate('hard',template='expanded_ivp',profile=r['generation']['profile'],parameters=params)
  except ValueError:n['above_capacity_boundary_rejected']=True
  else:raise AssertionError('equilibrium admitted as above-cap distractor')
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(kp,n)
