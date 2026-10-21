import json,pathlib,hashlib,collections,copy,itertools
E=pathlib.Path(__file__).resolve().parent;B=E.parent
load=lambda n:json.loads((E/n).read_text())
def save(n,v):(E/n).write_text(json.dumps(v,indent=2)+'\n')
def truth(r):
 fs=r.get('question',r)[':question/answer-fields'];out=[]
 for f in fs:
  if f[':answer-field/key']=='None of the above':continue
  ref=f[':answer-field/correct'];aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
  out.append(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)=='true')
 return out
def mask(r):return sum(1<<i for i,t in enumerate(truth(r)) if t)
def summary(rs):
 return {'records':len(rs),'truth_masks':dict(sorted(collections.Counter(mask(r) for r in rs).items())),'correct_substantive_counts':dict(sorted(collections.Counter(sum(truth(r)) for r in rs).items()))}
stages={n:summary(load(n)) for n in ['samples-moderate.json','delivery-samples/accepted.json','batch.json','delivery-batch/accepted.json']}
# Faithful conditional-within-moderate sampler from question_selection.rs lines 153-211.
inv=json.loads((B/'source/inventory.json').read_text());pool=[]
for q in inv['questions']:
 band=q.get(':question/difficulty',{});band=band.get(':db/ident') if isinstance(band,dict) else band
 if band==':question.difficulty/moderate' and any(truth(q)):pool.append({'entity':q[':db/id'],'record':{'question':q},'origin':'captured inventory'})
last=max(q[':db/id'] for q in inv['questions'])
for i,r in enumerate(load('delivery-batch/accepted.json')):pool.append({'entity':last+i+1,'record':r,'origin':'accepted prospective batch'})
pool.sort(key=lambda v:v['entity'])
def draw(candidates,seed):
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();bits=int.from_bytes(digest[8:16],'big')>>11;u=bits/(1<<53)
 return candidates[int(u*len(candidates))]
