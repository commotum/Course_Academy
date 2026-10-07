"""Restored server screens and activity solver judgment keep recovery autonomous."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from playwright.sync_api import TimeoutError
from assessment import restore_assessment_intents, take_assessment, reconcile_graded_answer
from multistep import with_context
import test_multistep as multistep_cases


class AutonomousAssessmentTests(unittest.TestCase):
    def reader(self, *, final=False, started=True):
        reader = Mock()
        def locator(selector):
            node = Mock()
            node.is_visible.return_value = (final if selector == '#finalScreen' else
                                           not started if selector == '#startButton' else False)
            node.count.return_value = int(started and not final)
            return node
        reader.page.locator.side_effect = locator
        return reader

    def test_confirming_checkpoint_resolves_from_fresh_unsubmitted_server_test(self):
        reader = self.reader()
        state = {'test_submission_status':'confirming', 'assessment_started':True,
                 'task_id':1, 'test_id':2, 'questions':{'q-1':{'status':'filled'}}}
        with tempfile.TemporaryDirectory() as work:
            restore_assessment_intents(reader, state, Path(work))
            saved = json.loads((Path(work)/'state.json').read_text())
        reader.navigate.assert_called_once_with('https://mathacademy.com/tasks/1/tests/2', force=True)
        self.assertNotIn('test_submission_status', saved)
        self.assertEqual(saved['questions']['q-1']['status'], 'filled')
        self.assertEqual(saved['assessment_intent_recoveries'][0]['reason'], 'server_restored_unsubmitted_test')

    def test_final_result_is_not_submitted_or_reloaded_again(self):
        reader = self.reader(final=True)
        state = {'test_submission_status':'confirming', 'task_id':1, 'test_id':2}
        with tempfile.TemporaryDirectory() as work:
            restore_assessment_intents(reader, state, Path(work))
        reader.navigate.assert_not_called()
        self.assertEqual(state['test_submission_status'], 'confirming')

    def test_start_intent_resolves_when_server_instructions_are_still_visible(self):
        reader = self.reader(started=False)
        state = {'assessment_start_intent':True, 'task_id':1, 'test_id':2}
        with tempfile.TemporaryDirectory() as work:
            restore_assessment_intents(reader, state, Path(work))
        self.assertNotIn('assessment_start_intent', state)
        self.assertEqual(state['assessment_intent_recoveries'][0]['reason'], 'server_restored_instruction_screen')

    def test_past_recovery_attempts_do_not_permanently_disable_resume(self):
        reader = self.reader()
        reader.page.content.return_value = '<html></html>'
        state = {'assessment_started':True, 'activity_url':'https://mathacademy.com/tasks/1/tests/2',
                 'assessment_recovery_attempts':8, 'questions':{'q-1':{'status':'filled'}}}
        with tempfile.TemporaryDirectory() as work, patch('assessment._take_assessment', side_effect=[TimeoutError('transient'), None]) as take:
            take_assessment(reader, state, Path(work))
        self.assertEqual(take.call_count, 2)
        self.assertEqual(state['assessment_recovery_attempts'], 9)
        reader.pacer.backoff.assert_called_once_with(7)
        reader.navigate.assert_called_once_with(state['activity_url'], force=True)

    def test_solver_weighs_solution_and_grade_and_preserves_original_prediction(self):
        reader = Mock()
        previous = {'key':'selection', 'correct_value':'1', 'value_type':'math', 'correct_option':'a'}
        reviewed = {**previous, 'correct_value':'2', 'correct_option':'b'}
        reader.solver.solve.return_value = {'confident':True, 'answers':[reviewed], 'explanation':'Source solution supports 2.'}
        record = {'actual_result':'Correct', 'before':{'problem':'Choose a number', 'fields':[
            {'key':'selection', 'submitted_value':'2', 'submitted_option':'b'}]},
            'decision':{'answers':[previous], 'explanation':'Previous prediction'}}
        with tempfile.TemporaryDirectory() as work:
            reconcile_graded_answer(reader, record, {'worked_solution':'The value is 2.'}, Path(work)/'image.png', Path(work), 'q-1')
        self.assertEqual(record['decision']['answers'][0]['correct_value'], '2')
        self.assertEqual(record['predicted_answers'][0]['correct_value'], '1')
        self.assertEqual(record['before']['fields'][0]['submitted_value'], '2')
        self.assertIn('"actual_grade": "Correct"', reader.solver.solve.call_args.args[0]['worked_solution'])
        self.assertEqual(reader.solver.solve.call_args.args[-1], 'reconcile-grade')

    def test_multistep_uses_recovered_correct_answer_after_incorrect_part(self):
        state = {'multistep_question_order':['q-1', 'q-2'], 'questions':{'q-1':{
            'actual_result':'Incorrect', 'verification':{'confident':True}, 'sequence_position':1,
            'local_problem':'Find x: {{field-1}}', 'decision':{'answers':[
                {'key':'field-1', 'correct_value':'2', 'value_type':'math'}]}}}}
        item = with_context(state, {'problem':'Now find x+1'}, 'q-2')
        self.assertIn('Find x: $2$', item['problem'])
        self.assertIn('Now find x+1', item['problem'])


class AutonomousMultistepDOMTests(unittest.TestCase):
    setUpClass = multistep_cases.MultistepTests.__dict__['setUpClass']
    tearDownClass = multistep_cases.MultistepTests.__dict__['tearDownClass']
    setUp = multistep_cases.MultistepTests.setUp
    tearDown = multistep_cases.MultistepTests.tearDown
    reader = multistep_cases.MultistepTests.reader
    activity_html = multistep_cases.MultistepTests.activity_html

    def respond(self, route):
        if route.request.url.endswith('/fixture/grade/0'):
            self.graded.add(0)
            self.submissions.append(0)
            html = multistep_cases.POOL['questions'][0]['grade_html']
            html = html.replace('correctAnswerText', 'incorrectAnswerText').replace('>Correct<', '>Incorrect<')
            route.fulfill(status=200, content_type='text/html; charset=utf-8', body=html)
            return
        return multistep_cases.MultistepTests.respond(self, route)

    def test_incorrect_part_is_solver_reviewed_and_remaining_parts_continue(self):
        reader = self.reader()
        reader.solver.solve = Mock(wraps=reader.solver.solve)
        activity, = reader.queue()
        state = multistep_cases.MultistepTests.state(activity)
        with tempfile.TemporaryDirectory() as work:
            reader.start(activity)
            reader.activity(state, Path(work), None)
        self.assertTrue(state['activity_complete'])
        self.assertEqual(self.submissions, list(range(6)))
        first = state['questions']['q-167521']
        self.assertEqual(first['actual_result'], 'Incorrect')
        self.assertTrue(first['verification'])
        self.assertTrue(first['predicted_answers'])
        self.assertIn('Earlier part 1:', state['questions']['q-167522']['before']['problem'])
        self.assertEqual(reader.solver.solve.call_count, 7)


if __name__ == '__main__':
    unittest.main()
