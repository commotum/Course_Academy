"""Exercise independent report repair and real generator repairs end to end."""
import json
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
