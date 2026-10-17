"""Read-only source/content review and nine display-only answer-vector repairs."""
from pathlib import Path
import hashlib
import json
import re
import sys

from bs4 import BeautifulSoup
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from math_format import matrix_answer, MATH

snapshot = json.loads((HERE.parent / 'lesson.json').read_text())
CAPTURE = ROOT / 'reference/mathacademy/question-capture/13977620'
WORKER = ROOT / 'reference/mathacademy/question-capture-workers/linear/14043216'
PATTERN = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def lexical(text):
    text = re.sub(r'\\(?:begin|end)\{aligned\}', '', text)
    text = text.replace(r'\cdot', '*').replace('⋅', '*').replace('−', '-').replace('∗', 'AST')
    text = text.replace(r'\,', '').replace('{', '').replace('}', '')
    return re.sub(r'\s+', '', text)


def matrices(text):
    return [[[lexical(cell) for cell in row.split('&')]
             for row in body.split(r'\\')] for body in PATTERN.findall(text)]


def expression(text):
    return parse_expr(lexical(text).replace('^', '**'),
                      transformations=standard_transformations + (implicit_multiplication_application,))


def sym_matrix(rows):
    return sp.Matrix([[expression(cell) for cell in row] for row in rows])


def source_matrices(node):
    result = []
    for table in node.select('math mtable'):
        parent = table.parent
        # An actual source matrix is a table between square-bracket operators;
        # the surrounding aligned-equation table is not itself a matrix.
        siblings = list(parent.find_all(recursive=False))
        if not (siblings[0].name == 'mo' and siblings[0].get_text() == '['
                and siblings[-1].name == 'mo' and siblings[-1].get_text() == ']'):
            continue
        result.append([[lexical(cell.get_text()) for cell in row.find_all('mtd', recursive=False)]
                       for row in table.find_all('mtr', recursive=False)])
    return result


