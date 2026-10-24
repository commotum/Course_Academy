"""Three-phase ownership with real package execution and fake agent/EDB edges."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import test_generator_pipeline as fixtures
from generator_packages import resolve_registered_script
from generator_pipeline import Pipeline, digest
from test_generator_publish import record


class ThreePhaseTests(unittest.TestCase):
    setUp = fixtures.GeneratorPipelineTests.setUp
    tearDown = fixtures.GeneratorPipelineTests.tearDown
    pipeline = fixtures.GeneratorPipelineTests.pipeline

    def test_investigator_publishes_three_questions_before_author_gets_their_entities(self):
        events = []
        publisher = self.publisher
        original_publish = publisher.publish_exemplars

        def publish(*args, **kwargs):
            events.append('publish_exemplars')
            return original_publish(*args, **kwargs)

        publisher.publish_exemplars = publish

        def prepare(current_publisher, source, directory):
            self.assertIs(current_publisher, publisher)
            events.append('prepare_reference')
            return {**fixtures.fixture_investigation(current_publisher, source, directory),
                    'needs_exemplars': True, 'reference_kp': 456}

        testcase = self

        class Session(fixtures.FakeSession):
            def __call__(self, role, context, directory):
                events.append(role)
                if role == 'investigate':
                    records = []
                    for index, band in enumerate(('easy', 'moderate', 'hard')):
                        item = record(20 + index)
                        item['knowledge_point'] = 123
                        item['question'][':question/difficulty'] = ':question.difficulty/' + band
                        records.append(item)
                    path = Path(context['workspace']) / 'exemplars.json'
                    path.write_text(json.dumps(records))
                    return {'status': 'ready', 'exemplars_file': 'exemplars.json',
                            'summary': 'Three complete examples.', 'evidence_paths': [], 'limitations': []}
                if role == 'author':
                    testcase.assertEqual(len(publisher.exemplar_publications), 1)
                    saved = json.loads(Path(context['exemplars_file']).read_text())
                    testcase.assertEqual([q[':db/id'] for q in saved], [1000, 1001, 1002])
                    testcase.assertEqual(context['investigation_file'], str(testcase.job / 'investigation/investigation.json'))
                return super().__call__(role, context, directory)

        session = Session()
        pipeline = Pipeline(self.job, self.request, publisher, root=self.root, environment=self.environment,
                            session=session, investigation_preparer=prepare)
        result = pipeline.run()
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual(events, ['prepare_reference', 'investigate', 'publish_exemplars', 'author', 'review'])
        self.assertTrue(result['investigation_complete'])
        self.assertEqual(result['exemplar_publication']['source'], ':agent/codex')

    def test_verifier_repairs_generator_and_engine_then_accepts_final_bytes_in_same_phase(self):
        testcase = self
        observations = {}
        pipeline = None

        class RepairingVerifier(fixtures.FakeSession):
            def __call__(self, role, context, directory):
                if role == 'review':
                    observations['before_package'] = context['review_binding']['package_hash']
                    observations['before_engine'] = context['review_binding']['engine_hash']
                    before = json.loads(Path(context['batch_file']).read_text())
                    testcase.assertTrue(any(int(q['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])
                        != int(q['question'][':question/problem'].split()[1]) ** 2 for q in before))
                    (Path(context['workspace']) / 'helper.py').write_text('def square(n): return n * n\n')
                    engine = Path(context['repo_root']) / 'engine/rust/grader.rs'
                    engine.parent.mkdir(parents=True)
                    engine.write_text('// Rebuilt engine fixture identity.\n')
                    finalized = pipeline.finalize_review(Path(context['evidence_root']))
                    observations['final_binding'] = finalized['binding']
                    context = pipeline.context(Path(context['evidence_root']))
                result = super().__call__(role, context, directory)
                if role == 'author':
                    (Path(context['workspace']) / 'helper.py').write_text('def square(n): return n + n\n')
                return result

        session = RepairingVerifier()
        pipeline = self.pipeline(session)
        result = pipeline.run()
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual([role for role, _ in session.calls], ['author', 'review'])
        self.assertNotEqual(result['package_hash'], observations['before_package'])
        self.assertNotEqual(result['engine_hash'], observations['before_engine'])
        self.assertEqual(result['review_binding'], digest(observations['final_binding']))
        installed = resolve_registered_script(result['registration'], self.root, self.math)
        self.assertEqual(installed.with_name('helper.py').read_text(), 'def square(n): return n * n\n')
        publication = json.loads((self.job / 'publication/request.json').read_text())
        for record in publication['records']:
            question = record['question']
            number = int(question[':question/problem'].split()[1])
            self.assertEqual(int(question[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']), number ** 2)

    def test_relative_images_are_hashed_and_published_from_generator_output_directory(self):
        class RelativeImages(fixtures.FakeSession):
            def __call__(self, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == 'author':
                    path = Path(context['workspace']) / 'generator.py'
                    path.write_text(path.read_text().replace('str(image)', 'image.name'))
                return result

        pipeline = self.pipeline(RelativeImages(image=True))
        result = pipeline.run()
        self.assertEqual(result['stage'], 'verified')
        output = self.job / 'outputs-1'
        self.assertEqual(result['assets_directory'], str(output))
        self.assertEqual(self.publisher.prepare_options['assets_directory'], str(output))
        self.assertTrue(result['assets'])
        self.assertTrue(all(Path(path).parent == output and Path(path).is_file() for path in result['assets']))
        self.assertFalse(list(Path(result['runtime']).glob('question-*.svg')))

    def test_accepted_historical_observation_never_invokes_inventory_repair(self):
        class HistoricalObservation(fixtures.FakeSession):
            def __call__(self, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == 'review':
                    result['findings'] = [{'kind': 'inventory', 'description': 'An imported source lacks its solution.',
                        'source_refs': ['q-1'], 'reproduction': 'Inspect the captured source.',
                        'requested_change': 'Leave the import unchanged; the complete generator is verified.'}]
                return result

        pipeline = self.pipeline(HistoricalObservation())
        with patch.object(pipeline, 'repair_inventory', side_effect=AssertionError('Historical observation triggered mutation')) as repair:
            result = pipeline.run()
        self.assertEqual(result['stage'], 'verified')
        repair.assert_not_called()
        self.assertFalse(list(self.job.rglob('affected-inventory.json')))
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_missing_report_evidence_returns_to_same_verifier_without_author_roundtrip(self):
        contexts = []

        class CompleteOwnReport(fixtures.FakeSession):
            def __call__(self, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == 'review':
                    contexts.append(context)
                    evidence = Path(context['evidence_root'])
                    if len(contexts) == 1:
                        (evidence / 'events.jsonl').write_text(json.dumps({'type': 'thread.started', 'thread_id': 'verifier-thread'}) + '\n')
                    else:
                        (evidence / 'arithmetic.json').write_text('{"checked":true}')
                    result['checks']['math']['evidence_paths'] = ['arithmetic.json']
                return result

        session = CompleteOwnReport()
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual([role for role, _ in session.calls], ['author', 'review', 'review'])
        self.assertEqual(contexts[1]['resume_session_id'], 'verifier-thread')
        self.assertEqual(contexts[0]['evidence_root'], contexts[1]['evidence_root'])
        self.assertEqual(result['attempt'], 1)


if __name__ == '__main__':
    unittest.main()
