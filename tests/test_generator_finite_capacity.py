"""Finite batch bounds exercise real CLIs; agent/EDB I/O stays fake."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from generator_pipeline import Pipeline, generation_limits
from test_generator_pipeline import FakePublisher, FakeSession, fixture_investigation, write_package

NAME = 'generation-limits.json'
FORMAT = 'course-academy-generator-limits-v1'
LIMITS = {'format': FORMAT, 'maximum_distinct_batch': {'easy': 4}}


def finite_package(directory, *, declared=True):
    manifest = write_package(directory)
    path = directory/'generator.py'
    code = path.read_text().replace('args = parser.parse_args()',
        "args = parser.parse_args()\nif args.difficulty == 'easy' and args.count > 4:\n    parser.error('easy has only four distinct calculations')")
    code = code.replace('range(2, 99), args.count',
                        "(range(2, 6) if args.difficulty == 'easy' else range(2, 99)), args.count")
    path.write_text(code)
    (directory/NAME).write_text(json.dumps(LIMITS))
    if declared: manifest['files'].append(NAME)
    (directory/'package.json').write_text(json.dumps(manifest))
    return manifest


class FiniteSession(FakeSession):
    def __init__(self):
        super().__init__()
        self.review_contexts = []

    def __call__(self, role, context, directory):
        result = super().__call__(role, context, directory)
        if role == 'author': finite_package(Path(context['workspace']))
        if role == 'review': self.review_contexts.append(context)
        return result


class GeneratorFiniteCapacityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.math = self.root/'math'
        self.environment = {**os.environ, 'EDB_MATH_ROOT': str(self.math),
                            'COURSE_ACADEMY_GENERATOR_PYTHON': sys.executable}

    def tearDown(self):
        for path in self.root.rglob('*'):
            if path.is_dir() and not path.is_symlink(): path.chmod(0o755)
        self.temp.cleanup()

    def pipeline(self, *, difficulty='easy', count=5, refill=False, name='job', session=None, publisher=None, registration=None):
        request = {'kp': 123, 'difficulty': difficulty, 'count': count, 'existing_entrypoint': None}
        if refill: request.update(job_kind='refill', registered_package=registration)
        return Pipeline(self.root/name, request, publisher or FakePublisher(self.root/(name+'-publisher')),
                        root=self.root, environment=self.environment, session=session or FakeSession(),
                        investigation_preparer=fixture_investigation)

    def sampling_pipeline(self, *, declared=True, difficulty='easy', count=5, refill=False, name='sample'):
        pipeline = self.pipeline(difficulty=difficulty, count=count, refill=refill, name=name)
        workspace = pipeline.directory/'workspace'
        finite_package(workspace, declared=declared)
        pipeline.persist(manifest='package.json', seed=17)
        return pipeline

    def test_real_finite_cli_rejects_oversize_but_primary_sampling_caps_count(self):
        pipeline = self.sampling_pipeline(count=9)
        source, _ = pipeline.manifest()
        command = [sys.executable, str(source/'generator.py'), '--difficulty', 'easy',
                   '--count', '5', '--seed', '17', '--format', 'json']
        failed = subprocess.run(command, capture_output=True, text=True,
                                env={**self.environment, 'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR': str(self.root/'direct-output')})
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('only four distinct calculations', failed.stderr)
        pipeline.sample()
        row = pipeline.state['verification_batches']['easy']
        self.assertEqual((row['requested_count'], row['count'], row['maximum_distinct_batch']), (9, 4, 4))
        self.assertEqual(len(json.loads(Path(row['batch_file']).read_text())), 4)
        self.assertEqual(pipeline.state['batch_metadata'], {'requested_count': 9, 'count': 4, 'maximum_distinct_batch': 4})
        self.assertEqual(pipeline.review_binding()['verification_batches']['easy']['count'], 4)
        self.assertEqual(pipeline.state['verification_batches']['hard']['count'], 9)
        self.assertIn(NAME, [p.name for p in Path(row['runtime']).iterdir()])

    def test_secondary_verification_and_refill_sampling_both_cap_without_changing_request(self):
        pipeline = self.sampling_pipeline(difficulty='moderate', count=3, name='secondary')
        pipeline.sample()
        easy = pipeline.state['verification_batches']['easy']
        self.assertEqual((easy['requested_count'], easy['count']), (5, 4))
        self.assertEqual(pipeline.state['verification_batches']['moderate']['count'], 3)
        self.assertEqual(pipeline.state['request']['count'], 3)
        refill = self.sampling_pipeline(count=8, refill=True, name='refill-sample')
        refill.sample()
        self.assertEqual(refill.state['verification_batches'], {})
        self.assertEqual(refill.state['batch_metadata'], {'requested_count': 8, 'count': 4, 'maximum_distinct_batch': 4})
        self.assertEqual(len(refill.publication_records()), 4)

    def test_undeclared_limit_is_ignored_and_no_limit_preserves_existing_counts(self):
        pipeline = self.sampling_pipeline(declared=False, name='undeclared')
        # Even malformed undeclared data must not influence package execution.
        (pipeline.directory/'workspace'/NAME).write_text('not JSON')
        self.assertEqual(generation_limits(*pipeline.manifest()), {})
        with self.assertRaisesRegex(ValueError, 'only four distinct calculations'):
            pipeline.sample()
        self.assertFalse((pipeline.directory/'runtime-0'/NAME).exists())
        regular = self.pipeline(count=6, name='unrestricted')
        write_package(regular.directory/'workspace')
        regular.persist(manifest='package.json')
        regular.sample()
        for row in regular.state['verification_batches'].values():
            self.assertEqual((row['requested_count'], row['count']), (6, 6))
            self.assertNotIn('maximum_distinct_batch', row)

    def test_declared_malformed_missing_or_invalid_limits_fail_before_cli(self):
        pipeline = self.sampling_pipeline(name='invalid')
        source, manifest = pipeline.manifest()
        invalid = [None, [], {}, {'format': 'unknown', 'maximum_distinct_batch': {'easy': 4}},
                   {'format': FORMAT, 'maximum_distinct_batch': []},
                   {'format': FORMAT, 'maximum_distinct_batch': {'unclassified': 4}}]
        invalid += [{'format': FORMAT, 'maximum_distinct_batch': {'easy': value}}
                    for value in (0, -1, True, 4.0, '4', None)]
        for value in invalid:
            with self.subTest(value=value):
                (source/NAME).write_text(json.dumps(value))
                with patch('generator_pipeline.subprocess.run') as run, self.assertRaisesRegex(ValueError, 'generation-limits'):
                    pipeline.sample()
                run.assert_not_called()
        (source/NAME).write_text('{')
        with self.assertRaisesRegex(ValueError, 'generation-limits'): generation_limits(source, manifest)
        (source/NAME).unlink()
        with self.assertRaisesRegex(ValueError, 'generation-limits'): generation_limits(source, manifest)
        (source/NAME).write_text(json.dumps({'format': FORMAT, 'maximum_distinct_batch': {}}))
        self.assertEqual(generation_limits(source, manifest), {})
        (source/NAME).write_text(json.dumps({'format': FORMAT, 'maximum_distinct_batch': {'easy': 1, 'hard': 7}}))
        self.assertEqual(generation_limits(source, manifest), {'easy': 1, 'hard': 7})

    def test_pipeline_still_requires_exactly_the_capped_count(self):
        pipeline = self.sampling_pipeline(name='wrong-count')
        source, _ = pipeline.manifest()
        code = (source/'generator.py').read_text().replace('print(json.dumps(records, sort_keys=True))',
                                                        'print(json.dumps(records[:-1], sort_keys=True))')
        (source/'generator.py').write_text(code)
        with self.assertRaisesRegex(ValueError, 'exactly the requested number'):
            pipeline.sample()

    def test_all_band_approval_and_fast_refill_report_actual_four_item_publication(self):
        session = FiniteSession()
        pipeline = self.pipeline(count=5, session=session, name='approval')
        state = pipeline.run()
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual(set(state['verified_bands']), {'easy', 'moderate', 'hard'})
        context = session.review_contexts[0]
        self.assertEqual((context['requested_count'], context['count']), (5, 4))
        approval = json.loads(pipeline.approval_path().read_text())
        easy = approval['verification_binding']['verification_batches']['easy']
        self.assertEqual((easy['requested_count'], easy['count'], easy['maximum_distinct_batch']), (5, 4, 4))
        self.assertEqual(approval['verification_binding']['verification_batches']['hard']['count'], 5)
        self.assertEqual(approval['publication']['receipt']['new_questions'], 4)
        publisher = FakePublisher(self.root/'fast-publisher')
        publisher.registered_generator = {':question-generator/script': state['registration']}
        refill_session = FakeSession()
        refill = self.pipeline(count=11, refill=True, name='fast', publisher=publisher,
                               session=refill_session, registration=state['registration'])
        result = refill.run()
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual(refill_session.calls, [])
        self.assertEqual(result['publication']['new_questions'], 4)
        self.assertEqual(result['batch_metadata'], {'count': 4, 'requested_count': 11, 'maximum_distinct_batch': 4})
        self.assertEqual(result['request']['count'], 11)
        self.assertEqual(len(refill.publication_records()), 4)

    def test_actual_trig_cli_and_pipeline_primary_refill_and_secondary_when_available(self):
        package = ROOT/'generate/repairs/2026-11-04-four-trig-lessons/sine-double/17592186059672'
        if not (package/'generator.py').exists(): self.skipTest('Trig repair package is not present in this checkout')
        closure = json.loads((package/'runtime-manifest.json').read_text())
        failed = subprocess.run([sys.executable, str(package/'generator.py'), '--difficulty', 'easy',
                                 '--count', '5', '--seed', '17', '--format', 'json'], capture_output=True, text=True)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('at most 4', failed.stderr)
        for difficulty, refill, expected_request in [('easy', False, 7), ('easy', True, 7), ('moderate', False, 5)]:
            with self.subTest(difficulty=difficulty, refill=refill):
                pipeline = self.pipeline(difficulty=difficulty, count=7 if difficulty=='easy' else 3,
                                         refill=refill, name='trig-'+difficulty+str(refill))
                workspace = pipeline.directory/'workspace'; workspace.mkdir()
                for name in closure['runtime_files']: shutil.copyfile(package/name, workspace/name)
                manifest = {'entrypoint': 'generator.py', 'files': closure['runtime_files'], 'dependencies': closure['dependencies']}
                (workspace/'package.json').write_text(json.dumps(manifest))
                pipeline.persist(manifest='package.json', seed=17)
                pipeline.sample()
                row = pipeline.state['batch_metadata'] if difficulty=='easy' else pipeline.state['verification_batches']['easy']
                self.assertEqual((row['requested_count'], row['count'], row['maximum_distinct_batch']), (expected_request, 4, 4))
                if difficulty=='easy': self.assertEqual(len(pipeline.publication_records()), 4)


if __name__ == '__main__': unittest.main()
