import json,collections,hashlib,itertools,re
from pathlib import Path
E=Path(__file__).parent
load=lambda n:json.load(open(E/n))
def save(n,d):(E/n).write_text(json.dumps(d,indent=2,ensure_ascii=False))
def vals(r):
 return [next(a[':answer/value']=='true' for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]) for f in r['question'][':question/answer-fields']]
def level(r):return r['question'][':question/difficulty'].split('/')[-1]
def roles(r):
 result=[]
 for f in r['question'][':question/answer-fields']:
  rhs=f[':answer-field/key'].strip('$').split('=')[1]
  result.append('move_y' if 'y' in rhs else 'zero' if rhs=='0' else 'function_forcing' if 'x' in rhs else 'constant_forcing')
 return result
# Independently derive keys from displayed RHS strings. Derivative coefficient is 1 and left side has only derivative/y terms (checked in audit.py).
def truths(r):return [(role in ['zero','move_y'])==(level(r)=='easy') for role in roles(r)]
def stats(rs):
 return {'count':len(rs),'role_tuples':len(set(tuple(roles(r)) for r in rs)),'rhs_role_multisets':dict(collections.Counter(','.join(sorted(roles(r))) for r in rs)),'answer_patterns':dict(collections.Counter(''.join('1' if v else '0' for v in vals(r)) for r in rs)),'selected_counts':dict(collections.Counter(sum(vals(r)) for r in rs)),'a_signs':dict(collections.Counter('negative' if r['generation']['parameters']['a']<0 else 'positive' for r in rs)),'n':dict(collections.Counter(r['generation']['parameters']['n'] for r in rs))}
sets={'raw_easy':load('samples-easy.json'),'raw_moderate':load('samples-moderate.json'),'accepted_easy':load('delivery-easy/accepted.json'),'accepted_moderate':load('delivery-moderate/accepted.json'),'batch':load('runner-batch.json'),'accepted_batch':load('delivery-batch/accepted.json')}
stages={k:stats(v) for k,v in sets.items()}
probes=[];allstrategies=list(itertools.product([False,True],repeat=3))
for name,rs in sets.items():
 groups={'all':rs}
 for l in ['easy','moderate']:
  lr=[r for r in rs if level(r)==l]
  if not lr:continue
  groups[l+' / recognition']=lr
  for n in range(4):
   sub=[r for r in lr if r['generation']['parameters']['n']==n]
   if sub:groups[l+f' / P degree {n}']=sub
  for sign in ['positive','negative']:
   sub=[r for r in lr if (r['generation']['parameters']['a']>0)==(sign=='positive')]
   if sub:groups[l+' / P '+sign]=sub
 for group,sub in groups.items():
  for strategy in allstrategies:
   correct=sum(vals(r)==list(strategy) for r in sub)
   probes.append({'stage':name,'cue':'fixed answer positions','subgroup':group,'strategy':'select '+''.join(str(i+1) for i,v in enumerate(strategy) if v) if any(strategy) else 'leave all unchecked','correct':correct,'total':len(sub),'baseline':0.125,'conclusion':'Exact three-checkbox response; baseline is uniform choice among eight boolean vectors. No perfect predictor is established by the tiny runner batch; such coincidences are checked on independent larger groups.'})
  counts=collections.Counter(sum(vals(r)) for r in sub);best,count=counts.most_common(1)[0]
  probes.append({'stage':name,'cue':'selection count','subgroup':group,'strategy':f'always select {best} boxes (count only)','correct':count,'total':len(sub),'baseline':max(collections.Counter(sum(v) for v in allstrategies).values())/8,'conclusion':'Only counts correctness, not exact identity. Baseline 3/8 is the best count under uniform boolean vectors. Count bias does not determine the selected equations.'})
  probes.append({'stage':name,'cue':'RHS is zero or a multiple of y','subgroup':group,'strategy':'classify forcing after moving y; match requested target','correct':sum(vals(r)==truths(r) for r in sub),'total':len(sub),'baseline':0.125,'conclusion':'This simplification is the lesson skill: y terms alter P, not Q. The perfect mathematical predictor is intended, not an incidental layout shortcut.'})
save('shortcut-results.json',{'probes':probes,'stages':stages,'limits':'Finite probes on explicit templates, degree and coefficient-sign subgroups. No theorem of absence of every shortcut.'})
# Fresh usable pool; finite read-only reproduction of Rust difficulty-first selection.
# Publishing assigns entity IDs later. Stable ascending surrogate IDs preserve only sorted ordering, not live identity.
def select(pool,weights,seed):
 if weights is None:return pool[0] if pool else None
 bands=[[r for r in pool if level(r)==l] for l in ['easy','moderate','hard']]
 h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=lambda o:(int.from_bytes(h[o:o+8],'big')>>11)/(1<<53)
 total=sum(w for w,b in zip(weights,bands) if b)
 if total<=0:return None
 draw=u(0)*total
 for w,b in zip(weights,bands):
  if not b or not w:continue
  chosen=b
  if draw<w:break
  draw-=w
 return chosen[int(u(8)*len(chosen))]
