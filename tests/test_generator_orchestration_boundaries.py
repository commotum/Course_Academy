"""Offline lifecycle regressions for evidence revisions and local design anchors."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import test_generator_pipeline as fixtures
from generator_pipeline import CodexSession, Pipeline
from generator_session_binding import input_binding, bind_session

ROOT = Path(__file__).resolve().parents[1]


class SessionInputTests(unittest.TestCase):
    setUp = fixtures.GeneratorPipelineTests.setUp
    tearDown = fixtures.GeneratorPipelineTests.tearDown

    def setup_call(self):
        self.publisher.extract_source(123, self.job / 'source')
        (self.job / 'workspace').mkdir()
        self.directory = self.job / 'author-1'
        self.context = {'workspace': str(self.job / 'workspace'), 'evidence_root': str(self.directory)}
        self.pipeline = Pipeline(self.job, self.request, self.publisher, root=self.root,
            environment=self.environment, session=CodexSession(root=ROOT))
        self.expected = {'status': 'ready', 'manifest': 'package.json'}
        self.process = Mock(returncode=0)
        self.process.communicate.side_effect = lambda *args, **kwargs: (self.directory / 'result.json').write_text(json.dumps(self.expected))

    def test_same_target_changed_reference_relaunches_and_preserves_old_input(self):
        self.setup_call()
        reference = self.job / 'reference.json'
        reference.write_text('{"task":"choose substitution"}')
        self.context['reference_file'] = str(reference)
        with patch('generator_pipeline.subprocess.Popen', return_value=self.process) as start:
            self.pipeline.session_call('author', self.context, self.directory)
            reference.write_text('{"task":"given substitution"}')
            self.pipeline.session_call('author', self.context, self.directory)
        self.assertEqual(start.call_count, 2)
        self.assertEqual(json.loads((self.directory / 'execution.json').read_text())['launches'], 2)
        self.assertEqual(len(list((self.directory / 'input-revisions').glob('*/result.json'))), 1)
        snapshots = [p.read_text() for p in (self.directory / 'supplied-files').glob('*/reference.json')]
        self.assertEqual(set(snapshots), {'{"task":"choose substitution"}', '{"task":"given substitution"}'})

    def test_inventory_only_source_snapshot_change_reuses_completed_result(self):
        self.setup_call()
        with patch('generator_pipeline.subprocess.Popen', return_value=self.process) as start:
            self.pipeline.session_call('author', self.context, self.directory)
            path = self.job / 'source/source.json'
            value = json.loads(path.read_text()); value['basis'] = 900
            value['registered_generator'] = {':question-generator/script': 'operational-change'}
            path.write_text(json.dumps(value))
            self.pipeline.session_call('author', self.context, self.directory)
        self.assertEqual(start.call_count, 1)

    def test_changed_target_or_completed_account_invalidates_result(self):
        for kind in ('target', 'account'):
            with self.subTest(kind=kind):
                self.job = self.root / kind
                self.setup_call()
                account = self.job / 'workspace/instructional-account.md'
                account.write_text('Choose the substitution independently.')
                with patch('generator_pipeline.subprocess.Popen', return_value=self.process) as start:
                    self.pipeline.session_call('author', self.context, self.directory)
                    if kind == 'target':
                        self.publisher.material['question'] = 'Different target operation.'
                        self.publisher.extract_source(123, self.job / 'source')
                    else:
                        account.write_text('Supply the substitution.')
                    self.pipeline.session_call('author', self.context, self.directory)
                self.assertEqual(start.call_count, 2)

    def test_prompt_change_invalidates_cache_without_resetting_launch_budget(self):
        self.setup_call()
        policy_root = self.root / 'policy'
        templates = policy_root / 'generate/pipeline'; templates.mkdir(parents=True)
        (templates / 'author.md').write_text('First instruction {{context}}')
        (templates / 'author.schema.json').write_text('{}')
        session = CodexSession(root=policy_root)
        with patch('generator_pipeline.subprocess.Popen', return_value=self.process) as start:
            session('author', self.context, self.directory)
            (templates / 'author.md').write_text('Changed instruction {{context}}')
            session('author', self.context, self.directory)
        self.assertEqual(start.call_count, 2)
        self.assertEqual(json.loads((self.directory / 'execution.json').read_text())['launches'], 2)


class LegacyExemplarRecoveryTests(unittest.TestCase):
    setUp = fixtures.GeneratorPipelineTests.setUp
    tearDown = fixtures.GeneratorPipelineTests.tearDown
    pipeline = fixtures.GeneratorPipelineTests.pipeline

    def test_lost_legacy_reply_recovers_exact_request_then_never_republishes(self):
        legacy = self.job / 'investigation/publication'
        legacy.mkdir(parents=True)
        request = {'request_key': 'legacy-example-write', 'records': [{'question': {':question/id': 'old-example'}}]}
        (legacy / 'request.json').write_text(json.dumps(request))
        self.publisher.extract_source(123, self.job / 'source')
        calls = []
        def publish(directory):
            calls.append(json.loads((Path(directory) / 'request.json').read_text()))
            if len(calls) == 1:
                raise ConnectionError('Committed; reply lost')
            return {'passed': True, 'request_key': request['request_key'], 'basis_after': 2,
                    'source': ':agent/codex', 'questions': [request['records'][0]['question']]}
        self.publisher.publish = publish
        pipeline = self.pipeline(fixtures.FakeSession())
        with self.assertRaises(ConnectionError): pipeline.run(stop_after='generate')
        result = self.pipeline(fixtures.FakeSession()).run(stop_after='generate')
        self.assertEqual(result['stage'], 'validate')
        self.assertEqual(calls, [request, request])
        self.assertEqual(result['legacy_exemplar_publication']['source'], ':agent/codex')
        self.pipeline(fixtures.FakeSession()).run(stop_after='generate')
        self.assertEqual(len(calls), 2)
        self.assertEqual(self.publisher.exemplar_publications, [])


if __name__ == '__main__': unittest.main()
