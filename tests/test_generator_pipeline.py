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
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generator_packages import publish_package, resolve_registered_script
from generator_pipeline import CodexSession, Pipeline, SessionRetryExhausted, main
from generator_publish import SourceChanged, digest as source_digest
from generator_review import CHECKS, REVIEW_POLICY_VERSION
from generator_review_fixtures import write_decision_evidence


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
            workspace = Path(context['workspace'])
            if self.reject:
                config = workspace / 'config.json'
                value = json.loads(config.read_text())
                value['revision'] = len([r for r, _ in self.calls if r == 'author'])
                config.write_text(json.dumps(value))
            history = Path(context['repair_history_file'])
            if history.exists():
                (workspace / 'repair_check.py').write_text('from helper import square\nassert square(7) == 49\n')
                (workspace / 'repair-regressions.json').write_text(json.dumps({'findings': [
                    {'id': row['id'], 'script': 'repair_check.py'}
                    for row in json.loads(history.read_text())['findings']]}))
            return {"status": "ready", "manifest": "package.json"}
        analysis = {"skill": "Square a positive integer", "reasoning_steps": ["Multiply n by itself"],
                    "invariants": ["One squaring operation"], "permitted_variations": ["Positive integer n"],
                    "source_refs": ["fixture-source-1"], "evidence_paths": ["source-analysis.json"]}
        (directory / "source-analysis.json").write_text(json.dumps(analysis))
        (directory / "checks.json").write_text(json.dumps({"fixture": True, "checks": list(CHECKS)}))
        checks = {name: {"status": "passed", "details": "Structured boundary fixture.",
                         "evidence_paths": ["checks.json"]} for name in CHECKS}
        checks["decision_variation"]["evidence_paths"] = [write_decision_evidence(directory)]
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
        self.root.mkdir(parents=True, exist_ok=True)
        self.prepares, self.publishes = 0, 0
        self.available_difficulties = ["moderate"] if available_difficulties is None else available_difficulties
        self.registered_generator = None
        self.material = {"question": "Square 7."}
        self.prepare_options = None
        self.inventory_extractions = 0

    def extract_inventory(self, kp, directory):
        self.inventory_extractions += 1
        value = {"database": "fixture", "lineage": "fixture-lineage", "basis": 1,
                 "kp_id": kp, "questions": [], "canonical_example": None,
                 "fingerprints": [source_digest(self.material)]}
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "inventory.json").write_text(json.dumps(value))
        return value

    def extract_source(self, kp, directory):
        value = {"database": "fixture", "lineage": "fixture-lineage", "basis": 1, "kp_id": kp,
                 "source_sha256": source_digest(self.material), "material": self.material,
                 "registered_generator": self.registered_generator,
                 "available_difficulties": self.available_difficulties}
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "source.json").write_text(json.dumps(value))
        self.extract_inventory(kp, directory)
        return value

    def prepare(self, kp, records, reference, package_hash, directory, **kwargs):
        self.prepares += 1
        self.prepare_options = kwargs
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

    def approve_for_refill(self, **options):
        result = self.pipeline(FakeSession(**options)).run()
        self.publisher = FakePublisher(self.root / "refill-store")
        self.publisher.registered_generator = {":question-generator/script": result["registration"]}
        self.job = self.root / "refill-job"
        return {**self.request, "job_kind": "refill", "registered_package": result["registration"]}, result

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

    def test_negative_reviews_exhaust_durable_budget_and_explicit_resume_preserves_feedback(self):
        session = FakeSession(reject=True)
        result = self.pipeline(session).run()
        self.assertEqual(result["stage"], "blocked")
        self.assertEqual(result['error']['code'], 'author_attempts_exhausted')
        self.assertEqual([r for r, _ in session.calls], ["author", "review", "author", "review"])
        kinds = [json.loads((Path(directory) / "result.json").read_text())["findings"][0]["kind"]
                 for role, directory in session.calls if role == "review"]
        self.assertEqual(kinds, ["restriction", "drift"])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))
        self.assertFalse((self.math / "generators").exists())
        history = json.loads((self.job / 'repair-history.json').read_text())
        self.assertEqual([r['finding']['kind'] for r in history['findings']], ['restriction', 'drift'])
        self.assertEqual(self.pipeline(session).context(self.job / 'next')['repair_mode'], 'root_cause')
        # Restarting (even with a larger default budget) cannot grant sessions.
        untouched = FakeSession()
        self.assertEqual(self.pipeline(untouched, attempts=100).run()['stage'], 'blocked')
        self.assertEqual(untouched.calls, [])
        # A deliberate recovery preserves counterexamples and requires a new
        # independent acceptance before publishing the repaired candidate.
        result = self.pipeline(FakeSession()).run(resume_reason='Repair both retained generator defects')
        self.assertEqual(result['stage'], 'verified')
        self.assertFalse(result['needs_repair'])
        preflight = json.loads((self.job / 'repair-preflight.json').read_text())
        self.assertEqual(set(preflight['finding_ids']), {r['id'] for r in history['findings']})
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_reviewer_repairs_its_own_report_without_reauthoring_or_resampling(self):
        class ReportSession(FakeSession):
            def __call__(self, role, context, directory):
                result = super().__call__(role, context, context['evidence_root'] if role == 'review' else directory)
                if role == 'review' and not context.get('review_contract_feedback'):
                    result['checks']['math']['evidence_paths'] = ['not-written.json']
                return result
        session = ReportSession()
        pipeline = self.pipeline(session)
        with patch.object(pipeline, 'sample', wraps=pipeline.sample) as sample:
            result = pipeline.run()
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual([role for role, _ in session.calls], ['author', 'review', 'review'])
        self.assertEqual((result['attempt'], sample.call_count), (1, 1))
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_invalid_report_exhausts_durable_corrections_then_explicitly_resumes(self):
        class BrokenReport(FakeSession):
            def __call__(self, role, context, directory):
                result = super().__call__(role, context, context['evidence_root'] if role == 'review' else directory)
                if role == 'review':
                    result['checks']['math']['evidence_paths'] = ['not-written.json']
                return result
        session = BrokenReport()
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual(result['error']['code'], 'review_report_correction_exhausted')
        self.assertEqual([role for role, _ in session.calls], ['author', 'review', 'review', 'review'])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))
        self.assertTrue((self.job / 'workspace/generator.py').exists())
        cached_samples = (self.job / 'samples.json').read_bytes()
        repaired = FakeSession()
        self.assertEqual(self.pipeline(repaired).run()['stage'], 'blocked')
        self.assertEqual(repaired.calls, [])
        result = self.pipeline(repaired).run(resume_reason='Repaired reviewer report fixture')
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual([role for role, _ in repaired.calls], ['review'])
        self.assertEqual((self.job / 'samples.json').read_bytes(), cached_samples)
        self.assertEqual(result['attempt'], 1)

    def test_a_reviewed_math_flaw_is_fixed_checked_and_published_within_budget(self):
        class RepairMath(FakeSession):
            def __call__(self, role, context, directory):
                first_author = role == 'author' and not self.calls
                self.reject = role == 'review' and not any(r == 'review' for r, _ in self.calls)
                result = super().__call__(role, context, directory)
                if first_author:
                    (Path(context['workspace']) / 'helper.py').write_text('def square(n): return n + n\n')
                if role == 'review' and self.reject:
                    result['checks']['variety']['status'] = 'passed'
                    result['checks']['math']['status'] = 'failed'
                    result['findings'][0].update(kind='math', description='Squaring doubles instead of multiplying.',
                                                reproduction='square(7) returned 14 instead of 49',
                                                requested_change='Use n * n and retain the square(7) counterexample.')
                return result
        session = RepairMath()
        result = self.pipeline(session, attempts=2).run()
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual(result['attempt'], 2)
        self.assertEqual([role for role, _ in session.calls], ['author', 'review', 'author', 'review'])
        script = resolve_registered_script(result['registration'], self.root, self.math)
        self.assertEqual(script.with_name('helper.py').read_text(), 'def square(n): return n * n\n')
        self.assertTrue(json.loads((self.job / 'repair-preflight.json').read_text())['passed'])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_review_evidence_reuse_requires_same_source_and_policy(self):
        pipeline = self.pipeline(FakeSession(reject=True))
        pipeline.run()
        context = pipeline.context(self.job / 'author-next')
        self.assertIsNotNone(context['previous_review'])
        pipeline.state['source_hash'] = 'changed-source'
        self.assertIsNone(pipeline.context(self.job / 'author-next')['previous_review'])
        pipeline.state['source_hash'] = context['previous_review']['binding']['source_hash']
        with patch('generator_pipeline.REVIEW_POLICY_VERSION', REVIEW_POLICY_VERSION + 1):
            self.assertIsNone(pipeline.context(self.job / 'author-next')['previous_review'])

    def test_failed_regression_stops_before_another_independent_review(self):
        class FailingCheck(FakeSession):
            def __call__(self, role, context, directory):
                result = super().__call__(role, context, directory)
                script = Path(context['workspace']) / 'repair_check.py'
                if role == 'author' and script.exists():
                    script.write_text('raise AssertionError("retained counterexample persists")\n')
                return result
        session = FailingCheck(reject=True)
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual([role for role, _ in session.calls], ['author', 'review', 'author'])
        self.assertIn('Retained repair regression failed', result['error']['cause']['error'])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))

    def test_unchanged_rejected_candidate_does_not_spend_another_review(self):
        class Unchanged(FakeSession):
            def __call__(self, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == 'author':
                    config = Path(context['workspace']) / 'config.json'
                    value = json.loads(config.read_text());value.pop('revision', None)
                    config.write_text(json.dumps(value))
                return result
        session = Unchanged(reject=True)
        result = self.pipeline(session, attempts=9).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual(result['error']['code'], 'no_progress')
        self.assertTrue(result['repeated_candidate'])
        self.assertEqual([role for role, _ in session.calls], ['author', 'review', 'author'])
        self.assertEqual(self.publisher.prepares, 0)

    def test_sample_checkpoint_resumes_without_reauthoring(self):
        session = FakeSession()
        pipeline = self.pipeline(session)
        pipeline.run('generate')
        pipeline.persist(stage='sample')
        before = list(session.calls)
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual([role for role, _ in session.calls[len(before):]], ['review'])

    def test_identical_failed_candidates_block_before_spending_full_attempt_budget(self):
        session = FakeSession(difficulty='hard')
        state = self.pipeline(session, attempts=9).run()
        self.assertEqual(state['stage'], 'blocked')
        self.assertEqual(state['error']['code'], 'no_progress')
        self.assertEqual([role for role, _ in session.calls], ['author', 'author'])
        self.assertIn('wrong difficulty band', state['error']['cause']['error'])
        for _ in range(3):
            self.assertEqual(self.pipeline(session, attempts=99).run()['stage'], 'blocked')
        self.assertEqual(len(session.calls), 2)
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))

    def test_legacy_runaway_attempts_do_not_receive_a_new_budget_on_restart(self):
        pipeline = self.pipeline(FakeSession())
        pipeline.run('generate')
        pipeline.state.pop('author_attempt_limit')
        pipeline.persist(stage='generate', attempt=1001, author_running=False)
        session = FakeSession()
        state = self.pipeline(session).run()
        self.assertEqual(state['stage'], 'blocked')
        self.assertEqual(state['error']['code'], 'author_attempts_exhausted')
        self.assertEqual(state['attempt'], 1001)
        self.assertEqual(state['author_attempt_limit'], 2)
        self.assertEqual(session.calls, [])

    def test_a_changed_artifact_does_not_silently_rearm_a_blocked_job(self):
        pipeline = self.pipeline(FakeSession(difficulty='hard'), attempts=1)
        pipeline.run()
        (self.job / 'workspace/helper.py').write_text('def square(n): return n ** 2\n')
        session = FakeSession()
        state = self.pipeline(session).run()
        self.assertEqual(state['stage'], 'blocked')
        self.assertEqual(session.calls, [])
        state = self.pipeline(session).run(resume_reason='Correct difficulty after diagnosing the failed sample')
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual(state['attempt'], 2)
        self.assertEqual(len(state['resume_events']), 1)
        self.assertEqual(state['resume_events'][0]['prior_error']['code'], 'author_attempts_exhausted')

    def test_explicit_session_recovery_preserves_total_launch_count(self):
        session = CodexSession(root=Path(__file__).resolve().parents[1])
        pipeline = self.pipeline(session)
        directory = self.job / 'author-1'
        directory.mkdir()
        execution = directory / 'execution.json'
        execution.write_text(json.dumps({'launches': 3, 'status': 'failed', 'error': 'transport failure'}))
        pipeline.persist(attempt=1, author_running=True)
        pipeline.block('agent_session_retry_exhausted', {
            'code': 'agent_session_retry_exhausted', 'session_directory': str(directory)}, 'generate')
        with patch.object(pipeline, '_run', return_value=None):
            pipeline.run(resume_reason='Transport service recovered')
        saved = json.loads(execution.read_text())
        self.assertEqual((saved['launches'], saved['launch_limit']), (3, 6))
        self.assertEqual(pipeline.state['attempt'], 1)
        self.assertEqual(pipeline.state['stage'], 'generate')

    def test_unsupported_author_blocks_once_without_repeated_sessions(self):
        session = Mock(return_value={'status': 'unsupported', 'reason': 'Required repair is outside the author workspace'})
        state = self.pipeline(session, attempts=9).run()
        self.assertEqual(state['stage'], 'blocked')
        self.assertEqual(state['error']['code'], 'author_reported_limitation')
        for _ in range(3):
            self.assertEqual(self.pipeline(session).run()['stage'], 'blocked')
        self.assertEqual(session.call_count, 1)

    def test_review_budget_counts_new_directories_once_across_restarts(self):
        first = self.pipeline(FakeSession(), attempts=1)
        directory = self.job / 'review-first'
        self.assertTrue(first.admit_review_session(directory))
        self.assertTrue(first.admit_review_session(directory))
        restarted = self.pipeline(FakeSession(), attempts=20)
        self.assertTrue(restarted.admit_review_session(directory))
        self.assertEqual(len(restarted.state['review_sessions']), 1)
        self.assertEqual(restarted.state['review_session_limit'], 3)
        self.assertTrue(restarted.admit_review_session(self.job / 'review-second'))
        self.assertTrue(restarted.admit_review_session(self.job / 'review-third'))
        self.assertFalse(restarted.admit_review_session(self.job / 'review-fourth'))
        self.assertEqual(restarted.state['stage'], 'blocked')
        self.assertEqual(restarted.state['error']['code'], 'review_sessions_exhausted')
        self.assertEqual(len(restarted.state['review_sessions']), 3)

    def test_engine_refresh_reviews_share_a_durable_budget_until_explicit_resume(self):
        session = FakeSession()
        state = self.pipeline(session, attempts=1).run()
        self.assertEqual(state['stage'], 'verified')
        engine = self.root / 'engine/rust'
        engine.mkdir(parents=True)
        for revision in range(3):
            (engine / 'grading.rs').write_text(f'// engine revision {revision}\n')
            state = self.pipeline(session, attempts=1).run()
        self.assertEqual(state['stage'], 'blocked')
        self.assertEqual(state['error']['code'], 'review_sessions_exhausted')
        self.assertEqual([role for role, _ in session.calls], ['author', 'review', 'review', 'review'])
        self.assertEqual(state['review_session_limit'], 3)
        for _ in range(2):
            self.assertEqual(self.pipeline(session, attempts=99).run()['stage'], 'blocked')
        self.assertEqual(len(session.calls), 4)
        state = self.pipeline(session, attempts=1).run(resume_reason='Engine updates have stabilized; review current engine')
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual(state['review_session_limit'], 6)
        self.assertEqual(len(state['review_sessions']), 4)
        self.assertEqual(state['attempt'], 1)
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_scheduler_locks_survive_the_author_reviewer_handoff(self):
        fake = FakeSession()
        class RecordingSession(CodexSession):
            def __call__(inner, role, context, directory):
                self.assertEqual(tuple(inner.lock_fds[:2]), descriptors)
                self.assertEqual(len(inner.lock_fds), 3)
                return fake(role, context, directory)
        with (self.root/'lane.lock').open('a') as lane, (self.root/'kp.lock').open('a') as kp:
            descriptors = (lane.fileno(), kp.fileno())
            self.environment['COURSE_ACADEMY_GENERATOR_LOCK_FDS'] = json.dumps(descriptors)
            result = self.pipeline(RecordingSession(root=self.root)).run()
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual([role for role, _ in fake.calls], ['author', 'review'])

    def test_engine_update_gets_a_fresh_review_without_reauthoring_or_stale_cache(self):
        first = FakeSession()
        state = self.pipeline(first).run('validate')
        old_review = state['review']
        engine = self.root / 'engine/rust'
        engine.mkdir(parents=True)
        (engine/'grading.rs').write_text('// independent fixture engine revision\n')
        second = FakeSession()
        state = self.pipeline(second).run()
        self.assertEqual(state['stage'], 'verified')
        self.assertEqual([role for role, _ in second.calls], ['review'])
        self.assertNotEqual(state['review'], old_review)
        self.assertEqual(self.publisher.publishes, 1)

    def test_old_attempt_failure_requires_explicit_resume_with_feedback_and_workspace(self):
        session = FakeSession(reject=True)
        pipeline = self.pipeline(session)
        result = pipeline.run()
        pipeline.persist(stage='failed', error=result['error'])
        original = (self.job / 'source/source.json').read_bytes()
        idle = FakeSession()
        self.assertEqual(self.pipeline(idle).run()['stage'], 'failed')
        self.assertEqual(idle.calls, [])
        result = self.pipeline(FakeSession()).run(resume_reason='Repair retained findings after inspecting failure')
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual((self.job / 'source/source.json').read_bytes(), original)
        self.assertEqual(result['attempt'], 3)
        self.assertEqual(self.publisher.publishes, 1)

    def test_changed_package_still_requires_author_repair(self):
        class ChangedPackage(FakeSession):
            def __call__(self, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == 'review' and len([r for r, _ in self.calls if r == 'review']) == 1:
                    helper = Path(context['workspace']) / 'helper.py'
                    helper.write_text(helper.read_text() + '\n# changed during review\n')
                return result
        session = ChangedPackage()
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'verified')
        self.assertEqual([role for role, _ in session.calls], ['author', 'review', 'author', 'review'])

    def test_completed_agent_result_is_reused_without_a_new_session(self):
        directory = self.root / 'cached-agent'
        directory.mkdir()
        expected = {'status': 'ready', 'manifest': 'package.json'}
        (directory / 'result.json').write_text(json.dumps(expected))
        session = CodexSession(root=Path(__file__).resolve().parents[1])
        with patch('generator_pipeline.subprocess.Popen') as start:
            self.assertEqual(session('author', {}, directory), expected)
        start.assert_not_called()

    def test_session_transport_failures_stop_across_restarts_without_author_attempt_churn(self):
        repo = Path(__file__).resolve().parents[1]
        for failure in ('exit', 'timeout'):
            with self.subTest(failure=failure):
                self.job = self.root / failure
                process = Mock(returncode=1, pid=12345)
                if failure == 'timeout':
                    process.communicate.side_effect = subprocess.TimeoutExpired(['codex'], 1)
                expected = subprocess.TimeoutExpired if failure == 'timeout' else subprocess.CalledProcessError
                with patch('generator_pipeline.subprocess.Popen', return_value=process) as start, \
                        patch('generator_pipeline.os.killpg') as kill:
                    for _ in range(2):
                        with self.assertRaises(expected):
                            self.pipeline(CodexSession(root=repo)).run()
                    result = self.pipeline(CodexSession(root=repo)).run()
                    self.assertEqual(result['stage'], 'blocked')
                    self.assertEqual(result['error']['code'], 'agent_session_retry_exhausted')
                    self.assertEqual(result['error']['resume_stage'], 'generate')
                    self.assertEqual(result['attempt'], 1)
                    self.assertEqual(result['error']['cause']['launches'], 3)
                    self.assertTrue((self.job / 'workspace').exists())
                    self.assertEqual(self.pipeline(CodexSession(root=repo)).run(), result)
                    self.assertEqual(start.call_count, 3)
                    self.assertEqual(kill.call_count, 3 if failure == 'timeout' else 0)
                self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))

    def test_session_retry_can_succeed_and_cached_result_survives_exhausted_budget(self):
        repo = Path(__file__).resolve().parents[1]
        for role in ('author', 'review'):
            with self.subTest(role=role):
                directory = self.root / role
                context = {'workspace': str(self.root), 'evidence_root': str(directory)}
                expected = {'status': 'ready', 'manifest': 'package.json'}
                failed = Mock(returncode=1)
                succeeded = Mock(returncode=0)
                succeeded.communicate.side_effect = lambda *a, **k: (directory / 'result.json').write_text(json.dumps(expected))
                with patch('generator_pipeline.subprocess.Popen', side_effect=[failed, succeeded]) as start:
                    with self.assertRaises(subprocess.CalledProcessError):
                        CodexSession(root=repo)(role, context, directory)
                    self.assertEqual(CodexSession(root=repo)(role, context, directory), expected)
                    self.assertEqual(CodexSession(root=repo, max_launches=1)(role, context, directory), expected)
                    self.assertEqual(start.call_count, 2)
                execution = json.loads((directory / 'execution.json').read_text())
                self.assertEqual(execution, {'launches': 2, 'status': 'completed'})

    def test_interrupted_session_budget_is_not_reset_by_new_process(self):
        directory = self.root / 'interrupted-review'
        directory.mkdir()
        (directory / 'execution.json').write_text(json.dumps({'launches': 3, 'status': 'running'}))
        session = CodexSession(root=Path(__file__).resolve().parents[1])
        with patch('generator_pipeline.subprocess.Popen') as start:
            with self.assertRaises(SessionRetryExhausted):
                session('review', {'workspace': str(self.root)}, directory)
        start.assert_not_called()

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
                self.assertEqual(result["stage"], "blocked")
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

    def test_unclassified_request_reuses_single_source_band_without_reauthoring(self):
        request = {**self.request, "difficulty": "unclassified", "count": 5}
        missing = FakeSession()
        result = self.pipeline(missing, request=request, attempts=1).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual(result['effective_difficulty'], 'moderate')
        self.assertEqual([role for role, _ in missing.calls], ["author", "review"])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))
        self.job = self.root / "classified-job"
        result = self.pipeline(FakeSession(default_difficulty="moderate"), request=request).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual(result["effective_difficulty"], "moderate")
        samples = json.loads((self.job / "samples.json").read_text())
        self.assertEqual(len(samples), 5)
        self.assertEqual({q["question"][":question/difficulty"] for q in samples}, {":question.difficulty/moderate"})

    def test_ambiguous_source_bands_still_require_author_classification(self):
        self.publisher.available_difficulties = ['easy', 'moderate']
        result = self.pipeline(FakeSession(), request={**self.request, 'difficulty':'unclassified'}, attempts=1).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertIn('default_difficulty', result['error']['cause']['error'])
        self.assertEqual(self.publisher.prepares, 0)

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

    def test_approved_refill_runs_without_agents_and_binds_registration_at_preparation(self):
        request, approved = self.approve_for_refill(image=True)
        session = FakeSession()
        result = self.pipeline(session, request=request).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual(session.calls, [])
        self.assertEqual(result["package_hash"], approved["package_hash"])
        self.assertEqual(result["registration"], approved["registration"])
        self.assertEqual(self.publisher.prepare_options["expected_registered_generator"], approved["registration"])
        self.assertTrue(result["assets"])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))
        approval = json.loads((self.math / "generators/approvals" / approved["package_hash"] / "123.json").read_text())
        self.assertEqual(set(approval["bands"]), {"easy"})
        self.assertEqual(approval["bands"]["easy"]["review_policy_version"], REVIEW_POLICY_VERSION)

    def downgrade_saved_review(self):
        """Emulate a job stopped under the previous review contract."""
        state = json.loads((self.job / "job.json").read_text())
        path = Path(state["review"])
        legacy = self.job / ("review-" + str(state["attempt"]))
        path.parent.rename(legacy)
        path = legacy / "result.json"
        review = json.loads(path.read_text())
        review["checks"].pop("decision_variation")
        path.write_text(json.dumps(review))
        state["review"] = str(path)
        state.pop("review_policy_version", None)
        state.pop("review_binding", None)
        (self.job / "job.json").write_text(json.dumps(state))
        return path, path.read_bytes()

    def test_legacy_band_approval_requests_review_without_running_generator(self):
        request, approved = self.approve_for_refill()
        path = self.math / "generators/approvals" / approved["package_hash"] / "123.json"
        approval = json.loads(path.read_text())
        approval["bands"]["easy"].pop("review_policy_version")
        path.write_text(json.dumps(approval))
        session = FakeSession()
        result = self.pipeline(session, request=request).run()
        self.assertEqual(result["stage"], "unsupported")
        self.assertTrue(result["needs_repair"])
        self.assertEqual(result["error"]["code"], "approval_policy_stale")
        self.assertEqual(session.calls, [])
        self.assertFalse((self.job / "samples.json").exists())
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))

    def test_saved_legacy_prepare_gets_fresh_review_without_authoring_or_resampling(self):
        self.pipeline(FakeSession()).run("validate")
        legacy, old_review = self.downgrade_saved_review()
        files = [self.job / name for name in ("samples.json", "source/source.json", "workspace/generator.py")]
        original = [path.read_bytes() for path in files]
        session = FakeSession()
        result = self.pipeline(session).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual([role for role, _ in session.calls], ["review"])
        self.assertIn(f"-policy-{REVIEW_POLICY_VERSION}-", result["review"])
        self.assertEqual(legacy.read_bytes(), old_review)
        self.assertEqual([path.read_bytes() for path in files], original)
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_current_saved_review_is_revalidated_before_preparation(self):
        state = self.pipeline(FakeSession()).run("validate")
        path = Path(state["review"])
        review = json.loads(path.read_text())
        review["checks"]["decision_variation"]["status"] = "failed"
        path.write_text(json.dumps(review))
        with self.assertRaisesRegex(ValueError, "accepted review requires passing decision_variation"):
            self.pipeline(FakeSession()).run()
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))

    def test_legacy_source_gets_delivery_inventory_without_replacing_instructional_snapshot(self):
        self.pipeline(FakeSession()).run("validate")
        self.downgrade_saved_review()
        source = (self.job / "source/source.json").read_bytes()
        inventory = self.job / "source/inventory.json"
        inventory.unlink()
        state = json.loads((self.job / "job.json").read_text())
        state.pop("inventory_hash")
        (self.job / "job.json").write_text(json.dumps(state))
        session = FakeSession()
        result = self.pipeline(session).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual([role for role, _ in session.calls], ["review"])
        self.assertEqual(self.publisher.inventory_extractions, 2)
        self.assertTrue(inventory.is_file())
        self.assertEqual((self.job / "source/source.json").read_bytes(), source)

    def test_source_refresh_replaces_delivery_binding_and_allows_repair(self):
        original_prepare = self.publisher.prepare
        attempts = []
        def prepare(*args, **kwargs):
            attempts.append(True)
            if len(attempts) == 1:
                self.publisher.material = {"question": "Square 9."}
                raise SourceChanged("Source changed before publication")
            return original_prepare(*args, **kwargs)
        session = FakeSession()
        with patch.object(self.publisher, "prepare", side_effect=prepare):
            result = self.pipeline(session).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual([role for role, _ in session.calls], ["author", "review", "author", "review"])
        self.assertEqual(self.publisher.inventory_extractions, 2)
        inventory = json.loads((self.job / "source/inventory.json").read_text())
        self.assertEqual(inventory["fingerprints"], [source_digest(self.publisher.material)])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_policy_upgrade_recovers_unknown_commit_before_review_without_republication(self):
        first = FakePublisher(self.root, lose_ack=True)
        with self.assertRaises(ConnectionError):
            self.pipeline(FakeSession(), publisher=first).run()
        request_path = self.job / "publication/request.json"
        saved = request_path.read_bytes()
        legacy, old_review = self.downgrade_saved_review()
        restarted = FakePublisher(self.root)
        class RecoveryOrderedSession(FakeSession):
            def __call__(inner, role, context, directory):
                self.assertEqual(restarted.publishes, 1)
                self.assertEqual(request_path.read_bytes(), saved)
                return super().__call__(role, context, directory)
        session = RecoveryOrderedSession()
        result = self.pipeline(session, publisher=restarted).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual([role for role, _ in session.calls], ["review"])
        self.assertEqual((restarted.prepares, restarted.publishes), (0, 1))
        self.assertEqual(result["publication"]["writes"], 1)
        self.assertEqual(request_path.read_bytes(), saved)
        self.assertEqual(legacy.read_bytes(), old_review)
        approval = json.loads((self.math / "generators/approvals" / result["package_hash"] / "123.json").read_text())
        self.assertEqual(approval["bands"]["easy"]["review_policy_version"], REVIEW_POLICY_VERSION)

    def test_postcommit_policy_review_failure_keeps_receipt_and_requests_repair(self):
        first = FakePublisher(self.root, lose_ack=True)
        with self.assertRaises(ConnectionError):
            self.pipeline(FakeSession(), publisher=first).run()
        saved = (self.job / "publication/request.json").read_bytes()
        self.downgrade_saved_review()
        restarted = FakePublisher(self.root)
        session = FakeSession(reject=True)
        result = self.pipeline(session, publisher=restarted).run()
        self.assertEqual(result["stage"], "unsupported")
        self.assertTrue(result["needs_repair"])
        self.assertTrue(result["publication"]["passed"])
        self.assertEqual(result["publication"]["writes"], 1)
        self.assertEqual([role for role, _ in session.calls], ["review"])
        self.assertEqual((restarted.prepares, restarted.publishes), (0, 1))
        self.assertEqual((self.job / "publication/request.json").read_bytes(), saved)
        self.assertFalse((self.math / "generators/approvals" / result["package_hash"] / "123.json").exists())
        repeated = self.pipeline(session, publisher=restarted).run()
        self.assertEqual(repeated, result)
        self.assertEqual((restarted.prepares, restarted.publishes), (0, 1))

    def test_refill_unknown_commit_is_recovered_even_when_approval_policy_is_now_stale(self):
        request, approved = self.approve_for_refill()
        self.publisher.lose_ack = True
        session = FakeSession()
        with self.assertRaises(ConnectionError):
            self.pipeline(session, request=request).run()
        saved = (self.job / "publication/request.json").read_bytes()
        path = self.math / "generators/approvals" / approved["package_hash"] / "123.json"
        approval = json.loads(path.read_text())
        approval["bands"]["easy"]["review_policy_version"] = REVIEW_POLICY_VERSION - 1
        path.write_text(json.dumps(approval))
        result = self.pipeline(session, request=request).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual(session.calls, [])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 2))
        self.assertEqual((self.job / "publication/request.json").read_bytes(), saved)

    def test_refill_requires_matching_current_registration_source_and_reviewed_band(self):
        request, approved = self.approve_for_refill()
        for failure, code in (("registration", "registration_changed"), ("source", "source_changed"),
                              ("band", "approval_band_missing"), ("missing", "approval_missing")):
            with self.subTest(failure=failure):
                self.job = self.root / ("refill-" + failure)
                self.publisher.registered_generator = {":question-generator/script": request["registered_package"]}
                self.publisher.material = {"question": "Square 7."}
                current = dict(request)
                if failure == "registration":
                    self.publisher.registered_generator = None
                elif failure == "source":
                    self.publisher.material = {"question": "Cube 7."}
                elif failure == "band":
                    current["difficulty"] = "hard"
                else:
                    (self.math / "generators/approvals" / approved["package_hash"] / "123.json").unlink()
                session = FakeSession()
                result = self.pipeline(session, request=current).run()
                self.assertEqual(result["stage"], "unsupported")
                self.assertTrue(result["needs_repair"])
                self.assertEqual(result["error"]["code"], code)
                self.assertEqual(session.calls, [])
                self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))

    def test_refill_recovers_unknown_publication_without_agents_or_repreparation(self):
        request, _ = self.approve_for_refill()
        self.publisher.lose_ack = True
        session = FakeSession()
        with self.assertRaises(ConnectionError):
            self.pipeline(session, request=request).run()
        saved_request = (self.job / "publication/request.json").read_bytes()
        result = self.pipeline(session, request=request).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual(session.calls, [])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 2))
        self.assertEqual((self.job / "publication/request.json").read_bytes(), saved_request)

    def test_refill_source_changed_during_preparation_never_starts_an_agent(self):
        request, _ = self.approve_for_refill()
        session = FakeSession()
        with patch.object(self.publisher, "prepare", side_effect=SourceChanged("Source or registration changed")):
            result = self.pipeline(session, request=request).run()
        self.assertEqual(result["stage"], "unsupported")
        self.assertEqual(result["error"]["code"], "source_changed")
        self.assertEqual(session.calls, [])
        self.assertEqual(self.publisher.publishes, 0)

    def test_refill_deterministic_preparation_failure_requests_repair_once(self):
        request, _ = self.approve_for_refill()
        session = FakeSession()
        with patch.object(self.publisher, "prepare", side_effect=ValueError("Canonical answer must belong to its field bank")) as prepare:
            result = self.pipeline(session, request=request).run()
            repeated = self.pipeline(session, request=request).run()
        self.assertEqual(result["stage"], "unsupported")
        self.assertTrue(result["needs_repair"])
        self.assertEqual(result["error"]["code"], "preparation_invalid")
        self.assertEqual(repeated, result)
        self.assertEqual(prepare.call_count, 1)
        self.assertEqual(session.calls, [])
        self.assertEqual(self.publisher.publishes, 0)

    def test_refill_preparation_transport_failure_remains_resumable(self):
        request, _ = self.approve_for_refill()
        session = FakeSession()
        with patch.object(self.publisher, "prepare", side_effect=ConnectionError("Database disconnected")):
            with self.assertRaises(ConnectionError):
                self.pipeline(session, request=request).run()
        self.assertEqual(json.loads((self.job / "job.json").read_text())["stage"], "prepare")
        samples = (self.job / "samples.json").read_bytes()
        result = self.pipeline(session, request=request).run()
        self.assertEqual(result["stage"], "verified")
        self.assertEqual((self.job / "samples.json").read_bytes(), samples)
        self.assertEqual(session.calls, [])

    def test_refill_prepublication_rejection_is_terminal_only_without_saved_intent(self):
        request, _ = self.approve_for_refill()
        session = FakeSession()
        result = self.pipeline(session, request=request).run("prepare")
        self.assertEqual(result["stage"], "push")
        intent = self.job / "publication/request.json"
        saved_intent = intent.read_bytes()
        with patch.object(self.publisher, "publish", side_effect=ValueError("Receipt differs from prepared assertions")):
            with self.assertRaisesRegex(ValueError, "Receipt differs"):
                self.pipeline(session, request=request).run()
        self.assertEqual(intent.read_bytes(), saved_intent)
        self.assertEqual(json.loads((self.job / "job.json").read_text())["stage"], "push")
        self.assertEqual(self.publisher.prepares, 1)
        # Real Publisher creates the intent only after native preview succeeds.
        # Simulate its pre-intent boundary separately from the saved-intent case.
        intent.unlink()
        with patch.object(self.publisher, "publish", side_effect=ValueError("Preview contains an invalid answer field")):
            result = self.pipeline(session, request=request).run()
        self.assertEqual(result["stage"], "unsupported")
        self.assertTrue(result["needs_repair"])
        self.assertEqual(result["error"]["code"], "prepublication_invalid")
        self.assertEqual(session.calls, [])

    def test_refill_rechecks_package_and_batch_before_publication(self):
        request, _ = self.approve_for_refill()
        session = FakeSession()
        result = self.pipeline(session, request=request).run("validate")
        self.assertEqual(result["stage"], "prepare")
        (self.job / "workspace/helper.py").write_text("def square(n): return n + n\n")
        result = self.pipeline(session, request=request).run()
        self.assertEqual(result["stage"], "unsupported")
        self.assertTrue(result["needs_repair"])
        self.assertEqual(session.calls, [])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))

    def test_refill_rejects_corrupted_archive_without_agents(self):
        request, approved = self.approve_for_refill()
        script = resolve_registered_script(approved["registration"], self.root, self.math)
        script.chmod(0o755)
        script.write_text(script.read_text() + "\n# corrupt immutable archive\n")
        session = FakeSession()
        result = self.pipeline(session, request=request).run()
        self.assertEqual(result["stage"], "unsupported")
        self.assertTrue(result["needs_repair"])
        self.assertEqual(session.calls, [])
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (0, 0))

    def test_prior_verified_job_can_backfill_approval_without_republication(self):
        session = FakeSession()
        result = self.pipeline(session).run()
        path = self.math / "generators/approvals" / result["package_hash"] / "123.json"
        path.unlink()
        result.pop("approval_recorded")
        (self.job / "job.json").write_text(json.dumps(result))
        calls_before = list(session.calls)
        result = self.pipeline(session).run()
        self.assertTrue(path.exists())
        self.assertTrue(result["approval_recorded"])
        self.assertEqual(session.calls, calls_before)
        self.assertEqual((self.publisher.prepares, self.publisher.publishes), (1, 1))

    def test_inventory_refill_kind_is_forwarded_but_saved_build_request_wins(self):
        inventory = self.root / "inventory.json"
        inventory.write_text(json.dumps({"cycle": 1, "request": {
            "knowledgePoint": 123, "difficulty": "easy", "missing": 2,
            "stage": "replenish", "jobKind": "refill", "script": "generators/ab/" + "ab" * 32 + "/generator.py"}}))
        for saved in (False, True):
            if saved:
                directory = inventory.with_suffix(".pipeline") / "1"
                directory.mkdir(parents=True)
                (directory / "job.json").write_text(json.dumps({"request": self.request}))
            with patch("generator_publish.Publisher.from_environment", return_value=self.publisher), \
                    patch("serve_graph_explorer.database_environment", return_value=self.environment), \
                    patch("generator_pipeline.Pipeline") as pipeline, patch("builtins.print"):
                pipeline.return_value.run.return_value = {"stage": "verified"}
                self.assertEqual(main(["--inventory-job", str(inventory)]), 0)
            admitted = pipeline.call_args.args[1]
            if saved:
                self.assertEqual(admitted, self.request)
            else:
                self.assertEqual(admitted["job_kind"], "refill")
                self.assertEqual(admitted["count"], 2)


if __name__ == "__main__":
    unittest.main()
