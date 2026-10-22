#!/usr/bin/env python3
"""Retained finding regressions; visible-matrix Fraction oracle, offline only."""
import collections
from fractions import Fraction as F
import importlib.util
import itertools
import json
from pathlib import Path
import re
import sys
import subprocess

H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate',H/'17592186119807.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
E=H/'evidence';E.mkdir(exist_ok=True)
def save(name,obj):(E/name).write_text(json.dumps(obj,indent=2)+'\n')
def number(s):
 s=re.sub(r'\s+','',s)
 s=re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 s=s.replace('(','').replace(')','')
 return F(s)
def vecs(r):
 q=r.get('question',r)
 return [tuple(number(x) for x in body.split(r'\\')) for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)]
def solve(r):
 a,c,b=vecs(r);assert len(a)==len(c)==len(b)==3
 for i,j in itertools.combinations(range(3),2):
  det=a[i]*c[j]-a[j]*c[i]
  if det:
   x=(b[i]*c[j]-b[j]*c[i])/det;y=(a[i]*b[j]-a[j]*b[i])/det
   return (x,y),all(a[k]*x+c[k]*y==b[k] for k in range(3))
 raise AssertionError('Dependent columns')
def choices(r):return r['question'][':question/answer-fields'][0][':answer-field/choices']
def key(r):
 f=r['question'][':question/answer-fields'][0]
 return next(a[':answer/value'] for a in choices(r) if a[':answer/id']==f[':answer-field/correct'][1])
def canonical(v):return v if v=='No solution' else str(number(v))
def expected(r):
 x,ok=solve(r);return str(sum(x)) if ok else 'No solution'
def rank(r):
 return None if key(r)=='No solution' else sorted(number(a[':answer/value']) for a in choices(r) if a[':answer/type']==':answer.type/math').index(number(key(r)))+1
def params(residual=0,rank=2,t=0):return {'translation':t,'residual':residual,'rank':rank,'gaps':[1,2,3]}
def check(r):
 assert canonical(key(r))==expected(r)
 f=r['question'][':question/answer-fields'][0]
 assert f[':answer-field/type']==':answer-field.type/radio'
 assert len(choices(r))==5 and len({canonical(a[':answer/value']) for a in choices(r)})==5
 assert r==g.generate('moderate',r['generation']['seed'],r['generation']['source_id'],r['generation']['parameters'])
 # Read rendered solution: supplied vectors and its final concrete check must follow prompt.
 q=r['question'];a,c,b=vecs(r);text=q[':question/worked-solution']
 if len(r['generation']['parameters'])>1:
  ms=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)
  assert [tuple(number(z) for z in m.split(r'\\')) for m in ms[:3]]==[a,c,b]
  # Solve the source method's pair independently, then verify the displayed residual equality.
  plan=g.PLANS[r['generation']['source_id']];i,j=plan[2:4];d=a[i]*c[j]-a[j]*c[i]
  x=(b[i]*c[j]-b[j]*c[i])/d;y=(a[i]*b[j]-a[j]*b[i])/d;k=plan[-1]
  def latex(z):
   return str(z.numerator) if z.denominator==1 else ('- ' if z<0 else '')+r'\frac{'+str(abs(z.numerator))+'}{'+str(z.denominator)+'}'
  if a[0]==c[0]==0 and b[0]!=0:assert 'first equation is a false statement' in text
  else:
   assert latex(a[k]*x+c[k]*y)+' &='+latex(b[k]) in text
   assert ('true statement.' in text)==(expected(r)!='No solution')
   assert ('false statement.' in text)==(expected(r)=='No solution')
 return r

