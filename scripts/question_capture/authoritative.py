"""Prepare Math Academy originals from saved observations, never solver answers.

The capture/solver checkpoints remain untouched. This module returns a separate
content payload and review notes; callers must hold an activity if held_questions
is nonempty. No database access, model calls, or mathematical answer inference.
"""
from copy import deepcopy
import json
from pathlib import Path
import re
import sys

VERSION = 'math-academy-originals-v1'


class AuthoritativeReview(ValueError):
    """One or more complete source answer fields still require review."""


def _read(path):
    return json.loads(path.read_text()) if path.is_file() else {}


def _answer(value):
    if (isinstance(value, dict) and value.get('type') in ('math', 'text', 'image')
            and isinstance(value.get('value'), str) and value['value'].strip()):
        return {'type': value['type'], 'value': value['value']}
    return None


def _same(a, b):
    from core import normalize
    return a['type'] == b['type'] and (a['value'] == b['value'] or
        normalize(a['value'], a['type']) == normalize(b['value'], b['type']))


def _raw_fields(item):
    return {field['key']: field for field in item.get('fields', []) if field.get('key')}


def _same_layout(source, target):
    """A grade is usable only for this observed field, not just its ordinal."""
    if source.get('key') != target.get('key') or source.get('type') != target.get('type'):
        return False
    if source.get('dom_id') and target.get('dom_id') and source['dom_id'] != target['dom_id']:
        return False
    if target.get('type') in ('radio', 'select'):
        incoming = [_answer(c) for c in source.get('choices', [])]
        original = [_answer(c) for c in target.get('choices', [])]
        if incoming and original:
            return len(incoming) == len(original) and all(
                a and any(b and _same(a, b) for b in original) for a in incoming)
    return True


def _displayed_history(raw_html, fields, topic, assets):
    """Read only MA's displayed correct fields in the completed-activity DOM.

    Do not read studentAnswer blocks. Require the full ordered field layout to
    match the before capture; a partial layout must not shift field-N bindings.
    """
    if not raw_html or not any(x in raw_html for x in ('freeResponseTextbox', 'selectList')):
        return {}, None
    try:
        from bs4 import BeautifulSoup, Comment
        scripts_path = str(Path(__file__).resolve().parents[1])
        if scripts_path not in sys.path:
            sys.path.insert(0, scripts_path)
        from import_historical_question_content import Renderer
    except ImportError:
        return {}, 'history_field_parser_unavailable'
    soup = BeautifulSoup(raw_html, 'html.parser')
    for node in soup.select('.studentAnswer, .studentAnswerHeader, .questionExplanation, .questionWidget-explanation'):
        node.decompose()
    for comment in soup.find_all(string=lambda value: isinstance(value, Comment)):
        comment.extract()
    nodes = [n for n in soup.select('.freeResponseTextbox, .selectList')
             if not n.parent.find_parent(class_=['freeResponseTextbox', 'selectList'])]
    targets = [f for f in fields if f['type'] != 'radio']
    if len(nodes) != len(targets):
        return {}, 'history_field_layout_mismatch'
    result = {}
    source_paths = {a.get('source_url'): a.get('path') or a.get('stored_path')
                    for a in assets if a.get('source_url') and (a.get('path') or a.get('stored_path'))}
    for node, field in zip(nodes, targets):
        kind = 'blank' if 'freeResponseTextbox' in node.get('class', []) else 'select'
        if kind != field['type']:
            return {}, 'history_field_layout_mismatch'
        selected = node if kind == 'blank' else node.select_one(
            '.selectListFrame.correctSelection, .selectListFrameDisabled.correctSelection, '
            '.selectListFrame.correctSelectionMultipleAttempts, .selectListFrameDisabled.correctSelectionMultipleAttempts')
        if selected is None:
            continue
        renderer = Renderer(str(topic or ''))
        # A source image answer must reuse saved bytes, not a remote dependency.
        renderer.asset = lambda url: source_paths.get(url, url)
        value = renderer.text(selected)
        if renderer.errors or not value:
            continue
        if re.fullmatch(r'\$[^$]+\$', value):
            answer = {'type': 'math', 'value': value[1:-1]}
        elif re.fullmatch(r'!\[\]\([^)]+\)', value):
            answer = {'type': 'image', 'value': value[4:-1]}
        else:
            answer = {'type': 'text', 'value': value}
        result[field['key']] = answer
    return result, None


