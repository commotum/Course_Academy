#!/usr/bin/env python3
"""Strict radius regression plus full-family, same-bank counterfactual witnesses.
No runtime file changes or service access. Test records come from current code.
"""
import sys
sys.dont_write_bytecode=True
import argparse,importlib.util,json,random,re
from collections import Counter
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
R=Path(__file__).resolve().parent;E=R/'evidence';E.mkdir(exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,default=R);a=ap.parse_args()
spec=importlib.util.spec_from_file_location('radius_candidate',a.package/'17592186229183.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def probe(r):
 f=r['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];key=f[':answer-field/correct'];key=key[1] if isinstance(key,list) else key[':answer/id']
 vals=[Fraction(re.search(r'\d+(?:\.\d+)?',x[':answer/value'])[0]) for x in choices]
 eligible=[i for i,v in enumerate(vals) if all(abs(v-u)<=2 for u in vals)]
 ki=next(i for i,x in enumerate(choices) if x[':answer/id']==key);ordered=sorted(vals);mu=sum(vals)/5
 selectors={'median':ordered[2], 'lowest':ordered[0], 'highest':ordered[-1],
 'nearest_mean':min(ordered,key=lambda v:abs(v-mu)),
 'smallest_neighbor_gap':min(ordered,key=lambda v:min(abs(v-w) for w in vals if w!=v)),
 'largest_neighbor_gap':max(ordered,key=lambda v:min(abs(v-w) for w in vals if w!=v))}
 return {'question_id':r['question'][':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],
 'sorted_choices':[str(v) for v in ordered],'key':str(vals[ki]),'rank':ordered.index(vals[ki])+1,'position':ki+1,
 'singleton':len(eligible)==1,'success':len(eligible)==1 and eligible[0]==ki,
 'selected_id':choices[eligible[0]][':answer/id'] if len(eligible)==1 else None,
 'radius_key_eligible':ki in eligible,'selector_success':{k:v==vals[ki] for k,v in selectors.items()}}
def independent(r):
 # Read physical quantities and correct value from visible text, not metadata.
 terms=re.findall(r'\$([^$]+)\$',r['question'][':question/problem'])[:6]
 def num(v):
  m=re.search(r'\\frac\{(\d+)\}\{(\d+)\}',v)
  return Fraction(int(m[1]),int(m[2])) if m else Fraction(re.search(r'\d+(?:\.\d+)?',v)[0])
 H,v,q,c,ri,ro=map(num,terms);assert ro/(ri-ro)==2
 z=c*H+(q-c*v)*(v/H)**2
 from decimal import Decimal,ROUND_HALF_UP
 expected=(Decimal(z.numerator)/Decimal(z.denominator)).quantize(Decimal('.1'),rounding=ROUND_HALF_UP)
 assert Fraction(probe(r)['key'])==Fraction(expected)
 return str(expected)
p={'H':'20','v':'10','q':'1','c':'0.4','rin':'6','rout':'4'}
minimal=g.generate('easy',seed=41072,template='q-336506',parameters=p)
assert independent(minimal)=='7.3'
m=probe(minimal);save('radius-minimal-records.json',[minimal])
failures=[]
if m['success']:failures.append('exact seed 41072 still identifies key by unique 2 lb radius')
samples=[g.generate('easy',seed=seed,template=t) for t in g.MASKS for seed in range(8)]
for r in samples:independent(r)
# Inject only a legal random draw stream for four gaps. The real rank draw,
# generator, mathematical model, rendering, identities and key remain untouched.
# Same seed set was already used by prior rank regressions.
RealRandom=random.Random
class FixedShapeRandom(RealRandom):
 def __init__(self,seed):super().__init__(seed);self.draw=0
 def randint(self,lo,hi):
  self.draw+=1
  if self.draw==1:return super().randint(lo,hi)
  assert (lo,hi)==(1,20),(lo,hi)
  return 10
by_rank={1:2,2:1,3:7,4:0,5:5}
controls=[]
for t in g.MASKS:
 for rank,seed in by_rank.items():
  params={'H':'100','v':'50','q':str(1+4*(rank-1)),'c':'0.4','rin':'6','rout':'4'}
  with patch.object(g.random,'Random',FixedShapeRandom):r=g.generate('easy',seed=seed,template=t,parameters=params)
  independent(r);controls.append(r)
# Same visible bank 35.3..39.3, unique radius center 37.3. Changed initial
# mass independently changes the computed key; all five roles are exercised.
for t in g.MASKS:
 rs=[r for r in controls if r['generation']['template']==t];zs=[probe(r) for r in rs]
 assert len({tuple(z['sorted_choices']) for z in zs})==1
 assert {z['rank'] for z in zs}=={1,2,3,4,5}
 assert all(z['singleton'] for z in zs)
 assert sum(z['success'] for z in zs)==1
 for cue in zs[0]['selector_success']:
  assert sum(z['selector_success'][cue] for z in zs)==1,(t,cue)
save('same-bank-counterfactual-records.json',controls)
groups={}
for t in g.MASKS:
 zs=[probe(r) for r in samples if r['generation']['template']==t]
 assert len({z['rank'] for z in zs})>1 and len({z['position'] for z in zs})>1
 # Requires both a right and a wrong radius singleton, rather than mistaking
 # an accidental success for a universal inference.
 assert any(z['singleton'] and not z['success'] for z in zs)
 assert any(not z['radius_key_eligible'] for z in zs),t
 groups[t]={'count':len(zs),'rank_counts':dict(Counter(z['rank'] for z in zs)),
 'position_counts':dict(Counter(z['position'] for z in zs)),
 'radius_singletons':sum(z['singleton'] for z in zs),'radius_successes':sum(z['success'] for z in zs),
 'key_outside_radius':sum(not z['radius_key_eligible'] for z in zs),
 'selector_successes':{k:sum(z['selector_success'][k] for z in zs) for k in zs[0]['selector_success']}}
# Check real delivered inputs when provided; these are diagnostics, not fixtures
# used to satisfy the primary regression. Generated controls above always rerun.
stages={}
for name,path in [('sample before','sample-records.json'),('sample after','delivery-sample/accepted.json'),('batch before','batch-records.json'),('batch after','delivery-batch/accepted.json'),('same bank after','delivery-controls/accepted.json')]:
 if (E/path).exists():
  rs=json.loads((E/path).read_text());zs=[probe(r) for r in rs]
  stages[name]={'count':len(zs),'singletons':sum(z['singleton'] for z in zs),'successes':sum(z['success'] for z in zs),'rows':zs}
 if name=='same bank after' and (E/path).exists():
  for t in g.MASKS:
   zs=[probe(r) for r in rs if r['generation']['template']==t]
   assert len(zs)==5 and sum(z['success'] for z in zs)==1
save('shortcut-results.json',{'passed':not failures,'command':sys.argv,'minimal':m,'by_template':groups,'delivery_stages':stages,
 'same_bank':{'records':len(controls),'correct_ranks':[1,2,3,4,5],'radius_successes_per_template':1,'radius_rejections_per_template':4,'gap_draw_control':'Current entrypoint with legal deterministic randint gap draws 10,10,10,10; actual initial mass changes q=1,5,9,13,17.'},
 'limits':'Finite probes plus an all-rank same-shape witness remove the demonstrated structural implication; no claim of exhaustive adversarial shortcut absence. Random shape/position changes are not counted as distinct physical tasks.', 'failures':failures})
save('shortcut-grader-input.json',[{'label':'same visible radius center / '+r['generation']['template']+' / key rank '+str(probe(r)['rank']),'record':r,'checks':[{'field_index':0,'submitted_answer_id':probe(r)['selected_id'],'expected':'accepted' if probe(r)['success'] else 'rejected','purpose':'Same radius center must fail for four changed initial masses and pass only for independently computed center mass.'}]} for r in controls])
print(json.dumps({'passed':not failures,'minimal':m,'normal_records':len(samples),'same_bank_records':len(controls),'failures':failures}));sys.exit(bool(failures))
