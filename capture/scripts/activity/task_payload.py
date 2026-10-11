"""Task-specific agent evidence; complete browser/source records stay on disk."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

from .policy import answer_fields


def _pick(record, keys):
    return {key: deepcopy(record[key]) for key in keys if record.get(key) is not None and record[key] != '' and record[key] != []}


def _assets(record):
    assets = []
    for asset in record.get('assets', []) + record.get('images', []):
        if isinstance(asset, str):
            assets.append({'path': asset})
        elif isinstance(asset, dict):
            item = _pick(asset, ('index', 'path', 'local_path', 'image_path', 'sha256', 'source_url', 'content_type', 'representation', 'alt', 'unavailable'))
            # SVGs cannot be attached to Codex as raster images; their source is
            # the actual diagram, not redundant browser markup.
            if asset.get('tag') == 'svg' or asset.get('content_type') == 'image/svg+xml':
                item.update(_pick(asset, ('html',)))
            assets.append(item)
    return assets


def compact_question(question):
    """Keep all normalized math and field/source evidence exactly once."""
    result = _pick(question, ('math_academy_id', 'source_id', 'sequence_position', 'problem',
        'worked_solution', 'calculator_instructions', 'requires_calculator', 'answer_fields_complete',
        'proof_feedback', 'result', 'grade', 'source_grade', 'field_grades', 'errors',
        'html_path', 'source_file', 'source_url', 'solution_evidence', 'screenshot', 'screenshot_path'))
    fields = []
    for index, field in enumerate(answer_fields(question)):
        value = _pick(field, ('key', 'type', 'presentation', 'prompt', 'label', 'context', 'disabled',
            'choices_complete', 'source_selected', 'source_correct', 'source_result',
            'correct_value', 'correct_option', 'value_type', 'correct_origin', 'evidence', 'correct_evidence'))
        value.setdefault('key', str(index))
        if field.get('choices'):
            value['choices'] = [_pick(choice, ('option', 'type', 'value', 'source_url', 'source_urls',
                'feedback', 'image_path', 'local_path', 'path', 'alt')) for choice in field['choices']]
        fields.append(value)
    if fields:
        result['fields'] = fields
    assets = _assets(question)
    if assets:
        result['assets'] = assets
    return result


def feedback_evidence(record):
    return _pick(record or {}, ('grade', 'source_grade', 'result', 'field_grades',
        'proof_feedback', 'worked_solution', 'solution_evidence', 'html_path', 'source_file'))


def compact_submissions(submissions):
    """Repeated identical UI attempts add counts, not repeated mathematical evidence."""
    groups = []
    for submission in submissions:
        item = _pick(submission, ('action', 'outcome', 'grade', 'field_grades'))
        item['responses'] = [_pick(response, ('key', 'value', 'option', 'value_type'))
                             for response in submission.get('responses', [])]
        signature = json.dumps(item, sort_keys=True, default=str)
        previous = next((group for group in groups if group['_signature'] == signature), None)
        if previous:
            previous['attempt_count'] += 1
        else:
            groups.append({**item, 'attempt_count': 1, '_signature': signature})
    for item in groups:
        item.pop('_signature')
    return groups


def compact_presentation(record):
    return {'key': record.get('key'), 'submissions': compact_submissions(record.get('submissions', [])),
            'feedback': feedback_evidence({**(record.get('feedback') or {}), **_pick(record, ('grade',))})}


def shared_evidence(context):
    if isinstance(context, list):
        return [shared_evidence(item) for item in context]
    if not isinstance(context, dict):
        return context
    if 'shared_contexts' in context:
        return shared_evidence(context['shared_contexts'])
    result = compact_question(context)
    result.update(_pick(context, ('id', 'context', 'content', 'title')))
    return result


def part_summary(record):
    question = record.get('question', {})
    solution = record.get('solution') or {}
    return {'question_id': question.get('math_academy_id'), 'problem': question.get('problem'),
            'status': solution.get('status'), 'answers': [_pick(answer, ('key', 'correct_value',
                'ma_value', 'ma_basis', 'ma_evidence')) for answer in solution.get('answers', [])],
            'feedback': feedback_evidence(record.get('feedback') or {})}


def task_payload(task, payload):
    """An explicit contract per task, without size caps or math truncation."""
    if payload.get('evidence_contract') == task + ':1':
        return deepcopy(payload)
    if task in ('solve_question', 'judge_question'):
        result = {'evidence_contract': task + ':1', 'question': compact_question(payload.get('question', payload))}
        observation = payload.get('observation') or {}
        # A history merge may expose field evidence but omit the live graphics.
        if observation.get('screenshot') and not result['question'].get('screenshot'):
            result['question']['screenshot'] = observation['screenshot']
        feedback = feedback_evidence(observation)
        if feedback:
            # Don't repeat the question's already retained source facts.
            feedback = {key: value for key, value in feedback.items() if result['question'].get(key) != value}
            if feedback:
                result['current_feedback'] = feedback
        if payload.get('previous_submissions'):
            result['previous_submissions'] = compact_submissions(payload['previous_submissions'])
        if payload.get('presentations'):
            result['presentations'] = [compact_presentation(record) for record in payload['presentations']]
        activity_kind = (payload.get('activity') or {}).get('kind')
        if activity_kind == 'multistep' or payload.get('shared_context'):
            context = shared_evidence(payload.get('shared_context'))
            if context:
                result['shared_context'] = context
            problem = str(result['question'].get('problem') or '')
            dependencies = payload.get('depends_on') or payload.get('question', {}).get('depends_on')
            # Independent parts can be solved from their shared setup. Explicit
            # references to preceding results need answer summaries, not captures.
            references_prior = bool(dependencies) or bool(re.search(
                r'previous|earlier|preceding|above|part\s+[a-z0-9(]|your\s+(?:answer|result)|(?:result|answer).*?(?:found|obtained|calculated)|hence|therefore', problem, re.I))
            if payload.get('earlier_parts') and references_prior:
                parts = payload['earlier_parts']
                if dependencies:
                    allowed = {str(value) for value in (dependencies if isinstance(dependencies, list) else [dependencies])}
                    parts = [record for record in parts if str(record.get('question', {}).get('math_academy_id')) in allowed]
                result['earlier_parts'] = [part_summary(record) for record in parts]
        identity = str(result['question'].get('math_academy_id') or result['question'].get('sequence_position') or '')
        limits = [item for item in payload.get('source_limitations', [])
                  if not isinstance(item, dict) or 'question' not in item or str(item['question']) == identity]
        if limits:
            result['source_limitations'] = deepcopy(limits)
        result.update(_pick(payload, ('gap', 'recovery')))
        return result
    if task == 'match_topic':
        topics = [_pick(topic, ('topic_id', 'id', 'math_academy_id', 'title', 'description', 'learning_outcomes'))
                  if isinstance(topic, dict) else topic for topic in payload.get('topics', [])]
        return {'evidence_contract': task + ':1', 'question': compact_question(payload.get('question', {})), 'topics': topics,
                **_pick(payload, ('course_topics', 'graph', 'screenshot'))}
    if task == 'interpret_page':
        observation = payload.get('observation') or {}
        return {'evidence_contract': task + ':1', 'observation': _pick(observation, ('kind', 'key', 'buttons', 'grade', 'accepted',
            'reload_required', 'ready', 'action', 'screenshot', 'html_path', 'visible_text', 'text',
            'can_dont_know', 'can_skip')), **_pick(payload, ('previous_recovery_count',))}
    return deepcopy(payload)


def semantic_identity(task, payload):
    """Ignore provenance location/time, but bind the cache to actual graphic bytes."""
    paths = ('html_path', 'source_file', 'solution_evidence', 'source_url', 'screenshot',
             'screenshot_path', 'local_path', 'image_path', 'path')
    def normalize(value, key=None):
        if isinstance(value, dict):
            return {name: normalize(child, name) for name, child in value.items()
                    if name not in ('captured_at', 'observed_at', 'started_at', 'returned_at', 'judged_at')
                    and (name not in paths or isinstance(child, str) and Path(child).suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'))}
        if isinstance(value, list):
            return [normalize(child) for child in value]
        if key in paths and isinstance(value, str):
            path = Path(value)
            if path.is_file():
                return {'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
            # An absent attachment is a different evidence state; preserve its
            # basename without tying otherwise equal questions to output roots.
            return {'unavailable_image': path.name}
        return value
    return hashlib.sha256(json.dumps({'contract_version': 1, 'task': task,
        'payload': normalize(payload)}, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()
