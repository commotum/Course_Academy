"""Strict acceptance + visible-math regression for repeated/unit literal banks.
No services, DB writes or runtime edits. Run with the job's Python -B.
"""
import sys
sys.dont_write_bytecode=True
import collections, copy, json
from author_old_unit import W, E, g, check, bank, answer, field, key, mask, negative_corner, save

FINDING='9ffb0e3daa5aa34af617'

def surface_probes(records):
 groups=collections.defaultdict(list)
 for r in records:groups[r['generation']['template']].append(r)
 report={}
 for name,rs in groups.items():
  counts=collections.Counter();positions=collections.Counter()
  for r in rs:
   bs=bank(r);target=next(i for i,a in enumerate(field(r)[':answer-field/choices']) if a[':answer/id']==key(r))
   positions[target]+=1
   assert len({str(mask(m)) for m in bs})==1, 'Sign-mask shortcut reintroduced'
   assert not negative_corner(r), 'Old exact corner shortcut persists'
   for label,fun in [('sum',lambda m:sum(map(sum,m))),('absolute_sum',lambda m:sum(abs(v) for row in m for v in row)),('corner',lambda m:m[-1][-1]),('first',lambda m:m[0][0]),('first_row_sum',lambda m:sum(m[0])),('negative_count',lambda m:sum(v<0 for row in m for v in row)),('zero_count',lambda m:sum(v==0 for row in m for v in row)),('unit_count',lambda m:sum(abs(v)==1 for row in m for v in row)),('lexicographic',lambda m:tuple(v for row in m for v in row))]:
    vals=[fun(m) for m in bs]
    for direction,op in [('min',min),('max',max)]:
     matches=[i for i,v in enumerate(vals) if v==op(vals)]
     counts[label+'_'+direction]+=matches==[target]
  assert len(positions)>1,(name,positions)
  assert all(n<len(rs) for n in counts.values()),(name,counts)
  report[name]={'records':len(rs),'positions':dict(positions),'unique_extreme_correct':dict(counts),'negative_corner_successes':0,'single_sign_mask_banks':len(rs),'semantic_matrices':len({str(answer(r)) for r in rs})}
 return report

def main():
 records=[];labels=[];seen=set()
 def add(name,params,label):
  src=g.PROFILES[name];level=src[':question/difficulty'][':db/ident'].split('/')[-1]
  token=(name,tuple(sorted(params.items())))
  if token in seen:return
  seen.add(token)
  r=g.generate(level,941713401+len(records),profile=name,parameters=params)
  want=check(r)
  assert len(bank(r))==5 and bank(r).count(want)==1
  assert len({str(mask(m)) for m in bank(r)})==1
  assert not negative_corner(r)
  records.append(r);labels.append(label)
 # Exact latest failure, including seed, and its negative-unit counterpart.
 exact=g.generate('easy',941713401,profile='q-71722',parameters={'2':1,'3':4})
 assert check(exact)==[[1,-1,4],[1,1,-1]]
 add('q-71722',{'2':1,'3':4},'exact positive unit failure')
 add('q-71722',{'2':2,'3':4},'adjacent coefficient at fixed constant')
 neg=g.generate('easy',941713401,profile='q-71722',parameters={'2':-1,'3':4})
 assert check(neg)==[[1,1,4],[-1,1,-1]]
 for a in (-1,1):
  for b in (-24,-4,-2,-1,1,2,4,24):add('q-71722',{'2':a,'3':b},f'unit {a}, constant {b}')
 for a in (-24,-2,2,24):
  for b in (-1,1):add('q-71722',{'2':a,'3':b},f'coefficient {a}, repeated unit constant {b}')
 # Same defect class in every supported source family, including missing zeros.
 for name,src in g.PROFILES.items():
  slots=[str(n) for n in g.slots(src)]
  for value in (-1,1,-2,2):add(name,{s:value for s in slots},f'all literals {value}')
 # A changed decisive coefficient at fixed remaining evidence and seed.
 pair=[g.generate('easy',941713401,profile='q-71722',parameters={'2':v,'3':4}) for v in (1,-1,2)]
 for r in pair:check(r)
 assert len({str(answer(r)) for r in pair})==3
 assert len({r['question'][':question/problem'] for r in pair})==3
 assert len({r['question'][':question/worked-solution'] for r in pair})==3
 # Oracle mutation: a wrong key must fail, even with correct bank metadata.
 bad=copy.deepcopy(exact);field(bad)[':answer-field/correct'][1]=next(a[':answer/id'] for a in field(bad)[':answer-field/choices'] if a[':answer/id']!=key(bad))
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('Visible-math witness accepted stale key')
 # All prior source replays and a small ordinary sample are graded as controls.
 replays=[];sample=[]
 for name,src in g.PROFILES.items():
  level=src[':question/difficulty'][':db/ident'].split('/')[-1]
  replays.append(g.generate(level,941713201,profile=name,parameters={str(n):n for n in g.slots(src)}))
  sample.extend(g.generate(level,941713511+i,profile=name) for i in range(2))
 cases=[]
 for i,r in enumerate(records+pair+replays+sample):
  check(r);cases.append({'label':str(i)+'-'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(r) else 'rejected','purpose':'Independently parsed equations and full five-choice bank'} for a in field(r)[':answer-field/choices']]})
 report=surface_probes(records)
 save('unit-records.json',records);save('unit-counterfactual-records.json',pair);save('unit-grader-input.json',cases)
 for level in ('easy','moderate'):save('unit-'+level+'.json',[r for r in records if r['question'][':question/difficulty'].endswith('/'+level)])
 save('unit-shortcuts-before-delivery.json',report)
 save('unit-regression-results.json',{'finding':FINDING,'passed':True,'records':len(records),'cases':labels,'exact_positive_and_negative_units':True,'all_source_profiles':len(g.PROFILES),'counterfactuals':3,'source_replay_grader_controls':10,'ordinary_sample_grader_controls':20,'grader_cases':len(cases),'stale_key_mutation_rejected':True,'semantic_matrices':len({str(answer(r)) for r in records}),'finite_probe_limit':'No universal tested within-profile position or scalar cue. Collapsed all-unit systems admit direct unit recognition, a valid coefficient-reading simplification.'})
 print(json.dumps({'finding':FINDING,'passed':True,'records':len(records),'grader_cases':len(cases),'profiles':len(report)}))
if __name__=='__main__':main()
