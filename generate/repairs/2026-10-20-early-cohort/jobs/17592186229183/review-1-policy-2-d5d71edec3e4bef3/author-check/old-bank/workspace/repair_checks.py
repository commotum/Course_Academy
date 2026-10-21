#!/usr/bin/env python3
"""Strict visible-record regressions. No services or runtime mutations."""
import sys
sys.dont_write_bytecode=True
import json,re,importlib.util
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from collections import Counter
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import qa_math as qa
g=qa.g
OUT=ROOT/'evidence';OUT.mkdir(exist_ok=True)
def save(name,obj): (OUT/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
def number(tex):
 m=re.search(r'\\frac\{(-?\d+)\}\{(\d+)\}',tex)
 return Fraction(int(m[1]),int(m[2])) if m else Fraction(re.search(r'-?\d+(?:\.\d+)?',tex)[0])
def measure(r):
 q=r['question'];f=q[':question/answer-fields'][0];opts=f[':answer-field/choices'];key=f[':answer-field/correct'];key=key[1] if isinstance(key,list) else key[':answer/id']
 correct=next(a for a in opts if a[':answer/id']==key);val=number(correct[':answer/value'])
 ordered=sorted(opts,key=lambda a:number(a[':answer/value']))
 return {'rank':1+next(i for i,a in enumerate(ordered) if a[':answer/id']==key),
 'position':1+next(i for i,a in enumerate(opts) if a[':answer/id']==key),'mass':str(val),
 'nearest_mean':abs(val-sum(number(a[':answer/value']) for a in opts)/5)==min(abs(number(a[':answer/value'])-sum(number(b[':answer/value']) for b in opts)/5) for a in opts),
 'template':r['generation']['template']}
def independent_numeric(r):
 # Only visible physical quantities, never metadata or generator calculations.
 vals=[number(z) for z in re.findall(r'\$([^$]+)\$',r['question'][':question/problem'])[:6]]
 H,v,q,c,ri,ro=vals;d=ri-ro;n=ro/d
 assert n.denominator==1
 mass=c*H+(q-c*v)*(v/H)**int(n)
 dec=(Decimal(mass.numerator)/Decimal(mass.denominator)).quantize(Decimal('.1'),rounding=ROUND_HALF_UP)
 assert Fraction(dec)==Fraction(measure(r)['mass'])
 opts=r['question'][':question/answer-fields'][0][':answer-field/choices']
 assert len(opts)==5 and len({number(a[':answer/value']) for a in opts})==5
 assert all(number(a[':answer/value'])>0 for a in opts)
 assert all(re.fullmatch(r'\d+\.\d\\,\\text\{lb\}',a[':answer/value']) for a in opts)
 return str(dec)
def probes(records):
 groups={}
 for t in sorted({r['generation']['template'] for r in records}):
  ms=[measure(r) for r in records if r['generation']['template']==t]
  groups[t]={'count':len(ms),'ranks':dict(Counter(m['rank'] for m in ms)),
  'positions':dict(Counter(m['position'] for m in ms)),
  'median_successes':sum(m['rank']==3 for m in ms),'nearest_mean_successes':sum(m['nearest_mean'] for m in ms),'random_baseline':0.2}
  assert len({m['rank'] for m in ms})>1,(t,'fixed numerical rank')
  assert len({m['position'] for m in ms})>1,(t,'fixed displayed position')
  assert not all(m['nearest_mean'] for m in ms),(t,'nearest-mean shortcut')
 return groups

def main():
 source=json.loads((ROOT.parent/'source/source.json').read_text());rows=[];raw=[];math_count=0
 for q in source['material']['kp'][':knowledge-point/questions']:
  sid=q[':question/math-academy-id'];r=g.generate('easy',seed=9041,profile='observed:'+sid);rq=r['question'];raw.append(r)
  for key in (':question/problem',':question/worked-solution'):
   assert rq.get(key)==q.get(key),(sid,key)
  assert (':question/difficulty' in rq)==(':question/difficulty' in q)
  assert len(rq[':question/answer-fields'])==len(q[':question/answer-fields'])
  for sf,rf in zip(q[':question/answer-fields'],rq[':question/answer-fields']):
   assert rf[':answer-field/key']==sf[':answer-field/key']
   assert sorted(a[':answer/value'] for a in rf[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
   assert (':answer-field/correct' in sf)==(':answer-field/correct' in rf)
   if ':answer-field/correct' in sf:
    expected=sf[':answer-field/correct'][':answer/value'];assert next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])==expected
  qa.independent(r);math_count+=1
  rows.append({'source_id':sid,'source_uuid':q[':question/id'],'prompt_and_solution_exact':True,'complete_bank':True,'fields':len(rq[':question/answer-fields'])})
 save('source-replay.json',{'passed':True,'cases':rows,'banks':len(rows),'choices':5*len(rows),'missing_evidence':'q-336499 retains missing key, difficulty and solution; no invented observed content'})
 save('source-replay-records.json',raw)
 params={'H':'20','v':'10','q':'1','c':'0.4','rin':'6','rout':'4'}
 minimal=g.generate('easy',seed=9041,template='q-336506',parameters=params)
 assert measure(minimal)['rank']!=3,'exact latest counterexample still median'
 qa.independent(minimal);independent_numeric(minimal)
 save('minimal-records.json',[minimal])
 samples=[g.generate('easy',seed=seed,template=t) for t in g.MASKS for seed in range(8)]
 for i,r in enumerate(samples):
  independent_numeric(r)
  if i%8==0:qa.independent(r);math_count+=1
 save('sample-records.json',samples)
 pre=probes(samples)
 controls=[g.generate('easy',seed=seed,template=t,parameters=params) for t in g.MASKS for seed in (0,1,2,5,7)]
 for r in controls:assert independent_numeric(r)=='7.3'
 for t in g.MASKS:assert {measure(r)['rank'] for r in controls if r['generation']['template']==t}=={1,2,3,4,5}
 save('rank-controlled-records.json',controls)
 p={'H':'210','v':'90','q':'18','c':'0.5','rin':'18','rout':'12'}
 cfs=[g.generate('easy',seed=9041,template='q-336506',parameters=z) for z in [p,{**p,'H':'240'},{**p,'q':'30'},{**p,'rin':'9','rout':'6'}]]
 cfs.append(g.generate('easy',seed=9041,template='q-336513',parameters=p))
 masses=[independent_numeric(r) for r in cfs]
 assert masses[0]!=masses[1] and masses[0]!=masses[2]
 assert masses[0]==masses[3]==masses[4]
 for r in cfs:qa.independent(r);math_count+=1
 save('counterfactual-records.json',cfs)
 for label,delta in [('capacity equals volume',{'H':'10'}),('no filling',{'rin':'4'}),('zero mass',{'q':'0'}),('equilibrium',{'q':'4'})]:
  try:g.generate('easy',seed=9041,template='q-336506',parameters={**params,**delta})
  except ValueError:pass
  else:raise AssertionError(label)
 smoke=[g.generate(level,seed=seed,template='q-336503') for level in ('moderate','hard') for seed in (1,2)]
 for r in smoke:qa.independent(r);math_count+=1
 save('band-smoke-records.json',smoke)
 save('pedagogical-variation.json',{'passed':True,'normal_before_delivery':pre,'controlled_ranks':probes(controls),'counterfactual_masses':masses,
 'counterfactual_order':['base','capacity 210→240','initial mass 18→30','both flows halved','context only'],
 'unique_physical_tasks':len({r['generation']['mathematical_fingerprint'] for r in samples}),
 'independent_exact_ode_and_displayed_solution_checks':math_count,
 'numeric_checks':len(samples)+len(controls)+len(cfs)+1,
 'scope':'easy source method; rank is incidental, physical variation changes computation; controlled bank-only changes do not count as semantic instances',
 'limits':'No universal shortcut claim beyond measured numerical rank, display position and nearest-mean probes. Inventory/history selection checked separately.'})
 batch=[g.generate('easy',seed=seed) for seed in range(20261021,20261026)]
 save('batch-records.json',batch)
 save('render-records.json',batch+[minimal,cfs[1],samples[-8]])
 save('regression-results.json',{'passed':True,'findings':['74a9fcca07a8526db5eb','430695a16af4478adc1f'],'normal_records':len(samples),'source_cases':len(rows)})
 print(json.dumps({'passed':True,'normal_records':len(samples),'source_cases':len(rows),'ode_and_solution_checks':math_count,'batch':len(batch)}))
if __name__=='__main__':main()
