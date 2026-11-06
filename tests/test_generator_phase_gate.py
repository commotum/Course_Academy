"""Adversarial admission checks; agent judgments are explicit test doubles."""
import json
from pathlib import Path
import unittest

from generator_pipeline import Pipeline, digest
import test_generator_pipeline as fixtures
from test_generator_pipeline import FakeSession, PhaseSession, fixture_investigation


class PhaseGateTests(unittest.TestCase):
    setUp = fixtures.GeneratorPipelineTests.setUp
    tearDown = fixtures.GeneratorPipelineTests.tearDown
    pipeline = fixtures.GeneratorPipelineTests.pipeline

    def prepare(self, session):
        pipeline = self.pipeline(session)
        source = self.publisher.extract_source(123, self.job / 'source')
        (self.job / 'workspace').mkdir(exist_ok=True)
        pipeline.persist(stage='investigate', source_hash=digest(source))
        return pipeline

    def test_source_accounts_precede_donor_and_exemplar_exposure_and_same_verifier_continues(self):
        events, contexts = [], []
        class Session(FakeSession):
            def phase_call(inner, role, context, directory):
                events.append((role, context['phase']))
                contexts.append((role, dict(context)))
                return super().phase_call(role, context, directory)
            def __call__(inner, role, context, directory):
                events.append((role, context.get('phase', 'generator')))
                return super().__call__(role, context, directory)
        def donor(publisher, source, directory):
            events.append(('runner', 'donors'))
            self.assertTrue(list((self.job / 'investigation/source-account/revisions').glob('*/original-*.json')))
            return fixture_investigation(publisher, source, directory)
        session = Session()
        pipeline = Pipeline(self.job, self.request, self.publisher, root=self.root,
            environment=self.environment, session=PhaseSession(session), investigation_preparer=donor)
        result = pipeline.run(stop_after='validate')
        self.assertEqual(result['stage'], 'prepare')
        self.assertLess(events.index(('investigate', 'source_account')), events.index(('runner', 'donors')))
        self.assertLess(events.index(('review', 'source_account')), events.index(('review', 'exemplars')))
        self.assertLess(events.index(('review', 'exemplars')), events.index(('author', 'generator')))
        for role, context in contexts:
            if context['phase'] == 'source_account':
                self.assertFalse(set(context) & {'reference_file', 'exemplars_file', 'manifest', 'initial_source_analysis_file', 'investigation_account_file'})
        self.assertEqual(result['review_thread'], 'fixture-review')
        gate = result['exemplar_gate']
        final = json.loads(Path(result['review']).read_text())
        original = json.loads(Path(result['verifier_account']['path']).read_text())
        self.assertEqual(final['source_analysis']['reasoning_steps'], original['reasoning_steps'])
        self.assertEqual(gate['binding']['initial_source_analysis_sha256'], result['verifier_account']['sha256'])

    def test_missing_target_account_never_queries_donors_or_calls_author(self):
        class Missing(FakeSession):
            def phase_call(inner, role, context, directory):
                return {'status': 'ready', 'account_file': 'source-analysis.json'}
        session = Missing()
        pipeline = self.prepare(session)
        pipeline.investigation_preparer = lambda *args: self.fail('Donor exposed before target account')
        result = pipeline.run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual(session.calls, [])

    def test_ready_investigator_survives_verifier_repairs_and_parent_reload_without_launch(self):
        from unittest.mock import Mock, patch
        from generator_pipeline import CodexSession, RunnerChanged
        from generator_session_binding import bind_session
        pending = {}
        class RealDesign(FakeSession):
            repaired = False
            crash = False
            def __call__(inner, role, context, directory):
                if role == 'investigate':
                    self.assertNotIn('initial_source_analysis_file', context)
                    self.assertNotIn('investigation_result', context)
                    pending.update(role=role, context=context, directory=directory)
                    return CodexSession(root=Path(__file__).resolve().parents[1])(role, context, directory)
                return super().__call__(role, context, directory)
            def phase_call(inner, role, context, directory):
                if context['phase'] == 'exemplars' and not inner.repaired:
                    account = Path(context['investigation_account_file'])
                    account.write_text(account.read_text() + '\nVerifier clarified the independent multiplication.\n')
                    path = Path(context['exemplars_file'])
                    rows = json.loads(path.read_text())
                    rows[0]['question'][':question/worked-solution'] += ' Verifier checked this multiplication.'
                    path.write_text(json.dumps(rows))
                    inner.repaired = True
                elif context['phase'] == 'exemplars':
                    inner.crash = True
                return super().phase_call(role, context, directory)
        session = RealDesign()
        pipeline = self.prepare(session)
        def spawn(command, **kwargs):
            process = Mock(returncode=0, pid=-1)
            def finish(*args, **kwargs):
                result = FakeSession.__call__(session, pending['role'], pending['context'], pending['directory'])
                handoff = Path(pending['context']['investigation_account_file'])
                handoff.write_text(handoff.read_text() + '\nInvestigator completed the design handoff.\n')
                Path(command[command.index('--output-last-message') + 1]).write_text(json.dumps(result))
            process.communicate.side_effect = finish
            return process
        def reload():
            if session.crash:
                session.crash = False
                raise RunnerChanged('Simulated parent reload after accepted exemplar result')
        pipeline.reload_repaired_runner = reload
        with patch('generator_pipeline.subprocess.Popen', side_effect=spawn) as launches:
            with self.assertRaises(RunnerChanged): pipeline.investigate()
            self.assertIn('investigation_draft', pipeline.state)
            handoff = (self.job / 'workspace/investigation.md').read_bytes()
            anchors = (self.job / 'workspace/exemplars.json').read_bytes()
            execution = (self.job / 'investigation/execution.json').read_bytes()
            resumed = self.pipeline(session); resumed.investigate()
            self.assertEqual(resumed.state['stage'], 'generate')
            self.assertEqual(launches.call_count, 1)
            self.assertEqual((self.job / 'investigation/execution.json').read_bytes(), execution)
            self.assertEqual((self.job / 'workspace/investigation.md').read_bytes(), handoff)
            self.assertEqual((self.job / 'workspace/exemplars.json').read_bytes(), anchors)
            self.assertTrue(resumed.exemplar_gate_current())
            # Reproduce the old archive+exhaustion bug and migrate its intact
            # ready result, without granting a new execution allowance.
            resumed.state.pop('investigation_draft')
            directory = self.job / 'investigation'
            old = json.loads((directory / 'input-binding.json').read_text())
            changed = json.loads(json.dumps(old)); changed['inputs']['upstream']['initial_source_analysis_file'] = {'sha256': 'downstream'}
            bind_session(directory, changed)
            budget = json.loads((directory / 'execution.json').read_text()); budget['launches'] = 3
            (directory / 'execution.json').write_text(json.dumps(budget))
            resumed.persist(stage='blocked', error={'code': 'agent_session_retry_exhausted',
                'cause': {'role': 'investigate', 'session_directory': str(directory)}, 'resume_stage': 'investigate'})
            before = (directory / 'execution.json').read_bytes()
            self.assertTrue(resumed.recover_completed_investigation())
            resumed.investigate()
            self.assertEqual(resumed.state['stage'], 'generate')
            self.assertEqual(launches.call_count, 1)
            self.assertEqual((directory / 'execution.json').read_bytes(), before)
            self.assertFalse(resumed.state['completed_result_recoveries'][-1]['launch_budget_changed'])
            # The recovered checkpoint still binds immutable upstream inputs.
            context = resumed.investigation_context({'investigation_file': resumed.state['investigation_file'],
                'reference_file': resumed.state['reference_file']}, directory)
            for key in ('investigation_file', 'reference_file', 'target_account_file'):
                with self.subTest(changed=key):
                    changed_path = self.job / (key + '.json')
                    changed_path.write_text('{"meaning":"different upstream evidence"}')
                    self.assertIsNone(resumed.saved_investigation_draft({**context, key: str(changed_path)}, directory))
            self.publisher.material['question'] = 'Different target operation.'
            self.publisher.extract_source(123, self.job / 'source')
            self.assertIsNone(resumed.saved_investigation_draft(context, directory))

    def test_exemplar_cli_uses_runner_binding_and_rejects_missing_tool_report(self):
        import subprocess
        import sys
        from generator_review import validate_review
        class BindingPresent(FakeSession):
            def phase_call(inner, role, context, directory):
                if context['phase'] == 'exemplars':
                    binding = json.loads((Path(directory) / 'final-binding.json').read_text())
                    self.assertEqual(binding, context['review_binding'])
                    self.assertEqual(binding['phase'], 'exemplars')
                    self.assertNotIn('refill_plan', binding)
                return super().phase_call(role, context, directory)
        pipeline = self.prepare(BindingPresent()); pipeline.investigate()
        self.assertEqual(pipeline.state['stage'], 'generate')
        gate = pipeline.state['exemplar_gate']
        result = Path(gate['report']); evidence = result.parent
        command = [sys.executable, str(Path(__file__).resolve().parents[1] / 'scripts/generator_review.py'),
                   '--result', str(result), '--evidence-root', str(evidence)]
        valid = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertTrue(json.loads(valid.stdout)['valid'])
        # Exemplar dispatch is a CLI convenience, never a relaxation of final
        # generator review when the runner invokes that validator directly.
        with self.assertRaisesRegex(ValueError, 'refill review plan'):
            validate_review(json.loads(result.read_text()), evidence, gate['binding'])
        binding_file = evidence / 'final-binding.json'
        binding_file.write_text(json.dumps({**gate['binding'], 'phase': 'unrecognized'}))
        unknown = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(unknown.returncode, 1)
        self.assertIn('refill review plan', json.loads(unknown.stderr)['error'])
        binding_file.write_text('[]')
        malformed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(malformed.returncode, 1)
        self.assertIn('must be an object', json.loads(malformed.stderr)['error'])
        binding_file.write_text(json.dumps(gate['binding']))
        (evidence / 'easy-grading.json').unlink()
        invalid = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(invalid.returncode, 1)
        self.assertIn('easy-grading.json', json.loads(invalid.stderr)['error'])

    def test_missing_ready_design_output_reaches_bounded_repair_instead_of_empty_retries(self):
        class CountDesigns(FakeSession):
            designs = 0
            def __call__(inner, role, context, directory):
                if role == 'investigate': inner.designs += 1
                return super().__call__(role, context, directory)
        session = CountDesigns(); pipeline = self.prepare(session); pipeline.investigate()
        (self.job / 'workspace/exemplars.json').unlink()
        pipeline.persist(stage='investigate')
        pipeline.investigate()
        self.assertEqual(pipeline.state['stage'], 'generate')
        self.assertEqual(session.designs, 2)
        self.assertEqual(pipeline.state['investigation_rounds'], 1)

    def test_missing_exemplars_never_calls_author(self):
        class Missing(FakeSession):
            def __call__(inner, role, context, directory):
                if role == 'investigate':
                    return {'status': 'ready', 'exemplars_file': None}
                return super().__call__(role, context, directory)
        session = Missing()
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual(session.calls, [])

    def test_independent_math_rejection_blocks_wrong_key_before_author(self):
        class WrongKey(FakeSession):
            def __call__(inner, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == 'investigate':
                    path = Path(context['workspace']) / result['exemplars_file']
                    rows = json.loads(path.read_text())
                    rows[0]['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'] = '999'
                    path.write_text(json.dumps(rows))
                return result
            def phase_call(inner, role, context, directory):
                result = super().phase_call(role, context, directory)
                if context['phase'] == 'exemplars':
                    rows = json.loads(Path(context['exemplars_file']).read_text())
                    q = rows[0]['question']; n = int(q[':question/problem'].split()[1])
                    actual = int(q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])
                    if actual != n * n:
                        result['verdict'] = 'revise'
                        result['checks']['math']['status'] = 'failed'
                return result
        session = WrongKey()
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertFalse(any(role == 'author' for role, _ in session.calls))
        self.assertEqual(self.publisher.prepares, 0)

    def test_declared_acceptance_without_actual_tool_evidence_never_calls_author(self):
        class MissingEvidence(FakeSession):
            def phase_call(inner, role, context, directory):
                result = super().phase_call(role, context, directory)
                if context['phase'] == 'exemplars':
                    (Path(directory) / 'easy-grading.json').unlink()
                return result
        session = MissingEvidence()
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual(session.calls, [])

    def test_anchor_image_edit_invalidates_both_list_and_wrapper_gate(self):
        for wrapper in (False, True):
            with self.subTest(wrapper=wrapper):
                self.job = self.root / ('wrapper' if wrapper else 'list')
                class Images(FakeSession):
                    preserve = False
                    reject_gate = False
                    def __call__(inner, role, context, directory):
                        if role == 'investigate' and inner.preserve:
                            return {'status': 'ready', 'exemplars_file': 'exemplars.json'}
                        result = super().__call__(role, context, directory)
                        if role == 'investigate':
                            path = Path(context['workspace']) / 'exemplars.json'
                            rows = json.loads(path.read_text())
                            rows[0]['question'][':question/problem'] += ' <img src="diagram.svg">'
                            path.write_text(json.dumps({'records': rows} if wrapper else rows))
                            path.with_name('diagram.svg').write_text('<svg>original visible operand</svg>')
                        return result
                    def phase_call(inner, role, context, directory):
                        result = super().phase_call(role, context, directory)
                        if context['phase'] == 'exemplars' and inner.reject_gate:
                            result['verdict'] = 'revise'
                        return result
                session = Images(); pipeline = self.prepare(session)
                pipeline.investigate()
                self.assertEqual(pipeline.state['stage'], 'generate')
                self.assertTrue(pipeline.exemplar_gate_current())
                (self.job / 'workspace/diagram.svg').write_text('<svg>changed answer-bearing operand</svg>')
                self.assertFalse(pipeline.exemplar_gate_current())
                session.preserve = session.reject_gate = True
                result = pipeline.run()
                self.assertEqual(result['stage'], 'blocked')
                self.assertEqual(session.calls, [])

    def test_rewritten_initial_verifier_account_cannot_establish_acceptance(self):
        class Rewrite(FakeSession):
            def phase_call(inner, role, context, directory):
                result = super().phase_call(role, context, directory)
                if context['phase'] == 'exemplars':
                    path = Path(directory) / 'source-analysis.json'
                    account = json.loads(path.read_text()); account['skill'] = 'Copy the displayed answer'
                    path.write_text(json.dumps(account))
                return result
        session = Rewrite()
        result = self.pipeline(session).run()
        self.assertEqual(result['stage'], 'blocked')
        self.assertEqual(session.calls, [])

    def test_enum_difficulty_anchors_are_each_bound_to_one_record(self):
        class Enums(FakeSession):
            def __call__(inner, role, context, directory):
                result = super().__call__(role, context, directory)
                if role == 'investigate':
                    path = Path(context['workspace']) / 'exemplars.json'
                    rows = json.loads(path.read_text())
                    for row in rows:
                        row['question'][':question/difficulty'] = {':db/ident': row['question'][':question/difficulty']}
                    path.write_text(json.dumps(rows))
                return result
        pipeline = self.prepare(Enums()); pipeline.investigate()
        self.assertEqual(pipeline.state['stage'], 'generate')
        for row in pipeline.state['exemplar_gate']['binding']['verification_batches'].values():
            self.assertEqual(len(json.loads(Path(row['batch_file']).read_text())), 1)

    def test_changed_source_after_downstream_exposure_starts_source_only_thread(self):
        accounts = []
        class Recording(FakeSession):
            def phase_call(inner, role, context, directory):
                if context['phase'] == 'source_account':
                    accounts.append((role, context.get('resume_session_id'), context['source_account_identity']))
                return super().phase_call(role, context, directory)
        session = Recording()
        pipeline = self.pipeline(session)
        self.assertEqual(pipeline.run(stop_after='generate')['stage'], 'validate')
        original = {role: identity for role, _, identity in accounts}
        self.publisher.material['question'] = 'Square 8 independently.'
        source = self.publisher.extract_source(123, self.job / 'source')
        pipeline.persist(stage='investigate', source_hash=digest(source), inventory_hash=None)
        pipeline.investigate()
        for role, resumed, identity in accounts[2:]:
            self.assertIsNone(resumed)
            self.assertNotEqual(identity, original[role])
        self.assertEqual(len(accounts), 4)

    def test_source_only_capture_preserves_relative_diagrams_and_image_revisions(self):
        snapshots = []
        class Diagrams(FakeSession):
            def phase_call(inner, role, context, directory):
                if context['phase'] == 'source_account':
                    captured = Path(context['source_file']).parent / 'diagram.svg'
                    snapshots.append(captured)
                    self.assertTrue(captured.is_file())
                return super().phase_call(role, context, directory)
        pipeline = self.prepare(Diagrams())
        original = self.job / 'source/diagram.svg'; original.write_text('<svg>original diagram</svg>')
        self.publisher.material['question'] = 'Interpret ![diagram](diagram.svg) and square the value.'
        self.publisher.extract_source(123, self.job / 'source')
        pipeline.source_account_phase('investigate')
        original.write_text('<svg>revised diagram</svg>')
        pipeline.source_account_phase('investigate')
        self.assertNotEqual(snapshots[0], snapshots[1])
        self.assertEqual(snapshots[0].read_text(), '<svg>original diagram</svg>')
        self.assertEqual(snapshots[1].read_text(), '<svg>revised diagram</svg>')

    def test_fixed_directory_account_is_not_reused_and_new_workspace_has_no_prior_outputs(self):
        import hashlib
        from generator_session_binding import policy_identity
        contexts = []
        class Isolated(FakeSession):
            def phase_call(inner, role, context, directory):
                if context['phase'] == 'source_account':
                    contexts.append(dict(context))
                    self.assertFalse((Path(context['workspace']) / 'source-analysis.json').exists())
                    self.assertFalse((Path(context['workspace']) / 'result.json').exists())
                    self.assertFalse((Path(context['workspace']) / 'session-outputs.json').exists())
                    self.assertIsNone(context.get('resume_session_id'))
                    self.assertIsNone(context.get('feedback'))
                return super().phase_call(role, context, directory)
        pipeline = self.prepare(Isolated())
        old = self.job / 'investigation/source-account'; old.mkdir(parents=True)
        original = old / 'source-analysis.json'; original.write_text(json.dumps(FakeSession.source_account()))
        (old / 'result.json').write_text('{"status":"ready","account_file":"source-analysis.json"}')
        (old / 'session-outputs.json').write_text(json.dumps({'files': {str(original): 'old'}}))
        (old / 'execution.json').write_text(json.dumps({'launches': 3, 'thread_id': 'contaminated', 'persistent_session': True}))
        pipeline.persist(target_account={'path': str(original), 'sha256': hashlib.sha256(original.read_bytes()).hexdigest(),
            'source': pipeline.phase_source_identity(), 'policy': policy_identity(self.root, 'investigate')},
            target_account_error='Old account at ' + str(original), investigate_thread='contaminated')
        saved = pipeline.source_account_phase('investigate')
        self.assertEqual(saved['isolation_version'], 1)
        self.assertTrue(Path(saved['path']).is_relative_to(old / 'revisions'))
        self.assertEqual(json.loads((old / 'execution.json').read_text())['launches'], 3)
        self.assertTrue(original.exists())
        self.assertEqual(len(contexts), 1)

    def test_missing_legacy_root_budget_still_retains_correction_launches(self):
        pipeline = self.prepare(FakeSession())
        phase = self.job / 'investigation/source-account'
        correction = phase / 'correction-1'; correction.mkdir(parents=True)
        (correction / 'execution.json').write_text(json.dumps({'launches': 2, 'launch_limit': 4}))
        pipeline.source_account_phase('investigate')
        budget = json.loads((phase / 'execution.json').read_text())
        self.assertEqual((budget['launches'], budget['launch_limit']), (2, 4))
        pipeline.source_account_phase('investigate')
        self.assertEqual(json.loads((phase / 'execution.json').read_text())['launches'], 2)

    def test_actual_session_gets_clean_revision_for_changed_source_and_policy_with_one_budget(self):
        from unittest.mock import Mock, patch
        from generator_pipeline import CodexSession, SessionRetryExhausted
        templates = self.root / 'generate/pipeline'; templates.mkdir(parents=True)
        prompt = templates / 'source-account.md'; prompt.write_text('Read target only. {{context}}')
        (templates / 'source-account.schema.json').write_text('{}')
        workspaces = []
        class Inspecting(CodexSession):
            def __call__(inner, role, context, directory):
                workspaces.append(Path(context['workspace']))
                self.assertFalse((Path(context['workspace']) / 'source-analysis.json').exists())
                self.assertIsNone(context.get('resume_session_id'))
                return super().__call__(role, context, directory)
        session = Inspecting(root=self.root)
        pipeline = Pipeline(self.job, self.request, self.publisher, root=self.root,
            environment=self.environment, session=session, investigation_preparer=fixture_investigation)
        self.publisher.extract_source(123, self.job / 'source')
        (self.job / 'workspace').mkdir()
        commands = []
        def spawn(command, **kwargs):
            commands.append(command)
            output = Path(command[command.index('--output-last-message') + 1])
            process = Mock(returncode=0, pid=-1)
            def completed(*args, **kwargs):
                output.with_name('source-analysis.json').write_text(json.dumps(FakeSession.source_account()))
                output.write_text('{"status":"ready","account_file":"source-analysis.json"}')
            process.communicate.side_effect = completed
            return process
        with patch('generator_pipeline.subprocess.Popen', side_effect=spawn):
            first = pipeline.source_account_phase('investigate')
            self.publisher.material['question'] = 'Square 8.'
            self.publisher.extract_source(123, self.job / 'source')
            second = pipeline.source_account_phase('investigate')
            prompt.write_text('Changed target-only instructions. {{context}}')
            third = pipeline.source_account_phase('investigate')
            self.publisher.material['question'] = 'Square 9.'
            self.publisher.extract_source(123, self.job / 'source')
            with self.assertRaises(SessionRetryExhausted):
                pipeline.source_account_phase('investigate')
        self.assertEqual(len(commands), 3)
        self.assertEqual(len(set(workspaces)), 4)
        self.assertTrue(all('resume' not in command for command in commands))
        self.assertTrue(all(Path(account['path']).exists() for account in (first, second, third)))
        budget = json.loads((self.job / 'investigation/source-account/execution.json').read_text())
        self.assertEqual(budget['launches'], 3)

    def test_active_approval_binds_retained_counterexample_and_nested_input_bytes(self):
        pipeline = self.pipeline(FakeSession())
        state = pipeline.run(stop_after='validate')
        evidence = Path(state['review']).parent
        history = {'findings': [{'id': 'old-given-step', 'finding': {'kind': 'restriction',
            'description': 'Earlier account required supplying the target operation.'}}], 'events': []}
        history_path = self.job / 'repair-history.json'; history_path.write_text(json.dumps(history))
        (evidence / 'rationale.md').write_text('Target source requires the learner to choose the operation independently.')
        (evidence / 'witness.json').write_text(json.dumps({'given': 'operand only', 'required': 'choose and calculate'}))
        (evidence / 'counterexample.json').write_text(json.dumps({'input_file': 'witness.json'}))
        (evidence / 'finding-dispositions.json').write_text(json.dumps({
            'format': 'course-academy-finding-dispositions-v1', 'findings': [{
                'id': 'old-given-step', 'disposition': 'superseded', 'reason': 'Original demand removed the target decision.',
                'source_refs': ['fixture-source-1'], 'evidence_paths': ['rationale.md'],
                'counterexample_path': 'counterexample.json'}]}))
        pipeline.check_repair_regressions(evidence)
        pipeline.verify_approval_inputs()
        self.assertIn('witness.json', pipeline.state['finding_dispositions']['evidence_binding']['files'])
        (evidence / 'witness.json').write_text(json.dumps({'given': 'answer supplied'}))
        with self.assertRaisesRegex(ValueError, 'counterexample changed'):
            pipeline.verify_approval_inputs()
        self.assertEqual(json.loads(history_path.read_text()), history)
        # Historical dispositions have no new marker and are not mass-upgraded.
        value = dict(pipeline.state['finding_dispositions']); value.pop('evidence_binding')
        pipeline.persist(finding_dispositions=value)
        pipeline.verify_approval_inputs()


if __name__ == '__main__': unittest.main()
