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
        self.assertEqual(result["error"]["code"], "review_sessions_exhausted")
        self.assertEqual(result["error"]["resume_stage"], "validate")
        # The same durable six-session cap includes source-account and exemplar
        # verification, leaving four final-report correction sessions.
        self.assertEqual([role for role, _ in session.calls], ["author"] + ["review"] * 4)
        self.assertEqual(list(result["review_report_rounds"].values()), [4])
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

    def test_engine_change_rechecks_in_same_verifier_without_reusing_cached_correction(self):
        pipeline = self.pipeline(fixtures.FakeSession())
        pipeline.run(stop_after="generate")
        original_evidence = pipeline.review_directory()
        original_evidence.mkdir(exist_ok=True)
        pipeline.seed_verifier_account(original_evidence)
        pipeline.prepare_refill_review(original_evidence)
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
        self.assertEqual([role for role, _ in session.calls], ['review', 'review'])
        directory, context = session.review_contexts[0]
        self.assertEqual(directory, original_evidence / 'contract-repair')
        self.assertEqual(context['review_binding'], original_binding)
        self.assertEqual(Path(result['review']), original_evidence / 'result.json')
        final = json.loads((original_evidence / 'review-binding.json').read_text())
        self.assertNotEqual(final['engine_hash'], original_binding['engine_hash'])
        self.assertEqual(final['batch_hash'], original_binding['batch_hash'])
        next_directory, next_context = session.review_contexts[1]
        self.assertEqual(next_directory, original_evidence / 'contract-repair-2')
        self.assertEqual(next_context['resume_session_id'], 'engine-repair-thread')
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
        # This regression now also retains the demonstrated sampler defect in
        # the approved refill contract, using real survivor delivery/grading.
        actual_root = Path(__file__).resolve().parents[1]
        self.publisher.material['kp'] = {':knowledge-point/id': '12345678-1234-5678-1234-567812345678'}
        native = self.root / 'generate/runs/current/check-engine'
        native.parent.mkdir(parents=True)
        native.symlink_to(actual_root / 'generate/runs/current/check-engine')
        from scripts.generator_native_build import ensure_native_grader
        self.enterContext(patch('scripts.generator_native_build.ensure_native_grader',
            side_effect=lambda repo, env: ensure_native_grader(actual_root, env)))
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
                    checker = workspace / 'check_refill.py'
                    checker.write_text(textwrap.dedent('''\
                        import argparse, hashlib, json, os, subprocess, sys, tempfile
                        from pathlib import Path
                        p=argparse.ArgumentParser()
                        for name in ('records','inventory','output'): p.add_argument('--'+name)
                        args=p.parse_args(); records=json.loads(Path(args.records).read_text())
                        band=records[0]['question'][':question/difficulty'].split('/')[-1]
                        with tempfile.TemporaryDirectory() as output:
                            raw=json.loads(subprocess.check_output([sys.executable,'-E','-s','-B','generator.py',
                                '--difficulty',band,'--count','5','--seed','607','--format','json'],
                                env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':output},text=True))
                        assert len({r['question'][':question/problem'] for r in raw})==5, 'Sampler repeats a fixed question'
                        fingerprints=[]; native=[]
                        for row in records:
                            q=row['question']; n=int(q[':question/problem'].split()[1]); f=q[':question/answer-fields'][0]
                            correct=f[':answer-field/correct']; correct=correct[-1] if isinstance(correct,list) else correct
                            answer=next(a for a in f[':answer-field/choices'] if a[':answer/id']==correct)
                            assert int(answer[':answer/value'])==n*n
                            content={':question/problem':q[':question/problem'],':question/answer-fields':[{
                                ':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'],
                                ':answer-field/correct':{':answer/type':answer[':answer/type'],':answer/value':answer[':answer/value']}}]}
                            identity=hashlib.sha256(json.dumps(content,sort_keys=True,separators=(',',':')).encode()).hexdigest()
                            fingerprints.append(identity)
                            native.append({'fingerprint':identity,'checks':[{'field_index':0,'submitted':str(n*n+1),
                                'expected':'rejected','purpose':'One more than the independently computed square is wrong'}]})
                        fingerprints.sort()
                        Path(args.output).write_text(json.dumps({'status':'passed','checked_fingerprints':fingerprints,
                            'check_results':[{'id':'distinct-sampler','status':'passed','checked_fingerprints':fingerprints}],
                            'native_checks':native}))
                    '''))
                    (workspace / 'refill-validation.json').write_text(json.dumps({
                        'format':'course-academy-refill-check-v1','script':checker.name,'args':[],'files':[]}))
                    plan_path = workspace / 'refill-review-plan.json'
                    plan = json.loads(plan_path.read_text())
                    plan.update(status='checks',reason='Retain distinct sampling plus independently checked survivor arithmetic.',
                        checks=[{'id':'distinct-sampler','purpose':'Detect the fixed-question sampler on a fresh seed and check actual survivor answers.',
                                 'finding_ids':[row['id'] for row in findings]}], finding_exemptions=[])
                    plan_path.write_text(json.dumps(plan))
                    manifest_path = workspace / 'package.json'; manifest = json.loads(manifest_path.read_text())
                    manifest['files'] += [checker.name, 'refill-validation.json']
                    manifest_path.write_text(json.dumps(manifest))
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
