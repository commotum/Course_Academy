from copy import deepcopy
import json
from pathlib import Path
import tempfile
import threading
import unittest

from scripts.activity import ActivityCapture
from scripts.activity.solver import SolverUnavailable
from scripts.config import Config
from scripts.runtime import StopRequested


def question(identity='q-1', **extra):
    return {'math_academy_id': identity, 'problem': 'What is 1 + 1?', 'topic_id': '7', 'kp_id': '8',
            'fields': [{'key': 'answer', 'type': 'blank'}], **extra}


class Agent:
    def __init__(self):
        self.calls = []
        self.solve_failures = 0
        self.judge_failures = 0

    def request(self, task, payload, **options):
        self.calls.append((task, deepcopy(payload), options))
        if task == 'interpret_page':
            return {'action': 'reload', 'reasoning': 'Reload the saved active page.'}
        if task == 'match_topic':
            return {'topic_id': '7', 'confidence': 1, 'reasoning': 'Same source skill.'}
        if task == 'solve_question' and self.solve_failures:
            self.solve_failures -= 1
            raise SolverUnavailable('Temporary solver outage')
        if task == 'judge_question' and self.judge_failures:
            self.judge_failures -= 1
            raise SolverUnavailable('Temporary final-review outage')
        q = payload['question']
        return {'status': 'confirmed', 'reasoning': 'Adding one and one gives two.', 'confidence': 1,
                'answers': [{'key': f['key'], 'correct_value': '2', 'wrong_value': '3', 'value_type': 'math',
                             'ma_value': '2' if task == 'judge_question' else None,
                             'ma_basis': 'worked_solution' if task == 'judge_question' else 'none',
                             'ma_evidence': 'The answer is 2.', 'disagrees': False}
                            for f in q.get('fields', q.get('answer_fields', []))]}


class Browser:
    def __init__(self, questions, kind='review'):
        self.questions = deepcopy(questions)
        self.index = 0
        self.kind = kind
        self.accepted = False
        self.submitted = False
        self.responses = []
        self.advances = 0
        self.opens = 0
        self.histories = 0
        self.fail_response_after_acceptance = False
        self.fail_continue_after_acceptance = False
        self.stop_after_response = None

    def open(self, activity, directory, checkpoint):
        self.opens += 1

    def observe(self, directory):
        if self.index >= len(self.questions):
            if self.kind == 'assessment' and not self.submitted:
                return {'kind': 'instructions', 'key': 'submit', 'action': 'submit_assessment'}
            return {'kind': 'complete', 'key': 'complete', 'completion': {'earned_xp': 8, 'base_xp': 13}}
        q = deepcopy(self.questions[self.index])
        if self.accepted:
            q['worked_solution'] = 'The answer is 2.'
        return {'kind': 'question', 'key': 'presentation-' + str(self.index), 'question': q,
                'accepted': self.accepted, 'grade': 'Correct' if self.accepted else None,
                'html_path': '/source.html', 'remaining_seconds': None,
                'can_dont_know': self.kind == 'diagnostic'}

    def respond(self, observation, responses, directory):
        self.responses.append(deepcopy(responses))
        if isinstance(responses, dict) and responses.get('action') == 'submit_assessment':
            self.submitted = True
            return
        self.accepted = True
        if self.kind == 'assessment':
            self.index += 1
            self.accepted = False
        if self.stop_after_response:
            self.stop_after_response.set()
            raise StopRequested()
        if self.fail_response_after_acceptance:
            self.fail_response_after_acceptance = False
            raise TimeoutError('Response accepted; transport lost its acknowledgement')

    def advance(self, observation, directory):
        self.advances += 1
        if self.accepted:
            self.index += 1
            self.accepted = False
        if self.fail_continue_after_acceptance:
            self.fail_continue_after_acceptance = False
            raise TimeoutError('Continue accepted; transport lost its acknowledgement')

    def history(self, activity, directory):
        self.histories += 1
        questions = []
        for i, q in enumerate(self.questions, 1):
            questions.append({**q, 'math_academy_id': q.get('math_academy_id') or 'q-' + str(i),
                              'sequence_position': i, 'worked_solution': 'The answer is 2.',
                              'difficulty': 'easy', 'grade': 'Correct', 'html_path': '/history.html'})
        result = {'questions': questions, 'canonical_examples': [], 'tutorials': [],
                  'completion': {'earned_xp': 8, 'base_xp': 13}}
        if self.kind == 'lesson':
            result['lesson_definition'] = {'steps': []}
        if self.kind == 'multistep':
            result['multistep'] = {'context': 'Shared setup', 'part_order': [q['math_academy_id'] for q in questions]}
        return result


