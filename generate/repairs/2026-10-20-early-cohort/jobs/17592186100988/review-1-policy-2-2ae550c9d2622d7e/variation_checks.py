import json,pathlib,re,collections,importlib.util,sys
R=pathlib.Path(__file__).resolve().parent;sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('g',R.parent/'workspace/17592186100988.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def load(p):return json.load(open(R/p))
def save(p,x):(R/p).write_text(json.dumps(x,indent=2))
def answer(r):
 f=r['question'][':question/answer-fields'][0];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def desc(records):
 radios=[r for r in records if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio')]
 return {'count':len(records),'templates':dict(collections.Counter(r['generation']['template'] for r in records)),'profiles':dict(collections.Counter(r['generation']['profile'] for r in records)),'dimensions':dict(collections.Counter(str([len(r['generation']['parameters']['matrix']),len(r['generation']['parameters']['matrix'][0])]) for r in records)),'valid':sum(answer(r)!='No such entry' for r in records),'absent':sum(answer(r)=='No such entry' for r in records),'radio_correct_positions':dict(collections.Counter(next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/value']==answer(r)) for r in radios))}
probes=[]
for file in ['samples.json','batch.json','delivery-sample/accepted.json','delivery-batch/accepted.json']:
 rs=load(file);radios=[r for r in rs if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio')]
 groups={'all radio':radios,'display radio with No such entry':[r for r in radios if '$$' in r['question'][':question/problem'] and any(a[':answer/value']=='No such entry' for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])]}
 for template in sorted(set(r['generation']['template'] for r in radios)):
  groups[template]=[r for r in radios if r['generation']['template']==template]
 for group,records in groups.items():
  if not records:continue
  for index in range(5):
   count=sum(r['question'][':question/answer-fields'][0][':answer-field/choices'][index][':answer/value']==answer(r) for r in records)
   probes.append({'file':file,'subgroup':group,'strategy':'choose stored position '+str(index+1),'correct':count,'total':len(records),'baseline':.2,'note':'Stored order is not UI order; UI renderer shuffled choices, so stored-order predictors alone are not learner shortcuts.'})
  if group=='display radio with No such entry':
   probes.append({'file':file,'subgroup':group,'strategy':'Eliminate No such entry using display layout only','correct':sum(answer(r)!='No such entry' for r in records),'total':len(records),'baseline':.8,'note':'Baseline .8 is safe-elimination chance for an arbitrary one of five options. This predicts one elimination, not the final numeric answer. Both existence cases are now supported in all radio layouts.'})
 summaries={file:desc(load(file)) for file in ['samples.json','batch.json','delivery-sample/accepted.json','delivery-batch/accepted.json']}
save('coverage-shortcuts.json',{'commands':'python variation_checks.py','summaries':summaries,'probes':probes})
# Instrument rejection/resampling with unchanged implementation, only observing calls.
original_guard=g.guard;original_sample=g.sample;attempts=[];active=False;profile=None

def guard(p,*args,**kw):
 if active:attempts.append({'profile':profile,'dimensions':[len(p['matrix']),len(p['matrix'][0])],'i':p['i'],'j':p['j']})
 return original_guard(p,*args,**kw)
def sample(level,rng,p):
 global active,profile
 active=True;profile=p
 try:return original_sample(level,rng,p)
 finally:active=False
g.guard=guard;g.sample=sample
replayed=[g.generate('easy',seed=s) for s in range(731100,731160)]
save('resampling.json',{'seeds':[731100,731159],'attempts':attempts,'attempt_count':len(attempts),'accepted_count':len(replayed),'matches_uninstrumented':replayed==load('samples.json'),'pre_profile_counts':dict(collections.Counter(a['profile'] for a in attempts)),'post_profile_counts':dict(collections.Counter(r['generation']['profile'] for r in replayed)),'interpretation':'Profile selected before rejection. Invalid swap locations, duplicate location recipes or scalar collisions resample the complete instance within that profile. No profile is dropped; shape and target frequencies within a profile are conditional on valid recipes.'})
# Pair outcomes: explicitly submit before and after answers against both questions.
grade=load('grader-input.json');pairs=load('counterfactual-records.json')
for pair in load('counterfactual-results.json'):
 vals=[pair['before_answer'],pair['after_answer']]
 for side in ['before','after']:
  r=pairs[pair[side+'_index']];f=r['question'][':question/answer-fields'][0];checks=[]
  for v in set(vals):
   if f[':answer-field/type'].endswith('/blank'):
    checks.append({'submitted':v,'expected':'accepted' if v==answer(r) else 'rejected','purpose':'controlled pair: before/after response'})
   else:
    for choice in f[':answer-field/choices']:
     if choice[':answer/value']==v:checks.append({'submitted_answer_id':choice[':answer/id'],'expected':'accepted' if v==answer(r) else 'rejected','purpose':'controlled pair: before/after response'})
  grade.append({'label':f"controlled-{pair['before_index']}-{side}",'record':r,'checks':checks})
save('grader-input.json',grade)
# Source-only pool eligibility and selection rule.
inv=load('../source/inventory.json');eligible=[];excluded=[]
for q in inv['questions']:
 reason='retired' if q.get(':question/retired') else 'missing correct reference' if any(':answer-field/correct' not in f for f in q.get(':question/answer-fields',[])) else None
 (excluded if reason else eligible).append({'id':q[':question/id'],'entity_id':q[':db/id'],'reason':reason})
save('selection-analysis.json',{'captured_basis':inv['basis'],'eligible_originals':eligible,'excluded_originals':excluded,'candidate_batch':summaries['delivery-batch/accepted.json'],'rules':['learning.rs validate_practice_question excludes retired and missing correct reference records.','question_selection.rs seen_before_task plus caller prefix removes prior exposures.','select deduplicates and sorts candidates; for positive easy weight, all eligible easy candidates are uniform within that band; no profile or format weighting.','Without configured distribution, first sorted candidate is returned. Explicit zero easy weight excludes all easy candidates rather than restoring missing cases.'],'conclusion':'Five original questions are graded and not retired; two original inline questions have no correct reference and are ineligible. No stored generated records exist at this basis. Current candidate batch and its counts are recorded above; both existence cases survive filtering. No universal answer-value or choice-position shortcut is demonstrated in the batch. The missing branch is documented, not rejected solely for its absence from five draws.','limits':['No learner history or policy distribution supplied; exact next question cannot be predicted. Selection supports any fresh candidate in its positive-weight difficulty band; none of its rules fixes generator coverage restrictions.','Capture is basis5665; later inventory changes are outside this review.']})
print(json.dumps({'summaries':summaries,'attempt_count':len(attempts),'display_elimination':[p for p in probes if p['strategy'].startswith('Eliminate')]} ,indent=2))
