#!/usr/bin/env python3
"""Restartable generator authoring, independent review, and deterministic publication."""
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
            path = (Path(math_root) if path.parts and path.parts[0] == 'images' else Path(runtime)) / path
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
        template = templates / ('reviewer.md' if role == 'review' else 'author.md')
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
        launch_limit = execution.get('launch_limit', self.max_launches)
        if execution['launches'] >= launch_limit:
            raise SessionRetryExhausted(role, directory, execution)
        (directory / 'prompt.txt').write_text(prompt)
        executable = self.environment.get('COURSE_ACADEMY_CODEX_EXECUTABLE') or shutil.which('codex', path=self.environment.get('PATH')) or str(Path.home() / '.local/bin/codex')
        command = [executable, 'exec', '--ephemeral', '--skip-git-repo-check',
                   '--sandbox', 'workspace-write', '-c', 'approval_policy="never"',
                   '-c', 'sandbox_workspace_write.network_access=true',
                   '-C', str(self.root if role == 'author' and context.get('engine_repair_allowed') else context['workspace'] if role == 'author' else context['evidence_root']),
                   '--output-schema', str(templates / (role + '.schema.json')),
                   '--output-last-message', str(output), '--json', '-']
        # Count before spawning so parent/process crashes cannot reset an
        # unfinished ephemeral session's budget and launch it forever.
        execution = {**execution, 'launches': execution['launches'] + 1, 'status': 'running'}
        execution.pop('error', None)
        save(execution_path, execution)
        try:
            with (directory / 'events.jsonl').open('a') as log:
                process = subprocess.Popen(command, stdin=subprocess.PIPE, text=True, stdout=log,
                                           stderr=subprocess.STDOUT, env={
                                               **{k: v for k, v in self.environment.items() if k != 'COURSE_ACADEMY_GENERATOR_LOCK_FDS'},
                                               'PYTHONDONTWRITEBYTECODE': '1'},
                                           start_new_session=True, pass_fds=getattr(self, 'lock_fds', ()))
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
            execution.update(status='failed', error=str(error))
            save(execution_path, execution)
            if execution['launches'] >= launch_limit:
                raise SessionRetryExhausted(role, directory, execution) from error
            raise
        save(execution_path, {**execution, 'status': 'completed'})
        return result


