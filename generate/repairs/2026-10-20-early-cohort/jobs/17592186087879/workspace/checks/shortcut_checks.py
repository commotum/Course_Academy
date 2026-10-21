"""Inspect actual visible choices before/after shared delivery filtering."""
import collections, hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence'
sys.path.insert(0,str(Path(__file__).resolve().parent))
from coefficient_regression import g
from validate_repair import key, grading
from visible_math import expr, eq, mathcheck, promptdata, s, x
def save(name,value): (E/name).write_text(json.dumps(value,indent=2,default=str))
def inspect(rows):
 positions=[collections.Counter(),collections.Counter()];ranks=collections.Counter()
 coefficients=collections.Counter();byh=collections.defaultdict(set);byb=collections.defaultdict(set)
 probes=collections.Counter();pair_slopes=[]
 for r in rows:
  p,q,t,h=promptdata(r);coefficients[int(p)]+=1
  byh[str(s.sign(h))].add(int(p));byb[str(q/p)].add(int(p))
  fields=r['question'][':question/answer-fields'];slopes=[]
  for i,f in enumerate(fields):
   cid=f[':answer-field/correct'][1];positions[i][next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==cid)]+=1
  for a in fields[0][':answer-field/choices']:
   v=expr(a[':answer/value']);slope=s.simplify(s.diff(v,x)/v)
   assert slope.is_Integer and 1<=slope<=6
   slopes.append(int(slope))
  ranks[sorted(slopes).index(int(p))]+=1
  probes['always_e_x']+=int(p==1)
  probes['minimum_exponent']+=int(p==min(slopes))
  probes['maximum_exponent']+=int(p==max(slopes))
  counts=collections.Counter()
  for a in fields[1][':answer-field/choices']:
   counts.update(int(-v.args[0]/x) for v in expr(a[':answer/value']).atoms(s.exp))
  candidates=set(slopes)&set(counts)
  assert len(candidates)==2, ('Cross-field unique-slope shortcut',candidates)
  most=[k for k in candidates if counts[k]==max(counts.values())]
  least=[k for k in candidates if counts[k]==min(counts.values())]
  probes['unique_most_frequent_solution_slope']+=int(most==[p])
  probes['unique_least_frequent_solution_slope']+=int(least==[p])
  pair_slopes.append(sorted(candidates))
 n=len(rows)
 assert set(coefficients)==set(range(1,7)),coefficients
 assert set(ranks)==set(range(4)),ranks
 assert all(len(pos)==count for pos,count in zip(positions,[4,5])),positions
 assert all(v<n for v in probes.values()),probes
 assert all(len(v)>1 for v in byh.values())
 return {'records':n,'semantic_ODE_IC_pairs':len({tuple(map(str,promptdata(r))) for r in rows}),
  'coefficient_counts':coefficients,'IF_correct_exponent_rank':ranks,'key_positions':positions,
  'strategy_success_counts':probes,'two_cross_field_candidates_every_record':True,
  'coefficient_support_by_initial_value_sign':{k:sorted(v) for k,v in byh.items()},
  'coefficient_support_by_particular_level':{k:sorted(v) for k,v in byb.items()},
  'limits':'These specific fixed-value, rank, position and cross-field probes are not proof against every conceivable strategy. Select fields necessarily have one correct choice.'}

def main():
 before=json.loads((E/'sample-records.json').read_text());after=json.loads((E/'delivery/accepted.json').read_text())
 report={'before_delivery':inspect(before),'after_delivery':inspect(after)}
 # A recognizable identical IF bank must not determine its correct coefficient.
 bankrows=[];attempts=[]
 for a in range(1,5):
  for seed in range(100):
   r=g.generate('easy',seed=seed,parameters={'a':a,'b':2,'h':-1})
   f=r['question'][':question/answer-fields'][0]
   slopes={int(s.simplify(s.diff(expr(v[':answer/value']),x)/expr(v[':answer/value']))) for v in f[':answer-field/choices']}
   if slopes=={1,2,3,4}:
    assert mathcheck(r)['passed'];bankrows.append(r);attempts.append({'a':a,'seed':seed});break
  else:raise AssertionError('No controlled same-bank witness')
 assert len({str(key(r,0)) for r in bankrows})==4
 report['same_bank_changed_key_witnesses']=attempts
 save('same-bank-records.json',bankrows);save('same-bank-grader-input.json',grading(bankrows))
 # Conditional easy selection, using the exact hash draw in question_selection.rs.
 pool=sorted(after,key=lambda r:r['question'][':question/id']);selected=[]
 for i in range(16):
  seed='repair-'+str(i)
  bits=int.from_bytes(hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()[8:16],'big')>>11
  r=pool[int(bits/(1<<53)*len(pool))]
  selected.append({'seed':seed,'question_id':r['question'][':question/id'],'P':str(promptdata(r)[0])})
 assert len({v['P'] for v in selected})>1
 report['conditional_selection']={'cases':selected,'scope':'Exact within-easy hash draw with UUID-sorted surrogate IDs. Live entity ordering, history and policy weights are unavailable; no claim about every learner pool. Unconfigured selection instead takes the first candidate.'}
 save('shortcut-results.json',report)
 print(json.dumps({'input':len(before),'delivered':len(after),'same_bank_keys':len(bankrows),'strategy_success_after':report['after_delivery']['strategy_success_counts']}))
if __name__=='__main__':main()
