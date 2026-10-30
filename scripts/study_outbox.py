"""Durably admit study interactions before the single EDB writer is available.

The native projection runs the normal lesson/assessment/assignment planner.
This file owns transport, atomic acknowledgement, ordered replay and recovery;
it never duplicates grading or stopping rules.
"""
from __future__ import annotations
import copy
from contextlib import contextmanager
import fcntl
import json
from pathlib import Path
import threading
import time
import uuid


class StudyOutbox:
    ACTIONS = {'queue', 'answer', 'continue', 'pause', 'resume', 'skip', 'start', 'study-topic',
               'review-topic', 'profile-settings', 'daily-xp-goal', 'target', 'queue-topic',
               'assignment-focus', 'assignment-answer', 'assignment-pause',
               'draft', 'navigate', 'submit', 'expire', 'regenerate-assessment'}

    def __init__(self, directory, grader, writer, save, stop, refresh=lambda: None):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.grader, self.writer, self.save = grader, writer, save
        self.stop, self.refresh = stop, refresh
        self.lock = threading.RLock()
        self.writer_lock = threading.Lock()
        self.wake = threading.Event()
        self.state_path = self.directory / 'study.json'

    @contextmanager
    def locked(self):
        with self.lock, (self.directory / 'study.lock').open('a') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            yield

    def load(self):
        if self.state_path.exists():
            return json.loads(self.state_path.read_text())
        return {'operations': [], 'overlay': None, 'views': {}, 'aliases': {}, 'retryAt': 0}

    def pending(self, state):
        return [op for op in state['operations'] if not op.get('saved')]

    def save_state(self, state):
        pending = self.pending(state)
        return {'status': 'error' if state.get('error') else 'pending' if pending else 'saved',
                'pending': len(pending), 'error': state.get('error'),
                'retrying': any(op.get('lastError') for op in pending)}

    def with_status(self, state, view):
        value = copy.deepcopy(view)
        value['saveState'] = self.save_state(state)
        if not self.pending(state):
            value['idAliases'] = copy.deepcopy(state['aliases'])
        return value

    def decorate(self, view):
        with self.locked():
            return self.with_status(self.load(), view)

    def task_view(self, task):
        with self.locked():
            state = self.load()
            if not self.pending(state):
                return None
            view = state['views'].get(str(task))
            if view is None:
                view = state['views'].get(str(state['aliases'].get(str(task))))
            if view is not None and view.get('status') == 'started' and view.get('step', {}).get('status') == 'started':
                local = (state['overlay'] or {}).get('entities', {})
                aliases = {key: value for key, value in state['aliases'].items() if key not in local}
                operation = self.normalize_ids({'action': 'task', 'taskId': task}, aliases)
                result = self.grader.request({'action': 'study-read', 'operation': operation, 'overlay': state['overlay'],
                                             'aliases': state['aliases'], 'committedBasis': state.get('committedBasis', 0)})
                if not result.get('ok'):
                    raise ValueError(result.get('error', 'Unable to read saved study progress'))
                view = result['data']
            return self.with_status(state, view) if view is not None else None

    def overlay_view(self, action, body):
        if action == 'task':
            value = self.task_view(body['taskId'])
            if value is not None:
                return value
        if action not in {'home', 'queue', 'task', 'profile', 'learner', 'assignment', 'assignments',
                          'activity-history', 'activity-history-detail', 'study-stats', 'topic-study-availability'}:
            return None
        with self.locked():
            state = self.load()
            if not self.pending(state) and not state.get('committedBasis'):
                return None
            local = (state['overlay'] or {}).get('entities', {})
            aliases = {key: value for key, value in state['aliases'].items() if key not in local}
            operation = self.normalize_ids(body, aliases)
            result = self.grader.request({'action': 'study-read', 'operation': operation, 'overlay': state['overlay'],
                                          'aliases': state['aliases'], 'committedBasis': state.get('committedBasis', 0)})
            if not result.get('ok'):
                raise ValueError(result.get('error', 'Unable to read locally saved study progress'))
            return self.with_status(state, result['data'])

    def status(self, task=None):
        with self.locked():
            return self.save_state(self.load())

    def retry(self, task=None):
        with self.locked():
            state = self.load()
            state.pop('error', None)
            state['retryAt'] = 0
            self.save(self.state_path, state)
        self.wake.set()
        return self.status(task)

    def normalize_ids(self, value, aliases):
        if isinstance(value, dict):
            return {key: aliases.get(str(item), item) if key in {'taskId', 'itemId', 'activityId', 'questionId', 'entityId', 'choiceId', 'fieldId', 'id'} and type(item) is int
                    else self.normalize_ids(item, aliases) for key, item in value.items()}
        if isinstance(value, list):
            return [self.normalize_ids(item, aliases) for item in value]
        return value

    def resolve_ids(self, body):
        with self.locked():
            state = self.load()
            local = (state.get('overlay') or {}).get('entities', {})
            aliases = {key: value for key, value in state['aliases'].items() if key not in local}
            return self.normalize_ids(body, aliases)

    def receipt_path(self, request):
        return self.directory / 'receipts' / f'{request}.json'

    def request(self, body, now=None):
        if body.get('action') not in self.ACTIONS:
            return None
        request = body.get('requestId', '')
        if not isinstance(request, str) or not 8 <= len(request) <= 128 or not all(c.isascii() and (c.isalnum() or c == '-') for c in request):
            raise ValueError('A stable request ID is required')
        now = int(time.time() * 1000) if now is None else now
        with self.locked():
            state = self.load()
            prior = next((op for op in state['operations'] if op['requestId'] == request), None)
            receipt = self.receipt_path(request)
            if prior is None and receipt.exists():
                prior = json.loads(receipt.read_text())
            if prior:
                if prior['input'] != body:
                    raise ValueError('Request ID already used for another study interaction')
                return copy.deepcopy(prior['response'])
            if state.get('error'):
                raise ValueError('Study saving needs attention: ' + state['error'])
            local = (state['overlay'] or {}).get('entities', {})
            aliases = {key: value for key, value in state['aliases'].items() if key not in local}
            operation = self.normalize_ids(body, aliases)
            projected = self.grader.request({'action': 'study-project', 'operation': operation,
                                             'overlay': state['overlay'], 'receivedAt': now,
                                             'aliases': state['aliases'], 'committedBasis': state.get('committedBasis', 0)})
            if not projected.get('ok'):
                return {'_error': projected.get('error', 'Unable to update study'),
                        '_code': projected.get('code', 'validation')}
            data = projected['data']
            state['overlay'] = data['overlay']
            state['views'].update(data.get('views', {}))
            view = data['view']
            if type(view.get('taskId')) is int:
                state['views'][str(view['taskId'])] = copy.deepcopy(view)
            if body['action'] == 'profile-settings':
                state['profile'] = copy.deepcopy(view)
            if body['action'] in {'profile-settings', 'target', 'queue-topic', 'daily-xp-goal'}:
                state['learner'] = {'basis': view.get('basis'), 'learner': copy.deepcopy(view.get('learner'))}
            op = {'requestId': request, 'input': copy.deepcopy(body), 'operation': data['operation'],
                  'saved': False, 'receivedAt': now}
            state['operations'].append(op)
            response = self.with_status(state, view)
            op['response'] = copy.deepcopy(response)
            # Both the exact acknowledgement and its recoverable native plan
            # reach local durable storage before the HTTP request can complete.
            self.save(self.state_path, state)
            self.wake.set()
            return response

    def run_one(self):
        # Separate admission and writer locks: a hung EDB write never prevents
        # another answer, Next, page reload, or process from admitting progress.
        if not self.writer_lock.acquire(blocking=False):
            return False
        try:
            with (self.directory / 'writer.lock').open('a') as writer_lock:
                try:
                    fcntl.flock(writer_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    return False
                with self.locked():
                    state = self.load()
                    pending = self.pending(state)
                    if not pending or state.get('error') or state.get('retryAt', 0) > time.time():
                        return False
                    op = copy.deepcopy(pending[0])
                try:
                    result = self.writer.request({'action': 'persist-study', 'operation': op['operation']})
                except (OSError, ValueError) as error:
                    result = {'ok': False, 'code': 'unavailable', 'error': str(error)}
                with self.locked():
                    state = self.load()
                    current = next(row for row in state['operations'] if row['requestId'] == op['requestId'])
                    if result.get('ok'):
                        current['saved'] = True
                        current['savedAt'] = int(time.time() * 1000)
                        current.pop('lastError', None)
                        state['retryAt'] = 0
                        data = result.get('data', {})
                        state['aliases'].update(data.get('aliases', {}))
                        state['committedBasis'] = max(state.get('committedBasis', 0), data.get('basis', 0))
                        if not self.pending(state):
                            state['views'] = {key: self.normalize_ids(value, state['aliases']) for key, value in state['views'].items()}
                            if data.get('view', {}).get('taskId') is not None:
                                view = data['view']
                                state['views'][str(view['taskId'])] = view
                                for local, durable in state['aliases'].items():
                                    if durable == view['taskId'] and local in state['views']:
                                        state['views'][local] = copy.deepcopy(view)
                            state['overlay'] = None
                    elif result.get('code') == 'basis-conflict':
                        # Recompute only after the writer proves this exact
                        # attempt was rejected, never after an unknown outcome.
                        current['operation']['requestId'] = str(uuid.uuid4())
                        state['retryAt'] = time.time() + .1
                    elif result.get('code') == 'unavailable':
                        current['lastError'] = result.get('error', 'Saving temporarily unavailable')
                        state['retryAt'] = time.time() + 2
                    else:
                        state['error'] = result.get('error', 'Study save failed')
                    if result.get('ok'):
                        # Receipt first, then prune. A crash between these writes
                        # replays the same already-committed request safely.
                        self.save(self.receipt_path(current['requestId']), current)
                        state['operations'] = [row for row in state['operations'] if row['requestId'] != current['requestId']]
                        if not self.pending(state):
                            state['views'] = {}
                            state.pop('profile', None)
                            state.pop('learner', None)
                    self.save(self.state_path, state)
                if result.get('ok'):
                    self.refresh()
                return True
        finally:
            self.writer_lock.release()

    def loop(self):
        while not self.stop.is_set():
            try:
                if self.run_one():
                    continue
            except Exception as error:
                print(f'Study persistence deferred: {error}', flush=True)
            self.wake.wait(.5)
            self.wake.clear()

    def drain(self, timeout=55, *, pause_active=False):
        # Kept for explicit shutdown/admin callers. Ordinary study transitions
        # use this same ordered stream and must never drain before admission.
        deadline = time.monotonic() + timeout
        self.wake.set()
        while time.monotonic() < deadline:
            status = self.status()
            if status['error']:
                raise ValueError('A study save needs attention: ' + status['error'])
            if not status['pending']:
                return
            if self.stop.wait(.05):
                raise ValueError('Study saving is restarting; retry shortly')
        raise ValueError('Study progress is safely queued; saving has not finished yet')
