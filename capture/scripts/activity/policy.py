"""Durable answer intentions. Source grades and mathematical answers stay separate."""

from collections import deque
import random
import time


def topic_id(value):
    if isinstance(value, dict):
        value = value.get('topic_id', value.get('math_academy_id', value.get('id')))
    return str(value) if value is not None else None


def prerequisite_distances(course_topics, graph):
    """topic/next is prerequisite -> dependent; walk incoming edges from the course."""
    reverse = {}
    for source, dependents in graph.items():
        for dependent in dependents:
            reverse.setdefault(topic_id(dependent), set()).add(str(source))
    distances = {topic_id(value): 0 for value in course_topics if topic_id(value) is not None}
    queue = deque(distances)
    while queue:
        current = queue.popleft()
        for prerequisite in reverse.get(current, ()):
            if prerequisite not in distances:
                distances[prerequisite] = distances[current] + 1
                queue.append(prerequisite)
    return distances


class AnswerPolicy:
    """Mutates the caller's checkpoint; callers persist it before any response."""

    def __init__(self, activity, state, context=None, rng=None, clock=time.time):
        self.activity = activity
        self.state = state
        self.context = context or {}
        self.rng = rng or random.Random()
        self.clock = clock
        self.state.setdefault('patterns', {})
        self.state.setdefault('counts', {})
        self.state.setdefault('decisions', {})
        self.state.setdefault('distances', prerequisite_distances(
            self.context.get('course_topics', []), self.context.get('graph', {})))

    def decide(self, key, question, started_at=None):
        if key in self.state['decisions']:
            return self.state['decisions'][key]
        kind = self.activity['kind']
        decision = {'planned': 'C', 'action': 'answer', 'delay_seconds': 0,
                    'started_at': self.clock() if started_at is None else started_at,
                    'topic_id': topic_id(question.get('topic_id')), 'policy_version': 1}
        if kind == 'diagnostic':
            distance = self.state['distances'].get(decision['topic_id'])
            decision['distance'] = distance
            if distance is None:
                decision.update(planned='D', action='dont_know', reason='Topic is unknown or has no path to the course')
            elif distance == 0:
                decision['draw'] = self.rng.random()
                if decision['draw'] < .5:
                    decision['delay_seconds'] = self.rng.uniform(270, 360)
                else:
                    decision.update(planned='D', action='dont_know')
            else:
                bounds = (90, 120) if distance == 1 else (60, 90) if distance == 2 else (30, 60)
                decision['delay_seconds'] = self.rng.uniform(*bounds)
        elif kind == 'assessment':
            decision['draw'] = self.rng.random()
            decision['planned'] = 'C' if decision['draw'] < .8717 else 'W'
        elif kind in ('lesson', 'review') and not self.activity.get('details', {}).get('force_correct'):
            group = str(question.get('kp_id') or question.get('knowledge_point_id') or 'unknown') if kind == 'lesson' else 'review'
            if group not in self.state['patterns']:
                draw = self.rng.random()
                self.state['patterns'][group] = {'pattern': 'CWCWC' if draw < .7 else 'WCWCC', 'draw': draw}
            index = self.state['counts'].get(group, 0)
            pattern = self.state['patterns'][group]['pattern']
            decision.update(pattern=pattern, pattern_group=group, sequence_position=index)
            decision['planned'] = 'C' if kind == 'lesson' and index >= 5 else pattern[index % len(pattern)]
            self.state['counts'][group] = index + 1
        decision['intended'] = decision['planned']
        decision['submit_at'] = decision['started_at'] + decision['delay_seconds']
        self.state['decisions'][key] = decision
        return decision


def override(decision, intended, reason):
    """Keep the original draw and sequence position when completion needs a deviation."""
    decision['intended'] = intended
    decision['deviation_reason'] = reason
    decision['action'] = 'dont_know' if intended == 'D' else 'answer'


def answer_fields(question):
    return question.get('fields') or question.get('answer_fields') or []


def choice_token(choice):
    return choice.get('option', choice.get('key', choice.get('id', choice.get('dom_id'))))


def responses_for(question, solution, decision, *, source_preferred=False):
    """Rebind values to CURRENT choices; never reuse shuffled answer letters."""
    answers = {str(answer['key']): answer for answer in solution.get('answers', [])}
    responses = []
    changed = False
    for index, field in enumerate(answer_fields(question)):
        if field.get('disabled') or str(field.get('source_result', '')).lower() == 'correct':
            continue
        key = str(field.get('key', index))
        answer = answers.get(key, {})
        value = answer.get('ma_value') if source_preferred and answer.get('ma_value') is not None else answer.get('correct_value')
        if value is None:
            value = field.get('correct_value')
        choices = field.get('choices', [])
        option = None
        keys = answer.get('correct_keys', [])
        value_type = answer.get('value_type') or field.get('value_type') or ('math' if field.get('tag') == 'mathquill' else 'text')
        if choices:
            selected = next((c for c in choices if str(c.get('value')) == str(value)), None)
            # An agent may identify a choice by token, but only on this exact question.
            if selected is None and value is None:
                selected = next((c for c in choices if choice_token(c) == answer.get('correct_option')), None)
            if selected is None:
                selected = choices[0]
                override(decision, 'C', 'No confirmed answer matches the current choices; submit a valid best attempt')
            if decision['intended'] == 'W' and not changed:
                alternatives = [c for c in choices if str(c.get('value')) != str(selected.get('value'))]
                if alternatives:
                    selected, changed = alternatives[0], True
            value, option = selected.get('value'), choice_token(selected)
            value_type = selected.get('type', value_type)
            keys = []
        else:
            if value is None:
                value = '0' if field.get('type') in ('math', 'number', 'blank') else 'unknown'
                override(decision, 'C', 'No supported answer available; submit a valid best attempt and resolve in history')
            if decision['intended'] == 'W' and not changed:
                wrong = answer.get('wrong_value')
                if wrong is not None and str(wrong) != str(value):
                    value, keys, changed = wrong, answer.get('wrong_keys', []), True
        responses.append({'key': key, 'value': value, 'option': option, 'keys': keys, 'value_type': value_type})
    if decision['intended'] == 'W' and not changed:
        override(decision, 'C', 'No demonstrably different valid response is available')
    return responses
