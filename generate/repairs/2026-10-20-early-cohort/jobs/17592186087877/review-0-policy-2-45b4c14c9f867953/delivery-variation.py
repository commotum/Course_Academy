import audit as a
import sympy as s,hashlib,collections,json,pathlib

def probe(rows):
 out=[]
 for r in rows:
  q=r['question'];hits=a.cue(q);cs=a.field(q)[':answer-field/choices'];k=a.correct_id(q)
  out.append({'question_id':q[':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],'parameters':r['generation']['parameters'],'bank_only_choice_ids':hits,'correct_choice_id':k,'correct':hits==[k],'correct_position':next(i+1 for i,c in enumerate(cs) if c[':answer/id']==k)})
 return {'total':len(rows),'successes':sum(z['correct'] for z in out),'by_template':{t:{'correct':sum(z['correct'] for z in out if z['template']==t),'total':sum(z['template']==t for z in out)} for t in sorted({z['template'] for z in out})},'records':out}
raw=a.load(a.EVID/'samples-independent.json');batch=a.load(a.EVID/'runner-batch.json');deliv=a.load(a.EVID/'delivery-independent/accepted.json');db=a.load(a.EVID/'delivery-batch/accepted.json')
pairs=a.load(a.EVID/'counterfactual-records.json')
reports={n:probe(r) for n,r in [('raw',raw),('runner_batch',batch),('delivered_independent',deliv),('delivered_batch',db),('controlled_pairs',pairs)]}
a.save('shortcut-results.json',{'strategy':'Ignore prompt and solution. Among exponential factors, select the one having both its reciprocal and its square present in the answer bank. Equivalent visible strategy: of the two same-sign exponential exponents, select the smaller absolute coefficient.','baseline':0.2,'baseline_explanation':'Uniform guessing among five radio choices.','stages':reports})
# Every normalized delivery record is independently parsed and sent to actual grader.
mc=[];gi=a.load(a.EVID/'grader-input.json')
for r in deliv+db:
 mc.append(a.math_check(r));q=r['question'];gi.append({'label':'delivered '+q[':question/id'],'record':r,'checks':[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==a.correct_id(q) else 'rejected','purpose':'Delivered normalized record: independent integrating-factor and RHS test'} for z in a.field(q)[':answer-field/choices']]})
a.save('delivery-math-results.json',mc);a.save('grader-input.json',gi)
# Counterfactual assertions independent of metadata.
def cv(r):
 q=r['question'];return next(z[':answer/value'] for z in a.field(q)[':answer-field/choices'] if z[':answer/id']==a.correct_id(q))
assert [a.ode(r['question'])[0] for r in pairs[:3]]==[1,-1,2]
assert [a.choice(cv(r))[0] for r in pairs[:3]]==[s.exp(a.x),s.exp(-a.x),s.exp(2*a.x)]
assert len({r['question'][':question/worked-solution'] for r in pairs[:3]})==3
assert pairs[0]['question'][':question/problem']==pairs[3]['question'][':question/problem']
assert pairs[0]['question'][':question/worked-solution']==pairs[3]['question'][':question/worked-solution']
assert a.correct_id(pairs[0]['question'])==a.correct_id(pairs[3]['question'])
assert a.field(pairs[0]['question'])[':answer-field/choices']!=a.field(pairs[3]['question'])[':answer-field/choices']
a.save('counterfactual-results.json',{'relevant':{'command':'audit.py constructs signed_constant_power seed=99017, n=3, a=1,-1,2','expected':'P changes sign/scale; correct factor and transformed RHS must follow.','observed_factors':['exp(x)','exp(-x)','exp(2x)'],'observed_prompt_and_solution_follow':True,'native_grader_evidence':'grader-report.json checks every option, including now-incorrect exp(x) for P=-1','rendered_evidence':'render-counterfactual/rendering.json; four screenshots inspected','bank_only_shortcut_persists':True},'irrelevant':{'change':'a=1,n=3 fixed; seed 99017 -> 99018 shuffles answer choices','same_prompt_solution_and_correct_id':True,'different_choice_order':True,'native_grader_evidence':'grader-report.json','rendered_evidence':'render-counterfactual/question-001.png and question-004.png'}})
# Inspect sampling rejection: all authored easy factors are pairwise inequivalent
# for any nonzero a; factor logarithmic derivatives are a,-a,2a,1/x,2/x.
# No legitimate nonzero a can make two of these equal as functions on an interval.
source=a.load(a.JOB/'source/source.json')['material']['kp'][':knowledge-point/questions']
inv=a.load(a.JOB/'source/inventory.json');historical=a.load(a.EVID/'generated-records.json');byid={r['question'][':question/id']:r for r in historical+deliv+db}
candidates={}
for q in inv['questions']:
 if ':answer-field/correct' not in a.field(q):continue
 band=q.get(':question/difficulty',{});band=band.get(':db/ident') if isinstance(band,dict) else band
 if band:candidates[q[':db/id']]={'id':q[':question/id'],'band':band.split('/')[-1],'defect':q[':question/id'] in byid and bool(a.cue(byid[q[':question/id']]['question']))}
# Synthetic future entity IDs only for read-only selection reproduction.
for i,r in enumerate(deliv+db):candidates[90000000000000+i]={'id':r['question'][':question/id'],'band':'easy','defect':True}
def select(cand,weights,seed):
 keys=sorted(cand)
 if weights is None:return keys[0] if keys else None
 bands=[[k for k in keys if cand[k]['band']==band] for band in ['easy','moderate','hard']]
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 def uniform(offset):return (int.from_bytes(digest[offset:offset+8],'big')>>11)/(1<<53)
 total=sum(w for w,b in zip(weights,bands) if b)
 if not total:return None
 draw=uniform(0)*total;pool=None
 for w,b in zip(weights,bands):
  if not b or w==0:continue
  pool=b
  if draw<w:break
  draw-=w
 return pool[int(uniform(8)*len(pool))]
selection=[]
for label,weights,seen in [('fresh_easy_only',[1,0,0],set()),('fresh_mixed_illustrative',[6,3,1],set()),('history_excludes_stored_easy',[1,0,0],{k for k,v in candidates.items() if k<90000000000000 and v['band']=='easy'}),('unconfigured',None,set())]:
 pool={k:v for k,v in candidates.items() if k not in seen};draws=[select(pool,weights,'independent-review-'+str(i)) for i in range(256)]
 cnt=collections.Counter(pool[k]['id'] for k in draws if k);hits=sum(pool[k]['defect'] for k in draws if k)
 selection.append({'case':label,'distribution':weights,'pool_size':len(pool),'draws':len(draws),'affected_draws':hits,'selected_question_counts':dict(cnt)})
a.save('selection-results.json',{'implementation':'Faithful read-only reproduction of engine/rust/question_selection.rs select: sorted entity candidates, rated bands, SHA256 deterministic uniforms at offsets 0 and 8, band draw then uniform member. Candidate usable sources and reproduced generated inventory plus accepted records with synthetic future entity IDs.','captured_basis':inv['basis'],'candidates':candidates,'cases':selection,'scope':'Actual per-learner history, future database IDs and configured policy are not captured. Illustrative distributions are explicit assumptions, not live-policy assertions. Every defective fresh record remains selectable under positive easy weight, and a history excluding old easy items leaves only defective new easy records. Unconfigured selects the smallest candidate ID and may defer these records.','rejection_and_resampling':'For every allowed nonzero easy a, bank factor logarithmic derivatives are a,-a,2a,1/x,2/x. They are distinct functions; exactly the first equals P=a. Thus the whole-bank rejection branch cannot break or filter the demonstrated signature. All 12 chosen samples accepted without parameter restriction; sample range includes positive and negative a.','before_after':{k:{'total':v['total'],'successes':v['successes'],'by_template':v['by_template']} for k,v in reports.items() if k!='controlled_pairs'}})
a.save('render-other-records.json',[raw[0],raw[4],a.load(a.EVID/'source-replay-records.json')[3],a.load(a.EVID/'source-replay-records.json')[7]])
a.save('scope-results.json',{'requested_difficulty':'easy','templates':['constant_cos','scaled_constant_power','signed_constant_power'],'source_comparison':'Constant P with signed small integer/simple fraction coefficients; powers n=1..4 and cos(bx); one common x leading factor for scaled source; no solution-for-y integration. All matches source method and easy workload. Q is not integrated in this task.','boundaries':'Explicit a=0, denominator 4, power 0, moderate template at easy, and free-entry response request rejected; see packaging-results.json.','supported_source_families':'All eight supplied source cases replayed, including moderate reciprocal and linear-P forms. No supplied hard source; exposed authored hard extension is outside this requested-easy delivery review.','source_prose':'Eight replay prompts/solutions read; canonical stages retained, negative-source sign corrected.','variation_limit':'All easy templates share the demonstrated incidental bank signature, so scope compliance does not establish meaningful decision variety.'})
print({k:(v['successes'],v['total']) for k,v in reports.items()});print('Selection affected draws',[(z['case'],z['affected_draws']) for z in selection])
