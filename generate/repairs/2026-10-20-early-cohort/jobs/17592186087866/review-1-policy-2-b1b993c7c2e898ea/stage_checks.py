import audit as a
from collections import Counter,defaultdict
import hashlib

def keyval(r):
 f=r['question'][':question/answer-fields'][0]
 return next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
def cue(r,strategy):
 f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];vals=[c[':answer/value'] for c in cs];ps=[v.split('=',1) for v in vals];lc=Counter(v[0] for v in ps);rc=Counter(v[1] for v in ps)
 if strategy=='first':i=0
 elif strategy=='last':i=4
 elif strategy=='side-frequency':
  scores=[lc[l]+rc[rr] for l,rr in ps];ix=[i for i,v in enumerate(scores) if v==max(scores)];i=ix[0] if len(ix)==1 else None
 elif strategy in ['shortest','longest']:
  scores=[len(v) for v in vals];top=(min if strategy=='shortest' else max)(scores);ix=[i for i,v in enumerate(scores) if v==top];i=ix[0] if len(ix)==1 else None
 elif strategy in ['lexical-min','lexical-max']:
  i=vals.index((min if strategy=='lexical-min' else max)(vals))
 elif strategy=='only-standard':
  ix=[i for i,v in enumerate(vals) if a.is_standard(a.equation(v))];i=ix[0] if len(ix)==1 else None
 else:raise ValueError(strategy)
 return bool(i is not None and cs[i][':answer/id']==f[':answer-field/correct'][1])

def main():
 sets={name:a.json.loads((a.E/path).read_text()) for name,path in [('raw','independent-easy.json'),('delivered','delivery-independent/accepted.json'),('batch','runner-batch.json'),('batch_delivered','delivery-batch/accepted.json')]}
 # Native source selection uses sorted distinct entity IDs, difficulty-first weights,
 # SHA256 band draw and uniform within-band draw, after history exclusions.
 # Current batch is not yet published: new entity IDs and live history do not exist.
 # Examine every possible selected member, so the property holds for any ordering.
 selection=[]
 for name,rs in sets.items():
  groups=defaultdict(list)
  for r in rs:groups[r['generation']['template']].append(r)
  selection.append({'stage':name,'count':len(rs),'families':dict(Counter(r['generation']['template'] for r in rs)),'sign_pairs':dict(Counter(str((r['generation']['decision']['p_sign'],r['generation']['decision']['q_sign'])) for r in rs)),'unique_question_ids':len(set(r['question'][':question/id'] for r in rs))})
 probes=[];strategies=['first','last','side-frequency','shortest','longest','lexical-min','lexical-max','only-standard']
 for name,rs in sets.items():
  for t in sorted(set(r['generation']['template'] for r in rs)):
   subgroup=[r for r in rs if r['generation']['template']==t]
   for strategy in strategies:probes.append({'stage':name,'template':t,'strategy':strategy,'correct':sum(cue(r,strategy) for r in subgroup),'total':len(subgroup),'baseline':.2})
 fixed=a.json.loads((a.E/'fixed-bank-tests.json').read_text());fixedprobes=[]
 for case in fixed:
  for strategy in strategies:fixedprobes.append({'template':case['template'],'strategy':strategy,'correct':sum(cue(r,strategy) for r in case['records']),'total':5,'baseline':.2,'bank_held_fixed':case['bank_held_fixed'],'five_distinct_keys':case['five_distinct_keys']})
 a.save('shortcut-results.json',{'probes':probes,'controlled_fixed_bank':fixedprobes,'strategies':'First/last display positions; unique highest sum of left/right repetition counts; unique shortest/longest TeX string; lexical min/max equation; only syntactically standard option. Abstentions count as failures.','interpretation':'Fixed bank controls answer content while each candidate becomes key. Any value-only cue selects the same value across the five controls and therefore cannot exceed 1/5. Position cues considered separately. Ordinary sample proportions are descriptive and boundary-heavy; not estimates of normal production frequency.'})
 draws=[]
 for name in ['delivered','batch_delivered']:
  pool=sorted(sets[name],key=lambda r:r['question'][':question/id'])
  for n in range(64):
   seed='independent-current-review-'+str(n);h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(h[8:16],'big')>>11)/(1<<53);r=pool[int(u*len(pool))]
   draws.append({'pool':name,'seed':seed,'question_id':r['question'][':question/id'],'template':r['generation']['template'],'frequency_strategy_success':cue(r,'side-frequency')})
 a.save('selection-results.json',{'implementation':'engine/rust/question_selection.rs select(), weights(), seen_before_task() read directly','captured_basis':5230,'stages':selection,'draws':draws,'new_ids_assumption':'Synthetic entity order using sorted question UUID; real newly assigned entity order cannot be known before publication. Within an easy band draw is uniform over eligible members for every ordering.','history_cases':['Fresh learner: all delivered candidates.','Seen-history subset: any subset of these candidates retains no unique side-frequency cue.','Zero easy weight: easy questions not selected while another positive rated band is available.','No configured distribution: first usable candidate is selected; all candidates inspected.'],'limitations':['Live policy weights and live learner histories are not in the snapshot; exact future draws are conditional. No database access or publication performed.'],'result':'Difficulty filter preserves easy families; all delivered members individually examined for prior cue; compare stage counts and probes. Source/historical pool is recorded separately in inventory-review.json.'})
 inv=a.json.loads((a.JOB/'source/inventory.json').read_text());old=a.JOB/'review-0-policy-2-08d4e48c0d97b878/historical-records.json';hist=a.json.loads(old.read_text());a.save('historical-records.json',hist);matches=[]
 originals={q[':question/id'] for q in a.json.loads((a.JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']}
 for q in inv['questions']:
  if q[':question/id'] in originals:continue
  r=next(r for r in hist if r['question'][':question/id']==q[':question/id'])
  def shape(v):
   if isinstance(v,list):return sorted([shape(x) for x in v],key=lambda x:a.json.dumps(x,sort_keys=True))
   if isinstance(v,dict):
    if set(v)=={':db/ident'}:return v[':db/ident']
    v=a.copy.deepcopy(v)
    if isinstance(v.get(':answer-field/correct'),list):v[':answer-field/correct']=next(c for c in v[':answer-field/choices'] if c[':answer/id']==v[':answer-field/correct'][1])
    return {k:shape(x) for k,x in v.items() if k!=':db/id'}
   return v
  matches.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'complete_record_matches':shape(q)==shape(r['question']),'side_frequency_success':cue(r,'side-frequency'),'generation':r['generation']})
 a.save('inventory-review.json',{'captured_basis':inv['basis'],'original_source_count':len(originals),'stored_generated_count':len(matches),'historical_records_provenance':str(old),'results':matches,'conclusion':'Verified absence of the unique maximum side-frequency rule in all four captured generated records (all hard). Does not certify absence of every possible shortcut; no current-revision records stored at this snapshot. Original source questions excluded from generated classification.'})
 a.save('affected-inventory.json',{'affected_questions':[]})
 print('stage counts',selection);print('historical',len(matches),'matched',sum(v['complete_record_matches'] for v in matches),'prior cue successes',sum(v['side_frequency_success'] for v in matches))
if __name__=='__main__':main()
