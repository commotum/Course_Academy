"""An activity stays pinned until its source review and agent judgments are complete."""

from copy import deepcopy
import hashlib
import json
import logging
from pathlib import Path
import random
import time

from ..runtime import StopRequested, backoff, check_stop, wait
from ..storage import append_event, atomic_json, read_json
from .evidence import capture_gaps, finalize_answers, merge_question, question_key
from .policy import AnswerPolicy, answer_fields, override, responses_for, topic_id
from .solver import SolverClient, SolverUnavailable, validate_result


class ActivityCapture:
    def __init__(self, config, browser, stop_event, context_provider=None, *, solver=None,
                 clock=time.time, sleeper=None, rng=None):
        self.config, self.browser, self.stop_event = config, browser, stop_event
        self.context_provider = context_provider
        self.solver = solver
        self.clock = clock
        self.sleep = sleeper or (lambda seconds: wait(stop_event, seconds))
        self.rng = rng or random.Random(config.seed)

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
        if self.solver is None:
            self.solver = SolverClient(self.config, self.directory, self.stop_event)
        if self.state.get('context') is None:
            try:
                self.state['context'] = self.context_provider(activity) if self.context_provider else {}
            except StopRequested:
                raise
            except Exception as error:
                # The database provider may use its own last good snapshot. An absent
                # graph is an explicit unknown-topic diagnostic action, not a halt.
                self.state['context'] = {'unavailable': str(error)}
            self._save()
        self.policy = AnswerPolicy(activity, self.state['policy'], self.state['context'], self.rng, self.clock)
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
        atomic_json(self.checkpoint_path, self.state)

    def _event(self, event, **values):
        append_event(self.directory / 'activity-events.jsonl', event, **values)

    def _browser_call(self, method, *args):
        attempts = 0
        while True:
            check_stop(self.stop_event)
            try:
                return getattr(self.browser, method)(*args)
            except StopRequested:
                raise
            except Exception as error:
                attempts += 1
                self.state['recoveries'] += 1
                self._save()
                self._event('browser_retry', method=method, error=str(error), attempt=attempts)
                logging.warning('%s task %s: %s; retrying', method, self.activity['task_id'], error)
                self.sleep(backoff(attempts, self.config.retry_delay, self.config.recovery_max_delay))
                # A timed-out Start/Continue/Submit may already have succeeded.
                # Return to observation before ANY further state-changing action.
                if method in ('respond', 'advance', 'recover'):
                    return {'unknown_outcome': True, 'error': str(error)}
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
            if observation.get('shared_contexts'):
                self.state['shared_context'] = observation['shared_contexts']
            signature = self._signature(observation)
            repeated = repeated + 1 if signature == last_signature else 0
            last_signature = signature
            kind = observation.get('kind', 'unknown')
            if kind == 'complete':
                self.state.update(stage='history', completion=observation, completed_at=self.clock())
                self._save()
                return
            if kind == 'question':
                if (self.activity['kind'] == 'assessment' and observation.get('remaining_seconds') is not None
                        and float(observation['remaining_seconds']) <= 5):
                    self._event('assessment_deadline_submission', remaining_seconds=observation['remaining_seconds'])
                    self.state['assessment_timing_deviation'] = 'Submit entered answers before the timer expires; judge any unanswered items in history'
                    self._save()
                    self._browser_call('respond', observation, {'action': 'submit_assessment'}, self.directory)
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
                           observation.get('grade'), shape], sort_keys=True, default=str)

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
                              for response in submission.get('responses', []) if response['key'] == field['key']), None)
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
            self._save()
            self._browser_call('advance', observation, self.directory)
            return
        # A source-visible editable question means an unknown response did not
        # advance it. Reconcile its current shape before choosing another action.
        if self.activity['kind'] == 'diagnostic' and key not in self.state['policy']['decisions']:
            self._classify(question, observation)
            record['question'] = merge_question(record['question'], question)
        decision = self.policy.decide(key, question, record['started_at'])
        record['decision'] = decision
        self._save()
        if decision['action'] == 'dont_know':
            if observation.get('can_dont_know', True):
                self._submit(record, observation, {'action': 'dont_know'})
                return
            override(decision, 'C', "Don't Know is unavailable; use the best valid response")
        # An assessment filled answer is entered, not graded. The browser adapter
        # marks those observations accepted only after verifying the entered values.
        solution = record.get('solution')
        current_binding = self._answer_binding(question)
        if not solution or record.get('solution_binding') != current_binding:
            payload = self._question_payload(question, observation, record)
            try:
                solution = self.solver.request('solve_question', payload, timeout=self._solver_budget(observation))
                record.update(solution=solution, solution_binding=current_binding)
            except SolverUnavailable as error:
                self._event('solver_best_attempt', key=key, error=str(error))
                solution = {'status': 'unavailable', 'reasoning': str(error), 'answers': []}
                record['solver_failure'] = str(error)
            self._save()
        if (solution.get('status') in ('ambiguous', 'unavailable', 'source_error') or solution.get('confidence', 1) < .5) and decision['intended'] == 'W':
            override(decision, 'C', 'Resolve uncertainty using the best supported response instead of an intentional error')
        source_preferred = bool(record['submissions']) and any(a.get('ma_value') is not None for a in solution.get('answers', []))
        if source_preferred:
            override(decision, 'C', "Use Math Academy's revealed expected response to advance")
        if repeated >= 2 and record['submissions']:
            # A rejected/partial response gets new observed evidence and a focused
            # reconsideration, rather than an infinite replay of the same answer.
            payload = self._question_payload(question, observation, record)
            payload['recovery'] = 'The current response has not advanced; inspect the revealed feedback and any additional fields.'
            try:
                solution = self.solver.request('solve_question', payload, force_new=repeated >= 4,
                                               timeout=self._solver_budget(observation))
                record['solution'] = solution
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
        remaining = max(0, decision['submit_at'] - self.clock())
        deadline = observation.get('remaining_seconds')
        if deadline is not None and remaining > max(0, float(deadline) - 5):
            remaining = max(0, float(deadline) - 5)
            decision['timing_deviation'] = 'Submit before the activity timer expires'
        self._save()
        self.sleep(remaining)
        # Waiting or solving may have changed the page; read again before writing.
        fresh = self._browser_call('observe', self.directory)
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
        submission['outcome'] = 'unknown' if isinstance(result, dict) and result.get('unknown_outcome') else 'observe_to_confirm'
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
        return {'activity': self.activity, 'question': question, 'observation': observation,
                'previous_submissions': record.get('submissions', []),
                'shared_context': self.state.get('shared_context'),
                'instructional_content': [s for s in self.state['steps'] if s.get('kind') in ('tutorial', 'example')],
                'earlier_parts': [{'question': r['question'], 'feedback': r.get('feedback'), 'solution': r.get('solution')}
                                 for r in self.state['presentations'].values() if r['key'] != record['key']]}

    def _solver_budget(self, observation):
        remaining = observation.get('remaining_seconds')
        if remaining is None:
            return self.config.solver_timeout
        available = float(remaining) - 10
        count = self.activity.get('details', {}).get('question_count')
        position = observation.get('sequence_position') or observation.get('question', {}).get('sequence_position')
        if self.activity['kind'] == 'assessment' and count and position:
            available /= max(1, int(count) - int(position) + 1)
        return max(.1, min(self.config.solver_timeout, available))

    def _classify(self, question, observation):
        context = self.state['context']
        bindings = context.get('question_topics', context.get('source_question_bindings', {}))
        bound = bindings.get(question.get('math_academy_id'))
        if bound:
            question['topic_id'] = topic_id(bound)
        if question.get('topic_id') is not None:
            return
        topics = context.get('topics') or context.get('all_topics') or context.get('course_topics', [])
        distances = self.state['policy']['distances']
        topics = [topic for topic in topics if topic_id(topic) in distances]
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
        self._event('page_recovery', observation_key=observation.get('key'), repeated=repeated)
        action = 'reload' if repeated >= 3 else 'wait'
        result = None
        if repeated >= 2:
            try:
                payload = {'observation': observation, 'activity': self.activity,
                           'previous_recovery_count': self.state['recoveries']}
                result = self.solver.request('interpret_page', payload, timeout=self._solver_budget(observation))
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
        else:
            self.sleep(backoff(repeated + 1, self.config.retry_delay, self.config.recovery_max_delay))

    def _review(self):
        history = self.state.get('history')
        if history is None:
            history = self._browser_call('history', self.activity, self.directory)
            self.state['history'] = history
            self._save()
        content = self._merge_history(history)
        gaps = capture_gaps(content)
        if gaps and not self.state.get('source_recovery_attempted'):
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
        for name in ('questions', 'canonical_examples'):
            for index, question in enumerate(content.get(name, [])):
                self._normalize_kp(question, example=name == 'canonical_examples')
                key = name + ':' + question_key(question)
                presentations = self._question_presentations(question)
                evidence_hash = hashlib.sha256(json.dumps({'question': question, 'presentations': presentations}, sort_keys=True).encode()).hexdigest()
                saved = self.state['judgments'].get(key)
                if saved and saved.get('evidence_hash') == evidence_hash:
                    judgment = saved
                else:
                    payload = {'question': question, 'presentations': presentations,
                        'activity': self.activity, 'source_limitations': content['source_limitations'],
                        'instructional_content': content.get('tutorials', []),
                        'shared_context': content.get('multistep'),
                        'final_review': True}
                    attempt = 0
                    while True:
                        check_stop(self.stop_event)
                        try:
                            judgment = self.solver.request('judge_question', payload, force_new=attempt > 0)
                            break
                        except SolverUnavailable as error:
                            attempt += 1
                            self._event('final_agent_retry', question=key, error=str(error), attempt=attempt)
                            self.sleep(backoff(attempt, self.config.retry_delay, self.config.recovery_max_delay))
                    judgment = {**judgment, 'question_id': question.get('math_academy_id'),
                                'capture_key': question_key(question), 'record_kind': name,
                                'evidence_hash': evidence_hash, 'final': True, 'judged_at': self.clock()}
                    self.state['judgments'][key] = judgment
                    self._save()
                content[name][index] = finalize_answers(question, presentations, judgment)
        content['lesson_workload_sample'] = self._lesson_sample(content)
        return content

    def _question_presentations(self, question):
        identity = question.get('math_academy_id')
        position = question.get('sequence_position')
        return [r for r in self.state['presentations'].values()
                if (identity and r['question'].get('math_academy_id') == identity) or
                (not r['question'].get('math_academy_id') and position is not None and r.get('observed_position', -1) + 1 == position)]

    def _merge_history(self, history):
        content = {'task_id': str(self.activity['task_id']), 'kind': self.activity['kind'],
                   'title': self.activity.get('title'), 'topic_id': self.activity.get('topic_id'),
                   'course_id': self.activity.get('course_id'), 'activity': self.activity,
                   'questions': [], 'canonical_examples': [], 'tutorials': [],
                   'observed_steps': deepcopy(self.state['steps'])}
        live = {'questions': [deepcopy(r['question']) for r in self.state['presentations'].values()],
                'canonical_examples': [s['question'] for s in self.state['steps'] if s.get('kind') == 'example' and s.get('question')],
                'tutorials': [s.get('tutorial', s) for s in self.state['steps'] if s.get('kind') == 'tutorial']}
        content = self._merge_content(content, live)
        # Diagnostic source IDs are revealed in history. Align source positions only
        # when the live question did not already provide a permanent identity.
        for question in history.get('questions', []):
            position = question.get('sequence_position')
            if position is not None:
                for record in self.state['presentations'].values():
                    if record['observed_position'] + 1 == position and not record['question'].get('math_academy_id'):
                        record['question']['math_academy_id'] = question.get('math_academy_id')
                        for old in content['questions']:
                            if not old.get('math_academy_id') and self._answer_binding(old) == self._answer_binding(record['question']):
                                old['math_academy_id'] = question.get('math_academy_id')
                    if record['observed_position'] + 1 == position and record['question'].get('math_academy_id') == question.get('math_academy_id'):
                        record['feedback'] = {**record.get('feedback', {}), **question}
        self._save()
        return self._merge_content(content, history)

    @staticmethod
    def _merge_content(before, after):
        result = deepcopy(before)
        for key, value in after.items():
            if key == 'examples':
                key = 'canonical_examples'
            if key in ('questions', 'canonical_examples'):
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
