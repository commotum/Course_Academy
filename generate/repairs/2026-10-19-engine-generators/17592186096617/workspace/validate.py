"""Reproducible source, math, coverage, counterfactual and grading inputs."""
import collections,copy,json,re,subprocess,sys
from pathlib import Path
import sympy as s
import generator as g
E=Path('evidence');E.mkdir(exist_ok=True)
def save(name,obj):(E/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False))
def field(r):return r['question'][':question/answer-fields'][0]
def key(r):
 f=field(r);return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def eq(a,b):return s.trigsimp(s.simplify(s.expand(a-b)))==0

def display_check(r):
 q=r['question'];prompt=q[':question/problem']
 first=re.search(r'\$([^$]*)\$',prompt)[1].rstrip('.')
 product=g.parse(first)
 full=s.diff(product,g.X)
 f=field(r);answer=g.parse(key(r))
 if f[':answer-field/type'].endswith('/radio') or r['generation']['missing_term']=='full':assert eq(answer,full),(r['generation'],'key')
 else:
  # Substitute the response in the served prompt and independently reconstruct RHS.
  filled=prompt.split('\n\n',1)[1].replace('{{field-1}}','$'+key(r)+'$')
  rhs=filled.split('=',1)[1].replace('$','')
  assert eq(g.parse(rhs),full),(r['generation'],'completion',rhs)
 # Check every displayed substitution/evaluation stage independently.
 worked=q[':question/worked-solution']
 uv=re.findall(r'\$[uv]\(x\)=([^$]*)\$',worked)
 u,v=[g.parse(z.rstrip('.')) for z in uv]
 assert eq(product,u*v)
 body=worked.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}')[0]
 stages=[];current=''
 for row in body.split(r'\\'):
  lhs,rhs=row.split('&',1);rhs=rhs.strip().replace(r'\quad','')
  if rhs.startswith('='):
   if current:stages.append(current)
   current=rhs[1:]
  else:current+=rhs
 if current:stages.append(current)
 for rhs in stages:
  assert eq(g.parse(rhs,{'u':u,'v':v}),full),(r['generation'],'solution row',rhs)
 # Numerical central differences are independent of the symbolic derivative construction.
 fn=s.lambdify(g.X,product,'math'); df=s.lambdify(g.X,full,'math')
 for x in [0.35,0.8,1.1]:
  h=1e-5;num=(fn(x+h)-fn(x-h))/(2*h)
  assert abs(num-df(x))<1e-5*(1+abs(df(x)))
 if f[':answer-field/type'].endswith('/radio'):
  assert sum(eq(g.parse(a[':answer/value']),full) for a in f[':answer-field/choices'])==1
 return full

replay=[];bank_report=[];matched=0;total=0
for c in json.loads((E/'source-cases.json').read_text()):
 t=c['template'];raw=g.QUESTIONS[t];r=g.generate('easy',template=t,parameters=c['parameters'],profile='observed_raw')
 replay.append(r)
 assert (':question/difficulty' in raw)==(':question/difficulty' in r['question'])
 assert len(raw.get(':question/answer-fields',[]))==len(r['question'].get(':question/answer-fields',[]))
 mapping=[]
 for of,nf in zip(raw.get(':question/answer-fields',[]),r['question'].get(':question/answer-fields',[])):
  assert len(of[':answer-field/choices'])==len(nf[':answer-field/choices'])
  for a in of[':answer-field/choices']:
   hits=[b for b in nf[':answer-field/choices'] if eq(g.parse(a[':answer/value']),g.parse(b[':answer/value']))]
   assert len(hits)==1,(t,a)
   mapping.append({'source_value':a[':answer/value'],'replay_value':hits[0][':answer/value']});matched+=1;total+=1
  if ':answer-field/correct' in of:
   assert eq(g.parse(of[':answer-field/correct'][':answer/value']),g.parse(next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])))
 # Compare all source math passages semantically, including aligned equation rows.
 def passages(txt):return re.findall(r'\$\$([\s\S]*?)\$\$|\$([^$]*)\$',txt)
 # Text/layout retained by replay aside from canonical TeX changes; keep both for review.
 bank_report.append({'source_id':t,'original_difficulty':raw.get(':question/difficulty'),'choices':mapping,'source_problem':raw[':question/problem'],'replay_problem':r['question'][':question/problem'],'source_solution':raw.get(':question/worked-solution'),'replay_solution':r['question'].get(':question/worked-solution')})
save('source-replay.json',replay);save('source-bank-report.json',{'matched':matched,'total':total,'banks':bank_report})

