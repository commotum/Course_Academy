"""Account answer profiles and durable, confirmed practice exposure counts."""
from __future__ import annotations

import json
import time

from .storage import atomic_json, read_json

BASE_ACCURACY = {'shaky': .50, 'solid': .75, 'strong': .90}
ERROR_HALF_LIFE = {'slow': 36, 'steady': 12, 'fast': 4}
PROFILES = {'capture': None, **{
    f'{speed}-{base}': {'base_accuracy': accuracy, 'error_half_life': ERROR_HALF_LIFE[speed]}
    for speed in ERROR_HALF_LIFE for base, accuracy in BASE_ACCURACY.items()}}


def validate_profile(name):
    if name not in PROFILES:
        raise ValueError('Unknown answer profile: ' + str(name))
    return name


def account_profile(config):
    """Explicit run configuration wins; otherwise use the saved account setting."""
    configured = getattr(config, 'answer_profile', None)
    saved = read_json(config.state_root / 'answer-profile.json', {}) if configured is None else {}
    return validate_profile(configured or saved.get('answer_profile', 'capture'))


def set_account_profile(config, name):
    name = validate_profile(name)
    atomic_json(config.state_root / 'answer-profile.json',
                {'answer_profile': name, 'updated_at': time.time()})


def accuracy(name, exposures):
    settings = PROFILES[validate_profile(name)]
    if settings is None:
        raise ValueError('Capture uses its activity-specific answer policy')
    return 1 - (1 - settings['base_accuracy']) * 2 ** (-exposures / settings['error_half_life'])


def kp_key(question):
    # MA's source KP IDs are global. e-N is another spelling of the same ID.
    identity = (question.get('kp_id') or question.get('knowledge_point_id')
                or question.get('knowledge_point_source_id'))
    return str(identity).removeprefix('e-') if identity is not None else None


class ExposureStore:
    """One exposure per graded question presentation, including wrong answers.

    Events deduplicate retries and restarts. Assessment entry does not count until
    completion and history grading. Diagnostics and unsubmitted responses never
    count. Unidentified KPs stay at the base rate until a source association exists.
    """

    def __init__(self, config):
        self.config = config
        self.path = config.state_root / 'learning-exposures.json'
        self.data = read_json(self.path, None)
        if self.data is None:
            self.data = {'version': 1, 'account': config.account, 'counts': {},
                         'events': {}, 'question_kps': {}, 'initialized_at': time.time()}
            # Existing practice belongs to this learner, even if it used capture.
            for path in sorted(config.output_root.glob('*/checkpoint.json')):
                self._merge(read_json(path, {}))
            self._save()
        if self.data.get('account') != config.account or self.data.get('version') != 1:
            raise ValueError('Exposure ledger belongs to another account or version')

    def _save(self):
        atomic_json(self.path, self.data)

    def key(self, question):
        return kp_key(question) or self.data['question_kps'].get(str(question.get('math_academy_id')))

    def count(self, question):
        key = self.key(question)
        return self.data['counts'].get(key, 0) if key is not None else 0

    def _merge(self, state):
        activity = state.get('activity', {})
        kind = activity.get('kind')
        if kind not in ('lesson', 'review', 'multistep', 'assessment'):
            return False
        if kind == 'assessment' and state.get('stage') not in ('history', 'complete'):
            return False
        changed = False
        for presentation, record in state.get('presentations', {}).items():
            feedback = record.get('feedback') or {}
            question = {**record.get('question', {}), **feedback}
            key = kp_key(question)
            grade = str(feedback.get('grade') or record.get('grade') or '').strip().lower()
            if key is None or grade not in ('correct', 'incorrect', 'partial credit', 'full credit'):
                continue
            submitted = record.get('accepted') or any(
                s.get('action', 'answer') == 'answer'
                and s.get('outcome') not in ('entry_failed', 'not_submitted')
                for s in record.get('submissions', []))
            if not submitted:
                continue
            event_id = json.dumps([str(activity.get('task_id')), str(presentation)])
            old = self.data['events'].get(event_id)
            event = {'kp_id': key, 'kind': kind,
                'task_id': str(activity.get('task_id')), 'presentation_key': str(presentation),
                'question_id': question.get('math_academy_id'), 'grade': grade}
            if old == event:
                continue
            if not old or old['kp_id'] != key:
                if old:
                    self.data['counts'][old['kp_id']] -= 1
                self.data['counts'][key] = self.data['counts'].get(key, 0) + 1
            self.data['events'][event_id] = event
            if question.get('math_academy_id'):
                self.data['question_kps'][str(question['math_academy_id'])] = key
            changed = True
        return changed

    def reconcile(self, state):
        if self._merge(state):
            self._save()
