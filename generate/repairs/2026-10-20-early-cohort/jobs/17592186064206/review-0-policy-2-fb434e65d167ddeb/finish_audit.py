import collections,hashlib,json,pathlib,sys
sys.dont_write_bytecode=True
from audit import *
m=module(JOB/'workspace/17592186064206.py')
sets={name:load(ROOT/file) for name,file in {'raw':'independent-samples.json','delivered':'delivery-independent/accepted.json','batch_raw':'runner-batch.json','batch_delivered':'delivery-batch/accepted.json'}.items()}
stages={}
for name,rs in sets.items():
 stages[name]={'count':len(rs),'profiles':dict(collections.Counter(r['generation']['profile'] for r in rs)),'templates':dict(collections.Counter(r['generation']['template'] for r in rs)),'parameter_ranges':{k:sorted(set(r['generation']['parameters'][i] for r in rs)) for i,k in enumerate(['n','a','b'])},'probes':probes(rs)}
save('delivered-probes.json',stages)
# Trace the real deterministic duplicate-rejection loop on an independently chosen seed.
bs=m.batch('easy',15,77201);last=bs[-1]['generation']['seed'];raw=[m.generate(seed=s) for s in range(77201,last+1)];save('resampling-records.json',{'seed':77201,'count':15,'attempts':raw,'selected':bs,'rejected_offsets':[r['generation']['seed']-77201 for r in raw if r['generation']['seed'] not in {r['generation']['seed'] for r in bs}]})
# Faithful selection for one easy band, preserving caller supplied eligible candidate pools.
def select(ids,seed):
 ids=sorted(set(ids));d=hashlib.sha256(f'course-academy/question-selection/v1/{seed}'.encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/2**53
 return ids[int(u*len(ids))] if ids else None
rs=sets['batch_delivered'];ids=list(range(1,len(rs)+1));history=[]
for seed in range(8):
 pool=ids.copy();order=[]
 while pool:
  i=select(pool,f'review-{seed}-{len(order)}');pool.remove(i);order.append({'fixture_entity_id':i,'question_id':rs[i-1]['question'][':question/id'],'profile':rs[i-1]['generation']['profile']})
 history.append({'seed':seed,'order':order})
save('selection-analysis.json',{'implementation':'engine/rust/question_selection.rs select, lines 125-195; engine/rust/learning.rs validate_practice_question and validate_response_question, lines 149-245','inventory_basis':5669,'publication_present':(JOB/'publication/preparation.json').exists(),'selection_model':'Faithful hash and uniform choice within the sole easy band; positive easy weight. Fixture IDs are positional surrogate IDs, not claims about future entity IDs. Histories remove already selected items. All eligible positive-weight easy members remain selectable; weights/history never alter answer banks.','fixture_runs':history,'unweighted_policy':'Without configured weights the lowest candidate entity ID is selected. No particular prospective entity ID order is claimed.','eligibility':'Five keyed, non-retired, radio batch records. Inventory has five complete easy original questions and one unkeyed unusable source. No stored generated questions.','limits':['Learner policy, future database entity IDs and actual learner histories are not captured; no live exposure probabilities claimed.','Every possible subset of a defective recognizable bank family retains the same bank-only predictor; selector cannot eliminate that within-family fact.']})
cf=load(ROOT/'counterfactual-records.json')
def correctval(r):return next(a[':answer/value'] for a in field(r)[':answer-field/choices'] if a[':answer/id']==key(field(r)))
save('counterfactual-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python audit.py; native grader-input.json; render-counterfactual-records.json','relevant':{'before':cf[0],'after':cf[1],'change':'Numerator 2 -> 3, same slope 1 and intercept 7, template q-15707 and seed 912.','expected':'Correct coefficient 2 -> 3; substitution and final solution follow.','observed_answers':[correctval(cf[0]),correctval(cf[1])],'passed':correctval(cf[0])!=correctval(cf[1]) and all(check_math(r)['passed'] for r in cf[:2]),'shortcut_remains':probes(cf[:2])},'irrelevant':{'before':cf[0],'after':cf[2],'change':'Equal-ending vs Calculate wording; identical integral and same bank (q-15707 vs q-49453).','expected':'Mathematical response preserved; identifiers can change.','observed_answers':[correctval(cf[0]),correctval(cf[2])],'passed':correctval(cf[0])==correctval(cf[2]),'grading_evidence':'grader-results.json counterfactual cases each accept exactly the derivative-matching option','rendering_evidence':'render-counterfactual/rendering.json'}})
save('scope-analysis.json',{'records_checked':sum(len(x) for x in sets.values()),'in_scope':True,'reason':'Prompts all request a single integral of a constant over an affine expression; radio response is five logarithm-plus-C options. Worked solutions use one linear substitution, reciprocal integration and back substitution. Bounds have small integers, no sums of rational functions, powers, partial fractions, or absorbing C. Positive nonunit slope omission is restriction, not scope drift.','source_refs':load(ROOT/'source-analysis.json')['source_refs'],'math_evidence':'math-results.json','solution_inspection':'The fixed solution templates exactly reproduce five complete sources; numerator, slope inverse and affine substitutions are derived from bounded parameters. Canonical positive slope remains unsupported.'})
save('package-hashes-after.json',{p:hashlib.sha256((JOB/'workspace'/p).read_bytes()).hexdigest() for p in load(JOB/'workspace/package.json')['files']})
assert load(ROOT/'package-hashes-before.json')==load(ROOT/'package-hashes-after.json')
print(json.dumps({k:{'count':v['count'],'profiles':v['profiles'],'probes':[{a:b for a,b in p.items() if a!='cases'} for p in v['probes']]} for k,v in stages.items()},indent=2))