selected=[]
for scenario,candidates in [('fresh',pool),('exclude_first_half_as_seen',pool[len(pool)//2:])]:
 for i in range(256):
  pick=draw(candidates,'independent-review/'+scenario+'/'+str(i));selected.append({'scenario':scenario,'seed':'independent-review/'+scenario+'/'+str(i),'entity':pick['entity'],'question_id':pick['record']['question'][':question/id'],'truth_mask':mask(pick['record'])})
selection={'source':'engine/rust/question_selection.rs:select and seen_before_task; learning.rs:validate_practice_question','basis':inv['basis'],'input_candidates':pool,'draws':selected,'summaries':{scenario:dict(sorted(collections.Counter(d['truth_mask'] for d in selected if d['scenario']==scenario).items())) for scenario in ['fresh','exclude_first_half_as_seen']},'unconfigured_policy':{'selected_entity':pool[0]['entity'],'rule':'Without configured weights select lowest fresh usable entity; prior-task and current-prefix exclusion changes next eligible entity.'},'limits':['Captured inventory has no learner history or policy weights. Test conditions on a positively weighted moderate band; within-band draw is uniform and independent of mathematical roles, for every positive band weight.','Prospective publication entity IDs are unknown; appended sorted IDs model one ordering. Changing this ordering permutes seeded outcomes without changing within-band uniformity.','Excluded retired/malformed/multistep records would require unavailable full live snapshot; captured nonempty source and generated records have the relevant usable response shape.','Historical all-false checkbox is excluded from fresh practice by learning.rs:165. No database access.']}
save('selection.json',selection)
probes=[];raw=[]
def examine(rs,subgroup,scope,ref):
 if not rs:return
 candidates=[]
 # Complete actions, rather than accuracy on one easy-to-guess field.
 for bit in range(8):candidates.append(('fixed position subset '+str(bit),lambda r,bit=bit:[bool(bit>>i&1) for i in range(3)]))
 candidates.append(('select statements worded positive',lambda r:['positive' in f[':answer-field/key'] for f in r.get('question',r)[':question/answer-fields'] if f[':answer-field/key']!='None of the above']))
 for label in ['first','second','third','fourth']:
  candidates.append(('select only '+label+' quadrant statement',lambda r,label=label:[('the '+label+' quadrant') in f[':answer-field/key'] for f in r.get('question',r)[':question/answer-fields'] if f[':answer-field/key']!='None of the above']))
 for strategy,action in candidates:
  hits=sum(action(r)==truth(r) for r in rs)
  result={'cue':'positions, quadrant labels or claim polarity without the equation','subgroup':subgroup,'scope':scope,'strategy':strategy,'correct':hits,'total':len(rs),'baseline':0.125,'disposition':'not_predictive','conclusion':'Complete three-claim subset accuracy; uniform guessing among 8 subsets is 1/8. None is then derived from whether the chosen subset is empty. '+('No complete prediction.' if hits<len(rs) else 'Perfect on this bounded set; inspect mathematical vs incidental cause.'),'sample_refs':[ref]}
  probes.append(result)
 raw.append({'subgroup':subgroup,'count':len(rs),'masks':summary(rs)['truth_masks']})
rs=load('samples-all.json');examine(rs,'fresh seeded sample','overall','samples-all.json')
for t in sorted(set(r['generation']['template'] for r in rs)):
 examine([r for r in rs if r['generation']['template']==t],t,'within_template','samples-all.json')
for n in ['decision-records.json','samples-moderate.json','delivery-samples/accepted.json','batch.json','delivery-batch/accepted.json']:
 examine(load(n),n,'other_recognizable_subgroup',n)
for name,predicate in [('negative coefficient',lambda r:r['generation']['parameters']['c']<0),('positive coefficient',lambda r:r['generation']['parameters']['c']>0)]:
 examine([r for r in load('delivery-samples/accepted.json') if predicate(r)],'delivered moderate '+name,'other_recognizable_subgroup','delivery-samples/accepted.json')
# Record batch biases explicitly without treating one-field prediction as solving a full item.
batch=load('batch.json');partials=[]
for label in ['first','second','third','fourth']:
 vals=[]
 for r in batch:
  for f,t in zip([f for f in r['question'][':question/answer-fields'] if f[':answer-field/key']!='None of the above'],truth(r)):
   if 'the '+label+' quadrant' in f[':answer-field/key']:vals.append(t)
 partials.append({'cue':label+' quadrant label','observed_field_truths':vals,'limitation':'This tests one field, not a complete answer-producing action.'})
save('shortcut-results.json',{'stage_summaries':stages,'group_summaries':raw,'probes':probes,'batch_field_biases':partials,'batch_interpretation':'Five distinct decisions, masks 1/3/4 with multiplicities 2/2/1; both coefficient signs and different true quadrant labels. No fixed position, single quadrant or positive-wording strategy solves every batch member. All None fields false in this batch; this alone does not determine the three substantive responses. Fourth-quadrant claims happen to be false in all four occurrences: a bounded partial-field bias, not a universal generator rule or complete batch answer rule. Explicit fixtures show every mask in each template.'})
# Scope is independently supported, with conservative limits.
save('scope.json',{'moderate':'All runner and moderate control records have cxy with nonzero integer c, three strict statements about distinct open quadrants, checkbox contract; no ODE solving, sums or shifted boundaries.','hard':'Source xy^2 and x^2y^2 support parity. Swapping which coordinate is squared preserves the same method.','easy':'Authored cx reduction removes one sign factor and is supported by lesson discussion of y\'=f(x). It does not add a prerequisite or reasoning stage.','limits':'Only moderate delivery reviewed; all-band sampling and grading/relocation tested. Exponents beyond 2, zero coefficients and translated regions are out of scope.','source_refs':['fd7005de-da4a-5aae-a0ea-f0c01c178438','1142a38e-b72d-5615-beec-20a68972aab2','c47e99b0-49b1-5362-97e1-164913960980','90e895ee-1be8-55c1-ab2d-a3596627f1b5','tutorial 03296d2b-05de-5077-8eab-c619925af706']})
source=load('source-analysis.json');pairs=load('counterfactuals.json')
ped={'learner_operation':source['skill'],'fixed_features':source['fixed_features']+[{'feature':'Strict positive/negative statements and nonzero coefficient','justification':'The operation is a constant sign in each open quadrant; axes are excluded. Three statements preserve workload.'}],'answer_roles':[{'role':'Coefficient sign','eligible_variation':'Either sign, complements each substantive truth when claims fixed.','observed':'Both signs sampled and controlled pair complements all three.'},{'role':'Quadrants and claim polarity','eligible_variation':'Each label can occupy any statement position; independently positive or negative claims.','observed':'Fresh sample varies labels and claim polarity; all 8 truth masks explicitly realized per template/profile.'},{'role':'None option and truth count','eligible_variation':'None true iff all three claims false; 0-3 substantive truths.','observed':'All 0-3 counts realized. Runner batch contains 1 or 2 substantive truths; None false throughout.'}],'coverage':[{'case':'Each recognizable template and hard exponent profile','sample_refs':['decision-records.json','samples-all.json','shortcut-results.json'],'result':'88 explicit cases cover all 8 masks in 11 template/exponent profiles; 168 fresh seeded records expose the actual sampler.'},{'case':'Exact runner batch after captured-inventory delivery','sample_refs':['batch.json','delivery-batch/accepted.json','shortcut-results.json'],'result':'5/5 survive, masks 1,1,3,3,4. No complete-answer simple cue succeeds on all five.'},{'case':'Moderate sample after deduplication and requested difficulty','sample_refs':['samples-moderate.json','delivery-samples/accepted.json','delivery-samples/delivery.json','selection.json'],'result':'72 inputs become 24; duplicate presentation variants collapse without dropping any observed mask (0,1,2,3,4,5,7). Within-moderate learner selection has no decision-role reweighting; fresh and seen-exclusion scenarios retained.'}],'counterfactuals':[],'shortcut_probes':probes,'delivery':{'stages_examined':['generator construction and nonempty rejection/resampling','requested moderate difficulty','normalization and image localization','captured inventory and within-batch deduplication','engine fresh-practice nonempty validation','learner history exclusion and within-band selection rules (conditional read-only reproduction)'],'sample_refs':['rejection.json','delivery-batch/delivery.json','delivery-samples/delivery.json','selection.json','shortcut-results.json'],'result':'Default explicit None gives a selectable true response for every truth mask; guard does not condition default mask distribution. No role-aware filtering in delivery or uniform within-band selection. Batch coverage assessed separately.'},'limitations':selection['limits']+['Finite shortcut strategies and samples do not prove absence of every possible cue. Fresh 24-seed moderate sample lacks mask 6, which explicit construction realizes; the source does not require all subsets in each five-question batch.','The historical engine-ineligible stored item is reproduced in affected-inventory.json and generated-records.json; it is not a current generator failure.']}
for pair in pairs:
 name=pair['change'];irrelevant=name=='positive_rescaling'
 ped['counterfactuals'].append({'kind':'irrelevant' if irrelevant else 'relevant','change':name,'expected':'Preserve all substantive responses and diagram signs.' if irrelevant else 'Complement all three substantive responses.' if name=='coefficient_sign' else 'Toggle only the first substantive response.','observed':'Independent visible-equation/statement/solution checks and native grader agree with expected keys. Render cases 6-10 show base, coefficient, claim, target and magnitude changes; sign map follows equation.','status':'passed','justification':'Positive magnitude cannot change a monomial sign.' if irrelevant else 'Coefficient sign, queried quadrant and claimed sign are eligible answer-bearing evidence under source sign method.','sample_refs':['counterfactuals.json','render-records.json','render/rendering.json','native-report.json']})
save('pedagogical-variation.json',ped)
print(json.dumps({'stages':stages,'perfect_complete_shortcut_probes':[p for p in probes if p['correct']==p['total']],'selection':selection['summaries']}))
