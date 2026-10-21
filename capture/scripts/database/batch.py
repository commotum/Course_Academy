"""Whole-activity transactions prepared at one basis, with durable group recovery."""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor

import copy
import traceback
from pathlib import Path

from .client import StaleBasis
from .archive import read_manifest
from .commit import Committer, VerificationError
from .edn import dumps, kw
from .prepare import digest
from .pipeline import jsonable
from ..runtime import StopRequested
from ..storage import atomic_json, atomic_text, read_json

# These memberships are additive. Every other shared mutation starts a new
# batch, even if one observation was a no-op against db-before. This prevents
# an earlier revision from changing what a later activity intended to retain.
APPEND_ONLY = {':knowledge-point/questions', ':topic/knowledge-points'}


class ActivityPreparationError(ValueError):
    def __init__(self, directory, error):
        self.directory = directory
        super().__init__('Preparation failed for capture ' + directory + ': ' + str(error))


def footprint(prepared, snapshot):
    reads = set()
    for entity in snapshot.get('entities', []):
        if set(entity) - {':db/id', ':question/id', ':question/math-academy-id', ':db/ident'}:
            reads.add(entity[':db/id'])
    writes, exclusive = set(), set()
    for batch in prepared['batches']:
        for entity, attr, _ in batch['assertions']:
            writes.add(entity)
            if str(attr) not in APPEND_ONLY:
                exclusive.add(entity)
        for entity, _, _ in batch['retractions']:
            writes.add(entity)
            exclusive.add(entity)
    return reads | writes, exclusive


def compatible(members, prepared, snapshot):
    reads, exclusive = footprint(prepared, snapshot)
    return all(not (exclusive & prior_reads or prior_exclusive & reads)
               for _, prior_prepared, prior_snapshot in members
               for prior_reads, prior_exclusive in [footprint(prior_prepared, prior_snapshot)])


def union(left, right):
    """Union overlapping partial Pulls from exactly the same database value."""
    return _union_owned(_copy_tree(left), right)


