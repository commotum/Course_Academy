"""Join live and history records without promoting a learner guess into MA content."""

from copy import deepcopy
import hashlib
import json

from .policy import answer_fields


def question_key(question):
    return str(question.get('math_academy_id') or question.get('source_id') or
               question.get('sequence_position') or hashlib.sha256(
                   str(question.get('problem', '')).encode()).hexdigest()[:16])


def merge_question(before, after):
    result = deepcopy(before)
    for key, value in after.items():
        if value is not None and value != '' and value != [] and key not in ('fields', 'answer_fields'):
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
    return result


def correct_grade(value):
    return value is True or str(value).strip().lower() in ('correct', 'full credit', '100%', 'passed')


def source_file(question):
    evidence = question.get('evidence') or {}
    return question.get('solution_evidence') or question.get('source_file') or question.get('html_path') or (evidence.get('html') if isinstance(evidence, dict) else None)


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
        # A parser-supplied value is retained only with source evidence attached.
        supported = isinstance(evidence, dict) and evidence.get('kind') in (
            'ma_answer', 'ma_correct_grade', 'worked_solution', 'radio_image_filename')
        if not supported:
            field.pop('correct_value', None)
            field.pop('correct_option', None)
        for presentation in presentations:
            feedback = presentation.get('feedback') or {}
            grade = feedback.get('grade', presentation.get('grade'))
            submissions = presentation.get('submissions', [])
            if not submissions:
                continue
            submission = submissions[-1]
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
        if not supported and answer.get('ma_basis') == 'worked_solution' and answer.get('ma_value') is not None:
            quote = answer.get('ma_evidence', '').strip()
            solution = str(question.get('worked_solution') or '')
            if quote and quote in solution:
                value = answer['ma_value']
                choices = field.get('choices', [])
                # Preserve an explicit MA error even when no available choice matches;
                # preparation validates how that answer can be stored by the schema.
                field['correct_value'] = value
                field['value_type'] = answer.get('value_type', field.get('value_type', 'math'))
                field['evidence'] = {'kind': 'worked_solution', 'value': value,
                                     'source_file': source_file(question), 'solution_quote': quote,
                                     'matches_worked_solution': True,
                                     'choice_present': not choices or any(str(c.get('value')) == str(value) for c in choices)}
                supported = True
        if not supported:
            field['source_answer_status'] = 'unavailable'
    result['answer_fields'] = fields
    result.pop('fields', None)
    return result


def capture_gaps(content):
    """Optional history metadata is retained as absent; required missing content is explicit."""
    gaps = []
    for question in content.get('questions', []):
        missing = []
        if not question.get('problem'):
            missing.append('problem')
        if not answer_fields(question):
            missing.append('answer_fields')
        if not question.get('worked_solution'):
            missing.append('worked_solution')
        if not question.get('math_academy_id'):
            missing.append('source_question_id')
        if missing:
            gaps.append({'question': question_key(question), 'missing': missing})
    if content.get('kind') == 'lesson' and not content.get('lesson_definition'):
        gaps.append({'missing': ['lesson_definition']})
    if content.get('kind') == 'multistep' and not content.get('multistep'):
        gaps.append({'missing': ['multistep']})
    return gaps