def _explicit_solution(field, fields, solution):
    """Accept an explicit answer statement, never an incidental formula.

    Multiple fields need their separately displayed answers. For a choice
    question a source conclusion must match exactly one captured choice; no
    equation solving, choice elimination, or solver interpretation is performed.
    """
    if len(fields) != 1 or not solution:
        return None
    statement = re.search(r'\b(?:the\s+)?correct\s+answer\s+is\s*:?\s*([^\n]+)', solution, re.I)
    text = statement[1].strip().strip('\"\'“”‘’* ').removesuffix('.').strip() if statement else None
    if text:
        letter = re.fullmatch(r'(?:option\s+)?\(?([a-zA-Z])\)?', text, re.I)
        if letter and field['type'] == 'radio':
            matches = [_answer(c) for c in field.get('choices', [])
                       if str(c.get('option', '')).lower() == letter[1].lower()]
            return matches[0] if len(matches) == 1 else None
    if field['type'] == 'blank':
        if not text:
            return None
        return ({'type': 'math', 'value': text[1:-1].removesuffix('.')}
                if re.fullmatch(r'\$[^$]+\$', text) else {'type': 'text', 'value': text})
    # Explicit final source prose such as "Therefore, the solutions are $x=...$"
    # is an authored key if the entire expression is already an original option.
    candidates = [text] if text else []
    final = solution.strip().split('\n\n')[-1].strip()
    conclusion = re.fullmatch(
        r'(?:(?:Therefore|Thus|Hence|So)[,:]?\s+)?'
        r'(?:(?:the\s+)?(?:correct\s+)?(?:answer|solutions?|result)\s+(?:is|are)\s+)?'
        r'(\$[^$]+\$)\.?', final, re.I)
    signaled = bool(re.match(r'(?:Therefore|Thus|Hence|So)\b', final, re.I) or
                    re.search(r'\b(?:answer|solutions?|result)\s+(?:is|are)\b', final, re.I))
    if conclusion and signaled:
        candidates.append(conclusion[1])
    matches = []
    for text in candidates:
        value = ({'type': 'math', 'value': text[1:-1].removesuffix('.')}
                 if re.fullmatch(r'\$[^$]+\$', text) else {'type': 'text', 'value': text})
        for choice in field.get('choices', []):
            choice = _answer(choice)
            if choice and _same(choice, value) and choice not in matches:
                matches.append(choice)
    return matches[0] if len(matches) == 1 else None


def _submitted(field):
    value = field.get('submitted_value')
    if not isinstance(value, str) or not value.strip():
        return None
    if field['type'] in ('radio', 'select'):
        # Match the actual entered value, never a solver option or prediction.
        matches = [_answer(c) for c in field.get('choices', []) if _answer(c)
                   and (c['value'] == value or _same(_answer(c), {'type': c['type'], 'value': value}))]
        return matches[0] if len(matches) == 1 else None
    return {'type': 'math' if field.get('tag') == 'mathquill' else 'text', 'value': value}


def _complete_choices(field, before):
    if field['type'] == 'blank':
        return True
    choices = field.get('choices', [])
    if not choices or any(not _answer(c) for c in choices):
        return False
    if field.get('choices_complete') is True:
        return True
    # Original captures predate the explicit completeness field.
    count = len(re.findall(r'class="[^"\n]*\b(?:questionWidget-choiceText|choiceText)\b', before.get('html', '')))
    return 'choices_complete' not in field and field['type'] == 'radio' and count == len(choices)


def _metadata(directory):
    rows = _read(directory / 'activity-metadata.json')
    if isinstance(rows, dict):
        rows = rows.get('questions', list(rows.values()))
    return {r['id'].replace('question-', 'q-'): r for r in rows
            if isinstance(r, dict) and isinstance(r.get('id'), str)}


