import copy
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generator_review import CHECKS, validate_review, _inventory_evidence, main
from generator_review_fixtures import write_decision_evidence


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReviewEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        (self.directory / "source-analysis.json").write_text('{"skill":"read an entry"}')
        (self.directory / "measurements.json").write_text('{"targets":["11","12","21","22"]}')
        self.review = {
            "verdict": "accepted", "summary": "Source-supported entry reading with four targets.",
            "source_analysis": {"skill": "read matrix entries", "reasoning_steps": ["row then column"],
                                "invariants": ["one entry, no arithmetic"], "permitted_variations": ["row, column, integer values"],
                                "source_refs": ["fixture-q11", "fixture-q12", "fixture-q21", "fixture-q22"],
                                "evidence_paths": ["source-analysis.json"]},
            "checks": {name: {"status": "passed", "details": "Recorded reproducible check.",
                              "evidence_paths": ["measurements.json"]} for name in CHECKS},
            "findings": [],
        }

        evidence = write_decision_evidence(self.directory)
        self.review["checks"]["decision_variation"]["evidence_paths"] = [evidence]
        self.review["checks"]["scope"]["evidence_paths"] = ['solution-paths.json']

    def tearDown(self):
        self.temp.cleanup()

    def test_structured_acceptance_needs_real_evidence_and_no_failures(self):
        validate_review(self.review, self.directory)
        for mutation in (
            lambda result: result["checks"]["variety"].update(status="failed"),
            lambda result: result["checks"]["scope"].update(status="not_applicable"),
            lambda result: result["checks"]["rendering"].update(status="not_applicable"),
            lambda result: result["checks"]["math"].update(evidence_paths=[]),
            lambda result: result["checks"]["grading"].update(evidence_paths=["invented.json"]),
            lambda result: result["source_analysis"].update(source_refs=[]),
            lambda result: result["source_analysis"].update(evidence_paths=[]),
        ):
            result = copy.deepcopy(self.review)
            mutation(result)
            with self.assertRaises(ValueError):
                validate_review(result, self.directory)
        (self.directory / "source-analysis.json").write_text("source analysis was done")
        with self.assertRaises(ValueError):
            validate_review(self.review, self.directory)

    def test_empty_external_and_symlink_evidence_cannot_satisfy_gate(self):
        (self.directory / "empty.json").touch()
        external = self.directory.parent / (self.directory.name + "-outside.json")
        external.write_text("outside")
        try:
            (self.directory / "link.json").symlink_to(external)
            for path in ("empty.json", str(external), "../" + external.name, "link.json"):
                result = copy.deepcopy(self.review)
                result["checks"]["math"]["evidence_paths"] = [path]
                with self.assertRaises(ValueError):
                    validate_review(result, self.directory)
        finally:
            external.unlink()

    def test_repair_requires_actionable_findings_and_cannot_be_accepted(self):
        self.review["verdict"] = "revise"
        with self.assertRaises(ValueError):
            validate_review(self.review, self.directory)
        self.review["findings"] = [{
            "kind": "restriction", "description": "Only the upper-left target is sampled.",
            "source_refs": ["fixture-q12", "fixture-q21", "fixture-q22"],
            "reproduction": "Generate seeds 0 through 63; every prompt asks a11.",
            "requested_change": "Sample all four eligible targets.",
        }]
        validate_review(self.review, self.directory)
        self.review["verdict"] = "accepted"
        with self.assertRaises(ValueError):
            validate_review(self.review, self.directory)

    def test_old_or_cosmetic_only_reviews_cannot_pass_new_gate(self):
        legacy = copy.deepcopy(self.review)
        del legacy["checks"]["decision_variation"]
        with self.assertRaisesRegex(ValueError, "eight named checks"):
            validate_review(legacy, self.directory)
        self.review["checks"]["decision_variation"]["evidence_paths"] = ["measurements.json"]
        with self.assertRaisesRegex(ValueError, "pedagogical-variation.json"):
            validate_review(self.review, self.directory)

    def test_distribution_evidence_rejects_missing_pairs_aggregate_only_and_known_shortcuts(self):
        path = self.directory / "pedagogical-variation.json"
        original = json.loads(path.read_text())
        for change in (
            lambda r: r.update(counterfactuals=r["counterfactuals"][:1]),
            lambda r: r["counterfactuals"][0].update(status="failed"),
            lambda r: r["shortcut_probes"][0].update(scope="overall"),
            lambda r: r["shortcut_probes"][0].update(disposition="defect"),
            lambda r: r["shortcut_probes"][0].update(correct=3),
            lambda r: r["delivery"].update(sample_refs=[]),
            lambda r: r["coverage"][0].update(sample_refs=["not-created.json"]),
            lambda r: r["fixed_features"][0].update(justification=""),
        ):
            report = copy.deepcopy(original)
            change(report)
            path.write_text(json.dumps(report))
            with self.assertRaises(ValueError):
                validate_review(self.review, self.directory)
        path.write_text(json.dumps(original))
        validate_review(self.review, self.directory)

    def test_legitimate_invariant_needs_reasoning_not_random_answers(self):
        path = self.directory / "pedagogical-variation.json"
        report = json.loads(path.read_text())
        report["shortcut_probes"][0].update(correct=2, disposition="intended_skill",
            strategy="Recognize the source lesson's intended identity.",
            conclusion="In this narrowly scoped instructional family, recognizing the identity is the objective; no broader mastery claim.")
        path.write_text(json.dumps(report))
        validate_review(self.review, self.directory)

    def test_scope_requires_explicit_answer_transition_evidence(self):
        original = copy.deepcopy(self.review)
        self.review['checks']['scope']['evidence_paths'] = ['measurements.json']
        with self.assertRaisesRegex(ValueError, 'solution-paths.json'):
            validate_review(self.review, self.directory)
        self.review = original
        path = self.directory / 'solution-paths.json'
        saved = json.loads(path.read_text())
        for change in (
            lambda r: r.update(cases=[]),
            lambda r: r['cases'][0].update(status='failed'),
            lambda r: r['cases'][0].update(sample_refs=[]),
            lambda r: r['cases'][0].update(conversions=[{'rule': 'sine oddness', 'scope_source': '',
                'shown_step': '', 'status': 'passed'}]),
            lambda r: r['cases'][0].update(conversions=[{'rule': 'sine oddness', 'scope_source': 'lesson',
                'shown_step': 'line 3', 'status': 'failed'}]),
        ):
            report = copy.deepcopy(saved)
            change(report)
            path.write_text(json.dumps(report))
            with self.assertRaises(ValueError):
                validate_review(self.review, self.directory)
        path.write_text(json.dumps(saved))
        validate_review(self.review, self.directory)

    def inventory_report(self):
        self.review.update(verdict='revise', findings=[{
            'kind': 'inventory', 'description': 'Stored bank reveals its answer.',
            'source_refs': ['q-original'], 'reproduction': 'Run the retained bank-only probe.',
            'requested_change': 'Resolve the stored defect separately from package repair.'}])
        return {'affected_questions': [{
            'question_id': '77c551c0-c155-56eb-9f11-d8d660941796', 'entity_id': 17592186524997,
            'finding': 'Bank-only shortcut', 'reproduction': 'Run retained probe.',
            'evidence_path': 'stored-original.json'}]}

    def test_explicit_pool_action_requires_complete_handoff(self):
        report = self.inventory_report()
        path = self.directory / 'affected-inventory.json'
        with self.assertRaisesRegex(ValueError, 'affected-inventory.json'):
            _inventory_evidence(self.directory)
        for invalid in ('{', '[]', '{"affected_questions":[]}'):
            path.write_text(invalid)
            with self.assertRaisesRegex(ValueError, 'affected-inventory.json'):
                _inventory_evidence(self.directory)
        path.write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError, 'evidence_path'):
            _inventory_evidence(self.directory)
        (self.directory / 'stored-original.json').write_text(json.dumps({
            ':db/id': 17592186524997, ':question/id': report['affected_questions'][0]['question_id'],
            ':question/math-academy-id': 'q-107463'}))
        for key, value in [('question_id', 'not-a-uuid'), ('entity_id', True),
                           ('entity_id', 0), ('finding', ''), ('reproduction', ''),
                           ('evidence_path', '../outside.json')]:
            invalid = copy.deepcopy(report)
            invalid['affected_questions'][0][key] = value
            path.write_text(json.dumps(invalid))
            with self.assertRaises(ValueError):
                _inventory_evidence(self.directory)

    def test_historical_inventory_observation_does_not_block_acceptance(self):
        self.inventory_report()
        self.review['verdict'] = 'accepted'
        validate_review(self.review, self.directory)
        self.assertFalse((self.directory / 'affected-inventory.json').exists())
        self.review['findings'][0]['kind'] = 'math'
        with self.assertRaisesRegex(ValueError, 'unresolved findings'):
            validate_review(self.review, self.directory)

    def test_report_cli_detects_omission_and_accepts_same_session_correction(self):
        from contextlib import redirect_stdout, redirect_stderr
        from io import StringIO
        result = self.directory / 'final-result.json'
        invalid = copy.deepcopy(self.review)
        invalid['checks']['math']['evidence_paths'] = ['missing.json']
        result.write_text(json.dumps(invalid))
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()) as errors:
            self.assertEqual(main(['--result', str(result), '--evidence-root', str(self.directory)]), 1)
        self.assertIn('missing.json', errors.getvalue())
        result.write_text(json.dumps(self.review))
        with redirect_stdout(StringIO()) as output:
            self.assertEqual(main(['--result', str(result), '--evidence-root', str(self.directory)]), 0)
        self.assertTrue(json.loads(output.getvalue())['valid'])

    def test_valid_original_source_report_does_not_authorize_retirement(self):
        from generator_pool_repair import eligible, generated_proof
        report = self.inventory_report()
        question = {':db/id': 17592186524997,
                    ':question/id': report['affected_questions'][0]['question_id'],
                    ':question/math-academy-id': 'q-107463'}
        (self.directory / 'stored-original.json').write_text(json.dumps(question))
        (self.directory / 'affected-inventory.json').write_text(json.dumps(report))
        validate_review(self.review, self.directory)
        self.assertEqual(eligible(question), (False, 'original_source'))
        self.assertFalse(generated_proof(report['affected_questions'][0], self.directory))



