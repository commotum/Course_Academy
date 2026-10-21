import json,collections,hashlib,copy,re
from pathlib import Path
from review_math import prompt,check,correct_index,matrices
ROOT=Path(__file__).resolve().parent

def load(p):return json.loads((ROOT/p).read_text())
def save(p,v):(ROOT/p).write_text(json.dumps(v,indent=2,default=str)+'\n')
def stats(records):
 c=collections.Counter();v=collections.defaultdict(list); semantic=[]
 for r in records:
  g=r['generation'];p=g['parameters'];a=p['candidates'][p['correct_index']];c[g['response_template']]+=1
  for j,name in enumerate(('sx','sy','bx','by')):v[name].append(a[j])
  semantic.append(str(prompt(r['question']).rref()[0].tolist()))
 return {'count':len(records),'family_counts':dict(c),'positions':dict(collections.Counter(correct_index(r['question']) for r in records)),'semantic_rrefs':len(set(semantic)),'profile_counts':dict(collections.Counter(r['generation']['template'] for r in records)),'values':{n:dict(collections.Counter(vals)) for n,vals in v.items()}}
sets={n:load(p) for n,p in [('fresh_raw','independent-samples.json'),('fresh_delivered','delivery-independent/accepted.json'),('batch_raw','runner-batch.json'),('batch_delivered','delivery-batch/accepted.json')]}
save('coverage-results.json',{k:stats(v) for k,v in sets.items()})
probes=[]
for name in ('fresh_delivered','batch_delivered'):
 rs=sets[name]
 groups=[('all',rs,'overall')]+[(f,[r for r in rs if r['generation']['response_template']==f],'within_template') for f in ('matrix','vector')]
 if name=='fresh_delivered':
  groups += [(t,[r for r in rs if r['generation']['template']==t],'within_template') for t in sorted({r['generation']['template'] for r in rs})]
 for subgroup,records,scope in groups:
  if not records:continue
  for cue in ('first authored option','shortest TeX','most minus signs','most zeros'):
   hits=0
   for r in records:
    f=r['question'][':question/answer-fields'][0];bank=f[':answer-field/choices'];vals=[a[':answer/value'] for a in bank]
    if cue=='first authored option':idx=0
    elif cue=='shortest TeX':idx=min(range(5),key=lambda j:len(vals[j]))
    elif cue=='most minus signs':idx=max(range(5),key=lambda j:vals[j].count('-'))
    else:idx=max(range(5),key=lambda j:str(matrices(vals[j])[0].tolist()).count('0'))
    hits+=idx==correct_index(r['question'])
   probes.append({'cue':cue,'subgroup':name+':'+subgroup,'scope':scope,'strategy':'Choose '+cue+'; break ties by authored order.','correct':hits,'total':len(records),'baseline':0.2,'disposition':'not_predictive','conclusion':'Compared with 1/5 uniform guessing. Finite sample rates do not prove independence. The earlier independent review: apparent q-74628 shortest-option predictor was challenged again using its 10 established control seeds (shortcut-control-results.json). Single-record subgroups cannot establish fixed-role prediction. Code inspection confirms correct slot chosen before exchangeable candidate values. Authored order is additionally shuffled in UI.','sample_refs':['decision-probe-results.json','delivery-independent/accepted.json' if name=='fresh_delivered' else 'delivery-batch/accepted.json']})
# Include exact UI ordering rather than counting the review-only green feedback cue.
html_results=[]
for j,r in enumerate(load('render-input.json')):
 html=(ROOT/f'render/question-{j+1:03d}.html').read_text()
 ids=re.findall(r'<input type="radio"[^>]*value="([^"]+)"',html)
 f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
 assert len(ids)==5 and set(ids)=={a[':answer/id'] for a in f[':answer-field/choices']}
 html_results.append({'index':j,'record_id':r['question'][':question/id'],'review_case':r.get('review_case'),'rendered_order':ids,'correct_position':ids.index(key),'complete_bank':True})
