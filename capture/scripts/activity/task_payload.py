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
            if (asset.get('tag') == 'svg' or asset.get('content_type') == 'image/svg+xml') and not (record.get('screenshot') or record.get('screenshot_path')):
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
    # The adapter screenshot is scoped to this question. Attach it only when
    # normalized text lacks the field layout or extraction reported missing math.
    needs_layout = len(fields) > 1 and any('{{' + str(field['key']) + '}}' not in str(result.get('problem', '')) for field in fields)
    needs_graphic_fallback = any(asset.get('unavailable') or asset.get('content_type') == 'image/svg+xml'
        or str(asset.get('path', '')).lower().endswith('.svg') for asset in assets)
    if result.get('problem') and not result.get('errors') and not needs_layout and not needs_graphic_fallback:
        result.pop('screenshot', None)
        result.pop('screenshot_path', None)
    return result


def feedback_evidence(record):
    return _pick(record or {}, ('grade', 'source_grade', 'result', 'field_grades',
        'proof_feedback', 'worked_solution', 'solution_evidence', 'html_path', 'source_file'))


def compact_submissions(submissions):
    """Repeated identical UI attempts add counts, not repeated mathematical evidence."""
    groups = []
    for submission in submissions:
        item = _pick(submission, ('action', 'outcome', 'grade', 'field_grades', 'browser_error'))
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
        observation = payload.get('observation') or {}
        question = {**payload.get('question', payload)}
        if observation.get('screenshot'):
            question.setdefault('screenshot', observation['screenshot'])
        result = {'evidence_contract': task + ':1', 'question': compact_question(question)}
        if task == 'solve_question' and payload.get('current_example'):
            result['current_example'] = compact_question(payload['current_example'])
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
            if payload.get('earlier_parts'):
                # Earlier multistep answers can be implicit dependencies. Their
                # compact summaries preserve that context without source replay.
                result['earlier_parts'] = [part_summary(record) for record in payload['earlier_parts']]
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
        question = {**payload.get('question', {})}
        if payload.get('screenshot'):
            question.setdefault('screenshot', payload['screenshot'])
        # Python computes course/prerequisite distances. Classification needs
        # the authored candidate topics; no duplicate graph/course catalog.
        return {'evidence_contract': task + ':1', 'question': compact_question(question), 'topics': topics}
    if task == 'interpret_page':
        observation = payload.get('observation') or {}
        result = {'evidence_contract': task + ':1', 'observation': _pick(observation, ('kind', 'key', 'buttons', 'grade', 'accepted',
            'reload_required', 'ready', 'action', 'screenshot', 'html_path', 'visible_text', 'text',
            'can_dont_know', 'can_skip'))}
        question = payload.get('question') or observation.get('question')
        if question:
            result['question'] = compact_question(question)
        if payload.get('browser_error'):
            result['browser_error'] = _pick(payload['browser_error'], ('method', 'error'))
        return result
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
        if isinstance(value, str):
            if value.startswith('/') and Path(value).suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'):
                return normalize(value, 'path')
            def image_reference(match):
                return match[1] + json.dumps(normalize(match[2], 'path'), sort_keys=True) + match[3]
            return re.sub(r'(!\[[^\]]*\]\()([^\)\s]+)(\))', image_reference, value)
        return value
    return hashlib.sha256(json.dumps({'contract_version': 1, 'task': task,
        'payload': normalize(payload)}, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()