class Pipeline:
    def __init__(self, directory, request, publisher, *, root=ROOT, environment=None,
                 session=None, max_attempts=3):
        self.directory, self.root = Path(directory).resolve(), Path(root).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.environment = dict(os.environ if environment is None else environment)
        self.publisher, self.session = publisher, session or CodexSession(self.root, self.environment)
        if max_attempts < 1:
            raise ValueError('max_attempts must be positive')
        self.max_attempts = max_attempts
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
            self.state = {'request': request, 'stage': 'source', 'attempt': 0,
                          'seed': int.from_bytes(os.urandom(4), 'big'), 'created': time.time()}
            self.persist()

    def persist(self, **updates):
        self.state.update(updated=time.time(), **updates)
        save(self.path, self.state)

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
                **({'engine_hash': self.state['engine_hash']} if 'engine_hash' in self.state else {})}

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
        validate_review(review, path.parent)
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
        if review['verdict'] != 'accepted' or not self.state.get('publication', {}).get('passed'):
            raise ValueError('Generator approval requires accepted review and verified publication')
        reference = self.state['registration']
        resolve_registered_script(reference, self.root, self.math_root)
        identity = {**source_identity(read(self.directory / 'source/source.json')),
                    'package_sha256': self.state['package_hash'], 'registration': reference}
        path = self.approval_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.with_suffix('.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            old = read(path) if path.exists() else {}
            bands = old.get('bands', {}) if old.get('identity') == identity else {}
            bands[self.state['effective_difficulty']] = {
                'review_policy_version': REVIEW_POLICY_VERSION,
                'review_sha256': digest(review), 'batch_sha256': self.state['batch_hash'],
                'evidence': str(review_path), 'publication': self.state['publication']}
            save(path, {'format': 1, 'identity': identity, 'bands': bands})

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
        if value.get('format') != 1 or value.get('identity') != identity:
            raise RefillNeedsReview('source_changed', 'Registered package approval does not match current instructional source')
        band = self.state['request']['difficulty']
        if band not in value.get('bands', {}):
            raise RefillNeedsReview('approval_band_missing', 'Registered package has not been reviewed for ' + band)
        approval = value['bands'][band]
        if not isinstance(approval, dict) or approval.get('review_policy_version') != REVIEW_POLICY_VERSION:
            raise RefillNeedsReview('approval_policy_stale',
                                    'Registered package needs an independent review under the current policy')
        if (not isinstance(approval, dict) or not approval.get('publication', {}).get('passed')
                or any(not re.fullmatch(r'[0-9a-f]{64}', str(approval.get(key, '')))
                       for key in ('review_sha256', 'batch_sha256'))):
            raise RefillNeedsReview('approval_invalid', 'Registered generator approval is incomplete')
        return {'identity': identity, 'difficulty': band, 'approval': approval}

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
                'previous_review': previous_review, 'evidence_root': str(evidence),
                'package_root': str((self.directory / 'workspace' / self.state.get('manifest', 'package.json')).parent),
                'manifest_file': str(self.directory / 'workspace' / self.state.get('manifest', 'package.json')),
                'requested_difficulty': self.state.get('effective_difficulty', request['difficulty']), 'count': request['count'],
                'sample_seed': self.state['seed'],
                'knowledge_point': request['kp'], 'python': python_executable(self.root, self.environment),
                'review_policy_version': REVIEW_POLICY_VERSION, 'review_binding': self.review_binding(),
                'math_root': self.environment.get('EDB_MATH_ROOT', '/media/jake/SSD/EDB/math'),
                'batch_file': str(self.directory / 'samples.json'),
                'repair_history_file': str(self.directory / 'repair-history.json'),
                'repair_mode': 'root_cause' if self.state.get('repair_cycle', 0) or self.state.get('repeated_candidate') else 'targeted',
                'repair_regressions_file': str(self.directory / 'workspace/repair-regressions.json'),
                'repair_preflight_file': str(self.directory / 'repair-preflight.json'),
                'engine_repair_allowed': any(row['finding']['kind'] == 'grading' for row in history['findings'])}

    def review_candidate(self, evidence):
        """Repair reports in the reviewer's writable root with a durable budget."""
        evidence.mkdir(parents=True, exist_ok=True)
        binding_path = evidence / 'review-binding.json'
        binding = self.review_binding()
        previous = self.state.get('previous_review') or {}
        recorded = read(binding_path) if binding_path.exists() else (
            previous.get('binding') if previous.get('directory') == str(evidence) else None)
        if recorded is not None and recorded != binding:
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
        save(binding_path, binding)
        rounds = self.state.get('review_report_rounds', {})
        count = rounds.get(str(evidence), 0)
        limit = self.state.get('review_report_limits', {}).get(str(evidence), 3)
        error = self.state.get('review_report_error') if count else None
        while count < limit:
            directory = evidence if count == 0 else evidence / ('contract-repair' if count == 1 else f'contract-repair-{count}')
            context = self.context(evidence)
            if error:
                context['review_contract_feedback'] = {
                    'error': error, 'result_file': self.state.get('review_report_result_file', str(evidence / 'result.json')),
                    'instruction': 'Correct your report/evidence in evidence_root; preserve the reviewed package and completed checks.'}
            if not self.admit_review_session(directory):
                return None
            result = self.session('review', context, directory)
            save(directory / 'result.json', result)
            # A changed candidate is a separate failure, never a report repair.
            try:
                self.verify_approval_inputs()
            except EngineChanged:
                self.sample()
                self.persist(stage='validate')
                return None
            except ValueError as changed:
                self.repair({'code': 'reviewed_inputs_changed', 'error': str(changed)})
                return None
            self.persist(previous_review={'directory': str(evidence), 'binding': self.review_binding()})
            try:
                validate_review(result, evidence)
            except ValueError as invalid:
                error = str(invalid)
            else:
                if not evidence_only_review(result):
                    save(evidence / 'result.json', result)
                    self.persist(review_report_error=None, review_report_result_file=None,
                                 report_repair_directory=None)
                    if result['verdict'] == 'accepted':
                        repaired = self.repair_inventory(evidence)
                        if repaired and repaired.get('unresolved'):
                            self.block_inventory(repaired)
                            return None
                        if repaired and repaired['inventory_changed']:
                            self.persist(stage='validate', needs_repair=True)
                            return None
                    return result
                error = {'code': 'review_evidence_correction', 'findings': result['findings'],
                         'instruction': 'Fix the report and evidence under evidence_root; the generator does not need an author pass for these findings.'}
                self.remember_repair(result)
            count += 1
            rounds[str(evidence)] = count
            self.persist(review_report_rounds=rounds, review_report_error=error,
                         review_report_result_file=str(directory / 'result.json'))
            save(evidence / 'contract-feedback.json', {'error': error, 'correction': count})
        self.block('review_report_correction_exhausted', {
            'error': error, 'evidence_root': str(evidence), 'rounds': count,
            'details': 'Independent report correction exhausted its saved budget; repair the reported cause before explicit resume.'}, 'validate')
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

    def sample(self):
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
        runtime = self.directory / f'runtime-{self.state["attempt"]}'
        if runtime.exists():
            shutil.rmtree(runtime)
        runtime.mkdir(exist_ok=True)
        output = self.directory / f'outputs-{self.state["attempt"]}'
        if output.exists():
            shutil.rmtree(output)
        for name in manifest['files']:
            destination = inside(runtime, name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(inside(source, name), destination)
        command = [python_executable(self.root, self.environment), '-E', '-s', '-B', str(inside(runtime, manifest['entrypoint'])),
                   '--difficulty', difficulty, '--count', str(self.state['request']['count']),
                   '--seed', str(self.state['seed']), '--format', 'json']
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
            images.append(asset_hashes(outputs[-1], runtime, self.environment.get('EDB_MATH_ROOT', '/media/jake/SSD/EDB/math')))
        if outputs[0] != outputs[1] or images[0] != images[1]:
            raise ValueError('Generator is not deterministic for the saved seed')
        records = outputs[0]
        if isinstance(records, dict):
            records = records.get('records', records.get('questions', [records] if 'question' in records else None))
        if not isinstance(records, list) or len(records) != self.state['request']['count']:
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
        save(self.directory / 'samples.json', records)
        self.persist(batch_hash=digest(records), runtime=str(runtime),
                     engine_hash=self.engine_identity(),
                     report_repair_directory=None, review_report_error=None,
                     review_report_result_file=None,
                     assets=asset_hashes(records, runtime, self.environment.get('EDB_MATH_ROOT', '/media/jake/SSD/EDB/math')))

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
            repaired = self.repair_inventory()
            if not repaired or repaired.get('unresolved'):
                self.block_inventory(repaired or {'unresolved': ['Missing reviewed affected-inventory.json evidence']})
                return
            content = [row for row in findings if row.get('kind') not in {'inventory', 'evidence'}]
            if not content:
                if not repaired['inventory_changed']:
                    self.block_inventory({'unresolved': ['Review still rejects inventory already repaired; no delivery evidence changed.']})
                    return
                self.check_repair_regressions()
                self.sample()
                self.persist(stage='validate', package_hash=self.candidate_hash(), needs_repair=True)
                return
            reason = {**reason, 'findings': content}
        self.remember_repair(reason)
        save(self.directory / 'feedback.json', {**reason,
            'repair_history_file': str(self.directory / 'repair-history.json'),
            'instruction': 'Fix the concrete generator defect, retain earlier counterexamples, and declare executable checks in repair-regressions.json. If the required action belongs outside the author workspace, return blocked with the exact required action; do not repeat unchanged checks.'})
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
            self.sample()
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

    def _run(self, stop_after):
        stale_retries = 0
        while True:
            stage = self.state['stage']
            publication = self.directory / 'publication'
            if (stage in {'source', 'generate', 'sample', 'repair', 'report-repair', 'failed', 'validate', 'prepare'}
                    and not self.state.get('review_after_publication')
                    and (publication / 'request.json').exists()):
                # A durable intent can already have committed. Resolve its exact
                # bytes before policy upgrades, review, or authoring touch inputs.
                self.persist(stage='push')
                continue
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
                    if not self.has_current_review():
                        try:
                            self.verify_approval_inputs()
                        except EngineChanged:
                            self.sample()
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
                self.persist(stage='refill' if self.is_refill else 'generate', source_hash=digest(read(source)))
                if self.is_refill:
                    continue
                reference = self.state['request'].get('registered_package')
                current = read(source).get('registered_generator') or {}
                if not reference and current.get(':question-generator/script', '').startswith('generators/'):
                    reference = current[':question-generator/script']
                if reference:
                    package = self.load_registered_package(reference)
                    try:
                        self.sample()
                        self.persist(stage='validate', package_hash=package.digest)
                    except (OSError, ValueError, subprocess.SubprocessError) as error:
                        self.repair({'error': str(error)})
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
                result = self.session('author', self.context(evidence), evidence)
                save(evidence / 'result.json', result)
                self.persist(author_running=False)
                if result.get('status') in {'unsupported', 'blocked'}:
                    self.block('author_reported_limitation', result, 'generate')
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
                    self.sample()
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
                    self.sample()
                evidence = Path(self.state['report_repair_directory']) if self.state.get('report_repair_directory') else self.review_directory()
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
                                           assets_directory=self.state['runtime'],
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
                self.persist(stage='push', registration=package.reference)
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
                    'package': request.get('registered_package'), 'reason': result.get('error')})
            failed |= result['stage'] in {'blocked', 'failed', 'unsupported', 'repair', 'report-repair'}
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            failed = True
            print(json.dumps({'kp': kp, 'error': str(error), 'directory': str(directory)}), file=sys.stderr, flush=True)
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