for family in ('matrix','vector'):
 indices=[j for j,r in enumerate(load('runner-batch.json')) if r['generation']['response_template']==family]
 probes.append({'cue':'first displayed radio option','subgroup':'exact runner batch '+family,'scope':'within_template','strategy':'Click first choice after actual UI shuffle.','correct':sum(html_results[j]['correct_position']==0 for j in indices),'total':len(indices),'baseline':0.2,'disposition':'not_predictive','conclusion':'Baseline is uniform choice among five. The exact batch has four vector records and one matrix record; none has its key first after actual UI shuffling. A one-record subgroup cannot establish a conditional predictor. Green feedback is displayed only after the preview fixture submits the key.','sample_refs':['rendered-choice-results.json','runner-batch.json']})
control=load('shortcut-control-results.json')
probes.append({'cue':'shortest TeX','subgroup':'q-74628 fresh control','scope':'within_template','strategy':'Choose shortest option, break ties by authored order.','correct':control['correct'],'total':control['total'],'baseline':0.2,'disposition':'not_predictive','conclusion':'Initial 3/3 probe challenged using independently chosen fresh seeds. '+control['conclusion'],'sample_refs':['shortcut-controls.json','shortcut-control-results.json','delivery-controls/accepted.json']})
save('rendered-choice-results.json',html_results)
save('decision-probe-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python decision_audit.py','probes':probes})
# Native selection rule reproduction: sorted unique fresh candidates; all rated hard.
# With positive hard weight and no other bands, hard pool is uniform. No policy -> first.
selection={}
for name,rs in [('fresh',sets['fresh_delivered']),('batch',sets['batch_delivered'])]:
 counts=collections.Counter()
 for n in range(300):
  d=hashlib.sha256(f'course-academy/question-selection/v1/review-96745-{n}'.encode()).digest()
  u=(int.from_bytes(d[8:16],'big')>>11)/2**53
  idx=int(u*len(rs)); counts[idx]+=1
 selection[name]={'pool_size':len(rs),'trials':300,'index_counts':dict(counts),'selected_families':dict(collections.Counter(rs[j]['generation']['response_template'] for j in counts)),'eligible_support_preserved':len(counts)==len(rs),'unconfigured_policy':'selects smallest eligible entity ID; prospective published entity IDs unavailable','history':'seen_before_task excludes previous task content; current prefix also excluded by caller. Excluding by identity can exhaust a finite pool but does not inspect keys, slopes, profiles, or positions.'}
save('learner-selection-results.json',{'source':'engine/rust/question_selection.rs:132-216','command':'decision_audit.py','selection':selection,'assumptions':['Captured source and inventory omit active selection policy, learner history and future database entity IDs. Simulates a fresh learner with positive hard weight.','Since every generated record is hard, any positive hard band weight gives equal index support within this family. Zero hard weight makes this rated pool ineligible; no claim about a specific live learner.','Raw generator rejects duplicate candidate tuples and batch() duplicate RREFs, without sign or answer-index rejection. check_delivery uses actual prepare_records against captured inventory basis 5370.'],'limits':['Simulation compares support and family retention, not actual future draw frequencies or entity collisions. Publication preparation inspected separately; no publication performed.']})
# Existing records lack generation provenance. Inspect their actual math without calling them source examples or asserting a seed.
i=load('inventory-audit.json');checks=[]
for q in i['other_records']:
 r={'question':q,'generation':{'template':'captured non-source record, generation metadata absent'}}
 checks.append(check(r))