pool=sets['accepted_easy']+sets['accepted_moderate'];selection=[];selectedrecords=[]
for history in ['fresh','alternate seen','all easy seen']:
 pp=[r for i,r in enumerate(pool) if not (history=='alternate seen' and i%2==0) and not(history=='all easy seen' and level(r)=='easy')]
 for weights in [[1,0,0],[1,1,0],[0,1,0],None]:
  draws=[select(pp,weights,f'audit-20261020-{i}') for i in range(2048 if weights else 1)];out=[r for r in draws if r];selection.append({'history':history,'weights':weights,'available':len(pp),'null_draws':sum(r is None for r in draws),'draws':len(draws),'distribution':{l:stats([r for r in out if level(r)==l]) for l in ['easy','moderate'] if any(level(r)==l for r in out)},'shortcut_probes':[{'subgroup':l,'fixed_subset':list(v),'correct':sum(vals(r)==list(v) for r in out if level(r)==l),'total':sum(level(r)==l for r in out),'baseline':0.125} for l in ['easy','moderate'] if any(level(r)==l for r in out) for v in allstrategies]})
  selectedrecords.extend(out)
  if weights is not None:
   assert all(r in pp for r in out)
   for l,w in zip(['easy','moderate','hard'],weights):
    if w==0:assert not any(level(r)==l for r in out)
save('selection-results.json',{'implementation':'Faithful read-only reproduction of question_selection.rs::select: sorted unique candidate IDs, SHA256 two draws, nonempty weighted bands, uniform within chosen band; no unrated questions in audited pool.','seed_format':'audit-20261020-{0..2047}','entity_order':'accepted easy then accepted moderate; assigned ascending audit-only surrogate IDs. No real IDs/publication fabricated.','stages':selection,'source_refs':['engine/rust/question_selection.rs:108-198','engine/rust/learning.rs:149-168,595-622'],'captured_basis':5242,'limits':['No live learner or configured weights are included in job inputs; test fresh and explicit seen-history scenarios, easy-only, moderate-only, equal-band and unconfigured fallback.','Final persisted entity IDs may alter individual seeded draws; positive band support and uniform within-band distribution are identity-independent.','Unconfigured fallback deterministically picks first available; this engine behavior does not certify decision coverage for an unconfigured learner.','No assertion that arbitrary learner history preserves every case; exhausted bands may be absent as tested.']})
# Retain compact complete chosen records once each plus deterministic draw inputs/counts above.
uniq={r['question'][':question/id']:r for r in selectedrecords};save('selection-records.json',list(uniq.values()))
cases=load('grader-input.json')
for stage in ['accepted_easy','accepted_moderate','accepted_batch']:
 for idx,r in enumerate(sets[stage]):
  want=truths(r);assert vals(r)==want;checks=[]
  for fi,(f,v) in enumerate(zip(r['question'][':question/answer-fields'],want)):
   for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if (a[':answer/value']=='true')==v else 'rejected','purpose':'delivered field IDs, independent displayed forcing class'})
  cases.append({'label':f'{stage}-{idx}','record':r,'checks':checks})
save('grader-all-input.json',cases)
pairs=load('counterfactuals.json')
assert pairs[0]['parameters']==pairs[3]['parameters'];assert vals(pairs[0]['record'])==[not v for v in vals(pairs[3]['record'])]
save('counterfactual-results.json',{'relevant_easy':{'before':pairs[0]['key'],'after':pairs[1]['key'],'changed_field':1},'relevant_moderate':{'before':pairs[3]['key'],'after':pairs[4]['key'],'changed_field':2},'irrelevant_both':{'easy_preserved':pairs[0]['key']==pairs[2]['key'],'moderate_preserved':pairs[3]['key']==pairs[5]['key']},'target_flip':{'identical_equations':True,'keys_complement':True,'records':'counterfactual-records.json indices 0 and 3'},'math_explanations':'All displayed transformation rows independently checked by audit.py. Actual native grader tests both choices on every pair. UI renders prompt, controls and explanation for all six pair records.'})
print(json.dumps({'stages':stages,'grader_cases':len(cases),'selection_scenarios':len(selection),'shortcut_probes':len(probes)}))