def _canonical_capture(question, directory):
    mid = question['math_academy_id'].removeprefix('e-')
    if question.get('source_kind') != 'topic_page_example':
        return _read(directory / ('example-' + mid + '.json'))
    source = directory / 'lesson-topic.html'
    raw = _read(directory / ('lesson-example-' + mid + '.json'))
    if not raw or not source.is_file():
        return {}
    if any(Path(item.get('source_file', '')).resolve() != source.resolve() for item in (question, raw)):
        return {}
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(raw.get('html', ''), 'html.parser')
    fragment = soup.select_one('div.step[steptype="example"][contentid="' + mid + '"]')
    original = BeautifulSoup(source.read_text(), 'html.parser').select_one(
        'div.step[steptype="example"][contentid="' + mid + '"]')
    if not all(node is not None and node.select_one('.exampleQuestion') is not None
               and node.select_one('.exampleExplanation') is not None for node in (fragment, original)):
        return {}
    return raw


def prepare_authoritative_content(content, directory, *, state=None):
    """Return (prepared_content, review) without modifying capture files.

    review has held_questions, disagreements, and observations lists. A held
    practice question is omitted entirely; the caller holds the whole activity
    rather than transacting a partial multistep or an incomplete lesson.
    """
    directory = Path(directory)
    state = deepcopy(state) if state is not None else _read(directory / 'state.json')
    metadata = _metadata(directory)
    prepared = deepcopy(content)
    prepared['questions'], prepared['canonical_examples'] = [], []
    review = {'policy': VERSION, 'source': ':org/Math-Academy',
              'held_questions': [], 'disagreements': [], 'observations': []}
    for canonical, questions in ((False, content.get('questions', [])), (True, content.get('canonical_examples', []))):
        for original in questions:
            q = deepcopy(original)
            mid = q['math_academy_id']
            record = state.get('questions', {}).get(mid, {})
            if canonical:
                before = _canonical_capture(q, directory)
                after = history = before
            else:
                before = record.get('before') or _read(directory / (mid + '-before.json'))
                after = record.get('after') or _read(directory / (mid + '-after.json'))
                history = record.get('history') or _read(directory / ('history-' + mid + '.json'))
            source_solution = history if history.get('worked_solution') else after
            reasons = []
            if not before or not source_solution:
                reasons.append('missing_original_capture')
            if before.get('errors') or source_solution.get('errors'):
                reasons.append('source_extraction_errors')
            problem = before.get('source_problem') or before.get('problem')
            if content.get('task_type') == 'multistep':
                problem = record.get('local_problem') or before.get('local_problem') or q.get('local_problem') or before.get('problem')
            solution = source_solution.get('worked_solution')
            if not problem or not solution:
                reasons.append('missing_source_problem_or_solution')
            elif any(marker in problem + solution for marker in ('[Missing image:', '[MATH:', '[IMG:', '@asset-')):
                reasons.append('unresolved_source_markup')
            q['problem'], q['worked_solution'] = problem, solution
            for name in ('source_feedback_interpretation', 'source_answer_policy', 'mathematical_assessment', 'submission_recovery'):
                q.pop(name, None)
            if original.get('problem') != problem and problem:
                review['disagreements'].append({'question': mid, 'attribute': 'question/problem',
                    'reason': 'original_source_problem_restored', 'source_value': problem,
                    'previous_prepared_value': original.get('problem')})
            q.pop('requires_calculator', None)
            instructions = before.get('calculator_instructions', '')
            if instructions:
                q['requires_calculator'] = not bool(re.search(r'not|without|forbidden', instructions, re.I))
            rating = metadata.get(mid, {}).get('difficulty')
            if rating in ('E', 'M', 'H'):
                q['difficulty'] = {'E': 'easy', 'M': 'moderate', 'H': 'hard'}[rating]
            fields = before.get('fields', [])
            if not canonical and not fields:
                reasons.append('missing_original_answer_fields')
            if canonical and fields:
                reasons.append('unexpected_canonical_example_answer_fields')
            if len({f.get('key') for f in fields}) != len(fields):
                reasons.append('duplicate_answer_field_keys')
            # DOM-only snapshots; predictions and verification model output are
            # deliberately absent. Proof stages can contain earlier accepted keys.
            snapshots = [('before', before)] + [
                ('proof_stage_' + str(i), stage['observation'])
                for i, stage in enumerate(record.get('proof_stages', []))
                if isinstance(stage.get('observation'), dict)] + [('after', after), ('history', history)]
            displayed, observation = _displayed_history(metadata.get(mid, {}).get('raw_html'), fields,
                q.get('topic_id', content.get('topic_id')), before.get('assets', []) + source_solution.get('assets', []))
            if observation:
                review['observations'].append({'question': mid, 'reason': observation})
            prepared_fields = []
            for raw in fields:
                key, kind = raw.get('key'), raw.get('type')
                if not key or kind not in ('radio', 'select', 'blank'):
                    reasons.append('unsupported_answer_field')
                    continue
                if not _complete_choices(raw, before):
                    reasons.append('incomplete_original_choices:' + key)
                    continue
                candidates = []
                for stage, item in snapshots:
                    captured = _raw_fields(item).get(key)
                    if not captured or item.get('errors') or not _same_layout(captured, raw):
                        continue
                    direct = _answer(captured.get('source_correct'))
                    if direct:
                        candidates.append((3, direct, 'ma_explicit_answer', stage))
                    if captured.get('source_result') == 'Correct':
                        selected = _answer(captured.get('source_selected')) or _submitted(captured)
                        if selected:
                            candidates.append((2, selected, 'ma_successful_field_grade', stage))
                grade = record.get('actual_result') or after.get('result') or metadata.get(mid, {}).get('result')
                if grade in ('Correct', 'Full Credit'):
                    submitted = _submitted(raw)
                    if submitted:
                        candidates.append((1, submitted, 'ma_successful_grade', 'before+after'))
                explicit = _explicit_solution(raw, fields, solution)
                if explicit:
                    candidates.append((2, explicit, 'ma_explicit_solution_statement', 'worked_solution'))
                if key in displayed:
                    candidates.append((4, displayed[key], 'ma_history_displayed_answer', 'activity-metadata.json'))
                if not candidates:
                    reasons.append('unconfirmed_correct_answer:' + key)
                    continue
                # Displayed source keys take precedence over accepted alternative
                # submissions. Retain differing observations as review evidence.
                _, correct, origin, stage = sorted(candidates, key=lambda x: x[0])[-1]
                choices = [_answer(c) for c in raw.get('choices', [])] if kind != 'blank' else [correct]
                if kind != 'blank':
                    matches = [choice for choice in choices if _same(choice, correct)]
                    if len(matches) == 1:
                        correct = matches[0]
                    elif len(matches) == 0:
                        reasons.append('source_key_not_in_original_choices:' + key)
                        continue
                    else:
                        reasons.append('ambiguous_original_choice:' + key)
                        continue
                for _, candidate, category, at in candidates:
                    if not _same(candidate, correct):
                        review['observations'].append({'question': mid, 'field': key,
                            'reason': 'source_answer_values_differ', 'selected': correct,
                            'other': candidate, 'evidence': category, 'stage': at})
                out = {'key': key, 'type': kind, 'choices': choices,
                       'correct_value': correct['value'], 'choices_complete': kind != 'blank',
                       'correct_origin': origin, 'source_evidence': {'stage': stage, 'policy': VERSION}}
                prepared_fields.append(out)
                predictions = record.get('predicted_answers', []) + record.get('decision', {}).get('answers', [])
                predictions += record.get('verification', {}).get('answers', [])
                predictions += [{'key': f['key'], 'correct_value': f.get('correct_value'),
                                 'value_type': next((c['type'] for c in f.get('choices', []) if c['value'] == f.get('correct_value')), 'text')}
                                for f in original.get('answer_fields', [])]
                seen = set()
                for predicted in predictions:
                    other = _answer({'type': predicted.get('value_type'), 'value': predicted.get('correct_value')})
                    if predicted.get('key') == key and other and not _same(other, correct) and (other['type'], other['value']) not in seen:
                        seen.add((other['type'], other['value']))
                        review['disagreements'].append({'question': mid, 'field': key,
                            'reason': 'assistant_answer_differs_from_math_academy', 'source_answer': correct,
                            'assistant_answer': other, 'source_evidence': out['source_evidence'],
                            'action': 'preserve_math_academy_original; review_later'})
            q['answer_fields'] = prepared_fields
            if reasons:
                review['held_questions'].append({'question': mid, 'canonical': canonical, 'reasons': sorted(set(reasons))})
            else:
                prepared['canonical_examples' if canonical else 'questions'].append(q)
    prepared['answer_preparation_policy'] = VERSION
    review['ready'] = not review['held_questions']
    review['prepared_questions'] = len(prepared['questions'])
    review['prepared_canonical_examples'] = len(prepared['canonical_examples'])
    return prepared, review
