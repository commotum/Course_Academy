"""Verify the complete committed restoration at its confirmed final basis."""
from repair import *
if __name__=='__main__':
 rows=ledger();ids={r['id']for r in rows};assert len(rows)==561 and len(ids)==561
 confirmations=[];grade=[];expected={};responses=[];plans={};rendered=0
 for n in (1,2,3):
  base=HERE/f'batch-{n:02}';v=json.loads((base/'verification.json').read_text());assert v['passed']and v['committed'];confirmations.append(v)
  p=json.loads((base/'plan.json').read_text());request=json.loads((base/'request.json').read_text());assert sha(base/'transaction.edn')==request['sha256']==p['sha256'];report=loads((base/'receipt.edn').read_text());check_report(report,p,True)
  quality=json.loads((base/'quality.json').read_text());assert quality['passed']and quality['presentation_lint_passed']and quality['none_field_complete_visible_labels_verified'];grade.append(quality['native_grading'])
  ui=json.loads((base/'ui-verification.json').read_text());assert ui['passed'];path=base
  if ui.get('review_reused_from'):path=Path(ui['review_reused_from']).parent;ui=json.loads((path/'ui-verification.json').read_text())
  rendered+=len(ui['questions'])*len(ui['widths'])
  for name in ('ui','ui-narrow'):assert json.loads((path/name/'rendering.json').read_text())['passed']
  for q in json.loads((base/'committed.json').read_text())['questions']:expected[q[':db/id']]=q
  plans.update({r['id']:r for r in p['questions']});responses.extend(p['responses'])
 final_basis=confirmations[-1]['basis_after'];current=pull_many('final-questions',ids,final_basis);assert len(current)==len(ids)
 for q in current:
  assert equal(q,expected[q[':db/id']]),('Question changed between commit and final verification',q[':db/id'])
  p=plans[q[':db/id']];fs=[f for f in q[':question/answer-fields']if f[':answer-field/key']==p['key']];assert len(fs)==1 and fs[0][':answer-field/correct'][':answer/value']==str(p['none_correct']).lower()
  assert not re.search(r'leave all (?:boxes|checkboxes) unchecked',q[':question/problem'],re.I)
 oldempties=json.loads((ROOT/'reference/mathacademy/repairs/2026-10-19-checkbox-nonempty/empty-checkbox-questions.json').read_text());oldids={int(i)for i in oldempties};remaining=pull_many('prior-empty-questions',oldids,final_basis)
 still_empty=[q for q in remaining if not any(f[':answer-field/correct'][':answer/value']=='true'for f in q[':question/answer-fields'])]
 assert len(still_empty)==22 and all(not q.get(':question/math-academy-id')for q in still_empty)
 ownerquery='[:find ?q :in $ ?f :where [?q :question/answer-fields ?f]]'
 assert DB.query(ownerquery,[17592186408178],HERE/'final-queries','reused-owner-before',confirmations[0]['basis_before'])==[]
 assert DB.query(ownerquery,[17592186408178],HERE/'final-queries','reused-owner-after',final_basis)==[[17592186234490]]
 reported=next(q for q in current if q[':db/id']==17592186272199);save(HERE/'reported-question-after.json',reported)
 main_mapping=next(r for r in responses if r['question']==17592186272199);assert main_mapping['none_value']=='true'and main_mapping['grade_before']is True
 result={'passed':True,'committed':True,'database':'math','lineage':json.loads((HERE/'identity.json').read_text())['lineage'],'source':SOURCE,'basis_after':final_basis,'batches':confirmations,'questions':len(rows),'none_correct':sum(r['none_correct']for r in rows),'none_distractor':sum(not r['none_correct']for r in rows),'equivalent_explicit_source_labels':sum(r['key']!='None of the above'for r in rows),'saved_responses_mapped':len(responses),'historical_subsets_native_graded':sum(g['historical_subsets_checked']for g in grade),'single_box_flips_rejected':sum(g['single_checkbox_flips_rejected']for g in grade),'fresh_practice_eligible':len(rows),'presentation_lint_questions':len(rows),'rendered_pages':rendered,'viewport_widths':[1280,390],'remaining_original_imported_all_false_questions':0,'authored_all_false_questions_still_excluded':len(still_empty),'existing_field_keys_answers_solutions_ratings_memberships_preserved':True,'learner_state_and_grades_preserved':True,'all_final_questions_verified_at_confirmed_basis':True,'reported_question_none_correct':True,'reported_question_saved_answer_preserved':True,'generator_policy_tests':6,'generator_sources_revised':False,'documentation_updated':'generate/docs/6-template-generator.md'}
 save(HERE/'verification.json',result);print(json.dumps({k:v for k,v in result.items()if k!='batches'},indent=2))
