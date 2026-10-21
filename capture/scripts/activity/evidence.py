"""Join live and history records without promoting a learner guess into MA content."""

from copy import deepcopy
import hashlib
import json
import re

from .policy import answer_fields
from ..database.evidence import evidence_value, UnsupportedContent, math_spacing_identity


def question_key(question):
    return str(question.get('math_academy_id') or question.get('source_id') or
               question.get('sequence_position') or hashlib.sha256(
                   str(question.get('problem', '')).encode()).hexdigest()[:16])


def _extraction_parts(record):
    """The adapter records which source sections a read actually inspected."""
    if 'extraction_parts' in record:
        return set(record['extraction_parts'])
    # Older captures have no section metadata. A solution fragment cannot vouch
    # for a prompt or fields retained from an earlier live capture.
    if str(record.get('dom_id', '')).startswith('questionExplanation-'):
        return {'solution'}
    parts = {'problem'} if 'problem' in record else set()
    if answer_fields(record):
        parts.add('fields')
    if (record.get('worked_solution') or record.get('solution_evidence') or
            re.search(r'(?:exampleExplanation|questionWidget-explanation|questionExplanation)', record.get('html', ''))):
        parts.add('solution')
    return parts


def _error_parts(error, record):
    """Only known capture failures can be replaced by a later source read."""
    error = str(error)
    if error.startswith('Screenshot unavailable:'):
        needed = {'screenshot'}
    elif error.startswith('History expansion:'):
        needed = {'solution'}
    elif error.startswith(('Unsupported math editor:', 'Select frame has no ID:',
                           'Unsupported input type:', 'Choice circle has no observed ID')):
        needed = {'fields'}
    elif error.startswith(('Unsupported MathML', 'Unsupported decorated MathML phantom', 'SVG formula has no local title or MathML',
                           'MathJax formula has no assistive MathML', 'Image unavailable:',
                           'Graphic rendering unavailable:', 'Visual asset is not rendered',
                           'Source rendering remained incomplete:', 'Lesson source rendering:')):
        needed = _extraction_parts(record)
    else:
        return set()  # Authored errors and unknown findings remain unchanged.
    return set(record.get('extraction_error_parts', {}).get(error, needed))


def _recaptured_error(error, before, after):
    """Clear a capture failure only when a clean read replaced its source scope."""
    if not isinstance(after.get('errors'), list) or not (after.get('html_path') or after.get('source_file')):
        return False
    identity = before.get('math_academy_id')
    if not identity or str(identity) != str(after.get('math_academy_id')):
        return False
    if str(before.get('source_id', '')).startswith('unreconciled:'):
        return False
    needed = _error_parts(error, before)
    covered = _extraction_parts(after) | ({'screenshot'} if after.get('screenshot') else set())
    if not needed or not needed <= covered:
        return False
    for current in after.get('errors', []):
        # Unscoped failures cannot prove any section was clean. New reads carry
        # exact error scopes, so a solution failure need not block prompt repair.
        current_parts = _error_parts(current, after)
        if not current_parts or needed & current_parts:
            return False
    if ('problem' in needed and not after.get('problem') or
            'solution' in needed and not after.get('worked_solution')):
        return False
    if 'fields' in needed:
        fields = answer_fields(after)
        keys = [field.get('key') for field in fields]
        old_keys = {field['key'] for field in answer_fields(before) if isinstance(field.get('key'), str) and field['key']}
        if (not fields or after.get('answer_fields_complete') is False or after.get('fields_complete') is False or
                any(not isinstance(key, str) or not key for key in keys) or len(set(keys)) != len(keys) or
                not old_keys <= set(keys) or
                set(re.findall(r'\{\{(field-\d+)\}\}', after.get('problem', ''))) - set(keys) or
                any(field.get('type') not in ('blank', 'radio', 'select') or
                    (field.get('type') in ('radio', 'select') and
                     (field.get('choices_complete') is False or len(field.get('choices', [])) < 2))
                    for field in fields)):
            return False
    return not any((asset.get('unavailable') or asset.get('render_unavailable')) and
                   (not asset.get('extraction_part') or asset['extraction_part'] in needed)
                   for asset in after.get('assets', []))


