"""Exercise independent report repair and real generator repairs end to end."""
import json
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
        self.assertEqual(result["error"]["code"], "review_report_correction_exhausted")
        self.assertEqual(result["error"]["resume_stage"], "validate")
        self.assertEqual([role for role, _ in session.calls], ["author", "review", "review", "review"])
        self.assertEqual(list(result["review_report_rounds"].values()), [3])
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

    def test_engine_change_during_report_correction_requires_fresh_review(self):
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
                    engine = Path(context["repo_root"]) / "engine/rust/grader.rs"
                    engine.parent.mkdir(parents=True)
                    engine.write_text("// Different grader requires independent verification.\n")
                return result

        session = ChangedEngine()
        result = self.pipeline(session).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual([role for role, _ in session.calls], ["review", "review"])
        first_directory, first_context = session.review_contexts[0]
        second_directory, second_context = session.review_contexts[1]
        self.assertEqual(first_directory, original_evidence / "contract-repair")
        self.assertNotEqual(first_context["evidence_root"], second_context["evidence_root"])
        self.assertNotEqual(first_context["review_binding"]["engine_hash"], second_context["review_binding"]["engine_hash"])
        self.assertEqual(json.loads((original_evidence / "review-binding.json").read_text()), original_binding)
        self.assertEqual(Path(result["review"]), second_directory / "result.json")
        self.assertEqual(json.loads((second_directory / "review-binding.json").read_text()), second_context["review_binding"])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_demonstrated_generator_defect_is_fixed_rechecked_and_published(self):
        class ArithmeticRepair(ReportSession):
            def __init__(self):
                super().__init__()
                self.math_observations = []

            def __call__(self, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == "author" and len([r for r, _ in self.calls if r == "author"]) == 1:
                    (Path(context["workspace"]) / "helper.py").write_text("def square(n): return n + n\n")
                if role == "review":
                    records = json.loads(Path(context["batch_file"]).read_text())
                    failures = []
                    for record in records:
                        question = record["question"]
                        number = int(question[":question/problem"].split()[1])
                        actual = int(question[":question/answer-fields"][0][":answer-field/choices"][0][":answer/value"])
                        if actual != number * number:
                            failures.append({"number": number, "actual": actual, "expected": number * number})
                    self.math_observations.append(failures)
                    (Path(context["evidence_root"]) / "arithmetic.json").write_text(json.dumps({"failures": failures}))
                    result["checks"]["math"]["evidence_paths"] = ["arithmetic.json"]
                    if failures:
                        result.update(verdict="revise", findings=[{
                            "kind": "math", "description": "The square operation adds its input twice.",
                            "source_refs": ["fixture-source-1"], "reproduction": "helper.square(7) returns 14; expected 49.",
                            "requested_change": "Multiply the input by itself and retain square(7)==49 as a regression."}])
                        result["checks"]["math"]["status"] = "failed"
                return result

        session = ArithmeticRepair()
        result = self.pipeline(session).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual([role for role, _ in session.calls], ["author", "review", "author", "review"])
        self.assertTrue(session.math_observations[0])
        self.assertEqual(session.math_observations[1], [])
        preflight = json.loads((self.job / "repair-preflight.json").read_text())
        self.assertTrue(preflight["passed"])
        self.assertEqual(len(preflight["finding_ids"]), 1)
        installed = resolve_registered_script(result["registration"], self.root, self.math)
        self.assertEqual(installed.with_name("helper.py").read_text(), "def square(n): return n * n\n")
        publication = json.loads((self.job / "publication/request.json").read_text())
        for record in publication["records"]:
            question = record["question"]
            number = int(question[":question/problem"].split()[1])
            self.assertEqual(int(question[":question/answer-fields"][0][":answer-field/choices"][0][":answer/value"]), number * number)
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_batch_repair_checks_current_generator_before_runner_replaces_rejected_batch(self):
        class BatchRepair(ReportSession):
            def __init__(self):
                super().__init__()
                self.reviewed_prompts = []

            def __call__(self, role, context, directory):
                result = super().__call__(role, context, directory)
                workspace = Path(context['workspace'])
                if role == 'author':
                    if len([r for r, _ in self.calls if r == 'author']) == 1:
                        generator = workspace / 'generator.py'
                        generator.write_text(generator.read_text().replace(
                            'random.Random(args.seed).sample(range(2, 99), args.count)', '[2] * args.count'))
                    else:
                        # The author repairs package code. Its regression can
                        # check the prospective batch without editing samples.
                        script = textwrap.dedent('''\
                            import json, os, subprocess, sys, tempfile
                            from pathlib import Path
                            old = json.loads(Path(BATCH_FILE).read_text())
                            with tempfile.TemporaryDirectory() as output:
                                result = subprocess.run(
                                    [sys.executable, '-E', '-s', '-B', 'generator.py',
                                     '--difficulty', BAND, '--count', str(COUNT),
                                     '--seed', str(SEED), '--format', 'json'],
                                    env={**os.environ, 'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR': output},
                                    capture_output=True, text=True, check=True)
                            prospective = json.loads(result.stdout)
                            prompts = lambda rows: [r['question'][':question/problem'] for r in rows]
                            assert len(set(prompts(old))) == 1, 'Saved rejected batch changed prematurely'
                            assert len(set(prompts(prospective))) == COUNT, 'Batch-selection defect remains'
                            Path('prospective-batch.json').write_text(json.dumps({
                                'seed': SEED, 'old': prompts(old), 'fixed': prompts(prospective)}))
                        ''')
                        bindings = {'BATCH_FILE': context['batch_file'], 'BAND': context['requested_difficulty'],
                                    'COUNT': context['count'], 'SEED': context['sample_seed']}
                        (workspace / 'batch_regression.py').write_text(
                            '\n'.join(f'{key} = {value!r}' for key, value in bindings.items()) + '\n' + script)
                        findings = json.loads(Path(context['repair_history_file']).read_text())['findings']
                        (workspace / 'repair-regressions.json').write_text(json.dumps({'findings': [
                            {'id': row['id'], 'script': 'batch_regression.py'} for row in findings]}))
                else:
                    rows = json.loads(Path(context['batch_file']).read_text())
                    prompts = [row['question'][':question/problem'] for row in rows]
                    self.reviewed_prompts.append(prompts)
                    if len(set(prompts)) != len(prompts):
                        result.update(verdict='revise', findings=[{
                            'kind': 'restriction', 'description': 'Batch selection repeats one question.',
                            'source_refs': ['fixture-source-1'], 'reproduction': f'seed={context["sample_seed"]}: all prompts match.',
                            'requested_change': 'Repair generator sampling to select distinct questions in each finite batch.'}])
                        result['checks']['variety']['status'] = 'failed'
                return result

        session = BatchRepair()
        state = self.pipeline(session).run()
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual([role for role, _ in session.calls], ['author', 'review', 'author', 'review'])
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
