"""An activity stays pinned until its source review and agent judgments are complete."""

from copy import deepcopy
import hashlib
import json
import logging
from pathlib import Path
import random
import re
import time

from ..runtime import StopRequested, backoff, check_stop, wait
from ..storage import append_event, atomic_json, read_json
from ..timing import Pacer
from ..profiles import ExposureStore, account_profile
from ..database.evidence import authoritative_question, UnsupportedContent
from .evidence import capture_gaps, finalize_answers, merge_question, question_key
from .policy import AnswerPolicy, answer_fields, override, responses_for, supports_intentional_error, topic_id
from .solver import SolverClient, SolverUnavailable, validate_result
from .task_payload import task_payload, semantic_identity, feedback_evidence


class ResponseNotSubmitted(Exception):
    """A guarded browser return is a failed entry, not a successful action."""
    submitted = False


class ActivityCapture:
    def __init__(self, config, browser, stop_event, context_provider=None, *, solver=None,
                 clock=time.time, sleeper=None, rng=None):
        self.config, self.browser, self.stop_event = config, browser, stop_event
        self.context_provider = context_provider
        self.solver = solver
        self.exposures = None
        self.clock = clock
        self.sleep = sleeper or (lambda seconds: wait(stop_event, seconds))
        self.rng = rng or random.Random(config.seed)
        self.pacer = Pacer(config, stop_event, clock=clock, rng=self.rng, sleeper=self.sleep)

    def run(self, activity, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.checkpoint_path = self.directory / 'checkpoint.json'
        complete = read_json(self.directory / 'capture-complete.json')
        if complete and str(complete['task_id']) == str(activity['task_id']):
            return read_json(self.directory / 'content.json')
        self.activity = deepcopy(activity)
        self.state = read_json(self.checkpoint_path, {'version': 1, 'activity': self.activity,
            'stage': 'activity', 'policy': {}, 'presentations': {}, 'steps': [], 'judgments': {},
            'started_at': self.clock(), 'context': None, 'recoveries': 0})
        if str(self.state['activity']['task_id']) != str(activity['task_id']):
            raise ValueError('Capture directory belongs to another task')
        if self.state.get('rng_state') and hasattr(self.rng, 'setstate'):
            def tuples(value):
                return tuple(tuples(v) for v in value) if isinstance(value, list) else value
            self.rng.setstate(tuples(self.state['rng_state']))
        self._set_browser_deadline()
        if self.solver is None:
            self.solver = SolverClient(self.config, self.directory, self.stop_event)
        if self.state.get('context') is None or self.state['context'].get('unavailable') or self.state['context'].get('snapshot_unavailable'):
            try:
                self.state['context'] = self.context_provider(activity) if self.context_provider else {}
            except StopRequested:
                raise
            except Exception as error:
                # The database provider may use its own last good snapshot. An absent
                # graph is an explicit unknown-topic diagnostic action, not a halt.
                self.state['context'] = {'unavailable': str(error), 'snapshot_unavailable': True}
            self._save()
        name = account_profile(self.config)
        self.exposures = ExposureStore(self.config) if (name != 'capture' or
            (self.config.state_root / 'learning-exposures.json').exists()) else None
        if self.exposures:
            self.exposures.reconcile(self.state)
        self.policy = AnswerPolicy(activity, self.state['policy'], self.state['context'], self.rng, self.clock,
                                   answer_profile=name, exposures=self.exposures)
        if self.state['stage'] == 'activity':
            self._browser_call('open', activity, self.directory, self.state)
            self._execute()
        content = self._review()
        content['judgments'] = list(self.state['judgments'].values())
        content['capture_version'] = 3
        content['pipeline'] = 'capture-modules-v3'
        content['captured_at'] = self.clock()
        content['attempts'] = list(self.state['presentations'].values())
        content['policy'] = deepcopy(self.state['policy'])
        content['topic_context'] = self.state['context']
        content['completion'] = self.state.get('completion', {})
        if isinstance(content['completion'].get('completion'), dict):
            content['completion'] = content['completion']['completion']
        content['base_xp'] = content.get('base_xp') or content['completion'].get('base_xp')
        atomic_json(self.directory / 'content.json', content)
        self.state['stage'] = 'complete'
        self._save()
        atomic_json(self.directory / 'capture-complete.json', {
            'task_id': str(activity['task_id']), 'completed_at': self.clock(), 'version': 3,
            'question_judgments': len(content['judgments'])})
        return content

    def _save(self):
        if hasattr(self.rng, 'getstate'):
            self.state['rng_state'] = self.rng.getstate()
        atomic_json(self.checkpoint_path, self.state)

    def _event(self, event, **values):
        append_event(self.directory / 'activity-events.jsonl', event, **values)

    def _set_browser_deadline(self):
        deadline = (self.state.get('assessment_timing') or {}).get('deadline_at')
        if self.state.get('stage') != 'activity':
            deadline = None
        setter = getattr(self.browser, 'set_deadline', None)
        if setter:
            setter(deadline)

    @staticmethod
    def _time_limit(value):
        units = re.findall(r'(\d+(?:\.\d+)?)\s*(hours?|minutes?|seconds?)', str(value or ''), re.I)
        return sum(float(amount) * (3600 if unit.lower().startswith('hour') else
                   60 if unit.lower().startswith('minute') else 1) for amount, unit in units) or None

    def _start_assessment_timing(self, observation):
        timing = self.state.setdefault('assessment_timing', {})
        if timing.get('started_at') is not None or timing.get('deadline_at') is not None:
            return
        details = self.activity.get('details', {})
        seconds = self._time_limit(details.get('time_limit') or observation.get('time_limit'))
        timing.update(started_at=self.clock(),
                      question_count=timing.get('question_count') or details.get('question_count'),
                      time_limit_seconds=seconds, started_by_capture=True)
        if seconds:
            timing['deadline_at'] = timing['started_at'] + seconds
        self.state['assessment_timing'] = timing
        self._assessment_schedule()
        self._save()  # Saved before Start: a lost acknowledgment cannot restart the clock.
        self._set_browser_deadline()

    def _assessment_schedule(self):
        timing = self.state.get('assessment_timing') or {}
        count, limit = timing.get('question_count'), timing.get('time_limit_seconds')
        if (not timing.get('started_by_capture') or not count or not limit
                or 'answer_offsets_seconds' in timing):
            return
        low, high = getattr(self.config, 'assessment_time_min', .7), getattr(self.config, 'assessment_time_max', .85)
        target = float(limit) * self.rng.uniform(low, high)
        weights = [self.rng.uniform(.65, 1.35) for _ in range(int(count))]
        cumulative, offsets = 0, []
        for weight in weights:
            cumulative += weight
            offsets.append(target * cumulative / sum(weights))
        timing.update(target_seconds=target, answer_offsets_seconds=offsets)

    def _observe_timing(self, observation):
        if self.activity['kind'] != 'assessment' or observation.get('kind') == 'complete':
            return
        timing = self.state.setdefault('assessment_timing', {})
        # An instruction screen before Start has no live assessment clock yet.
        if observation.get('action') == 'start' and not timing:
            self.state.pop('assessment_timing', None)
            return
        observed_at = float(observation.get('observed_at', self.clock()))
        deadlines = [timing.get('deadline_at'), observation.get('deadline_at')]
        if observation.get('remaining_seconds') is not None:
            deadlines.append(observed_at + max(0, float(observation['remaining_seconds'])))
        deadlines = [float(value) for value in deadlines if value is not None]
        if deadlines:
            timing['deadline_at'] = min(deadlines)
        count = observation.get('question_count') or self.activity.get('details', {}).get('question_count')
        if count:
            timing['question_count'] = int(count)
        self._assessment_schedule()
        self._set_browser_deadline()
        self._save()

    def _remaining_seconds(self, observation=None):
        if self.activity.get('kind') != 'assessment' or self.state.get('stage') != 'activity':
            return None
        deadlines = [(self.state.get('assessment_timing') or {}).get('deadline_at')]
        if observation and observation.get('remaining_seconds') is not None:
            deadlines.append(float(observation.get('observed_at', self.clock())) + float(observation['remaining_seconds']))
        values = [float(value) - self.clock() for value in deadlines if value is not None]
        return max(0, min(values)) if values else None

    def _submission_reserve(self):
        limit = (self.state.get('assessment_timing') or {}).get('time_limit_seconds') or 300
        return max(15, min(60, float(limit) * .05))

    def _submit_if_due(self, observation):
        remaining = self._remaining_seconds(observation)
        if remaining is None or remaining > self._submission_reserve():
            return False
        self._event('assessment_deadline_submission', remaining_seconds=remaining)
        self.state['assessment_timing_deviation'] = 'Submit entered answers before the timer expires; judge any unanswered items in history'
        self._save()
        self._browser_call('respond', observation, {'action': 'submit_assessment'}, self.directory)
        return True

    def _prepare_answer_pacing(self, record, observation):
        decision = record['decision']
        kind = self.activity['kind']
        if kind in ('lesson', 'review', 'multistep'):
            # Each newly revealed proof stage has its own budget; a resumed or
            # rejected submission does not draw another delay.
            stage = str(observation.get('key') or record['key'])
            pacing = record.setdefault('answer_pacing', {})
            if stage not in pacing:
                started = (record['started_at'] if not pacing else observation.get('observed_at', self.clock()))
                delay = self.pacer.duration('answer')
                pacing[stage] = {'started_at': started, 'delay_seconds': delay, 'submit_at': started + delay}
            decision.update(pacing[stage])
        elif kind == 'assessment':
            timing = self.state.get('assessment_timing') or {}
            position = observation.get('sequence_position') or observation.get('question', {}).get('sequence_position')
            offsets = timing.get('answer_offsets_seconds', [])
            if position and 0 < int(position) <= len(offsets):
                decision['submit_at'] = timing['started_at'] + offsets[int(position) - 1]
                decision['delay_seconds'] = max(0, decision['submit_at'] - record['started_at'])

    def _pace_answer(self, record, observation):
        due = record['decision']['submit_at']
        budget = max(0, due - self.clock())
        while True:
            check_stop(self.stop_event)
            delay = min(budget, max(0, due - self.clock()))
            available = self._remaining_seconds(observation)
            if available is not None:
                timing = self.state.get('assessment_timing') or {}
                count = timing.get('question_count') or 1
                position = observation.get('sequence_position') or 1
                allowance = max(0, available - self._submission_reserve() - 15 * max(0, int(count) - int(position)))
                if delay > allowance:
                    record['decision']['timing_deviation'] = 'Preserve time for remaining questions and final submission'
                delay = min(delay, allowance)
            if delay <= 0:
                return
            chunk = min(30, delay)
            self.sleep(chunk)
            budget -= chunk
            timer = (getattr(self.browser, 'read_remaining_seconds', None)
                     or getattr(self.browser, 'remaining_seconds', None))
            if available is not None and timer:
                try:
                    seconds = timer()
                    if seconds is not None:
                        self._observe_timing({'remaining_seconds': seconds, 'observed_at': self.clock()})
                except StopRequested:
                    raise
                except Exception as error:
                    self._event('assessment_timer_read_failed', error=str(error))

    def _diagnostic_retry(self, observation):
        record = next(reversed(self.state['presentations'].values()), {}) if self.state['presentations'] else {}
        if 'diagnostic_retry_taken' in record:
            return {**observation, 'retry_diagnostic': record['diagnostic_retry_taken']}
        decision = record.get('decision', {})
        take = bool(decision.get('intended') == 'C' and decision.get('distance', 0)
                    and not self.state.get('diagnostic_retry_active'))
        record['diagnostic_retry_taken'] = take
        self.state['diagnostic_retry_active'] = take
        self._save()
        return {**observation, 'retry_diagnostic': take}

    def _browser_call(self, method, *args):
        attempts = 0
        while True:
            check_stop(self.stop_event)
            try:
                result = getattr(self.browser, method)(*args)
                if method == 'respond' and isinstance(result, dict) and result.get('not_submitted'):
                    raise ResponseNotSubmitted(result.get('reason') or 'Response was not submitted; reread the current page')
                pending = self.state.get('pending_browser_error') or {}
                observed_progress = method == 'observe' and isinstance(result, dict) and (
                    (result.get('accepted') and pending.get('method') == 'respond')
                    or result.get('kind') == 'complete'
                    or (pending.get('observation_key') and result.get('key') is not None
                        and result['key'] != pending['observation_key']))
                recovered = pending and (method == pending['method'] or observed_progress or self.state.get('stage') == 'history')
                if recovered and not (isinstance(result, dict) and result.get('unknown_outcome')):
                    previous = self.state.pop('pending_browser_error')
                    self.state.get('browser_failures', {}).pop(previous.get('failure_key'), None)
                    self._event('browser_recovered', method=method, previous_error=previous)
                    self._save()
                return result
            except StopRequested:
                raise
            except Exception as error:
                key = (args[0].get('key') if args and isinstance(args[0], dict)
                       else (self.state.get('last_observation') or {}).get('key'))
                family = re.sub(r'\b\d+(?:\.\d+)?\b', 'N', str(error).split('Call log:')[0])
                failure_key = hashlib.sha256(json.dumps([method, key, type(error).__name__, family]).encode()).hexdigest()
                failures = self.state.setdefault('browser_failures', {})
                attempts = failures.get(failure_key, 0) + 1
                failures[failure_key] = attempts
                self.state['recoveries'] += 1
                self.state['pending_browser_error'] = {'method': method, 'error': str(error), 'attempt': attempts,
                    'observation_key': key, 'failure_key': failure_key,
                    'not_submitted': isinstance(error, ResponseNotSubmitted),
                    'entry_failed': getattr(error, 'submitted', None) is False,
                    'error_type': type(error).__name__}
                if getattr(error, 'layout', None) is not None:
                    self.state['pending_browser_error']['layout'] = error.layout
                if getattr(error, 'http_status', None) is not None:
                    self.state['pending_browser_error']['http_status'] = error.http_status
                self._save()
                self._event('browser_retry', method=method, error=str(error), attempt=attempts,
                            layout=getattr(error, 'layout', None))
                logging.warning('%s task %s: %s; retrying', method, self.activity['task_id'], error)
                delay = self.pacer.backoff(attempts, retry_after=getattr(error, 'retry_after', 0))
                available = self._remaining_seconds()
                if (available is not None and method == 'respond'
                        and getattr(error, 'submitted', None) is False
                        and not getattr(error, 'retry_after', 0)):
                    # A local editor failure made no network submission. Re-read
                    # promptly so focused entry recovery can fit in the exam.
                    delay = min(delay, 1.0)
                # Ordinary recovery must leave enough time to submit the whole
                # assessment. A server throttle is never shortened into a retry.
                if available is not None and available > 0 and method != 'open' and not getattr(error, 'retry_after', 0):
                    delay = min(delay, max(0, available - self._submission_reserve()))
                self.sleep(delay)
                # A timed-out Start/Continue/Submit may already have succeeded.
                # Return to observation before ANY further state-changing action.
                if method in ('respond', 'advance', 'recover'):
                    return {'unknown_outcome': True, 'error': str(error),
                            'http_status': getattr(error, 'http_status', None),
                            'entry_failed': getattr(error, 'submitted', None) is False,
                            'not_submitted': isinstance(error, ResponseNotSubmitted)}
                if method == 'observe' and available is not None and self._remaining_seconds() <= self._submission_reserve():
                    # Preserve the last known page for final submission even if
                    # optional capture work can no longer fit before expiry.
                    previous = self.state.get('last_observation')
                    if previous:
                        return {**previous, 'remaining_seconds': self._remaining_seconds(),
                                'observed_at': self.clock(), 'deadline_recovery': str(error)}
                if attempts % 3 == 0 and hasattr(self.browser, 'restart'):
                    try:
                        self.browser.restart()
                        if method not in ('open', 'history'):
                            self.browser.open(self.activity, self.directory, self.state)
                    except StopRequested:
                        raise
                    except Exception as restart_error:
                        self._event('browser_restart_retry', error=str(restart_error))

    def _execute(self):
        repeated = 0
        last_signature = None
        while True:
            check_stop(self.stop_event)
            observation = self._browser_call('observe', self.directory)
            self.state['last_observation'] = observation
            self._observe_timing(observation)
            if observation.get('shared_contexts'):
                self.state['shared_context'] = observation['shared_contexts']
            signature = self._signature(observation)
            blocker = self.state.get('pending_capture_blocker')
            if blocker and blocker['signature'] != signature:
                self.state.pop('pending_capture_blocker')
                self._event('capture_progress_resumed', observation_key=observation.get('key'))
                self._save()
            repeated = repeated + 1 if signature == last_signature else 0
            last_signature = signature
            kind = observation.get('kind', 'unknown')
            blocker = self.state.get('pending_capture_blocker')
            if blocker and kind != 'complete':
                if self._submit_if_due(observation):
                    continue
                delay = blocker['retry_at'] - self.clock()
                if delay > 0:
                    remaining = self._remaining_seconds(observation)
                    if remaining is not None:
                        delay = min(delay, max(0, remaining - self._submission_reserve()))
                    self.sleep(min(60, delay))
                    continue
            if kind == 'complete':
                self.state.update(stage='history', completion=observation, completed_at=self.clock())
                self._set_browser_deadline()
                self._save()
                return
            if kind == 'question':
                if self._submit_if_due(observation):
                    continue
                self._question(observation, repeated)
            elif kind in ('tutorial', 'example'):
                self._record_step(observation)
                self._save()
                self._browser_call('advance', observation, self.directory)
            elif kind == 'instructions':
                self._record_step(observation)
                self._save()
                if observation.get('action') == 'submit_assessment':
                    self.state['assessment_submission_started'] = self.clock()
                    self._save()
                    self._browser_call('respond', observation, {'action': 'submit_assessment'}, self.directory)
                else:
                    if self.activity['kind'] == 'assessment' and observation.get('action') == 'start':
                        self._start_assessment_timing(observation)
                    if self.activity['kind'] == 'diagnostic' and observation.get('action') in ('decline_retry', 'diagnostic_retry'):
                        observation = self._diagnostic_retry(observation)
                    self._browser_call('advance', observation, self.directory)
            else:
                self._recover_page(observation, repeated)
            if repeated >= 3 and kind not in ('question', 'unknown'):
                self._recover_page(observation, repeated)

    @staticmethod
    def _signature(observation):
        question = observation.get('question', {})
        shape = [(f.get('key'), f.get('disabled'), [(c.get('value'), c.get('option')) for c in f.get('choices', [])])
                 for f in answer_fields(question)]
        return json.dumps([observation.get('kind'), observation.get('key'), observation.get('accepted'),
                           observation.get('grade'), question.get('problem'),
                           [(a.get('tag'), a.get('source_url'), a.get('html')) for a in question.get('assets', [])],
                           shape], sort_keys=True, default=str)

    def _record_step(self, observation):
        key = str(observation.get('key') or self._signature(observation))
        existing = next((s for s in self.state['steps'] if s.get('capture_key') == key), None)
        step = deepcopy(observation)
        if step.get('kind') == 'example' and step.get('question'):
            self._normalize_kp(step['question'], example=True)
        step['capture_key'] = key
        if existing is None:
            step['observed_position'] = len(self.state['steps'])
            self.state['steps'].append(step)
        else:
            existing.update(step)

    def _question(self, observation, repeated):
        question = deepcopy(observation.get('question') or {})
        question.setdefault('topic_id', observation.get('topic_id') or self.activity.get('topic_id'))
        self._normalize_kp(question)
        if not question.get('kp_id'):
            # Lesson questions follow the current canonical example; its e-N is
            # the same source KP anchor revealed later by the history page.
            example = next((s.get('question') for s in reversed(self.state['steps']) if s.get('kind') == 'example'), None)
            if example and self.activity['kind'] == 'lesson':
                question['kp_id'] = example.get('kp_id')
        key = str(observation.get('key') or question_key(question)).split(':fields:', 1)[0]
        record = self.state['presentations'].setdefault(key, {'key': key, 'question': question,
            'started_at': observation.get('appeared_at') or observation.get('observed_at') or self.clock(),
            'submissions': [], 'observed_position': len(self.state['presentations'])})
        for field in answer_fields(question):
            if str(field.get('source_result', '')).lower() != 'correct':
                continue
            submitted = next((response for submission in reversed(record['submissions'])
                              for response in submission.get('responses', []) if response['key'] == field['key']
                              and submission.get('outcome') not in ('entry_failed', 'not_submitted')
                              and (submission.get('outcome') == 'observe_to_confirm'
                                   or str(response.get('value')) == str((field.get('source_selected') or field.get('source_correct') or {}).get('value')))), None)
            if submitted is not None:
                field['correct_value'] = submitted['value']
                if submitted.get('value_type'):
                    field['value_type'] = submitted['value_type']
                field['evidence'] = {'kind': 'ma_correct_grade', 'value': submitted['value'], 'grade': 'correct',
                                     'source_file': observation.get('html_path') or question.get('html_path'),
                                     'presentation_key': key}
        record['question'] = merge_question(record['question'], question)
        record['last_observation'] = observation
        self._record_step(observation)
        if observation.get('accepted'):
            record['accepted'] = True
            record['feedback'] = {**question, **{k: v for k, v in observation.items() if k != 'question'}}
            if observation.get('grade'):
                record['grade'] = observation['grade']
                if self.activity['kind'] == 'diagnostic' and str(observation['grade']).lower() in ('correct', 'full credit', 'skipped question'):
                    self.state['diagnostic_retry_active'] = False
            self._save()
            if self.exposures:
                self.exposures.reconcile(self.state)
            failure = self.state.get('pending_browser_error') or {}
            if (repeated >= 3 and failure.get('method') == 'advance'
                    and failure.get('attempt', 0) > record.get('continuation_recovery_attempt', 0)):
                record['continuation_recovery_attempt'] = failure['attempt']
                self._save()
                self._recover_page(observation, repeated)
                return
            self._browser_call('advance', observation, self.directory)
            return
        server_failures = record.get('submission_server_failures') or {}
        if (self.activity['kind'] not in ('assessment', 'diagnostic')
                and server_failures.get('count', 0) >= 3
                and server_failures.get('binding') == self._answer_binding(question)):
            # A reload can clear local spinner state without fixing the server.
            # Observe this pinned question, but stop repeating unconfirmed POSTs
            # or asking the mathematics agent to solve a transport failure.
            self.state['pending_capture_blocker'] = {
                'signature': self._signature(observation), 'observation_key': observation.get('key'),
                'error': server_failures['error'] + '; repeated submissions held pending recovery',
                'retry_at': self.clock() + self.config.recovery_max_delay,
                'submission_server_failure': True}
            self._save()
            return
        # A source-visible editable question means an unknown response did not
        # advance it. Reconcile its current shape before choosing another action.
        if self.activity['kind'] == 'diagnostic' and key not in self.state['policy']['decisions']:
            self._classify(question, observation)
            record['question'] = merge_question(record['question'], question)
        self.policy.answer_profile = account_profile(self.config)
        if self.policy.answer_profile != 'capture' and self.exposures is None:
            self.exposures = ExposureStore(self.config)
            self.exposures.reconcile(self.state)
            self.policy.exposures = self.exposures
        decision = self.policy.decide(key, question, record['started_at'])
        record['decision'] = decision
        self._prepare_answer_pacing(record, observation)
        self._save()
        if self._submit_if_due(observation):
            return
        if decision['action'] == 'dont_know':
            if observation.get('can_dont_know', True):
                self._submit(record, observation, {'action': 'dont_know'})
                return
            override(decision, 'C', "Don't Know is unavailable; use the best valid response")
        # An assessment filled answer is entered, not graded. The browser adapter
        # marks those observations accepted only after verifying the entered values.
        solution = record.get('solution')
        current_binding = self._answer_binding(question)
        failure = self.state.get('pending_browser_error') or {}
        reconsider_after = 2 if self.activity['kind'] == 'assessment' and failure.get('entry_failed') else 4
        if failure.get('method') == 'respond' and failure.get('attempt', 0) >= reconsider_after and not failure.get('not_submitted'):
            recovery_key = failure.get('failure_key', '') + ':' + current_binding
            attempts = record.setdefault('entry_reconsiderations', {}).get(recovery_key, 0)
            if attempts < 2:
                record['entry_reconsiderations'][recovery_key] = attempts + 1
                record['reconsider_reason'] = {'browser_error': failure['error'],
                    'instruction': 'The answer could not be entered or verified. Check the source fields and return valid alternative entry keys or a supported response.',
                    'attempt': attempts + 1}
                record['replace_solver'] = attempts > 0
                record.pop('solution_binding', None)
            elif observation.get('can_dont_know') or observation.get('can_skip'):
                override(decision, 'D', 'Repeated entry failures persist after focused reconsideration; use the offered skip to continue')
                self._submit(record, observation, {'action': 'dont_know' if observation.get('can_dont_know') else 'skip'})
                return
        if not solution or record.get('solution_binding') != current_binding:
            payload = self._question_payload(question, observation, record)
            try:
                solution = self.solver.request('solve_question', payload, timeout=self._solver_budget(observation),
                                               force_new=bool(record.pop('replace_solver', False)))
                record.update(solution=solution, solution_binding=current_binding)
            except SolverUnavailable as error:
                self._event('solver_best_attempt', key=key, error=str(error))
                solution = {'status': 'unavailable', 'reasoning': str(error), 'answers': []}
                record['solver_failure'] = str(error)
            self._save()
        if self._submit_if_due(observation):
            return
        supports_wrong = supports_intentional_error(question, solution)
        obsolete_overrides = (
            'Resolve uncertainty using the best supported response instead of an intentional error',
            "Use Math Academy's revealed expected response to advance")
        actual_attempts = any(submission.get('outcome') not in ('entry_failed', 'not_submitted')
                              for submission in record['submissions'])
        # A paused, unsubmitted response may carry the old source-key override.
        # Restore its original draw only when the current mathematics supports it.
        if (supports_wrong and not actual_attempts and decision.get('planned') == 'W'
                and decision.get('intended') == 'C'
                and decision.get('deviation_reason') in obsolete_overrides):
            previous_reason = decision['deviation_reason']
            override(decision, 'W', 'Restore the planned wrong response; missing MA key does not make the mathematics uncertain')
            self._event('answer_policy_restored', key=key, previous_reason=previous_reason)
        if not supports_wrong and decision['intended'] == 'W':
            override(decision, 'C', 'Resolve uncertainty using the best supported response instead of an intentional error')
        source_preferred = actual_attempts and any(a.get('ma_value') is not None for a in solution.get('answers', []))
        if source_preferred:
            override(decision, 'C', "Use Math Academy's revealed expected response to advance")
        source_rejection = bool(question.get('proof_feedback')) or any(
            str(field.get('source_result', '')).lower() in ('incorrect', 'partial credit')
            for field in answer_fields(question))
        feedback_binding = semantic_identity('source_feedback', {
            'feedback': feedback_evidence(question),
            'fields': [{'key': field.get('key'), 'source_result': field.get('source_result'),
                        'source_selected': field.get('source_selected')} for field in answer_fields(question)]})
        if (source_rejection and actual_attempts
                and record.get('reconsidered_feedback') != feedback_binding):
            # A rejected/partial response gets new observed evidence and a focused
            # reconsideration, rather than an infinite replay of the same answer.
            payload = self._question_payload(question, observation, record)
            payload['recovery'] = 'The current response has not advanced; inspect the revealed feedback and any additional fields.'
            try:
                solution = self.solver.request('solve_question', payload, timeout=self._solver_budget(observation))
                record['solution'] = solution
                record['reconsidered_feedback'] = feedback_binding
                source_preferred = any(a.get('ma_value') is not None for a in solution.get('answers', []))
            except SolverUnavailable as error:
                self._event('solver_reconsider_unavailable', key=key, error=str(error))
            override(decision, 'C', 'The previous action did not advance; use a reconsidered best response')
        responses = responses_for(question, solution, decision, source_preferred=source_preferred)
        if not responses:
            if observation.get('can_skip') or observation.get('can_dont_know'):
                self._submit(record, observation, {'action': 'dont_know' if observation.get('can_dont_know') else 'skip'})
            else:
                self._recover_page(observation, repeated)
            return
        self._save()
        self._pace_answer(record, observation)
        if self._submit_if_due(observation):
            return
        # Waiting or solving may have changed the page; read again before writing.
        fresh = self._browser_call('observe', self.directory)
        self._observe_timing(fresh)
        if fresh.get('kind') != 'complete' and self._submit_if_due(fresh):
            return
        if fresh.get('kind') != 'question' or fresh.get('accepted') or str(fresh.get('key') or key).split(':fields:', 1)[0] != key:
            return
        current = fresh.get('question') or question
        if self._answer_binding(current) != current_binding:
            record.pop('solution_binding', None)
            self._save()
            return
        # Display order/tokens can change independently of content; rebind now.
        responses = responses_for(current, solution, decision, source_preferred=source_preferred)
        self._submit(record, fresh, responses)
        if repeated >= 5:
            self._recover_page(fresh, repeated)

    def _submit(self, record, observation, responses):
        submission = {'started_at': self.clock(), 'responses': responses if isinstance(responses, list) else [],
                      'action': responses.get('action') if isinstance(responses, dict) else 'answer',
                      'intended': record['decision']['intended'], 'planned': record['decision']['planned']}
        record['submissions'].append(submission)
        self._save()
        result = self._browser_call('respond', observation, responses, self.directory)
        submission['returned_at'] = self.clock()
        submission['outcome'] = ('not_submitted' if isinstance(result, dict) and result.get('not_submitted') else
                                 'entry_failed' if isinstance(result, dict) and result.get('entry_failed') else
                                 'unknown' if isinstance(result, dict) and result.get('unknown_outcome') else 'observe_to_confirm')
        if isinstance(result, dict) and result.get('error'):
            submission['browser_error'] = result['error']
        http_status = result.get('http_status') if isinstance(result, dict) else None
        if http_status is not None and http_status >= 500:
            submission['http_status'] = result['http_status']
            binding = self._answer_binding(observation.get('question') or record['question'])
            previous = record.get('submission_server_failures') or {}
            record['submission_server_failures'] = {'binding': binding,
                'count': previous.get('count', 0) + 1 if previous.get('binding') == binding else 1,
                'error': result['error'], 'http_status': result['http_status']}
        self._save()

    @staticmethod
    def _answer_binding(question):
        # Choice order and letter labels are intentionally excluded.
        fields = [{'key': f.get('key'), 'type': f.get('type'),
                   'choices': sorted((str(c.get('type')), str(c.get('value'))) for c in f.get('choices', []))}
                  for f in answer_fields(question)]
        return hashlib.sha256(json.dumps({'problem': question.get('problem'), 'fields': fields}, sort_keys=True).encode()).hexdigest()

    @staticmethod
    def _normalize_kp(question, example=False):
        identity = question.get('kp_id') or question.get('knowledge_point_id') or question.get('knowledge_point_source_id')
        if identity is None and example and str(question.get('math_academy_id', '')).startswith('e-'):
            identity = question['math_academy_id'][2:]
        if identity is not None:
            if str(identity).startswith('e-'):
                identity = str(identity)[2:]
            question['kp_id'] = str(identity)
            question['knowledge_point_id'] = str(identity)

    def _question_payload(self, question, observation, record):
        # Independent lesson/review questions need no preceding practice archive.
        payload = {'question': question, 'observation': observation,
                   'previous_submissions': record.get('submissions', [])}
        if record.get('reconsider_reason'):
            payload['recovery'] = deepcopy(record['reconsider_reason'])
        example_id = str(question.get('source_example_id') or 'e-' + str(question.get('kp_id') or ''))
        example = next((step['question'] for step in reversed(self.state['steps'])
                        if step.get('kind') == 'example' and step.get('question')
                        and str(step['question'].get('math_academy_id')) == example_id), None)
        if example:
            payload['current_example'] = example
        if self.activity['kind'] == 'multistep':
            payload.update(activity={'kind': 'multistep'}, shared_context=self.state.get('shared_context'),
                earlier_parts=[r for r in self.state['presentations'].values()
                               if r['key'] != record['key'] and r.get('observed_position', 0) < record.get('observed_position', 0)])
        return task_payload('solve_question', payload)

    def _solver_budget(self, observation):
        remaining = self._remaining_seconds(observation)
        if remaining is None:
            return self.config.solver_timeout
        available = float(remaining) - self._submission_reserve()
        count = (self.state.get('assessment_timing') or {}).get('question_count') or self.activity.get('details', {}).get('question_count')
        position = observation.get('sequence_position') or observation.get('question', {}).get('sequence_position')
        if self.activity['kind'] == 'assessment' and count and position:
            available /= max(1, int(count) - int(position) + 1)
        return max(.1, min(self.config.solver_timeout, available))

    def _classify(self, question, observation):
        context = self.state['context']
        if self.context_provider and (context.get('unavailable') or context.get('snapshot_unavailable')):
            try:
                context = self.context_provider(self.activity)
                self.state['context'] = context
                self.policy.refresh_context(context)
                self._save()
            except StopRequested:
                raise
            except Exception as error:
                self._event('context_unavailable', error=str(error))
        bindings = context.get('question_topics', context.get('source_question_bindings', {}))
        bound = bindings.get(question.get('math_academy_id'))
        if bound:
            question['topic_id'] = topic_id(bound)
        if question.get('topic_id') is not None:
            return
        source_id = question.get('math_academy_id')
        lookup = getattr(self.context_provider, 'question_topic', None)
        if source_id and lookup:
            try:
                source_binding = lookup(source_id)
            except StopRequested:
                raise
            except Exception as error:
                source_binding = None
                self._event('question_topic_lookup_unavailable', question=source_id, error=str(error))
            if source_binding and source_binding.get('topic_id') is not None:
                question['topic_id'] = str(source_binding['topic_id'])
                question['topic_match'] = source_binding
                return
        topics = context.get('topics') or context.get('all_topics') or context.get('course_topics', [])
        distances = self.state['policy']['distances']
        topics = [topic for topic in topics if topic_id(topic) in distances]
        if not topics:
            question['topic_match'] = {'topic_id': None, 'reasoning': 'No course topic context available'}
            return
        graph = {str(source): [target for target in targets if topic_id(target) in distances]
                 for source, targets in context.get('graph', {}).items() if str(source) in distances}
        try:
            result = self.solver.request('match_topic', {'question': question, 'topics': topics,
                'course_topics': context.get('course_topics', []), 'graph': graph,
                'screenshot': observation.get('screenshot')}, timeout=self._solver_budget(observation))
            if result.get('confidence', 0) >= .5:
                question['topic_id'] = result.get('topic_id')
            question['topic_match'] = result
        except SolverUnavailable as error:
            question['topic_match'] = {'topic_id': None, 'reasoning': str(error)}

    def _recover_page(self, observation, repeated):
        if self._submit_if_due(observation):
            return
        failure = self.state.get('pending_browser_error') or {}
        rendering_key = observation.get('key')
        rendering_reloads = self.state.setdefault('rendering_reloads', {})
        if (repeated >= 3 and str(rendering_key or '').startswith('unready-')
                and observation.get('readiness_errors')
                and self.activity['kind'] not in ('assessment', 'diagnostic')
                and not rendering_reloads.get(rendering_key) and hasattr(self.browser, 'open')):
            # A missing widget script cannot recover by waiting on its empty
            # placeholder. Reload once, then reread the pinned server activity.
            rendering_reloads[rendering_key] = {'at':self.clock()}
            self._save()
            self._event('source_rendering_reload', observation_key=rendering_key,
                        errors=observation['readiness_errors'])
            self._browser_call('open', self.activity, self.directory, self.state)
            return
        reloads = self.state.setdefault('dropdown_reloads', {})
        failure_key = failure.get('failure_key')
        if (repeated >= 3 and failure.get('attempt', 0) >= 2
                and failure.get('method') == 'respond' and failure.get('entry_failed')
                and failure.get('error_type') == 'DropdownUnavailable' and failure_key
                and self.activity['kind'] not in ('assessment', 'diagnostic')
                and not reloads.get(failure_key) and hasattr(self.browser, 'open')):
            # A page reload can clear stale widget state; asking the solver for
            # another answer cannot. Reobserve server state before any entry.
            reloads[failure_key] = {'at': self.clock(), 'observation_key': observation.get('key')}
            self._save()
            self._event('dropdown_layout_reload', observation_key=observation.get('key'),
                        failure_key=failure_key, layout=failure.get('layout'))
            self._browser_call('open', self.activity, self.directory, self.state)
            return
        self._event('page_recovery', observation_key=observation.get('key'), repeated=repeated)
        action = 'reload' if repeated >= 3 else 'wait'
        result = None
        payload = {'observation': observation, 'activity': self.activity,
                   'browser_error': self.state.get('pending_browser_error'),
                   'question': observation.get('question')}
        identity = semantic_identity('interpret_page', task_payload('interpret_page', payload))
        attempts = self.state.setdefault('page_recovery_attempts', {}).get(identity, 0)
        if repeated >= 3 and attempts >= 2:
            # The same evidence exhausted focused recovery. Keep the task pinned,
            # expose the blocker, and permit only spaced probes until it changes.
            action = 'wait'
            previous = self.state.get('pending_capture_blocker') or {}
            probes = previous.get('probes', 0) + 1
            error = (self.state.get('pending_browser_error') or {}).get('error') or 'Activity did not advance after focused recovery'
            self.state['pending_capture_blocker'] = {'signature': self._signature(observation),
                'observation_key': observation.get('key'), 'error': error, 'probes': probes,
                'retry_at': self.clock() + self.pacer.backoff(probes + 3)}
            if not previous:
                self._event('capture_stalled', observation_key=observation.get('key'), error=error)
        if repeated >= 2 and attempts < 2:
            try:
                self.state['page_recovery_attempts'][identity] = attempts + 1
                self._save()
                result = self.solver.request('interpret_page', payload, timeout=self._solver_budget(observation), force_new=attempts > 0)
                validate_result('interpret_page', payload, result)
                action = result['action']
                self._event('page_interpretation', judgment=result)
            except (SolverUnavailable, ValueError) as error:
                result = None
                self._event('page_interpretation_unavailable', error=str(error))
        self.state['recoveries'] += 1
        self.state['recovery_action'] = {'observation_key': observation.get('key'), 'action': action,
                                         'decision': result, 'started_at': self.clock()}
        self._save()
        if action == 'advance':
            if result and result.get('button_selector') and hasattr(self.browser, 'recover'):
                self._browser_call('recover', observation, result, self.directory)
            else:
                self._browser_call('advance', observation, self.directory)
        elif action == 'reload' and hasattr(self.browser, 'restart'):
            self._browser_call('restart')
            self._browser_call('open', self.activity, self.directory, self.state)
        elif action == 'retry_answer':
            key = str(observation.get('key', '')).split(':fields:', 1)[0]
            record = self.state['presentations'].get(key)
            if record:
                record.pop('solution_binding', None)
                record['replace_solver'] = attempts > 0
                record['reconsider_reason'] = {'instruction': result['reasoning'],
                    'browser_error': self.state.get('pending_browser_error'), 'retry': attempts + 1}
                self._save()
        else:
            if self.state.get('pending_capture_blocker'):
                return  # The execution loop observes, waits, and probes safely.
            delay = self.pacer.backoff(repeated + 1)
            remaining = self._remaining_seconds(observation)
            self.sleep(min(delay, max(0, remaining - self._submission_reserve())) if remaining is not None else delay)

    def _review(self):
        history = self.state.get('history')
        if history is None:
            history = self._browser_call('history', self.activity, self.directory)
            self.state['history'] = history
            self._save()
        lookup = getattr(self.context_provider, 'source_dependencies', None)
        if (lookup and hasattr(self.browser, 'lesson_source') and self.activity['kind'] != 'lesson'
                and not self.state.get('source_dependencies_checked')):
            for tid in lookup(history.get('questions', [])):
                source = self._browser_call('lesson_source', tid, self.directory / 'dependencies' / str(tid))
                definition = source.get('lesson_definition') or {}
                history.setdefault('source_lesson_definitions', {})[str(tid)] = definition
                history = self._merge_content(history, self._dependency_content(source, history.get('questions', [])))
                self.state['history'] = history
                self._save()
            self.state['source_dependencies_checked'] = True
            self._save()
        content = self._merge_history(history)
        gaps = capture_gaps(content)
        if any(not gap.get('final') for gap in gaps) and not self.state.get('source_recovery_attempted'):
            self.state['source_recovery_attempted'] = True
            self.state['source_gaps'] = gaps
            self._save()
            # Fetch the source pages while still in this activity. The browser's
            # history reader includes its full lesson-page review and image retries.
            retry = self._browser_call('history', self.activity, self.directory)
            history = self._merge_content(history, retry)
            self.state['history'] = history
            self._save()
            content = self._merge_history(history)
        content['source_limitations'] = content.get('source_limitations', []) + capture_gaps(content)
        for name in ('questions', 'reference_questions', 'canonical_examples'):
            for index, question in enumerate(content.get(name, [])):
                self._normalize_kp(question, example=name == 'canonical_examples')
                key = name + ':' + question_key(question)
                presentations = self._question_presentations(question)
                payload = {'question': question, 'presentations': presentations,
                           'source_limitations': content['source_limitations']}
                if self.activity['kind'] == 'multistep':
                    payload.update(activity={'kind': 'multistep'}, shared_context=content.get('multistep'),
                        earlier_parts=[r for r in self.state['presentations'].values()
                            if r not in presentations and (r['question'].get('sequence_position') or r.get('observed_position', -1) + 1)
                            < (question.get('sequence_position') or index + 1)])
                payload = task_payload('judge_question', payload)
                evidence_hash = semantic_identity('judge_question', payload)
                saved = self.state['judgments'].get(key)
                if saved and saved.get('evidence_hash') == evidence_hash:
                    judgment = saved
                else:
                    attempts = max(1, int(getattr(self.config, 'solver_attempts', 2)))
                    for attempt in range(attempts):
                        check_stop(self.stop_event)
                        try:
                            judgment = self.solver.request('judge_question', payload)
                            break
                        except SolverUnavailable as error:
                            self._event('final_agent_retry', question=key, error=str(error), attempt=attempt + 1)
                            if not getattr(error, 'retryable', True) or attempt + 1 == attempts:
                                raise
                            self.sleep(backoff(attempt + 1, self.config.retry_delay, self.config.recovery_max_delay))
                    judgment = {**judgment, 'question_id': question.get('math_academy_id'),
                                'capture_key': question_key(question), 'record_kind': name,
                                'evidence_hash': evidence_hash, 'final': True, 'judged_at': self.clock()}
                    self.state['judgments'][key] = judgment
                    self._save()
                    self._event('judgment_saved', question=key, status=judgment['status'])
                content[name][index] = self._validate_final_answers(question, presentations, judgment, payload, name, key, content)
        content['lesson_workload_sample'] = self._lesson_sample(content)
        content['answer_validation_version'] = 1
        return content

    def _validate_final_answers(self, question, presentations, judgment, payload, name, key, content):
        finalized = finalize_answers(question, presentations, judgment)
        try:
            checked = authoritative_question(finalized, example=name == 'canonical_examples')
        except UnsupportedContent as error:
            gap = str(error)
            repair_payload = task_payload('judge_question', {**payload, 'question': finalized,
                'gap': gap, 'recovery': 'Final source validation failed. For each unsupported field, return the exact current typed choice and one contiguous verbatim worked-solution span alone, without added quotation marks, labels, or explanation, or identify its captured visible answer. Quote the intervening source when several answer components are needed. Explain authored source errors separately in reasoning. Do not attribute an unbound grade to a response.'})
            evidence_hash = semantic_identity('judge_question', repair_payload)
            repairs = self.state.setdefault('answer_evidence_reviews', {})
            repair = repairs.get(evidence_hash)
            if repair is None:
                repair = self.solver.request('judge_question', repair_payload)
                repair = {**repair, 'question_id': question.get('math_academy_id'),
                    'capture_key': question_key(question), 'record_kind': name,
                    'gap': gap, 'evidence_hash': evidence_hash, 'final': True, 'judged_at': self.clock()}
                repairs[evidence_hash] = repair
                self._save()
            finalized = finalize_answers(finalized, presentations, repair)
            self.state['judgments'][key] = repair
            self._save()
            try:
                checked = authoritative_question(finalized, example=name == 'canonical_examples')
            except UnsupportedContent as final_error:
                finalized['answer_validation'] = {'status': 'unavailable', 'gap': str(final_error),
                    'evidence_hash': evidence_hash, 'judgment': repair, 'final': True}
                content['source_limitations'].append({'question': question_key(question), 'record_kind': name,
                    'reason': str(final_error), 'judgment': repair, 'final': True})
                return finalized
        checked['answer_validation'] = {'status': 'supported', 'version': 1,
            'evidence_hash': semantic_identity('finalized_source', checked)}
        return checked

    @staticmethod
    def _dependency_content(source, questions):
        """Retain the examples needed by captured practice, without importing empty KPs."""
        required = {(str(q.get('topic_id')), str(q.get('kp_id') or q.get('knowledge_point_id') or ''),
                     q.get('knowledge_point') or q.get('kp_title')) for q in questions}
        examples = []
        for example in source.get('canonical_examples', []):
            tid = str(example.get('topic_id'))
            kid = str(example.get('kp_id') or example.get('knowledge_point_id') or
                      str(example.get('math_academy_id', '')).removeprefix('e-'))
            title = example.get('knowledge_point') or example.get('kp_title')
            if any(t == tid and (k and k == kid or name and name == title) for t, k, name in required):
                examples.append(example)
        return {'canonical_examples': examples, 'tutorials': source.get('tutorials', [])}

    @staticmethod
    def _source_binding_matches(before, after):
        """History positions and permanent IDs still need matching source content."""
        def binding(question):
            def text(value, *, boundaries=False):
                value = str(value) if value is not None else ''
                # A history page can lose MathJax's boldsymbol extension and
                # render the formatting command itself as a red error token.
                # Ignore only that DOM-proven artifact for source comparison;
                # retain both original prompts and all mathematical operands.
                if re.search(r'<mtext\b[^>]*\bmathcolor=[\"\']red[\"\'][^>]*>\\boldsymbol</mtext>',
                             question.get('html', ''), re.I):
                    value = value.replace(r'\text{\boldsymbol}', '')
                for asset in question.get('assets', []):
                    if asset.get('sha256'):
                        for name in ('path', 'source_url'):
                            if asset.get(name):
                                value = value.replace(asset[name], '@image:' + asset['sha256'])
                if boundaries:
                    # Live/history paragraph wrappers can move whitespace next
                    # to a formula or input without changing authored content.
                    # Keep each mathematical span intact: "1 2" is not "12".
                    value = re.sub(r'(?<!\\)(\$\$.*?(?<!\\)\$\$|\$(?:\\.|[^$])*?(?<!\\)\$|\{\{field-\d+\}\})',
                                   lambda match: ' ' + match[0] + ' ', value, flags=re.S)
                    # Live reasoning is adjacent to its introduction; history
                    # wraps it in a paragraph. Compare that prose boundary,
                    # retaining whitespace and punctuation inside mathematics.
                    spans = re.split(r'(?<!\\)(\$\$.*?(?<!\\)\$\$|\$(?:\\.|[^$])*?(?<!\\)\$)', value, flags=re.S)
                    value = ''.join(span if index % 2 else
                        re.sub(r'(?<=[.!?])(?=[A-Za-z])', ' ',
                            re.sub(r'<p>\s*</p>', '', span))
                        for index, span in enumerate(spans))
                return re.sub(r'\s+', ' ', value).strip()
            fields = [{'key': str(field.get('key', index)), 'type': field.get('type'),
                       'choices': sorted((str(choice.get('type')), text(choice.get('value')))
                                         for choice in field.get('choices', []))}
                      for index, field in enumerate(answer_fields(question))]
            return text(question.get('problem'), boundaries=True), sorted(fields, key=lambda field: field['key'])
        return bool(before.get('problem') and after.get('problem')) and binding(before) == binding(after)

    @classmethod
    def _history_content_matches(cls, before, after):
        """Fieldless history can refresh source text without confirming a response."""
        identity = str(before.get('math_academy_id') or '')
        parts = set(after.get('extraction_parts', []))
        if (not re.fullmatch(r'q-\d+', identity) or identity != str(after.get('math_academy_id')) or
                str(before.get('source_id', '')).startswith('unreconciled:') or
                not {'problem', 'solution'} <= parts or 'fields' in parts or answer_fields(after)):
            return False
        # Keep the same normalization of source images and whitespace, but do
        # not demand controls that this history view explicitly did not expose.
        return cls._source_binding_matches({**before, 'fields': [], 'answer_fields': []}, after)

    @staticmethod
    def _verified_history_revision(before, after, *, diagnostic=False):
        """A permanent DOM identity survives a content/rendering revision.

        This proves identity only. It never transfers a grade or answer between
        different versions; the complete history version is judged on its own.
        """
        identity = str(before.get('math_academy_id') or '')
        if (not re.fullmatch(r'q-\d+',identity) or identity != str(after.get('math_academy_id'))
                or after.get('answer_fields_complete') is not True
                or not answer_fields(after) or not after.get('problem') or not after.get('worked_solution')
                or any(not str(error).startswith('Screenshot unavailable:') for error in after.get('errors',[]))):
            return False
        from bs4 import BeautifulSoup
        for index,question in enumerate((before,after)):
            root = BeautifulSoup(question.get('html') or '', 'html.parser').find()
            dom_id = root.get('id') if root else None
            allowed = ('step-q'+identity[2:],) if diagnostic and index == 0 else (
                'step-q'+identity[2:], 'question-'+identity[2:])
            if not dom_id or dom_id != question.get('dom_id') or dom_id not in allowed:
                return False
        return True

    def _question_presentations(self, question):
        identity = question.get('math_academy_id')
        position = question.get('sequence_position')
        return [r for r in self.state['presentations'].values()
                if self._source_binding_matches(r['question'], question) and
                ((identity and str(r['question'].get('math_academy_id')) == str(identity)) or
                 (question.get('live_presentation_key') is not None and question['live_presentation_key'] == r.get('key')) or
                 (not r['question'].get('math_academy_id') and position is not None and
                  r.get('observed_position', -1) + 1 == position))]

    def _merge_history(self, history):
        content = {'task_id': str(self.activity['task_id']), 'kind': self.activity['kind'],
                   'title': self.activity.get('title'), 'topic_id': self.activity.get('topic_id'),
                   'course_id': self.activity.get('course_id'), 'activity': self.activity,
                   'questions': [], 'canonical_examples': [], 'tutorials': [],
                   'observed_steps': deepcopy(self.state['steps'])}
        sources = history.get('questions', [])
        records = list(self.state['presentations'].values())
        limitations, questions, source_variants = [], [], []
        # A missed/repeated diagnostic presentation shifts history positions.
        # Never grant an ID or grade from the position without source agreement.
        for record in records:
            question = record['question']
            if not question.get('math_academy_id'):
                matching = [q for q in sources if q.get('math_academy_id') and
                    q.get('sequence_position') == record.get('observed_position', -1) + 1 and
                    self._source_binding_matches(question, q)]
                if len(matching) == 1:
                    question['math_academy_id'] = matching[0]['math_academy_id']

        for record in records:
            question = record['question']
            identity = question.get('math_academy_id')
            same_id = [q for q in sources if identity is not None and str(q.get('math_academy_id')) == str(identity)]
            matching = [q for q in same_id if self._source_binding_matches(question, q)]
            repeated = [r for r in records if (r['question'].get('math_academy_id') is None or
                        str(r['question'].get('math_academy_id')) == str(identity)) and
                        self._source_binding_matches(question, r['question'])]
            positioned = [q for q in matching if q.get('sequence_position') == record.get('observed_position', -1) + 1]
            if len(positioned) == 1 and (len(repeated) == 1 or len(repeated) == len(matching)):
                record['feedback'] = {**record.get('feedback', {}), **positioned[0]}
            elif positioned:
                limitations.append({'question': str(identity), 'presentation_key': record.get('key'),
                    'reason': 'History grade cannot be assigned unambiguously across repeated presentations'})

            live_question = deepcopy(question)
            feedback = record.get('feedback') or {}
            if feedback.get('problem') and not self._source_binding_matches(question, feedback):
                record['unmatched_history_feedback'] = feedback
                record['feedback'] = {}
            content_matches = matching or [q for q in same_id if self._history_content_matches(question, q)]
            if (not content_matches and len(same_id) == 1
                    and self._verified_history_revision(question,same_id[0],
                        diagnostic=self.activity['kind']=='diagnostic')):
                # Preserve the earlier source version and its actual learner
                # observations, rather than inventing an ID-less extra question.
                source_variants.append({'math_academy_id':identity,'presentation_key':record.get('key'),
                    'question':live_question,'history_source':same_id[0].get('html_path'),
                    'reason':'Same verified permanent DOM ID; complete history has different content or rendering. No grade transferred.'})
                continue
            if (same_id and not content_matches) or not identity:
                if same_id or sources:
                    limitations.append({'question': str(identity) if identity is not None else question_key(question),
                        'presentation_key': record.get('key'),
                        'reason': 'Live source content did not match the history identity and position'})
                if same_id:
                    # Keep conflicting originals without letting the ID merge
                    # overwrite one problem or promote its grade onto the other.
                    live_question['observed_math_academy_id'] = live_question.pop('math_academy_id')
                live_question['source_id'] = 'unreconciled:' + str(record.get('key'))
                live_question['live_presentation_key'] = record.get('key')
            questions.append(live_question)

        live = {'questions': questions,
                'canonical_examples': [s['question'] for s in self.state['steps'] if s.get('kind') == 'example' and s.get('question')],
                'tutorials': [s.get('tutorial', s) for s in self.state['steps']
                              if s.get('kind') == 'tutorial' and self.activity['kind'] != 'multistep']}
        content = self._merge_content(content, live)
        self._save()
        content = self._merge_content(content, history)
        if source_variants:
            content['source_variants'] = source_variants
        content['source_limitations'] = content.get('source_limitations', []) + limitations
        if self.exposures:
            self.exposures.reconcile(self.state)
        return content

    @staticmethod
    def _merge_content(before, after):
        result = deepcopy(before)
        for key, value in after.items():
            if key == 'examples':
                key = 'canonical_examples'
            if key in ('questions', 'reference_questions', 'canonical_examples'):
                records = {question_key(q): q for q in result.get(key, [])}
                for q in value or []:
                    identity = question_key(q)
                    records[identity] = merge_question(records.get(identity, {}), q)
                result[key] = list(records.values())
            elif key == 'tutorials':
                records = {str(q.get('math_academy_id') or q.get('source_id') or q.get('capture_key') or q.get('title')): q for q in result.get(key, [])}
                for q in value or []:
                    identity = str(q.get('math_academy_id') or q.get('source_id') or q.get('capture_key') or q.get('title'))
                    records[identity] = {**records.get(identity, {}), **q}
                result[key] = list(records.values())
            elif value is not None and value != '' and value != []:
                result[key] = deepcopy(value)
        return result

    def _lesson_sample(self, content):
        if self.activity['kind'] != 'lesson':
            return None
        by_id = {q.get('math_academy_id'): q for q in content.get('questions', [])}
        samples = {}
        for presentation in sorted(self.state['presentations'].values(), key=lambda p: p.get('observed_position', 0)):
            question = by_id.get(presentation['question'].get('math_academy_id'), presentation['question'])
            kp = str(question.get('kp_id') or question.get('knowledge_point_source_id') or question.get('knowledge_point_id') or 'unknown')
            selected = samples.setdefault(kp, [])
            identity = question.get('math_academy_id')
            if identity and identity not in selected and len(selected) < 2:
                selected.append(identity)
        completion = self.state.get('completion', {})
        completion = completion.get('completion', completion)
        return {'questions_by_knowledge_point': samples, 'base_xp': content.get('base_xp') or completion.get('base_xp'),
                'selection': 'first-two-distinct-practice-questions-in-observed-order', 'expected_difficulty_weight': 1.6}
