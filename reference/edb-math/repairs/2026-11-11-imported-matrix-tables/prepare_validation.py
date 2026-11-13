"""Build exact before/after UI and native-grader records for layout edits."""
import copy
import json
from pathlib import Path
import re
import sys

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import normalized_question, answer_id, enum


def build(proposals, output, final=False):
    output.mkdir(parents=True, exist_ok=True)
    original = json.loads((H/'capture/questions.json').read_text())
    parents = json.loads((H/'capture/parents.json').read_text())
    owned = {}
    for parent in parents:
        for q in parent.get(':knowledge-point/questions', []) + [parent.get(':knowledge-point/canonical-example', {})]:
            if ':db/id' in q:
                owned[q[':db/id']] = parent
    by_entity = {q[':db/id']: q for q in original}
    # Tutorials have no question record; they are verified separately as content.
    changes = {r['entity']: [] for r in proposals if r['entity'] in by_entity}
    for row in proposals:
        if row['entity'] in changes:
            changes[row['entity']].append(row)
    records = {'before': [], 'after': []}
    cases = {'before': [], 'after': []}
    incomplete = []
    overrides = {q[':db/id']: q for q in json.loads((H/'questions-after.json').read_text())} if final else {}
    created = {r['field_entity'] for r in json.loads((H/'plan.json').read_text())['answer_creations']} if final else set()
    for qid, rows in sorted(changes.items()):
        q = by_entity[qid]
        patched = copy.deepcopy(overrides.get(qid, q))
        bad = [f[':answer-field/key'] for f in patched.get(':question/answer-fields', [])
               if ':answer-field/correct' not in f]
        if bad:
            incomplete.append({'entity': qid, 'missing_correct_keys': bad})
            continue
        if not final:
            for row in rows:
                assert q[':'+row['attribute']] == row['before']
                patched[':'+row['attribute']] = row['after']
        parent = owned.get(qid, {})
        for state, question in [('before', q), ('after', patched)]:
            if any(':answer-field/correct' not in f for f in question.get(':question/answer-fields', [])):
                continue
            n = normalized_question(question)
            for field in n[':question/answer-fields']:
                field[':answer-field/correct'] = [':answer/id', field[':answer-field/correct']]
            record = {'knowledge_point': {'db_id': parent.get(':db/id'),
                       'title': parent.get(':knowledge-point/title', 'Imported matrix question')},
                      'question': n, 'generation': {'template': 'imported-matrix-layout-repair', 'entity': qid}}
            records[state].append(record)
            checks = []
            for index, field in enumerate(n[':question/answer-fields']):
                correct = answer_id(field[':answer-field/correct'])
                if enum(field[':answer-field/type']) != ':answer-field.type/blank':
                    for choice in field[':answer-field/choices']:
                        checks.append({'field_index': index, 'submitted_answer_id': choice[':answer/id'],
                            'expected': 'accepted' if choice[':answer/id'] == correct else 'rejected',
                            'purpose': 'Preserve grading of every authored choice during layout-only repair'})
                else:
                    value = next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id'] == correct)
                    checks.append({'field_index': index, 'submitted': value, 'expected': 'accepted',
                        'purpose': 'Preserve the existing canonical field answer through a layout-only repair'})
                    if re.fullmatch(r'[+-]?\d+', value):
                        checks.append({'field_index': index, 'submitted': str(int(value)+1), 'expected': 'rejected',
                            'purpose': 'A distinct numeric entry must remain incorrect after moving its input'})
            if checks:
                if final and state == 'after':
                    # Newly completed blank banks are checked with an algebraic
                    # equivalent and a distinct value, beyond identity matching.
                    original_fields = {f[':answer-field/key']: f for f in question.get(':question/answer-fields', [])}
                    for index, field in enumerate(n[':question/answer-fields']):
                        if original_fields[field[':answer-field/key']][':db/id'] not in created or field[':answer-field/type'] != ':answer-field.type/blank':
                            continue
                        value = next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id'] == answer_id(field[':answer-field/correct']))
                        checks.extend([{'field_index': index, 'submitted': '2*('+value+')/2', 'expected': 'accepted', 'purpose': 'Equivalent expression for independently derived new canonical answer'},
                                       {'field_index': index, 'submitted': '('+value+')+1', 'expected': 'rejected', 'purpose': 'Incorrect perturbation of newly completed field'}])
                cases[state].append({'label': str(qid), 'record': record, 'checks': checks})
    for state in records:
        for name, value in [(f'records-{state}.json', records[state]), (f'native-{state}-input.json', cases[state])]:
            (output/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
    (output/'preexisting-incomplete.json').write_text(json.dumps(incomplete, indent=2)+'\n')
    result = {'question_entities_changed': len(changes), 'complete_questions': len(records['after']),
              'preexisting_incomplete_questions': len(incomplete), 'changed_content_fields': len(proposals)}
    (output/'scope.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    name = sys.argv[1] if len(sys.argv) > 1 else 'proposals.json'
    output = H/(sys.argv[2] if len(sys.argv) > 2 else 'validation')
    build(json.loads((H/name).read_text()), output, final='--final' in sys.argv)
