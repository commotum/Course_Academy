"""Independent decision cases and read-only learner-selection reproduction."""
from independent_lib import *
from fractions import Fraction
def cases(records):
 counts=collections.Counter()
 for r in records:
  h,force,v=params_from_prompt(r);counts['total']+=1
  text=r['question'][':question/problem'].split('$$')[1].split('=',1)[1].split(r',\,')[0]
  rates=[texparse(z).coeff(x) for z in re.findall(r'\{e\}\^\{([^{}]+)\}',text)]
  position=next((i+1 for i,k in enumerate(rates) if k==h),0)
  counts['resonant_position_'+str(position)]+=1
  alpha=[S.expand(force).coeff(S.exp(k*x))/(1 if k==h else k-h) for k in rates]
  A=v-sum(z for k,z in zip(rates,alpha) if k!=h)
  counts['A_zero' if A==0 else 'A_positive' if A>0 else 'A_negative']+=1
  counts['h_positive' if h>0 else 'h_negative']+=1
  counts['first_rate_above_h' if rates[0]>h else 'first_rate_below_h' if rates[0]<h else 'first_rate_equal_h']+=1
 return dict(counts)
sets={'batch_raw':load(ROOT/'runner-batch.json'),'batch_delivered':load(ROOT/'delivery-batch/accepted.json'),'easy_raw':load(ROOT/'independent-easy.json'),'easy_delivered':load(ROOT/'delivery-independent/accepted.json'),'hard_raw':load(ROOT/'hard-samples.json'),'hard_delivered':load(ROOT/'delivery-hard/accepted.json'),'fresh_mixed':load(ROOT/'hard-samples.json')[9:33],'historical_generated':load(ROOT/'generated-records.json')}
save('coverage-results.json',{n:cases(rs) for n,rs in sets.items()})
def features(r):
 h,f,v=params_from_prompt(r);text=r['question'][':question/problem'].split('$$')[1].split('=',1)[1].split(r',\,')[0]
 rates=[texparse(z).coeff(x) for z in re.findall(r'\{e\}\^\{([^{}]+)\}',text)]
 pos=next((i+1 for i,k in enumerate(rates) if k==h),0)
 return pos,{'h_sign':'positive' if h>0 else 'negative','rate_order':'ascending' if rates[0]<rates[1] else 'descending','first_coefficient_sign':'negative' if text.startswith('-') else 'positive'}
groups=collections.defaultdict(list)
for r in sets['fresh_mixed']:
 pos,fs=features(r);groups['all_fresh_mixed'].append((r,pos))
 for k,v in fs.items():groups[k+':'+v].append((r,pos))
probes=[]
for name,rows in groups.items():
 correct=sum(pos==1 for r,pos in rows);total=len(rows)
 probes.append({'cue':'Last forcing position; '+name,'subgroup':'fresh mixed '+name,'scope':'within_template' if name=='all_fresh_mixed' else 'other_recognizable_subgroup','strategy':'Use an ordinary exponential trial for the second term without comparing its exponent with h.','correct':correct,'total':total,'baseline':max(correct,total-correct)/total,'disposition':'not_predictive' if correct<total else 'defect','conclusion':'Observed '+str(correct)+'/'+str(total)+'. Baseline is the best constant binary role guess within this subgroup. Both trial roles occur here; position/sign/order supplies no perfect action rule. Exponent equality itself is the intended mathematical test.','sample_refs':['hard-samples.json','shortcut-results.json']})
assert all(p['disposition']=='not_predictive' for p in probes)
probes += [
 {'cue':'Single nonresonant easy IVP','subgroup':'Exact runner batch after delivery','scope':'within_template','strategy':'Always use ordinary exponential trial, then solve its coefficient and initial constant.','correct':5,'total':5,'baseline':0.5,'disposition':'intended_skill','conclusion':'Binary uninformed trial guess baseline 0.5. All rated easy sources fix nonresonance; this supplies neither scalar coefficient nor full solution and is a justified easy scope.','sample_refs':['runner-batch.json','delivery-batch/accepted.json','math-results.json']},
 {'cue':'Given initial value v and complementary rate h','subgroup':'Exact runner batch','scope':'overall','strategy':'Copy v*exp(h*x) as the complete answer, omitting forcing.','correct':0,'total':5,'baseline':0,'disposition':'not_predictive','conclusion':'Baseline 0 for this strategy because nonzero forcing rules out the homogeneous-only response; measured 0/5. Five keys have differing rates and rational coefficients, not sign-only variants.','sample_refs':['runner-batch.json','math-results.json']},
 {'cue':'Last forcing position in unchanged historical hard pool','subgroup':'Five reproduced stored generated records','scope':'other_recognizable_subgroup','strategy':'Always assign an ordinary exponential trial to the second forcing term.','correct':5,'total':5,'baseline':0.5,'disposition':'defect','conclusion':'Binary trial baseline 0.5. This historical cohort still has the prior shortcut, including four mixed records. It is not a defect of the repaired sampler; affected-inventory.json retains exact records for separate downstream remediation.','sample_refs':['generated-records.json','affected-inventory.json','inventory-reproduction-results.json']}
]
historical_probe=probes.pop()
save('historical-shortcut.json',{'prior_probe':historical_probe,'retired':True,'current_eligible_affected':0,'eligibility_evidence':'inventory-eligibility.json'})
save('shortcut-results.json',{'fresh_mixed_probes':probes[:-2],'batch_probes':probes[-2:],'parameter_source':'Visible prompts parsed independently, not template metadata','scope':'Fresh mixed seed range 230101..230124 and exact requested batch. No claim of exhaustive shortcut absence.'})
# Mirror select() in question_selection.rs, including difficulty and history filtering.
def select(candidates,weights,seed):
 cs=sorted(candidates,key=lambda q:q['entity'])
 if weights is None:return cs[0] if cs else None
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 def u(off):return (int.from_bytes(digest[off:off+8],'big')>>11)/2**53
 bs=[[q for q in cs if q['band']==band] for band in ['easy','moderate','hard']];unrated=[q for q in cs if q['band'] is None]
 total=sum(w for w,qs in zip(weights,bs) if qs);pool=unrated
 if total>0:
  draw=u(0)*total
  for w,qs in zip(weights,bs):
   if not qs or w==0:continue
   pool=qs
   if draw<w:break
   draw-=w
 return pool[int(u(8)*len(pool))] if pool else None
