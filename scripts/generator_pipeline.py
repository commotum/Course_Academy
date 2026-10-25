#!/usr/bin/env python3
"""Restartable investigation, authorship, verification/repair, and publication."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from inventory_jobs import save
from generator_packages import package_digest, publish_package, resolve_registered_script, check_dependencies, verify_package
from generator_review import REVIEW_POLICY_VERSION, validate_review, evidence_only_review
from generator_report_repair import generator_repair_findings, pending_report_repair
from generator_progress import failure_signature, material_identity
from generator_approval import make_approval, approved_band, ApprovalError

PHASE_POLICY_VERSION = 2
VERIFICATION_BANDS = ('easy', 'moderate', 'hard')


def read(path):
    return json.loads(Path(path).read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


class RefillNeedsReview(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


class EngineChanged(ValueError):
    pass


class RunnerChanged(RuntimeError):
    """Reload this worker after its agent repaired shared Python code."""


class SessionRetryExhausted(RuntimeError):
    def __init__(self, role, directory, execution):
        self.role, self.directory, self.execution = role, Path(directory), execution
        super().__init__(f'{role} session failed after {execution["launches"]} launches; '
                         f'workspace retained at {directory}: {execution.get("error", "interrupted")}')


def source_identity(snapshot):
    """Bind approval to instructional evidence, excluding changing pool links."""
    from generator_publish import digest as source_digest, instructional_material
    if snapshot.get('source_sha256') != source_digest(snapshot.get('material')):
        raise ValueError('Instructional source evidence failed its integrity check')
    return {**{key: snapshot[key] for key in ('database', 'lineage', 'kp_id')},
            'source_sha256': source_digest(instructional_material(snapshot['material']))}


def inside(root, name):
    path = (Path(root) / name).resolve()
    if not path.is_relative_to(Path(root).resolve()):
        raise ValueError('Artifact path escapes its workspace: ' + str(name))
    return path


def asset_hashes(records, runtime, math_root):
    """Bind reviewed diagrams and image answer choices to their actual bytes."""
    references = set()
    def visit(value):
        if isinstance(value, dict):
            if value.get(':answer/type') in (':answer.type/image', {':db/ident': ':answer.type/image'}):
                references.add(value[':answer/value'])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
        elif isinstance(value, str):
            references.update(re.findall(r'!\[[^\]]*\]\(([^)]+)\)', value))
            references.update(re.findall(r'<img\b[^>]*\bsrc=["\']([^"\']+)', value))
    visit(records)
    result = {}
    for reference in references:
        if reference.startswith('data:') or reference.startswith('<img') or reference.startswith('!['):
            # Data URLs are already covered by the batch hash; embedded images
            # have been extracted by the recursive text visitor.
            continue
        path = Path(reference)
        if not path.is_absolute():
            local = Path(runtime) / path
            if path.parts and path.parts[0] == 'images':
                canonical = Path(math_root) / path
                # New byte-addressed output is still local until publication.
                # Match ImageLibrary's canonical-first, local-fallback lookup.
                path = canonical if canonical.is_file() else local
            else:
                path = local
        result[str(path.resolve())] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def python_executable(root=ROOT, environment=None):
    env = os.environ if environment is None else environment
    return env.get('COURSE_ACADEMY_GENERATOR_PYTHON') or str(root / '.venv/bin/python' if (root / '.venv/bin/python').exists() else Path(sys.executable))


def existing_generator(kp, root=ROOT):
    """Adopt the approved draft, which can differ from the registered script."""
    manifest = root / 'generate/runs/current/manifest.json'
    if manifest.exists():
        for job in read(manifest).get('jobs', []):
            if job.get('kp_id') == kp and job.get('status') == 'qa_passed' and job.get('script'):
                path = inside(root, job['script'])
                if path.is_file():
                    return str(path)
    path = root / f'generate/scratch/{kp}.py'
    return str(path) if path.is_file() else None


class CodexSession:
    def __init__(self, root=ROOT, environment=None, timeout=3600, max_launches=3):
        self.root, self.environment, self.timeout = Path(root), dict(os.environ if environment is None else environment), timeout
        self.max_launches = max_launches

    def __call__(self, role, context, directory):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        templates = self.root / 'generate/pipeline'
        template = templates / {'investigate': 'investigator.md', 'review': 'reviewer.md', 'author': 'author.md'}[role]
        prompt = template.read_text().replace('{{context}}', json.dumps(context, indent=2))
        output = directory / 'result.json'
        # A completed structured result survives a parent crash. The caller
        # still validates its contract and the exact candidate/evidence bytes.
        if output.exists():
            try:
                return read(output)
            except json.JSONDecodeError:
                output.unlink()
        execution_path = directory / 'execution.json'
        execution = read(execution_path) if execution_path.exists() else {'launches': 0}
        from generator_lifecycle import begin_launch, credit_interruption, finish_launch
        execution = credit_interruption(execution_path, execution, self.max_launches)
        launch_limit = execution.get('launch_limit', self.max_launches)
        if execution['launches'] >= launch_limit:
            raise SessionRetryExhausted(role, directory, execution)
        (directory / 'prompt.txt').write_text(prompt)
        executable = self.environment.get('COURSE_ACADEMY_CODEX_EXECUTABLE') or shutil.which('codex', path=self.environment.get('PATH')) or str(Path.home() / '.local/bin/codex')
        resume_id = context.get('resume_session_id') or (
            execution.get('thread_id') or session_thread(directory) if execution.get('persistent_session') else None)
        command = [executable, 'exec',
                   '--sandbox', 'workspace-write', '-c', 'approval_policy="never"',
                   '-c', 'sandbox_workspace_write.network_access=true',
                   '-C', str(self.root)]
        for extra in dict.fromkeys((context['workspace'], context.get('evidence_root', directory))):
            command += ['--add-dir', str(extra)]
        if resume_id:
            command += ['resume']
        command += ['--skip-git-repo-check', '--model', 'gpt-6.1-sol',
                   '-c', 'model_reasoning_effort="high"',
                   '--output-schema', str(templates / (role + '.schema.json')),
                   '--output-last-message', str(output), '--json']
        command += [resume_id, '-'] if resume_id else ['-']
        # Count before spawning so parent/process crashes cannot reset an
        # unfinished ephemeral session's budget and launch it forever.
        execution = {**execution, 'launches': execution['launches'] + 1, 'status': 'running',
                     'persistent_session': True}
        execution.pop('error', None)
        try:
            with (directory / 'events.jsonl').open('a') as log:
                execution, process = begin_launch(execution_path, execution, self.environment,
                    lambda: subprocess.Popen(command, stdin=subprocess.PIPE, text=True, stdout=log,
                                           stderr=subprocess.STDOUT, env={
                                               **{k: v for k, v in self.environment.items() if k != 'COURSE_ACADEMY_GENERATOR_LOCK_FDS'},
                                               'PYTHONDONTWRITEBYTECODE': '1'},
                                           start_new_session=True, pass_fds=getattr(self, 'lock_fds', ())))
                try:
                    process.communicate(prompt, timeout=self.timeout)
                except BaseException:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                    raise
                if process.returncode:
                    raise subprocess.CalledProcessError(process.returncode, command)
            result = read(output)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            execution.update(thread_id=session_thread(directory) or resume_id)
            execution.update(status='failed', error=str(error))
            finish_launch(execution_path, execution)
            if execution['launches'] >= launch_limit:
                raise SessionRetryExhausted(role, directory, execution) from error
            raise
        finish_launch(execution_path, {**execution, 'status': 'completed',
                                     'thread_id': session_thread(directory) or resume_id})
        return result


def session_thread(directory):
    """Read the last started thread without loading large tool-event bodies."""
    path = Path(directory) / 'events.jsonl'
    found = None
    if path.exists():
        with path.open() as stream:
            for line in stream:
                if '"thread.started"' not in line[:120]:
                    continue
                try:
                    row = json.loads(line)
                    if row.get('type') == 'thread.started':
                        found = row.get('thread_id')
                except ValueError:
                    continue
    return found


class Pipeline:
    def __init__(self, directory, request, publisher, *, root=ROOT, environment=None,
                 session=None, max_attempts=3, investigation_preparer=None):
        self.directory, self.root = Path(directory).resolve(), Path(root).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.environment = dict(os.environ if environment is None else environment)
        self.publisher, self.session = publisher, session or CodexSession(self.root, self.environment)
        if max_attempts < 1:
            raise ValueError('max_attempts must be positive')
        self.max_attempts = max_attempts
        self.investigation_preparer = investigation_preparer
        self.runner_code_identity = self.worker_code_identity()
        inherited = json.loads(self.environment.get('COURSE_ACADEMY_GENERATOR_LOCK_FDS', '[]'))
        if not isinstance(inherited, list) or any(type(fd) is not int or fd < 0 for fd in inherited):
            raise ValueError('Inherited generator locks must be a list of file descriptors')
        for fd in inherited:
            fcntl.fcntl(fd, fcntl.F_GETFD)
        self.inherited_lock_fds = tuple(inherited)
        self.path = self.directory / 'job.json'
        if self.path.exists():
            self.state = read(self.path)
            if self.state['request'] != request:
                raise ValueError('Saved job has different inputs; use a new job directory')
        else:
            self.state = {'request': request, 'stage': 'source', 'attempt': 0, 'phase_policy_version': PHASE_POLICY_VERSION,
                          'seed': int.from_bytes(os.urandom(4), 'big'), 'created': time.time()}
            self.persist()

    def persist(self, **updates):
        self.state.update(updated=time.time(), **updates)
        save(self.path, self.state)

    def worker_code_identity(self):
        paths = sorted({path for directory in ('scripts', 'generate/pipeline', 'capture/scripts/database')
                        for path in (self.root / directory).rglob('*.py')})
        return digest({str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})

    def reload_repaired_runner(self):
        if self.worker_code_identity() != self.runner_code_identity:
            raise RunnerChanged('Shared runner code changed; resume this job with its completed agent result')

    @property
    def is_refill(self):
        return self.state['request'].get('job_kind') == 'refill'

    @property
    def math_root(self):
        return Path(self.environment.get('EDB_MATH_ROOT', '/media/jake/SSD/EDB/math'))

    def approval_path(self):
        return self.math_root / 'generators/approvals' / self.state['package_hash'] / (str(self.state['request']['kp']) + '.json')

    def review_binding(self):
        """Separate cached reviews by policy and the exact reviewed inputs."""
        return {'policy_version': REVIEW_POLICY_VERSION,
                **{key: self.state.get(key) for key in
                   ('package_hash', 'batch_hash', 'source_hash', 'inventory_hash', 'assets', 'effective_difficulty')},
                **({'engine_hash': self.state['engine_hash']} if 'engine_hash' in self.state else {}),
                'verification_batches': {band: {key: row[key] for key in ('batch_hash', 'assets', 'seed', 'count')}
                    for band, row in self.state.get('verification_batches', {}).items()}}

    def ensure_inventory(self):
        """Backfill delivery evidence for saved jobs without changing their source."""
        path = self.directory / 'source/inventory.json'
        if not path.exists():
            self.publisher.extract_inventory(self.state['request']['kp'], path.parent)
        inventory = read(path)
        source = read(self.directory / 'source/source.json')
        if any(inventory.get(key) != source.get(key) for key in ('database', 'lineage', 'kp_id')):
            raise ValueError('Delivery inventory does not match the instructional source identity')
        fingerprint = digest(inventory)
        if self.state.get('inventory_hash') not in (None, fingerprint):
            raise ValueError('Reviewed delivery inventory changed')
        if self.state.get('inventory_hash') is None:
            self.persist(inventory_hash=fingerprint)

    def review_directory(self):
        binding = digest(self.review_binding())[:16]
        return self.directory / f'review-{self.state["attempt"]}-policy-{REVIEW_POLICY_VERSION}-{binding}'

    def has_current_review(self):
        return (self.state.get('review_policy_version') == REVIEW_POLICY_VERSION
                and self.state.get('review_binding') == digest(self.review_binding())
                and ('engine_hash' not in self.state or self.state['engine_hash'] == self.engine_identity())
                and bool(self.state.get('review')))

    def validate_approved_review(self):
        if not self.has_current_review():
            raise ValueError('Generator requires a review under the current policy')
        path = Path(self.state['review'])
        review = read(path)
        validate_review(review, path.parent, self.review_binding())
        if review['verdict'] != 'accepted':
            raise ValueError('Generator publication requires an accepted review')
        return review

    def record_approval(self):
        """Persist reviewed scope only after publication has been acknowledged."""
        if self.is_refill:
            return
        self.verify_approval_inputs()
        review_path = Path(self.state['review'])
        review = self.validate_approved_review()
        if review['verdict'] != 'accepted' or not (self.state.get('publication') or {}).get('passed'):
            raise ValueError('Generator approval requires accepted review and verified publication')
        reference = self.state['registration']
        resolve_registered_script(reference, self.root, self.math_root)
        if Path(reference).parts[2] != self.state['package_hash']:
            raise ValueError('Published registration does not match the verified package')
        identity = {**source_identity(read(self.directory / 'source/source.json')),
                    'package_sha256': self.state['package_hash'], 'registration': reference}
        path = self.approval_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.with_suffix('.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            value = make_approval(identity, review, self.review_binding(), str(review_path),
                                  self.state['publication'], self.state['effective_difficulty'],
                                  REVIEW_POLICY_VERSION,
                                  publication_batch_hash=self.state.get('publication_batch_hash'))
            save(path, value)
        self.persist(verified_bands=list(VERIFICATION_BANDS))

    def refill_approval(self):
        """A hash alone is not approval: require current registration and scope."""
        snapshot = read(self.directory / 'source/source.json')
        reference = self.state['request'].get('registered_package')
        if not reference or not reference.startswith('generators/'):
            raise RefillNeedsReview('package_invalid', 'Fast refill requires an immutable registered generator package')
        if (snapshot.get('registered_generator') or {}).get(':question-generator/script') != reference:
            raise RefillNeedsReview('registration_changed', 'Requested package is no longer the registered generator')
        path = self.approval_path()
        if not path.exists():
            raise RefillNeedsReview('approval_missing', 'Registered package needs an independent review before fast refill')
        value = read(path)
        identity = {**source_identity(snapshot), 'package_sha256': self.state['package_hash'], 'registration': reference}
        try:
            return approved_band(value, identity, self.state['request']['difficulty'],
                                 REVIEW_POLICY_VERSION, self.engine_identity())
        except ApprovalError as error:
            raise RefillNeedsReview(error.code, str(error)) from error

    def load_registered_package(self, reference):
        resolve_registered_script(reference, self.root, self.math_root)
        parts = Path(reference).parts
        package = verify_package(self.math_root.joinpath(*parts[:3]), parts[2])
        workspace = self.directory / 'workspace'
        workspace.mkdir(exist_ok=True)
        for name in package.manifest['files']:
            target = inside(workspace, name)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(package.directory / name, target)
            target.chmod(target.stat().st_mode | 0o200)
        save(workspace / 'package.json', {'entrypoint': package.entrypoint,
             'files': list(package.manifest['files']), 'dependencies': package.manifest['dependencies'],
             'default_difficulty': next(iter(read(self.directory / 'source/source.json').get('available_difficulties', [])), None)})
        self.persist(manifest='package.json', package_hash=package.digest)
        return package

    def manifest(self):
        workspace = self.directory / 'workspace'
        path = inside(workspace, self.state['manifest'])
        value = read(path)
        if not isinstance(value.get('entrypoint'), str) or not isinstance(value.get('files'), list):
            raise ValueError('package.json must declare entrypoint and files')
        return path.parent, value

    def candidate_hash(self):
        root, manifest = self.manifest()
        return package_digest(root, manifest['entrypoint'], manifest['files'], dependencies=manifest.get('dependencies'))

    def interrupted_review_evidence(self, evidence):
        """Offer compatible unfinished work as evidence, never as approval."""
        current = {key: value for key, value in self.review_binding().items() if key != 'engine_hash'}
        for saved in reversed(self.state.get('review_sessions', [])):
            try:
                directory = inside(self.directory, saved)
                if directory == Path(evidence).resolve() or (directory / 'result.json').exists():
                    continue
                binding = read(directory / 'review-binding.json')
            except (OSError, ValueError):
                continue
            if not isinstance(binding, dict) or {key: value for key, value in binding.items()
                                                if key != 'engine_hash'} != current:
                continue
            if not any((directory / name).is_file() for name in ('source-analysis.json', 'session-state.md')):
                continue
            return {'directory': str(directory), 'binding': binding, 'status': 'incomplete'}
        return None

    def context(self, evidence):
        self.ensure_inventory()
        request = self.state['request']
        previous_review = self.state.get('previous_review')
        if (not previous_review or previous_review['binding'].get('source_hash') != self.state['source_hash']
                or previous_review['binding'].get('policy_version') != REVIEW_POLICY_VERSION):
            previous_review = None
        history_path = self.directory / 'repair-history.json'
        history = read(history_path) if history_path.exists() else {'findings': []}
        return {'repo_root': str(self.root), 'workspace': str(self.directory / 'workspace'),
                'source_root': str(self.directory / 'source'), 'source_file': str(self.directory / 'source/source.json'),
                'inventory_file': str(self.directory / 'source/inventory.json'),
                'publisher_file': str(self.root / 'scripts/generator_publish.py'),
                'question_selection_file': str(self.root / 'engine/rust/question_selection.rs'),
                'publication_file': str(self.directory / 'publication/preparation.json'),
                'existing_entrypoint': request.get('existing_entrypoint'),
                'feedback_file': str(self.directory / 'feedback.json') if (self.directory / 'feedback.json').exists() else None,
                'previous_review': previous_review,
                'interrupted_review': self.interrupted_review_evidence(evidence), 'evidence_root': str(evidence),
                'package_root': str((self.directory / 'workspace' / self.state.get('manifest', 'package.json')).parent),
                'manifest_file': str(self.directory / 'workspace' / self.state.get('manifest', 'package.json')),
                'requested_difficulty': self.state.get('effective_difficulty', request['difficulty']), 'count': request['count'],
                'sample_seed': self.state['seed'],
                'knowledge_point': request['kp'], 'python': python_executable(self.root, self.environment),
                'review_policy_version': REVIEW_POLICY_VERSION, 'review_binding': self.review_binding(),
                'math_root': self.environment.get('EDB_MATH_ROOT', '/media/jake/SSD/EDB/math'),
                'batch_file': str(self.directory / 'samples.json'),
                'verification_bands': list(VERIFICATION_BANDS),
                'verification_batches': self.state.get('verification_batches', {}),
                'sampling_errors': self.state.get('sampling_errors', {}),
                'prior_verification': self.state.get('prior_verification'),
                'repair_history_file': str(self.directory / 'repair-history.json'),
                'repair_mode': 'root_cause' if self.state.get('repair_cycle', 0) or self.state.get('repeated_candidate') else 'targeted',
                'repair_regressions_file': str(self.directory / 'workspace/repair-regressions.json'),
                'repair_preflight_file': str(self.directory / 'repair-preflight.json'),
                'engine_repair_allowed': True,
                'investigation_file': self.state.get('investigation_file'),
                'investigation_result': self.state.get('investigation_result'),
                'exemplars_file': self.state.get('exemplars_file'),
                'assets_directory': self.state.get('assets_directory'),
                'finalize_review_command': [python_executable(self.root, self.environment),
                    str(self.root / 'scripts/finalize_generator_review.py'), '--job', str(self.directory),
                    '--evidence-root', str(evidence)],
                'shared_repair_command': [python_executable(self.root, self.environment),
                    str(self.root / 'scripts/generator_shared_repair.py')]}

    def investigate(self):
        """Let one investigator finish the source account and publish its examples."""
        from generator_investigation import prepare_investigation
        evidence = self.directory / 'investigation'
        evidence.mkdir(exist_ok=True)
        source = read(self.directory / 'source/source.json')
        prepare = self.investigation_preparer or prepare_investigation
        prepared = prepare(self.publisher, source, evidence)
        self.persist(investigation_file=prepared.get('investigation_file'))
        attempts = self.state.get('investigation_rounds', 0)
        while attempts < self.max_attempts:
            directory = evidence if attempts == 0 else evidence / f'correction-{attempts}'
            context = {**self.context(evidence), **prepared,
                       'investigation_feedback': self.state.get('investigation_error')}
            if attempts:
                context['resume_session_id'] = session_thread(evidence)
            result = self.session('investigate', context, directory)
            save(directory / 'result.json', result)
            self.reload_repaired_runner()
            if result.get('status') != 'ready':
                error = {'error': 'Finish the investigation and construct the missing examples using the supplied reference. Repair relevant tools yourself.',
                         'result': result}
            else:
                try:
                    filename = result.get('exemplars_file')
                    if prepared.get('needs_exemplars') and not filename:
                        raise ValueError('This source needs three complete exemplar questions; save exemplars_file before returning ready')
                    if filename:
                        path = inside(self.directory / 'workspace', filename)
                        records = read(path)
                        if isinstance(records, dict):
                            records = records.get('records', records.get('questions'))
                        from generator_publish import StaleBasis
                        for publication_attempt in range(6):
                            try:
                                published = self.publisher.publish_exemplars(self.state['request']['kp'], records,
                                    evidence / 'publication', assets_directory=path.parent)
                                break
                            except StaleBasis:
                                if publication_attempt == 5:
                                    raise
                        # This is a separate normal question publication, attributed
                        # to the investigator. Original imports stay untouched.
                        save(evidence / 'published-exemplars.json', published['questions'])
                        save(self.directory / 'source/source.json', published['fresh_source'])
                        self.publisher.extract_inventory(self.state['request']['kp'], self.directory / 'source')
                        self.persist(exemplars_file=str(evidence / 'published-exemplars.json'),
                                     exemplar_publication={k: v for k, v in published.items()
                                                           if k not in {'questions', 'fresh_source'}},
                                     source_hash=digest(published['fresh_source']), inventory_hash=None)
                    self.persist(stage='sample' if self.state['request'].get('review_existing') and self.state.get('manifest') else 'generate', investigation_result=str(directory / 'result.json'),
                                 investigation_complete=True, phase_policy_version=PHASE_POLICY_VERSION,
                                 investigation_error=None)
                    return
                except (OSError, ValueError) as invalid:
                    # Never replace an unresolved database request. The publisher
                    # recovers it before evaluating any fresh exemplar proposal.
                    error = {'error': str(invalid), 'instruction': 'Correct the exemplar records or helper, then finish the same investigation. Do not edit imported questions.'}
            attempts += 1
            self.persist(investigation_rounds=attempts, investigation_error=error)
            save(evidence / 'feedback.json', error)
        self.block('investigation_unfinished', error, 'investigate')

    def finalize_review(self, evidence):
        """Refresh final bytes before the verifier checks and accepts its repair."""
        evidence = inside(self.directory, evidence)
        previous_hash = self.state.get('publication_package_hash') or self.state.get('package_hash')
        if (self.state.get('publication') or {}).get('passed') and not self.state.get('publication_batch_hash'):
            self.persist(publication_batch_hash=self.state['batch_hash'])
        self.check_repair_regressions()
        self.sample()
        candidate = self.candidate_hash()
        if self.state.get('review_after_publication') and candidate != previous_hash:
            publication = self.directory / 'publication'
            if not (publication / 'verification.json').exists() and not (self.state.get('publication') or {}).get('passed'):
                raise ValueError('Recover the existing publication before repairing a published package')
            if publication.exists():
                publication.rename(self.directory / ('publication-before-repair-' + str(time.time_ns())))
            self.persist(review_after_publication=False, publication=None, registration=None, publication_batch_hash=None, publication_package_hash=None)
        self.persist(package_hash=candidate, stage='validate', approval_recorded=False)
        self.ensure_inventory()
        binding = self.review_binding()
        save(evidence / 'final-binding.json', binding)
        return {'binding': binding, 'batch_file': str(self.directory / 'samples.json'),
                'assets_directory': self.state['assets_directory'],
                'verification_batches': self.state['verification_batches'],
                'instruction': 'Check every final easy/moderate/hard batch, including delivery, grading, visible rendering, and progression, before returning accepted.'}

    def refresh_engine_review(self):
        """Refresh changed grading evidence while keeping its verifier thread."""
        active = (self.state.get('active_review_directory') or self.state.get('report_repair_directory')
                  or (str(Path(self.state['review']).parent) if self.state.get('review') else None))
        self.sample(tolerate_failures=True)
        if not active:
            return
        evidence = inside(self.directory, active)
        path = evidence / 'review-binding.json'
        if path.exists():
            save(evidence / ('engine-binding-before-' + str(time.time_ns()) + '.json'), read(path))
        save(path, self.review_binding())
        rounds = self.state.get('review_report_rounds', {})
        if (evidence / 'result.json').exists():
            count = max(1, rounds.get(str(evidence), 0))
            while (evidence / ('contract-repair' if count == 1 else f'contract-repair-{count}') / 'result.json').exists():
                count += 1
            rounds[str(evidence)] = count
        self.persist(active_review_directory=str(evidence), report_repair_directory=str(evidence),
                     review_report_rounds=rounds,
                     review_report_error={'error': 'The shared engine changed since these checks.',
                         'instruction': 'Continue your verification, finalize again, and rerun grading and affected checks against the current engine.'})

    def review_candidate(self, evidence):
        """Keep verification, repairs, and report corrections with one agent."""
        evidence.mkdir(parents=True, exist_ok=True)
        binding_path = evidence / 'review-binding.json'
        binding = self.review_binding()
        recorded = read(binding_path) if binding_path.exists() else None
        finalized = read(evidence / 'final-binding.json') if (evidence / 'final-binding.json').exists() else None
        if recorded is not None and recorded != binding and finalized != binding:
            if self.state.get('report_repair_directory'):
                self.persist(stage='validate', report_repair_directory=None,
                             review_report_error=None, review_report_result_file=None)
            else:
                self.block('review_binding_changed', {'evidence_root': str(evidence),
                           'expected': binding, 'recorded': recorded}, 'validate')
            return None
        if recorded is None and (evidence / 'result.json').exists():
            self.block('review_binding_missing', {'evidence_root': str(evidence),
                       'error': 'Cached review has no saved binding to current inputs.'}, 'validate')
            return None
        if recorded is None:
            save(binding_path, binding)
        rounds = self.state.get('review_report_rounds', {})
        count = rounds.get(str(evidence), 0)
        limit = self.state.get('review_report_limits', {}).get(str(evidence), self.max_attempts * 3)
        error = self.state.get('review_report_error')
        while count < limit:
            directory = evidence if count == 0 else evidence / ('contract-repair' if count == 1 else f'contract-repair-{count}')
            context = self.context(evidence)
            if error:
                context['review_contract_feedback'] = {
                    'error': error, 'result_file': self.state.get('review_report_result_file', str(evidence / 'result.json')),
                    'instruction': 'Finish the repair yourself, including relevant shared tools or engine. Finalize the package, check the final batch and correct your report before returning accepted.'}
                context['resume_session_id'] = session_thread(evidence)
            if not self.admit_review_session(directory):
                return None
            self.persist(active_review_directory=str(evidence))
            result = self.session('review', context, directory)
            save(directory / 'result.json', result)
            self.reload_repaired_runner()
            # The verifier's finalization helper may have resampled and saved
            # new package/asset/engine identities during this same session.
            self.state = read(self.path)
            try:
                self.verify_approval_inputs()
                if result.get('verdict') == 'accepted':
                    final_path = evidence / 'final-binding.json'
                    if not final_path.exists() or read(final_path) != self.review_binding():
                        raise ValueError('Run finalize_review_command, check its final batch, then return acceptance bound to final-binding.json.')
                validate_review(result, evidence, self.review_binding())
            except EngineChanged:
                self.sample(tolerate_failures=True)
                save(binding_path, self.review_binding())
                error = {'error': 'The shared engine changed during verification.',
                         'instruction': 'Continue this same verification session: finalize again and rerun grading plus checks affected by the engine repair.'}
            except (OSError, ValueError) as invalid:
                error = str(invalid)
            else:
                self.persist(previous_review={'directory': str(evidence), 'binding': self.review_binding()})
                if result['verdict'] == 'accepted':
                    save(evidence / 'result.json', result)
                    save(binding_path, self.review_binding())
                    self.persist(review_report_error=None, review_report_result_file=None,
                                 report_repair_directory=None, active_review_directory=None)
                    return result
                self.remember_repair(result)
                error = {'code': 'verification_unfinished', 'findings': result.get('findings', []),
                         'instruction': 'Repair and recheck in this verification session. Incomplete imports are observations, never repair obligations. Earlier requirements may be revised with evidence.'}
            count += 1
            rounds[str(evidence)] = count
            self.persist(review_report_rounds=rounds, review_report_error=error,
                         report_repair_directory=str(evidence),
                         review_report_result_file=str(directory / 'result.json'))
            save(evidence / 'contract-feedback.json', {'error': error, 'correction': count})
        self.block('verification_unfinished', {
            'error': error, 'evidence_root': str(evidence), 'rounds': count,
            'details': 'Verification did not converge within its durable session budget; completed work and exact failure are retained.'}, 'validate')
        return None

    def recover_report_handoff(self):
        """Recover an old evidence-only rejection without another author pass."""
        history = self.directory / 'repair-history.json'
        if not history.exists():
            return False
        pending = pending_report_repair(self.state, read(history), self.review_binding())
        if not pending:
            return False
        try:
            self.verify_approval_inputs()
        except EngineChanged:
            self.sample()
            self.persist(stage='validate', author_running=False)
            return True
        except (OSError, ValueError):
            return False
        evidence = inside(self.directory, pending['directory'])
        rounds = self.state.get('review_report_rounds', {})
        # The old root verdict is already known to require a correction. Move
        # past its cached result, preserving existing correction launch counts.
        rounds[str(evidence)] = max(1, rounds.get(str(evidence), 0))
        self.persist(stage='validate', report_repair_directory=str(evidence),
                     review_report_rounds=rounds, author_running=False,
                     review_report_error=pending['reason'],
                     review_report_result_file=str(evidence / 'result.json'))
        return True

    def sample(self, *, tolerate_failures=False):
        source, manifest = self.manifest()
        difficulty = self.state['request']['difficulty']
        if difficulty == 'unclassified':
            difficulty = manifest.get('default_difficulty')
            if difficulty is None:
                bands = read(self.directory / 'source/source.json').get('available_difficulties', [])
                if len(bands) == 1 and bands[0] in {'easy', 'moderate', 'hard'}:
                    difficulty = bands[0]
                    manifest['default_difficulty'] = difficulty
                    save(self.directory / 'workspace' / self.state['manifest'], manifest)
            if difficulty not in {'easy', 'moderate', 'hard'}:
                raise ValueError('Classification requires a source-justified default_difficulty in package.json')
        self.persist(effective_difficulty=difficulty)
        bands = (difficulty,) if self.is_refill else VERIFICATION_BANDS
        batches, errors = {}, {}
        for index, band in enumerate(bands):
            primary = band == difficulty
            seed = self.state['seed'] if primary else (self.state['seed'] + index + 1) % (2 ** 32)
            count = self.state['request']['count'] if primary else max(5, self.state['request']['count'])
            try:
                batches[band] = self.sample_band(source, manifest, band, count, seed,
                                                 '' if primary else '-' + band)
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                if not tolerate_failures:
                    raise
                errors[band] = str(error)
        primary = batches.get(difficulty)
        if primary is None:
            # A broken catch-up package belongs to the verifier. This explicit
            # empty placeholder cannot be approved: finalization must produce
            # every complete batch before the report contract can pass.
            path = self.directory / 'samples.json'
            save(path, [])
            primary = {'batch_hash': digest([]), 'runtime': str(self.directory / f'runtime-{self.state["attempt"]}'),
                       'assets_directory': str(self.directory / f'outputs-{self.state["attempt"]}'), 'assets': {}}

        self.persist(batch_hash=primary['batch_hash'], runtime=primary['runtime'],
                     assets_directory=primary['assets_directory'], assets=primary['assets'],
                     engine_hash=self.engine_identity(), verification_batches={} if self.is_refill else batches,
                     sampling_errors=errors,
                     report_repair_directory=None, review_report_error=None, review_report_result_file=None)

    def sample_band(self, source, manifest, difficulty, count, seed, suffix):
        runtime = self.directory / f'runtime-{self.state["attempt"]}{suffix}'
        if runtime.exists():
            shutil.rmtree(runtime)
        runtime.mkdir(exist_ok=True)
        output = self.directory / f'outputs-{self.state["attempt"]}{suffix}'
        if output.exists():
            shutil.rmtree(output)
        for name in manifest['files']:
            destination = inside(runtime, name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(inside(source, name), destination)
        command = [python_executable(self.root, self.environment), '-E', '-s', '-B', str(inside(runtime, manifest['entrypoint'])),
                   '--difficulty', difficulty, '--count', str(count),
                   '--seed', str(seed), '--format', 'json']
        env = {**self.environment, 'PYTHONDONTWRITEBYTECODE': '1', 'MPLBACKEND': 'Agg',
               'COURSE_ACADEMY_REPO_ROOT': str(self.root),
               'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR': str(output)}
        dependencies = check_dependencies(manifest.get('dependencies', {}), command[0], environment=env)
        save(self.directory / 'runtime-dependencies.json', dependencies)
        outputs = []
        images = []
        for _ in range(2):
            result = subprocess.run(command, cwd=runtime, env=env, capture_output=True, text=True, timeout=180, check=False)
            (runtime / f'run-{len(outputs)}.stderr').write_text(result.stderr)
            (runtime / f'run-{len(outputs)}.stdout').write_text(result.stdout)
            if result.returncode:
                raise ValueError(f'Generator exited {result.returncode}; {runtime}/run-{len(outputs)}.stderr:\n' + result.stderr[-4000:])
            outputs.append(json.loads(result.stdout))
            images.append(asset_hashes(outputs[-1], output, self.environment.get('EDB_MATH_ROOT', '/media/jake/SSD/EDB/math')))
        if outputs[0] != outputs[1] or images[0] != images[1]:
            raise ValueError('Generator is not deterministic for the saved seed')
        records = outputs[0]
        if isinstance(records, dict):
            records = records.get('records', records.get('questions', [records] if 'question' in records else None))
        if not isinstance(records, list) or len(records) != count:
            raise ValueError('Generator must return exactly the requested number of records; report finite limits explicitly')
        if any(not isinstance(r, dict) or not isinstance(r.get('question'), dict) for r in records):
            raise ValueError('Each generated record must contain a question object')
        for record in records:
            band = record['question'].get(':question/difficulty')
            if isinstance(band, dict):
                band = band.get(':db/ident')
            if band != ':question.difficulty/' + difficulty:
                raise ValueError('Generated question is in the wrong difficulty band')
        if self.candidate_hash() != package_digest(runtime, manifest['entrypoint'], manifest['files'], dependencies=manifest.get('dependencies')):
            raise ValueError('Running generator modified its declared package files')
        batch_file = self.directory / ('samples' + suffix + '.json')
        save(batch_file, records)
        return {'batch_file': str(batch_file), 'batch_hash': digest(records),
                'runtime': str(runtime), 'assets_directory': str(output), 'seed': seed, 'count': count,
                'assets': asset_hashes(records, output, self.math_root)}

    def verify_approval_inputs(self):
        if self.candidate_hash() != self.state['package_hash'] or digest(read(self.directory / 'samples.json')) != self.state['batch_hash']:
            raise ValueError('Reviewed package or publication batch changed')
        if digest(read(self.directory / 'source/source.json')) != self.state['source_hash']:
            raise ValueError('Reviewed source snapshot changed')
        if (self.state.get('inventory_hash') is not None
                and digest(read(self.directory / 'source/inventory.json')) != self.state['inventory_hash']):
            raise ValueError('Reviewed delivery inventory changed')
        if any(hashlib.sha256(Path(path).read_bytes()).hexdigest() != sha for path, sha in self.state['assets'].items()):
            raise ValueError('Reviewed image bytes changed')
        for band, batch in self.state.get('verification_batches', {}).items():
            if digest(read(batch['batch_file'])) != batch['batch_hash']:
                raise ValueError('Reviewed ' + band + ' verification batch changed')
            if any(hashlib.sha256(Path(path).read_bytes()).hexdigest() != sha
                   for path, sha in batch['assets'].items()):
                raise ValueError('Reviewed ' + band + ' image bytes changed')
        _, manifest = self.manifest()
        observed = check_dependencies(manifest['dependencies'], python_executable(self.root, self.environment), environment=self.environment)
        if observed != read(self.directory / 'runtime-dependencies.json'):
            raise ValueError('Runtime dependencies changed after generation')
        if self.state.get('engine_hash') is not None and self.state['engine_hash'] != self.engine_identity():
            raise EngineChanged('Grading engine changed after sampling; a fresh independent review is required')
        if self.is_refill:
            resolve_registered_script(self.state['request']['registered_package'], self.root, self.math_root)
            if digest(self.refill_approval()) != self.state['approval_hash']:
                raise ValueError('Registered generator approval changed during refill')

    def publication_records(self):
        return read(self.directory / 'samples.json')

    def engine_identity(self):
        paths = list((self.root / 'engine/rust').rglob('*.rs'))
        helper = self.root / 'generate/runs/current/check-engine'
        if helper.is_file():
            paths.append(helper)
        return digest({str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})

    def remember_repair(self, reason):
        """Keep every finding across attempts, rather than replacing the task."""
        path = self.directory / 'repair-history.json'
        history = read(path) if path.exists() else {'format': 1, 'findings': [], 'events': []}
        review = self.state.get('previous_review', {}).get('directory')
        for finding in reason.get('findings', []):
            identity = {**finding, 'source_hash': self.state.get('source_hash')}
            key = digest(identity)[:20]
            if not any(row['id'] == key for row in history['findings']):
                history['findings'].append({'id': key, 'finding': finding,
                    'source_hash': self.state.get('source_hash'), 'review_directory': review,
                    'attempt': self.state['attempt']})
        event = {'attempt': self.state['attempt'], 'package_hash': self.state.get('package_hash'),
                 'reason': reason, 'review_directory': review}
        if not history['events'] or history['events'][-1] != event:
            history['events'].append(event)
        save(path, history)
        return history

    def check_repair_regressions(self):
        """Run retained counterexamples before spending another full review."""
        history = self.directory / 'repair-history.json'
        required = generator_repair_findings(read(history)) if history.exists() else []
        if not required:
            return
        root = self.directory / 'workspace'
        manifest = read(root / 'repair-regressions.json')
        rows = manifest.get('findings', [])
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise ValueError('repair-regressions.json must list finding IDs and executable Python checks')
        by_id = {row.get('id'): row for row in rows}
        missing = [row['id'] for row in required if row['id'] not in by_id]
        if missing:
            raise ValueError('Missing retained regression checks for findings: ' + ', '.join(missing))
        before = self.candidate_hash()
        results, commands = [], set()
        for finding in required:
            row = by_id[finding['id']]
            script = inside(root, row.get('script', ''))
            args = row.get('args', [])
            if not script.is_file() or script.suffix != '.py' or not isinstance(args, list) or any(not isinstance(a, str) for a in args):
                raise ValueError('Repair regression must name a workspace Python script and string arguments')
            command = (str(script), *args)
            if command in commands:
                continue
            commands.add(command)
            result = subprocess.run([python_executable(self.root, self.environment), '-E', '-s', '-B', *command],
                cwd=root, env={**self.environment, 'PYTHONDONTWRITEBYTECODE': '1'},
                capture_output=True, text=True, timeout=180)
            results.append({'script': str(script.relative_to(root)), 'args': args,
                'sha256': hashlib.sha256(script.read_bytes()).hexdigest(),
                'exit_code': result.returncode, 'stdout': result.stdout[-4000:], 'stderr': result.stderr[-4000:]})
            save(self.directory / 'repair-preflight.json', {'passed': result.returncode == 0,
                'finding_ids': [f['id'] for f in required], 'checks': results})
            if result.returncode:
                raise ValueError('Retained repair regression failed: ' + str(script) + '\n' + result.stderr[-2000:])
        if self.candidate_hash() != before:
            raise ValueError('Repair checks modified the runtime package')

    def repair_inventory(self, evidence=None):
        from generator_inventory import repair_inventory
        return repair_inventory(self, evidence)

    def block_inventory(self, result):
        self.block('inventory_repair_blocked', {
            'owner': 'inventory',
            'error': 'Stored-question repair needs intervention; see pool-repair/verification.json.',
            'unresolved': result.get('unresolved', [])}, 'validate')

    def repair(self, reason):
        findings = reason.get('findings', [])
        if any(row.get('kind') == 'inventory' for row in findings):
            self.remember_repair(reason)
            # Imported incompleteness and historical observations never create
            # a database-repair prerequisite for this generator.
            content = [row for row in findings if row.get('kind') != 'inventory']
            if not content:
                self.persist(stage='validate', needs_repair=True, error=None)
                return
            reason = {**reason, 'findings': content}

        self.remember_repair(reason)
        save(self.directory / 'feedback.json', {**reason,
            'repair_history_file': str(self.directory / 'repair-history.json'),
            'instruction': 'Fix the concrete generator defect, retain earlier counterexamples, and declare executable checks in repair-regressions.json. Repair relevant shared tools, policy or engine yourself, and verify the result; earlier requirements may be corrected with evidence.'})
        if self.is_refill or self.state.get('review_after_publication'):
            self.persist(stage='unsupported', needs_repair=True, error=reason)
        else:
            updates = {'last_rejected_package': self.state.get('package_hash'),
                       'last_rejected_source': self.state.get('source_hash'),
                       'last_rejected_engine': self.engine_identity()} if reason.get('verdict') in {'revise', 'unsupported'} else {}
            signature = failure_signature(reason, material_identity(self))
            failures = self.state.get('progress_failures', {})
            failures[signature] = failures.get(signature, 0) + 1
            self.persist(progress_failures=failures)
            if failures[signature] >= 2:
                self.block('no_progress', reason, 'generate')
                return
            self.persist(stage='generate', needs_repair=True, error=reason, **updates)

    def admit_publication(self):
        """Recheck saved approvals before making any new publication intent."""
        try:
            self.verify_approval_inputs()
            if not self.is_refill:
                if not self.has_current_review():
                    self.persist(stage='validate')
                    return False
                self.validate_approved_review()
        except EngineChanged:
            if self.is_refill:
                self.repair({'code': 'engine_changed', 'error': 'Grading engine changed during refill; independent review is required.'})
                return False
            self.refresh_engine_review()
            self.persist(stage='validate')
            return False
        except (ValueError, FileNotFoundError) as error:
            if not self.is_refill:
                raise
            self.repair({'code': getattr(error, 'code', 'generator_failed'), 'error': str(error)})
            return False
        return True

    def admit_review_session(self, directory):
        """Count a new review before launch, across every evidence binding."""
        if self.state['stage'] == 'blocked':
            return False
        identity = str(inside(self.directory, directory))
        sessions = self.state.get('review_sessions', [])
        if identity in sessions:
            # Retries and cached results retain their per-session launch cap.
            return True
        limit = self.state.get('review_session_limit', self.max_attempts * 3)
        if len(sessions) >= limit:
            self.block('review_sessions_exhausted', {
                'sessions': len(sessions), 'limit': limit, 'next_directory': identity,
                'error': 'Independent reviews exhausted the durable job budget, including evidence or engine refreshes.'}, 'validate')
            return False
        self.persist(review_sessions=[*sessions, identity], review_session_limit=limit)
        return True

    def block(self, code, reason, resume_stage):
        self.persist(stage='blocked', needs_repair=True,
                     repair_cycle=self.state.get('repair_cycle', 0) + 1, error={
            'code': code, 'cause': reason, 'resume_stage': resume_stage,
            'instruction': 'Resolve the recorded cause, then explicitly resume with --resume-reason. Automatic retries are disabled.'})

    def resume_blocked(self, reason):
        """Grant one recorded, bounded recovery; a process restart grants none."""
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError('An explicit resume requires a nonempty reason')
        if self.state['stage'] not in {'blocked', 'failed', 'unsupported', 'repair', 'report-repair'}:
            raise ValueError('Only a blocked or yielded repair can be explicitly resumed')
        error = self.state.get('error') or {}
        prior_stage = self.state['stage']
        stage = error.get('resume_stage') if isinstance(error, dict) else None
        stage = stage or ('validate' if prior_stage == 'report-repair' else 'generate')
        cause = error.get('cause', error) if isinstance(error, dict) else {}
        if isinstance(cause, dict) and cause.get('code') == 'agent_session_retry_exhausted':
            execution_path = inside(self.directory, cause['session_directory']) / 'execution.json'
            execution = read(execution_path)
            save(execution_path, {**execution, 'launch_limit': execution['launches'] + getattr(self.session, 'max_launches', 3)})
        events = self.state.get('resume_events', [])
        events.append({'time': time.time(), 'reason': reason.strip(), 'attempt': self.state['attempt'],
                       'prior_stage': prior_stage, 'prior_error': error,
                       'material': material_identity(self)})
        report_limits = {key: count + 3 for key, count in self.state.get('review_report_rounds', {}).items()}
        self.persist(stage=stage, author_attempt_limit=self.state['attempt'] + self.max_attempts,
                     resume_events=events, progress_failures={}, review_report_limits=report_limits,
                     review_session_limit=len(self.state.get('review_sessions', [])) + self.max_attempts * 3,
                     needs_repair=True)

    def run(self, stop_after='push', *, resume_reason=None):
        with (self.directory / 'worker.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # A caller may have constructed this object before another worker
            # finished. Always make launch decisions from the locked state.
            self.state = read(self.path)
            self.upgrade_phases()
            if isinstance(self.session, CodexSession):
                self.session.lock_fds = (*getattr(self, 'inherited_lock_fds', ()), lock.fileno())
            if 'author_attempt_limit' not in self.state:
                # Existing attempts count, including jobs admitted by older
                # runners. A deployment must not rearm a runaway job.
                self.persist(author_attempt_limit=self.max_attempts)
            if 'review_session_limit' not in self.state:
                self.persist(review_session_limit=self.max_attempts * 3,
                             review_sessions=self.state.get('review_sessions', []))
            if resume_reason is not None:
                self.resume_blocked(resume_reason)
            self._attempt_limit = self.state['author_attempt_limit']
            try:
                return self._run(stop_after)
            except SessionRetryExhausted as error:
                reason = {'code': 'agent_session_retry_exhausted', 'role': error.role,
                          'session_directory': str(error.directory), 'launches': error.execution['launches'],
                          'error': error.execution.get('error', 'Session was interrupted')}
                self.block('agent_session_retry_exhausted', reason, self.state['stage'])
                return self.state

    def upgrade_phases(self):
        """One evidence-changing migration; retain drafts and unresolved writes."""
        if self.is_refill or self.state.get('phase_policy_version', 0) >= PHASE_POLICY_VERSION:
            return
        if self.state['stage'] == 'verified' or (self.directory / 'publication/request.json').exists():
            return
        save(self.directory / 'job-before-three-phase.json', self.state)
        source = self.directory / 'source/source.json'
        if source.exists():
            save(source.with_name('source-before-three-phase.json'), read(source))
            fresh = self.publisher.extract_source(self.state['request']['kp'], source.parent)
            save(source, fresh)
        self.persist(stage='source', phase_policy_version=PHASE_POLICY_VERSION,
                     author_running=False, investigation_complete=False, inventory_hash=None,
                     review=None, review_binding=None, review_policy_version=None,
                     review_after_publication=False, approval_recorded=False,
                     report_repair_directory=None, review_report_error=None,
                     active_review_directory=None,
                     error=None, progress_failures={},
                     author_attempt_limit=self.state['attempt'] + self.max_attempts,
                     review_session_limit=len(self.state.get('review_sessions', [])) + self.max_attempts * 3)

    def upgrade_verification(self):
        """Resume saved single-band work in its verifier, never grant new bands."""
        if self.is_refill or self.state.get('verification_policy_version') == REVIEW_POLICY_VERSION:
            return
        if self.state['stage'] not in {'validate', 'prepare', 'verified'}:
            return
        previous = self.state.get('review')
        active = self.state.get('active_review_directory') or self.state.get('report_repair_directory')
        if self.state.get('publication') and self.state['publication'].get('passed'):
            self.persist(publication_batch_hash=self.state.get('publication_batch_hash', self.state.get('batch_hash')),
                         publication_package_hash=self.state.get('publication_package_hash') or self.state.get('package_hash'))
        # A new sample checkpoint already contains all bands. Old saved jobs do
        # not, so sample them once without authoring or publishing again.
        extending_scope = (set(self.state.get('verification_batches', {})) != set(VERIFICATION_BANDS)
                           or bool(previous) and self.state.get('review_policy_version') != REVIEW_POLICY_VERSION)
        if set(self.state.get('verification_batches', {})) != set(VERIFICATION_BANDS):
            self.sample(tolerate_failures=True)
        self.persist(package_hash=self.candidate_hash())
        updates = {'verification_policy_version': REVIEW_POLICY_VERSION}
        if extending_scope:
            updates.update(review_session_limit=max(self.state.get('review_session_limit', 0),
                                len(self.state.get('review_sessions', [])) + 3),
                           verification_upgrade={'policy': REVIEW_POLICY_VERSION, 'time': time.time(),
                               'reason': 'One bounded catch-up allowance for newly required difficulty bands.'})
        if previous:
            updates['prior_verification'] = previous
        if active:
            evidence = inside(self.directory, active)
            path = evidence / 'review-binding.json'
            if path.exists():
                save(evidence / ('binding-before-all-bands-' + str(time.time_ns()) + '.json'), read(path))
            save(path, self.review_binding())
            rounds = self.state.get('review_report_rounds', {})
            count = max(1, rounds.get(str(evidence), 0))
            while (evidence / ('contract-repair' if count == 1 else f'contract-repair-{count}') / 'result.json').exists():
                count += 1
            rounds[str(evidence)] = count
            if extending_scope:
                limits = self.state.get('review_report_limits', {})
                limits[str(evidence)] = max(limits.get(str(evidence), self.max_attempts * 3), count + 3)
                updates['review_report_limits'] = limits
            updates.update(active_review_directory=str(evidence), report_repair_directory=str(evidence),
                review_report_rounds=rounds,
                review_report_error={'error': 'Verification now covers easy, moderate and hard together.',
                    'instruction': 'Reuse your investigation and checks, test and repair all three final batches, check progression, and finalize again. Earlier single-band acceptance is evidence, not all-band approval.'})
        self.persist(**updates)

    def reuse_completed_work(self):
        """Adopt same-package investigation and authored workspace for catch-up."""
        previous = self.state['request'].get('reuse_pipeline')
        if not previous:
            return False
        directory = Path(previous).resolve()
        prior = read(directory / 'job.json')
        if (prior.get('stage') != 'verified' or prior['request']['kp'] != self.state['request']['kp']
                or prior.get('registration') != self.state['request'].get('registered_package')
                or not prior.get('investigation_complete')
                or source_identity(read(directory / 'source/source.json')) != source_identity(read(self.directory / 'source/source.json'))):
            return False
        old_workspace = directory / 'workspace'
        if not old_workspace.is_dir():
            return False
        shutil.copytree(old_workspace, self.directory / 'workspace', dirs_exist_ok=True)
        self.persist(manifest=prior['manifest'])
        if self.candidate_hash() != prior.get('package_hash'):
            # A retained workspace can have later edits; reload the immutable
            # registered version rather than trusting those unreviewed bytes.
            self.load_registered_package(prior['registration'])
        self.persist(stage='sample', investigation_complete=True,
                     investigation_file=prior.get('investigation_file'),
                     investigation_result=prior.get('investigation_result'),
                     exemplars_file=prior.get('exemplars_file'),
                     reused_pipeline=str(directory), prior_verification=prior.get('review'))
        return True

    def _run(self, stop_after):
        stale_retries = 0
        while True:
            stage = self.state['stage']
            publication = self.directory / 'publication'
            if (stage in {'source', 'investigate', 'generate', 'sample', 'repair', 'report-repair', 'failed', 'validate', 'prepare'}
                    and not self.state.get('review_after_publication')
                    and (publication / 'request.json').exists()):
                # A durable intent can already have committed. Resolve its exact
                # bytes before policy upgrades, review, or authoring touch inputs.
                self.persist(stage='push')
                continue
            source_path=self.directory/'source/source.json'
            if stage in {'source','investigate','generate','sample','validate','prepare','refill','repair','report-repair'} and source_path.exists():
                from generator_source_policy import POLICY_VERSION
                saved_source=read(source_path)
                if saved_source.get('material',{}).get('source_eligibility',{}).get('policy_version')!=POLICY_VERSION:
                    # Pending durable submissions were routed to recovery above.
                    # Archive old evidence; never silently review a stale pool.
                    archive=self.directory/'source/source-before-eligibility.json'
                    if not archive.exists():save(archive,saved_source)
                    fresh=self.publisher.extract_source(self.state['request']['kp'],source_path.parent)
                    if fresh.get('material',{}).get('source_eligibility',{}).get('policy_version')!=POLICY_VERSION:
                        raise ValueError('Source extractor did not establish current standalone eligibility')
                    request=dict(self.state['request'])
                    registered=(fresh.get('registered_generator') or {}).get(':question-generator/script')
                    if request.get('registered_package') and registered and registered.startswith('generators/'):
                        request['registered_package']=registered
                    next_stage='validate' if self.state.get('review_after_publication') else 'source'
                    self.persist(stage=next_stage,request=request,source_hash=digest(fresh),inventory_hash=None,
                                 review=None,review_binding=None,review_policy_version=None,approval_recorded=False,
                                 source_eligibility_refreshed=True)
                    continue
            self.upgrade_verification()
            error = self.state.get('error')
            if stage == 'failed' and isinstance(error, dict) and error.get('code') == 'review_contract_invalid':
                rounds = self.state.get('review_report_rounds', {})
                rounds.setdefault(str(self.review_directory()), 2)
                self.persist(stage='report-repair', review_report_rounds=rounds,
                             review_report_error=error.get('error'))
                continue
            if stage == 'repair':
                self.persist(stage='generate')
                continue
            if stage == 'report-repair':
                self.persist(stage='validate')
                continue
            if stage in {'verified', 'failed', 'unsupported', 'blocked'}:
                if stage == 'verified' and not self.is_refill:
                    from generator_source_policy import POLICY_VERSION
                    if (source_path.exists() and read(source_path).get('material',{}).get('source_eligibility',{}).get('policy_version')!=POLICY_VERSION):
                        # The acknowledged write remains final. Refresh and
                        # review its evidence without authoring or republishing.
                        self.persist(stage='validate',review_after_publication=True,
                                     review_binding=None,review_policy_version=None,approval_recorded=False)
                        continue
                    if not self.has_current_review():
                        try:
                            self.verify_approval_inputs()
                        except EngineChanged:
                            self.refresh_engine_review()
                        self.persist(stage='validate', review_after_publication=True)
                        continue
                    if not self.state.get('approval_recorded'):
                        self.record_approval()
                        self.persist(approval_recorded=True)
                return self.state
            if stage == 'source':
                source = self.directory / 'source/source.json'
                source.parent.mkdir(exist_ok=True)
                if not source.exists():
                    snapshot = self.publisher.extract_source(self.state['request']['kp'], source.parent)
                    save(source, snapshot)
                (self.directory / 'workspace').mkdir(exist_ok=True)
                self.persist(stage='refill' if self.is_refill else 'investigate', source_hash=digest(read(source)))
                if self.is_refill:
                    continue
                reference = self.state['request'].get('registered_package')
                current = read(source).get('registered_generator') or {}
                if not reference and current.get(':question-generator/script', '').startswith('generators/'):
                    reference = current[':question-generator/script']
                if reference:
                    manifest = self.directory / 'workspace' / self.state.get('manifest', 'package.json')
                    if manifest.is_file():
                        # A policy upgrade or interrupted investigation must not
                        # replace completed repairs with the registered draft.
                        self.persist(manifest=str(manifest.relative_to(self.directory / 'workspace')))
                    else:
                        self.load_registered_package(reference)
                    if self.state['request'].get('reuse_pipeline'):
                        self.reuse_completed_work()
            elif stage == 'investigate':
                self.investigate()
            elif stage == 'refill':
                try:
                    reference = self.state['request'].get('registered_package')
                    if not reference or not reference.startswith('generators/'):
                        raise RefillNeedsReview('package_invalid', 'Fast refill requires an immutable registered package')
                    package = self.load_registered_package(reference)
                    approval = self.refill_approval()
                    self.persist(approval_hash=digest(approval))
                    self.sample()
                    self.persist(stage='prepare', registration=package.reference)
                except (ValueError, FileNotFoundError, subprocess.SubprocessError) as error:
                    self.repair({'code': getattr(error, 'code', 'generator_failed'), 'error': str(error)})
            elif stage == 'generate':
                if self.recover_report_handoff():
                    continue
                attempt = self.state['attempt'] if self.state.get('author_running') else self.state['attempt'] + 1
                if attempt > self._attempt_limit:
                    self.block('author_attempts_exhausted', self.state.get('error'), 'generate')
                    return self.state
                self.persist(attempt=attempt, author_running=True)
                evidence = self.directory / f'author-{attempt}'
                context = self.context(evidence)
                if attempt > 1:
                    previous = self.directory / f'author-{attempt - 1}'
                    execution = read(previous / 'execution.json') if (previous / 'execution.json').exists() else {}
                    if execution.get('persistent_session'):
                        context['resume_session_id'] = execution.get('thread_id') or session_thread(previous)
                result = self.session('author', context, evidence)
                save(evidence / 'result.json', result)
                self.reload_repaired_runner()
                self.persist(author_running=False)
                if result.get('status') in {'unsupported', 'blocked'}:
                    self.repair({'code': 'author_unfinished', 'result': result,
                                 'error': 'Take responsibility for the source or tool limitation, use investigation exemplars, and finish the generator. Relevant shared repairs are authorized.'})
                    continue
                if result.get('status') != 'ready' or not isinstance(result.get('manifest'), str):
                    self.repair({'error': 'Author did not return a ready package', 'result': result})
                    continue
                self.persist(stage='sample', manifest=result['manifest'])
            elif stage == 'sample':
                try:
                    candidate = self.candidate_hash()
                    if (candidate == self.state.get('last_rejected_package')
                            and self.state.get('source_hash') == self.state.get('last_rejected_source')
                            and self.engine_identity() == self.state.get('last_rejected_engine')):
                        self.persist(repeated_candidate=True)
                        self.block('no_progress', {'error': 'Candidate is byte-identical to the rejected package. Apply and test the requested repair before another independent review.'}, 'generate')
                        return self.state
                    self.check_repair_regressions()
                    self.sample(tolerate_failures=bool(self.state['request'].get('review_existing')))
                    self.persist(stage='validate', package_hash=candidate)
                except (OSError, ValueError, subprocess.SubprocessError) as error:
                    self.repair({'error': str(error)})
                if stop_after == 'generate' and self.state['stage'] == 'validate':
                    return self.state
            elif stage == 'validate':
                if stop_after == 'generate':
                    return self.state
                self.ensure_inventory()
                try:
                    self.verify_approval_inputs()
                except EngineChanged:
                    self.refresh_engine_review()
                active = self.state.get('report_repair_directory') or self.state.get('active_review_directory')
                evidence = Path(active) if active else self.review_directory()
                result = self.review_candidate(evidence)
                if result is None:
                    if self.state['stage'] in {'report-repair', 'blocked'}:
                        return self.state
                    continue
                if result['verdict'] == 'accepted':
                    self.persist(stage='verified' if self.state.get('review_after_publication') else 'prepare',
                                 review=str(evidence / 'result.json'), review_policy_version=REVIEW_POLICY_VERSION,
                                 review_binding=digest(self.review_binding()), approval_recorded=False)
                elif self.state.get('review_after_publication'):
                    self.repair(result)
                elif result['verdict'] == 'unsupported':
                    self.repair(result)
                else:
                    self.repair(result)
            elif stage == 'prepare':
                if stop_after in {'generate', 'validate'}:
                    return self.state
                if not self.admit_publication():
                    continue
                source, manifest = self.manifest()
                package = publish_package(source, manifest['entrypoint'], manifest['files'],
                                          Path(self.environment.get('EDB_MATH_ROOT', '/media/jake/SSD/EDB/math')),
                                          dependencies=manifest.get('dependencies'), expected_digest=self.state['package_hash'])
                from generator_publish import SourceChanged
                try:
                    self.publisher.prepare(self.state['request']['kp'], self.publication_records(),
                                           package.reference, package.digest, self.directory / 'publication',
                                           source_snapshot=read(self.directory / 'source/source.json'),
                                           assets_directory=self.state.get('assets_directory', self.state['runtime']),
                                           **({'expected_registered_generator': package.reference} if self.is_refill else {}))
                except SourceChanged as error:
                    if not self.is_refill:
                        self.publisher.extract_source(self.state['request']['kp'], self.directory / 'source')
                        self.persist(source_hash=digest(read(self.directory / 'source/source.json')), inventory_hash=None)
                    self.repair({'code': 'source_changed', 'error': str(error)})
                    continue
                except ValueError as error:
                    # Preparation performs no submission. Invalid generated
                    # content is a repair request, not an infrastructure retry.
                    # Never retire or replace an already saved exact intent.
                    if (self.directory / 'publication/request.json').exists():
                        raise
                    self.repair({'code': 'preparation_invalid', 'error': str(error)})
                    continue
                self.persist(stage='push', registration=package.reference, publication_batch_hash=self.state['batch_hash'],
                             publication_package_hash=package.digest)
            elif stage == 'push':
                if stop_after != 'push':
                    return self.state
                if not ((publication / 'request.json').exists() or (publication / 'verification.json').exists()):
                    if not self.admit_publication():
                        continue
                from generator_publish import StaleBasis
                try:
                    result = self.publisher.publish(self.directory / 'publication')
                except StaleBasis:
                    # Only a confirmed rejection may replace the saved intent.
                    self.persist(stage='prepare')
                    stale_retries += 1
                    if stale_retries >= 3:
                        raise
                    continue
                except ValueError as error:
                    publication = self.directory / 'publication'
                    # A speculative preview can reject content before an intent
                    # exists. Any saved intent or completed verification retains
                    # exact publication recovery, including post-submit failures.
                    if ((publication / 'request.json').exists()
                            or (publication / 'verification.json').exists()):
                        raise
                    self.repair({'code': 'prepublication_invalid', 'error': str(error)})
                    continue
                self.persist(stage='verified', publication=result, error=None, needs_repair=False, completed=time.time())
            else:
                raise ValueError('Unknown pipeline stage: ' + str(stage))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kp', type=int, action='append', help='Knowledge point DB id; repeat to process a small queue')
    parser.add_argument('--inventory-job', type=Path)
    parser.add_argument('--inventory-cycle', type=int, help=argparse.SUPPRESS)
    parser.add_argument('--directory', type=Path, default=ROOT / '.local/generation')
    parser.add_argument('--difficulty', choices=['auto', 'easy', 'moderate', 'hard'], default='auto')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--database', default='math')
    parser.add_argument('--max-attempts', type=int, default=3, help='Durable author attempt budget; restarts do not replenish it')
    parser.add_argument('--resume-reason', help='Explicitly grant a blocked job a bounded recovery after addressing its cause')
    parser.add_argument('--stop-after', choices=['generate', 'validate', 'prepare', 'push'], default='push')
    args = parser.parse_args(argv)
    if args.count < 1 or args.max_attempts < 1:
        parser.error('count and max-attempts must be positive')
    from generator_publish import Publisher
    from serve_graph_explorer import database_environment
    env = database_environment(args.database)
    publisher = Publisher.from_environment(database=args.database)
    jobs = []
    if args.inventory_job:
        job = read(args.inventory_job)
        if args.inventory_cycle is not None and job.get('cycle', 1) != args.inventory_cycle:
            return 0
        request = job['request']
        directory = args.inventory_job.with_suffix('.pipeline') / str(job.get('cycle', 1))
        jobs.append((request['knowledgePoint'], request['difficulty'], request['missing'] or 5, directory, request.get('script'), request.get('jobKind')))
    else:
        if not args.kp:
            parser.error('Specify --kp (repeatable) or --inventory-job')
        for kp in args.kp:
            jobs.append((kp, 'unclassified' if args.difficulty == 'auto' else args.difficulty, args.count,
                         args.directory / args.database / f'{kp}-{args.difficulty}', None, None))
    failed = False
    for kp, difficulty, count, directory, registered, job_kind in jobs:
        try:
            existing = None if job_kind == 'refill' or registered and registered.startswith('generators/') else existing_generator(kp)
            if not existing and registered and not registered.startswith('generators/') and job_kind != 'refill':
                existing = str(resolve_registered_script(registered, ROOT, Path(env['EDB_MATH_ROOT'])))
            request = {'kp': kp, 'difficulty': difficulty, 'count': count, 'existing_entrypoint': existing}
            if job_kind:
                request['job_kind'] = job_kind
            if args.inventory_job and job['request'].get('stage') == 'review-generator':
                request['review_existing'] = True
            if args.inventory_job and job['request'].get('reuse_pipeline'):
                request['reuse_pipeline'] = job['request']['reuse_pipeline']
            if registered and (registered.startswith('generators/') or job_kind == 'refill'):
                request['registered_package'] = registered
            # Once admitted, keep the original inputs across inventory refreshes.
            if (directory / 'job.json').exists():
                request = read(directory / 'job.json')['request']
            result = Pipeline(directory, request, publisher, environment=env, max_attempts=args.max_attempts).run(args.stop_after, resume_reason=args.resume_reason)
            print(json.dumps({'kp': kp, 'stage': result['stage'], 'directory': str(directory),
                              **({'error': result.get('error')} if result['stage'] == 'blocked' else {})}), flush=True)
            if args.inventory_job:
                save(args.inventory_job.with_suffix('.result'), {
                    'outcome': 'generated' if result['stage'] == 'verified' else 'blocked' if result['stage'] == 'blocked' else 'repair-pending' if result['stage'] in {'repair', 'report-repair'} else 'unsupported' if result['stage'] == 'unsupported' else 'failed',
                    'evidence': str(directory / 'job.json'), 'generator': result.get('registration'),
                    'publication': result.get('publication'), 'needs_repair': result.get('needs_repair', False),
                    'difficulty': result.get('effective_difficulty', request['difficulty']),
                    'package': request.get('registered_package'), 'reason': result.get('error'),
                    'verified_bands': result.get('verified_bands', []) if result['stage'] == 'verified' else [],
                    'verified_package': result.get('registration') if result.get('approval_recorded') else None})
            failed |= result['stage'] in {'blocked', 'failed', 'unsupported', 'repair', 'report-repair'}
        except RunnerChanged:
            # Completed agent output and durable DB intents are already saved.
            # Re-exec keeps supervisor/KP ownership, and releases/reacquires the
            # worker's own lock without charging a process or model failure.
            os.execv(sys.executable, [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]])
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            failed = True
            print(json.dumps({'kp': kp, 'error': str(error), 'directory': str(directory)}), file=sys.stderr, flush=True)
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
