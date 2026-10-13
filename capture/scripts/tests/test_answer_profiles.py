import io
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import threading
import unittest

from scripts.activity import ActivityCapture
from scripts.activity.policy import AnswerPolicy
from scripts.config import Config
from scripts.profiles import PROFILES, ExposureStore, accuracy, account_profile, set_account_profile
from scripts.runtime import StopRequested
from scripts.storage import atomic_json, read_json
from scripts.terminal import main as terminal_main
from scripts.tests.test_activity_capture import Agent, Browser, question
from scripts.tests.test_activity_policy import Draws


def checkpoint(kind='lesson', stage='activity', **records):
    return {'activity': {'task_id': '99', 'kind': kind}, 'stage': stage, 'presentations': records}


def graded(kp='8', grade='Correct', **extra):
    return {'question': question(kp_id=kp), 'accepted': True, 'grade': grade, **extra}


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = Config(repo_root=Path(self.temp.name))

    def test_all_nine_profiles_have_the_agreed_rates_and_shared_limit(self):
        self.assertEqual(len(PROFILES), 10)
        for speed, half_life in [('slow', 36), ('steady', 12), ('fast', 4)]:
            for base, initial in [('shaky', .5), ('solid', .75), ('strong', .9)]:
                name = speed + '-' + base
                self.assertEqual(accuracy(name, 0), initial)
                self.assertAlmostEqual(1 - accuracy(name, half_life), (1 - initial) / 2)
                self.assertGreater(accuracy(name, half_life * 10), .999)

    def test_settings_persist_per_account_and_explicit_run_override_wins(self):
        self.assertEqual(account_profile(self.config), 'capture')
        set_account_profile(self.config, 'fast-strong')
        self.assertEqual(account_profile(Config(repo_root=self.config.repo_root)), 'fast-strong')
        self.assertEqual(account_profile(Config(repo_root=self.config.repo_root, account='linear')), 'capture')
        self.assertEqual(account_profile(Config(repo_root=self.config.repo_root, answer_profile='capture')), 'capture')
        with self.assertRaises(ValueError):
            Config(answer_profile='genius')

    def test_profile_command_changes_only_the_named_account(self):
        config_path = self.config.repo_root / 'config.json'
        atomic_json(config_path, {'repo_root': str(self.config.repo_root)})
        with redirect_stdout(io.StringIO()):
            self.assertEqual(terminal_main(['set-profile', 'linear', '--answer-profile', 'fast-strong',
                                            '--config', str(config_path)]), 0)
        self.assertEqual(account_profile(Config(repo_root=self.config.repo_root, account='linear')), 'fast-strong')
        self.assertEqual(account_profile(self.config), 'capture')

    def test_graded_right_and_wrong_count_once_across_retries_and_restarts(self):
        store = ExposureStore(self.config)
        state = checkpoint(a=graded(), b=graded(grade='Incorrect'), c=graded(kp='9'))
        store.reconcile(state)
        store.reconcile(state)
        restored = ExposureStore(self.config)
        restored.reconcile(state)
        self.assertEqual(restored.count(question()), 2)
        self.assertEqual(restored.count(question(kp_id='9')), 1)
        self.assertEqual(ExposureStore(Config(repo_root=self.config.repo_root, account='linear')).count(question()), 0)

    def test_entry_failures_and_ungraded_presentations_do_not_count(self):
        store = ExposureStore(self.config)
        state = checkpoint(a={'question': question(), 'submissions': [{'outcome': 'not_submitted'}]},
                           b={'question': question(), 'accepted': True},
                           c=graded(accepted=False, submissions=[{'outcome': 'entry_failed'}]),
                           d=graded(grade='Skipped Question'))
        store.reconcile(state)
        self.assertEqual(store.count(question()), 0)

    def test_assessment_counts_only_after_completion_and_bound_history_grade(self):
        store = ExposureStore(self.config)
        state = checkpoint('assessment', a=graded())
        store.reconcile(state)
        self.assertEqual(store.count(question()), 0)
        state['stage'] = 'history'
        store.reconcile(state)
        self.assertEqual(store.count(question()), 1)
        store.reconcile(state)
        self.assertEqual(store.count(question()), 1)

    def test_diagnostic_does_not_count_and_policy_is_identical_for_all_profiles(self):
        store = ExposureStore(self.config)
        store.reconcile(checkpoint('diagnostic', 'complete', a=graded()))
        self.assertEqual(store.count(question()), 0)
        context = {'course_topics': ['7'], 'graph': {'6': ['7']}}
        for name in PROFILES:
            policy = AnswerPolicy({'kind': 'diagnostic'}, {}, context, Draws([.8]),
                                  clock=lambda: 10, answer_profile=name, exposures=store)
            self.assertEqual(policy.decide('a', question())['planned'], 'D')
            prerequisite = policy.decide('b', question(topic_id='6'))
            self.assertEqual((prerequisite['planned'], prerequisite['delay_seconds']), ('C', 105))

    def test_prior_capture_practice_is_backfilled_without_diagnostics_or_duplicates(self):
        atomic_json(self.config.output_root / '99/checkpoint.json', checkpoint(a=graded(), b=graded(grade='Incorrect')))
        atomic_json(self.config.output_root / '100/checkpoint.json', checkpoint('diagnostic', 'complete', a=graded()))
        store = ExposureStore(self.config)
        self.assertEqual(store.count(question()), 2)
        store.reconcile(checkpoint(a=graded(), b=graded(grade='Incorrect')))
        self.assertEqual(store.count(question()), 2)

    def test_profile_draws_apply_to_all_activities_and_ignore_force_correct(self):
        store = ExposureStore(self.config)
        store.reconcile(checkpoint(a=graded(), b=graded(), c=graded(), d=graded()))
        for kind in ('lesson', 'review', 'assessment', 'multistep'):
            policy = AnswerPolicy({'kind': kind, 'details': {'force_correct': True}}, {},
                                  rng=Draws([.9499, .95]), answer_profile='fast-strong', exposures=store)
            self.assertEqual(policy.decide('a', question())['planned'], 'C')
            saved = policy.decide('b', question())
            self.assertEqual((saved['planned'], saved['exposure_count']), ('W', 4))
            self.assertAlmostEqual(saved['correct_probability'], .95)
            restored = AnswerPolicy({'kind': kind}, policy.state, rng=Draws([]), answer_profile='slow-shaky')
            self.assertEqual(restored.decide('b', question()), saved)

    def test_unknown_kps_do_not_pool_exposures_and_history_can_resolve_them(self):
        store = ExposureStore(self.config)
        store.reconcile(checkpoint(a=graded()))
        unknown = question('another', kp_id=None)
        self.assertEqual(store.count(unknown), 0)
        self.assertIsNone(store.key(unknown))
        known = question(kp_id=None)
        self.assertEqual(store.count(known), 1)
        state = checkpoint(a=graded(kp='9'))
        store.reconcile(state)
        self.assertEqual((store.count(question()), store.count(question(kp_id='9'))), (0, 1))

    def test_capture_loop_improves_before_the_next_question_and_resumes_without_double_count(self):
        set_account_profile(self.config, 'fast-strong')
        browser = Browser([question(), question('q-2')])
        activity = {'task_id': '99', 'kind': 'review', 'topic_id': '7', 'details': {}}
        directory = self.config.output_root / '99'
        draws = Draws([.91, .91])
        capture = ActivityCapture(self.config, browser, threading.Event(), solver=Agent(),
                                  rng=draws, clock=lambda: 1000, sleeper=lambda _: None)
        # Avoid real-time pacing in this fixture while still exercising the draw.
        capture._pace_answer = lambda *args: None
        content = capture.run(activity, directory)
        decisions = list(content['policy']['decisions'].values())
        self.assertEqual([d['planned'] for d in decisions], ['W', 'C'])
        self.assertEqual([d['exposure_count'] for d in decisions], [0, 1])
        self.assertEqual(ExposureStore(self.config).count(question()), 2)
        capture.run(activity, directory)
        self.assertEqual(ExposureStore(self.config).count(question()), 2)

    def test_assessment_loop_does_not_learn_from_entered_answers_before_results(self):
        set_account_profile(self.config, 'fast-strong')
        browser = Browser([question(), question('q-2')], kind='assessment')
        activity = {'task_id': '99', 'kind': 'assessment', 'topic_id': '7', 'details': {}}
        capture = ActivityCapture(self.config, browser, threading.Event(), solver=Agent(),
                                  rng=Draws([.91, .91]), clock=lambda: 1000, sleeper=lambda _: None)
        capture._pace_answer = lambda *args: None
        content = capture.run(activity, self.config.output_root / '99')
        decisions = list(content['policy']['decisions'].values())
        self.assertEqual([d['planned'] for d in decisions], ['W', 'W'])
        self.assertEqual([d['exposure_count'] for d in decisions], [0, 0])
        self.assertEqual(ExposureStore(self.config).count(question()), 2)

    def test_resume_after_lost_submission_ack_preserves_draw_and_counts_once(self):
        set_account_profile(self.config, 'fast-strong')
        browser = Browser([question(), question('q-2')])
        stop = threading.Event()
        browser.stop_after_response = stop
        directory = self.config.output_root / '99'
        activity = {'task_id': '99', 'kind': 'review', 'topic_id': '7', 'details': {}}
        capture = ActivityCapture(self.config, browser, stop, solver=Agent(),
                                  rng=Draws([.99]), clock=lambda: 1000, sleeper=lambda _: None)
        capture._pace_answer = lambda *args: None
        with self.assertRaises(StopRequested):
            capture.run(activity, directory)
        saved = read_json(directory / 'checkpoint.json')['policy']['decisions']['presentation-0']
        self.assertEqual(saved['planned'], 'W')
        self.assertEqual(ExposureStore(self.config).count(question()), 0)
        set_account_profile(self.config, 'slow-shaky')
        stop.clear()
        browser.stop_after_response = None
        resumed = ActivityCapture(self.config, browser, stop, solver=Agent(),
                                  rng=Draws([.99]), clock=lambda: 1000, sleeper=lambda _: None)
        resumed._pace_answer = lambda *args: None
        content = resumed.run(activity, directory)
        self.assertEqual(content['policy']['decisions']['presentation-0'], saved)
        self.assertEqual(content['policy']['decisions']['presentation-1']['answer_profile'], 'slow-shaky')
        self.assertEqual(ExposureStore(self.config).count(question()), 2)
        self.assertEqual(len(browser.responses), 2)

    def test_capture_after_a_profile_switch_keeps_learning_history(self):
        ExposureStore(self.config)
        browser = Browser([question()])
        capture = ActivityCapture(self.config, browser, threading.Event(), solver=Agent(),
                                  clock=lambda: 1000, sleeper=lambda _: None, rng=Draws([.1]))
        capture._pace_answer = lambda *args: None
        content = capture.run({'task_id': '99', 'kind': 'review', 'topic_id': '7', 'details': {}},
                              self.config.output_root / '99')
        self.assertEqual(content['policy']['decisions']['presentation-0']['answer_profile'], 'capture')
        self.assertEqual(ExposureStore(self.config).count(question()), 1)


if __name__ == '__main__':
    unittest.main()
