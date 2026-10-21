"""Read actual accepted banks, compare cues and state selection limits."""
import collections,json,sys
sys.dont_write_bytecode=True
from validate_repair import E,load,save,cues
from repair_regression import probe,g
from visible_math import sep,resolved,same
raw=load(E/'delivery-input.json');accepted=load(E/'delivery/accepted.json');batch=load(E/'delivery-batch/accepted.json')
pools={'before':raw,'accepted':accepted,'replacement_batch':batch};summary={}
for name,rs in pools.items():
 summary[name]=cues(rs)
 for r in rs:
  t=r['generation']['template'];cs=r['question'][':question/answer-fields'][0][':answer-field/choices']
  if t in ('simple_quotient','exp_quotient'):
   assert not probe(r)['shortcut_success']
   assert sum(sep(c[':answer/value']) and r'\frac' not in c[':answer/value'].replace(g.D,'D') for c in cs)>=2
  if t=='sqrt_quotient':
   ns=[c[':answer/value'].replace(g.D,'D').count(r'\frac') for c in cs]
   assert sum(sep(c[':answer/value']) and ns[i]==max(ns) for i,c in enumerate(cs))>=2
for t in ('simple_quotient','exp_quotient'):
 row=summary['accepted'][t]
 assert len(row['profiles'])==2 and row['semantic_odes']>=4
 assert row['unique_fractionless']==0 and row['unique_min_fractions']==0 and row['unique_max_fractions']==0
 assert row['shortest']<row['count'] and row['longest']<row['count'] and max(row['positions'])<row['count']
assert summary['accepted']['sqrt_quotient']['unique_max_fractions']==0
# A controlled same-bank counterfactual: yD=x and y^2 D=x exchange their
# correctness when the visible ODE changes x/y -> x/y^2. Their equation values
# are held constant, rather than counting shuffled labels as skill variation.
r1=next(r for r in accepted if r['generation']['template']=='simple_quotient' and r['generation']['parameters']['n']==1)
r2=next(r for r in accepted if r['generation']['template']=='simple_quotient' and r['generation']['parameters']['n']==2)
def ode(r):
 import re
 return resolved(re.findall(r'\$\$(.*?)\$\$',r['question'][':question/problem'],re.S)[0])
A='y'+r'\cdot '+g.D+'=x';B='{y}^{2}'+r'\cdot '+g.D+'=x'
assert same(resolved(A),ode(r1)) and not same(resolved(B),ode(r1))
assert same(resolved(B),ode(r2)) and not same(resolved(A),ode(r2))
save('shortcut-after-delivery.json',{'passed':True,'pools':summary,'controlled_response_swap':{'before_ode':str(ode(r1)),'after_ode':str(ode(r2)),'A':A,'B':B,'A_correct_before_only':True,'B_correct_after_only':True},'baseline_random_radio':0.2})
save('delivery-selection.json',{'passed':True,'raw':len(raw),'accepted':len(accepted),'replacement_batch_accepted':len(batch),'generator_rejection':'No rejection/resampling loop. Invalid explicit parameters fail; semantic bank validation raises on ambiguity. Complete bank profile is chosen before parameter sampling for the revised quotient families.','selection_source':'engine/rust/question_selection.rs select(): deduplicate and sort fresh usable IDs; choose a positive-weight available difficulty band, uniform within that band using digest bytes 8:16; without configured weights choose first sorted candidate. Upstream learner activities determine seen IDs.','conditional_result':'Every tested accepted revised record defeats the reported cue individually, so neither within-band choice nor history restriction can restore it in those records. All six easy families and both revised quotient bank profiles survive actual delivery.','limits':['Captured inventory basis 5365 only. Live policy weights, learner history, future entity IDs and reservations not supplied; no live personalized-selection run claimed.','Source radical canonical example lacks an answer bank. Original source banks intentionally retain historical layouts for explicit replay; normal generation uses repaired banks.','Checks establish absence of the named layout cues on tested records, not arbitrary future or learned heuristics.']})
print('delivery:',len(raw),'raw ->',len(accepted),'accepted; batch',len(batch),'; revised shortcut probes passed')
