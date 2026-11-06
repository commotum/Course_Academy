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

    def test_example_image_change_invalidates_cached_author_for_list_and_wrapper(self):
        from test_generator_publish import record
        for wrapper in (False, True):
            with self.subTest(wrapper=wrapper):
                self.job = self.root / ('wrapper' if wrapper else 'list')
                self.setup_call()
                path = self.job / 'workspace/examples.json'
                row = record(2); row['question'][':question/problem'] += ' <img src="diagram.svg">'
                path.write_text(json.dumps({'records': [row]} if wrapper else [row]))
                diagram = path.with_name('diagram.svg'); diagram.write_text('<svg>original</svg>')
                self.context['exemplars_file'] = str(path)
                with patch('generator_pipeline.subprocess.Popen', return_value=self.process) as start:
                    self.pipeline.session_call('author', self.context, self.directory)
                    diagram.write_text('<svg>changed learner-visible evidence</svg>')
                    self.pipeline.session_call('author', self.context, self.directory)
                self.assertEqual(start.call_count, 2)
                self.assertEqual(json.loads((self.directory / 'execution.json').read_text())['launches'], 2)
                self.pipeline.persist(exemplars_file=str(path))
                self.assertIn(str(diagram.resolve()), self.pipeline.instructional_evidence())

    def test_linked_instruction_change_is_bound_and_old_content_retained(self):
        self.setup_call()
        policy_root = self.root / 'policy'
        templates = policy_root / 'generate/pipeline'; templates.mkdir(parents=True)
        guide = policy_root / 'references/required.md'; guide.parent.mkdir()
        guide.write_text('Original instructional rule')
        (templates / 'author.md').write_text('Read [required](../../references/required.md). {{context}}')
        (templates / 'author.schema.json').write_text('{}')
        session = CodexSession(root=policy_root)
        with patch('generator_pipeline.subprocess.Popen', return_value=self.process) as start:
            session('author', self.context, self.directory)
            guide.write_text('Changed instructional rule')
            session('author', self.context, self.directory)
        self.assertEqual(start.call_count, 2)
        retained = {path.read_text() for path in (self.directory / 'instruction-inputs').glob('*/references/required.md')}
        self.assertEqual(retained, {'Original instructional rule', 'Changed instructional rule'})

    def test_source_revision_does_not_resume_execution_thread_or_reset_launches(self):
        self.setup_call()
        self.directory.mkdir(parents=True)
        (self.directory / 'execution.json').write_text(json.dumps({'launches': 1, 'persistent_session': True,
            'thread_id': 'thread-already-saw-author-output', 'source_account_identity': 'old-source', 'status': 'completed'}))
        context = {**self.context, 'phase': 'source_account', 'source_account_identity': 'new-source'}
        with patch('generator_pipeline.subprocess.Popen', return_value=self.process) as start:
            CodexSession(root=ROOT)('review', context, self.directory)
        command = start.call_args.args[0]
        self.assertNotIn('resume', command)
        self.assertNotIn('thread-already-saw-author-output', command)
        self.assertEqual(json.loads((self.directory / 'execution.json').read_text())['launches'], 2)

    def test_isolated_revisions_share_launch_budget_and_hide_budget_path_from_prompt(self):
        from generator_pipeline import SessionRetryExhausted
        self.setup_call()
        phase = self.job / 'source-account'; phase.mkdir()
        budget = phase / 'execution.json'
        budget.write_text(json.dumps({'launches': 2, 'thread_id': 'old-account-thread', 'persistent_session': True}))
        session = CodexSession(root=ROOT)
        contexts = []
        for identity in ('revision-a', 'revision-b'):
            self.directory = phase / 'revisions' / identity; self.directory.mkdir(parents=True)
            contexts.append({'workspace': str(self.directory), 'evidence_root': str(self.directory),
                'phase': 'source_account', 'source_account_identity': identity, 'source_account_isolation': 1,
                'source_account_revision': str(self.directory), '_execution_budget_file': str(budget)})
        self.directory = Path(contexts[0]['workspace'])
        with patch('generator_pipeline.subprocess.Popen', return_value=self.process) as start:
            session('investigate', contexts[0], self.directory)
            self.directory = Path(contexts[1]['workspace'])
            with self.assertRaises(SessionRetryExhausted) as stopped:
                session('investigate', contexts[1], self.directory)
        self.assertEqual(start.call_count, 1)
        self.assertEqual(stopped.exception.execution_path, budget)
        self.assertEqual(json.loads(budget.read_text())['launches'], 3)
        prompt = (Path(contexts[0]['workspace']) / 'prompt.txt').read_text()
        self.assertNotIn('_execution_budget_file', prompt)
        self.assertNotIn(str(budget), prompt)

    def test_crash_persists_no_old_thread_under_new_source_revision(self):
        self.setup_call()
        self.directory.mkdir(parents=True)
        execution = self.directory / 'execution.json'
        execution.write_text(json.dumps({'launches': 1, 'thread_id': 'contaminated',
            'persistent_session': True, 'source_account_identity': 'old'}))
        context = {**self.context, 'phase': 'source_account', 'source_account_identity': 'new',
            'source_account_isolation': 1, 'source_account_revision': str(self.directory)}
        class ParentCrash(BaseException): pass
        with patch('generator_pipeline.subprocess.Popen', side_effect=ParentCrash):
            with self.assertRaises(ParentCrash):
                CodexSession(root=ROOT)('review', context, self.directory)
        persisted = json.loads(execution.read_text())
        self.assertNotIn('thread_id', persisted)
        self.assertEqual(persisted['source_account_identity'], 'new')
        with patch('generator_pipeline.subprocess.Popen', return_value=self.process) as start:
            CodexSession(root=ROOT)('review', context, self.directory)
        self.assertNotIn('resume', start.call_args.args[0])
        self.assertEqual(json.loads(execution.read_text())['launches'], 3)


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
