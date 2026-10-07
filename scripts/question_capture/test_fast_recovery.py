"""Saved import formatting and the late-rendering quiz START regression."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
from core import compare_answers
from database import Database
from assessment import _take_assessment
from playwright.sync_api import TimeoutError

class RecoveryTests(unittest.TestCase):
    def test_successful_grade_corrects_prediction_without_another_model_call(self):
        from browser import CaptureBrowser
        record = {'intended':'W','actual_result':'Correct',
            'before':{'problem':'Select the answer.','fields':[{'key':'selection','type':'radio',
                'submitted_option':'b','submitted_value':'No solutions',
                'choices':[{'option':'a','type':'math','value':'3'},
                           {'option':'b','type':'text','value':'No solutions'}]}]},
            'after':{'worked_solution':'There are no solutions.'},
            'decision':{'answers':[{'key':'selection','correct_option':'a',
                'correct_value':'3','value_type':'math'}]}}
        reader = object.__new__(CaptureBrowser);reader.solver = Mock()
        reader.finalize_question({'task_type':'review'},Path('/tmp/unused'),'q-1',record)
        answer = record['decision']['answers'][0]
        self.assertEqual((answer['correct_value'],answer['value_type']),('No solutions','text'))
        self.assertEqual(record['predicted_answers'][0]['correct_value'],'3')
        self.assertTrue(record['finalized'])
        reader.solver.solve.assert_not_called()

    def test_rates_and_wrapped_math_keep_actual_values_and_units(self):
        for a,b in [('92 m/s²',r'92\,{\text{m/s}}^{2}'),('2.5cm/s',r'2.5\,\text{cm/s}'),
                    ('18m/s^{2}',r'18\,{\text{m/s}}^{2}'),
                    ('[MATH: x ∈ (- ∞,-3]∪[4, ∞)]',r'x\in (-\infty ,-3]\cup [4,\infty )')]:
            self.assertEqual(compare_answers(a,b)['outcome'],'equivalent',(a,b))
        for a,b in [('92m/s²','93m/s²'),('92m/s²','92m/s'),('92m/s²','92cm/s²'),
                    ('2.5cm/s','2.5cm'),('[MATH: x ∈ [-3,4]]','x ∈ [-3,5]')]:
            self.assertNotEqual(compare_answers(a,b)['outcome'],'equivalent',(a,b))

    def test_precision_prompt_accepts_styling_but_does_not_erase_precision(self):
        a=r'z = \sqrt{5}e^{2.034\textrm{i}}'
        b=r'z=\sqrt{5}\,{\text{e}}^{2.034\,\text{i}}'
        prompt='Give the angle in radians to 3 decimal places.'
        self.assertEqual(compare_answers(a,b,prompt=prompt)['outcome'],'equivalent')
        for wrong in (b.replace('2.034','2.035'),b.replace('sqrt{5}','sqrt{3}')):
            self.assertNotEqual(compare_answers(a,wrong,prompt=prompt)['outcome'],'equivalent')
        with patch('native_comparison.compare',return_value={'outcome':'different'}) as native:
            self.assertNotEqual(compare_answers('2.0','2',prompt='Use 1 decimal place')['outcome'],'equivalent')
            native.assert_called_once()

    def test_saved_ellipse_verification_uses_native_equivalence(self):
        from browser import CaptureBrowser
        directory=Path(__file__).parent/'fixtures'
        evidence=json.loads((directory/'ellipse-verification.json').read_text())
        state={'task_type':'review'}
        record=copy.deepcopy(evidence['record'])
        answer=copy.deepcopy(evidence['verification'])
        reader=object.__new__(CaptureBrowser);reader.solver=Mock()
        reader.solver.solve.return_value=answer
        reader.finalize_question(state,directory,'q-279151',record)
        self.assertTrue(record['finalized'])
        record.pop('verification');record.pop('finalized')
        answer=copy.deepcopy(answer);answer['answers'][0]['correct_value']=r'\frac{4x^2}{48}+\frac{y^2}{16}'
        reader.solver.solve.return_value=answer
        reader.finalize_question(state,directory,'q-279151',record)
        self.assertTrue(record['finalized'])
        self.assertEqual(record['decision']['answers'][0]['correct_value'],answer['answers'][0]['correct_value'])
        self.assertEqual(record['answer_reconciliations'][0]['comparison'],'different')
        self.assertIn('predicted_answers',record)

    def test_precommit_basis_race_replans_without_model(self):
        db=Database(SimpleNamespace())
        with patch.object(db,'_import_content',side_effect=[ValueError('Database changed during planning; rerun before any commit'),{'committed':True}]) as run:
            self.assertEqual(db.import_content({},Path('/tmp/unused')),{'committed':True})
            self.assertEqual(run.call_count,2)
        with patch.object(db,'_import_content',side_effect=ValueError('Real conflict')) as run:
            with self.assertRaisesRegex(ValueError,'Real conflict'):db.import_content({},Path('/tmp/unused'))
            self.assertEqual(run.call_count,1)

    def test_start_screen_waits_for_render_before_deciding_to_click(self):
        with tempfile.TemporaryDirectory() as work:
            page=Mock();ready=Mock();start=Mock();questions=Mock();final=Mock();message=Mock()
            visible={'start':False}
            ready.first.wait_for.side_effect=lambda **kw:visible.update(start=True)
            start.is_visible.side_effect=lambda:visible['start']
            start.evaluate.return_value='<div id="screen">START</div>'
            final.is_visible.return_value=False;message.is_visible.return_value=False
            def locator(selector):
                if selector.startswith('#startButton:visible,'):return ready
                if selector in ('#startButton','[id="startButton"]'):return start
                if selector=='#screen':return start
                if selector=='#finalScreen':return final
                if selector=='#messageBox-message':return message
                return questions
            page.locator.side_effect=locator
            questions.first.wait_for.side_effect=TimeoutError('stop after START for fixture')
            reader=Mock();reader.page=page;reader.args.assessment_correct_weight=.8717
            reader.pacer.args.assessment_time_max=0
            state={'task_id':1,'test_id':2,'assessment_requirement':'required',
                   'assessment_details':{'Questions':'11','Time Limit':'15 minutes'},'questions':{}}
            with self.assertRaises(TimeoutError):_take_assessment(reader,state,Path(work))
            ready.first.wait_for.assert_called_once_with(state='visible')
            start.click.assert_called_once()
            self.assertTrue(state['assessment_start_intent'])
            self.assertEqual(state['activity_url'],'https://mathacademy.com/tasks/1/tests/2')

if __name__=='__main__':unittest.main()
