"""Durable, deduplicated handoff from scheduler inventory to generator workers.

The creator runs the documented generation pipeline. A job completes only when
a subsequent captured inventory confirms replenishment, not when a process exits.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time
from generator_priority import PRIORITY_FIELDS, PRIORITY_POLICY, priority_key


def build_worker_count(environment: dict) -> int:
    value = environment.get('COURSE_ACADEMY_GENERATOR_BUILD_WORKERS', '3')
    try:
        count = int(value)
    except (TypeError, ValueError):
        raise ValueError('COURSE_ACADEMY_GENERATOR_BUILD_WORKERS must be a positive integer') from None
    if count < 1:
        raise ValueError('COURSE_ACADEMY_GENERATOR_BUILD_WORKERS must be a positive integer')
    return count


def review_worker_count(environment: dict, builders: int | None = None) -> int:
    """Give existing-package reviews capacity without adding worker processes.

    Keep at least one builder on the ordinary shortage ordering. A single
    builder therefore has no reserved review slot; reviews still use its queue.
    """
    builders = build_worker_count(environment) if builders is None else builders
    value = environment.get('COURSE_ACADEMY_GENERATOR_REVIEW_WORKERS',
                            '1' if builders > 1 else '0')
    try:
        count = int(value)
    except (TypeError, ValueError):
        raise ValueError('COURSE_ACADEMY_GENERATOR_REVIEW_WORKERS must be an integer from 0 to build workers minus 1') from None
    if not 0 <= count < builders:
        raise ValueError('COURSE_ACADEMY_GENERATOR_REVIEW_WORKERS must be an integer from 0 to build workers minus 1')
    return count


def ranked_reason(common: dict, reason: dict) -> dict:
    """A shared KP's demand may belong to a different topic than its winner."""
    result = {**common, **{field: reason[field] for field in
              (*PRIORITY_FIELDS, 'score', 'purpose', 'shortage', 'next_activity') if field in reason}}
    result['topic'] = reason.get('topic_entity', reason.get('topic', common['topic']))
    return result


def speculative_review(request: dict) -> bool:
    """A reserve band without observations is a fallback, not a rejection.

    Observed ratings are a useful scheduling hint, not a package capability or
    approval certificate. Actual shortages and assessment variety keep their
    priority even when this hint does not support their requested band.
    """
    return (request.get('stage') == 'review-generator'
            and request.get('purpose') == 'routine-replenishment'
            and request.get('difficulty') not in request.get('observed_difficulties', []))


def review_request(path: Path, previous: dict, request: dict) -> dict:
    """Prefer the failed refill's eligible source over broad inventory ratings."""
    request = {**request, 'jobKind': 'build', 'stage': 'review-generator'}
    try:
        source = json.loads((path.with_suffix('.pipeline') / str(previous.get('cycle', 1))
                             / 'source/source.json').read_text())
    except (OSError, ValueError):
        return request
    if not isinstance(source, dict):
        return request
    generator, material = source.get('registered_generator'), source.get('material')
    eligibility = material.get('source_eligibility') if isinstance(material, dict) else None
    if not isinstance(generator, dict) or not isinstance(eligibility, dict):
        return request
    bands = source.get('available_difficulties')
    if (source.get('kp_id') == request['knowledgePoint']
            and source.get('lineage') == previous.get('lineage')
            and generator.get(':question-generator/script') == request['script']
            and eligibility.get('policy_version')
            and isinstance(bands, list) and all(band in ('easy', 'moderate', 'hard') for band in bands)):
        request.update(observed_difficulties=bands, difficulty_evidence='captured-eligible-source',
                       difficulty_evidence_basis=source.get('basis'))
    return request


