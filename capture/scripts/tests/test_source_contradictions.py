"""A contradictory conclusion cannot erase a source-supported result."""
from copy import deepcopy
import unittest
from unittest.mock import Mock,patch

from scripts.activity.evidence import finalize_answers
from scripts.activity import solver
from scripts.database.evidence import authoritative_question,UnsupportedContent
from scripts.database.prepare import Preparation
from scripts.tests.test_database import question,source_snapshot


class SourceContradictionTests(unittest.TestCase):
    def fixture(self):
        source=('Statement I is true. Periodicity gives I.\n\n'
                'Statement II is true. The extension agrees everywhere.\n\n'
                'Statement III is false. A counterexample gives -1 instead of 1.\n\n'
                'Therefore, the correct answer is "I only".')
        q={'math_academy_id':'q-42','problem':'Which statements are true?',
           'worked_solution':source,'solution_evidence':'/saved-source.html',
           'answer_fields_complete':True,'answer_fields':[{'key':'selection','type':'radio',
           'choices_complete':True,'choices':[{'type':'text','value':v} for v in
             ['III only','I, II, and III','II and III only','I and II only','II only']],
           'correct_value':'I only','value_type':'text','evidence':{
             'kind':'worked_solution','value':'I only','source_file':'/saved-source.html',
             'solution_quote':'Therefore, the correct answer is "I only".','matches_worked_solution':True}}]}
        judgment={'status':'source_error','reasoning':'The source marks I and II true and III false; its final I-only conclusion contradicts those explicit results.',
          'answers':[{'key':'selection','correct_value':'I and II only','ma_value':'I and II only',
           'ma_basis':'worked_solution','ma_evidence':source.split('\n\nTherefore')[0],
           'value_type':'text','disagrees':True}]}
        return q,judgment

    def test_source_body_can_support_choice_without_changing_bad_conclusion_or_grade(self):
        q,j=self.fixture();original=deepcopy(q)
        attempts=[{'feedback':{'grade':'Incorrect'},'submissions':[{'outcome':'observe_to_confirm',
            'responses':[{'key':'selection','value':'III only'}]}]}]
        original_attempts=deepcopy(attempts)
        result=authoritative_question(finalize_answers(q,attempts,j))
        field=result['answer_fields'][0]
        self.assertEqual(field['correct_value'],'I and II only')
        self.assertEqual(field['evidence']['kind'],'worked_solution')
        self.assertNotIn('grade',field['evidence'])
        self.assertEqual(field['source_answer_conflicts'][0]['previous_value'],'I only')
        self.assertIn('"I only"',field['source_answer_conflicts'][0]['previous_evidence']['solution_quote'])
        self.assertEqual(result['worked_solution'],original['worked_solution'])
        self.assertEqual(result['answer_fields'][0]['choices'],original['answer_fields'][0]['choices'])
        self.assertEqual((q,attempts),(original,original_attempts))

    def test_math_alone_or_noncontiguous_source_quote_does_not_repair_key(self):
        q,j=self.fixture()
        for changes in ({'ma_basis':'none'}, {'ma_evidence':'Statement I is true. Statement II is true.'}):
            with self.subTest(changes=changes):
                changed=deepcopy(j);changed['answers'][0].update(changes)
                with self.assertRaises(UnsupportedContent):
                    authoritative_question(finalize_answers(q,[],changed))

    def test_direct_correct_grade_keeps_precedence_over_solution_interpretation(self):
        q,j=self.fixture()
        attempts=[{'feedback':{'grade':'Correct'},'submissions':[{'outcome':'observe_to_confirm',
            'responses':[{'key':'selection','value':'II only'}]}]}]
        field=finalize_answers(q,attempts,j)['answer_fields'][0]
        self.assertEqual(field['correct_value'],'II only')
        self.assertEqual(field['evidence']['kind'],'ma_correct_grade')

    def test_final_judgment_cache_is_bound_to_interpretation_policy(self):
        q=question();resolve=Mock(return_value={'status':'unavailable','reasoning':'Old policy','answers':[]})
        first=Preparation(source_snapshot(),resolve=resolve).final_judgment({},q,UnsupportedContent('Missing key'))
        content={'judgments':[first]}
        repeated=Preparation(source_snapshot(),resolve=resolve).final_judgment(content,q,UnsupportedContent('Missing key'))
        self.assertEqual(repeated['evidence_hash'],first['evidence_hash']);self.assertEqual(resolve.call_count,1)
        with patch.object(solver,'INSTRUCTIONS',solver.INSTRUCTIONS+'\nNew interpretation policy'):
            updated=Preparation(source_snapshot(),resolve=resolve).final_judgment(content,q,UnsupportedContent('Missing key'))
        self.assertNotEqual(updated['evidence_hash'],first['evidence_hash']);self.assertEqual(resolve.call_count,2)


if __name__=='__main__':unittest.main()
