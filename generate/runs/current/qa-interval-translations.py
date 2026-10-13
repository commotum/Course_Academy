"""Root set semantics of actual interval prompts, whole banks and worked steps."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_interval_readback',P/'interval-readback.py');g=module('root_interval_gen'+str(K),D.with_suffix('.py'))
C=dict(records=0,choices=0,whole_banks=0,solution_sets=0,source_prompts=0,source_values=0,source_banks=0,source_absent_keys=0,source_absent_solutions=0,source_absent_ratings=0,missing_raw_assessments=0)
def check(r):
 q=r['question'];target=p.task(q[':question/problem']);f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];values=[p.meaning(z[':answer/value']) for z in choices];assert len(values)==5 and len(set(values))==5
 actual=[z[':answer/id'] for z,v in zip(choices,values) if v==target];assert len(actual)==1
 if ':answer-field/correct' not in f:
  assert ':question/difficulty' not in q and ':question/worked-solution' not in q;C['missing_raw_assessments']+=1
 else:
  assert actual==[f[':answer-field/correct'][1]]
  if K==17592186059826:assert target.left_open and target.right_open
  elif K==17592186059827:assert target.left_open!=target.right_open
  else:assert not target.left_open and not target.right_open
  a,b=target.start,target.end;level=q[':question/difficulty'].split('/')[-1];profile=r['generation'].get('profile',r['generation'].get('bank_profile',''))
  if K==17592186059826:
   if level=='easy':assert a.is_Integer and b.is_Integer and 1<=a<b<=12
   elif level=='moderate':assert a.is_Integer and b.is_Integer and a<0 and -12<=a<b<=12
   else:assert a.is_Rational and b.is_Rational and not a.is_Integer and not b.is_Integer and 2<=a.q<=4 and 2<=b.q<=4 and abs(a)<=6 and abs(b)<=6
  if K==17592186059827:
   if level=='easy':assert a.is_Integer and b.is_Integer and 0<=a<b<=15
   elif level=='moderate':assert a.is_Rational and b.is_Rational and not(a.is_Integer and b.is_Integer) and a<0 and a.q<=5 and b.q<=5 and abs(a)<=10 and abs(b)<=10
   else:assert a<0 and not(a.is_Rational and b.is_Rational) and all(abs(z)<=15 and (z.is_Integer or z**2 in range(1,145)) for z in (a,b))
  if K==17592186059829:
   if level=='easy':assert a.is_Integer and b.is_Integer and -12<=a<b<=12
   elif level=='moderate':assert a.is_Rational and b.is_Rational and not(a.is_Integer and b.is_Integer) and all(z.q<=5 and abs(z.p)<=12 and abs(z)<=8 for z in (a,b))
   else:
    domain={s.Rational(n,d) for d in (1,2,3) for n in range(-6,7)}|{sgn*c*s.sqrt(rr) for sgn in (-1,1) for c in (1,2,3) for rr in (2,3,5,7)}
    assert a in domain and b in domain and not a.is_Integer and not b.is_Integer and (a.is_irrational or b.is_irrational) and a<0
   base={s.Interval(a,b,left_open=l,right_open=rr) for l in (True,False) for rr in (True,False)}
   extra=s.Union(s.Interval(-s.oo,a,right_open=True),s.Interval(b,s.oo,left_open=True)) if r['generation']['template']=='interval_to_inequality' else s.Interval(-s.oo,b,right_open=False)
   assert set(values)==base|{extra}
  if K==17592186059826:
   base={s.Interval(a,b,left_open=l,right_open=rr) for l in (True,False) for rr in (True,False)}
   extra=s.Union(s.Interval(-s.oo,a,right_open=True),s.Interval(b,s.oo,left_open=True)) if r['generation']['template']=='interval_to_inequality' else s.Interval(-s.oo,b,right_open=True)
   assert set(values)==base|{extra}
  if K==17592186059827:
   base={s.Interval(a,b,left_open=l,right_open=rr) for l in (True,False) for rr in (True,False)}
   extra=s.Interval(-a,b,left_open=target.left_open,right_open=target.right_open) if profile.startswith('observed_25754') else s.EmptySet
   assert set(values)==base|{extra}
  blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S);assert len(blocks)>=2
  for block in blocks:assert p.meaning(block)==target,('Stale/false interval teaching stage',block,target);C['solution_sets']+=1
 C['records']+=1;C['choices']+=5;C['whole_banks']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 level=case.get('level',case.get('difficulty',case.get('replay_level','easy')));q=check(g.generate(level,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];C['source_prompts']+=1
 of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in f[':answer-field/choices']);C['source_values']+=len(of[':answer-field/choices']);C['source_banks']+=1
 assert ':answer-field/correct' not in of and ':question/difficulty' not in old and ':question/worked-solution' not in old;C['source_absent_keys']+=1;C['source_absent_solutions']+=1;C['source_absent_ratings']+=1
review=json.loads((D/'review.json').read_text());review=review if isinstance(review,list) else [r for values in review.values() for r in values]
for item in review:check(item.get('record',item))
for item in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(item)
for level in ('easy','moderate','hard'):
 for template in g.TEMPLATES:
  for seed in range(35):check(g.generate(level,seed+410,template=template))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