def ranked_requests(inventory: dict) -> list[dict]:
    """One build per KP; approved packages replenish independently per band."""
    builds, refills = {}, {}
    gate = inventory.get('selection_gate')
    selected = set(gate['selected_knowledge_points']) if gate and not gate['open'] else None
    contexts = [kp for topic in inventory['topics'] for kp in topic['knowledge_points']]
    contexts += inventory.get('maintained_knowledge_points', [])
    for kp in [*inventory['knowledge_points'], *contexts]:
        script = kp.get('generator_script')
        usable = kp.get('generator_usable', False)
        packaged = usable and bool(script) and script.startswith('generators/')
        eligible = bool(kp.get('build_eligible', kp.get('build_required') or kp.get('urgency_value')))
        if not packaged and not eligible:
            continue
        common = {'knowledgePoint': kp['db/id'], 'topic': kp['topic_entity'],
                  'script': script, 'basis': inventory['basis'],
                  'score': kp['score'], 'purpose': kp['purpose'],
                  'shortage': kp.get('shortage', 0), 'urgency_value': kp.get('urgency_value', 0),
                  'first_studied_at': kp.get('first_studied_at'), 'waiting_since': kp.get('waiting_since'),
                  'next_activity': kp.get('next_activity'), 'priority_reasons': kp.get('priority_reasons', []),
                  'observed_difficulties': kp['inventory'].get('supported_difficulties', []),
                  'difficulty_evidence': 'inventory',
                  **{field: kp[field] for field in PRIORITY_FIELDS if field in kp}}
        if not packaged:
            # The selection gate reserves agent work for selected KPs. Existing
            # packages may still refill automatically after approval checks.
            if selected is not None and kp['db/id'] not in selected:
                continue
            # Existing repository scripts must pass the independent review once
            # before the inexpensive refill lane may execute their package.
            request = {**common, 'jobKind': 'build',
                       'difficulty': kp.get('generated_band', 'unclassified'), 'missing': 5,
                       'stage': 'migrate-generator' if usable else kp.get('build_action') or 'create-generator'}
            old = builds.get(kp['db/id'])
            if old is None or priority_key(request) < priority_key(old):
                builds[kp['db/id']] = request
            continue
        for band in ('easy', 'moderate', 'hard'):
            missing = kp.get('refill_deficits', {}).get(band, max(0, 5 - kp['inventory']['available'].get(band, 0)))
            if missing <= 0:
                continue
            reasons = [ranked_reason(common, reason) for reason in kp.get('priority_reasons', []) if eligible
                       and reason['purpose'] != 'advance-build' and reason.get('generated_band', band) == band]
            routine = {'purpose': 'routine-replenishment', 'shortage': missing,
                       'score': 1000 * missing + 100 * kp.get('urgency_value', 0)}
            if 'baseline_relevance_tier' in kp:
                routine['relevance_tier'] = kp['baseline_relevance_tier']
            reasons.append(ranked_reason(common, routine))
            request = {**min(reasons, key=priority_key),
                       'jobKind': 'refill', 'difficulty': band, 'missing': missing,
                       'available': 5 - missing, 'stage': 'generate'}
            key = kp['db/id'], band
            if key not in refills or priority_key(request) < priority_key(refills[key]):
                refills[key] = request
    return sorted([*builds.values(), *refills.values()], key=priority_key)


def request_variant(request: dict) -> str:
    """Content failures reopen only after a material request change."""
    return hashlib.sha256(json.dumps([request.get(k) for k in
        ('knowledgePoint', 'stage', 'script', 'difficulty', 'missing')]).encode()).hexdigest()