inventory=load(JOB/'source/inventory.json');historical={r['question'][':question/id']:r for r in sets['historical_generated']}
pool=[]
for q in inventory['questions']:
 if q.get(':question/retired',False):continue
 if not q.get(':question/worked-solution') or not q[':question/answer-fields'][0].get(':answer-field/choices'):continue
 band=q.get(':question/difficulty');band=band.get(':db/ident') if isinstance(band,dict) else band
 pool.append({'entity':q[':db/id'],'id':q[':question/id'],'band':band.split('/')[-1] if band else None,'record':historical.get(q[':question/id'])})
# Prospective normalized records have content UUIDs but no DB entity IDs. Assign a deterministic
# order solely to exercise the uniform within-band rule; any actual ordering has equal mass.
freshpool=[dict(entity=max(q['entity'] for q in pool)+i+1,id=r['question'][':question/id'],band='hard',record=r) for i,r in enumerate(sorted(sets['hard_delivered'],key=lambda r:r['question'][':question/id']))]
scenarios=[]
for name,cs,weights in [('captured_easy',pool,[1,0,0]),('captured_hard',pool,[0,0,1]),('prospective_hard',pool+freshpool,[0,0,1]),('prospective_some_seen',pool+freshpool[5:],[0,0,1]),('no_policy',pool,None),('only_second_position_fresh_remaining',[q for q in freshpool if features(q['record'])[0]==2],[0,0,1])]:
 draws=[select(cs,weights,'independent-review-'+str(i)) for i in range(128)]
 roles=collections.Counter(str(features(q['record'])[0]) for q in draws if q and q['record'])
 scenarios.append({'name':name,'eligible':len(cs),'draws':len(draws),'bands':dict(collections.Counter(q['band'] for q in draws if q)),'hard_resonance_position_counts':dict(roles),'selected_question_ids':sorted({q['id'] for q in draws if q})})
 if name.startswith('prospective_') and name!='prospective_some_seen' or name=='prospective_some_seen':assert roles['1'] and roles['2']
