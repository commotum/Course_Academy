"""Exercise handoffs with real Python packages; agent and database boundaries are fake."""
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import textwrap
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generator_packages import publish_package, resolve_registered_script
from generator_pipeline import Pipeline, main
from generator_review import CHECKS


GENERATOR = textwrap.dedent('''\
    import argparse, json, os, random, uuid
    from pathlib import Path
    from helper import square

    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty')
    parser.add_argument('--count', type=int)
    parser.add_argument('--seed', type=int)
    parser.add_argument('--format')
    args = parser.parse_args()
    config = json.loads(Path(__file__).with_name('config.json').read_text())
    output = Path(os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'])
    if output.resolve().is_relative_to(Path(__file__).resolve().parent):
        raise ValueError('Generated assets must be outside the runtime package')
    records = []
    for n in random.Random(args.seed).sample(range(2, 99), args.count):
        aid = str(uuid.uuid5(uuid.NAMESPACE_URL, 'answer:' + str(n)))
        prompt = 'Calculate ' + str(n) + ' squared.'
        if config['image']:
            output.mkdir(parents=True, exist_ok=True)
            image = output / ('question-' + str(n) + '.svg')
            image.write_text('<svg xmlns="http://www.w3.org/2000/svg"><text>' + str(n) + '</text></svg>')
            prompt += ' ![number](' + str(image) + ')'
        records.append({'knowledge_point': 123, 'question': {
            ':question/id': str(uuid.uuid5(uuid.NAMESPACE_URL, prompt)),
            ':question/problem': prompt,
            ':question/worked-solution': str(n) + ' times itself is ' + str(square(n)) + '.',
            ':question/difficulty': ':question.difficulty/' + (config['difficulty'] or args.difficulty),
            ':question/answer-fields': [{
                ':answer-field/id': str(uuid.uuid5(uuid.NAMESPACE_URL, 'field:' + str(n))),
                ':answer-field/key': 'answer', ':answer-field/type': ':answer-field.type/blank',
                ':answer-field/correct': [':answer/id', aid],
                ':answer-field/choices': [{':answer/id': aid, ':answer/type': ':answer.type/math',
                                          ':answer/value': str(square(n))}]
            }]
        }})
    print(json.dumps(records, sort_keys=True))
''')


def write_package(directory, *, image=False, difficulty=None, declare_helper=True, default_difficulty=None):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "generator.py").write_text(GENERATOR)
    (directory / "generator.py").chmod(0o755)
    (directory / "helper.py").write_text("def square(n): return n * n\n")
    (directory / "config.json").write_text(json.dumps({"image": image, "difficulty": difficulty}))
    (directory / "scratch-only.txt").write_text("This file is not a runtime dependency.\n")
    files = ["generator.py", "config.json"] + (["helper.py"] if declare_helper else [])
    manifest = {"entrypoint": "generator.py", "files": files,
                "dependencies": {"python": platform.python_version(), "packages": {}}}
    if default_difficulty is not None:
        manifest["default_difficulty"] = default_difficulty
    (directory / "package.json").write_text(json.dumps(manifest))
    return manifest


class FakeSession:
    """Structured agent fixtures test admission, not pedagogical judgement."""
    def __init__(self, *, reject=False, interrupt_author=False, image=False,
                 difficulty=None, declare_helper=True, default_difficulty=None):
        self.calls = []
        self.reject, self.interrupt_author = reject, interrupt_author
        self.image, self.difficulty, self.declare_helper = image, difficulty, declare_helper
        self.default_difficulty = default_difficulty

    def __call__(self, role, context, directory):
        self.calls.append((role, str(directory)))
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        if role == "author":
            if self.interrupt_author:
                self.interrupt_author = False
                raise subprocess.TimeoutExpired(["fake-codex", "exec"], 1)
            write_package(Path(context["workspace"]), image=self.image, difficulty=self.difficulty,
                          declare_helper=self.declare_helper, default_difficulty=self.default_difficulty)
            return {"status": "ready", "manifest": "package.json"}
        analysis = {"skill": "Square a positive integer", "reasoning_steps": ["Multiply n by itself"],
                    "invariants": ["One squaring operation"], "permitted_variations": ["Positive integer n"],
                    "source_refs": ["fixture-source-1"], "evidence_paths": ["source-analysis.json"]}
        (directory / "source-analysis.json").write_text(json.dumps(analysis))
        (directory / "checks.json").write_text(json.dumps({"fixture": True, "checks": list(CHECKS)}))
        checks = {name: {"status": "passed", "details": "Structured boundary fixture.",
                         "evidence_paths": ["checks.json"]} for name in CHECKS}
        findings = []
        if self.reject:
            kind = "restriction" if len([r for r, _ in self.calls if r == "review"]) % 2 else "drift"
            check = "variety" if kind == "restriction" else "scope"
            checks[check]["status"] = "failed"
            findings = [{"kind": kind, "description": "Fixture counterexample requires repair.",
                         "source_refs": ["fixture-source-1"], "reproduction": "seed=17; compare source operation",
                         "requested_change": "Restore the source-supported sampling domain."}]
        return {"verdict": "revise" if self.reject else "accepted", "summary": "Structured review fixture.",
                "source_analysis": analysis, "checks": checks, "findings": findings}