def metrics(rs):
 groups=collections.defaultdict(list)
 for r in rs:groups[r['generation']['source_id']].append(r)
 def summary(items):
  return {'count':len(items),'consistent':sum(expected(r)!='No solution' for r in items),'ranks':dict(collections.Counter(str(rank(r)) for r in items)), 'key_positions':dict(collections.Counter(str(next(i for i,a in enumerate(choices(r)) if a[':answer/value']==key(r))) for r in items)), 'second_largest_success':sum(rank(r)==3 for r in items), 'no_solution_success':sum(expected(r)=='No solution' for r in items)}
 return {'overall':summary(rs),'profiles':{p:summary(items) for p,items in groups.items()},'semantic_systems':len({tuple(vecs(r)) for r in rs})}

def main():
 source=json.loads((H.parent/'source/source.json').read_text())['material']['kp']
 replay=[];records=[]
 for q in source[':knowledge-point/questions']:
  sid=q[':question/math-academy-id'];r=check(g.generate('moderate',83,sid,{'translation':0}))
  bank=lambda cc:sorted((canonical(a[':answer/value']), a[':answer/type'].get(':db/ident') if isinstance(a[':answer/type'],dict) else a[':answer/type']) for a in cc)
  assert bank(q[':question/answer-fields'][0][':answer-field/choices'])==bank(choices(r))
  assert canonical(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])==expected(r)
  assert g.normalize_prose(q[':question/problem'])==r['question'][':question/problem']
  old=q[':question/worked-solution']
  if sid=='q-105163':
   assert '-\\frac{33}{2} & =-8' in old
   old=old.replace(r'-\frac{33}{2} & =-8',r'-\frac{39}{2} & =-11')
   assert F(-3)+3*F(-11,2)==F(-39,2)!=-11
  assert g.normalize_prose(old)==r['question'][':question/worked-solution']
  replay.append({'profile':sid,'question_id':q[':question/id'],'complete_bank':True,'matched_choices':5,'worked_method_preserved':True,'arithmetic_correction':sid=='q-105163'})
  records.append(r)
 # Every recognizable coefficient profile: change only decisive RHS row; ranks vary at fixed evidence.
 controls=[]
 for sid in sorted(g.CASES):
  group=[]
  for residual in (0,1):
   for rk in range(1,5):
    r=check(g.generate('moderate',83,sid,params(residual,rk)));records.append(r);group.append(r)
  assert {expected(r)=='No solution' for r in group}=={False,True}
  assert {rank(r) for r in group if expected(r)!='No solution'}=={1,2,3,4}
  first,other=group[0],group[4]
  av,bv=vecs(first),vecs(other)
  assert av[:2]==bv[:2] and sum(x!=y for x,y in zip(av[2],bv[2]))==1
  assert first['question'][':question/worked-solution']!=other['question'][':question/worked-solution']
  assert expected(first)!='No solution' and expected(other)=='No solution'
  assert len({r['question'][':question/problem'] for r in group[:4]})==1
  controls.append({'profile':sid,'only_one_target_component_changed':True,'consistent_numeric_ranks':[rank(r) for r in group[:4]]})
 # Exact retained counterexample, no metadata-based truth assertion.
 bad=check(g.generate('moderate',83,'q-34568',params(-2)))
 good=check(g.generate('moderate',83,'q-34568',params(0)))
 assert vecs(bad)[2]==(3,4,5) and vecs(good)[2]==(3,4,7)
 assert expected(bad)=='No solution' and expected(good)=='2'
 controls_records=[bad,good]
 # Original q-105166 t=-1: hold its vectors fixed, move key away from rank three.
 for rk in (1,4):
  r=check(g.generate('moderate',83,'q-105166',params(0,rk,-1)))
  assert expected(r)=='-1' and rank(r)==rk;controls_records.append(r)
 # Irrelevant choice ordering changes neither mathematical truth nor explanation.
 alt=check(g.generate('moderate',84,'q-34568',params(0)))
 assert alt['question'][':question/problem']==good['question'][':question/problem']
 assert alt['question'][':question/worked-solution']==good['question'][':question/worked-solution']
 assert choices(alt)!=choices(good) and expected(alt)==expected(good)
 controls_records.append(alt)
 # Boundaries of the same repaired slots, including fractional source candidate arithmetic.
 for sid in ('q-105163','q-34242','q-73954'):
  for t in (-2,2):records.append(check(g.generate('moderate',211,sid,params(-1,3,t))))
 for args in [('easy',),('hard',),('moderate',83,'unknown'),('moderate',83,'q-34568',{'translation':3}),('moderate',83,'q-34568',params(0,5)),('moderate',83,'q-34568',dict(params(),gaps=[0,1,2]))]:
  try:g.generate(*args)
  except ValueError:pass
  else:raise AssertionError('Invalid input accepted')
 # Small unforced sampler probe for the two formerly cue-bearing surface families.
 normal=[check(g.generate('moderate',seed,sid)) for sid in ('q-34568','q-105165') for seed in range(8)]
 for sid in ('q-34568','q-105165'):
  items=[r for r in normal if r['generation']['source_id']==sid]
  assert {expected(r)=='No solution' for r in items}=={False,True}
  assert len({rank(r) for r in items if expected(r)!='No solution'})>1
  assert len({next(i for i,a in enumerate(choices(r)) if a[':answer/value']==key(r)) for r in items if expected(r)=='No solution'})>1
  assert all(len([a for a in choices(r) if a[':answer/type']==':answer.type/text'])==1 for r in items)
 save('normal-sampler-records.json',normal)
 records+=normal
 batch=[check(r) for r in g.batch('moderate',5,119807)]
 assert any(rank(r)!=3 for r in batch)
 assert batch==g.batch('moderate',5,119807)
 save('replacement-batch.json',batch);save('source-replay.json',replay)
 save('test-records.json',records+controls_records)
 save('counterfactual-records.json',controls_records)
 save('pedagogical-variation.json',{'controlled_cases':controls,'raw':metrics(records),'replacement_batch':metrics(batch),'irrelevant_order_preserves_response':True,'exact_review_flip':{'before':'(3,4,5): No solution','after':'(3,4,7): 2'},'fixed_zero_row':'0 = nonzero is valid decisive mathematical evidence; both outcomes supported'})
 repo=H.parents[5]
 for name,folder in [('test-records.json','delivery'),('replacement-batch.json','delivery-batch')]:
  subprocess.run([sys.executable,str(repo/'generate/pipeline/check_delivery.py'),'--input',str(E/name),'--source',str(H.parent/'source/source.json'),'--inventory',str(H.parent/'source/inventory.json'),'--difficulty','moderate','--output',str(E/folder),'--asset-root',str(E/'assets')],check=True,capture_output=True,text=True)
 delivered=json.loads((E/'delivery/accepted.json').read_text());dbatch=json.loads((E/'delivery-batch/accepted.json').read_text())
 assert len(dbatch)==5 and any(rank(r)!=3 for r in dbatch)
 groups=collections.defaultdict(list)
 for r in delivered:
  assert canonical(key(r))==expected(r)
  groups[r['generation']['source_id']].append(r)
 for sid in g.CASES:
  assert {expected(r)=='No solution' for r in groups[sid]}=={False,True}
  assert {rank(r) for r in groups[sid] if expected(r)!='No solution'}=={1,2,3,4}
 save('post-delivery-shortcuts.json',{'raw':metrics(records+controls_records),'accepted':metrics(delivered),'replacement_batch':metrics(dbatch),'all_profiles_both_branches_and_all_numeric_ranks':True,'zero_writes':True})
 save('regression-results.json',{'passed':True,'source_banks':len(replay),'matched_source_choices':len(replay)*5,'checked_records':len(records)+len(controls_records)+len(batch),'retained_findings':['ff8f3c22155f60689a0c','6eae84335e516e298861','0afea531a58b614ace78']})
 print(json.dumps({'passed':True,'source_banks':len(replay),'records':len(records)+len(controls_records)+len(batch),'batch':metrics(batch)['overall']}))
if __name__=='__main__':main()