selection={'implementation_sha256':hashlib.sha256((REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'inventory_basis':inventory['basis'],'scenarios':scenarios,'method':'Exact digest, 53-bit uniform draws, difficulty-first weights and sorted distinct entities from question_selection.rs select. History represented by removal.','limits':['Live learner policy and histories are absent.','Prospective entity order is assigned deterministically; actual future entity IDs are unknown. Uniform within-band mass does not depend on that order.','Unconfigured selection picks the lowest entity; exhausted histories may leave one role. No per-learner coverage guarantee.','Four affected historical mixed records are retired and excluded from current practice. The remaining generated hard question is a legitimate both-nonresonant case.']}
save('selection-results.json',selection)
pv={'learner_operation':'Compare each forcing rate with the supplied complementary exponent, choose ordinary or x-multiplied exponential trial, solve its coefficient, impose y(0), and enter an explicit equivalent solution.',
 'fixed_features':[{'feature':'One blank, supplied complementary solution, initial point 0','justification':'All source IVPs and canonical d2382def-85b2-5002-9614-692f272355c8 isolate this same simple initial-constant step.'},{'feature':'Easy is one nonresonant term; moderate one resonant term','justification':'All rated sources fix these branches at their respective levels. Fixing this family does not fix the coefficients or full answer.'},{'feature':'Two distinct exponential rates at hard','justification':'Same-lesson examples 5e56989a-feb1-590a-8684-9442dee1b1cb and 1ea06d66-de30-514a-817f-8749abb4ab25 support two coefficient decisions without a new ODE method.'}],
 'answer_roles':[{'role':'Which mixed term requires x multiplication','eligible_variation':'Either term may share h. Position, coefficient sign and rate ordering are incidental.','observed':str(cases(sets['fresh_mixed']))+'; both positions survive all examined stages.'},{'role':'Complementary coefficient A','eligible_variation':'Positive, negative, fractional or zero as v and particular coefficients vary.','observed':str(cases(sets['batch_delivered']))+'; controlled cancellation included.'},{'role':'Forcing coefficient and rate','eligible_variation':'Signed small integers and either nonresonant rate ordering; answer coefficient derived from f/(k-h).','observed':str(cases(sets['easy_delivered']))}],
 'coverage':[{'case':n,'sample_refs':[{'batch_raw':'runner-batch.json','batch_delivered':'delivery-batch/accepted.json','easy_raw':'independent-easy.json','easy_delivered':'delivery-independent/accepted.json','hard_raw':'hard-samples.json','hard_delivered':'delivery-hard/accepted.json','fresh_mixed':'hard-samples.json','historical_generated':'generated-records.json'}[n],'coverage-results.json'],'result':str(cases(rs))} for n,rs in sets.items()],
 'counterfactuals':[
 {'kind':'relevant','change':'Hold forcing e^x+e^(2x) and v=0 fixed; change only h=1 to h=2.','expected':'Resonance transfers from first to second; response changes from (x-1)e^x+e^(2x) to -e^x+(x+1)e^(2x).','observed':'Both admitted. Prompt, trial, product-rule rows, equations, explanation and final response track h; native grader rejects old response on transfer and accepts the independently factored new response. Both rendered.','status':'passed','justification':'Tutorial e6655774-c9ab-58c6-bfec-5013b08b7918 defines overlap as the operative evidence, independent of position.','sample_refs':['hard-controlled-records.json','controlled-results.json','hard-math-results.json','grader-input.json','grader-delivered-report.json','render/rendering.json']},
 {'kind':'irrelevant','change':'Swap both forcing components, preserving coefficients, h and v; include signed boundary and A=0 pairs.','expected':'Same IVP and response; trial, derivative and explanation follow the resonant term to its new position.','observed':'All four reorder pairs admitted with equivalent independent solutions. Both minimum-case orders accept the same native response; rendered prompts and worked stages show the changed position.','status':'passed','justification':'Forcing addition is commutative. The specific first position in lesson example 1ea06d66-de30-514a-817f-8749abb4ab25 is incidental.','sample_refs':['hard-controlled-records.json','controlled-results.json','hard-math-results.json','grader-input.json','grader-delivered-report.json','render/rendering.json']},
 {'kind':'relevant','change':'For h=2,k=3,f=4 change initial v=1 to v=4.','expected':'A changes from -3 to 0 and solution reduces to 4e^(3x).','observed':'ODE and initial residuals zero; rendered prompt and solution show changed initial value and cancellation; original key rejected on changed instance.','status':'passed','justification':'Canonical IVP initial-constant reasoning and edaf01e0-f315-5b89-a42e-b20571efeafe support cancellation.','sample_refs':['counterfactual-records.json','math-results.json','grader-input.json','grader-delivered-report.json','render/rendering.json']},
 {'kind':'irrelevant','change':'Hold easy parameters fixed and change compact presentation profile, or seed only.','expected':'Equivalent answer and same native acceptance.','observed':'Independent solutions and native acceptance unchanged; compact solution rendered with source-supported condensed coefficient rows. Seed-only prompt unchanged.','status':'passed','justification':'Source q-332906 and q-332903 show compact/grouped layouts for the same method; seed has no mathematical role.','sample_refs':['counterfactual-records.json','grader-input.json','grader-delivered-report.json','render/rendering.json']}],
 'shortcut_probes':probes,
 'delivery':{'stages_examined':['Direct valid mixed-role sampling and explicit generator guards; no rejection/resampling loop','Shared publisher prepare_records validation and normalization','Requested-difficulty filtering','Within-batch and captured-inventory deduplication','Read-only difficulty-first, uniform-within-band learner selection with history removal'],'sample_refs':['runtime-results.json','construction-review.json','delivery-batch/delivery.json','delivery-hard/delivery.json','delivery-independent/delivery.json','delivery-stored/delivery.json','coverage-results.json','selection-results.json'],'result':'Requested batch 5 -> 5, independent easy 8 -> 8, focused hard 41 -> 41. Both mixed positions preserved. Stored 5 -> 0 on resubmission (deduplicated). Prospective selection reaches both repaired positions; historical-only pool retains prior limitation.'},
 'limitations':['Finite fresh sample is not proof against all shortcuts.','Original capture lacks key/solution/difficulty for two unrated practice questions; unknown source evidence is not invented.','Four historical mixed records are retired and excluded from eligible selection; affected-inventory.json is empty after verification, with historical evidence retained.','No live publication, database writes, learner histories or policy state used. Prospective entity ordering is a faithful conditional uniform-within-band analysis.']}
save('pedagogical-variation.json',pv)
print(json.dumps({'coverage':load(ROOT/'coverage-results.json'),'fresh_shortcut_probes':len(groups),'prospective_selection_passed':True},indent=2))