class FakePublisher:
    """Durable fake commit acknowledgement separates pipeline recovery from EDB tests."""
    def __init__(self, root, *, lose_ack=False, available_difficulties=None):
        self.root, self.lose_ack = Path(root), lose_ack
        self.prepares, self.publishes = 0, 0
        self.available_difficulties = ["moderate"] if available_difficulties is None else available_difficulties

    def extract_source(self, kp, directory):
        value = {"database": "fixture", "lineage": "fixture-lineage", "basis": 1, "kp_id": kp,
                 "source_sha256": "source-v1", "material": {"question": "Square 7."},
                 "available_difficulties": self.available_difficulties}
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "source.json").write_text(json.dumps(value))
        return value

    def prepare(self, kp, records, reference, package_hash, directory, **kwargs):
        self.prepares += 1
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        value = {"request_key": "fixture-request", "records": records, "generator": reference,
                 "package_sha256": package_hash}
        (directory / "request.json").write_text(json.dumps(value))
        return value

    def publish(self, directory):
        self.publishes += 1
        request = json.loads((Path(directory) / "request.json").read_text())
        store = self.root / "committed.json"
        if store.exists():
            receipt = json.loads(store.read_text())
            if receipt["request_key"] != request["request_key"]:
                raise AssertionError("Pipeline replaced an unresolved request")
        else:
            receipt = {"passed": True, "request_key": request["request_key"],
                       "new_questions": len(request["records"]), "writes": 1}
            store.write_text(json.dumps(receipt))
        if self.lose_ack:
            self.lose_ack = False
            raise ConnectionError("Commit completed, response lost")
        return receipt


class GeneratorPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.math = self.root / "math"
        self.job = self.root / "job"
        self.request = {"kp": 123, "difficulty": "easy", "count": 3, "existing_entrypoint": None}
        self.environment = {**os.environ, "EDB_MATH_ROOT": str(self.math),
                            "COURSE_ACADEMY_GENERATOR_PYTHON": sys.executable}
        self.publisher = FakePublisher(self.root)

    def tearDown(self):
        for directory in self.root.rglob("*"):
            if directory.is_dir() and not directory.is_symlink():
                directory.chmod(0o755)
        self.temp.cleanup()

    def pipeline(self, session, *, publisher=None, attempts=2, request=None):
        return Pipeline(self.job, request or self.request, publisher or self.publisher,
                        root=self.root, environment=self.environment, session=session, max_attempts=attempts)

    def test_interrupted_author_resumes_same_attempt_and_uses_declared_files_only(self):
        session = FakeSession(interrupt_author=True)
        with self.assertRaises(subprocess.TimeoutExpired):
            self.pipeline(session).run()
        result = self.pipeline(session).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual(result["attempt"], 1)
        authors = [directory for role, directory in session.calls if role == "author"]
        self.assertEqual(authors, [str(self.job / "author-1")] * 2)
        script = resolve_registered_script(result["registration"], self.root, self.math)
        self.assertTrue(script.with_name("helper.py").is_file())
        self.assertFalse(script.with_name("scratch-only.txt").exists())
        self.assertFalse((Path(result["runtime"]) / "scratch-only.txt").exists())
        self.assertEqual(self.publisher.prepares, 1)

    def test_both_negative_review_kinds_stop_at_attempt_limit_without_publication(self):
        session = FakeSession(reject=True)
        result = self.pipeline(session).run()
        self.assertEqual(result["stage"], "failed")
        self.assertEqual([r for r, _ in session.calls], ["author", "review", "author", "review"])
        kinds = [json.loads((self.job / f"review-{n}/result.json").read_text())["findings"][0]["kind"] for n in (1, 2)]
        self.assertEqual(kinds, ["restriction", "drift"])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))
        self.assertFalse((self.math / "generators").exists())

    def test_unknown_commit_response_resumes_exact_request_without_agents_or_reprepare(self):
        session = FakeSession()
        first_publisher = FakePublisher(self.root, lose_ack=True)
        with self.assertRaises(ConnectionError):
            self.pipeline(session, publisher=first_publisher).run()
        request_path = self.job / "publication/request.json"
        approved_request = request_path.read_bytes()
        calls_before = list(session.calls)
        restarted_publisher = FakePublisher(self.root)
        result = self.pipeline(session, publisher=restarted_publisher).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual(session.calls, calls_before)
        self.assertEqual(request_path.read_bytes(), approved_request)
        self.assertEqual(restarted_publisher.prepares, 0)
        self.assertEqual(result["publication"]["writes"], 1)

    def test_changed_approved_code_or_image_cannot_reach_preparation(self):
        for target in ("code", "image"):
            with self.subTest(target=target):
                self.job = self.root / ("mutation-" + target)
                publisher = FakePublisher(self.root / target)
                session = FakeSession(image=True)
                state = self.pipeline(session, publisher=publisher).run("validate")
                self.assertEqual(state["stage"], "prepare")
                if target == "code":
                    path = self.job / "workspace/helper.py"
                else:
                    path = Path(next(iter(state["assets"])))
                path.write_text(path.read_text() + "\nchanged after approval\n")
                with self.assertRaisesRegex(ValueError, "Reviewed (package|image)"):
                    self.pipeline(session, publisher=publisher).run()
                self.assertEqual((publisher.prepares, publisher.publishes), (0, 0))

    def test_wrong_band_and_undeclared_runtime_import_are_rejected_before_review(self):
        for options in ({"difficulty": "hard"}, {"declare_helper": False}):
            with self.subTest(options=options):
                self.job = self.root / ("wrong-band" if "difficulty" in options else "missing-helper")
                session = FakeSession(**options)
                result = self.pipeline(session, attempts=1).run()
                self.assertEqual(result["stage"], "failed")
                self.assertEqual([role for role, _ in session.calls], ["author"])
                self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))

    def test_registered_package_is_reused_without_authoring_and_keeps_its_hash(self):
        original = self.root / "original"
        manifest = write_package(original)
        package = publish_package(original, manifest["entrypoint"], manifest["files"], self.math,
                                  dependencies=manifest["dependencies"])
        request = {**self.request, "difficulty": "unclassified", "count": 5,
                   "existing_entrypoint": str(package.script), "registered_package": package.reference}
        session = FakeSession()
        result = self.pipeline(session, request=request).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual([role for role, _ in session.calls], ["review"])
        self.assertEqual(result["package_hash"], package.digest)
        self.assertEqual(result["registration"], package.reference)
        self.assertEqual(result["effective_difficulty"], "moderate")
        samples = json.loads((self.job / "samples.json").read_text())
        self.assertEqual(len(samples), 5)
        self.assertEqual({q["question"][":question/difficulty"] for q in samples}, {":question.difficulty/moderate"})

    def test_unclassified_request_requires_declared_default_then_generates_that_band(self):
        request = {**self.request, "difficulty": "unclassified", "count": 5}
        missing = FakeSession()
        result = self.pipeline(missing, request=request, attempts=1).run()
        self.assertEqual(result["stage"], "failed")
        self.assertIn("default_difficulty", result["error"]["error"])
        self.assertEqual([role for role, _ in missing.calls], ["author"])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))
        self.job = self.root / "classified-job"
        result = self.pipeline(FakeSession(default_difficulty="moderate"), request=request).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual(result["effective_difficulty"], "moderate")
        samples = json.loads((self.job / "samples.json").read_text())
        self.assertEqual(len(samples), 5)
        self.assertEqual({q["question"][":question/difficulty"] for q in samples}, {":question.difficulty/moderate"})

    def test_inventory_classification_missing_zero_requests_five_samples(self):
        inventory = self.root / "inventory.json"
        inventory.write_text(json.dumps({"cycle": 1, "request": {
            "knowledgePoint": 123, "difficulty": "unclassified", "missing": 0,
            "stage": "classify", "script": None}}))
        with patch("generator_publish.Publisher.from_environment", return_value=self.publisher), \
                patch("serve_graph_explorer.database_environment", return_value=self.environment), \
                patch("generator_pipeline.existing_generator", return_value=None), \
                patch("generator_pipeline.Pipeline") as pipeline, patch("builtins.print"):
            pipeline.return_value.run.return_value = {"stage": "verified"}
            self.assertEqual(main(["--inventory-job", str(inventory)]), 0)
        admitted = pipeline.call_args.args[1]
        self.assertEqual(admitted["difficulty"], "unclassified")
        self.assertEqual(admitted["count"], 5)


if __name__ == "__main__":
    unittest.main()
