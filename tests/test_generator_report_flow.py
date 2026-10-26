"""Exercise independent report repair and real generator repairs end to end."""
import json
import os
import subprocess
import sys
from pathlib import Path
import textwrap
import unittest
from unittest.mock import patch

import test_generator_pipeline as fixtures
from generator_packages import resolve_registered_script


def report_finding(kind="evidence"):
    return {"kind": kind, "description": "The review omitted its independently computed measurement.",
            "source_refs": ["fixture-source-1"], "reproduction": "Inspect measurements.json in evidence_root.",
            "requested_change": "Save the independent measurement and repair the report reference."}


class ReportSession(fixtures.FakeSession):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.review_contexts = []

    def __call__(self, role, context, directory):
        if role == "review":
            self.review_contexts.append((Path(directory), dict(context)))
        return super().__call__(role, context, context["evidence_root"] if role == "review" else directory)


class GeneratorReportFlowTests(unittest.TestCase):
    setUp = fixtures.GeneratorPipelineTests.setUp
    tearDown = fixtures.GeneratorPipelineTests.tearDown
    pipeline = fixtures.GeneratorPipelineTests.pipeline

    def test_invalid_report_is_corrected_in_original_evidence_root_and_published(self):
        class CorrectedReport(ReportSession):
            def __call__(self, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == "review":
                    if context.get("review_contract_feedback"):
                        evidence = Path(context["evidence_root"])
                        (evidence / "measurements.json").write_text('{"independent_check":true}')
                    result["checks"]["math"]["evidence_paths"] = ["measurements.json"]
                return result

        session = CorrectedReport()
        pipeline = self.pipeline(session)
        with patch.object(pipeline, "sample", wraps=pipeline.sample) as sample:
            result = pipeline.run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual([role for role, _ in session.calls], ["author", "review", "review"])
        self.assertEqual((result["attempt"], sample.call_count), (1, 1))
        first_directory, first_context = session.review_contexts[0]
        repair_directory, repair_context = session.review_contexts[1]
        self.assertEqual(repair_directory, first_directory / "contract-repair")
        self.assertEqual(first_context["evidence_root"], repair_context["evidence_root"])
        self.assertTrue((first_directory / "measurements.json").is_file())
        self.assertEqual(Path(result["review"]), first_directory / "result.json")
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_valid_evidence_only_rejections_have_one_durable_budget_without_authors(self):
        class UncorrectedReport(ReportSession):
            def __call__(self, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == "review":
                    result.update(verdict="revise", findings=[report_finding()])
                    result["checks"]["math"]["status"] = "failed"
                return result

        session = UncorrectedReport()
        result = self.pipeline(session).run()
        self.assertEqual(result["stage"], "blocked")
        self.assertEqual(result["error"]["code"], "verification_unfinished")
        self.assertEqual(result["error"]["resume_stage"], "validate")
        self.assertEqual([role for role, _ in session.calls], ["author"] + ["review"] * 6)
        self.assertEqual(list(result["review_report_rounds"].values()), [6])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))
        original_samples = (self.job / "samples.json").read_bytes()
        restart = UncorrectedReport()
        for _ in range(3):
            self.assertEqual(self.pipeline(restart, attempts=100).run()["stage"], "blocked")
        self.assertEqual(restart.calls, [])
        self.assertEqual((self.job / "samples.json").read_bytes(), original_samples)
        self.assertEqual(len(json.loads((self.job / "repair-history.json").read_text())["findings"]), 1)

    def test_report_only_unsupported_returns_to_reviewer_instead_of_author(self):
        class PermissionReport(ReportSession):
            def __call__(self, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == "review" and not context.get("review_contract_feedback"):
                    result.update(verdict="unsupported", findings=[report_finding()])
                    result["checks"]["math"]["status"] = "failed"
                return result

        session = PermissionReport()
        result = self.pipeline(session).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual([role for role, _ in session.calls], ["author", "review", "review"])
        self.assertEqual(result["attempt"], 1)
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_engine_change_does_not_add_another_report_correction(self):
        pipeline = self.pipeline(fixtures.FakeSession())
        pipeline.run(stop_after="generate")
        original_evidence = pipeline.review_directory()
        original_binding = dict(pipeline.review_binding())
        pipeline.persist(report_repair_directory=str(original_evidence),
                         review_report_rounds={str(original_evidence): 1},
                         review_report_error="Save the missing independent measurement.",
                         review_report_result_file=str(original_evidence / "result.json"))

        class ChangedEngine(ReportSession):
            def __call__(self, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == "review" and len(self.review_contexts) == 1:
                    (Path(context['evidence_root']) / 'events.jsonl').write_text(
                        json.dumps({'type': 'thread.started', 'thread_id': 'engine-repair-thread'}) + '\n')
                    engine = Path(context["repo_root"]) / "engine/rust/grader.rs"
                    engine.parent.mkdir(parents=True)
                    engine.write_text("// Shared grader extension with its own regression tests.\n")
                return result

        session = ChangedEngine()
        result = self.pipeline(session).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual([role for role, _ in session.calls], ['review'])
        directory, context = session.review_contexts[0]
        self.assertEqual(directory, original_evidence / 'contract-repair')
        self.assertEqual(context['review_binding'], original_binding)
        self.assertEqual(Path(result['review']), original_evidence / 'result.json')
        self.assertEqual(json.loads((original_evidence / 'review-binding.json').read_text()), original_binding)
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_demonstrated_generator_defect_is_fixed_rechecked_and_published_by_verifier(self):
        pipeline = None
        class ArithmeticRepair(ReportSession):
            def __init__(self):
                super().__init__()
                self.math_observations = []

            def inspect(self, context):
                records = json.loads(Path(context['batch_file']).read_text())
                failures = []
                for record in records:
                    question = record['question']
                    number = int(question[':question/problem'].split()[1])
                    actual = int(question[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])
                    if actual != number * number:
                        failures.append({'number': number, 'actual': actual, 'expected': number * number})
                self.math_observations.append(failures)
                return failures

            def __call__(inner, role, context, directory):
                if role == 'review':
                    evidence = Path(context['evidence_root'])
                    failures = inner.inspect(context)
                    (evidence / 'arithmetic-before.json').write_text(json.dumps({'failures': failures}))
                    pipeline.remember_repair({'findings': [{
                        'kind': 'math', 'description': 'Squaring adds the input twice.',
                        'source_refs': ['fixture-source-1'], 'reproduction': 'square(7) == 14, expected 49.',
                        'requested_change': 'Multiply the input by itself.'}]})
                    (Path(context['workspace']) / 'helper.py').write_text('def square(n): return n * n\n')
                    context = fixtures.finalize_fixture_review(pipeline, context)
                    failures = inner.inspect(context)
                    (evidence / 'arithmetic.json').write_text(json.dumps({'failures': failures}))
                    self.assertEqual(failures, [])
                result = super().__call__(role, context, directory)
                if role == 'author':
                    (Path(context['workspace']) / 'helper.py').write_text('def square(n): return n + n\n')
                if role == 'review':
                    result['checks']['math']['evidence_paths'] = ['arithmetic.json']
                return result

        session = ArithmeticRepair()
        pipeline = self.pipeline(session)
        result = pipeline.run()
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual([role for role, _ in session.calls], ['author', 'review'])
        self.assertTrue(session.math_observations[0])
        self.assertEqual(session.math_observations[1], [])
        preflight = json.loads((self.job / 'repair-preflight.json').read_text())
        self.assertTrue(preflight['passed'])
        self.assertEqual(len(preflight['finding_ids']), 1)
        installed = resolve_registered_script(result['registration'], self.root, self.math)
        self.assertEqual(installed.with_name('helper.py').read_text(), 'def square(n): return n * n\n')
        publication = json.loads((self.job / 'publication/request.json').read_text())
        for record in publication['records']:
            question = record['question']
            number = int(question[':question/problem'].split()[1])
            self.assertEqual(int(question[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']), number * number)
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_verifier_repairs_batch_rule_and_checks_prospective_then_final_batch(self):
        pipeline = None
        class BatchRepair(ReportSession):
            def __init__(self):
                super().__init__()
                self.reviewed_prompts = []

            def __call__(inner, role, context, directory):
                if role == 'investigate':
                    return super().__call__(role, context, directory)
                workspace = Path(context['workspace'])
                if role == 'review':
                    evidence = Path(context['evidence_root'])
                    rows = json.loads(Path(context['batch_file']).read_text())
                    old = [row['question'][':question/problem'] for row in rows]
                    inner.reviewed_prompts.append(old)
                    self.assertEqual(len(set(old)), 1)
                    retained = evidence / 'rejected-batch.json'
                    retained.write_text(json.dumps(rows))
                    pipeline.remember_repair({'findings': [{
                        'kind': 'restriction', 'description': 'Batch selection repeats one question.',
                        'source_refs': ['fixture-source-1'], 'reproduction': 'All requested prompts match.',
                        'requested_change': 'Sample distinct mathematical instances.'}]})
                    script = textwrap.dedent("""\
                        import json, os, subprocess, sys, tempfile
                        from pathlib import Path
                        old = json.loads(Path(RETAINED_BATCH).read_text())
                        with tempfile.TemporaryDirectory() as output:
                            run = subprocess.run([sys.executable, '-E', '-s', '-B', 'generator.py',
                                '--difficulty', BAND, '--count', str(COUNT), '--seed', str(SEED), '--format', 'json'],
                                env={**os.environ, 'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR': output},
                                capture_output=True, text=True, check=True)
                        prospective = json.loads(run.stdout)
                        prompts = lambda records: [r['question'][':question/problem'] for r in records]
                        assert len(set(prompts(old))) == 1
                        assert len(set(prompts(prospective))) == COUNT, 'Batch-selection defect remains'
                        Path('prospective-batch.json').write_text(json.dumps({
                            'seed': SEED, 'old': prompts(old), 'fixed': prompts(prospective)}))
                    """)
                    bindings = {'RETAINED_BATCH': str(retained), 'BAND': context['requested_difficulty'],
                                'COUNT': context['count'], 'SEED': context['sample_seed']}
                    check = workspace / 'batch_regression.py'
                    check.write_text('\n'.join(f'{key} = {value!r}' for key, value in bindings.items()) + '\n' + script)
                    findings = json.loads(Path(context['repair_history_file']).read_text())['findings']
                    (workspace / 'repair-regressions.json').write_text(json.dumps({'findings': [
                        {'id': row['id'], 'script': 'batch_regression.py'} for row in findings]}))
                    before = subprocess.run([sys.executable, str(check)], cwd=workspace,
                        capture_output=True, text=True)
                    self.assertNotEqual(before.returncode, 0)
                    generator = workspace / 'generator.py'
                    generator.write_text(generator.read_text().replace('[2] * args.count',
                        'random.Random(args.seed).sample(range(2, 99), args.count)'))
                    pipeline.finalize_review(evidence)
                    context = pipeline.context(evidence)
                    rows = json.loads(Path(context['batch_file']).read_text())
                    inner.reviewed_prompts.append([row['question'][':question/problem'] for row in rows])
                result = super().__call__(role, context, directory)
                if role == 'author':
                    generator = workspace / 'generator.py'
                    generator.write_text(generator.read_text().replace(
                        'random.Random(args.seed).sample(range(2, 99), args.count)', '[2] * args.count'))
                return result

        session = BatchRepair()
        pipeline = self.pipeline(session)
        state = pipeline.run()
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual([role for role, _ in session.calls], ['author', 'review'])
        evidence = json.loads((self.job / 'workspace/prospective-batch.json').read_text())
        self.assertEqual(evidence['seed'], state['seed'])
        self.assertEqual(evidence['old'], session.reviewed_prompts[0])
        self.assertEqual(evidence['fixed'], session.reviewed_prompts[1])
        self.assertEqual(len(set(evidence['old'])), 1)
        self.assertEqual(len(set(evidence['fixed'])), self.request['count'])
        self.assertTrue(json.loads((self.job / 'repair-preflight.json').read_text())['passed'])
        publication = json.loads((self.job / 'publication/request.json').read_text())
        self.assertEqual([row['question'][':question/problem'] for row in publication['records']], evidence['fixed'])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))


if __name__ == "__main__":
    unittest.main()