def _source_evidence(record):
    return {key: deepcopy(record[key]) for key in
            ('html_path', 'source_file', 'solution_evidence', 'captured_at', 'source_url')
            if record.get(key) is not None}


def _error_history(record):
    history = deepcopy(record.get('extraction_error_history', []))
    if not history and record.get('errors') and _source_evidence(record):
        history.append({'errors': deepcopy(record['errors']), 'source': _source_evidence(record),
                        'error_parts': deepcopy(record.get('extraction_error_parts', {})),
                        'assets': deepcopy(record.get('assets', []))})
    return history


def merge_question(before, after):
    result = deepcopy(before)
    for key, value in after.items():
        if value is not None and value != '' and value != [] and key not in (
                'fields', 'answer_fields', 'assets', 'errors', 'extraction_error_history', 'extraction_parts', 'extraction_error_parts'):
            result[key] = deepcopy(value)
    old = {str(f.get('key', i)): deepcopy(f) for i, f in enumerate(answer_fields(before))}
    for i, field in enumerate(answer_fields(after)):
        key = str(field.get('key', i))
        if key not in old:
            old[key] = deepcopy(field)
        else:
            old[key].update({name: deepcopy(value) for name, value in field.items() if value is not None and value != '' and value != []})
    if old:
        result['fields'] = list(old.values())
        result['answer_fields'] = deepcopy(result['fields'])
    if isinstance(after.get('assets'), list):
        if 'extraction_parts' in after and (after.get('html_path') or after.get('source_file')):
            covered = _extraction_parts(after)
            # Section metadata makes an observed empty asset list meaningful.
            # Legacy unscoped graphics remain until their scope can be verified.
            kept = [asset for asset in before.get('assets', []) if asset.get('extraction_part') not in covered]
            result['assets'] = []
            for asset in kept + after['assets']:
                if asset not in result['assets']:
                    result['assets'].append(deepcopy(asset))
        elif after['assets']:
            result['assets'] = deepcopy(after['assets'])
    # Empty errors means a successful observed read, not an absent update.
    resolved = [error for error in (before.get('errors') or []) if _recaptured_error(error, before, after)]
    retained = [error for error in (before.get('errors') or []) if error not in resolved]
    if 'errors' in before or 'errors' in after:
        result['errors'] = list(dict.fromkeys(retained + (after.get('errors') or [])))
    error_parts = {}
    for source, errors in ((before, retained), (after, after.get('errors') or [])):
        for error in errors:
            parts = _error_parts(error, source)
            if parts:
                error_parts[error] = sorted(set(error_parts.get(error, [])) | parts)
    if error_parts or 'extraction_error_parts' in before or 'extraction_error_parts' in after:
        result['extraction_error_parts'] = error_parts
    history = _error_history(before)
    for record in _error_history(after):
        if record not in history:
            history.append(record)
    if resolved:
        record = {'errors': resolved, 'source': _source_evidence(before), 'replaced_by': _source_evidence(after),
                  'error_parts': {error: sorted(_error_parts(error, before)) for error in resolved},
                  'recaptured_parts': sorted(_extraction_parts(after))}
        if record not in history:
            history.append(record)
    if history:
        result['extraction_error_history'] = history
    if 'extraction_parts' in before or 'extraction_parts' in after:
        result['extraction_parts'] = sorted(_extraction_parts(before) | _extraction_parts(after))
    return result


def correct_grade(value):
    return value is True or str(value).strip().lower() in ('correct', 'full credit', '100%', 'passed')


def source_file(question):
    evidence = question.get('evidence') or {}
    return question.get('solution_evidence') or question.get('source_file') or question.get('html_path') or (evidence.get('html') if isinstance(evidence, dict) else None)


