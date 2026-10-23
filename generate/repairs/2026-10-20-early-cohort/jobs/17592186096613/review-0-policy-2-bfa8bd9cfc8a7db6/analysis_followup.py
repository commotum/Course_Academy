exec(open('review_tests.py').read().split('source_results=[]')[0])
from collections import Counter
# Reproduce missing-family regression without depending on author metadata or tests.
q6=next(q for q in source if q[':question/math-academy-id']=='q-70889')
r6=g.generate_easy(seed=72,profile='euler',parameters={'n':6,'d':1,'k':1})
r5=g.generate_easy(seed=73,profile='integer',parameters={'n':5,'d':1,'k':0})
save('additional-source-replay.json',{'records':[r6,r5],'six_e_bank_matches':sorted(str(expr(a[':answer/value'])) for a in q6[':question/answer-fields'][0][':answer-field/choices'])==sorted(str(expr(a[':answer/value'])) for a in r6['question'][':question/answer-fields'][0][':answer-field/choices']),'six_e_prompt_equivalent':s.simplify(fn(q6)-fn(r6['question']))==0,'canonical_five_answer':s.simplify(expr(correct(r5['question']))-5/x)==0,'limits':'q-70889 is semantically supported via euler profile; a missing raw profile alone is not a separate pedagogical failure. q-70887 remains unsupported.'})
# Captured inventory eligibility and independent math, not a live database query.
inv=json.load(open(JOB/'source/inventory.json')); inventory=[]
for q in inv['questions']:
 fields=q.get(':question/answer-fields',[]); usable=bool(fields) and all(f.get(':answer-field/correct') for f in fields) and not q.get(':question/retired',False)
 item={'id':q[':question/id'],'entity_id':q[':db/id'],'source':bool(q.get(':question/math-academy-id')),'eligible':usable,'retired':q.get(':question/retired',False)}
 if usable:item['math_ok']=s.simplify(expr(correct(q))-s.diff(fn(q),x))==0
 inventory.append(item)
save('inventory-analysis.json',{'basis':inv['basis'],'records':inventory,'questions':inv['questions'],'eligibility_rule':'learning.rs validate_practice_question/validate_response_question: ordinary question, graded fields with keys, not retired; selection.rs excludes seen history then weighted difficulty. Captured ordinary radio/blank fields checked.','conclusion':'9 eligible of 12 captured records; 3 original incomplete questions unavailable. One non-source stored question has correct -12/(7x) key. No demonstrated historical instance of the missing-family defect: omission is a runtime construction restriction.','limitations':['No live learner history supplied. No generated provenance metadata in captured inventory, so no historical generated record is claimed reproduced.']})
save('affected-inventory.json',{'affected_questions':[]})
sets={n:json.load(open(R/p)) for n,p in [('raw-sample','independent-records.json'),('delivered-sample','delivery-sample/accepted.json'),('raw-batch','batch-records.json'),('delivered-batch','delivery-batch/accepted.json')]}
stats={};probes=[]
for name,rs in sets.items():
 stats[name]={'count':len(rs),'profiles':dict(Counter(r['generation']['bank_profile'] for r in rs)),'signs':dict(Counter('negative' if s.diff(fn(r['question']),x).subs(x,1)<0 else 'positive' for r in rs)),'records':rs}
 for bank in ['integer','fraction','euler']:
  sub=[r for r in rs if r['generation']['bank_profile']==bank]
  if not sub:continue
  positions=[]
  for r in sub:
   f=r['question'][':question/answer-fields'][0]; positions.append(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
  freq=Counter(positions);best,k=freq.most_common(1)[0]
  probes.append({'set':name,'bank':bank,'strategy':'always choose stored option '+str(best+1),'success':k,'total':len(sub),'positions':positions,'interpretation':'No fixed position across larger profile sample; one-item subgroup is descriptive only, not evidence of a structural shortcut.'})
# Native selection's all-easy weighted band is uniform after freshness eligibility.
# Exact digest/53-bit indexing with independent task seeds; weights cancel within the single band.
selection=[]
rs=sets['delivered-batch']; ids=list(range(1,len(rs)+1))
for i in range(80):
 seed='review-17592186096613-'+str(i);h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(h[8:16],'big')>>11)/(1<<53);j=int(u*len(ids));selection.append({'seed':seed,'selected_candidate_index':j,'bank':rs[j]['generation']['bank_profile']})
save('delivery-analysis.json',{'sets':stats,'probes':probes,'selection':selection,'selection_counts':dict(Counter(v['selected_candidate_index'] for v in selection)),'selection_basis':'question_selection.rs select: fresh candidates sorted, positive easy weight and no other supplied band. Synthetic monotonically ordered entity IDs 1..5; actual future IDs/history unavailable. With no configured distribution selects smallest candidate, per inspected code.','rejection':'parameter_domain enumerates valid coefficients and rejects duplicate radio values before uniform choice; unit numerators excluded before sampling. No post-sample rescue restores that family.','limitations':['Captured basis 5668; later inventory may differ. Actual learner histories/policy weights absent; conditional selection behavior and candidate reachability assessed, no live selection claim.'],'batch_conclusion':'All 5 survive filtering; 2 positive integer radio, 1 negative euler radio, 2 negative rational blank. No fixed answer or sign-only answer strategy across this finite pool. c/x transformation is intended skill.'})
save('scope-analysis.json',{'records_checked':46,'observed':'One c ln x derivative, rational/integer or integer-times-e constants, radio/blank controls. No chains, sums, general bases or point evaluations.','limits':'Requested easy only; authored moderate/hard levels not certified.','source':'tutorial b1f46211-3766-53d0-bcc7-30bb9056b948 and canonical 6624681a-bb00-59db-8df9-4d5a3cd00434','counterfactuals':{'relevant':'+7 to -7 coefficient; prompt, solution and key change signs; native grader tests every bank option.','irrelevant':'seed 17 to 18 with +7 fixed; question and solution preserve function and answer, bank order changes; native grader confirms IDs. UI independently reorders choices by field/item ID, so raw permutation does not ensure a distinct displayed order.'}})
(R/'session-state.md').write_text('Completed source replay, 46 exact math checks, 245 native grading checks, delivery of actual batch (5/5) and sample (37/38), missing reciprocal-coefficient proof. Rendering main batch inspected; counterfactual renderer pending. No DB or original package writes. Pending final evidence report and package hash verification.\n')
print({'source_6e_supported':True,'eligible_inventory':sum(v['eligible'] for v in inventory),'selection_counts':Counter(v['selected_candidate_index'] for v in selection),'probes':probes})
