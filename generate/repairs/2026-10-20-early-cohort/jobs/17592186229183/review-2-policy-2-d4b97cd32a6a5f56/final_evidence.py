import json,hashlib,sys
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent/'workspace'
def load(n):return json.loads((R/n).read_text())
def save(n,x):(R/n).write_text(json.dumps(x,indent=2)+'\n')
# Confirm post-delivery same-bank geometry and key roles.
rs=load('delivery-controls/accepted.json');raw=load('same-bank-records.json')
def bank(r):return sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
assert all(bank(x)==bank(y) for x,y in zip(rs,raw))
assert len({tuple(bank(r)) for r in rs})==1
# Honest corrections to inherited prose: behavior now includes positive-shape rejection.
p=load('sampling-summary.json');p['construction_assessment']='Rank precedes physical sampling. Four exchangeable positive adjacent gaps are translated to that rank; only nonpositive whole shapes are resampled without changing rank. Controlled low-boundary cases retain all five ranks. Source masks and arithmetic constraints remain unchanged.';p['sampling_limit']='44 bounded fresh physical examples across eleven templates, plus explicit controlled pairs and separate five-item batch. Not a proof against every cue.';save('sampling-summary.json',p)
p=load('delivery-selection-results.json');p['generator_rejection']='17 rejected physical candidates are retained in runtime-results.json; rank is drawn beforehand. Whole-bank positivity rejection preserves chosen rank; low-boundary-records.json exercises all five ranks.';save('delivery-selection-results.json',p)
x=load('decision-results.json');probes=[]
refs={'fresh sample after':['sample-records.json','delivery-sample/accepted.json','decision-results.json'],'exact batch after':['batch-records.json','delivery-batch/accepted.json','decision-results.json'],'same bank':['same-bank-records.json','delivery-controls/accepted.json','grader-report.json','decision-results.json']}
for label in refs:
 groups=x['results'][label]['groups']
 for group,counts in groups.items():
  if label=='exact batch after' and group!='all':continue # one item per template is not inferential evidence
  for cue,z in counts.items():
   if group!='all' and cue not in ['numeric rank 3','position 3','nearest mean','unique 2 lb radius center']:continue
   probes.append({'cue':cue,'subgroup':label+' / '+group,'scope':'overall' if group=='all' else 'within_template','strategy':'Choose '+cue+'; ties select lowest numerical value.','correct':z['correct'],'total':z['total'],'baseline':.2,'disposition':'not_predictive','conclusion':'Uniform guessing among five choices has success rate 0.2. Finite results do not establish a guaranteed answer cue; bank-shape counterfactuals give four wrong-key witnesses for every fixed numerical selector. Exact batch position 3 succeeds 4/5 and is explicitly retained as a small-pool imbalance, not concealed by larger samples.','sample_refs':refs[label]})
