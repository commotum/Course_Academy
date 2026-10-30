"""Durably admit study interactions before the single EDB writer is available.

The native projection runs the normal lesson/assessment/assignment planner.
This file owns transport, atomic acknowledgement, ordered replay and recovery;
it never duplicates grading or stopping rules.
"""
from __future__ import annotations
import copy
from contextlib import contextmanager, nullcontext
import fcntl
import heapq
import os
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

    def __init__(self, directory, grader, writer, save, stop, refresh=lambda: None, *, planner=None, publication=None):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.grader, self.writer, self.save = grader, writer, save
        self.planner = planner if planner is not None else grader
        self.publication = publication if publication is not None else lambda: nullcontext(True)
        self.stop, self.refresh = stop, refresh
        self.lock = threading.RLock()
        self.writer_lock = threading.Lock()
        self.planning_lock = threading.Lock()
        self.wake = threading.Event()
        self.state_path = self.directory / 'study.json'
        self.restore_home_cache()

    @contextmanager
    def locked(self):
        with self.lock, (self.directory / 'study.lock').open('a') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            yield

    def load(self):
        if self.state_path.exists():
            return json.loads(self.state_path.read_text())
        return {'operations': [], 'overlay': None, 'views': {}, 'aliases': {}, 'retryAt': 0}

    def commit_state(self, state):
        state['revision'] = state.get('revision', 0) + 1
        self.save(self.state_path, state)

    def restore_home_cache(self):
        # Upgrade the display cache from existing acknowledgements. Only the
        # newest64 receipt bodies are inspected; no EDB work or learner intent
        # is created, and exact-retry receipts remain immutable.
        with self.locked():
            state = self.load()
            if isinstance(state.get('home'), dict):
                return
            rows = list(state['operations'])
            directory = self.directory / 'receipts'
            if directory.exists():
                with os.scandir(directory) as entries:
                    recent = heapq.nlargest(64, (entry for entry in entries if entry.is_file() and entry.name.endswith('.json')),
                                           key=lambda entry: entry.stat().st_mtime_ns)
                for entry in recent:
                    try:
                        rows.append(json.loads(Path(entry.path).read_text()))
                    except (OSError, ValueError):
                        continue  # A display cache can safely fall back to a read.
            rows = list({row.get('requestId'): row for row in rows if row.get('requestId')}.values())
            homes = [row for row in rows if row.get('input', {}).get('action') == 'queue'
                     and isinstance(row.get('response', {}).get('activities'), list)]
            if not homes:
                return
            source = max(homes, key=lambda row: (row.get('receivedAt', 0), row['requestId']))
            state['home'] = copy.deepcopy(source['response'])
            state['homeTasks'] = {}
            ordered = sorted((row for row in rows if row.get('receivedAt', 0) >= source.get('receivedAt', 0)),
                             key=lambda row: (row.get('receivedAt', 0), row['requestId']))
            for row in ordered:
                if isinstance(row.get('response'), dict):
                    self.record_home_updates(state, row['response'], row['requestId'])
            self.save(self.state_path, state)

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

    def home_view(self, state):
        if not isinstance(state.get('home'), dict):
            return None
        home = copy.deepcopy(state['home'])
        local = (state['overlay'] or {}).get('entities', {})
        aliases = {key: value for key, value in state['aliases'].items() if key not in local}
        home = self.normalize_ids(home, aliases)
        if state.get('homeLearner') is not None:
            home['learner'] = copy.deepcopy(state['homeLearner'])
        if 'homeCourse' in state:
            home['course'] = copy.deepcopy(state['homeCourse'])
            home['needsCourseSelection'] = state['homeCourse'] is None
        activities = home.setdefault('activities', [])
        waiting = home.setdefault('waitingActivities', [])
        for saved in state.get('homeTasks', {}).values():
            task = self.normalize_ids(saved, aliases)
            task_id, activity_id = task.get('taskId'), task.get('activityId')
            matches = lambda row: row.get('taskId') == task_id or (row.get('taskId') is None and activity_id is not None and row.get('activityId') == activity_id)
            terminal = task.get('status') in {'completed', 'failed', 'locked'}
            existing = next((row for row in activities if matches(row)), None)
            if terminal or task.get('awaitingQuestions'):
                activities[:] = [row for row in activities if not matches(row)]
                waiting[:] = [row for row in waiting if row.get('taskId') != task_id]
                if task.get('awaitingQuestions'):
                    waiting.append({'taskId': task_id, 'activityId': activity_id, 'title': task.get('title', ''),
                                    'pendingCount': len(task.get('deferredSteps') or []),
                                    'canResumePractice': task.get('canResumePractice', False)})
            elif task.get('status') in {'started', 'paused'}:
                if existing is None:
                    existing = {'activityId': activity_id, 'taskId': task_id, 'type': task.get('type'),
                                'title': task.get('title', ''), 'reason': 'Continue your activity'}
                    activities.insert(0, existing)
                for key in ('taskId', 'activityId', 'type', 'title', 'status', 'progress', 'xpBase'):
                    if key in task:
                        existing[key] = copy.deepcopy(task[key])
                waiting[:] = [row for row in waiting if row.get('taskId') != task_id]
        return self.with_status(state, home)

    def remember_home(self, view):
        if not isinstance(view, dict) or not isinstance(view.get('activities'), list):
            return view
        with self.locked():
            state = self.load()
            if isinstance(state.get('home'), dict):
                # A detached plan may have published while the first display
                # read was running. Never replace it with that older fallback.
                return self.home_view(state)
            state['home'] = copy.deepcopy(view)
            if not self.pending(state) and view.get('basis', 0) >= state.get('committedBasis', 0):
                state['homeLearner'] = copy.deepcopy(view.get('learner'))
                if 'course' in view:
                    state['homeCourse'] = copy.deepcopy(view['course'])
            # A display cache refresh is not a learner-state revision and must
            # not invalidate an otherwise current background preparation.
            self.save(self.state_path, state)
            return self.home_view(state)

    def record_home_updates(self, state, view, request):
        if isinstance(view.get('activities'), list):
            state['home'] = copy.deepcopy(view)
            recommended = {row.get('taskId') for row in view['activities'] if row.get('taskId') is not None}
            state['homeTasks'] = {key: task for key, task in state.get('homeTasks', {}).items() if task.get('taskId') not in recommended}
        if view.get('learner') is not None:
            state['homeLearner'] = copy.deepcopy(view['learner'])
        if 'course' in view:
            old_course = state.get('homeCourse', (state.get('home') or {}).get('course'))
            if old_course != view['course'] and state.get('home'):
                if not isinstance(view.get('activities'), list):
                    state['home']['activities'] = []
                    state['home']['waitingActivities'] = []
                state['homeTasks'] = {}
            state['homeCourse'] = copy.deepcopy(view['course'])
        if view.get('type') not in {'lesson', 'review', 'assessment', 'diagnostic'} or type(view.get('taskId')) is not int:
            return
        summary = {key: copy.deepcopy(view[key]) for key in
                   ('taskId', 'activityId', 'type', 'title', 'status', 'progress', 'xpBase',
                    'awaitingQuestions', 'deferredSteps', 'canResumePractice') if key in view}
        summary['requestId'] = request
        state.setdefault('homeTasks', {})[str(view['taskId'])] = summary

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
        if action in {'home', 'queue'}:
            with self.locked():
                return self.home_view(self.load())
        if action == 'task':
            value = self.task_view(body['taskId'])
            if value is not None:
                return value
        if action not in {'home', 'queue', 'task', 'profile', 'learner', 'assignment', 'assignments',
                          'activity-history', 'activity-history-detail', 'study-stats', 'topic-study-availability'}:
            return None
        with self.locked():
            state = self.load()
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
            self.commit_state(state)
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

    def invalidate_plans(self):
        """Local selection preferences participate in detached plan admission."""
        with self.locked():
            self.commit_state(self.load())

    def receipt_path(self, request):
        return self.directory / 'receipts' / f'{request}.json'

    def prior_response(self, state, body):
        request = body['requestId']
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
        return None

    def capture_request(self, state):
        return self.grader.request({'action': 'study-capture', 'overlay': state['overlay'],
                                   'committedBasis': state.get('committedBasis', 0)})

    def projection_request(self, state, body, now):
        local = (state['overlay'] or {}).get('entities', {})
        aliases = {key: value for key, value in state['aliases'].items() if key not in local}
        return {'action': 'study-project', 'operation': self.normalize_ids(body, aliases),
                'overlay': state['overlay'], 'receivedAt': now,
                'aliases': state['aliases'], 'committedBasis': state.get('committedBasis', 0)}

    def accept_projection(self, state, body, now, projected):
        if not projected.get('ok'):
            return {'_error': projected.get('error', 'Unable to update study'),
                    '_code': projected.get('code', 'validation')}
        data = projected['data']
        state['overlay'] = data['overlay']
        state['views'].update(data.get('views', {}))
        view = data['view']
        for task_view in data.get('views', {}).values():
            self.record_home_updates(state, task_view, body['requestId'])
        self.record_home_updates(state, view, body['requestId'])
        if type(view.get('taskId')) is int:
            state['views'][str(view['taskId'])] = copy.deepcopy(view)
        if body['action'] == 'profile-settings':
            state['profile'] = copy.deepcopy(view)
        if body['action'] in {'profile-settings', 'target', 'queue-topic', 'daily-xp-goal'}:
            state['learner'] = {'basis': view.get('basis'), 'learner': copy.deepcopy(view.get('learner'))}
        op = {'requestId': body['requestId'], 'input': copy.deepcopy(body), 'operation': data['operation'],
              'saved': False, 'receivedAt': now}
        state['operations'].append(op)
        response = self.with_status(state, view)
        op['response'] = copy.deepcopy(response)
        # Both the exact acknowledgement and its recoverable native plan
        # reach local durable storage before the HTTP request can complete.
        self.commit_state(state)
        self.wake.set()
        return response

    def request(self, body, now=None):
        if body.get('action') not in self.ACTIONS:
            return None
        request = body.get('requestId', '')
        if not isinstance(request, str) or not 8 <= len(request) <= 128 or not all(c.isascii() and (c.isalnum() or c == '-') for c in request):
            raise ValueError('A stable request ID is required')
        now = int(time.time() * 1000) if now is None else now
        if body['action'] == 'queue':
            return self.prepare_queue(body, now)
        with self.locked():
            state = self.load()
            prior = self.prior_response(state, body)
            if prior is not None:
                return prior
            projected = self.grader.request(self.projection_request(state, body, now))
            return self.accept_projection(state, body, now, projected)

    def prepare_queue(self, body, now):
        # Queue construction can inspect a large question bank. It runs on a
        # separate native peer without holding the admission/state lock. A
        # revision guard discards speculative results if any accepted operation
        # or durable receipt changed the captured learner state meanwhile.
        if not self.planning_lock.acquire(blocking=False):
            return {'_superseded': True}
        try:
            with (self.directory / 'planner.lock').open('a') as planner_lock:
                try:
                    fcntl.flock(planner_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    return {'_superseded': True}
                with self.locked():
                    state = self.load()
                    prior = self.prior_response(state, body)
                    if prior is not None:
                        return prior
                    revision = state.get('revision', 0)
                    capture = self.capture_request(state)
                    if not capture.get('ok'):
                        return {'_error': capture.get('error', 'Study snapshot unavailable'), '_code': capture.get('code', 'unavailable')}
                    if capture['data'].get('ready') is False:
                        return {'_superseded': True}
                    reference = capture['data']['reference']
                    request = self.projection_request(state, body, now)
                    request['baseReference'] = reference
                projected = self.planner.request(request)
                # Global mode/admission order precedes the state lock. The
                # callback is held only for the short acknowledgement, never
                # while expensive native queue construction is running.
                with self.publication() as allowed:
                    if not allowed:
                        return {'_disabled': True}
                    with self.locked():
                        state = self.load()
                        prior = self.prior_response(state, body)
                        if prior is not None:
                            return prior
                        if state.get('revision', 0) != revision:
                            return {'_superseded': True}
                        current_capture = self.capture_request(state)
                        if not current_capture.get('ok') or current_capture['data'].get('ready') is False or current_capture['data'].get('reference') != reference:
                            return {'_superseded': True}
                        return self.accept_projection(state, body, now, projected)
        finally:
            self.planning_lock.release()

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
                            state['homeTasks'] = {str(self.normalize_ids(value, state['aliases'])['taskId']): self.normalize_ids(value, state['aliases']) for value in state.get('homeTasks', {}).values()}
                            if state.get('home'):
                                state['home'] = self.normalize_ids(state['home'], state['aliases'])
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
                    self.commit_state(state)
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