def _current_answer_evidence(field, question):
    """Separate preserved source facts from a usable current field answer."""
    evidence = field.get('evidence') or {}
    if not isinstance(evidence, dict) or evidence.get('kind') not in (
            'ma_answer', 'ma_correct_grade', 'worked_solution', 'radio_image_filename'):
        return False, False
    checked = deepcopy(field)
    try:
        value = evidence_value(checked, question)
    except UnsupportedContent:
        return False, False
    if not isinstance(value, str):
        return False, False
    if value != field.get('correct_value'):
        if not (checked.get('evidence', {}).get('source_choice_quote') or
                checked.get('evidence', {}).get('source_choice_spacing')):
            return False, False
        # Reuse the validator's narrow exact-source-choice repair; never add
        # a mathematical equivalence or TeX normalization rule here.
        field['correct_value'] = value
        field['evidence'] = checked['evidence']
    # Explicit source keys and correctly bound grades remain source facts even
    # if MA authored an answer absent from its options. A quoted interpretation
    # that does not select a current typed choice must allow focused review.
    if evidence['kind'] != 'worked_solution' or not field.get('choices'):
        return True, True
    value_type = field.get('correct_type') or field.get('value_type')
    matches = {(choice.get('type'), choice.get('value')) for choice in field['choices']
               if choice.get('value') == value and
               (not value_type or choice.get('type') == value_type)}
    return True, len(matches) == 1


def finalize_answers(question, presentations, judgment):
    """Authoritative field values need observed grading, direct MA, or quoted solution evidence."""
    result = deepcopy(question)
    judged = {str(a['key']): a for a in judgment.get('answers', [])}
    fields = deepcopy(answer_fields(question))
    for index, field in enumerate(fields):
        key = str(field.get('key', index))
        evidence = field.get('evidence') or field.get('correct_evidence') or {}
        if evidence:
            field['evidence'] = deepcopy(evidence)
        # Recheck a saved quotation against this solution and typed choice set.
        # Its kind alone must not suppress a fresh focused source judgment.
        source_fact, supported = _current_answer_evidence(field, question)
        if not source_fact:
            field.pop('correct_value', None)
            field.pop('correct_option', None)
        for presentation in presentations:
            feedback = presentation.get('feedback') or {}
            grade = feedback.get('grade', presentation.get('grade'))
            submissions = presentation.get('submissions', [])
            if not submissions:
                continue
            selected = field.get('source_selected') or field.get('source_correct') or {}
            verified = [submission for submission in submissions
                if submission.get('outcome') not in ('entry_failed', 'not_submitted')
                and (submission.get('outcome') == 'observe_to_confirm'
                     or any(str(response.get('key')) == key and response.get('value') is not None
                            and str(response['value']) == str(selected.get('value'))
                            for response in submission.get('responses', [])))]
            if not verified:
                continue
            submission = verified[-1]
            # Successful overall grading confirms every submitted field. Accepted only
            # means the UI received it; that does not establish correctness.
            field_grades = feedback.get('field_grades', {})
            if not (correct_grade(grade) or correct_grade(field_grades.get(key))):
                continue
            response = next((a for a in submission.get('responses', []) if str(a.get('key')) == key), None)
            if response and response.get('value') is not None:
                field['correct_value'] = response['value']
                if response.get('value_type'):
                    field['value_type'] = response['value_type']
                field['evidence'] = {'kind': 'ma_correct_grade', 'value': response['value'],
                                     'source_file': feedback.get('source_file') or feedback.get('html_path') or source_file(question),
                                     'presentation_key': presentation.get('key'), 'grade': 'correct', 'observed_grade': grade}
                supported = True
        answer = judged.get(key, {})
        if answer.get('ma_basis') == 'worked_solution' and answer.get('ma_value') is not None:
            raw_quote = answer.get('ma_evidence', '')
            quote = raw_quote.strip() if isinstance(raw_quote, str) else ''
            solution = str(question.get('worked_solution') or '')
            if quote and quote in solution:
                value = answer['ma_value']
                choices = field.get('choices', [])
                value_type = answer.get('value_type', field.get('value_type', 'math'))
                spacing_binding = None
                if value_type == 'math' and answer.get('disagrees') is False and answer.get('correct_option') is not None:
                    spaced = [c for c in choices if c.get('type') == 'math'
                              and math_spacing_identity(c['value']) == math_spacing_identity(value)]
                    if (len(spaced) == 1 and spaced[0]['value'] == answer.get('correct_value')
                            and str(spaced[0].get('option')) == str(answer['correct_option'])
                            and spaced[0]['value'] != value):
                        spacing_binding = {'solution_value': value, 'source_choice_spacing': True,
                                           'source_choice_option': spaced[0]['option']}
                        value = spaced[0]['value']
                typed_choices = {(c.get('type'), c.get('value')) for c in choices
                                 if c.get('value') == value and c.get('type') == value_type}
                # A quotation can be literally present yet describe a premise,
                # not the answer. A fresh checked interpretation of the current
                # typed choice may supersede an older solution interpretation.
                # Direct keys, bound correct grades, and filename facts retain
                # precedence over the agent's interpretation of prose.
                current_evidence = field.get('evidence')
                reviewed_source_error = judgment.get('status') == 'source_error' and answer.get('disagrees') is True
                reviewed_solution = (isinstance(current_evidence, dict) and current_evidence.get('kind') == 'worked_solution'
                                     and value_type in ('math', 'text', 'image')
                                     and (len(typed_choices) == 1 or reviewed_source_error
                                          or (not choices and field.get('type') == 'blank')))
                if supported and not reviewed_solution:
                    continue
                # Preserve an explicit MA error even when no available choice matches;
                # preparation validates how that answer can be stored by the schema.
                if (source_fact and judgment.get('status') == 'source_error'
                        and field.get('correct_value') is not None and field['correct_value'] != value):
                    conflict = {'previous_value':field['correct_value'],
                        'previous_evidence':deepcopy(field.get('evidence')),
                        'reviewed_value':value, 'reasoning':judgment.get('reasoning')}
                    history = field.setdefault('source_answer_conflicts',[])
                    if conflict not in history:
                        history.append(conflict)
                field['correct_value'] = value
                field.pop('correct_option', None)
                field['value_type'] = value_type
                if len(typed_choices) == 1:
                    field['correct_type'] = field['value_type']
                field['evidence'] = {'kind': 'worked_solution', 'value': value,
                                     'source_file': source_file(question), 'solution_quote': quote,
                                     'matches_worked_solution': True,
                                     'choice_present': not choices or len(typed_choices) == 1}
                if spacing_binding:
                    field['evidence'].update(spacing_binding)
                supported = True
                field.pop('source_answer_status', None)
        if not supported:
            field['source_answer_status'] = 'unavailable'
    result['answer_fields'] = fields
    result.pop('fields', None)
    return result


