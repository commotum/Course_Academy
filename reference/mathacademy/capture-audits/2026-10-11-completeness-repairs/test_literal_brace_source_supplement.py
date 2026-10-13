import json,unittest
from pathlib import Path
from copy import deepcopy
from playwright.sync_api import sync_playwright
from literal_brace_source_supplement import refresh_source
R=Path(__file__).resolve().parent;P=R.parents[1]/'capture/linear/14114807/repairs/completeness-f31ec8f96c25ef6c'
class LocalSourceCertificates(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(headless=True)
  cls.old=next(q for q in json.loads((P/'originals/content.json').read_text())['questions'] if q['math_academy_id']=='q-172706')
  cls.new=next(q for q in json.loads((P/'content.json').read_text())['questions'] if q['math_academy_id']=='q-172706')
 @classmethod
 def tearDownClass(cls):cls.browser.close();cls.pw.stop()
 def setUp(self):self.context=self.browser.new_context();self.context.route('**/*',lambda r:r.abort());self.page=self.context.new_page()
 def tearDown(self):self.context.close()
 def run_refresh(self,old=None,new=None):return refresh_source(deepcopy(old or self.old),deepcopy(new or self.new),self.page,R/'literal-brace-local-tests')
 def test_exact_source_updates_value_and_solution_with_original_evidence(self):
  q=self.run_refresh();f=q['answer_fields'][0];proof=f['source_serializer_rebind'];self.assertEqual(f['correct_value'],r'\{a,b,d\}');self.assertEqual(proof['original_value'],'{a,b,d}');self.assertEqual(f['evidence']['source_file'],self.old['answer_fields'][0]['evidence']['source_file']);self.assertFalse(proof['grade_transfer']);self.assertTrue(q['external_solution_source_refresh']['old_rendered_solution_matches_original']);self.assertIn(r'$A=\{a,b,d\}.$',q['worked_solution'])
 def test_other_question_identity_blocks_all_changes(self):
  old=deepcopy(self.old);old['math_academy_id']='q-172707';q=self.run_refresh(old=old);self.assertNotIn('external_solution_source_refresh',q);self.assertNotIn('source_serializer_rebind',q['answer_fields'][0])
 def test_changed_control_identity_does_not_rebind_grade(self):
  new=deepcopy(self.new);new['answer_fields'][0]['choices'][0]['dom_id']='other-control';q=self.run_refresh(new=new);self.assertEqual(q['answer_fields'][0]['correct_value'],'{a,b,d}');self.assertNotIn('source_serializer_rebind',q['answer_fields'][0])
 def test_changed_control_html_does_not_rebind_grade(self):
  new=deepcopy(self.new);new['answer_fields'][0]['choices'][0]['html']+='<!-- changed -->';q=self.run_refresh(new=new);self.assertEqual(q['answer_fields'][0]['correct_value'],'{a,b,d}')
 def test_unmatched_saved_solution_retains_original(self):
  old=deepcopy(self.old);old['worked_solution']+=' changed';q=self.run_refresh(old=old);self.assertNotIn('external_solution_source_refresh',q);self.assertEqual(q['worked_solution'],self.new['worked_solution'])
 def test_incomplete_original_choices_do_not_rebind_grade(self):
  old=deepcopy(self.old);old['answer_fields'][0]['choices_complete']=False;q=self.run_refresh(old=old);self.assertNotIn('source_serializer_rebind',q['answer_fields'][0])
 def test_three_exact_own_ordered_lists_restore_literal_numbering(self):
  content=json.loads((R.parents[1]/'capture/linear/14117627/content.json').read_text())
  for identity in ['q-214483','q-214479','q-214481']:
   old=next(q for q in content['questions'] if q['math_academy_id']==identity);q=self.run_refresh(old=old,new=old)
   proof=q['external_solution_source_refresh']['explicit_original_ordered_list_restoration'];self.assertEqual(proof['literal_labels'],['1','2','3']);self.assertTrue(proof['legacy_rendering_exactly_matches_saved']);self.assertIn('1\\. ',q['worked_solution']);self.assertNotEqual(q['worked_solution'],old['worked_solution'])
 def custom_pair(self):
  p=R.parents[1]/'capture/linear/14117627/repairs/completeness-f31ec8f96c25ef6c'
  return tuple(deepcopy(next(q for q in json.loads((p/name).read_text())['questions'] if q['math_academy_id']=='q-214479')) for name in ['originals/content.json','content.json'])
 def test_exact_custom_select_frame_maps_own_ordinal_and_preserves_original_grade(self):
  old,new=self.custom_pair();q=self.run_refresh(old=old,new=new);f=q['answer_fields'][2];proof=f['source_serializer_rebind'];self.assertEqual(f['correct_value'],f['choices'][0]['value']);self.assertEqual(f['evidence']['source_file'],old['answer_fields'][2]['evidence']['source_file']);self.assertEqual(proof['exact_own_custom_select_control']['question_root'],'question-214479');self.assertEqual(proof['exact_own_custom_select_control']['complete_ordered_options'],len(f['choices']))
 def test_other_custom_frame_blocks_mapping(self):
  old,new=self.custom_pair();new['answer_fields'][2]['frame_id']='other-frame';q=self.run_refresh(old=old,new=new);self.assertNotIn('source_serializer_rebind',q['answer_fields'][2])
 def test_reordered_custom_ordinals_block_mapping(self):
  old,new=self.custom_pair();new['answer_fields'][2]['choices'].reverse();q=self.run_refresh(old=old,new=new);self.assertNotIn('source_serializer_rebind',q['answer_fields'][2])
 def test_duplicate_old_selected_custom_value_blocks_mapping(self):
  old,new=self.custom_pair();old['answer_fields'][2]['choices'][1]['value']=old['answer_fields'][2]['correct_value'];q=self.run_refresh(old=old,new=new);self.assertNotIn('source_serializer_rebind',q['answer_fields'][2])
 def test_incomplete_custom_list_blocks_mapping(self):
  old,new=self.custom_pair();old['answer_fields'][2]['choices_complete']=False;q=self.run_refresh(old=old,new=new);self.assertNotIn('source_serializer_rebind',q['answer_fields'][2])
 def test_other_root_even_with_same_frame_and_html_blocks_mapping(self):
  old,new=self.custom_pair();source=Path(old['answer_fields'][2]['evidence']['source_file']).read_text();self.assertIn('id="question-214479"',source);p=R/'literal-brace-local-tests/wrong-own-root.html';p.write_text(source.replace('id="question-214479"','id="question-214480"'));old['answer_fields'][2]['evidence']['source_file']=str(p);new['answer_fields'][2]['evidence']['source_file']=str(p);q=self.run_refresh(old=old,new=new);self.assertNotIn('source_serializer_rebind',q['answer_fields'][2])
 def test_jointly_forged_radio_rows_and_grade_are_rejected_by_raw_rows(self):
  old,new=deepcopy(self.old),deepcopy(self.new)
  for q in [old,new]:
   f=q['answer_fields'][0];c=f['choices'][0];c['html']=c['html'].replace('a,b,d','z');c['value']='{z}' if q is old else r'\{z\}'
  old['answer_fields'][0]['correct_value']='{z}';old['answer_fields'][0]['evidence']['value']='{z}';new['answer_fields'][0]['correct_value']='{z}';new['answer_fields'][0]['evidence']['value']='{z}';q=self.run_refresh(old=old,new=new);self.assertNotIn('source_serializer_rebind',q['answer_fields'][0])
 def test_jointly_forged_custom_rows_and_grade_are_rejected_by_raw_rows(self):
  old,new=self.custom_pair()
  for q in [old,new]:
   f=q['answer_fields'][2];f['choices'][0]['html']='<math><mo>{</mo><mi>z</mi><mo>}</mo></math>';f['choices'][0]['value']='{z}' if q is old else r'\{z\}';f['correct_value']='{z}';f['evidence']['value']='{z}'
  q=self.run_refresh(old=old,new=new);self.assertNotIn('source_serializer_rebind',q['answer_fields'][2])
 def test_changed_raw_correct_selection_marker_is_rejected(self):
  old,new=self.custom_pair();source=Path(old['answer_fields'][2]['evidence']['source_file']).read_text();p=R/'literal-brace-local-tests/missing-correct-selection.html';p.write_text(source.replace('class="selectListFrame correctSelection" id="selectListFrame-214479-2"','class="selectListFrame" id="selectListFrame-214479-2"'));old['answer_fields'][2]['evidence']['source_file']=str(p);new['answer_fields'][2]['evidence']['source_file']=str(p);q=self.run_refresh(old=old,new=new);self.assertNotIn('source_serializer_rebind',q['answer_fields'][2])
if __name__=='__main__':unittest.main()
