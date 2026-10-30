"""Recover pre-upgrade review journals alongside the general study outbox.

New interactions use StudyOutbox. Existing review acknowledgements retain their
original replay mechanism and exact receipts until they have reached EDB.
"""
from study_outbox import StudyOutbox
from review_outbox import ReviewOutbox
import threading


class CompatibleStudyOutbox:
    def __init__(self, directory, grader, writer, save, stop, refresh=lambda: None, *, learner=None, planner=None, publication=None):
        study_directory = directory.parent / 'study-outbox'
        if learner is not None:
            if not learner or not all(c.isascii() and (c.isalnum() or c == '-') for c in learner):
                raise ValueError('Invalid learner journal namespace')
            study_directory /= learner
        self.study = StudyOutbox(study_directory, grader, writer, save, stop, refresh, planner=planner, publication=publication)
        self.legacy = ReviewOutbox(directory, grader, writer, save, stop, refresh, learner=learner)
        self.stop = stop
        self.index_lock = threading.RLock()
        self.legacy_pending = set()
        self.legacy_receipts = set()
        for path in self.legacy.directory.glob('*.json'):
            state = self.legacy.load(path)
            if not self.legacy.owns(state):
                continue
            task = state['view']['taskId']
            self.legacy_receipts.update((task, op['requestId']) for op in state['operations'])
            if self.legacy.pending(state) or state.get('error'):
                self.legacy_pending.add(task)

    def legacy_states(self):
        with self.index_lock, self.legacy.lock:
            states = []
            for task in list(self.legacy_pending):
                state = self.legacy.load(self.legacy.path(task))
                if self.legacy.pending(state) or state.get('error'):
                    states.append(state)
                else:
                    self.legacy_pending.discard(task)
            return states

    def request(self, body, now=None):
        with self.index_lock:
            duplicate = (body.get('taskId'), body.get('requestId')) in self.legacy_receipts
        if duplicate:
            return self.legacy.request(body, now)
        states = self.legacy_states()
        for state in states:
            same_task = state['view'].get('taskId') == body.get('taskId')
            if same_task and (self.legacy.pending(state) or state.get('error')):
                result = self.legacy.request(body, now)
                if result is not None and '_error' not in result:
                    with self.index_lock:
                        self.legacy_receipts.add((body.get('taskId'), body.get('requestId')))
                return result
        if body.get('action') in self.study.ACTIONS and any(self.legacy.pending(state) for state in states):
            # Only upgrade recovery may need this barrier. Never interleave two
            # different persistence protocols for the same learner's progress.
            self.legacy.drain(pause_active=True)
        return self.study.request(body, now)

    def task_view(self, task):
        for state in self.legacy_states():
            if state['view'].get('taskId') == task and (self.legacy.pending(state) or state.get('error')):
                return self.legacy.task_view(task)
        return self.study.task_view(task)

    def overlay_view(self, action, body):
        if action == 'task':
            for state in self.legacy_states():
                if state['view'].get('taskId') == body['taskId'] and (self.legacy.pending(state) or state.get('error')):
                    return self.legacy.task_view(body['taskId'])
        return self.study.overlay_view(action, body)

    def resolve_ids(self, body):
        return self.study.resolve_ids(body)

    def invalidate_plans(self):
        self.study.invalidate_plans()

    def decorate(self, view):
        return self.study.decorate(view)

    def status(self, task=None):
        status = self.study.status(task)
        for state in self.legacy_states():
            pending = self.legacy.pending(state)
            if pending or state.get('error'):
                legacy = self.legacy.view(state)['saveState']
                status['pending'] += legacy['pending']
                status['error'] = status.get('error') or legacy.get('error')
                status['retrying'] = status.get('retrying', False) or legacy.get('retrying', False)
        status['status'] = 'error' if status.get('error') else 'pending' if status['pending'] else 'saved'
        return status

    def retry(self, task=None):
        self.study.retry(task)
        for state in self.legacy_states():
            if self.legacy.pending(state) or state.get('error'):
                self.legacy.retry(state['view']['taskId'])
        return self.status(task)

    def drain(self, timeout=55, *, pause_active=False):
        self.legacy.drain(timeout, pause_active=pause_active)
        self.study.drain(timeout, pause_active=pause_active)

    def loop(self):
        # One writer lane for both protocols. No admission mutex is held here.
        while not self.stop.is_set():
            try:
                states = self.legacy_states()
                if any(self.legacy.pending(s) or s.get('error') for s in states):
                    if self.legacy.run_one():
                        continue
                elif self.study.run_one():
                    continue
            except Exception as error:
                print(f'Study persistence deferred: {error}', flush=True)
            self.study.wake.wait(.1)
            self.study.wake.clear()