reviews = []
practice = []
changes = []
for kp in snapshot['topic'][':topic/knowledge-points']:
    example = kp[':knowledge-point/canonical-example']
    mid = example[':question/math-academy-id'].split('-')[1]
    path = CAPTURE / f'example-{mid}.json'
    raw = path.read_bytes()
    source = json.loads(raw)
    soup = BeautifulSoup(source['html'], 'html.parser')
    fields = []
    for attribute, selector in [(':question/problem', '.exampleQuestion'),
                                (':question/worked-solution', '.exampleExplanation')]:
        expected = source_matrices(soup.select_one(selector))
        actual = matrices(example[attribute])
        assert expected == actual, (mid, attribute, expected, actual)
        fields.append({'attribute': attribute, 'source_matrix_count': len(expected),
                       'stored_matrix_count': len(actual), 'all_cells_and_order_match': True,
                       'matrix_cells': actual})
    reviews.append({'entity': example[':db/id'], 'ma_id': example[':question/math-academy-id'],
                    'knowledge_point': kp[':db/id'], 'source': str(path.relative_to(ROOT)),
                    'source_sha256': hashlib.sha256(raw).hexdigest(), 'fields': fields,
                    'finding': 'Complete operands, intermediate dot products, and final result; no missing mathematical content.'})

    for q in [example] + kp[':knowledge-point/questions']:
        operands = matrices(q[':question/problem'])
        assert len(operands) == 2, q[':db/id']
        result = sym_matrix(operands[0]) * sym_matrix(operands[1])
        solution = q.get(':question/worked-solution')
        if solution:
            final = sym_matrix(matrices(solution)[-1])
            assert final.shape == result.shape and all(sp.simplify(a-b) == 0 for a,b in zip(final,result)), q[':db/id']
        if q is example:
            continue
        practice.append({'entity': q[':db/id'], 'ma_id': q.get(':question/math-academy-id'),
                         'knowledge_point': kp[':db/id'], 'operands_complete': True,
                         'matrix_shape': list(sym_matrix(operands[0]).shape),
                         'vector_shape': list(sym_matrix(operands[1]).shape),
                         'existing_solution_present': bool(solution),
                         'existing_solution_final_result_verified': bool(solution),
                         'missing_solution_deferred': not bool(solution)})
        before = q[':question/problem']
        if '| ---' not in before:
            continue
        mid = q[':question/math-academy-id'][2:]
        path = next(p for p in [CAPTURE / f'q-{mid}-before.json', WORKER / f'q-{mid}-before.json'] if p.exists())
        raw = path.read_bytes()
        captured = json.loads(raw)
        soup = BeautifulSoup(captured['html'], 'html.parser')
        table = next(table for table in soup.find_all('table') if table.select('[id^=freeResponseTextbox]'))
        rows = table.find('tbody').find_all('tr', recursive=False)
        mapping = []
        field_index = {f['dom_id']: f for f in captured['fields']}
        edb_fields = {f[':answer-field/key']: f for f in q[':question/answer-fields']}
        for i, row in enumerate(rows, 1):
            inputs = row.select('[id^=freeResponseTextbox]')
            assert len(inputs) == 1, (q[':db/id'], i)
            source_field = field_index[inputs[0]['id']]
            key = source_field['key']
            assert key in edb_fields
            mapping.append({'source_row': i, 'source_input_dom_id': inputs[0]['id'],
                            'source_dom_index': source_field['dom_index'], 'field_key': key,
                            'answer_field_entity': edb_fields[key][':db/id'],
                            'new_row': i, 'new_column': 1})
        assert len(rows) == result.rows
        # Source bracket columns are borders in empty cells, not mathematical
        # values. The answer vector contains one editable entry in every row.
        assert set(edb_fields) == {m['field_key'] for m in mapping}
        prefix, old_table = before.split('\n\n|', 1)
        old_table = '|' + old_table
        label_math = MATH.findall(old_table)
        assert len(label_math) == 1
        label = label_math[0][1:-1].split('=')[0]
        placeholders = [['{{' + m['field_key'] + '}}'] for m in mapping]
        after = prefix + '\n\n' + matrix_answer(label, placeholders)
        assert re.findall(r'\{\{([^{}]+)\}\}', before) == re.findall(r'\{\{([^{}]+)\}\}', after)
        assert matrices(before) == matrices(after)
        changes.append({'entity': q[':db/id'], 'attribute': ':question/problem',
                        'before': before, 'after': after,
                        'reason': 'Restore the source column-vector answer layout, exterior brackets, and vertical row alignment using the existing matrix_answer component; preserve all field identities and values.',
                        'source': str(path.relative_to(ROOT)), 'source_sha256': hashlib.sha256(raw).hexdigest(),
                        'source_answer_table_html': str(table), 'source_row_mapping': mapping,
                        'supplied_cells': [], 'answer_label_preserved': label,
                        'all_placeholder_keys_and_order_preserved': True,
                        'all_matrix_operands_preserved': True})

assert len(reviews) == 3 and len(practice) == 38 and len(changes) == 9
write('review.json', {'identity': snapshot['identity'], 'canonical_examples': reviews,
                     'practice': practice, 'summary': {
                         'canonical_examples_reviewed': 3, 'canonical_examples_complete': 3,
                         'practice_questions_reviewed': 38, 'practice_prompts_complete': 38,
                         'practice_existing_solutions_reviewed': 34, 'missing_solutions_left_untouched': 4,
                         'all_37_existing_canonical_and_practice_solution_results_verified': True,
                         'answer_vector_display_repairs': 9,
                         'answer_data_changes': 0,
                         'note': 'Source row colors/background shading are not retained, but every mathematical component of all three examples is present.'}})
write('proposedchanges.json', changes)
print(json.dumps({'canonical_examples_complete': 3, 'practice_prompts_complete': 38,
                  'existing_solution_results_verified': 37, 'answer_vector_repairs': len(changes)}))
