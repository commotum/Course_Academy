"""Visible-bank counterfactuals and delivery-stage shortcut audit."""
import json,re,hashlib
from collections import Counter
from html.parser import HTMLParser
import repair_check as c
E=c.W/'evidence'
def load(name):return json.loads((E/name).read_text())
def norm(v):return re.sub(r'\s+','',v.replace(r'\left','').replace(r'\right',''))
def signature(r):return tuple(sorted(norm(a[':answer/value']) for a in c.field(r)[':answer-field/choices']))
def answer(r):return norm(c.keyvalue(r))
controls=load('controlled-records.json');accepted=load('delivery-moderate/accepted.json')+load('delivery-hard/accepted.json')
ordinary=load('ordinary-records.json');batch=load('delivery-batch/accepted.json')
# Operate on visible choice text, not target indices or key IDs as predictors.
strategies={
 'lexicographically_first':lambda vals:sorted(vals)[0],
 'shortest_formula':lambda vals:min(vals,key=lambda v:(len(v),v)),
 'longest_formula':lambda vals:max(vals,key=lambda v:(len(v),v)),
}
results=[];coverage=[]
for t in sorted({r['generation']['template'] for r in controls}):
 rr=[r for r in controls if r['generation']['template']==t]
 expected_sig=signature(rr[0]);assert all(signature(r)==expected_sig for r in rr)
 assert len(set(map(answer,rr)))==len(rr)==5
 delivered=[r for r in accepted if r['generation']['template']==t and signature(r)==expected_sig]
 assert len(delivered)==5 and set(map(answer,delivered))==set(expected_sig)
 # Any deterministic answer selected from this visible bank can succeed only once.
 for stage,rs in [('before_filtering',rr),('after_filtering',delivered)]:
  for name,choose in strategies.items():
   count=sum(choose(signature(r))==answer(r) for r in rs);assert count==1
   results.append({'template':t,'stage':stage,'cue':name,'successes':count,'attempts':5,'baseline':0.2})
 coverage.append({'template':t,'all_five_formulas_can_qualify':True,'before':5,'after_delivery':5,'bank_only_strategy_upper_bound':0.2})
# Fixed-position probes on authored choices, separately from actual UI ordering.
positions={t:Counter(next(i for i,a in enumerate(c.field(r)[':answer-field/choices']) if a[':answer/id']==c.key(r)) for r in controls if r['generation']['template']==t) for t in {r['generation']['template'] for r in controls}}
assert all(max(cc.values())<5 for cc in positions.values()),positions
# Semantic instances are normalized differential equations, not UUIDs/seeds or banks.
semantic={}
for t in {r['generation']['template'] for r in controls}:
 rs=[r for r in controls+load('boundary-records.json') if r['generation']['template']==t]
 fingerprints={tuple(map(str,c.ode(r['question'][':question/problem'],r['generation']['parameters']['shift']))) for r in rs}
 assert len(fingerprints)==7
 semantic[t]={'independent_coefficient_equations':len(fingerprints),'a_values':sorted({r['generation']['parameters']['a'] for r in rs}),'b_values':sorted({r['generation']['parameters']['b'] for r in rs}),'shift_values':sorted({r['generation']['parameters']['shift'] for r in rs}),'normal_sample_count':sum(r['generation']['template']==t for r in ordinary)}
source_memory={signature(r):answer(r) for r in load('source-replays.json')}
memory={name:{'correct':sum(source_memory.get(signature(r))==answer(r) for r in rs),'total':len(rs)} for name,rs in [('ordinary',ordinary),('delivered_batch',batch)]}
class Inputs(HTMLParser):
 def __init__(self):super().__init__();self.ids=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='input' and a.get('type')=='radio':self.ids.append(a['value'])
ui=[]
for i,r in enumerate(load('render-records.json'),1):
 parser=Inputs();parser.feed((E/f'render/question-{i:03d}.html').read_text());assert len(parser.ids)==5
 ui.append({'template':r['generation']['template'],'correct_position':parser.ids.index(c.key(r))+1})
assert len({v['correct_position'] for v in ui})>1
# Read-only model of Rust weighted moderate selection: same-band entity pool,
# sorted/deduplicated IDs; hash-to-uniform at bytes 8..16 determines member.
# Role availability is checked, not a claim about unknown real learner history.
model=[]
for t in sorted({r['generation']['template'] for r in controls}):
 pool=[r for r in accepted if r['generation']['template']==t and signature(r)==signature(next(z for z in controls if z['generation']['template']==t))]
 counts=[0]*5
 for n in range(128):
  dd=hashlib.sha256(('course-academy/question-selection/v1/repair-'+str(n)).encode()).digest();v=(int.from_bytes(dd[8:16],'big')>>11)/2**53
  counts[int(v*len(pool))]+=1
 assert all(counts)
 model.append({'template':t,'modeled_future_ids':'1..5, ordered within one band','selection_counts':counts,'draws':128})
c.save('shortcut-results.json',{'within_fixed_bank_probes':results,'controlled_coverage':coverage,'authored_key_positions':{t:dict(v) for t,v in positions.items()},'semantic_coverage':semantic,'source_bank_memory':memory,'ui_positions':ui,'conclusion':'For each recognizable profile a single fixed visible bank has five different accepted formulas under five displayed ODEs; every assignment survives filtering. Any bank-only formula/sign/size cue is bounded at 1/5 on this controlled domain. Correct-choice count remains one because the source contract is radio.','limits':'No claim that all possible human strategies were exhaustively tested. Matching coefficients by mathematically differentiating a candidate is valid solution verification.'})
c.save('selection-results.json',{'engine_source':'engine/rust/question_selection.rs::select and seen_before_task','model':model,'delivered_batch_size':len(batch),'normal_inventory_selection':'All five final-batch records pass shared delivery preparation against captured inventory; no duplicates. Real learner history and live weights unavailable.','limits':'Future entity IDs are synthetic. Positive-weight bands preserve eligible role cases before history exclusions; arbitrary past history can remove particular cases. Selection does not alter question mathematics. No future draw prediction or live learner access claimed.'})
print(json.dumps({'controlled_banks':len(coverage),'visible_cue_tests':len(results),'all_five_roles_survive_delivery':True,'source_bank_memory':memory,'ui_positions':ui}))
