"""Elapsed solving, restarts and failed actions cannot reset capture timing."""
from copy import deepcopy
from pathlib import Path
import tempfile
import threading
import unittest

from scripts.activity.capture import ActivityCapture
from scripts.activity.policy import AnswerPolicy
from scripts.config import Config
from scripts.runtime import StopRequested
from scripts.storage import read_json
from scripts.tests.test_activity_capture import Agent, Browser, question


class ActivityTimingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.now = 1000.0
        self.delays = []
        self.stop = threading.Event()
        self.config = Config(repo_root=self.root, seed=17, recovery_jitter=0,
                             answer_min=10, answer_max=10)

    def sleep(self, seconds):
        self.delays.append(seconds)
        self.now += seconds

    def capture(self, browser=None, agent=None, activity=None):
        capture = ActivityCapture(self.config, browser or Browser([]), self.stop,
            solver=agent or Agent(), clock=lambda:self.now, sleeper=self.sleep)
        capture.activity = activity or {'task_id':'99', 'kind':'review', 'details':{}}
        capture.directory = self.root/'task'
        capture.directory.mkdir(exist_ok=True)
        capture.checkpoint_path = capture.directory/'checkpoint.json'
        capture.state = {'stage':'activity', 'recoveries':0, 'presentations':{}, 'steps':[],
                         'policy':{}, 'judgments':{}, 'activity':capture.activity}
        capture.policy = AnswerPolicy(capture.activity, capture.state['policy'], rng=capture.rng,
                                     clock=lambda:self.now)
        return capture

    def test_answer_wait_credits_solving_and_survives_restart(self):
        outer = self
        class SlowAgent(Agent):
            def request(self, task, payload, **options):
                if task == 'solve_question':outer.now += 7
                return super().request(task, payload, **options)
        browser = Browser([question()])
        capture = self.capture(browser, SlowAgent())
        capture.run(capture.activity, capture.directory)
        self.assertEqual(self.delays, [3])
        decision = read_json(capture.checkpoint_path)['policy']['decisions']['presentation-0']
        self.assertEqual(decision['delay_seconds'],10)
        self.assertEqual(decision['submit_at'],1010)

    def test_assessment_rechecks_deadline_after_solving(self):
        outer = self
        class TimedBrowser(Browser):
            def observe(self, directory):
                result = super().observe(directory)
                if result['kind'] == 'question':
                    result.update(remaining_seconds=max(0, 1030-outer.now), observed_at=outer.now,
                                  sequence_position=1, question_count=1)
                return result
        class SlowAgent(Agent):
            def request(self, task, payload, **options):
                if task == 'solve_question':outer.now += 20
                return super().request(task, payload, **options)
        browser = TimedBrowser([question()], 'assessment')
        # Final submission moves to the completion screen, even with blanks.
        original = browser.respond
        def respond(observation, responses, directory):
            original(observation, responses, directory)
            if isinstance(responses,dict):browser.index=len(browser.questions)
        browser.respond = respond
        capture = self.capture(browser, SlowAgent(), {'task_id':'99','kind':'assessment','details':{'question_count':1}})
        capture.run(capture.activity, capture.directory)
        self.assertEqual(browser.responses,[{'action':'submit_assessment'}])
        self.assertTrue(capture.state['assessment_timing_deviation'])

    def test_saved_assessment_schedule_does_not_redraw_or_restart(self):
        capture = self.capture(activity={'task_id':'99','kind':'assessment',
            'details':{'question_count':4,'time_limit':'15 minutes'}})
        capture._start_assessment_timing({'action':'start'})
        plan = deepcopy(capture.state['assessment_timing'])
        self.assertTrue(630 <= plan['target_seconds'] <= 765)
        self.assertEqual(plan['deadline_at'],1900)
        self.now += 200
        restored = self.capture(activity=capture.activity)
        restored.state=read_json(capture.checkpoint_path)
        restored._start_assessment_timing({'action':'start'})
        self.assertEqual(restored.state['assessment_timing'],plan)
        self.assertEqual(restored._remaining_seconds(),700)

    def test_aged_timer_and_live_question_count_bound_solver_budget(self):
        capture = self.capture(activity={'task_id':'99','kind':'assessment','details':{}})
        observation={'remaining_seconds':120,'observed_at':970,'question_count':3,'sequence_position':1}
        capture._observe_timing(observation)
        self.assertEqual(capture._remaining_seconds(),90)
        self.assertEqual(capture._solver_budget(observation),25)
        capture._observe_timing({'remaining_seconds':120,'observed_at':1000})
        self.assertEqual(capture._remaining_seconds(),90)  # An optimistic read never extends it.

    def test_answer_pacing_rechecks_visible_timer_before_another_wait(self):
        class TimerBrowser(Browser):
            timer_reads = 0
            def read_remaining_seconds(self):
                self.timer_reads += 1
                return 40
        browser = TimerBrowser([])
        capture = self.capture(browser, activity={'task_id':'99','kind':'assessment',
            'details':{'question_count':4,'time_limit':'15 minutes'}})
        capture._start_assessment_timing({'action':'start'})
        record = {'decision':{'submit_at':1300}}
        capture._pace_answer(record, {'sequence_position':1})
        self.assertEqual(browser.timer_reads, 1)
        self.assertEqual(self.delays, [30])
        self.assertEqual(capture._remaining_seconds(), 40)
        self.assertIn('timing_deviation', record['decision'])

    def test_repeated_action_failures_back_off_across_reobservations_and_resume(self):
        class Broken(Browser):
            def respond(self,*args):
                error=ValueError('Entry readback failed')
                error.submitted=False
                raise error
        capture=self.capture(Broken([question()]))
        for _ in range(2):capture._browser_call('respond',{'key':'q1'},[],capture.directory)
        restored=self.capture(Broken([question()]))
        restored.state=read_json(capture.checkpoint_path)
        restored._browser_call('respond',{'key':'q1'},[],restored.directory)
        self.assertEqual(self.delays,[30,60,90])
        self.assertEqual(restored.state['pending_browser_error']['attempt'],3)

    def test_retry_answer_requests_new_reasoning_with_browser_error(self):
        class RetryAgent(Agent):
            def request(self,task,payload,**options):
                if task=='interpret_page':
                    self.calls.append((task,payload,options))
                    return {'action':'retry_answer','reasoning':'Use keyboard entry for this field.'}
                return super().request(task,payload,**options)
        agent=RetryAgent()
        capture=self.capture(agent=agent)
        capture.state['presentations']['q1']={'key':'q1','solution_binding':'old'}
        capture.state['pending_browser_error']={'method':'respond','error':'Readback differs','attempt':4}
        observation={'kind':'question','key':'q1','question':question()}
        capture._recover_page(observation,5)
        record=capture.state['presentations']['q1']
        self.assertNotIn('solution_binding',record)
        self.assertEqual(record['reconsider_reason']['instruction'],'Use keyboard entry for this field.')
        self.assertEqual(agent.calls[0][1]['browser_error']['error'],'Readback differs')

    def test_diagnostic_dont_know_has_no_answer_delay_and_only_one_prerequisite_retry(self):
        capture=self.capture(activity={'task_id':'99','kind':'diagnostic','details':{}})
        capture.state['presentations']['q1']={'decision':{'intended':'C','distance':1}}
        self.assertTrue(capture._diagnostic_retry({'action':'decline_retry'})['retry_diagnostic'])
        self.assertTrue(capture._diagnostic_retry({'action':'decline_retry'})['retry_diagnostic'])
        capture.state['presentations']['q2']={'decision':{'intended':'C','distance':1}}
        self.assertFalse(capture._diagnostic_retry({'action':'decline_retry'})['retry_diagnostic'])
        capture.state['presentations']['q3']={'decision':{'intended':'D','distance':1}}
        self.assertFalse(capture._diagnostic_retry({'action':'decline_retry'})['retry_diagnostic'])
        self.assertEqual(self.delays,[])

    def test_manual_stop_interrupts_answer_pacing(self):
        capture=self.capture()
        self.stop.set()
        with self.assertRaises(StopRequested):
            capture._pace_answer({'decision':{'submit_at':1200}}, {})
        self.assertEqual(self.delays,[])
