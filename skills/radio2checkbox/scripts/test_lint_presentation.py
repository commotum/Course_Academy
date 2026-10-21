"""Regressions for actual historical conversions and presentation repairs."""
import copy
import json
from pathlib import Path
import unittest

from lint_presentation import lint_question

ROOT = Path(__file__).resolve().parents[3]


def question(prompt, keys, solution=''):
    return {':question/problem': prompt, ':question/worked-solution': solution,
            ':question/answer-fields': [{':answer-field/id': str(i),
                ':answer-field/key': key, ':answer-field/type': {':db/ident': ':answer-field.type/checkbox'}}
                for i, key in enumerate(keys)]}


def objects(contents, labels=None):
    labels = labels or ['I', 'II', 'III'][:len(contents)]
    return [{'source_label': label, 'field_id': str(i), 'content': content}
            for i, (label, content) in enumerate(zip(labels, contents))]


class PresentationTests(unittest.TestCase):
    def test_actual_statement_conversion_and_repair(self):
        path = ROOT / 'reference/edb-math/imports/authored-checkboxes/2026-10-12/finder-easy/plan.json'
        row = next(q for q in json.loads(path.read_text())['questions'] if q['id'] == 17592186262617)
        contents = ['$C$ is upper triangular', '$C$ is lower triangular', '${C}^{T}$ is upper triangular']
        before = question(row['problem_after'], row['labels'])
        errors = lint_question(before, objects(contents))
        self.assertIn('bare_label', {e['code'] for e in errors})
        self.assertIn('object_left_in_prompt', {e['code'] for e in errors})
        after = question(row['problem_after'].split('\n\n- **I.**')[0], contents)
        self.assertEqual(lint_question(after, objects(contents)), [])

    def test_actual_named_matrix_conversion_and_repair(self):
        path = ROOT / 'reference/edb-math/imports/authored-checkboxes/2026-10-12/finder-remaining/plan.json'
        row = next(q for q in json.loads(path.read_text())['questions'] if q['id'] == 17592186120421)
        contents = [r'$$A=\begin{bmatrix}8 & 0 & -1 & 0 \\ 0 & 0 & 0 & 7 \\ 0 & 0 & -4 & 5 \\ 0 & 0 & 0 & 1\end{bmatrix}$$',
                    r'$$B=\begin{bmatrix}1 & 0 & 6 \\ 0 & -1 & 3 \\ 5 & 7 & 11\end{bmatrix}$$',
                    r'$$C=\begin{bmatrix}2 & 0 & 1 \\ 0 & 1 & 0 \\ 0 & 3 & 0\end{bmatrix}$$']
        mapping = objects(contents, ['A', 'B', 'C'])
        before = question(row['problem_after'], row['labels'])
        self.assertIn('matrix_left_in_prompt', {e['code'] for e in lint_question(before, mapping)})
        after = question(row['problem_after'].split('\n\n$A=')[0], contents)
        self.assertEqual(lint_question(after, mapping), [])
        duplicate = question(row['problem_after'], contents)
        self.assertIn('matrix_left_in_prompt', {e['code'] for e in lint_question(duplicate, mapping)})

    def test_equation_options_move_into_fields(self):
        contents = ['$y=2x$', '$y=x^2$', '$y=x^3$']
        mapping = objects(contents)
        before = question('Which functions solve the equation?\n\n- **I.** $y=2x$\n- **II.** $y=x^2$\n- **III.** $y=x^3$', contents)
        self.assertIn('list_left_in_prompt', {e['code'] for e in lint_question(before, mapping)})
        after = question(r'Which functions solve $y\prime=2$? Select all that apply.', contents)
        self.assertEqual(lint_question(after, mapping), [])

    def test_shared_diagram_exception_requires_evidence(self):
        q = question('![Four graphs](graphs.svg)\nSelect all that apply.', ['Graph I', 'Graph II'])
        mapping = objects(['Graph I', 'Graph II'])
        self.assertIn('bare_label', {e['code'] for e in lint_question(q, mapping)})
        for obj in mapping:
            obj['shared_image'] = {'image': 'graphs.svg', 'evidence': 'captured-image sha256:abc', 'reason': 'Both graphs are part of one shared coordinate diagram.'}
        self.assertEqual(lint_question(q, mapping), [])
        missing = copy.deepcopy(q)
        missing[':question/problem'] = 'Select all that apply.'
        self.assertIn('unsupported_image_exception', {e['code'] for e in lint_question(missing, mapping)})
        missing[':question/problem'] = '![Logo](logo.svg)\nSelect all that apply.'
        self.assertIn('unsupported_image_exception', {e['code'] for e in lint_question(missing, mapping)})

    def test_literal_numerical_objects_are_not_choice_labels(self):
        self.assertEqual(lint_question(question('Select the positive roots.', ['$1$', '$2$']), objects(['$1$', '$2$'])), [])
        self.assertIn('bare_label', {e['code'] for e in lint_question(question('Select all that apply.', ['Option 1']), objects(['Option 1']))})

    def test_mapping_and_solution_references(self):
        q = question('Select all that apply.', ['$x>0$', '$x<0$'], 'Statement I is true. Therefore, select "I only".')
        mapping = objects(['$x>0$', '$x<0$'])
        self.assertIn('removed_solution_label', {e['code'] for e in lint_question(q, mapping)})
        mapping[1]['field_id'] = '0'
        self.assertIn('field_mapping', {e['code'] for e in lint_question(q, mapping)})

    def test_shared_matrix_in_property_statement_is_not_a_selectable_matrix(self):
        matrix = r'\begin{bmatrix}a & b \\ c & d\end{bmatrix}'
        content = '$det' + matrix + r'\ne 0$'
        mapping = objects([content])
        mapping[0]['source_fragment'] = '- **I.** ' + content
        q = question('If the system $' + matrix + 'x=0$ has the unique zero solution, select the true conclusion.', [content])
        self.assertEqual(lint_question(q, mapping), [])

    def test_source_bullet_is_not_a_substring_of_a_decimal(self):
        mapping = objects(['The number $0$'])
        mapping[0]['source_fragment'] = '- $0$'
        q = question('Which values are outputs of $f(x)=1.5^{2x}-0.5$?', ['The number $0$'])
        self.assertEqual(lint_question(q, mapping), [])
        q[':question/problem'] += '\n\n- $0$'
        self.assertIn('source_left_in_prompt', {e['code'] for e in lint_question(q, mapping)})


if __name__ == '__main__':
    unittest.main()
