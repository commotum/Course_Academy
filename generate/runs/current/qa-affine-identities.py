"""Root validates full affine solution sets and categorical banks from printed math."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186110719;D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_identity_scalar',P/'ode-scalar-parser.py');g=module('root_identity_gen',D.with_suffix('.py'));x=p.x
C=dict(records=0,actual_equations=0,choices=0,whole_banks=0,solution_set_stages=0,prose_unique_solutions=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0)
def scalar(v):return s.expand(p.scalar(v.strip().rstrip('.,').replace(r'\left','').replace(r'\right','')))
def roots(a,b):
 z=s.Poly(a-b,x);assert z.degree()<=1 or z.is_zero
 if z.is_zero:return ('identity',)
 if z.degree()==0:return ('empty',)
 return ('unique',s.cancel(-z.nth(0)/z.nth(1)))
def subset(v):return frozenset(re.findall(r'\b(?:III|II|I)\b',v))
BANKS={k:frozenset(v) for k,v in {'observed_a':['II only','III only','I and II only','II and III only','I, II, and III'],'observed_b':['None','I and II only','II only','III only','I and III only'],'observed_c':['I and II only','II only','I only','II and III only','III only'],'observed_d':['II and III only','III only','None','I and III only','II only']}.items()}
def check(r):
 q=r['question'];meta=r['generation'];raw=re.findall(r'^- \$(.*?)\$',q[':question/problem'],re.M);assert len(raw)==3;classes=[];level=q[':question/difficulty'].split('/')[-1]
 for z in raw:
  a,b=z.split('=');A,B=scalar(a),scalar(b);classes.append(roots(A,B));L,R=s.Poly(A,x),s.Poly(B,x);assert L.degree()==R.degree()==1 and L.nth(1) and R.nth(1)
  factors=re.findall(r'(-?\d+)\\left\((.*?)\\right\)',z)
  if level=='easy':assert not factors and all(v.is_Integer for v in [L.nth(1),L.nth(0),R.nth(1),R.nth(0)]) and abs(L.nth(1))<=7 and abs(R.nth(1))<=7 and abs(L.nth(0))<=9 and abs(R.nth(0))<=9
  else:
   assert len(factors)==(1 if level=='moderate' else 2)
   for c,inner in factors:
    c=int(c);I=s.Poly(scalar(inner),x);assert 2<=abs(c)<=(5 if level=='moderate' else 4)
    if level=='moderate':assert I.nth(1)==1 and 1<=abs(I.nth(0))<=5
    else:assert all(v.is_Integer and 1<=abs(v)<=4 for v in I.all_coeffs())
   if level=='hard':assert all(v.is_Integer and 1<=abs(v)<=15 for v in [L.nth(1),L.nth(0),R.nth(1),R.nth(0)])
 C['actual_equations']+=3;wanted=frozenset(label for label,c in zip(('I','II','III'),classes) if c[0]=='identity');f=q[':question/answer-fields'][0];values=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(values)==5 and frozenset(values)==BANKS[meta['profile']] and len({subset(v) for v in values})==5;good=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert subset(good[':answer/value'])==wanted and sum(subset(v)==wanted for v in values)==1;C['whole_banks']+=1;C['choices']+=5
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==3
 for block,expected in zip(blocks,classes):
  body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
  for row in body.split(r'\\'):
   sides=row.strip().rstrip('.,').split('=');assert len(sides)==2;assert roots(scalar(sides[0]),scalar(sides[1]))==expected,(row,expected);C['solution_set_stages']+=1
 chunks=re.split(r'- For the (?:first|second|third) equation, we have',sol)[1:];assert len(chunks)==3
 for chunk,expected in zip(chunks,classes):
  if expected[0]=='unique':
   m=re.search(r'has the unique solution \$x=(.*?)\$',chunk);assert m and scalar(m[1])==expected[1];C['prose_unique_solutions']+=1
  elif expected[0]=='identity':assert 'has infinitely many solutions.' in chunk and 'true for all values' in chunk
  else:assert 'false for all values' in chunk
 assert 'Therefore, the correct answer is "'+good[':answer/value']+'."' in sol;C['records']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution'];C['source_prompts']+=1;C['source_solutions']+=1;of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_values']+=5;C['source_banks']+=1;C['source_keys']+=1
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for profile in BANKS:
  for seed in range(12):check(g.generate(level,seed+1107,profile=profile))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
