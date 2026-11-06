"""Durable source-first handoffs using the existing investigator and verifier."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import time

from inventory_jobs import save


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def account_markdown(account):
    return '\n\n'.join('## ' + key.replace('_', ' ').title() + '\n\n' +
        (value if isinstance(value, str) else '\n'.join('- ' + row for row in value))
        for key, value in account.items()) + '\n'


class InstructionalPhases:
    def phase_source_identity(self):
        from generator_pipeline import source_identity, asset_hashes
        path = self.directory / 'source/source.json'
        source = read(path)
        return {**source_identity(source), 'assets': asset_hashes(source['material'], path.parent, self.math_root)}

    def source_account_phase(self, role):
        """Checkpoint an independently produced account before downstream exposure."""
        from generator_pipeline import session_thread
        from generator_review import validate_source_account_checkpoint
        key = 'target_account' if role == 'investigate' else 'verifier_account'
        source = self.phase_source_identity()
        saved = self.state.get(key)
        if saved and saved['source'] == source:
            validate_source_account_checkpoint(saved['path'], saved['sha256'])
            return saved
        directory = self.directory / ('investigation' if role == 'investigate' else 'verification') / 'source-account'
        directory.mkdir(parents=True, exist_ok=True)
        rounds = self.state.get('source_account_rounds', {})
        count = rounds.get(role, 0)
        while count < self.max_attempts:
            current = directory if count == 0 else directory / ('correction-' + str(count))
            current.mkdir(parents=True, exist_ok=True)
            context = {'phase': 'source_account', 'source_account_role': role,
                'repo_root': str(self.root), 'knowledge_point': self.state['request']['kp'],
                'source_file': str(self.directory / 'source/source.json'),
                'source_root': str(self.directory / 'source'),
                'workspace': str(current), 'evidence_root': str(current),
                'account_file': str(current / 'source-analysis.json'),
                'python': self.environment.get('COURSE_ACADEMY_GENERATOR_PYTHON'),
                'feedback': self.state.get(key + '_error')}
            # This context intentionally has no donor, authored workspace,
            # exemplar, generator, repair history or previous interpretation.
            thread = self.state.get(role + '_thread') or session_thread(directory)
            if thread:
                context['resume_session_id'] = thread
            result = self.session_call(role, context, current)
            save(current / 'result.json', result)
            try:
                if result.get('status') != 'ready' or result.get('account_file') != 'source-analysis.json':
                    raise ValueError('Finish the source-only account before exposing downstream artifacts')
                produced = current / 'source-analysis.json'
                identity = validate_source_account_checkpoint(produced)
                checkpoint = directory / ('original-' + identity + '.json')
                if not checkpoint.exists():
                    shutil.copy2(produced, checkpoint)
                value = {'path': str(checkpoint), 'sha256': identity, 'source': source}
                self.persist(**{key: value, role + '_thread': session_thread(current) or thread,
                                key + '_error': None})
                if role == 'investigate':
                    handoff = self.directory / 'workspace/investigation.md'
                    handoff.parent.mkdir(parents=True, exist_ok=True)
                    if handoff.exists():
                        shutil.copy2(handoff, directory / ('prior-handoff-' + str(time.time_ns()) + '.md'))
                    handoff.write_text(account_markdown(read(checkpoint)))
                return value
            except (OSError, ValueError) as error:
                count += 1
                rounds[role] = count
                self.persist(source_account_rounds=rounds, **{key + '_error': str(error)})
        self.block('source_account_unfinished', self.state.get(key + '_error'), 'investigate')
        return None

    def exemplar_records(self):
        from generator_pipeline import inside, asset_hashes, VERIFICATION_BANDS
        from generator_publish import validate_question, enum
        value = self.state.get('exemplars_file')
        if not value:
            raise ValueError('Three concrete local anchors are required before authoring')
        path = inside(self.directory / 'workspace', value)
        records = read(path)
        if isinstance(records, dict):
            records = records.get('records', records.get('questions'))
        if not isinstance(records, list) or len(records) != 3:
            raise ValueError('Local anchors require exactly three complete records')
        if {enum(row.get('question', {}).get(':question/difficulty')) for row in records} != {
                ':question.difficulty/' + band for band in VERIFICATION_BANDS}:
            raise ValueError('Local anchors require one easy, moderate and hard record')
        for row in records:
            validate_question(row['question'])
        asset_hashes(records, path.parent, self.math_root)
        return path, records

    def required_investigation_handoff(self):
        path = self.directory / 'workspace/investigation.md'
        if not path.is_file() or len(path.read_text().strip()) < 80:
            raise ValueError('Missing substantive workspace/investigation.md handoff')
        return path

    def required_author_handoff(self):
        from generator_review import validate_source_account_checkpoint
        account = self.directory / 'workspace/instructional-account.json'
        validate_source_account_checkpoint(account)
        path = self.directory / 'workspace/instructional-account.md'
        if not path.is_file() or len(path.read_text().strip()) < 80:
            raise ValueError('Missing substantive workspace/instructional-account.md handoff')

    def exemplar_inputs(self):
        from generator_pipeline import asset_hashes
        from generator_review import validate_source_account_checkpoint
        path, records = self.exemplar_records()
        target, verifier = self.state.get('target_account'), self.state.get('verifier_account')
        if not target or not verifier:
            raise ValueError('Both source-only accounts must be checkpointed before exemplar review')
        source = self.phase_source_identity()
        for account in (target, verifier):
            if account['source'] != source:
                raise ValueError('Source changed since its independent account')
            validate_source_account_checkpoint(account['path'], account['sha256'])
        return {'source': source, 'target_account_sha256': target['sha256'],
            'initial_source_analysis_sha256': verifier['sha256'],
            'investigation_sha256': sha(self.required_investigation_handoff()),
            'exemplars_sha256': sha(path), 'assets': asset_hashes(records, path.parent, self.math_root)}

    def exemplar_gate_current(self):
        from generator_review import validate_exemplar_review
        gate = self.state.get('exemplar_gate')
        if not gate:
            return False
        try:
            if gate['inputs'] != self.exemplar_inputs():
                return False
            if sha(gate['report']) != gate['report_sha256']:
                return False
            validate_exemplar_review(read(gate['report']), Path(gate['report']).parent, gate['binding'])
            return True
        except (OSError, ValueError, KeyError):
            return False

    def prepare_exemplar_binding(self, evidence):
        from generator_pipeline import digest, asset_hashes, VERIFICATION_BANDS
        from generator_review import REVIEW_POLICY_VERSION
        path, records = self.exemplar_records()
        evidence.mkdir(parents=True, exist_ok=True)
        self.ensure_inventory()
        # Each anchor has its own exact raw input. No generator or answer-account
        # is supplied to this phase.
        batches = {}
        for band in VERIFICATION_BANDS:
            selected = [row for row in records if row['question'][':question/difficulty'] == ':question.difficulty/' + band]
            batch = evidence / (band + '-anchor.json')
            save(batch, selected)
            batches[band] = {'batch_file': str(batch), 'batch_hash': digest(selected),
                'count': 1, 'requested_count': 1, 'seed': 0,
                'assets': asset_hashes(selected, path.parent, self.math_root)}
        original = Path(self.state['verifier_account']['path'])
        copy = evidence / 'source-analysis.json'
        if not copy.exists():
            shutil.copy2(original, copy)
        inputs = self.exemplar_inputs()
        helper = self.root / 'generate/runs/current/check-engine'
        binding = {'policy_version': REVIEW_POLICY_VERSION, 'phase': 'exemplars',
            'source_hash': digest(read(self.directory / 'source/source.json')),
            'inventory_hash': self.state['inventory_hash'],
            'initial_source_analysis_sha256': self.state['verifier_account']['sha256'],
            'exemplar_inputs': inputs, 'verification_batches': batches,
            'engine_hash': self.engine_identity(),
            'grader_sha256': sha(helper) if helper.is_file() else None}
        return binding, batches

    def review_exemplars(self):
        from generator_pipeline import session_thread
        from generator_review import validate_exemplar_review
        if self.exemplar_gate_current():
            return True
        if not self.source_account_phase('review'):
            return False
        count = self.state.get('exemplar_review_rounds', 0)
        root = self.directory / 'verification/exemplars'
        while count < self.max_attempts * 3:
            evidence = root if count == 0 else root / ('correction-' + str(count))
            binding, batches = self.prepare_exemplar_binding(evidence)
            context = {'phase': 'exemplars', 'repo_root': str(self.root),
                'workspace': str(self.directory / 'workspace'), 'evidence_root': str(evidence),
                'knowledge_point': self.state['request']['kp'],
                'source_file': str(self.directory / 'source/source.json'),
                'inventory_file': str(self.directory / 'source/inventory.json'),
                'source_root': str(self.directory / 'source'), 'math_root': str(self.math_root),
                'investigation_account_file': str(self.required_investigation_handoff()),
                'target_account_file': self.state['target_account']['path'],
                'initial_source_analysis_file': self.state['verifier_account']['path'],
                'exemplars_file': self.state['exemplars_file'], 'review_binding': binding,
                'verification_batches': batches, 'verification_bands': list(batches),
                'python': self.environment.get('COURSE_ACADEMY_GENERATOR_PYTHON'),
                'exemplar_feedback': self.state.get('exemplar_review_error'),
                'resume_session_id': self.state.get('review_thread')}
            result = self.session_call('review', context, evidence)
            save(evidence / 'result.json', result)
            self.persist(review_thread=session_thread(evidence) or self.state.get('review_thread'))
            try:
                if result.get('verdict') != 'accepted':
                    raise ValueError('Independent exemplar review must accept all three anchors before authoring')
                if self.exemplar_inputs() != binding['exemplar_inputs']:
                    raise ValueError('Exemplars/accounts changed during review; recheck the updated exact records')
                validate_exemplar_review(result, evidence, binding)
                self.persist(exemplar_gate={'inputs': binding['exemplar_inputs'], 'binding': binding,
                    'report': str(evidence / 'result.json'), 'report_sha256': sha(evidence / 'result.json')},
                    exemplar_review_error=None)
                return True
            except (OSError, ValueError) as error:
                count += 1
                self.persist(exemplar_review_rounds=count, exemplar_review_error=str(error))
        self.block('exemplars_unverified', self.state.get('exemplar_review_error'), 'investigate')
        return False

    def seed_verifier_account(self, evidence):
        """Final review must retain the original independently checkpointed account."""
        from generator_review import validate_source_account_checkpoint
        value = self.state.get('verifier_account')
        if value:
            validate_source_account_checkpoint(value['path'], value['sha256'])
            target = Path(evidence) / 'source-analysis.json'
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                shutil.copy2(value['path'], target)

