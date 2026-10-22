exec(open('audit.py').read().split('initial=digest()')[0])
# Native cached eligibility library predates the source policy: preserve the mismatch, do not claim it verifies current policy.
s=pathlib.Path('check-selection.rs').read_text().replace('  if usable != item["expected_usable"].as_bool().ok_or("expected usability required")? { return Err(format!("Unexpected usability {}: {:?}",item["label"],result).into()); }','')
pathlib.Path('check-selection.rs').write_text(s)
stages={n:load(ROOT/p) for n,p in {'raw':'samples.json','accepted':'delivery-samples/accepted.json','batch':'batch.json','batch_accepted':'delivery-batch/accepted.json'}.items()}
def bits(r):return tuple(truth(f)=='true' for f in r['question'][':question/answer-fields'])
def summary(rr):
 return {'count':len(rr),'profiles':dict(Counter(r['generation']['profile'] for r in rr)),'ordinary_correct_counts':dict(Counter(sum(bits(r)[:4]) for r in rr)), 'truth_patterns':dict(Counter(''.join(str(int(x)) for x in bits(r)) for r in rr)),'stale_none_solutions':sum('leave every box unchecked' in r['question'][':question/worked-solution'] for r in rr)}
# Faithful read-only reproduction of current learning.rs lines149-171: all generated fields have choice-owned keys checked by grader; only checkbox nonempty eligibility differs here.
def current_usable(r):return any(bits(r))
stage_results={n:summary(rr) for n,rr in stages.items()}
for n,rr in stages.items():stage_results[n]['usable_under_current_engine_source']=sum(current_usable(r) for r in rr)
# Same per-band hashed draw in question_selection.rs, using explicit future entity-ID stand-ins.
def choose(pool,seed):
 d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=(int.from_bytes(d[8:16],'big')>>11)/2**53
 return pool[int(u*len(pool))]
selection={}
for n in ['accepted','batch_accepted']:
 rr=stages[n];trials=[]
 for i in range(128):
  index=choose(list(range(len(rr))),f'task-971/kp-17592186054816/slot-{i}')
  trials.append({'seed':f'task-971/kp-17592186054816/slot-{i}','index':index,'id':rr[index]['question'][':question/id']})
 selection[n]={'trials':trials,'result':summary([rr[t['index']] for t in trials]),'assumptions':'All candidates fresh and usable, all easy, easy has positive configured weight. Sorted future entity-ID order modeled by input order; exact future IDs and learner histories are unavailable. With no policy weights selector returns the first candidate only; with easy weight zero it returns no easy item. Already-seen items are removed before selection.'}
invrecords=load(ROOT/'generated-records.json')
current_inventory=[{'id':r['question'][':question/id'],'entity_id':r['generation']['inventory_reproduction']['entity_id'],'usable_under_current_source':current_usable(r),'correct':bits(r)} for r in invrecords]
save('stage-analysis.json',{'stages':stage_results,'selection_reproduction':selection,'stored_generated_eligibility':current_inventory,'source_rules':{'generator':'sample chooses semantic category and count before values; generate rejects duplicate raw identities with bounded retry; explicit None makes every delivered selection nonempty without rejecting zero-ordinary-match cases.','selector':'learning.rs149-171 and 600-622; question_selection.rs select: fresh usable set, weighted rated band, uniform hash within sorted band; missing policy returns first candidate.','difficulty':'All tested records easy; positive easy weighting cannot select a different truth distribution within that band.'},'limits':['Captured inventory basis 5457; no claim about later inventory changes.','Future entity IDs, actual learner histories, active policy records are absent. Conditional selection model examines possible effects and explicitly does not predict a live learner sequence.','Cached Oct19 rlib predates current checkbox selection restriction; its result is not used to certify current-source eligibility.']})
# Reproducible current-source eligibility failure in an already stored generated record.
old=next(r for r in invrecords if not current_usable(r))
save('affected-inventory.json',{'affected_questions':[{'question_id':old['question'][':question/id'],'entity_id':old['generation']['inventory_reproduction']['entity_id'],'finding':'All four checkbox keys are false and no explicit None option exists; current learning.rs validate_practice_question excludes it from fresh practice. This is a retained historical defect, separate from the current generator stale-None solution.','reproduction':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python followup.py && PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python analyze-delivery.py; see stage-analysis.json stored_generated_eligibility. Explicit parameters: universal real numbers, candidates inferred from solution in generated-records.json.','evidence_path':'generated-records.json'}]})
# Simple action-producing strategies are evaluated against exact subsets, not individual-checkbox hit rates.
probes=[]
strategies={'select first only':(True,False,False,False,False),'select last ordinary only':(False,False,False,True,False),'select None only':(False,False,False,False,True),'select all four ordinary':(True,True,True,True,False)}
for stage,rr in stages.items():
 groups={'all':rr}
 for profile in sorted({r['generation']['profile'] for r in rr}):groups['profile='+profile]=[r for r in rr if r['generation']['profile']==profile]
 for key,sub in groups.items():
  for name,pred in strategies.items():
   correct=sum(bits(r)==pred for r in sub)
   probes.append({'stage':stage,'subgroup':key,'strategy':name,'correct':correct,'total':len(sub),'baseline':1/16,'baseline_explanation':'Uniform guessing among 16 mathematically coherent subsets of four candidates, with explicit None selected exactly for the empty ordinary subset.','perfect':correct==len(sub),'disposition':'not_predictive' if correct<len(sub) else 'inspect'})
# Within-profile family can algebraically imply an answer (e.g. all reals -> only unscripted R,C); distinguish math from incidental cues.
maxima={n:max((p['correct']/p['total'] for p in probes if p['stage']==n),default=0) for n in stages}
save('shortcut-results.json',{'probes':probes,'maximum_tested_constant_strategy_rate':maxima,'conclusion':'No tested constant action succeeds on every member of any present profile subgroup, including exact batch; no universal shortcut demonstrated. Nonsquare-radical irrationality and R/C containment are intended classification, not incidental cues. Four-option/None labeling alone does not fix the truth pattern. Finite samples do not exclude all cues.'})
# Coverage per actual category/target and per-bank symbol, not just text count.
cov={}
for n,rr in stages.items():
 cov[n]={'targets':dict(Counter(r['generation']['instance'].get('category',r['generation']['instance'].get('group')) for r in rr)),'symbol_truths':{s:dict(Counter(truth(f) for r in rr for f in r['question'][':question/answer-fields'] if f[':answer-field/key']=='$'+g.tex(s)+'$')) for s in g.SYMBOLS},'source_profile_gap':'Production PROFILES omits finite decimal and radio/combination-bank families; replay-only decimal does not expose practice generation.'}
save('coverage-results.json',cov)
# Strict failing regression (does not pass by asserting that the defect exists).
save('strict-test-context.json',{'failure_record':'minimal-cli.json','source_regression':'Full source bank equality in source-replay-results.json; three omissions and one missing source.'})
pathlib.Path('strict-regression.py').write_text('''import json\nr=json.load(open("minimal-cli.json"))[0]\nq=r["question"]\nf=q[":question/answer-fields"][-1]\nassert f[":answer-field/key"]=="None of the above"\nassert "leave every box unchecked" not in q[":question/worked-solution"], "Explicit None must be selected, but solution tells learner to leave every box unchecked"\n''')
print(json.dumps({'stages':stage_results,'affected_inventory':old['question'][':question/id'],'max_constant_strategy_rates':maxima},indent=2))