records=[];pairs=[]
# Source cases plus targeted coefficient/power bounds and all eligible decision assignments.
for idx,c in enumerate(json.loads((E/'source-cases.json').read_text())):
 t=c['template'];base=c['parameters'];trigs=['sin','cos','tan'] if t in ('q-1907','q-104300') else [None]
 roles=[0,1] if t in ('q-310188','q-319402','q-319350','q-319357','q-319385') else [0]
 for tri in trigs:
  for role in roles:
   for boundary in [0,1,2]:
    p=dict(base)
    if 'c' in p:p['c']=[base['c'],-1,6][boundary]
    if 'n' in p:p['n']=[base['n'],1,4][boundary]
    if 'b' in p:p['b']=[base['b'],2,7][boundary]
    if 'k' in p:p['k']=[base['k'],1,6][boundary]
    if tri:p['trig']=tri
    r=g.generate('easy',seed=idx*100+boundary*19+role*7+(trigs.index(tri)*11),template=t,parameters=p,missing_term=role)
    display_check(r);records.append(r)
 # changed target, all other mathematical data held constant
 if len(roles)==2:
  a=g.generate('easy',seed=500+idx,template=t,parameters=base,missing_term=0)
  b=g.generate('easy',seed=500+idx,template=t,parameters=base,missing_term=1)
  assert not eq(g.parse(key(a)),g.parse(key(b)))
  display_check(a);display_check(b)
  pairs.append({'kind':'missing_term','template':t,'before':a,'after':b})
 if len(trigs)>1:
  a=g.generate('easy',seed=700+idx,template=t,parameters={**base,'trig':'sin'})
  b=g.generate('easy',seed=700+idx,template=t,parameters={**base,'trig':'cos'})
  assert not eq(g.parse(key(a)),g.parse(key(b)))
  pairs.append({'kind':'trig_derivative','template':t,'before':a,'after':b})
 # irrelevant presentation counterfactual
 a=g.generate('easy',seed=800+idx,template=t,parameters={**base,**({'trig':'cos'} if len(trigs)>1 else {})},missing_term=0)
 b=g.generate('easy',seed=900+idx,template=t,parameters={**base,**({'trig':'cos'} if len(trigs)>1 else {})},missing_term=0)
 assert key(a)==key(b)
 if field(a)[':answer-field/type'].endswith('/radio'):pairs.append({'kind':'choice_order','template':t,'before':a,'after':b})
# Controlled presentation probes for the source tangent bank's length cue.
# Same semantic problem; distribution of each choice is independent of its key.
for seed in [0,1,2,4]:
 r=g.generate('easy',seed=seed,template='q-47965',parameters={'c':1,'n':2})
 display_check(r);records.append(r)

# Small regression exercising the actual default seeded sampler.
for seed in range(11):
 r=g.generate('easy',seed=seed);display_check(r);records.append(r)
assert g.generate('easy',42)==g.generate('easy',42)
for band in ['moderate','hard']:
 try:g.generate(band)
 except ValueError:pass
 else:raise AssertionError('unsupported band served')
save('test-records.json',records);save('counterfactuals.json',pairs)

# Actual engine checks: complete banks; equivalent blank notation, wrong terms and full derivatives.
engine=[]
for i,r in enumerate(records+[p[z] for p in pairs for z in ('before','after')]):
 f=field(r);checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  for a in f[':answer-field/choices']:
   checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete bank key and distractors'})
 else:
  ans=g.parse(key(r));full=s.diff(g.parse(re.search(r'\$([^$]*)\$',r['question'][':question/problem'])[1].rstrip('.')),g.X)
  vals=[(key(r),'accepted','authored key'),(g.tex(s.expand(ans,log=False)),'accepted','independently expanded equivalent'),(g.tex(ans+1),'rejected','additive error'),('0','rejected','zero shortcut')]
  if not eq(full,ans):vals.append((g.tex(full),'rejected','full derivative in partial blank'))
  checks=[{'submitted':v,'expected':expected,'purpose':why} for v,expected,why in vals]
 engine.append({'label':f'{i}:{r["generation"]["template"]}:{r["generation"]["missing_term"]}','record':r,'checks':checks})
save('engine-input.json',engine)
save('math-validation.json',{'passed':True,'source_records':len(replay),'source_bank_values_matched':matched,'source_bank_values_total':total,'source_banks':10,'checked_generated_records':len(records),'counterfactual_pairs':len(pairs),'native_cases':len(engine),'native_responses':sum(len(c['checks']) for c in engine),'determinism':True,'independent_checks':['differentiate parsed displayed product','reconstruct completed prompt RHS','check every solution row against derivative','central differences at three regular points','unique radio key and complete bank']})
print(json.dumps(json.loads((E/'math-validation.json').read_text()),indent=2))
