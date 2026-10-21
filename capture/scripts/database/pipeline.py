"""Independent database outbox work; capture never waits for its durability."""
from __future__ import annotations
import copy
import json
import tempfile
import traceback
from pathlib import Path
from .client import EDBClient, StaleBasis
from .commit import Committer, VerificationError
from .edn import dumps, loads
from .images import ImageLibrary
from .prepare import Preparation, digest, MA_SOURCE
from ..storage import atomic_json, atomic_text, read_json
from ..activity.evidence import question_key
from ..activity.task_payload import semantic_identity


def jsonable(value):
    return json.loads(json.dumps(value, default=str))


class DatabasePipeline:
    def __init__(self, config, stop_event, *, client=None, resolver=None):
        self.config, self.stop_event = config, stop_event
        self.client = client or EDBClient(config, stop_event)
        self.resolver = resolver

    def context(self, activity):
        # Unique read directories make simultaneous context and commit reads independent.
        root = Path(self.config.state_root) / 'database-context'
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='read-', dir=root) as directory:
            return self.client.context(activity, directory)

    def source_dependencies(self, questions):
        root = Path(self.config.state_root) / 'database-context'
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='source-dependencies-', dir=root) as directory:
            return self.client.source_dependencies(questions, directory)

    def question_topic(self, question_id):
        root = Path(self.config.state_root) / 'database-context'
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='question-topic-', dir=root) as directory:
            return self.client.question_topic(question_id, directory)

    def targets(self):
        root = Path(self.config.state_root) / 'database-context'
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='targets-', dir=root) as directory:
            return self.client.targets(directory)

    def _resolver(self, directory):
        def resolve(task, payload):
            path = directory / 'decisions' / (digest([task,payload]) + '.json')
            saved = read_json(path)
            if saved is not None:
                return saved
            if self.resolver:
                result = self.resolver(task, jsonable(payload))
            else:
                from ..activity.solver import SolverClient
                result = SolverClient(self.config, directory / 'source-resolution', self.stop_event).request(task, jsonable(payload))
            atomic_json(path, result)
            return result
        return resolve

    def _prepare(self, content, directory, basis):
        snapshot = self.client.snapshot(content, directory / ('snapshot-' + str(basis)), basis)
        return self._prepare_snapshot(content, directory, snapshot)

    def _prepare_snapshot(self, content, directory, snapshot):
        library = ImageLibrary(self.config.math_root, directory.parent)
        def record_source_evidence(proof):
            path = directory / 'source-evidence' / (digest(proof) + '.edn')
            atomic_text(path, dumps(proof))
            return str(path.resolve())
        prepared = Preparation(snapshot, resolve=self._resolver(directory),
                               record_source_evidence=record_source_evidence).prepare(
            content, library, getattr(self.config, 'derived_source', None))
        return prepared, snapshot

    def _verify(self, committer, request, receipt, content, directory):
        result = committer.verify_receipt(request, receipt)
        after = receipt[':edb/db-after-t']
        prepared, _ = self._prepare(content, directory, after)
        remaining = [b for b in prepared['batches'] if b['source'] == request['source']]
        if remaining:
            result.update(status='confirmed_needs_reconciliation', basis_before=request['basis'],
                          basis_after=after, request_key=request['request_key'],
                          reason='Committed receipt is valid; content readback requires fresh preparation')
            atomic_json(directory / 'verification.json', result)
            committer.retire(request, 'confirmed_needs_reconciliation', result)
            return result
        result.update(basis_before=request['basis'], basis_after=after, reimport_is_noop=True,
                      request_key=request['request_key'])
        atomic_json(directory / 'verification.json', result)
        committer.retire(request, 'verified', result)
        return result

    def _with_post_activity_base(self, content, capture_directory):
        """Supplement missing source XP from this task's saved completion only."""
        if content.get('base_xp') is not None or content.get('task_id') is None:
            return content
        path = Path(capture_directory) / 'post-activity.json'
        post = read_json(path, {})
        completion = post.get('completion', {}) if isinstance(post, dict) else {}
        if not isinstance(completion, dict) or str(completion.get('task_id')) != str(content['task_id']):
            return content
        base = completion.get('base_xp')
        if isinstance(base, bool) or not isinstance(base, (int, float)) or not base > 0 or int(base) != base:
            return content
        supplemented = copy.deepcopy(content)
        supplemented['base_xp'] = base
        supplemented['base_xp_evidence'] = {'source_file': str(path.resolve()),
            'task_id': str(content['task_id']), 'source_text': completion.get('source_text')}
        return supplemented

    def _persist_source_repairs(self, capture_directory, directory, repairs):
        """After verification, retain source-backed preparation repairs in capture."""
        if not repairs or (directory / 'request.json').exists():
            return
        path = Path(capture_directory) / 'content.json'
        content = read_json(path)
        updated = copy.deepcopy(content)
        applied = []
        for repair in repairs:
            records = updated.get(repair['record_kind'], [])
            original = next((q for q in records if question_key(q) == repair['capture_key']), None)
            if original is None or semantic_identity('preparation_source', original) != repair['source_evidence_hash']:
                continue
            original['answer_fields'] = copy.deepcopy(repair['question']['answer_fields'])
            original.pop('fields', None)
            original['preparation_answer_repair'] = {'source_evidence_hash': repair['source_evidence_hash'],
                'judgment': copy.deepcopy(repair['judgment']), 'source_file': str(directory / 'source-repairs.json')}
            original.pop('answer_validation', None)
            original['answer_validation'] = {'status': 'supported', 'version': 1,
                'evidence_hash': semantic_identity('finalized_source', original),
                'method': 'verified_preparation_repair'}
            applied.append(repair)
        if applied:
            archive = directory / 'source-repairs' / digest(content)
            if not (archive / 'original-content.json').exists():
                atomic_json(archive / 'original-content.json', content)
            atomic_json(directory / 'source-repairs.json', applied)
            atomic_json(path, updated)

    def process(self, capture_directory, apply=True):
        directory = Path(capture_directory) / 'database'
        directory.mkdir(parents=True, exist_ok=True)
        committer = Committer(self.config, self.client, directory)
        try:
            if not (Path(capture_directory) / 'capture-complete.json').exists():
                return {'status': 'pending', 'reason': 'Capture has not durably completed', 'database_writes': 0}
            content = read_json(Path(capture_directory) / 'content.json')
            if not isinstance(content, dict):
                raise ValueError('Completed capture has no content record')
            content = self._with_post_activity_base(content, capture_directory)
            if str(self.config.source) != MA_SOURCE:
                raise ValueError('Math Academy originals require :org/Math-Academy')
            raw_hash = digest(content)
            results, source_repairs = [], []
            for attempt in range(6):
                request = committer.pending()
                if request:
                    if request['content_sha256'] != raw_hash:
                        # Use saved immutable content to verify the original outcome first.
                        original = read_json(directory / 'request-content.json')
                        if original is None or digest(original) != request['content_sha256']:
                            raise VerificationError('Original content for the pending request is unavailable')
                    else:
                        original = content
                    if not apply:
                        return {'status': 'pending', 'reason': 'Exact saved request awaits recovery', 'request_key': request['request_key']}
                    try:
                        receipt = committer.submit(request)
                    except StaleBasis as error:
                        committer.retire(request, 'rejected_stale_basis', {'reason': str(error)})
                        continue
                    results.append(self._verify(committer, request, receipt, original, directory))
                basis = self.client.basis()
                prepared, snapshot = self._prepare(content, directory, basis)
                source_repairs.extend(prepared.get('source_repairs', []))
                atomic_json(directory / 'preparation.json', jsonable({k:v for k,v in prepared.items() if k != 'batches'}))
                atomic_text(directory / 'prepared-batches.edn', dumps(prepared['batches']))
                if not prepared['batches']:
                    result = {'status': 'verified' if results else 'no_changes', 'basis': basis,
                              'receipts': results, 'omissions': prepared['omissions'], 'calibration': prepared['calibration']}
                    atomic_json(directory / 'result.json', result)
                    if apply:
                        self._persist_source_repairs(capture_directory, directory, source_repairs)
                    return result
                batch = prepared['batches'][0]
                try:
                    committer.preview(batch, snapshot)
                except StaleBasis:
                    continue
                if not apply:
                    return {'status': 'previewed', 'basis': basis, 'source': batch['source'],
                            'batches': len(prepared['batches']), 'omissions': prepared['omissions']}
                atomic_json(directory / 'request-content.json', content)
                request = committer.save_request(batch, snapshot, raw_hash)
                try:
                    receipt = committer.submit(request)
                except StaleBasis as error:
                    committer.retire(request, 'rejected_stale_basis', {'reason': str(error)})
                    continue
                results.append(self._verify(committer, request, receipt, content, directory))
            return {'status': 'pending', 'reason': 'Database contention; saved capture will be retried', 'receipts': results}
        except Exception as error:
            from ..runtime import StopRequested
            if isinstance(error, StopRequested):
                raise
            request = committer.pending()
            result = {'status': 'pending', 'reason': str(error), 'error_type': type(error).__name__,
                      'unknown_or_unverified_commit': bool(request),
                      'request_key': request.get('request_key') if request else None}
            atomic_json(directory / 'pending.json', {**result, 'traceback': traceback.format_exc()})
            return result

    def process_batch(self, capture_directories, batch_directory, *, allow_underfilled=False):
        from .batch import ActivityBatch
        return ActivityBatch(self, batch_directory).process(capture_directories, allow_underfilled=allow_underfilled)
