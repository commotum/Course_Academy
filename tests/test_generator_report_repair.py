import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generator_pipeline import CodexSession
from generator_report_repair import evidence_only_review, generator_repair_findings, pending_report_repair
from generator_review import CHECKS, validate_review


def finding(kind):
    return {"kind": kind, "description": "A reproducible defect.", "reproduction": "Run retained-check.py.",
            "requested_change": "Repair the demonstrated defect.", "source_refs": ["source-q1"]}


class ReportRepairRoutingTests(unittest.TestCase):
    def setUp(self):
        self.binding = {"policy_version": 2, "package_hash": "package", "batch_hash": "batch",
                        "source_hash": "source", "inventory_hash": "inventory", "assets": {},
                        "effective_difficulty": "easy", "engine_hash": "engine"}
        self.result = {"verdict": "revise", "findings": [finding("evidence")]}
        self.event = {"attempt": 1, "package_hash": "package", "reason": self.result,
                      "review_directory": "/job/review-1"}
        self.history = {"findings": [{"id": "report", "finding": finding("evidence")}],
                        "events": [self.event]}
        self.state = {**self.binding,
                      "previous_review": {"directory": "/job/review-1", "binding": dict(self.binding)}}

    def test_only_evidence_findings_route_to_independent_report_repair(self):
        for verdict in ("revise", "unsupported"):
            self.assertTrue(evidence_only_review({"verdict": verdict, "findings": [finding("evidence")]}))
        for result in (None, {}, {"verdict": "accepted", "findings": [finding("evidence")]},
                       {"verdict": "revise", "findings": []},
                       {"verdict": "revise", "findings": [finding("evidence"), finding("math")]},
                       {"verdict": "revise", "findings": [finding("inventory")]},
                       {"verdict": "revise", "findings": [None]}):
            with self.subTest(result=result):
                self.assertFalse(evidence_only_review(result))

    def test_misrouted_report_can_recover_after_repeated_author_limitations(self):
        self.history["events"].extend({"attempt": index, "reason": {"code": "author_reported_limitation"}}
                                      for index in range(2, 20))
        pending = pending_report_repair(self.state, self.history, self.binding)
        self.assertEqual(pending["directory"], "/job/review-1")
        self.assertEqual(pending["reason"], self.result)
        self.assertEqual(pending_report_repair(self.state, self.history), pending)
        self.assertEqual(pending["reason"]["verdict"], "revise")

    def test_later_generator_failure_prevents_recovery_of_old_report_issue(self):
        self.history["events"].append({**self.event, "reason": {"verdict": "revise", "findings": [finding("math")]}})
        self.assertIsNone(pending_report_repair(self.state, self.history, self.binding))

    def test_report_recovery_requires_all_review_bindings_to_match(self):
        for key in self.binding:
            changed = copy.deepcopy(self.binding)
            changed[key] = {"image.png": "different"} if key == "assets" else "different"
            with self.subTest(key=key):
                self.assertIsNone(pending_report_repair(self.state, self.history, changed))
        self.event["package_hash"] = "different"
        self.assertIsNone(pending_report_repair(self.state, self.history, self.binding))
        self.event["package_hash"] = "package"
        self.event["review_directory"] = "/job/another-review"
        self.assertIsNone(pending_report_repair(self.state, self.history, self.binding))

    def test_generator_regressions_preserve_real_defects_and_retain_runner_history(self):
        self.history["findings"] += [{"id": "math", "finding": finding("math")},
                                     {"id": "pool", "finding": finding("inventory")}]
        before = copy.deepcopy(self.history)
        self.assertEqual([row["id"] for row in generator_repair_findings(self.history)], ["math"])
        self.assertEqual(self.history, before)

    def test_inventory_finding_is_valid_but_cannot_approve_unrepaired_pool(self):
        result = {"verdict": "revise", "summary": "Historical records require a pool repair.",
                  "source_analysis": {"skill": "Read matrix entries", "reasoning_steps": [], "invariants": [],
                                      "permitted_variations": [], "source_refs": [], "evidence_paths": []},
                  "checks": {name: {"status": "failed", "details": "Unresolved retained record defect.",
                                    "evidence_paths": []} for name in CHECKS},
                  "findings": [finding("inventory")]}
        with tempfile.TemporaryDirectory() as directory:
            validate_review(result, directory)
            result["verdict"] = "accepted"
            with self.assertRaises(ValueError):
                validate_review(result, directory)


class ReportRepairSandboxTests(unittest.TestCase):
    def test_nested_correction_can_write_its_actual_evidence_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            evidence = Path(temporary) / "review"
            directory = evidence / "contract-repair"
            directory.mkdir(parents=True)
            expected = {"verdict": "revise", "findings": [finding("evidence")]}
            process = Mock(returncode=0)
            process.communicate.side_effect = lambda *a, **k: (directory / "result.json").write_text(json.dumps(expected))
            with patch("generator_pipeline.subprocess.Popen", return_value=process) as start:
                result = CodexSession(root=ROOT)("review", {"workspace": str(Path(temporary) / "workspace"),
                    "evidence_root": str(evidence)}, directory)
            command = start.call_args.args[0]
            working = Path(command[command.index("-C") + 1]).resolve()
            extra_roots = [Path(command[index + 1]).resolve()
                           for index, value in enumerate(command[:-1]) if value == "--add-dir"]
            self.assertTrue(any(evidence.resolve().is_relative_to(root) for root in [working, *extra_roots]))
            self.assertEqual(result, expected)
            self.assertEqual(Path(command[command.index("--output-last-message") + 1]), directory / "result.json")


if __name__ == "__main__":
    unittest.main()
