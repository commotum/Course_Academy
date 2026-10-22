# Independent delivery, simple cue, selection and native grader inputs.
exec(compile(open('review.py').read().split('before=hashes();')[0], 'review-helpers', 'exec'))
# Definitions only from review.py (avoid rerunning completed sampler checks).
t=open('review.py').read();exec(t[t.index('def num(s):'):t.index('source=load(J/')])
raw=load(E/'raw-records.json');accepted=load(E/'delivery/accepted.json');batch=load(E/'delivery-batch/accepted.json')
def negative(r):return any(num(a[':answer/value'])<=0 for a in choices(r) if a[':answer/type']==':answer.type/math')
def signs(rs):
 return {'total':len(rs),'nonpositive_bank_count':sum(negative(r) for r in rs),'nonpositive_bank_no_solution':sum(negative(r) and truth(r)=='No solution' for r in rs),'positive_bank_count':sum(not negative(r) for r in rs),'positive_bank_no_solution':sum(not negative(r) and truth(r)=='No solution' for r in rs)}
# Probe the finite delivered pool separately. Subgroup cue needs no coefficient arithmetic.
probes=[]
def probe(cue,subgroup,scope,strategy,rs,predict,ref,disposition='not_predictive',comment=''):
 n=sum(canon(predict(r))==truth(r) for r in rs);probes.append({'cue':cue,'subgroup':subgroup,'scope':scope,'strategy':strategy,'correct':n,'total':len(rs),'baseline':.2,'disposition':disposition,'conclusion':f'{n}/{len(rs)}; baseline 0.2 is uniform selection among five choices. '+comment,'sample_refs':[ref]})
for label,rs,ref in [('raw',raw,'raw-records.json'),('post-filter',accepted,'delivery/accepted.json'),('exact batch',batch,'delivery-batch/accepted.json')]:
 probe('numeric order',label,'overall','Choose second-largest numeric option.',rs,lambda r:str(sorted(num(a[':answer/value']) for a in choices(r) if a[':answer/type']==':answer.type/math')[-2]),ref,comment='Repaired numeric rank varies; this old strategy has counterexamples.')
 cd=[r for r in rs if '{c}_{1}' in r['question'][':question/problem']]
 if cd:probe('c/d vector labels',label+' c/d','other_recognizable_subgroup','Choose No solution.',cd,lambda r:'No solution',ref,comment='Single-member batch subgroup alone is not treated as a defect; full controls contain both outcomes.')
 for sid in sorted({r['generation']['source_id'] for r in rs}):
  group=[r for r in rs if r['generation']['source_id']==sid]
  probe('coefficient-matrix signature',label+' '+sid,'within_template','Choose No solution.',group,lambda r:'No solution',ref,comment='Full controlled set supports both branches in each template; a one-member subgroup is not independently diagnostic.')
 neg=[r for r in rs if negative(r)]
 if neg:probe('signs of numeric answer choices',label+' contains a nonpositive numeric option','other_recognizable_subgroup','Choose No solution without reading vectors.',neg,lambda r:'No solution',ref,'not_predictive','Exact revised batch and controlled profiles contain counterexamples to the earlier sign strategy.')
# Native grader covers every choice on raw independent samples and exact normalized batch, one invocation.
rs=load(E/'source-records.json')+raw+batch
cases=[{'label':f'independent-{i}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if canon(a[':answer/value'])==truth(r) else 'rejected','purpose':'Fraction oracle on visible vectors; every authored radio alternative'} for a in choices(r)]} for i,r in enumerate(rs)]
save('grader-input.json',cases)
# Render the exact delivered batch and controlled relevant/irrelevant pair, plus restored rational source/profile.
render=batch+load(E/'counterfactual-records.json')
restored=load(E/'source-records.json')
render += [r for r in restored if r['generation']['source_id'] in ('q-105163','q-105164','q-105165','q-73957')]
render += [r for r in load(E/'boundary-records.json') if r['generation']['source_id']=='q-105163'][:1]
save('render-records.json',render)
save('shortcut-results.json',{'raw':signs(raw),'accepted':signs(accepted),'batch':signs(batch),'probes':probes,'batch_records':[{'id':r['question'][':question/id'],'profile':r['generation']['source_id'],'seed':r['generation']['seed'],'parameters':r['generation']['parameters'],'options':[a[':answer/value'] for a in choices(r)],'has_nonpositive':negative(r),'truth':truth(r)} for r in batch]})
# Faithful read-only reproduction of selection eligibility and SHA256 draw, conditional on staged synthetic entity IDs.
def select(candidates,distribution,seed,history=()):
 pool=sorted(set(candidates)-set(history))
 if distribution is None:return pool[0] if pool else None
 if distribution[1]<=0:return None
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/2**53
 return pool[int(u*len(pool))] if pool else None
ids=list(range(100,100+len(batch)));draws=collections.Counter(select(ids,[1,1,1],str(i)) for i in range(200))
history=[100];draws_history=collections.Counter(select(ids,[1,1,1],str(i),history) for i in range(200));assert 100 not in draws_history
assert set(draws)==set(ids) and select(ids,[1,0,1],'seed') is None
save('selection-results.json',{'source':'engine/rust/question_selection.rs: seen_before_task, select','captured_basis':5400,'publication_file':'Absent; shared check_delivery used instead.','raw_count':len(raw),'accepted_count':len(accepted),'batch_before':metrics(load(E/'batch.json')),'batch_after':metrics(batch),'pre_post_profiles':{s:{stage:metrics([r for r in items if r['generation']['source_id']==s]) for stage,items in [('raw',raw),('accepted',accepted)]} for s in sorted({r['generation']['source_id'] for r in raw})},'seed_trials':200,'synthetic_ids':ids,'draw_counts':dict(draws),'history_excluding_100_draws':dict(draws_history),'zero_moderate_weight_excludes_all':True,'unconfigured_policy_first_id':select(ids,None,'seed'),'rejection_resampling':'Current batch enforces all four sign/consistency combinations for count>=5; rejects repeated semantic fingerprints and whole pools lacking counterexamples for repeated recognizable groups; trace retained separately.','limits':['No concrete learner history, entity IDs or policy weights supplied. Every moderate fresh staged item remains eligible under positive moderate weight, equal probability within band. Exact future draws are unknown. History can remove counterexamples; no guarantee of balanced individual histories.','Inventory basis 5400 is captured; later concurrent writes may alter deduplication.'],'sign_shortcut_repaired':'All five exact batch items survive shared filtering. Both positive-only and nonpositive banks contain a numeric answer and No solution. Actual future history may remove counterexamples, as it can for any finite bank.'})
print(json.dumps({'grader_records':len(rs),'render_records':len(render),'signs':signs(batch)}))
