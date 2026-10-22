import json,re,collections,sys
from pathlib import Path
E=Path(__file__).resolve().parent
# Reuse independently written parser; audit.py is executable and writes only evidence.
exec((E/'audit.py').read_text().split('src=json.load')[0])
batch=json.load(open(E/'runner-batch.json'));samples=json.load(open(E/'independent-samples.json'));accepted=json.load(open(E/'delivery-batch/accepted.json'));ac_samples=json.load(open(E/'delivery-samples/accepted.json'))
reproduced=g.batch(seed=2086806769,count=5);assert reproduced==batch
save('batch-reproduction.json',{'command':'python -B decision_review.py','call':'g.batch(difficulty="moderate", count=5, seed=2086806769)','matches_runner_batch':True,'records':reproduced})
def group(r):
 q=r['question'];fs=q[':question/answer-fields'];ss=[f[':answer-field/key'] for f in fs] if len(fs)==3 else re.findall(r'(?:^|\n)(?:I|II|III)\. (.*)',q[':question/problem'])
 def c(s):
  for cue,tag in [('basis','basis'),('pivot','pivot'),('Col','col'),('rank','rank'),('nullity','nullity'),('Null','null'),('det','det'),('invertible','inv'),('Ax=','null-solution')]:
   if cue in s:return tag
  raise ValueError(s)
 return ('checkbox' if len(fs)==3 else 'radio')+':'+','.join(c(s) for s in ss)
def stage(rows):
 out={}
 for r in rows:
  key=group(r);out.setdefault(key,[]).append({'id':r['question'][':question/id'],'mask':bits(r),'template':r['generation']['template']})
 return out
stages={name:stage(rows) for name,rows in [('raw_samples',samples),('accepted_samples',ac_samples),('runner_batch',batch),('accepted_batch',accepted)]}
sub=[r for r in accepted if group(r)=='checkbox:det,col,pivot'];assert len(sub)==2
shortcut=sum(bits(r)==[False,True,False] for r in sub);assert shortcut==2
ctrl=[r for r in samples if group(r)=='checkbox:det,col,pivot'];control_hits=sum(bits(r)==[False,True,False] for r in ctrl)
save('minimal-failing-case.json',{'command':'python -B decision_review.py','seed':2086806769,'records':sub,'strategy':'For the checkbox det/column-space/pivot triplet, select only its column-space option (second visible field), ignoring the premise and signs.','correct':shortcut,'total':len(sub),'baseline':1/7,'control_correct':control_hits,'control_total':len(ctrl),'family_rule_to_change':'During finite batch selection, when this recognizable three-concept checkbox family repeats, retain different qualifying subsets rather than two sign variants of the same middle-only decision. Preserve the broad valid generator domain.','defect_scope':'The exact surviving five-record batch, within its two-record repeated checkbox family. Not a universal defect in generate().'})
# A strict failure test is retained; expected to fail on current batch, not concealed as passing.
result={'name':'repeated_checkbox_family_decision_varies','passed':len({tuple(bits(r)) for r in sub})>1,'expected':'more than one true subset across this repeated concept triplet','observed':{'count':len(sub),'masks':[bits(r) for r in sub]},'failure_is_expected_on_reviewed_batch':True}
save('batch-acceptance-test.json',result)
coverage={}
for r in samples:
 sid=r['generation']['template'];p=r['generation']['parameters'];z=coverage.setdefault(sid,{'masks':set(),'statuses':set(),'hypotheses':set(),'count':0});z['masks'].add(tuple(bits(r)));z['statuses'].add(p['invertible']);z['hypotheses'].add(p['hypothesis']);z['count']+=1
for x in coverage.values():
 for k in ['masks','statuses','hypotheses']:x[k]=sorted(x[k])
# Learner-selection implementation only conditions on rated band and freshness, not response masks.
selection={'source':'engine/rust/question_selection.rs select(), seen_before_task()','captured_basis':5418,'candidate_rule':'Fresh usable candidate IDs deduplicated and sorted; seen-before-task and current-prefix exclusion precede select. Difficulty band selected by positive configured weights; uniform seeded ID choice within eligible band. Without policy weights selects first ID.','applicable_batch_result':'All five delivery survivors are moderate. With fresh learner history, positive moderate weight and no other candidates, all five are eligible; both middle-only subgroup members remain selectable. Neither difficulty filter nor selection examines truth masks and neither repairs this subgroup shortcut.','limits':'No learner history, active policy weights, or live combined pool supplied. Exact per-learner order/probabilities and future inventory are not asserted.'}
save('selection-analysis.json',selection)
save('coverage-results.json',{'source_profile_coverage':coverage,'stages':stages,'batch_shortcut':{'correct':shortcut,'total':len(sub),'baseline':1/7},'same_family_independent_control':{'correct':control_hits,'total':len(ctrl),'baseline':1/7}})
inv=json.load(open(E.parent/'source/inventory.json'));source=json.load(open(E.parent/'source/source.json'));original_ids={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
inv_records=inv['questions'];assert all(q[':question/id'] in original_ids for q in inv_records)
save('inventory-assessment.json',{'basis':inv['basis'],'questions_examined':len(inv_records),'generated_provenance_records':sum(any('generat' in k for k in q) for q in inv_records),'all_ids_match_original_instructional_sources':True,'result':'No stored generated instances of the demonstrated batch-selection weakness exist in the captured inventory. All 16 captured questions are original source questions, not generated records; they are not relabelled or included as affected generated questions. This is a captured-inventory check, not an assertion about later live database contents.','questions':[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'classification':'original source'} for q in inv_records]})
save('affected-inventory.json',{'affected_questions':[]})
save('counterfactual-results.json',{'records':'counterfactual-records.json','native_cases':'native-input.json cases 102..105, native-report.json labels 102..105','base_truths':[True,False,True],'relevant_polarity_change':{'before':0,'after':1,'expected_and_observed_after':[False,False,True],'old_first_field_true_action':'rejected after; accepted before','solution_follows':'first implication changes true to false, with determinant fact retained'},'irrelevant_equivalent_hypothesis':{'before':0,'after':2,'change':'rank=7 to nullity=0','expected_and_observed_after':[True,False,True],'grader':'same selection action accepted on both','solution_follows':'conditional premise changes; full-rank consequence retained'},'relevant_premise_change':{'before':0,'after':3,'change':'rank=7 to rank<7, holding all three printed conclusions fixed','expected_and_observed_after':[False,True,False],'grader':'previous three selections rejected; complementary selections accepted','solution_follows':'rank/nullity fact and every implication truth changes together'},'rendering':'render-records.json indices 5..8; render/question-006.png through question-009.png'})
print(json.dumps({'batch_reproduced':True,'batch_shortcut':f'{shortcut}/{len(sub)}','control':f'{control_hits}/{len(ctrl)}','acceptance_test_passed':result['passed'],'inventory_generated':0}))
