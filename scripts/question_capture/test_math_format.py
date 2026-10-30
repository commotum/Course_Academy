"""Storage-contract regressions for the reported matrix/system failures."""
import copy
import unittest
from math_format import (cells, legacy_system_rows, matrix_tex, matrix_operands, matrix_answer, normalize_tex, normalize_prose,
                          normalize_capture_question, system_tex, validate_tex,
                          validate_prose, validate_generated_record)

class MathContentTests(unittest.TestCase):
    def test_augmented_arrays_stretch_without_losing_rules_or_outer_alignment(self):
        from math_format import scalable_array_fences, validate_matrix_layouts
        array = r'\begin{array}{cc|cc}1&0&1&0\\0&\frac{1}{12}&0&1\end{array}'
        source = r'\begin{aligned}{}[N\mid I]&=[' + array + r']&R_2:=12R_2\\&\sim[' + array + r']\end{aligned}'
        with self.assertRaisesRegex(ValueError, 'scalable delimiters'):
            validate_matrix_layouts('$$' + source + '$$')
        expected = source.replace('[' + array + ']', r'\left[' + array + r'\right]')
        self.assertEqual(scalable_array_fences(source), expected)
        self.assertEqual(normalize_tex(source), expected)
        self.assertEqual(scalable_array_fences(expected), expected)
        self.assertEqual(expected.count(array), 2)
        validate_matrix_layouts('$$' + expected + '$$')
        validate_tex(expected)

    def test_array_fence_spellings_and_nested_arrays(self):
        from math_format import scalable_array_fences
        array = r'\begin{array}{c|c}a&b\\c&d\end{array}'
        for left, right in [('[', ']'), ('(', ')'), (r'\{', r'\}'), ('|', '|'),
                            (r'\lbrack', r'\rbrack'), (r'\lparen', r'\rparen'),
                            (r'\lbrace', r'\rbrace'), (r'\vert', r'\vert'),
                            (r'\lvert', r'\rvert'), (r'\Vert', r'\Vert'),
                            (r'\lVert', r'\rVert'), (r'\langle', r'\rangle')]:
            with self.subTest(left=left):
                self.assertEqual(scalable_array_fences(left + array + right),
                                 r'\left' + left + array + r'\right' + right)
        nested = r'[\begin{array}{c}(' + array + r')\\x\end{array}]'
        expected = r'\left[\begin{array}{c}\left(' + array + r'\right)\\x\end{array}\right]'
        self.assertEqual(scalable_array_fences(nested), expected)
        self.assertEqual(scalable_array_fences(expected), expected)

    def test_array_fences_preserve_deliberate_sizes_optional_arguments_and_data_tables(self):
        from math_format import scalable_array_fences, validate_matrix_layouts
        array = r'\begin{array}{c}a\\b\end{array}'
        values = [array, r'\left[' + array + r'\right]', r'\bigl[' + array + r'\bigr]',
                  r'\Big[' + array + r'\Big]', r'\sqrt[' + array + r']{x}',
                  r'A\xrightarrow[' + array + r']{f}B', r'P(A\mid B)',
                  r'[x,y]', r'[\begin{array}{c}a\\b\end{array})']
        for source in values:
            with self.subTest(source=source):
                self.assertEqual(scalable_array_fences(source), source)
                validate_matrix_layouts('$' + source + '$')

    def test_spaced_array_fences_and_one_sided_condition_brace(self):
        from math_format import scalable_array_fences, validate_matrix_layouts
        array = r'\begin{array}{rl}x&=1\\y&=2\end{array}'
        source = r'\{\hspace{0.278em} ' + array
        expected = r'\left\{\hspace{0.278em} ' + array + r'\right.'
        self.assertEqual(scalable_array_fences(source), expected)
        self.assertEqual(scalable_array_fences('$$' + source + '$$'), '$$' + expected + '$$')
        self.assertEqual(scalable_array_fences(expected), expected)
        validate_tex(expected)
        with self.assertRaisesRegex(ValueError, 'scalable delimiters'):
            validate_matrix_layouts('$' + source + '$')
        spaced = r'[\quad ' + array + r'\,]'
        self.assertEqual(scalable_array_fences(spaced), r'\left[\quad ' + array + r'\,\right]')

    def test_capture_normalizes_array_choices_and_updates_matching_correct_value(self):
        bad = r'|\begin{array}{c|c}a&b\\c&d\end{array}|'
        source = {'problem': '$' + bad + '$', 'worked_solution': '$' + bad + '$',
                  'answer_fields': [{'correct_value': bad, 'choices': [{'type': 'math', 'value': bad}]}]}
        result = normalize_capture_question(source)
        good = r'\left' + bad[:-1] + r'\right|'
        self.assertEqual(result['problem'], '$' + good + '$')
        self.assertEqual(result['answer_fields'][0]['correct_value'], good)
        self.assertEqual(result['answer_fields'][0]['choices'][0]['value'], good)
        self.assertEqual(source['answer_fields'][0]['correct_value'], bad)

    def test_equation_system_and_gathered_condition_braces_stretch_too(self):
        from math_format import scalable_table_fences, validate_matrix_layouts
        for env in ['aligned', 'gathered']:
            body = r'x=1\\y=2' if env == 'gathered' else r'x&=1\\y&=2'
            source = r'\{\begin{' + env + '}' + body + r'\end{' + env + '}'
            expected = r'\left' + source + r'\right.'
            with self.subTest(env=env):
                self.assertEqual(scalable_table_fences(source), expected)
                with self.assertRaisesRegex(ValueError, 'scalable delimiters'):
                    validate_matrix_layouts('$' + source + '$')
                validate_matrix_layouts('$' + expected + '$')
                validate_tex(expected)
        inner = r'\{\begin{aligned}x&=1\\y&=2\end{aligned}'
        chain = r'\begin{aligned}' + inner + r'\,\Rightarrow\,' + inner + r'\end{aligned}'
        result = scalable_table_fences(chain)
        self.assertEqual(result, chain.replace(inner, r'\left' + inner + r'\right.'))
        validate_tex(result)

    def test_visible_aligned_prefix_survives_optional_placement_parsing(self):
        value = r'\begin{aligned}[A\,|\,I] &= M\end{aligned}'
        guarded = r'\begin{aligned}{}[A\,|\,I] &= M\end{aligned}'
        with self.assertRaisesRegex(ValueError, 'consumed as placement'): validate_tex(value)
        self.assertEqual(normalize_tex(value), guarded)
        validate_tex(guarded)
        self.assertEqual(normalize_tex(guarded), guarded)
        for option in ['t', 'b', 'c']:
            positioned = r'\begin{aligned}[' + option + r']x&=1\end{aligned}'
            self.assertEqual(normalize_tex(positioned), positioned)

    def test_legacy_matrix_controls_keep_rows_and_leave_data_tables_alone(self):
        from math_format import normalize_matrix_answer_tables
        given = r'$A=\begin{bmatrix}1&2\\3&4\end{bmatrix}$'
        source = given + '\n\n' + '\n'.join([
            '| $AI_2=$ | | {{a}} | {{b}} | |', '| --- | --- | --- | --- | --- |',
            '| | {{c}} | {{d}} | | |'])
        result = normalize_matrix_answer_tables(source)
        self.assertIn('<tr><td>{{a}}</td><td>{{b}}</td></tr>', result)
        self.assertIn('<tr><td>{{c}}</td><td>{{d}}</td></tr>', result)
        self.assertEqual(normalize_matrix_answer_tables(result), result)
        table = given + '\n| Input | Output |\n| --- | --- |\n| $x$ | {{a}} |'
        self.assertEqual(normalize_matrix_answer_tables(table), table)

    def test_quoted_display_math_keeps_markers_outside_tex_and_closes_in_quote(self):
        source = '> Rule\n>\n> $$\n> A\\cdot I_n=A\n> $$'
        self.assertEqual(normalize_prose(source), source)
        self.assertEqual(normalize_prose(normalize_prose(source)), source)
        nested = '> > $$\n> > > x\n> > $$'
        self.assertEqual(normalize_prose(nested), nested)

    def test_source_equality_chain_keeps_spaced_correctness_annotation(self):
        source = r'\begin{aligned}12x-28 &= \\ (4\cdot3x)-(4\cdot7) &= \\ 4(3x-7)&.\hspace{2em}{\color{green}{✓}}\end{aligned}'
        result = normalize_tex(source)
        validate_tex(result)
        self.assertIn(r'12x-28 &= (4\cdot3x)-(4\cdot7)', result)
        self.assertIn(r'&= 4(3x-7)', result)
        self.assertIn(r'.\hspace{2em}{\color{green}{✓}}', result)
        self.assertEqual(normalize_tex(result), result)
        independent = r'\begin{aligned}x&=2\\y&=3\end{aligned}'
        self.assertEqual(normalize_tex(independent), independent)

    def test_structural_check_includes_matrix_layout_after_source_recovery(self):
        from math_format import validate_math_structure
        with self.assertRaisesRegex(ValueError, 'matrix environment'):
            validate_math_structure(r'$D=|\begin{aligned}1&3\\2&-3\end{aligned}|$')
        validate_math_structure(r'$D=\begin{vmatrix}1&3\\2&-3\end{vmatrix}$')
        with self.assertRaisesRegex(ValueError, 'fence scope'):
            validate_tex(r'\left.\int\frac{\mid x\right|^3}{1+x}')
        with self.assertRaisesRegex(ValueError, 'Sizing command'):
            validate_tex(r'\left.x^2\Big\right|_0^1')
        validate_tex(r'\int\frac{\left|x\right|^3}{1+x}')
        with self.assertRaisesRegex(ValueError, 'delimiter glyph'):
            validate_tex(r'\left(\frac{7}{9}\right')
        validate_tex(r'\left(\frac{7}{9}\right.')

    def test_piecewise_brace_is_not_a_group_and_sized_bars_are_delimiters(self):
        source = r'f(x)={\begin{aligned}x^2&x<0\\0&x=0\\x&x>0\end{aligned}'
        self.assertEqual(normalize_tex(source), r'f(x)=\begin{cases}x^2&x<0\\0&x=0\\x&x>0\end{cases}')
        grouped = r'{\begin{aligned}a&b\\c&d\end{aligned}}'
        self.assertEqual(normalize_tex(grouped), grouped)
        self.assertEqual(normalize_tex(r'\big\mid A\big\mid=P(A\mid B)'),
                         r'\big\vert A\big\vert=P(A\mid B)')

    def test_limit_operator_keeps_its_tendency_condition(self):
        self.assertEqual(normalize_tex('\\displaystyle lim_(x → 2)f(x)'),
                         r'\displaystyle \lim_{x \to  2}f(x)')
        self.assertEqual(normalize_tex(r'\displaystyle {lim}_{x\to2}f(x)'),
                         r'\displaystyle \lim_{x\to2}f(x)')
        for source in (r'{lim}_{x\to 2}4^{x/2}', r'{\lim}_{x\to 2}4^{x/2}',
                       r'lim_{x\to 2}4^{x/2}', r'\lim_\limits{x\to 2}4^{x/2}'):
            self.assertEqual(normalize_tex(source), r'\lim_{x\to 2}4^{x/2}')
        self.assertEqual(normalize_tex('lim_(x → - ∞)2^x'), r'\lim_{x \to  - \infty}2^x')
        self.assertEqual(normalize_tex(r'a_{lim}+\text{lim}'), r'a_{lim}+\text{lim}')
        for source in (r'\text{lim}_{x\to 2}', r'\operatorname*{lim}_{x\to 2}', r'\mathbf {lim}_{x\to 2}'):
            self.assertEqual(normalize_tex(source), source)
        self.assertEqual(normalize_tex(r'{lim}_{{x}\rightarrow2}f(x)'), r'\lim_{{x}\rightarrow2}f(x)')
        self.assertEqual(normalize_tex(r'lim_{x\to2}f(x)'), r'\lim_{x\to2}f(x)')
        self.assertEqual(normalize_tex(r'{lim}_{x\downarrow0}f(x)'), r'\lim_{x\downarrow0}f(x)')
        self.assertEqual(normalize_tex('lim_((x,y)→(0,0))f(x,y)'), r'\lim_{(x,y)\to (0,0)}f(x,y)')
        self.assertEqual(normalize_tex(r'\text{lim_{x\to2}}'), r'\text{lim_{x\to2}}')

    def test_wrapped_additive_scalar_is_not_a_matrix(self):
        source = r'e^t\left(\begin{aligned}&x\\&{}+(y)\end{aligned}\right)'
        result = normalize_tex(source)
        self.assertIn(r'\begin{aligned}', result)
        self.assertNotIn('matrix', result)
        self.assertEqual(normalize_tex(result), result)
        self.assertEqual(normalize_tex(r'\left(\begin{aligned}1&2\\3&4\end{aligned}\right)'),
                         r'\begin{pmatrix}1&2\\3&4\end{pmatrix}')
        self.assertIn(r'\begin{pmatrix}',
            normalize_tex(r'\left(\begin{matrix}&x\\&{}+(y)\end{matrix}\right)'))

    def test_ruled_mathml_tables_keep_cells_rules_and_alignment(self):
        from math_format import mathml_ruled_table
        rows = [['x', '-1', '2'], ['u', '1', '10']]
        self.assertEqual(mathml_ruled_table(rows, {'columnalign': 'center center',
            'columnlines': 'solid', 'rowlines': 'solid', 'frame': 'solid'}),
            r'\begin{array}{|c|c|c|}\hline x & -1 & 2 \\ \hline u & 1 & 10 \\ \hline\end{array}')
        self.assertEqual(mathml_ruled_table([['a', 'b', 'c'], ['d', 'e', 'f']],
            {'columnalign': 'right left', 'columnlines': 'none solid'}),
            r'\begin{array}{rl|l}a & b & c \\ d & e & f\end{array}')
        self.assertIsNone(mathml_ruled_table(rows, {'columnalign': 'right left'}))
        with self.assertRaisesRegex(ValueError, 'columnlines'):
            mathml_ruled_table(rows, {'columnlines': 'dashed'})

    def test_html_emphasis_moves_padding_outside_markers(self):
        from math_format import markdown_emphasis
        self.assertEqual(markdown_emphasis(' Step 1', '**'), ' **Step 1**')
        self.assertEqual(markdown_emphasis('term ', '**'), '**term** ')
        self.assertEqual(markdown_emphasis(' hint ', '*'), ' *hint* ')
        self.assertEqual(markdown_emphasis(' *minimum* ', '**'), ' ***minimum*** ')
        self.assertEqual(markdown_emphasis(' ', '**'), ' ')
        self.assertEqual(markdown_emphasis('', '**'), '')

    def test_mixed_chain_relations_and_final_punctuation(self):
        cases = [
            (r'\begin{aligned}x+x &= \\ 2x & .\end{aligned}',
             r'\begin{aligned}x+x &= 2x.\end{aligned}'),
            (r'\begin{aligned}x+x &= \\ &=2x\end{aligned}',
             r'\begin{aligned}x+x &= 2x\end{aligned}'),
            (r'\begin{aligned}x+x= \\ 2x &\end{aligned}',
             r'\begin{aligned}x+x &= 2x\end{aligned}'),
            (r'\begin{aligned}\sqrt{2}+1 &≈ \\ 1.414+1 &= \\ 2.414 &≈ \\ 2.41\end{aligned}',
             r'\begin{aligned}\sqrt{2}+1 &≈ 1.414+1 \\ &= 2.414 \\ &≈ 2.41\end{aligned}'),
        ]
        for source, expected in cases:
            self.assertEqual(normalize_tex(source), expected)
            self.assertEqual(normalize_tex(expected), expected)
            validate_tex(expected)

    def test_ambiguous_chains_and_missing_proof_blanks_are_not_inferred(self):
        for source in (r'\begin{aligned}a_1 &=\end{aligned}',
                       r'\begin{aligned}a_1 &= \\ a_2 &=\end{aligned}',
                       r'\begin{aligned}a &= \\ b \\ c\end{aligned}',
                       r'\begin{aligned}a &= \\ &≈ b\end{aligned}',
                       r'\begin{aligned}x &=1 \\ y &=2\end{aligned}'):
            self.assertEqual(normalize_tex(source), source)

    def test_chain_result_annotations_and_conditional_prefixes_keep_their_roles(self):
        source = r'\begin{aligned}x=3\Rightarrow x^2-9 &= \\ 3^2-9 &= \\ 0 & \,{\color{green}{\checkmark}}\end{aligned}'
        expected = r'\begin{aligned}x=3\Rightarrow x^2-9 &= 3^2-9 \\ &= 0 && \,{\color{green}{\checkmark}}\end{aligned}'
        self.assertEqual(normalize_tex(source), expected)
        self.assertEqual(normalize_tex(expected), expected)
        validate_tex(expected)

    def test_preloaded_extensions_do_not_emit_unsupported_require(self):
        for extension, body in [('cancel', r'\cancel{2}'), ('enclose', r'\enclose{box}{x}')]:
            self.assertEqual(normalize_tex(r'\require{' + extension + '}' + body), body)
        self.assertEqual(normalize_tex(r'\require{other}x'), r'\require{other}x')
        with self.assertRaisesRegex(ValueError, 'Runtime TeX extension'):
            validate_tex(r'\require{cancel}\cancel{x}')
        with self.assertRaisesRegex(ValueError, 'Empty equation RHS'):
            validate_tex(r'\begin{aligned}a_1 &= \\ a_2 &=\end{aligned}')

    def test_empty_rhs_equation_chains_put_expressions_after_equals(self):
        source = r'\begin{aligned}(x^3)^2 &= \\ x^{3\cdot2} &= \\ x^6\end{aligned}'
        expected = r'\begin{aligned}(x^3)^2 &= x^{3\cdot2} \\ &= x^6\end{aligned}'
        self.assertEqual(normalize_tex(source), expected)
        self.assertEqual(normalize_tex(expected), expected)
        self.assertEqual(normalize_prose('Use $' + source + '$.'), 'Use $' + expected + '$.')
        legacy = '\\eqalign{(5^2)^3 &= \\\n5^{2\\cdot3} &= \\\n5^6}'
        self.assertEqual(normalize_tex(legacy), r'\begin{aligned}(5^2)^3 &= 5^{2\cdot3} \\ &= 5^6\end{aligned}')

    def test_equation_chain_spacing_labels_and_complete_equations_are_preserved(self):
        source = r'\eqalign{(5^2)^3 &= \\[5pt] \underbrace{5^2\cdot5^2\cdot5^2}_{3\text{ times}} &= \\[5pt] 5^6}'
        expected = r'\begin{aligned}(5^2)^3 &= \underbrace{5^2\cdot5^2\cdot5^2}_{3\text{ times}} \\[5pt] &= 5^6\end{aligned}'
        self.assertEqual(normalize_tex(source), expected)
        validate_tex(expected)
        for source in (r'\begin{aligned}x &= 1 \\ y &= 2\end{aligned}',
                       r'\begin{aligned}x &= y \\ &= z\end{aligned}'):
            self.assertEqual(normalize_tex(source), source)
        self.assertEqual(normalize_tex(r'\begin{aligned}a &= \\ b & \end{aligned}'),
                         r'\begin{aligned}a &= b\end{aligned}')

    def test_fraction_parentheses_scale_without_changing_inner_negative_bases(self):
        source = r'{(-\frac{2}{5})}^{2}={(\frac{(-2)}{5})}^{2}=\frac{(-2)^{2}}{{5}^{2}}'
        expected = r'{\left(-\frac{2}{5}\right)}^{2}={\left(\frac{(-2)}{5}\right)}^{2}=\frac{(-2)^{2}}{{5}^{2}}'
        self.assertEqual(normalize_tex(source), expected)
        self.assertEqual(normalize_tex(expected), expected)
        self.assertEqual(normalize_prose('Compute $' + source + '$.'), 'Compute $' + expected + '$.')
        validate_tex(expected)

    def test_fraction_parentheses_support_nested_groups_and_keep_explicit_sizes(self):
        for command in ('frac', 'dfrac', 'tfrac'):
            source = '( -\\' + command + r'{\frac{1}{2}}{(-3)^{2}} )^4'
            expected = '\\left( -\\' + command + r'{\frac{1}{2}}{(-3)^{2}} \right)^4'
            self.assertEqual(normalize_tex(source), expected)
        for source in (r'\left(-\dfrac{3}{2}\right)^3', r'\bigl(\frac{1}{2}\bigr)',
                       r'\big(\frac{1}{2})', r'(-2)^3', r'(4\div11)^3',
                       r'f(x)', r'\frac{(-2)^2}{5^2}', r'(\frac{1}{2}+x)',
                       r'(\frac{1}{2}', r'(\frac{1})', r'ordinary (prose)'):
            self.assertEqual(normalize_tex(source), source)

    def test_archived_svg_row_spacing_is_canonicalized_in_labels_and_spacing_formulas(self):
        for source in (r'\underset{\substack{\phantom{.} \[4pt] \uparrow \[6pt] I}}{x}',
                       r'\[6pt]', r'\ \[1ex]'):
            result = normalize_tex(source)
            self.assertEqual(normalize_tex(result), result)
            self.assertIn(r'\\[', result)
            validate_tex(result)
        with self.assertRaisesRegex(ValueError, 'Nested math delimiter'):
            validate_tex(r'x+\[y\]')

    def test_inline_legacy_matrix_with_single_backslash_newline_is_normalized(self):
        source = 'Use $\\left\\lbrack\\matrix{1 & 2 \\\n3 & 4}\\right\\rbrack$.'
        normalized = normalize_prose(source)
        self.assertIn(r'\begin{bmatrix}1 & 2 \\' + '\n3 & 4' + r'\end{bmatrix}', normalized)
        validate_prose(normalized)

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

    def test_reported_escaped_brace_system_has_two_rows_at_capture_boundary(self):
        # q 17592186529306: syntactically valid TeX used to render one flat line.
        broken = r'\{-3x - y = 8; 3x + y = -6'
        expected = r'\left\{\begin{aligned}-3x - y &=8 \\ 3x + y &=-6\end{aligned}\right.'
        self.assertEqual(legacy_system_rows(broken), ['-3x - y = 8', '3x + y = -6'])
        question = {'problem': 'Consider the following system:\n\n$' + broken + '$',
                    'answer_fields': [{'correct_value': 'No solutions', 'choices': [
                        {'type': 'text', 'value': 'No solutions'},
                        {'type': 'text', 'value': 'Infinitely many solutions'}]}]}
        original = copy.deepcopy(question)
        saved = normalize_capture_question(question)
        self.assertEqual(saved['problem'], 'Consider the following system:\n\n$' + expected + '$')
        self.assertEqual(saved['answer_fields'], original['answer_fields'])
        self.assertEqual(question, original)
        self.assertEqual(normalize_capture_question(saved), saved)
        # Structural TeX checks alone cannot detect this former failure.
        with self.assertRaisesRegex(ValueError, 'Flattened equation system'):
            validate_tex(broken)
        with self.assertRaisesRegex(ValueError, 'Flattened equation system'):
            validate_prose(question['problem'])
        validate_tex(expected)

    def test_flat_system_parser_preserves_groups_and_does_not_convert_sets(self):
        rows = [r'x=\frac{1}{2+\frac{3}{4}}', r'y=(a;b)', r'z=\text{a;b}']
        for opening in ('{', r'\{'):
            broken = opening + '; '.join(rows)
            self.assertEqual(legacy_system_rows(broken), rows)
            normalized = normalize_tex(broken)
            self.assertEqual(normalized, system_tex(rows))
            self.assertEqual(normalize_tex(normalized), normalized)
        untouched = [r'\{x=1;y=2\}', r'{x=1;y=2}',
                     r'\left\{x=1;y=2\right\}', r'\{x\in\mathbb{R};x>0',
                     r'\{x & x>0; 0 & x\leq0', r'\{x=1;',
                     r'\{x=(1; y=2', r'f(x)=\begin{cases}x & x>0 \\ 0 & x\leq0\end{cases}']
        for source in untouched:
            with self.subTest(source=source):
                self.assertIsNone(legacy_system_rows(source))
                self.assertEqual(normalize_tex(source), source)

    def test_equation_labels_require_explicit_evidence_and_keep_a_separate_column(self):
        # A formatter cannot infer whether 0(1) denotes multiplication or a label.
        broken = r'\{3x+y=0(1); x-2y=0(2)'
        self.assertEqual(legacy_system_rows(broken), ['3x+y=0(1)', 'x-2y=0(2)'])
        self.assertIn('0(1)', normalize_tex(broken))
        self.assertNotIn('&&', normalize_tex(broken))
        labeled = system_tex(['3x+y=0', 'x-2y=0'], annotations=['(1)', '(2)'])
        self.assertEqual(labeled, r'\left\{\begin{aligned}3x+y &=0 && (1) \\ x-2y &=0 && (2)\end{aligned}\right.')
        self.assertEqual(normalize_tex(labeled), labeled)
        operated = system_tex(['x+y=3', '2x-y=6'], annotations=[r'\mid\cdot(-2)', None])
        self.assertIn(r'x+y &=3 && \mid\cdot(-2)', operated)
        self.assertEqual(operated.count(r'\mid'), 1)
        self.assertEqual(normalize_tex(operated), operated)
        # Existing aligned systems need no incidental whitespace or empty-cell
        # rewrite when the formatter learns to recognize annotation columns.
        existing = r'\left\{\begin{aligned}x &= 1 && \\ y &= 2 && \mid\cdot(3)\end{aligned}\right.'
        self.assertEqual(normalize_tex(existing), existing)
        for annotations in (['(1)'], ['(1)', '(2)', '(3)'], ['$1$', ''], ['a & b', '']):
            with self.subTest(annotations=annotations), self.assertRaises(ValueError):
                system_tex(['x=1', 'y=2'], annotations=annotations)

    def test_whole_equation_multiplication_stays_inside_one_alignment_cell(self):
        # These source rows multiply a whole equality, not only its RHS.
        for first in (r'(-8a + 4b = 5)\cdot (3)', r'\left(-8a + 4b = 5\right)\cdot (3)'):
            rows = [first, '-2a - 12b = 5']
            expected = r'\left\{\begin{aligned}&' + first + r' \\ &-2a - 12b = 5\end{aligned}\right.'
            with self.subTest(first=first):
                self.assertEqual(system_tex(rows), expected)
                self.assertEqual(normalize_tex(r'\{' + '; '.join(rows)), expected)
                self.assertEqual(normalize_tex(expected), expected)
                self.assertIn(first, expected)
                self.assertNotIn('&=', expected)
                validate_tex(expected)

    def test_generator_rejects_flat_system_even_when_tex_groups_are_balanced(self):
        record = {'question': {':question/problem': r'$\{x+y=3; 2x-y=6$',
                               ':question/worked-solution': '$x=3$'}}
        with self.assertRaisesRegex(ValueError, 'Flattened equation system'):
            validate_generated_record(record)
        record['question'][':question/problem'] = normalize_prose(record['question'][':question/problem'])
        validate_generated_record(record)

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

    def test_legacy_row_spacing_keeps_all_gradient_derivation_rows(self):
        # Tutorial 2524's saved SVG title encodes each break as <span>\</span>.
        old = (r'\eqalign{\nabla f(x,y,z) &= \langle f_x, \: f_y, \:f_z\rangle \[5pt]'
               r'&= \dfrac12\langle2x, \: 2y, \: 2z\rangle\[5pt]'
               r'&= \langle x, \: y, \: z\rangle\[10pt]'
               r'\nabla f(0,0,1) &= \langle 0,\: 0,\: 1 \rangle.}')
        normalized = normalize_tex(old)
        self.assertEqual(normalized.count(r'\\[5pt]'), 2)
        self.assertEqual(normalized.count(r'\\[10pt]'), 1)
        self.assertIn(r'\nabla f(0,0,1)', normalized)
        validate_tex(normalized)
        self.assertEqual(normalize_tex(normalized), normalized)
        for bad in (r'\begin{aligned}a&=1\[5pt]b&=2\end{aligned}',
                    r'\eqalign{a&=1\[x+y\]}', r'\eqalign{a&=\(x\)}'):
            with self.subTest(source=bad), self.assertRaises(ValueError):
                validate_tex(normalize_tex(bad))

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

    def test_preloaded_boldsymbol_requires_no_runtime_extension(self):
        value = normalize_tex(r'\require{boldsymbol}\boldsymbol{\alpha}')
        self.assertEqual(value, r'\boldsymbol{\alpha}')
        validate_tex(value)

    def test_generator_checks_duplicate_controls_and_checkbox_statement_math(self):
        record = {'question': {':question/problem': '$x$', ':question/worked-solution': '$x$',
                               ':question/answer-fields': [
                                   {':answer-field/key': 'selection', ':answer-field/choices': []},
                                   {':answer-field/key': 'selection', ':answer-field/choices': []}]}}
        with self.assertRaisesRegex(ValueError, 'unique'): validate_generated_record(record)
        field = {':answer-field/key': r'$lim_{x\to0}x=0$',
                 ':answer-field/type': ':answer-field.type/checkbox', ':answer-field/choices': []}
        record['question'][':question/answer-fields'] = [field]
        with self.assertRaisesRegex(ValueError, 'Noncanonical|limit operator'): validate_generated_record(record)
        field[':answer-field/key'] = normalize_prose(field[':answer-field/key'])
        self.assertIs(validate_generated_record(record), record)

    def test_generator_contract_rejects_noncanonical_output(self):
        record = {'question': {':question/problem': '$x$', ':question/worked-solution': '$x$',
                               ':question/answer-fields': [{':answer-field/choices': [{':answer/type': ':answer.type/math', ':answer/value': '$x$'}]}]}}
        with self.assertRaises(ValueError): validate_generated_record(record)
        record['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'] = 'x'
        self.assertEqual(validate_generated_record(record)['generation']['math_format'], 'course-academy-tex-v1')

if __name__ == '__main__': unittest.main()