def capture_gaps(content):
    """Identify incomplete source capture without invalidating a final agent finding.

    These are recovery inputs and preserved limitations, never a reason to defer
    the activity. Optional history metadata (difficulty, XP, and topic labels) is
    deliberately not required.
    """
    gaps = []
    judgments = content.get('judgments', [])
    if isinstance(judgments, dict):
        judgments = list(judgments.values())

    def append(record, name, missing, **details):
        if not missing:
            return
        gap = {'question': question_key(record), 'record_kind': name,
               'missing': list(dict.fromkeys(missing)), **details}
        judgment = next((j for j in judgments if j.get('final') and
            j.get('status') in ('unavailable', 'source_error') and
            j.get('record_kind', name) == name and
            ((j.get('question_id') is not None and str(j['question_id']) == str(record.get('math_academy_id')))
             or j.get('capture_key') == question_key(record))), None)
        if judgment:
            gap.update(final=True, judgment_status=judgment['status'], reason=judgment.get('reasoning'))
        gaps.append(gap)

    def source_gaps(record):
        missing = []
        if record.get('errors'):
            missing.append('extraction_errors')
        if any(a.get('unavailable') or not a.get('path') or not a.get('sha256') for a in record.get('assets', [])):
            missing.append('assets')
        if any(a.get('render_unavailable') for a in record.get('assets', [])):
            missing.append('asset_rendering')
        values = [record.get(key, '') for key in ('problem', 'worked_solution', 'content')]
        values.extend(choice.get('value', '') for field in answer_fields(record) for choice in field.get('choices', []))
        if any(re.search(r'@asset-\d+@', str(value)) for value in values):
            missing.append('asset_references')
        return missing

    for name in ('questions', 'reference_questions', 'canonical_examples'):
        seen = {}
        for question in content.get(name, []):
            missing = source_gaps(question)
            if not str(question.get('problem') or '').strip():
                missing.append('problem')
            fields = answer_fields(question)
            # Canonical worked examples need not contain interactive fields.
            if name != 'canonical_examples' and not fields:
                missing.append('answer_fields')
            if question.get('answer_fields_complete') is False:
                missing.append('answer_fields_complete')
            keys = [str(field.get('key', '')) for field in fields]
            # Only the browser's known field-N control tokens are placeholders.
            # Literal nested sets and TeX groups may also have doubled braces.
            # Match the same source-control grammar as authoritative_question.
            placeholders = set(re.findall(r'\{\{(field-\d+)\}\}', str(question.get('problem', ''))))
            if set(question.get('problem_field_keys', [])) - placeholders:
                missing.append('answer_field_positions')
            if (any(not key for key in keys) or len(keys) != len(set(keys)) or
                    placeholders - set(keys) or any(not f.get('type') for f in fields)):
                missing.append('answer_field_structure')
            if any(f.get('type') in ('select', 'radio', 'checkbox', 'multi-select') and
                   (not f.get('choices') or f.get('choices_complete') is False) for f in fields):
                missing.append('answer_choices')
            # Reference catalog questions can supply an explicit source answer
            # without a revealed explanation. Encountered task questions still
            # require their full history solution; canonical examples do too.
            if name != 'reference_questions' and not str(question.get('worked_solution') or '').strip():
                missing.append('worked_solution')
            identity = question.get('math_academy_id')
            if not identity:
                missing.append('source_question_id')
            elif str(identity) in seen:
                # Repeated presentations belong to one source record. Surface an
                # unresolved merge, especially if the source problem changed.
                missing.append('duplicate_source_record')
                before = re.sub(r'\s+', ' ', str(seen[str(identity)].get('problem', ''))).strip()
                after = re.sub(r'\s+', ' ', str(question.get('problem', ''))).strip()
                if before != after:
                    missing.append('source_identity_conflict')
            if identity:
                seen[str(identity)] = question
            append(question, name, missing, **({'errors': question['errors']} if question.get('errors') else {}))

    kind = content.get('kind') or content.get('task_type')
    for tutorial in content.get('tutorials', []):
        missing = source_gaps(tutorial)
        if not str(tutorial.get('content') or tutorial.get('problem') or '').strip():
            missing.append('content')
        # Legacy multistep captures store their unnamed shared setup here.
        # It is source context, not a titled lesson tutorial entity.
        setup = kind == 'multistep' and not (tutorial.get('source_step') or {}).get('type')
        if not setup and not tutorial.get('title'):
            missing.append('title')
        if not setup and not tutorial.get('math_academy_id'):
            missing.append('source_tutorial_id')
        append(tutorial, 'tutorials', missing, **({'errors': tutorial['errors']} if tutorial.get('errors') else {}))

    if kind == 'lesson':
        definition = content.get('lesson_definition') or {}
        if not definition:
            gaps.append({'missing': ['lesson_definition']})
        else:
            if not definition.get('complete') or not definition.get('steps') or definition.get('issues'):
                gaps.append({'missing': ['lesson_definition_complete'], 'issues': definition.get('issues', [])})
            identities = {'tutorial': {str(q.get('math_academy_id')) for q in content.get('tutorials', [])},
                          'example': {str(q.get('math_academy_id')) for q in content.get('canonical_examples', [])}}
            for step in definition.get('steps', []):
                step_type = step.get('type')
                identity = str(step.get('content_id'))
                if step_type == 'example':
                    identity = 'e-' + identity.removeprefix('e-')
                if step_type in identities and identity not in identities[step_type]:
                    gaps.append({'record_kind': step_type, 'source_id': identity,
                                 'missing': ['lesson_step_content'], 'placement': step.get('math_academy_id')})
    if kind == 'multistep' and not content.get('multistep'):
        gaps.append({'missing': ['multistep']})
    return gaps