class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name) / 'task'
        self.config = Config(repo_root=Path(self.temp.name), retry_delay=.001, seed=3)
        self.stop = threading.Event()
        self.clock_value = 1000
        self.sleeps = []
        self.agent = Agent()

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.clock_value += seconds

    def run_capture(self, browser, **activity):
        capture = ActivityCapture(self.config, browser, self.stop,
                                  lambda _: {'course_topics': ['7'], 'graph': {}},
                                  solver=self.agent, clock=lambda: self.clock_value, sleeper=self.sleep)
        return capture.run({'task_id': '99', 'kind': browser.kind, 'topic_id': '7',
                            'title': 'Sample', 'details': {}, **activity}, self.directory)

    def test_review_completes_judges_and_preserves_source_answers(self):
        browser = Browser([question(), question('q-2')])
        content = self.run_capture(browser)
        self.assertEqual(len(browser.responses), 2)
        self.assertEqual(len(content['judgments']), 2)
        self.assertEqual(content['questions'][0]['answer_fields'][0]['correct_value'], '2')
        self.assertEqual(content['questions'][0]['difficulty'], 'easy')
        self.assertTrue((self.directory / 'capture-complete.json').exists())
        self.assertEqual(content['base_xp'], 13)

    def test_unknown_response_outcome_does_not_repeat_accepted_answer(self):
        browser = Browser([question()])
        browser.fail_response_after_acceptance = True
        self.run_capture(browser)
        self.assertEqual(len(browser.responses), 1)
        self.assertEqual(browser.advances, 1)

    def test_unknown_continue_outcome_observes_next_question_before_action(self):
        browser = Browser([question(), question('q-2')])
        browser.fail_continue_after_acceptance = True
        self.run_capture(browser)
        self.assertEqual(browser.advances, 2)
        self.assertEqual(len(browser.responses), 2)

    def test_manual_stop_resumes_accepted_submission_without_redraw_or_resubmit(self):
        browser = Browser([question()])
        browser.stop_after_response = self.stop
        with self.assertRaises(StopRequested):
            self.run_capture(browser)
        before = json.loads((self.directory / 'checkpoint.json').read_text())['policy']['decisions']
        self.stop.clear()
        browser.stop_after_response = None
        content = self.run_capture(browser)
        self.assertEqual(len(browser.responses), 1)
        self.assertEqual(content['policy']['decisions'], before)

    def test_finished_capture_is_returned_without_opening_or_judging_again(self):
        browser = Browser([question()])
        first = self.run_capture(browser)
        calls, opens = len(self.agent.calls), browser.opens
        second = self.run_capture(browser)
        self.assertEqual(first, second)
        self.assertEqual((len(self.agent.calls), browser.opens), (calls, opens))

    def test_assessment_fills_every_question_then_submits_once(self):
        browser = Browser([question(), question('q-2')], 'assessment')
        content = self.run_capture(browser)
        self.assertEqual(len(browser.responses), 3)
        self.assertEqual(browser.responses[-1], {'action': 'submit_assessment'})
        self.assertEqual(len(content['judgments']), 2)

    def test_solver_outage_uses_best_attempt_then_final_judgment_retry(self):
        browser = Browser([question()])
        self.agent.solve_failures = 1
        self.agent.judge_failures = 1
        content = self.run_capture(browser)
        self.assertEqual(len(browser.responses), 1)
        self.assertTrue(content['judgments'][0]['final'])
        self.assertEqual(len([c for c in self.agent.calls if c[0] == 'judge_question']), 2)

    def test_diagnostic_numbered_live_record_gains_history_identity_without_duplicate(self):
        browser = Browser([question(None)], 'diagnostic')
        content = self.run_capture(browser)
        self.assertEqual(len(content['questions']), 1)
        self.assertEqual(content['questions'][0]['math_academy_id'], 'q-1')
        self.assertEqual(content['attempts'][0]['question']['math_academy_id'], 'q-1')

    def test_lesson_first_two_distinct_questions_per_kp(self):
        browser = Browser([question(), question('q-2'), question('q-3')], 'lesson')
        content = self.run_capture(browser)
        self.assertEqual(content['lesson_workload_sample']['questions_by_knowledge_point'], {'8': ['q-1', 'q-2']})

    def test_multistep_keeps_shared_definition(self):
        browser = Browser([question(), question('q-2')], 'multistep')
        content = self.run_capture(browser)
        self.assertEqual(content['multistep']['part_order'], ['q-1', 'q-2'])
        self.assertEqual([a['decision']['planned'] for a in content['attempts']], ['C', 'C'])

    def test_revealed_fields_share_one_policy_position_and_keep_prior_field_grades(self):
        class StagedBrowser(Browser):
            stage = 0
            def observe(self, directory):
                result = super().observe(directory)
                if result['kind'] == 'question' and not result['accepted']:
                    if self.stage:
                        result['question']['fields'] = [
                            {'key': 'answer', 'type': 'blank', 'source_result': 'Correct'},
                            {'key': 'second', 'type': 'blank'}]
                    result['key'] += ':fields:' + ('second' if self.stage else 'answer')
                return result
            def respond(self, observation, responses, directory):
                if not self.stage:
                    self.responses.append(deepcopy(responses))
                    self.stage = 1
                else:
                    self.questions[0]['fields'].append({'key': 'second', 'type': 'blank'})
                    super().respond(observation, responses, directory)
        browser = StagedBrowser([question()])
        content = self.run_capture(browser)
        self.assertEqual(len(browser.responses), 2)
        self.assertEqual([r['key'] for r in browser.responses[1]], ['second'])
        self.assertEqual(len(content['attempts']), 1)
        self.assertEqual(content['policy']['counts'], {'review': 1})
        self.assertEqual(len(content['questions'][0]['answer_fields']), 2)
        self.assertEqual(content['questions'][0]['answer_fields'][0]['evidence']['kind'], 'ma_correct_grade')

    def test_near_deadline_submits_assessment_and_judges_unanswered_history(self):
        class DeadlineBrowser(Browser):
            def observe(self, directory):
                result = super().observe(directory)
                result['remaining_seconds'] = 3
                return result
            def respond(self, observation, responses, directory):
                super().respond(observation, responses, directory)
                if self.submitted:
                    self.index = len(self.questions)
        browser = DeadlineBrowser([question(), question('q-2')], 'assessment')
        content = self.run_capture(browser)
        self.assertEqual(browser.responses, [{'action': 'submit_assessment'}])
        self.assertEqual(len(content['judgments']), 2)

    def test_final_source_limitations_are_retained_without_human_queue(self):
        class MissingSourceBrowser(Browser):
            def history(self, *args):
                result = super().history(*args)
                result['questions'][0].pop('worked_solution')
                result['source_limitations'] = [{'source_url': '/lost', 'reason': 'Source returned 404'}]
                return result
        browser = MissingSourceBrowser([question()])
        content = self.run_capture(browser)
        self.assertTrue(content['source_limitations'])
        self.assertTrue(content['judgments'][0]['final'])

    def test_unknown_page_uses_observed_continue_then_reconciles_unknown_click_outcome(self):
        class UnknownBrowser(Browser):
            continued = False
            recover_calls = 0
            def observe(self, directory):
                if not self.continued:
                    return {'kind': 'unknown', 'key': 'unexpected-introduction',
                            'buttons': [{'selector': '#keep-going', 'text': 'Continue'}]}
                return super().observe(directory)
            def recover(self, observation, decision, directory):
                self.recover_calls += 1
                if (decision['button_selector'], decision['button_text']) != ('#keep-going', 'Continue'):
                    raise ValueError('Only the observed control is allowed')
                self.continued = True
                raise TimeoutError('Click accepted; acknowledgement lost')
        browser = UnknownBrowser([question()])
        original = self.agent.request
        def request(task, payload, **options):
            if task == 'interpret_page':
                return {'action': 'advance', 'reasoning': 'This introduction has a Continue button for the current activity.',
                        'button_selector': '#keep-going', 'button_text': 'Continue'}
            return original(task, payload, **options)
        self.agent.request = request
        content = self.run_capture(browser)
        self.assertEqual(browser.recover_calls, 1)
        self.assertEqual(len(browser.responses), 1)
        self.assertTrue(content['judgments'][0]['final'])


if __name__ == '__main__':
    unittest.main()
