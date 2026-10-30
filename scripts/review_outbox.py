"""Acknowledge review interactions on local durable storage; save to EDB in order.

The grading peer only reads. The persistence peer uses the ordinary guarded,
exact-request learning API. A crash before marking an operation saved replays
that same request, never an invented second answer/credit.
"""
from __future__ import annotations
import copy
import json
import threading
import time
import uuid
from pathlib import Path


class ReviewOutbox:
    ACTIONS = {'answer', 'continue', 'pause', 'resume', 'skip'}

    def __init__(self, directory, grader, writer, save, stop, refresh=lambda: None, *, learner=None):
        self.directory = Path(directory)
        self.grader, self.writer, self.save = grader, writer, save
        self.stop, self.refresh = stop, refresh
        self.lock = threading.RLock()
        self.wake = threading.Event()
        self.active = None
        self.learner = learner

    def owns(self, state):
        return self.learner is None or state['view'].get('learner', {}).get('id') == self.learner

    def path(self, task):
        if type(task) is not int or task <= 0:
            raise ValueError('A task entity ID is required')
        return self.directory / f'{task}.json'

    def load(self, path):
        return json.loads(path.read_text()) if path.exists() else None

    def pending(self, state):
        return [op for op in state['operations'] if not op.get('saved')]

    def measured(self, periods, now):
        return sum((p['end'] if p.get('end') is not None else now) - p['start'] for p in periods) / 1000

    def view(self, state, now=None):
        view = copy.deepcopy(state['view'])
        now = int(time.time() * 1000) if now is None else now
        elapsed = self.measured(state['periods'], now)
        view['step']['elapsedSeconds'] = elapsed
        view['elapsedSeconds'] = state['closedSeconds'] + elapsed
        pending = self.pending(state)
        view['saveState'] = {'status': 'error' if state.get('error') else 'pending' if pending else 'saved',
                             'pending': len(pending), 'error': state.get('error'),
                             'retrying': any(op.get('lastError') for op in pending)}
        return view

    def task_view(self, task):
        with self.lock:
            state = self.load(self.path(task))
            if state and state['view']['status'] in {'completed', 'failed'} and not self.pending(state) and not state.get('error'):
                return None  # Finished history comes from the authoritative database.
            return self.view(state) if state else None

    def status(self, task):
        with self.lock:
            state = self.load(self.path(task))
            return self.view(state)['saveState'] if state else {'status': 'saved', 'pending': 0, 'error': None}

    def retry(self, task):
        with self.lock:
            path = self.path(task)
            state = self.load(path)
            if state:
                state.pop('error', None)
                state['retryAt'] = 0
                self.save(path, state)
        self.wake.set()
        return self.status(task)

    def request(self, body, now=None):
        action, task = body.get('action'), body.get('taskId')
        if action not in self.ACTIONS or type(task) is not int:
            return None
        now = int(time.time() * 1000) if now is None else now
        with self.lock:
            path = self.path(task)
            state = self.load(path)
            if state is None:
                initial = self.grader.request({'action': 'review-session', 'taskId': task})
                if not initial.get('ok'):
                    # Other activity types and unsupported historical timing keep
                    # their existing authoritative path, including assessments.
                    return None
                data = initial['data']
                view = data.get('view', {})
                if view.get('type') != 'review':
                    return None
                if view['status'] not in {'started', 'paused'} or view.get('awaitingQuestions'):
                    return None
                cursor = next(i for i, step in enumerate(data['steps']) if step['contentId'] == view['step']['contentId'])
                periods = data['periods']
                state = {'view': view, 'steps': data['steps'], 'cursor': cursor,
                         'periods': periods, 'closedSeconds': view['elapsedSeconds'] - view['step']['elapsedSeconds'],
                         'operations': [], 'createdAt': now, 'retryAt': 0}
            # Input equality and the original acknowledgement survive page reload,
            # duplicate delivery, an uncertain reply, and a service restart.
            request = body.get('requestId', '')
            if not isinstance(request, str) or not 8 <= len(request) <= 128 or not all(c.isascii() and (c.isalnum() or c == '-') for c in request):
                raise ValueError('A stable request ID is required')
            prior = next((op for op in state['operations'] if op['requestId'] == request), None)
            if prior:
                if prior['input'] != body:
                    raise ValueError('Request ID already used for another review interaction')
                return copy.deepcopy(prior['response'])
            if state.get('error'):
                raise ValueError('Review saving needs attention: ' + state['error'])
            view, step = state['view'], state['view']['step']
            if view['status'] in {'completed', 'failed'}:
                raise ValueError('This review is already complete; reopen its saved result')
            if action in {'answer', 'continue', 'skip'} and body.get('itemId') != step['itemId']:
                raise ValueError('This presentation is no longer current')
            if action in {'answer', 'continue', 'skip'} and view['status'] != 'started':
                return {'_error': 'Resume the lesson before continuing', '_code': 'lesson-paused'}
            periods = copy.deepcopy(state['periods'])
            for p in periods:
                if p.get('end') is None:
                    if now < p['start']:
                        raise ValueError('Working clock moved backwards')
                    p['end'] = now
            q = step['contentId']
            clock_periods = periods
            op = {k: copy.deepcopy(v) for k, v in body.items() if k not in {'itemId', 'submittedAt', 'submissionId'}}
            if action == 'answer':
                if step['status'] in {'correct', 'incorrect', 'skipped', 'completed'}:
                    raise ValueError('This question has already been submitted')
                feedback = self.grader.request({'action': 'review-grade', 'taskId': task,
                                                'questionId': q, 'responses': body.get('responses')})
                if not feedback.get('ok'):
                    return {'_error': feedback.get('error', 'Unable to grade answer'), '_code': feedback.get('code', 'validation')}
                graded = feedback['data']['step']
                graded['itemId'] = step['itemId']
                view['step'] = graded
                view['progress']['answered'] = view['progress'].get('answered', 0) + 1
            elif action == 'skip':
                if step['status'] != 'started':
                    raise ValueError('This question has already ended')
                feedback = self.grader.request({'action': 'review-skip', 'taskId': task, 'questionId': q})
                if not feedback.get('ok'):
                    raise ValueError(feedback.get('error', 'Unable to skip question'))
                skipped = feedback['data']['step']
                skipped['itemId'] = step['itemId']
                view['step'] = skipped
            elif action == 'continue':
                if not step.get('canContinue'):
                    raise ValueError('Answer the current question before continuing')
                history = list(view.get('history', []))
                history.append({'order': state['cursor'] + 1, 'number': state['cursor'] + 1,
                                'total': len(state['steps']), 'step': copy.deepcopy(step)})
                outcomes = [entry['step']['status'] for entry in history]
                result = self.grader.request({'action': 'review-decision', 'taskId': task, 'outcomes': outcomes})
                if not result.get('ok'):
                    raise ValueError(result.get('error', 'Unable to continue review'))
                decision = result['data']
                view['history'] = history
                if decision['complete']:
                    view.update(status='completed' if decision['passed'] else 'failed', xp=decision['xp'])
                else:
                    state['closedSeconds'] += self.measured(periods, now)
                    state['cursor'] += 1
                    following = copy.deepcopy(state['steps'][state['cursor']])
                    following['itemId'] = f"review-{task}-{state['cursor']}"
                    following['status'] = 'started'
                    view['step'] = following
                    view['progress'].update(stepNumber=state['cursor'] + 1, presented=state['cursor'] + 1)
                    clock_periods = [{'id': str(uuid.uuid4()), 'start': now, 'end': None}]
            elif action == 'pause':
                view['status'] = 'paused'
                if step['status'] == 'started':
                    step['status'] = 'paused'
            elif action == 'resume':
                view['status'] = 'started'
                if step['status'] == 'paused':
                    step['status'] = 'started'
                    clock_periods = periods + [{'id': str(uuid.uuid4()), 'start': now, 'end': None}]
                elif step['status'] == 'started':
                    # Resume is idempotent and must not split a running clock.
                    clock_periods = state['periods']
            op['_queuedReview'] = {'questionId': q, 'periods': clock_periods}
            if action in {'answer', 'skip'}:
                op['_queuedReview']['expectedStatus'] = view['step']['status']
            if action == 'continue':
                op['_queuedReview']['nextQuestionId'] = view['step']['contentId'] if view['status'] == 'started' else None
                op['_queuedReview']['expectedTaskStatus'] = view['status']
            state['periods'] = clock_periods
            state['operations'].append({'requestId': request, 'input': copy.deepcopy(body), 'operation': op,
                                        'saved': False, 'receivedAt': now})
            response = self.view(state, now)
            state['operations'][-1]['response'] = response
            # The acknowledgement is not sent until this atomic file and its
            # directory are fsynced. The database can now safely lag the UI.
            self.save(path, state)
            self.wake.set()
            return response

    def run_one(self):
        with self.lock:
            candidates = []
            for path in self.directory.glob('*.json'):
                state = self.load(path)
                if not self.owns(state):
                    continue
                pending = self.pending(state)
                if pending and not state.get('error') and state.get('retryAt', 0) <= time.time():
                    candidates.append((pending[0]['receivedAt'], path, pending[0]))
            if not candidates:
                return False
            _, path, op = min(candidates, key=lambda row: (row[0], row[1].name))
            operation = copy.deepcopy(op['operation'])
        # No admission lock is held while EDB writes. More answers and Next
        # requests may be acknowledged and appended during this wait.
        try:
            result = self.writer.request({'action': 'persist-review', 'operation': operation})
        except (OSError, ValueError) as error:
            result = {'ok': False, 'code': 'unavailable', 'error': str(error)}
        with self.lock:
            state = self.load(path)
            current = next(row for row in state['operations'] if row['requestId'] == op['requestId'])
            if result.get('ok'):
                current['saved'] = True
                current['savedAt'] = int(time.time() * 1000)
                state['retryAt'] = 0
                current.pop('lastError', None)
            elif result.get('code') == 'basis-conflict':
                # An explicit stale-basis rejection proves no commit occurred.
                # Keep the admission identity/time and give only this rejected
                # database attempt a new durable request key.
                current['operation']['requestId'] = str(uuid.uuid4())
                state['retryAt'] = time.time() + 0.1
            elif result.get('code') == 'unavailable':
                current['lastError'] = result.get('error', 'Saving temporarily unavailable')
                state['retryAt'] = time.time() + 2
            else:
                state['error'] = result.get('error', 'Review save failed')
            self.save(path, state)
        if result.get('ok'):
            self.refresh()
        return True

    def loop(self):
        while not self.stop.is_set():
            try:
                if self.run_one():
                    continue
            except Exception as error:
                # A corrupt job or filesystem failure must remain observable
                # and must not silently kill the persistence lane.
                print(f'Review persistence deferred: {error}', flush=True)
            self.wake.wait(0.5)
            self.wake.clear()

    def drain(self, timeout=55, *, pause_active=False):
        if pause_active:
            # The ordinary start/assignment/profile path pauses other activity.
            # Admit that pause through the outbox first so its logical clock and
            # the database cannot diverge when another tab changes activities.
            with self.lock:
                active = [state for p in self.directory.glob('*.json') if self.owns(state := self.load(p))]
                for state in active:
                    if state['view']['status'] == 'started':
                        self.request({'action':'pause','taskId':state['view']['taskId'],'requestId':str(uuid.uuid4())})
        deadline = time.monotonic() + timeout
        self.wake.set()
        while time.monotonic() < deadline:
            with self.lock:
                states = [state for p in self.directory.glob('*.json') if self.owns(state := self.load(p))]
                if any(s.get('error') for s in states):
                    raise ValueError('A review save needs attention before starting another activity')
                if not any(self.pending(s) for s in states):
                    return
            if self.stop.wait(0.05):
                raise ValueError('Review saving is restarting; retry shortly')
        raise ValueError('Review answers are safely queued; saving has not finished yet')
