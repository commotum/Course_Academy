"""Storage-contract regressions for the reported matrix/system failures."""
import copy
import unittest
from math_format import (cells, matrix_tex, matrix_operands, matrix_answer, normalize_tex, normalize_prose,
                          normalize_capture_question, system_tex, validate_tex,
                          validate_prose, validate_generated_record)

class MathContentTests(unittest.TestCase):
    def test_matrix_question_layout_keeps_tex_and_field_order(self):
        operands = matrix_operands(['A=' + matrix_tex([[1, 2], [3, 4]]), 'B=' + matrix_tex([[5, 6], [7, 8]])])
        self.assertIn('class="matrix-operands"', operands)
        self.assertIn('1 & 2', operands)
        self.assertNotIn('&amp;', operands)
        self.assertIn('class="matrix-operands matrix-operands-stacked"', matrix_operands(['A=' + matrix_tex([[1]])], stacked=True))
        for size in (2, 3):
            entries = [['{{field-' + str(r * size + c + 1) + '}}' for c in range(size)] for r in range(size)]
            answer = matrix_answer('A-B', entries)
            self.assertEqual(answer.count('<tr>'), size)
            self.assertEqual(answer.count('<td>'), size * size)
            self.assertIn('class="matrix-answer-brackets"', answer)
            self.assertIn('$A-B=$', answer)
            for row in entries:
                self.assertIn('<tr>' + ''.join('<td>' + cell + '</td>' for cell in row) + '</tr>', answer)
            self.assertNotIn('| ---', answer)
        self.assertIn('<td>$-12$</td>', matrix_answer('A', [['{{x}}', '-12']]))
        with self.assertRaises(ValueError): matrix_answer('A', [['{{x}}'], ['1', '2']])
        with self.assertRaises(ValueError): matrix_answer('A', [['']])
        with self.assertRaises(ValueError): matrix_operands(['$A$'])

    def test_matrix_roles_and_rows(self):
        rows = [[1, -1], [1, 1]]
        self.assertEqual(matrix_tex(rows), r'\begin{bmatrix}1 & -1 \\ 1 & 1\end{bmatrix}')
        augmented = matrix_tex([[1, -1, -1], [1, 1, -1]], augmented=True)
        self.assertIn('{cc|c}', augmented)
        self.assertEqual(cells(r'1 & \frac{2}{3} \\ 4 & 5'), [['1', r'\frac{2}{3}'], ['4', '5']])
        for rows in ([], [[1], [2, 3]]):
            with self.assertRaises(ValueError): matrix_tex(rows)
        with self.assertRaises(ValueError): matrix_tex([[1], [2]], augmented=True)

    def test_reported_system_wrappers_and_equals(self):
        expected = system_tex(['x+3y=7', '2x+0y=4'])
        for source in (r'\{\begin{aligned}x+3y=7 \\ 2x+0y=4\end{aligned}',
                       r'{\begin{aligned}x+3y=7 \\ 2x+0y=4\end{aligned}',
                       r'\begin{aligned}{\begin{aligned}x+3y=7 \\ 2x+0y=4\end{aligned}\end{aligned}',
                       r'\begin{cases} & x+3y=7 \\ & 2x+0y=4\end{cases}',
                       r'{x+3y=7;2x+0y=4'):
            with self.subTest(source=source):
                result = normalize_tex(source)
                self.assertEqual(result, expected)
                self.assertEqual(normalize_tex(result), result)
                validate_tex(result)

    def test_piecewise_and_annotations_keep_their_roles(self):
        piecewise = r'f(x)=\begin{cases}x & x>0 \\ 0 & x\leq0\end{cases}'
        self.assertEqual(normalize_tex(piecewise), piecewise)
        annotated = normalize_tex(r'\{\begin{aligned}x=1 & R_1 \\ y=2 & R_2\end{aligned}')
        self.assertIn('x &=1 && R_1', annotated)
        self.assertIn('y &=2 && R_2', annotated)
        self.assertEqual(normalize_tex(r'{x=1;y=\frac{1}{2}'), system_tex(['x=1', r'y=\frac{1}{2}']))
        self.assertEqual(normalize_tex(r'{x=1;y=2}'), r'{x=1;y=2}')

    def test_legacy_matrix_keeps_two_rows_and_fraction(self):
        old = '[\\matrix{1 & 3\\\n2 & \\frac{1}{2}}]'
        result = normalize_tex(old)
        self.assertEqual(result, '\\begin{bmatrix}1 & 3\\\\\n2 & \\frac{1}{2}\\end{bmatrix}')
        validate_tex(result)
        self.assertEqual(normalize_tex(result), result)

    def test_prose_delimiters_and_bare_answers(self):
        self.assertEqual(normalize_prose(r'Value \(x\), matrix \[ [\begin{aligned}1 & 2 \\ 3 & 4\end{aligned}] \]'),
                         'Value $x$, matrix $$\n\\begin{bmatrix}1 & 2 \\\\ 3 & 4\\end{bmatrix}\n$$')
        self.assertEqual(normalize_tex('$$x$$'), 'x')
        self.assertEqual(normalize_prose(r'Price \$5 and $x$.'), r'Price \$5 and $x$.')
        for bad in ('$x', '$$x$', '$x$ and $'):
            with self.assertRaises(ValueError): validate_prose(bad)
        for bad in (r'\begin{bmatrix}1 & 2 \\ 3\end{bmatrix}', '{x', '$x$', r'\begin{aligned}x\end{cases}'):
            with self.assertRaises(ValueError): validate_tex(bad)

    def test_capture_boundary_normalizes_without_changing_source(self):
        question = {'problem': r'\[ [\matrix{1 & 3\cr 2 & 0}] \]',
                    'worked_solution': '$x=1$',
                    'answer_fields': [{'correct_value': '$x$', 'choices': [{'type': 'math', 'value': '$x$'}]}]}
        original = copy.deepcopy(question)
        saved = normalize_capture_question(question)
        self.assertEqual(question, original)
        self.assertEqual(saved['answer_fields'][0]['choices'][0]['value'], 'x')
        self.assertEqual(saved['answer_fields'][0]['correct_value'], 'x')
        self.assertIn(r'\begin{bmatrix}', saved['problem'])
        self.assertEqual(normalize_capture_question(saved), saved)

    def test_reported_display_commands_are_rejected_before_capture(self):
        # These rendered as red literal commands without MathJax merror nodes.
        for bad in (r'C^T=\=', r'\begin{aligned}a&=1\[5pt]b&=2\end{aligned}',
                    r'x+\(y\)'):
            with self.subTest(source=bad), self.assertRaises(ValueError):
                validate_tex(bad)
        with self.assertRaises(ValueError):
            normalize_capture_question({'problem': r'$C^T=\=$'})
        # A proper row separator with an optional gap remains valid, as do
        # scalable brackets and prose-level math delimiters.
        validate_tex(r'\begin{bmatrix}1 & 2 \\[3pt]3 & 4\end{bmatrix}')
        validate_tex(r'\left[x\right]')
        validate_prose(r'Value \(x\), display \[x=1\].')

    def test_generator_contract_rejects_noncanonical_output(self):
        record = {'question': {':question/problem': '$x$', ':question/worked-solution': '$x$',
                               ':question/answer-fields': [{':answer-field/choices': [{':answer/type': ':answer.type/math', ':answer/value': '$x$'}]}]}}
        with self.assertRaises(ValueError): validate_generated_record(record)
        record['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'] = 'x'
        self.assertEqual(validate_generated_record(record)['generation']['math_format'], 'course-academy-tex-v1')

if __name__ == '__main__': unittest.main()