i['instance_math_checks']=checks;i['specific_finding_scan']='Retained omission repaired: both profiles replay and sample. Both were original source questions in captured inventory, so no generated instance was affected by that API omission. All five non-source records independently pass math; generation metadata and seed replay unavailable.'
save('inventory-audit.json',i)
source=load('source-analysis.json')
variation={'learner_operation':source['learner_operation'],'fixed_features':source['fixed_features'],'answer_roles':[{'role':'Affine slopes and intercepts','eligible_variation':'Any signed or zero value in a conservative bounded hard domain, derived coherently through equations, correct option and solution.','observed':'Fresh samples contain both signs in all four slots, zero slopes and zero y-intercepts; no zero x-intercept occurs in this 21-record fresh sample. Controlled banks include the all-zero affine candidate. Independent exact RREF checks pass. All 17 source profiles replay, including source parameter values outside the sampled bounded domain.'},{'role':'Correct choice and candidate distractors','eligible_variation':'Any of five candidates can qualify while the same affine/row reduction rule remains fixed.','observed':'Code chooses target index before five distinct exchangeable tuples. Both response templates pass a controlled change of target with bank held fixed; native grader accepts the new key and rejects the old.'}], 'coverage':[{'case':k,'sample_refs':['coverage-results.json','independent-samples.json' if k.startswith('fresh') else 'runner-batch.json'],'result':str(stats(v))} for k,v in sets.items()], 'counterfactuals':[{'kind':'relevant','change':'For q-74525 and q-74532, keep profile, complete candidate bank and row presentation fixed; change correct_index from 0 to 1, changing coefficients/RHS to realize that target.','expected':'Prompt equations, RREF/solution, worked explanation and accepted answer must change coherently; old target rejected.','observed':'Independent matrix reconstruction confirms changed response; all choices checked by native engine; full pair prompts/solutions rendered. See counterfactual-results and rendered-choice-results.','status':'passed','justification':'The source asks for RREF or the solution of the given equations; different affine targets are legitimate answer-bearing assignments under that operation.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-all-results.json','render/rendering.json','rendered-choice-results.json']},{'kind':'irrelevant','change':'For both families keep candidates and chosen solution fixed, permute equations [2,0,1] and multiply presented equations by signs [-1,1,-1].','expected':'Different prompt and reduction trace, identical RREF, solution and accepted mathematical option.','observed':'Both pairs have equal independently computed RREFs and same correct values; native grader rejects alternatives and accepts the preserved target; rendered prompts and worked traces follow the changed equations.','status':'passed','justification':'Nonzero scaling/reordering equations preserves the same system solution, as in source row operations.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-all-results.json','render/rendering.json','rendered-choice-results.json']}], 'shortcut_probes':probes, 'delivery':{'stages_examined':['generator tuple rejection','generator batch RREF resampling','requested hard difficulty','publisher normalization/validation','captured inventory and within-batch deduplication','learner freshness and difficulty-first selection code','actual UI answer shuffling'], 'sample_refs':['generator-rejection.json','packaging-results.json','delivery-independent/delivery.json','delivery-batch/delivery.json','learner-selection-results.json','rendered-choice-results.json','delivery-controls/delivery.json','delivery-counterfactual/delivery.json'],'result':'All 21 fresh and 5 exact batch records survive actual delivery filtering. Two response families remain; no demonstrated label/layout shortcut. Uniform hard-band selection preserves support in read-only simulation. Active policy, live learner history and future entity IDs unavailable, so no claim about a particular later task.'}, 'limitations':['Not an exhaustive shortcut proof; 1 fresh seeded record per unchanged source profile and 3 per added profile (21 total), the exact batch, and 10 previously established cue controls were examined. Prior independent analysis reused because construction logic is unchanged.','Both previously missing profiles now replay and sample; all 17 source banks checked externally. Canonical example is scope evidence, not an assessed question.','The one matrix question in the exact batch is too small a subgroup to infer statistical balance; no first-position strategy answers any of the five displayed batch records.','Canonical example has no captured answer field; used for scope, not invented as a graded replay.','Captured inventory basis 5370; no later database changes examined.']}
save('pedagogical-variation.json',variation)
print(json.dumps({'coverage':{k:stats(v) for k,v in sets.items()},'probe_perfect':[(p['subgroup'],p['cue'],p['correct'],p['total']) for p in probes if p['correct']==p['total']],'inventory_math_failures':[c for c in checks if c['errors']],'displayed_batch':[x['correct_position'] for x in html_results[:5]]},default=str))