def _copy_tree(value):
    # Snapshot collection can share a nested Pull with its top-level entity.
    # Each aggregate path needs independent ownership: deepcopy's shared memo
    # would retain those aliases and let one path's merge change its sibling.
    if isinstance(value, dict):
        return {key: _copy_tree(child) for key, child in value.items()}
    if isinstance(value, list):
        return [_copy_tree(child) for child in value]
    if isinstance(value, tuple):
        return tuple(_copy_tree(child) for child in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value  # Includes immutable EDN keyword/symbol strings.
    return copy.deepcopy(value)


def _union_owned(left, right):
    """Merge into our private aggregate, copying only incoming additions.

    Callers must own the entire left tree. Inputs from member snapshots or
    prepared transactions are never used as mutable aggregates.
    """
    if isinstance(left, dict) and isinstance(right, dict):
        for key, value in right.items():
            left[key] = _union_owned(left[key], value) if key in left else _copy_tree(value)
        return left
    if isinstance(left, list) and isinstance(right, list):
        def key(value):
            return ('entity', value[':db/id']) if isinstance(value, dict) and ':db/id' in value else ('value', dumps(value))
        positions = {key(value): i for i, value in enumerate(left)}
        for value in right:
            index = positions.get(key(value))
            if isinstance(value, dict) and ':db/id' in value:
                if index is not None:
                    left[index] = _union_owned(left[index], value)
                    continue
            if index is None:
                positions[key(value)] = len(left)
                left.append(_copy_tree(value))
        return left
    if isinstance(left, dict) and right == left.get(':db/id'):
        return left
    if isinstance(right, dict) and left == right.get(':db/id'):
        return _copy_tree(right)
    if left != right:
        raise VerificationError('Overlapping batch snapshots disagree at the same basis')
    return left


def combine(members):
    snapshot, groups = None, {}
    for _, prepared, current in members:
        if snapshot is None:
            snapshot = _copy_tree(current)
        else:
            if (current['basis'], current.get('lineage')) != (snapshot['basis'], snapshot.get('lineage')):
                raise VerificationError('Batch preparation spans database values or lineages')
            for key in ('entities', 'facts', 'attributes', 'idents'):
                snapshot[key] = _union_owned(snapshot.get(key, []), current.get(key, []))
        for batch in prepared['batches']:
            group = groups.setdefault(batch['source'], {'source': batch['source'], 'forms': [],
                                                       'assertions': [], 'retractions': []})
            for key in ('forms', 'assertions', 'retractions'):
                group[key].extend(_copy_tree(batch[key]))
    for batch in groups.values():
        updates, forms, other_forms = {}, [], set()
        for form in batch['forms']:
            if isinstance(form, dict):
                target = form[kw('db/id')]
                if target not in updates:
                    updates[target] = len(forms)
                    forms.append(form)
                else:
                    index = updates[target]
                    forms[index] = _union_owned(forms[index], form)
            elif dumps(form) not in other_forms:
                other_forms.add(dumps(form))
                forms.append(form)
        batch['forms'] = forms
        for key in ('assertions', 'retractions'):
            batch[key] = list({dumps(row): row for row in batch[key]}.values())
    return list(groups.values()), snapshot


def size(batch):
    # Count expanded facts, removals and explicit ensures, rather than counting
    # each entity map as just one operation. Native preview remains authoritative.
    return {'bytes': len((dumps(batch['forms']) + '\n').encode()),
            'ops': len(batch['assertions']) + len(batch['retractions'])
                   + sum(len(form.get(kw('db/ensure'), [])) for form in batch['forms'] if isinstance(form, dict))}


def question_ids(content):
    return {q.get('math_academy_id') or q.get('capture_key') or digest(q)
            for bucket in ('questions', 'reference_questions', 'canonical_examples') for q in content.get(bucket, [])}


def question_count(content):
    return len(question_ids(content))


def supported_question_ids(prepared):
    # Explicitly exclude omissions, matching the status viewer's import set.
    omitted = {str(row['id']) for row in prepared.get('omissions', [])
               if row.get('kind') == 'question' and row.get('id')}
    return question_ids(prepared['content']) - omitted


class ActivityBatch:
    def __init__(self, pipeline, directory):
        self.pipeline, self.directory = pipeline, Path(directory)
        self.config = pipeline.config
        self.committer = Committer(self.config, pipeline.client, self.directory)
        self.manifest_path = self.directory / 'manifest.json'

    def prepare(self, member, basis, snapshot=None):
        directory = Path(member['directory']) / 'database'
        if snapshot is None:
            prepared, snapshot = self.pipeline._prepare(member['content'], directory, basis)
        else:
            prepared, snapshot = self.pipeline._prepare_snapshot(member['content'], directory, snapshot)
        atomic_json(directory / 'preparation.json', jsonable({k: v for k, v in prepared.items() if k != 'batches'}))
        atomic_text(directory / 'prepared-batches.edn', dumps(prepared['batches']))
        return member, prepared, snapshot

    def prepare_many(self, members, basis):
        factory = getattr(self.pipeline.client, 'snapshot_reader', None)
        if factory is None:
            for member in members:
                yield self.prepare(member, basis)
            return
        reader = factory(basis)
        # Parallelize only independent reads. Conversion, agent decisions,
        # preview, durable intent, submission and verification remain ordered.
        with ThreadPoolExecutor(max_workers=4) as pool:
            for start in range(0, len(members), 4):
                group = members[start:start + 4]
                futures = [pool.submit(reader.snapshot, member['content'],
                    Path(member['directory']) / 'database' / ('snapshot-' + str(basis)), basis)
                    for member in group]
                for member, future in zip(group, futures):
                    yield self.prepare(member, basis, future.result())

    def select(self, directories, allow_underfilled):
        basis = self.pipeline.client.basis()
        members, deferred, questions, boundary = [], [], set(), 'queue_end'
        candidates = []
        for path in directories:
            path = Path(path).resolve()
            if not (path / 'capture-complete.json').exists():
                raise ValueError('Only complete captures can enter a batch')
            content = read_json(path / 'content.json')
            if not isinstance(content, dict):
                raise ValueError('Completed capture has no content record')
            member = {'directory': str(path), 'content': self.pipeline._with_post_activity_base(content, path)}
            candidates.append(member)
        preparations = self.prepare_many(candidates, basis)
        for member in candidates:
            try:
                candidate = next(preparations)
            except StopRequested:
                raise
            except Exception as error:
                # A failed preparation is not an underfilled queue. Retain the
                # blocker and its exact capture so the outbox exposes it and
                # backs off instead of repeating a silent successful prefix.
                raise ActivityPreparationError(member['directory'], error) from error
            if (not compatible(members, candidate[1], candidate[2]) or
                    not compatible(deferred, candidate[1], candidate[2])):
                # Defer this revision and anything depending on it, but keep
                # collecting unrelated activities. Neither can overtake a
                # conflicting earlier observation under EDB's set semantics.
                deferred.append(candidate)
                boundary = 'shared_content_revision'
                continue
            batches, _ = combine(members + [candidate])
            sizes = [size(batch) for batch in batches]
            if any(s['bytes'] > self.config.database_batch_max_bytes or s['ops'] > self.config.database_batch_max_ops for s in sizes):
                if members:
                    deferred.append(candidate)
                    boundary = 'safety_limit'
                    continue
                raise ValueError('A complete activity exceeds database batch safety limits; retained without splitting')
            members.append(candidate)
            questions.update(supported_question_ids(candidate[1]))
            if len(questions) >= self.config.database_batch_questions:
                boundary = 'question_minimum'
                break
        preparations.close()
        manifest = {'members': [m for m, _, _ in members], 'boundary': boundary,
                    'questions': len(questions), 'status': 'pending', 'source_repairs': {}}
        for member, prepared, _ in members:
            manifest['source_repairs'][member['directory']] = prepared.get('source_repairs', [])
        if len(questions) >= self.config.database_batch_questions or allow_underfilled:
            atomic_json(self.manifest_path, manifest)
        return manifest, members

    def accumulating(self, manifest):
        return {'status': 'accumulating', 'questions': manifest['questions'],
                'minimum_questions': self.config.database_batch_questions,
                'candidate_activities': len(manifest['members']), 'boundary': manifest['boundary'],
                'reason': 'Waiting for enough distinct supported questions in compatible whole activities'}

    def receipts(self):
        return [read_json(path) for path in sorted((self.directory / 'requests').glob('*/result.json'))
                if read_json(path).get('status') in ('verified', 'confirmed_needs_reconciliation')]

    def verify(self, manifest, request, receipt):
        result = self.committer.verify_receipt(request, receipt)
        members = list(self.prepare_many(manifest['members'], receipt[':edb/db-after-t']))
        remaining = any(b['source'] == request['source'] for _, p, _ in members for b in p['batches'])
        status = 'confirmed_needs_reconciliation' if remaining else 'verified'
        result.update(status=status, basis_before=request['basis'], basis_after=receipt[':edb/db-after-t'],
                      request_key=request['request_key'], batch_directory=str(self.directory),
                      activities=len(members), reimport_is_noop=not remaining)
        atomic_json(self.directory / 'verification.json', result)
        # Install each activity's evidence before retiring group intent. A crash
        # during fan-out replays the same exact request and completes the copies.
        for member, _, _ in members:
            directory = Path(member['directory']) / 'database'
            archive = directory / 'requests' / request['request_key']
            atomic_json(archive / 'request.json', request)
            atomic_text(archive / 'receipt.edn', dumps(receipt))
            atomic_json(archive / 'result.json', result)
            atomic_json(directory / 'verification.json', result)
        self.committer.retire(request, status, result)

    def process(self, directories, *, allow_underfilled=False):
        manifest = read_manifest(self.manifest_path)
        try:
            if manifest and manifest.get('status') in ('verified', 'no_changes'):
                return manifest['result']
            if (manifest and not self.committer.pending() and not self.receipts()
                    and (manifest.get('status') == 'accumulating'
                         or manifest['questions'] < self.config.database_batch_questions)):
                manifest = None  # An unsubmitted small group can gather new work.
            if not manifest:
                manifest, members = self.select(directories, allow_underfilled)
                if (not allow_underfilled and manifest['questions'] < self.config.database_batch_questions
                        and any(p['batches'] for _, p, _ in members)):
                    return self.accumulating(manifest)
            else:
                members = None
            content_hash = digest(manifest['members'])
            for _ in range(6):
                request = self.committer.pending()
                if request:
                    if request['content_sha256'] != content_hash:
                        raise VerificationError('Batch manifest differs from the saved exact request')
                    try:
                        receipt = self.committer.submit(request)
                    except StaleBasis as error:
                        self.committer.retire(request, 'rejected_stale_basis', {'reason': str(error)})
                        members = None
                        continue
                    self.verify(manifest, request, receipt)
                    members = None
                if members is None:
                    basis = self.pipeline.client.basis()
                    members = list(self.prepare_many(manifest['members'], basis))
                for i, (member, prepared, snapshot) in enumerate(members):
                    if not compatible(members[:i], prepared, snapshot):
                        raise VerificationError('Batch now contains conflicting activity revisions; retaining it for reconciliation')
                    manifest['source_repairs'].setdefault(member['directory'], []).extend(prepared.get('source_repairs', []))
                atomic_json(self.manifest_path, manifest)
                batches, snapshot = combine(members)
                if not batches:
                    receipts = self.receipts()
                    status = 'verified' if receipts else 'no_changes'
                    results = {}
                    for member, prepared, _ in members:
                        result = {'status': status, 'basis': snapshot['basis'], 'receipts': receipts,
                                  'omissions': prepared['omissions'], 'calibration': prepared['calibration'],
                                  'batch_directory': str(self.directory), 'batch_activities': len(members),
                                  'content_sha256': digest(member['content'])}
                        directory = Path(member['directory']) / 'database'
                        atomic_json(directory / 'result.json', result)
                        self.pipeline._persist_source_repairs(member['directory'], directory, manifest['source_repairs'][member['directory']])
                        results[member['directory']] = result
                    result = {'status': status, 'activities': results, 'batch_directory': str(self.directory),
                              'questions': manifest['questions'], 'boundary': manifest['boundary']}
                    manifest.update(status=status, result=result)
                    atomic_json(self.manifest_path, manifest)
                    return result
                # The raw queue estimate is only an admission shortcut. Enforce
                # the floor again on supported, deduplicated preparation before
                # a first request. Already saved intents must still be recovered.
                supported = set().union(*(supported_question_ids(p) for _, p, _ in members))
                if (not allow_underfilled and len(supported) < self.config.database_batch_questions
                        and not self.receipts()):
                    manifest['questions'] = len(supported)
                    manifest['status'] = 'accumulating'
                    atomic_json(self.manifest_path, manifest)
                    return self.accumulating(manifest)
                batch = batches[0]
                limits = size(batch)
                if limits['bytes'] > self.config.database_batch_max_bytes or limits['ops'] > self.config.database_batch_max_ops:
                    raise ValueError('Reprepared whole-activity batch exceeds safety limits; retained without splitting')
                try:
                    self.committer.preview(batch, snapshot)
                except StaleBasis:
                    members = None
                    continue
                atomic_json(self.directory / 'batch-size.json', {**limits, 'activities': len(members),
                            'questions': manifest['questions'], 'source': batch['source'], 'basis': snapshot['basis']})
                request = self.committer.save_request(batch, snapshot, content_hash)
                # Return to the recovery path: every submission uses saved intent.
                members = None
            raise ValueError('Database contention; saved activity batch will be retried')
        except StopRequested:
            raise
        except Exception as error:
            request = self.committer.pending()
            affected = [member['directory'] for member in (manifest or {}).get('members', [])]
            if isinstance(error, ActivityPreparationError):
                affected = [error.directory]
            result = {'status': 'pending', 'reason': str(error), 'error_type': type(error).__name__,
                      'unknown_or_unverified_commit': bool(request),
                      'request_key': request.get('request_key') if request else None,
                      'batch_directory': str(self.directory),
                      'activities': {directory: {'status': 'pending', 'reason': str(error)}
                                     for directory in affected}}
            atomic_json(self.directory / 'pending.json', {**result, 'traceback': traceback.format_exc()})
            return result
