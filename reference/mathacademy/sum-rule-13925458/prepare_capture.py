#!/usr/bin/env python3
"""Join observed live widgets to activity metadata and read-only EDB matches."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'factorials-13831129'))
from verify_pilot import read_edn

CORRECT = {
    '71168': 'e', '29828': 'a', '113779': 'd', '71172': 'e', '113778': 'c',
    '113784': 'e', '2166': 'e', '113788': 'a', '2160': 'e', '113789': 'd',
    '49174': 'b', '49062': 'e', '113845': 'a', '113851': 'a', '2250': 'e',
}


def normalize_tex(value):
    # Comparison only: braces/spacing differ between the two MathJax renderers.
    return re.sub(r'[\s{}]', '', value).strip('$')


def main():
    live = json.loads((ROOT / 'live-capture.json').read_text())
    history = json.loads((ROOT / 'activity-capture.json').read_text())
    topic = read_edn(ROOT / 'database-before.edn')[0][0]
    matches = {r[0][':question/math-academy-id']: r[0]
               for r in read_edn(ROOT / 'id-matches.edn')}
    kps = {k[':knowledge-point/title']: k for k in topic[':topic/knowledge-points']}
    steps = {s['dom_id']: s for s in live['steps']}
    responses = {r['question_id']: r for r in live['responses']}
    questions, attempts, examples, report = [], [], [], []
    for index, hk in enumerate(history['kps']):
        title = hk['title'].split('. ', 1)[1]
        kp = kps[title]
        for hq in hk['questions']:
            number = hq['id'].removeprefix('question-')
            mid = 'q-' + number
            before, response = steps['step-q' + number], responses[number]
            after = response['after']
            assert len(before['choices']) == 5 and not before['controls']
            assert before['prompt']['markdown'] and after['worked_solution']['markdown']
            assert hq['explanation_html']
            expected = 'Correct' if response['submitted_letter'] == CORRECT[number] else 'Incorrect'
            assert response['actual_result'] == expected
            assert response['intended'] == ('C' if expected == 'Correct' else 'W')
            choices = [{'letter': c['letter'], 'type': 'math',
                        'value': c['content']['markdown'].strip('$'), 'dom_id': c['dom_id']}
                       for c in before['choices']]
            correct = next(c for c in choices if c['letter'] == CORRECT[number])
            record = matches.get(mid)
            questions.append({
                'math_academy_id': mid, 'is_example': False,
                'knowledge_point_id': kp[':knowledge-point/id'], 'knowledge_point': title,
                'problem': before['prompt']['markdown'],
                'difficulty': {'E': 'easy', 'M': 'moderate', 'H': 'hard'}[hq['difficulty']],
                'difficulty_source': 'activity .questionDifficulty',
                'worked_solution': after['worked_solution']['markdown'],
                'answer_fields': [{'key': 'selection', 'type': 'radio', 'choices': choices,
                                   'correct_letter': CORRECT[number], 'correct_value': correct['value']}],
                'field_type_evidence': 'Five clickable choice circles observed in the live question widget.',
                'correct_answer_evidence': 'Solved from the displayed problem and checked against the revealed worked solution; correct submissions also confirmed by the grader.',
                'database_question_id': record.get(':question/id') if record else None,
                'requires_calculator': None,
            })
            attempts.append({k: response[k] for k in ('question_id', 'intended', 'submitted_letter', 'actual_result')})
            entry = {'math_academy_id': mid, 'database_match': bool(record),
                     'knowledge_point_id': kp[':knowledge-point/id']}
            if record:
                field = record[':question/answer-fields'][0]
                entry['existing_type'] = field[':answer-field/type'][':db/ident']
                entry['correct_answer_matches'] = normalize_tex(field[':answer-field/correct'][':answer/value']) == normalize_tex(correct['value'])
                entry['choice_set_matches'] = {normalize_tex(c[':answer/value']) for c in field[':answer-field/choices']} == {normalize_tex(c['value']) for c in choices}
                entry['missing_attributes'] = [a for a in ('question/difficulty', 'question/worked-solution') if ':' + a not in record]
                assert entry['correct_answer_matches'] and entry['choice_set_matches']
                assert kp[':knowledge-point/id'] in [k[':knowledge-point/id'] for k in record[':knowledge-point/_questions']]
            report.append(entry)
        mid = 'e-' + str(371 + index)
        example = steps['step-e' + mid[2:]]
        record = matches[mid]
        assert kp[':knowledge-point/canonical-example'][':question/math-academy-id'] == mid
        examples.append({'math_academy_id': mid, 'is_example': True,
                         'knowledge_point_id': kp[':knowledge-point/id'], 'knowledge_point': title,
                         'problem': example['prompt']['markdown'],
                         'worked_solution': example['worked_solution']['markdown'],
                         'database_question_id': record[':question/id'],
                         'difficulty': None, 'answer_fields': [],
                         'missing_source_fields': ['difficulty', 'answer_fields', 'requires_calculator'],
                         'comparison': 'Same canonical example ID and mathematical problem/solution; rendering and punctuation differ.'})
    assert len(questions) == 15 and len(examples) == 3
    result = {'task_id': live['task_id'], 'topic_id': live['topic_id'],
              'source_url': history['source_url'], 'content_only': True,
              'sequence_policy': live['sequence_policy'], 'questions': questions, 'canonical_examples': examples}
    (ROOT / 'content.json').write_text(json.dumps(result, indent=2) + '\n')
    (ROOT / 'capture-attempts.json').write_text(json.dumps({'purpose': 'Intentional capture sequence; do not import as learner ability evidence.', 'attempts': attempts}, indent=2) + '\n')
    (ROOT / 'matching-report.json').write_text(json.dumps(report, indent=2) + '\n')
    summary = {'practice_questions': 15, 'canonical_examples': 3, 'practice_choices': 75,
               'existing_practice_questions': sum(r['database_match'] for r in report),
               'new_practice_questions': sum(not r['database_match'] for r in report),
               'existing_canonical_examples': 3, 'database_writes': 0,
               'practice_capture_complete': True,
               'canonical_source_has_no_answer_widgets_or_difficulty': True,
               'actual_sequences': ['WCWCC', 'CWCWC', 'CWCWC']}
    (ROOT / 'verification.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
