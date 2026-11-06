"""Adversarial admission checks; agent judgments are explicit test doubles."""
import json
from pathlib import Path
import unittest

from generator_pipeline import Pipeline, digest
import test_generator_pipeline as fixtures
from test_generator_pipeline import FakeSession, PhaseSession, fixture_investigation


class PhaseGateTests(unittest.TestCase):
    setUp = fixtures.GeneratorPipelineTests.setUp
    tearDown = fixtures.GeneratorPipelineTests.tearDown
    pipeline = fixtures.GeneratorPipelineTests.pipeline

    def prepare(self, session):
        pipeline = self.pipeline(session)
        source = self.publisher.extract_source(123, self.job / 'source')
        (self.job / 'workspace').mkdir(exist_ok=True)
        pipeline.persist(stage='investigate', source_hash=digest(source))
        return pipeline

    def test_source_accounts_precede_donor_and_exemplar_exposure_and_same_verifier_continues(self):
        events, contexts = [], []
        class Session(FakeSession):
            def phase_call(inner, role, context, directory):
                events.append((role, context['phase']))
                contexts.append((role, dict(context)))
                return super().phase_call(role, context, directory)
            def __call__(inner, role, context, directory):
                events.append((role, context.get('phase', 'generator')))
                return super().__call__(role, context, directory)
        def donor(publisher, source, directory):
            events.append(('runner', 'donors'))
            self.assertTrue(list((self.job / 'investigation/source-account').glob('original-*.json')))
            return fixture_investigation(publisher, source, directory)
        session = Session()
        pipeline = Pipeline(self.job, self.request, self.publisher, root=self.root,
            environment=self.environment, session=PhaseSession(session), investigation_preparer=donor)
        result = pipeline.run(stop_after='validate')
        self.assertEqual(result['stage'], 'prepare')
        self.assertLess(events.index(('investigate', 'source_account')), events.index(('runner', 'donors')))
        self.assertLess(events.index(('review', 'source_account')), events.index(('review', 'exemplars')))
        self.assertLess(events.index(('review', 'exemplars')), events.index(('author', 'generator')))
        for role, context in contexts:
            if context['phase'] == 'source_account':
                self.assertFalse(set(context) & {'reference_file', 'exemplars_file', 'manifest', 'initial_source_analysis_file', 'investigation_account_file'})
        self.assertEqual(result['review_thread'], 'fixture-review')
        gate = result['exemplar_gate']
        final = json.loads(Path(result['review']).read_text())
        original = json.loads(Path(result['verifier_account']['path']).read_text())
        self.assertEqual(final['source_analysis']['reasoning_steps'], original['reasoning_steps'])
        self.assertEqual(gate['binding']['initial_source_analysis_sha256'], result['verifier_account']['sha256'])

    def test_missing_target_account_never_queries_donors_or_calls_author(self):
        class Missing(FakeSession):
            def phase_call(inner, role, context, directory):
                return {'status': 'ready', 'account_file': 'source-analysis.json'}
        session = Missing()
        pipeline = self.prepare(session)
        pipeline.investigation_preparer = lambda *args: self.fail('Donor exposed before target account')
        result = pipeline.run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual(session.calls, [])

    def test_missing_exemplars_never_calls_author(self):
        class Missing(FakeSession):
            def __call__(inner, role, context, directory):
                if role == 'investigate':
                    return {'status': 'ready', 'exemplars_file': None}
                return super().__call__(role, context, directory)
        session = Missing()
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual(session.calls, [])

    def test_independent_math_rejection_blocks_wrong_key_before_author(self):
        class WrongKey(FakeSession):
            def __call__(inner, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == 'investigate':
                    path = Path(context['workspace']) / result['exemplars_file']
                    rows = json.loads(path.read_text())
                    rows[0]['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'] = '999'
                    path.write_text(json.dumps(rows))
                return result
            def phase_call(inner, role, context, directory):
                result = super().phase_call(role, context, directory)
                if context['phase'] == 'exemplars':
                    rows = json.loads(Path(context['exemplars_file']).read_text())
                    q = rows[0]['question']; n = int(q[':question/problem'].split()[1])
                    actual = int(q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])
                    if actual != n * n:
                        result['verdict'] = 'revise'
                        result['checks']['math']['status'] = 'failed'
                return result
        session = WrongKey()
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertFalse(any(role == 'author' for role, _ in session.calls))
        self.assertEqual(self.publisher.prepares, 0)

    def test_declared_acceptance_without_actual_tool_evidence_never_calls_author(self):
        class MissingEvidence(FakeSession):
            def phase_call(inner, role, context, directory):
                result = super().phase_call(role, context, directory)
                if context['phase'] == 'exemplars':
                    (Path(directory) / 'easy-grading.json').unlink()
                return result
        session = MissingEvidence()
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual(session.calls, [])

    def test_anchor_image_edit_invalidates_both_list_and_wrapper_gate(self):
        for wrapper in (False, True):
            with self.subTest(wrapper=wrapper):
                self.job = self.root / ('wrapper' if wrapper else 'list')
                class Images(FakeSession):
                    preserve = False
                    reject_gate = False
                    def __call__(inner, role, context, directory):
                        if role == 'investigate' and inner.preserve:
                            return {'status': 'ready', 'exemplars_file': 'exemplars.json'}
                        result = super().__call__(role, context, directory)
                        if role == 'investigate':
                            path = Path(context['workspace']) / 'exemplars.json'
                            rows = json.loads(path.read_text())
                            rows[0]['question'][':question/problem'] += ' <img src="diagram.svg">'
                            path.write_text(json.dumps({'records': rows} if wrapper else rows))
                            path.with_name('diagram.svg').write_text('<svg>original visible operand</svg>')
                        return result
                    def phase_call(inner, role, context, directory):
                        result = super().phase_call(role, context, directory)
                        if context['phase'] == 'exemplars' and inner.reject_gate:
                            result['verdict'] = 'revise'
                        return result
                session = Images(); pipeline = self.prepare(session)
                pipeline.investigate()
                self.assertEqual(pipeline.state['stage'], 'generate')
                self.assertTrue(pipeline.exemplar_gate_current())
                (self.job / 'workspace/diagram.svg').write_text('<svg>changed answer-bearing operand</svg>')
                self.assertFalse(pipeline.exemplar_gate_current())
                session.preserve = session.reject_gate = True
                result = pipeline.run()
                self.assertEqual(result['stage'], 'blocked')
                self.assertEqual(session.calls, [])

    def test_rewritten_initial_verifier_account_cannot_establish_acceptance(self):
        class Rewrite(FakeSession):
            def phase_call(inner, role, context, directory):
                result = super().phase_call(role, context, directory)
                if context['phase'] == 'exemplars':
                    path = Path(directory) / 'source-analysis.json'
                    account = json.loads(path.read_text()); account['skill'] = 'Copy the displayed answer'
                    path.write_text(json.dumps(account))
                return result
        session = Rewrite()
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual(session.calls, [])

    def test_enum_difficulty_anchors_are_each_bound_to_one_record(self):
        class Enums(FakeSession):
            def __call__(inner, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == 'investigate':
                    path = Path(context['workspace']) / 'exemplars.json'
                    rows = json.loads(path.read_text())
                    for row in rows:
                        row['question'][':question/difficulty'] = {':db/ident': row['question'][':question/difficulty']}
                    path.write_text(json.dumps(rows))
                return result
        pipeline = self.prepare(Enums()); pipeline.investigate()
        self.assertEqual(pipeline.state['stage'], 'generate')
        for row in pipeline.state['exemplar_gate']['binding']['verification_batches'].values():
            self.assertEqual(len(json.loads(Path(row['batch_file']).read_text())), 1)

    def test_changed_source_after_downstream_exposure_starts_source_only_thread(self):
        accounts = []
        class Recording(FakeSession):
            def phase_call(inner, role, context, directory):
                if context['phase'] == 'source_account':
                    accounts.append((role, context.get('resume_session_id'), context['source_account_identity']))
                return super().phase_call(role, context, directory)
        session = Recording()
        pipeline = self.pipeline(session)
        self.assertEqual(pipeline.run(stop_after='generate')['stage'], 'validate')
        original = {role: identity for role, _, identity in accounts}
        self.publisher.material['question'] = 'Square 8 independently.'
        source = self.publisher.extract_source(123, self.job / 'source')
        pipeline.persist(stage='investigate', source_hash=digest(source), inventory_hash=None)
        pipeline.investigate()
        for role, resumed, identity in accounts[2:]:
            self.assertIsNone(resumed)
            self.assertNotEqual(identity, original[role])
        self.assertEqual(len(accounts), 4)

    def test_source_only_capture_preserves_relative_diagrams_and_image_revisions(self):
        snapshots = []
        class Diagrams(FakeSession):
            def phase_call(inner, role, context, directory):
                if context['phase'] == 'source_account':
                    captured = Path(context['source_file']).parent / 'diagram.svg'
                    snapshots.append(captured)
                    self.assertTrue(captured.is_file())
                return super().phase_call(role, context, directory)
        pipeline = self.prepare(Diagrams())
        original = self.job / 'source/diagram.svg'; original.write_text('<svg>original diagram</svg>')
        self.publisher.material['question'] = 'Interpret ![diagram](diagram.svg) and square the value.'
        self.publisher.extract_source(123, self.job / 'source')
        pipeline.source_account_phase('investigate')
        original.write_text('<svg>revised diagram</svg>')
        pipeline.source_account_phase('investigate')
        self.assertNotEqual(snapshots[0], snapshots[1])
        self.assertEqual(snapshots[0].read_text(), '<svg>original diagram</svg>')
        self.assertEqual(snapshots[1].read_text(), '<svg>revised diagram</svg>')


if __name__ == '__main__': unittest.main()