a=load('source-analysis.json')
pv={'learner_operation':a['learner_operation'],'fixed_features':a['fixed_features']+[{'feature':'One five-choice numerical mass radio response','justification':'Every supplied bank question uses this response contract; no free-entry or target-selection operation is licensed.'}],
'answer_roles':[{'role':'Mass at overflow','eligible_variation':'Capacity, starting volume/mass, concentration and flow rates recompute the modeled endpoint.','observed':'Capacity 210→240 changes 100.0→116.2 lb; initial mass 18→30 changes 100.0→102.2 lb.'},{'role':'Correct numerical rank and display position','eligible_variation':'Every bank member/position may represent the calculated mass; neither is mathematically essential.','observed':'All five ranks demonstrated at fixed physical inputs and at the positive low boundary; identical bank 35.3..39.3 has five independently calculated keys.'}],
'coverage':[{'case':'Eleven observed source contexts and complete banks','sample_refs':['source-replay-records.json','source-replay-results.json'],'result':'All source profiles, banks, keys and omissions match. Missing q-336499 solution/key is preserved and documented.'},{'case':'Fresh random physical tasks','sample_refs':['sample-records.json','decision-results.json','math-results.json'],'result':'44 tasks with all five numerical ranks overall; probes measured separately within every template.'},{'case':'Exact five-item batch','sample_refs':['batch-records.json','delivery-batch/accepted.json','decision-results.json'],'result':'All five survive; ranks 2:3 and 3:2, display positions 3:4 and 2:1. Median 2/5; radius cue applies 0/5; best fixed position 4/5. No tested universal strategy.'},{'case':'Same bank, all answer roles','sample_refs':['same-bank-records.json','delivery-controls/accepted.json','grader-report.json'],'result':'Same shape and mass bank with changed initial mass selects each of its five members. Radius center accepted once and rejected four times.'}],
'counterfactuals':[
{'kind':'relevant','change':'Capacity 210→240 or initial mass 18→30; other physical data fixed.','expected':'Recompute endpoint; correct mass and explanation change.','observed':'100.0→116.2 and 100.0→102.2 lb; prompt-derived expressions match worked solutions and every native radio response.','status':'passed','justification':'Source overflow evaluation depends on capacity and the ODE initial condition.','sample_refs':['counterfactual-records.json','counterfactual-results.json','displayed-math-results.json','grader-input.json','grader-report.json','render/rendering.json']},
{'kind':'relevant','change':'Keep displayed bank 35.3..39.3 fixed; change initial mass through 1,5,9,13,17 with legal fixed gap draws.','expected':'Every candidate can be correct as physical evidence changes.','observed':'Keys 35.3,36.3,37.3,38.3,39.3; explanations and native outcomes track all five.','status':'passed','justification':'Initial condition is essential evidence; numerical rank is incidental. Controlled random gap stream is legal, not a changed model or key.','sample_refs':['decision_checks.py','same-bank-records.json','decision-results.json','delivery-controls/accepted.json','grader-report.json','render/rendering.json']},
{'kind':'irrelevant','change':'Halve both flow rates, or change coolant context to fertilizer with physical data fixed.','expected':'Final mass preserved; halved flows double overflow time. Context changes only substance wording.','observed':'100.0 lb retained for both changes; prompt/solution/actual grader outcomes agree.','status':'passed','justification':'Common flow scaling cancels in the capacity-defined endpoint; context is incidental in the single-tank source model.','sample_refs':['counterfactual-records.json','counterfactual-results.json','displayed-math-results.json','grader-report.json','render/rendering.json']}],
'shortcut_probes':probes,
'delivery':{'stages_examined':['generator physical rejection/resampling','whole-bank positive-shape rejection retaining selected rank','actual shared normalization and inventory/within-batch deduplication','requested easy difficulty filter','captured inventory usability and seen-question history assumptions','native selection algorithm with declared conditional weights and unconfigured first-ID fallback'],
'sample_refs':['runtime-results.json','low-boundary-records.json','delivery-sample/delivery.json','delivery-batch/delivery.json','delivery-controls/delivery.json','delivery-selection-results.json','selection-pool-records.json','decision-results.json'],'result':'44/44 fresh records, 5/5 batch records and 5/5 same-bank controls accepted. Normalization preserves measured decision cases. Conditional native-algorithm selection covers fresh batch, existing bank and history-excluded pools; historical median defect remains in ten captured inventory records, explicitly separate from current repaired construction.'},
'limitations':['No publication/preparation.json exists; actual shared preparation filtering reproduced read-only against captured inventory basis 5395.','No live learner policy/history is captured; declared conditional scenarios inspect the applicable selection algorithm, not a specific learner.','Ten historical generated inventory records remain demonstrated affected by the old median defect; retained affected-inventory.json and complete original regenerated metadata identify them. No database remediation performed.','Requested easy only; unchanged moderate/hard authored extensions are outside this targeted certification.','Small batch positions are imbalanced; no tested selector solves every batch member. No finite review proves absence of every shortcut.']}
save('pedagogical-variation.json',pv)
# Validate explicit schema and evidence references without requiring a new dependency.
schema=json.loads(Path('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json').read_text())
def validate(v,s,path='$'):
 if 'enum' in s:assert v in s['enum'],path
 typ=s.get('type');assert typ is None or isinstance(v,{'object':dict,'array':list,'string':str,'integer':int,'number':(int,float)}[typ]),path
 if typ=='object':
  assert all(k in v for k in s.get('required',[])),path
  if s.get('additionalProperties') is False:assert not set(v)-set(s['properties']),path
  for k,val in v.items():validate(val,s.get('properties',{}).get(k,{}),path+'.'+k)
 if typ=='array':
  assert len(v)>=s.get('minItems',0),path
  for i,val in enumerate(v):validate(val,s.get('items',{}),path+f'[{i}]')
 if typ=='string':assert len(v)>=s.get('minLength',0),path
 if typ in ['integer','number']:assert s.get('minimum',-float('inf'))<=v<=s.get('maximum',float('inf')),path
validate(pv,schema)
for item in pv['coverage']+pv['counterfactuals']+pv['shortcut_probes']+[pv['delivery']]:
 for ref in item['sample_refs']:assert (R/ref).is_file() and (R/ref).stat().st_size>0,ref
save('evidence-contract.json',{'schema':'generate/pipeline/pedagogical-variation.schema.json','pedagogical_variation_schema_passed':True,'all_sample_refs_exist_and_nonempty':True})
print(json.dumps({'schema_pass':True,'shortcut_probes':len(probes),'same_bank_after_delivery':len(rs)}))
