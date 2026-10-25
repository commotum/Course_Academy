"""Preparation races retain reviewed work and exact publication recovery."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from generator_publish import StaleBasis
from test_generator_pipeline import FakeSession, GeneratorPipelineTests


class GeneratorPrepareRetryTests(unittest.TestCase):
    setUp = GeneratorPipelineTests.setUp
    tearDown = GeneratorPipelineTests.tearDown
    pipeline = GeneratorPipelineTests.pipeline

    def test_transient_prepare_race_retries_without_reauthoring_or_reviewing(self):
        session = FakeSession()
        pipeline = self.pipeline(session)
        prepare = self.publisher.prepare
        attempts = []

        def race_once(*args, **kwargs):
            attempts.append(args[4])
            if len(attempts) == 1:
                self.assertFalse((Path(args[4]) / 'request.json').exists())
                raise StaleBasis('Database advanced during preparation')
            return prepare(*args, **kwargs)

        with patch.object(self.publisher, 'prepare', side_effect=race_once):
            state = pipeline.run()

        self.assertEqual(state['stage'], 'verified')
        self.assertEqual(len(attempts), 2)
        self.assertEqual([role for role, _ in session.calls], ['author', 'review'])
        self.assertEqual(self.publisher.publishes, 1)
        self.assertEqual(set(state['verified_bands']), {'easy', 'moderate', 'hard'})

    def test_repeated_prepare_races_have_a_bounded_budget_and_keep_the_review(self):
        session = FakeSession()
        pipeline = self.pipeline(session)
        with patch.object(self.publisher, 'prepare', side_effect=StaleBasis('Database advanced')) as prepare:
            with self.assertRaises(StaleBasis):
                pipeline.run()

        self.assertEqual(prepare.call_count, 3)
        state = json.loads((self.job / 'job.json').read_text())
        self.assertEqual(state['stage'], 'prepare')
        self.assertEqual(json.loads(Path(state['review']).read_text())['verdict'], 'accepted')
        self.assertEqual([role for role, _ in session.calls], ['author', 'review'])
        self.assertFalse((self.job / 'publication/request.json').exists())
        self.assertEqual(self.publisher.publishes, 0)

    def test_saved_intent_recovers_exact_bytes_without_any_new_preparation(self):
        session = FakeSession()
        pipeline = self.pipeline(session)
        state = pipeline.run('prepare')
        self.assertEqual(state['stage'], 'push')
        request = self.job / 'publication/request.json'
        original = request.read_bytes()
        pipeline.persist(stage='prepare')
        resumed_session = FakeSession()
        resumed = self.pipeline(resumed_session)

        with patch.object(self.publisher, 'prepare', side_effect=AssertionError('Must recover saved intent')) as prepare:
            result = resumed.run()

        self.assertEqual(result['stage'], 'verified')
        prepare.assert_not_called()
        self.assertEqual(request.read_bytes(), original)
        self.assertEqual(resumed_session.calls, [])
        self.assertEqual(self.publisher.publishes, 1)


del GeneratorPipelineTests

if __name__ == '__main__':
    unittest.main()