class PedagogicalControlTests(unittest.TestCase):
    """Verify that controls isolate instructional failures, not wrong arithmetic."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        builder = load(ROOT / "generate/pipeline/fixtures/build.py", "review_control_builder")
        builder.build(self.directory)
        self.packages = {name: load(self.directory / name / "generator.py", "control_" + name)
                         for name in ("a", "b", "c")}

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def read_display(record):
        question = record["question"]
        prompt = question[":question/problem"]
        raw = re.search(r"\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}", prompt).group(1)
        matrix = [[int(cell) for cell in row.split("&")] for row in raw.split(r"\\")]
        targets = re.findall(r"a_\{([12])([12])\}", prompt)
        answer = int(question[":question/answer-fields"][0][":answer-field/choices"][0][":answer/value"])
        return matrix, targets, answer

    def test_all_controls_replay_every_source_and_have_correct_answers(self):
        cases = json.loads((self.directory / "source/source-cases.json").read_text())
        for name, module in self.packages.items():
            for case in cases:
                with self.subTest(package=name, source=case["id"]):
                    matrix, targets, answer = self.read_display(module.generate(parameters=case["parameters"]))
                    self.assertEqual(len(targets), 1)
                    row, column = map(int, targets[0])
                    self.assertEqual(answer, matrix[row - 1][column - 1])
                    self.assertEqual(str(answer), case["answer"])
            for seed in range(64):
                matrix, targets, answer = self.read_display(module.generate(seed))
                expected = sum(matrix[int(row) - 1][int(column) - 1] for row, column in targets)
                self.assertEqual(answer, expected)

    def test_rendered_targets_expose_restriction_and_drift_despite_unique_text(self):
        observations = {}
        for name, module in self.packages.items():
            records = [module.generate(seed) for seed in range(64)]
            self.assertGreaterEqual(len({record["question"][":question/problem"] for record in records}), 60)
            observations[name] = [self.read_display(record)[1] for record in records]
        self.assertEqual({targets[0] for targets in observations["a"]}, {("1", "1"), ("1", "2"), ("2", "1"), ("2", "2")})
        self.assertEqual({tuple(targets) for targets in observations["b"]}, {(("1", "1"),)})
        self.assertTrue(all(targets == [("1", "1"), ("2", "2")] for targets in observations["c"]))

    def test_preview_preserves_raw_pull_fields_correct_answers_and_feedback(self):
        renderer = load(ROOT / "generate/pipeline/render_preview.py", "review_renderer")
        record = self.packages["a"].generate(17)
        field = record["question"][":question/answer-fields"][0]
        answer = field[":answer-field/choices"][0]
        answer[":answer/feedback"] = "Read the row first, then its column."
        normalized = renderer.preview(record, 0)
        field[":answer-field/type"] = {":db/ident": field[":answer-field/type"]}
        answer[":answer/type"] = {":db/ident": answer[":answer/type"]}
        field[":answer-field/correct"] = dict(answer)
        self.assertEqual(renderer.preview(record, 0), normalized)
        rendered_field = normalized["steps"][0]["fields"][0]
        self.assertEqual(rendered_field["correctAnswer"]["feedback"], answer[":answer/feedback"])
        self.assertEqual(rendered_field["response"]["value"], answer[":answer/value"])


if __name__ == "__main__":
    unittest.main()
