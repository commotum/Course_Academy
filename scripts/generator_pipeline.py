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
from generator_review import validate_review


def read(path):
    return json.loads(Path(path).read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


class RefillNeedsReview(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


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
    def __init__(self, root=ROOT, environment=None, timeout=3600):
        self.root, self.environment, self.timeout = Path(root), dict(os.environ if environment is None else environment), timeout

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
        (directory / 'prompt.txt').write_text(prompt)
        executable = self.environment.get('COURSE_ACADEMY_CODEX_EXECUTABLE') or shutil.which('codex', path=self.environment.get('PATH')) or str(Path.home() / '.local/bin/codex')
        command = [executable, 'exec', '--ephemeral', '--skip-git-repo-check',
                   '--sandbox', 'workspace-write', '-c', 'approval_policy="never"',
                   '-c', 'sandbox_workspace_write.network_access=true',
                   '-C', str(context['workspace'] if role == 'author' else directory),
                   '--output-schema', str(templates / (role + '.schema.json')),
                   '--output-last-message', str(output), '--json', '-']
        with (directory / 'events.jsonl').open('a') as log:
            process = subprocess.Popen(command, stdin=subprocess.PIPE, text=True, stdout=log,
                                       stderr=subprocess.STDOUT, env={**self.environment, 'PYTHONDONTWRITEBYTECODE': '1'},
                                       start_new_session=True, pass_fds=getattr(self, 'lock_fds', ()))
            try:
                process.communicate(prompt, timeout=self.timeout)
            except BaseException:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                raise
            if process.returncode:
                raise subprocess.CalledProcessError(process.returncode, command)
        return read(output)


class Pipeline:
    def __init__(self, directory, request, publisher, *, root=ROOT, environment=None,
                 session=None, max_attempts=3):
        self.directory, self.root = Path(directory).resolve(), Path(root).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.environment = dict(os.environ if environment is None else environment)
        self.publisher, self.session = publisher, session or CodexSession(self.root, self.environment)
        self.max_attempts = max_attempts
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
        self.state.update(updates)
        save(self.path, self.state)

    @property
    def is_refill(self):
        return self.state['request'].get('job_kind') == 'refill'

    @property
    def math_root(self):
        return Path(self.environment.get('EDB_MATH_ROOT', '/media/jake/SSD/EDB/math'))

    def approval_path(self):
        return self.math_root / 'generators/approvals' / self.state['package_hash'] / (str(self.state['request']['kp']) + '.json')

    def record_approval(self):
        """Persist reviewed scope only after publication has been acknowledged."""
        if self.is_refill:
            return
        self.verify_approval_inputs()
        review_path = Path(self.state['review'])
        review = read(review_path)
        validate_review(review, review_path.parent)
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
        request = self.state['request']
        return {'repo_root': str(self.root), 'workspace': str(self.directory / 'workspace'),
                'source_root': str(self.directory / 'source'), 'source_file': str(self.directory / 'source/source.json'),
                'existing_entrypoint': request.get('existing_entrypoint'),
                'feedback_file': str(self.directory / 'feedback.json'), 'evidence_root': str(evidence),
                'package_root': str((self.directory / 'workspace' / self.state.get('manifest', 'package.json')).parent),
                'manifest_file': str(self.directory / 'workspace' / self.state.get('manifest', 'package.json')),
                'requested_difficulty': self.state.get('effective_difficulty', request['difficulty']), 'count': request['count'],
                'knowledge_point': request['kp'], 'python': python_executable(self.root, self.environment),
                'math_root': self.environment.get('EDB_MATH_ROOT', '/media/jake/SSD/EDB/math'),
                'batch_file': str(self.directory / 'samples.json')}

    def sample(self):
        source, manifest = self.manifest()
        difficulty = self.state['request']['difficulty']
        if difficulty == 'unclassified':
            difficulty = manifest.get('default_difficulty')
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
                     assets=asset_hashes(records, runtime, self.environment.get('EDB_MATH_ROOT', '/media/jake/SSD/EDB/math')))

    def verify_approval_inputs(self):
        if self.candidate_hash() != self.state['package_hash'] or digest(read(self.directory / 'samples.json')) != self.state['batch_hash']:
            raise ValueError('Reviewed package or publication batch changed')
        if digest(read(self.directory / 'source/source.json')) != self.state['source_hash']:
            raise ValueError('Reviewed source snapshot changed')
        if any(hashlib.sha256(Path(path).read_bytes()).hexdigest() != sha for path, sha in self.state['assets'].items()):
            raise ValueError('Reviewed image bytes changed')
        _, manifest = self.manifest()
        observed = check_dependencies(manifest['dependencies'], python_executable(self.root, self.environment), environment=self.environment)
        if observed != read(self.directory / 'runtime-dependencies.json'):
            raise ValueError('Runtime dependencies changed after generation')
        if self.is_refill:
            resolve_registered_script(self.state['request']['registered_package'], self.root, self.math_root)
            if digest(self.refill_approval()) != self.state['approval_hash']:
                raise ValueError('Registered generator approval changed during refill')

    def repair(self, reason):
        save(self.directory / 'feedback.json', reason)
        if self.is_refill:
            self.persist(stage='unsupported', needs_repair=True, error=reason)
        else:
            self.persist(stage='failed' if self.state['attempt'] >= self.max_attempts else 'generate', error=reason)

    def run(self, stop_after='push'):
        with (self.directory / 'worker.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if isinstance(self.session, CodexSession):
                self.session.lock_fds = (lock.fileno(),)
            return self._run(stop_after)

    def _run(self, stop_after):
        stale_retries = 0
        while True:
            stage = self.state['stage']
            if stage in {'verified', 'failed', 'unsupported'}:
                if stage == 'verified' and not self.is_refill and not self.state.get('approval_recorded'):
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
                attempt = self.state['attempt'] if self.state.get('author_running') else self.state['attempt'] + 1
                if attempt > self.max_attempts:
                    self.persist(stage='failed', error='Authoring attempts exhausted')
                    continue
                self.persist(attempt=attempt, author_running=True)
                evidence = self.directory / f'author-{attempt}'
                result = self.session('author', self.context(evidence), evidence)
                save(evidence / 'result.json', result)
                self.persist(author_running=False)
                if result.get('status') == 'unsupported':
                    self.persist(stage='unsupported', error=result)
                    continue
                if result.get('status') != 'ready' or not isinstance(result.get('manifest'), str):
                    self.repair({'error': 'Author did not return a ready package', 'result': result})
                    continue
                self.persist(manifest=result['manifest'])
                try:
                    candidate = self.candidate_hash()
                    self.sample()
                    self.persist(stage='validate', package_hash=candidate)
                except (OSError, ValueError, subprocess.SubprocessError) as error:
                    self.repair({'error': str(error)})
                if stop_after == 'generate' and self.state['stage'] == 'validate':
                    return self.state
            elif stage == 'validate':
                if stop_after == 'generate':
                    return self.state
                evidence = self.directory / f'review-{self.state["attempt"]}'
                if self.candidate_hash() != self.state['package_hash']:
                    self.repair({'error': 'Package changed after generation'})
                    continue
                result = self.session('review', self.context(evidence), evidence)
                save(evidence / 'result.json', result)
                try:
                    validate_review(result, evidence)
                    self.verify_approval_inputs()
                except ValueError as error:
                    self.repair({'error': str(error), 'review': result})
                    continue
                if result['verdict'] == 'accepted':
                    self.persist(stage='prepare', review=str(evidence / 'result.json'))
                elif result['verdict'] == 'unsupported':
                    self.persist(stage='unsupported', error=result)
                else:
                    self.repair(result)
            elif stage == 'prepare':
                if stop_after in {'generate', 'validate'}:
                    return self.state
                try:
                    self.verify_approval_inputs()
                except (ValueError, FileNotFoundError) as error:
                    if not self.is_refill:
                        raise
                    self.repair({'code': getattr(error, 'code', 'generator_failed'), 'error': str(error)})
                    continue
                source, manifest = self.manifest()
                package = publish_package(source, manifest['entrypoint'], manifest['files'],
                                          Path(self.environment.get('EDB_MATH_ROOT', '/media/jake/SSD/EDB/math')),
                                          dependencies=manifest.get('dependencies'), expected_digest=self.state['package_hash'])
                from generator_publish import SourceChanged
                try:
                    self.publisher.prepare(self.state['request']['kp'], read(self.directory / 'samples.json'),
                                           package.reference, package.digest, self.directory / 'publication',
                                           source_snapshot=read(self.directory / 'source/source.json'),
                                           assets_directory=self.state['runtime'],
                                           **({'expected_registered_generator': package.reference} if self.is_refill else {}))
                except SourceChanged as error:
                    if not self.is_refill:
                        self.publisher.extract_source(self.state['request']['kp'], self.directory / 'source')
                        self.persist(source_hash=digest(read(self.directory / 'source/source.json')))
                    self.repair({'code': 'source_changed', 'error': str(error)})
                    continue
                except ValueError as error:
                    # Preparation performs no submission. Invalid generated
                    # content is a repair request, not an infrastructure retry.
                    # Never retire or replace an already saved exact intent.
                    if not self.is_refill or (self.directory / 'publication/request.json').exists():
                        raise
                    self.repair({'code': 'preparation_invalid', 'error': str(error)})
                    continue
                self.persist(stage='push', registration=package.reference)
            elif stage == 'push':
                if stop_after != 'push':
                    return self.state
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
                    if (not self.is_refill or (publication / 'request.json').exists()
                            or (publication / 'verification.json').exists()):
                        raise
                    self.repair({'code': 'prepublication_invalid', 'error': str(error)})
                    continue
                self.persist(stage='verified', publication=result, error=None, completed=time.time())
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
    parser.add_argument('--max-attempts', type=int, default=3)
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
            result = Pipeline(directory, request, publisher, environment=env, max_attempts=args.max_attempts).run(args.stop_after)
            print(json.dumps({'kp': kp, 'stage': result['stage'], 'directory': str(directory)}), flush=True)
            if args.inventory_job:
                save(args.inventory_job.with_suffix('.result'), {
                    'outcome': 'generated' if result['stage'] == 'verified' else 'unsupported' if result['stage'] == 'unsupported' else 'failed',
                    'evidence': str(directory / 'job.json'), 'generator': result.get('registration'),
                    'publication': result.get('publication'), 'needs_repair': result.get('needs_repair', False),
                    'difficulty': result.get('effective_difficulty', request['difficulty']),
                    'package': request.get('registered_package'), 'reason': result.get('error')})
            failed |= result['stage'] in {'failed', 'unsupported'}
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
            failed = True
            print(json.dumps({'kp': kp, 'error': str(error), 'directory': str(directory)}), file=sys.stderr, flush=True)
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