def save(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    with temp.open('w') as stream:
        json.dump(value, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    temp.replace(path)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class InventoryJobs:
    def __init__(self, root: Path, directory: Path, learner: str, environment: dict | None = None):
        self.root, self.directory, self.learner = root, directory, learner
        self.environment = dict(os.environ if environment is None else environment)
        directory.mkdir(parents=True, exist_ok=True)
        self._active_lock = threading.Lock()
        self._active_owners = set()
        self._stopping = False

    def mark_service_interruption(self):
        """Stop admissions and preserve exact launches owned by this supervisor."""
        from generator_lifecycle import mark_stopped
        with self._active_lock:
            self._stopping = True
            return [mark_stopped(owner) for owner in self._active_owners]

    def creator_executable(self) -> str:
        return (self.environment.get('COURSE_ACADEMY_CODEX_EXECUTABLE')
                or shutil.which('codex', path=self.environment.get('PATH', os.defpath))
                or str(Path.home() / '.local/bin/codex'))

    def accept(self, inventory: dict) -> None:
        if 'knowledge_points' not in inventory:
            return self._accept_legacy(inventory)
        requests = ranked_requests(inventory)
        gate = inventory.get('selection_gate')
        selected = set(gate['selected_knowledge_points']) if gate and not gate['open'] else None
        lineage = inventory['cursor']['lineage']
        with (self.directory / 'jobs.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            cursor_path = self.directory / 'cursor.json'
            cursor = json.loads(cursor_path.read_text()) if cursor_path.exists() else {}
            if cursor.get('lineage', lineage) != lineage:
                raise ValueError('Inventory database lineage changed; reconcile existing jobs before retargeting')
            if inventory['basis'] < cursor.get('basis', 0):
                raise ValueError('Inventory basis regressed')
            existing = {path: json.loads(path.read_text()) for path in self.directory.glob('*.json')
                        if path.name != 'cursor.json'}
            existing = {path: job for path, job in existing.items() if 'request' in job}
            build_records, refill_records = {}, {}
            for path, job in existing.items():
                request = job['request']
                if request.get('jobKind', 'build') == 'build':
                    build_records.setdefault(request['knowledgePoint'], []).append((path, job))
                else:
                    refill_records[(request['knowledgePoint'], request['difficulty'])] = path, job
            build_requests = [request for request in requests if request['jobKind'] == 'build']
            refill_requests = [request for request in requests if request['jobKind'] == 'refill']
            reopened_refills = set()
            for request in refill_requests:
                previous = refill_records.get((request['knowledgePoint'], request['difficulty']))
                if previous is None:
                    continue
                refill_path, old = previous
                if old.get('state') != 'repair-needed' or old['request'].get('script') != request['script']:
                    continue
                successful_review = any(
                    job['request'].get('jobKind') == 'build'
                    and job['request']['knowledgePoint'] == request['knowledgePoint']
                    and job['request']['difficulty'] == request['difficulty']
                    and job['request'].get('script') == request['script']
                    and job.get('outcome', {}).get('outcome') == 'generated'
                    and job.get('completedAt', 0) > old.get('completedAt', 0)
                    for _, job in build_records.get(request['knowledgePoint'], []))
                if successful_review:
                    reopened_refills.add((request['knowledgePoint'], request['difficulty']))
                elif selected is None or request['knowledgePoint'] in selected:
                    # A refill with missing/stale approval cannot start an
                    # outside agent review while selected work is incomplete.
                    build_requests.append(review_request(refill_path, old, request))
            # Each package/band is allowed its own independent review, but a
            # rejected unchanged band must not prevent other bands from running.
            blocked = {}
            for job in existing.values():
                if job['request'].get('jobKind', 'build') == 'build':
                    blocked.setdefault(job['request']['knowledgePoint'], set()).update(job.get('rejectedVariants', []))
                    if job.get('state') == 'rejected':
                        blocked[job['request']['knowledgePoint']].add(request_variant(job['request']))
            selected_builds = {}
            for request in sorted(build_requests, key=lambda request: (speculative_review(request), *priority_key(request))):
                kp = request['knowledgePoint']
                if request_variant(request) not in blocked.get(kp, set()):
                    selected_builds.setdefault(kp, request)
            requests = [*selected_builds.values(), *refill_requests]
            current = set()
            for request in requests:
                kind, kp = request['jobKind'], request['knowledgePoint']
                key = hashlib.sha256(json.dumps([self.learner, kp, kind,
                    request['difficulty'] if kind == 'refill' else None]).encode()).hexdigest()
                path = self.directory / f'{key}.json'
                if kind == 'build':
                    # Preserve old workspace paths and exact publication request
                    # identities while collapsing old per-band build requests.
                    candidates = [(p, job) for p, job in build_records.get(kp, []) if p not in current]
                    if candidates:
                        path, _ = min(candidates, key=lambda pair: (
                            not self.publication_recovery(pair[0], pair[1]),
                            not self.recoverable(pair[0], pair[1]),
                            pair[1]['request'].get('jobKind') != 'build',
                            pair[1].get('state') in {'verified', 'withdrawn'}, pair[0].name))
                        key = path.stem
                current.add(path)
                old = existing.get(path, {})
                recovering = self.recoverable(path, old)
                if recovering or old.get('state') == 'running':
                    request = {**request, **{field: old['request'].get(field) for field in
                        ('stage', 'missing', 'script', 'difficulty')},
                        'jobKind': old['request'].get('jobKind', 'build')}
                state, cycle = old.get('state', 'pending'), old.get('cycle', 1)
                previous_cycle = cycle
                changed = any(old.get('request', {}).get(k) != request.get(k)
                              for k in ('stage', 'missing', 'script', 'difficulty'))
                if state == 'awaiting-verification' and changed:
                    state, cycle = 'pending', cycle + 1
                    old = {**old, 'attempts': 0, 'replenishments': 0, 'retryAt': 0}
                elif state == 'awaiting-verification' and old.get('retryAt', 0) <= time.time():
                    state = 'pending' if old.get('replenishments', 0) < 3 else 'rejected'
                    if state == 'pending':
                        cycle += 1
                if (state in {'verified', 'withdrawn'} and not recovering or state in {'rejected', 'repair-needed', 'awaiting-verification'} and changed
                        or kind == 'refill' and (kp, request['difficulty']) in reopened_refills):
                    state, cycle = 'pending', cycle + 1
                    old = {**old, 'attempts': 0, 'replenishments': 0, 'retryAt': 0}
                if cycle != previous_cycle:
                    old = {**old, 'outcome': {}, 'completedAt': 0}
                if recovering:
                    # Resume the saved inputs and cycle without promoting an
                    # unfinished draft above currently higher-priority work.
                    state = 'running'
                value = {**old, 'key': key, 'learner': self.learner, 'lineage': lineage,
                         'request': request, 'state': state, 'cycle': cycle, 'recoveryOnly': False}
                previous = existing.get(path)
                comparable = {**value, 'request': {**request, 'basis': previous['request'].get('basis')}} if previous else value
                if comparable != previous:
                    save(path, value)
            captured_kps = [kp for topic in inventory['topics'] for kp in topic['knowledge_points']]
            captured_kps.extend(inventory.get('maintained_knowledge_points', []))
            present_kps = {kp['db/id'] for kp in captured_kps}
            # A topic can remain in diagnostics after its lesson demand ends.
            # Its mere presence does not verify an unfinished generator build.
            verifiable_builds = {kp['db/id'] for kp in captured_kps
                if kp.get('build_eligible', True) or (kp.get('generator_usable')
                    and (kp.get('generator_script') or '').startswith('generators/'))}
            for path, old in existing.items():
                if path in current:
                    continue
                if old.get('state') == 'blocked':
                    continue
                if self.publication_recovery(path, old):
                    save(path, {**old, 'request': {**old['request'], 'jobKind': old['request'].get('jobKind', 'build')},
                                'state': 'running', 'recoveryOnly': True})
                elif self.recoverable(path, old):
                    # Keep the unfinished workspace and cycle, but resume it
                    # only when the inventory supplies a current demand again.
                    if old.get('state') != 'withdrawn':
                        save(path, {**old, 'state': 'withdrawn', 'recoveryOnly': False})
                else:
                    # Being absent from this full ranked projection is the
                    # evidence that stock is satisfied, or eligibility ended.
                    kp = old['request']['knowledgePoint']
                    # Outside builds are excluded, not completed. Refills stay
                    # eligible, so captured full stock can verify their jobs.
                    in_scope = (old['request'].get('jobKind', 'build') == 'refill'
                                or (selected is None or kp in selected) and kp in verifiable_builds)
                    present = kp in present_kps and in_scope
                    state = 'rejected' if old.get('state') == 'rejected' else 'verified' if present else 'withdrawn'
                    if old.get('state') != state:
                        save(path, {**old, 'state': state, 'verifiedBasis': inventory['basis']})
            save(cursor_path, {'basis': inventory['basis'], 'lineage': lineage, 'ranking': PRIORITY_POLICY,
                               **({'selection_gate': inventory['selection_gate']} if 'selection_gate' in inventory else {})})

    def _accept_legacy(self, inventory: dict) -> None:
        """Cursor advances only after durable jobs are accepted at this basis."""
        with (self.directory / 'jobs.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            cursor_path = self.directory / 'cursor.json'
            cursor = json.loads(cursor_path.read_text()) if cursor_path.exists() else {}
            lineage = inventory['lineage']
            if cursor.get('lineage', lineage) != lineage:
                raise ValueError('Inventory database lineage changed; reconcile existing jobs before retargeting')
            if inventory['basis'] < cursor.get('basis', 0):
                raise ValueError('Inventory basis regressed')
            current = set()
            for request in inventory['jobs']:
                key = hashlib.sha256(json.dumps([self.learner, request['knowledgePoint'], request['difficulty']]).encode()).hexdigest()
                current.add(key)
                path = self.directory / f'{key}.json'
                old = json.loads(path.read_text()) if path.exists() else {}
                # Restore an interrupted worker; unchanged rejected requests wait
                # for new evidence instead of repeating impossible generation.
                changed = any(old.get('request', {}).get(k) != request.get(k) for k in ('stage', 'missing', 'script'))
                state = old.get('state', 'pending')
                cycle = old.get('cycle', 1)
                # The service manager may lack the interactive shell's PATH.
                # Installing/finding the executable is new operational evidence,
                # not a reason to retain a content-capability rejection.
                if state == 'rejected' and old.get('error') == "[Errno 2] No such file or directory: 'codex'" and Path(self.creator_executable()).is_file():
                    state = 'pending'
                    old = {**old, 'attempts': 0, 'retryAt': 0, 'error': None}
                if state == 'awaiting-verification' and old.get('retryAt', 0) <= time.time():
                    state = 'pending' if old.get('replenishments', 0) < 3 else 'rejected'
                    if state == 'pending':
                        cycle += 1
                if state in {'verified', 'withdrawn'} or state == 'rejected' and changed:
                    state = 'pending'
                    cycle += 1
                    old = {**old, 'attempts': 0, 'replenishments': 0, 'retryAt': 0}
                if state != old.get('state') or {k:v for k,v in request.items() if k != 'basis'} != {k:v for k,v in old.get('request', {}).items() if k != 'basis'}:
                    save(path, {**old, 'key': key, 'learner': self.learner, 'lineage': lineage, 'request': request, 'state': state, 'cycle': cycle})
            for path in self.directory.glob('*.json'):
                if path.stem in current or path.name == 'cursor.json':
                    continue
                old = json.loads(path.read_text())
                if 'request' in old:
                    if old.get('state') == 'blocked':
                        continue
                    state = 'verified' if old['request']['topic'] in inventory['qualifyingTopics'] else 'withdrawn'
                    if old.get('state') != state:
                        save(path, {**old, 'state': state, 'verifiedBasis': inventory['basis']})
            save(self.directory / 'cursor.json', {'basis': inventory['basis'], 'lineage': lineage, 'assessmentStatus': inventory.get('assessmentStatus')})

    @staticmethod
    def recoverable(path: Path, job: dict) -> bool:
        """Saved unfinished drafts retain their inputs even after withdrawal."""
        if not job or job.get('state') in {'verified', 'rejected', 'blocked'}:
            return False
        directory = path.with_suffix('.pipeline') / str(job.get('cycle', 1))
        state_path = directory / 'job.json'
        if state_path.exists():
            state = json.loads(state_path.read_text())
            if state.get('stage') in {'failed', 'blocked'}:
                return (directory / 'publication/request.json').exists()
            return state.get('stage') not in {'verified', 'unsupported'}
        return False

    @staticmethod
    def publication_recovery(path: Path, job: dict) -> bool:
        """Resolve a possible submission before authoring any newly ranked work."""
        if not InventoryJobs.recoverable(path, job):
            return False
        directory = path.with_suffix('.pipeline') / str(job.get('cycle', 1))
        state = json.loads((directory / 'job.json').read_text())
        if state.get('review_after_publication'):
            return False
        return (state.get('stage') == 'push'
                or (directory / 'publication/request.json').exists())

    def finish(self, path: Path, updates: dict, *, cycle=None) -> None:
        with (self.directory / 'jobs.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            current = json.loads(path.read_text())
            if current['state'] not in {'verified', 'withdrawn'} and (cycle is None or current.get('cycle', 1) == cycle):
                save(path, {**current, **updates})

    def run_one(self, lane: str = 'build', slot: int = 0) -> bool:
        """Independent bounded lanes, with one publisher per KP across lanes."""
        if lane not in {'build', 'refill'}:
            raise ValueError('Unknown inventory worker lane: ' + lane)
        limit = build_worker_count(self.environment) if lane == 'build' else 1
        if type(slot) is not int or not 0 <= slot < limit:
            raise ValueError(f'Invalid {lane} worker slot: {slot}')
        review_slots = review_worker_count(self.environment, limit) if lane == 'build' else 0
        prefer_reviews = lane == 'build' and slot >= limit - review_slots
        # Slot zero keeps the original lock so an inherited pre-upgrade worker
        # consumes one of the three slots until it finishes after a restart.
        lock_name = ('worker.lock' if slot == 0 else f'worker-build-{slot}.lock') if lane == 'build' else 'worker-refill.lock'
        lock_path = self.directory / lock_name
        with lock_path.open('a') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return False
            kp_lock = None
            with (self.directory / 'jobs.lock').open('a') as jobs_lock:
                fcntl.flock(jobs_lock, fcntl.LOCK_EX)
                jobs = []
                for path in self.directory.glob('*.json'):
                    job = json.loads(path.read_text())
                    if (job.get('state') in {'pending', 'running'} and job.get('retryAt', 0) <= time.time()
                            and job['request'].get('jobKind', 'build') == lane):
                        jobs.append((path, job))
                def ordering(pair):
                    path, job = pair
                    request = job['request']
                    if 'score' in request or 'priority_policy' in request or 'relevance_tier' in request:
                        rank = priority_key(request)
                    else:
                        # Unrefreshed, pre-score jobs wait behind the current
                        # policy while retaining their old relative ordering.
                        rank = (5, 1, job['state'] != 'running', request.get('urgency', 0),
                                request.get('proximity', 0), -request.get('priority', 0),
                                request['topic'], 0, request['knowledgePoint'], '')
                    # Some existing packages need independent review before the
                    # inexpensive refill lane can run. Pure priority ordering
                    # can starve them behind a continuous lesson backlog. Flex
                    # slots service that queue while the remaining builders keep
                    # the finder order. Immediate deficits and exact publication
                    # recovery retain precedence on every slot. Busy/empty review
                    # queues fall through to ordinary work below.
                    preference = (0 if rank[0] == 0 else
                                  1 + speculative_review(request) if request.get('stage') == 'review-generator'
                                  else 3) if prefer_reviews else 0
                    return (not self.publication_recovery(path, job), preference, *rank, job['key'])
                for path, job in sorted(jobs, key=ordering):
                    candidate_lock = (self.directory / f'kp-{job["request"]["knowledgePoint"]}.lock').open('a')
                    try:
                        fcntl.flock(candidate_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    except BlockingIOError:
                        candidate_lock.close()
                        continue
                    kp_lock = candidate_lock
                    break
                if kp_lock is None:
                    return False
                # Claim under the same lock as admission, using the latest job
                # cycle. The child inherits lane/KP locks across parent restarts.
                attempts = max(1, job.get('attempts', 0) + (job['state'] != 'running'))
                cycle = job.get('cycle', 1)
                save(path, {**job, 'state': 'running', 'attempts': attempts, 'error': None})
            result_path = path.with_suffix('.result')
            if result_path.exists():
                result_path.replace(path.with_suffix(f'.result.previous-{attempts}'))
            from generator_pipeline import python_executable
            command = [python_executable(self.root, self.environment),
                       str(self.root / 'scripts/generator_pipeline.py'),
                       '--inventory-job', str(path), '--inventory-cycle', str(cycle),
                       '--database', self.directory.parent.name]
            override = self.environment.get('COURSE_ACADEMY_GENERATOR_COMMAND')
            if override:
                command = json.loads(override) + [str(path)]
            from generator_lifecycle import create_owner, stopped, OWNER_ENV, INTERRUPTED_EXIT
            with self._active_lock:
                if self._stopping:
                    kp_lock.close()
                    return False
                owner = create_owner(path, cycle)
                self._active_owners.add(owner)
            try:
                with path.with_suffix('.log').open('a') as log:
                    descriptors = (lock.fileno(), kp_lock.fileno())
                    completed = subprocess.run(command, cwd=self.root, stdout=log, stderr=subprocess.STDOUT, timeout=21600, check=False,
                        env={**self.environment, 'COURSE_ACADEMY_GENERATOR_LOCK_FDS': json.dumps(descriptors),
                             OWNER_ENV: str(owner)}, pass_fds=descriptors)
                if completed.returncode == INTERRUPTED_EXIT and stopped(owner):
                    self.finish(path, {'state': 'pending', 'retryAt': 0, 'error': None}, cycle=cycle)
                    return True
                outcome = json.loads(result_path.read_text()) if result_path.exists() else {}
                state = ('blocked' if outcome.get('outcome') in {'blocked', 'failed', 'repair-pending'} else
                         'repair-needed' if lane == 'refill' and outcome.get('needs_repair') else
                         'rejected' if outcome.get('outcome') in {'unsupported', 'finite-limit'} else
                         'awaiting-verification' if completed.returncode == 0 else 'pending')
                failures = job.get('processFailures', 0) + 1 if completed.returncode and not outcome else 0
                if failures >= 3:
                    state = 'blocked'
                    outcome = {'outcome': 'blocked', 'reason': {'code': 'pipeline_process_failed',
                               'error': 'Pipeline failed three times without a structured result; inspect the saved log before resuming.'}}
                rejections = job.get('rejectedVariants', [])
                if state == 'rejected' and lane == 'build':
                    rejections = sorted(set([*rejections, request_variant(job['request'])]))
                self.finish(path, {'state': state, 'attempts': attempts, 'completedAt': time.time(),
                                  'processFailures': failures,
                                  'rejectedVariants': rejections,
                                  'replenishments': job.get('replenishments', 0) + (state == 'awaiting-verification'),
                                  'retryAt': time.time() + min(300, 10 * 2 ** min(attempts, 5)),
                                  'exitCode': completed.returncode, 'outcome': outcome}, cycle=cycle)
                if state == 'blocked':
                    print(json.dumps({'event': 'generator_blocked', 'knowledgePoint': job['request']['knowledgePoint'],
                                      'job': str(path), 'reason': outcome.get('reason')}), file=sys.stderr, flush=True)
            except (OSError, subprocess.SubprocessError, ValueError) as error:
                failures = job.get('processFailures', 0) + 1
                state = 'blocked' if failures >= 3 else 'pending'
                self.finish(path, {'state': state, 'attempts': attempts, 'processFailures': failures,
                                  'retryAt': time.time() + min(300, 10 * 2 ** min(attempts, 5)), 'error': str(error)}, cycle=cycle)
                if state == 'blocked':
                    print(json.dumps({'event': 'generator_blocked', 'knowledgePoint': job['request']['knowledgePoint'],
                                      'job': str(path), 'reason': str(error)}), file=sys.stderr, flush=True)
            finally:
                with self._active_lock:
                    self._active_owners.discard(owner)
                kp_lock.close()
            return True
