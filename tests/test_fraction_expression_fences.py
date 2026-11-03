import unittest
from pathlib import Path
from types import SimpleNamespace
from scripts.question_capture.math_format import scalable_fraction_parentheses as fix,validate_tex,validate_math_structure
from scripts.generator_publish import localize_record

class FractionExpressionFenceTests(unittest.TestCase):
    def test_mixed_function_arguments_and_vector_components(self):
        source=r'⟨6\cos(5\cdot\frac{\pi}{3}),(6\cdot\frac12),\frac34⟩'
        # The capture's explicit fraction groups establish complete TeX atoms.
        source=source.replace(r'\frac12',r'\frac{1}{2}').replace(r'\frac34',r'\frac{3}{4}')
        result=fix(source)
        self.assertIn(r'\cos\left(5\cdot\frac{\pi}{3}\right)',result)
        self.assertIn(r'\left(6\cdot\frac{1}{2}\right)',result)
        self.assertTrue(result.startswith(r'\left\langle '));self.assertIn(r'\right\rangle',result)
        self.assertEqual(fix(result),result);validate_tex(result)

    def test_other_balanced_fences_and_nested_groups(self):
        for source in (r'[x+\frac{1}{2}]',r'\langle x,\frac{1}{2}\rangle',r'((x+\frac{1}{2}))'):
            result=fix(source);self.assertNotEqual(result,source);self.assertEqual(fix(result),result);validate_tex(result)

    def test_scripts_annotations_indices_and_manual_sizes_keep_their_scope(self):
        for source in (r'(x^{\frac{1}{2}})',r'(x_{\frac{1}{2}})',
                       r'\sqrt[\frac{1}{2}]{x}',r'\text{(\frac{1}{2})}',
                       r'(\underset{\frac{1}{2}}{x})',r'\bigl(x+\frac{1}{2}\bigr)',
                       r'\left(x+\frac{1}{2}\right)',r'(\frac{1})',r'(x+\frac{1}{2}',r'(0,\frac{1}{2}]'):
            self.assertEqual(fix(source),source,source)
        self.assertEqual(fix(r'x^{(1+\frac{1}{2})}'),r'x^{\left(1+\frac{1}{2}\right)}')

    def test_alignment_cells_and_conditional_bars(self):
        source=r'\begin{aligned}(x&=\frac{1}{2})\end{aligned}'
        self.assertEqual(fix(source),source)
        self.assertEqual(fix(r'P(A|\frac{1}{2})'),r'P\left(A|\frac{1}{2}\right)')

    def test_publication_repairs_old_bundled_helpers_before_identities(self):
        q={':question/problem':r'Compute $f(5\cdot\frac{\pi}{3})$.',
           ':question/worked-solution':r'$\langle x,\frac{1}{2}\rangle$',
           ':question/answer-fields':[{':answer-field/type':':answer-field.type/radio',':answer-field/key':'selection',
               ':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':r'⟨3,\frac{3}{4}⟩'}]}]}
        result=localize_record({'question':q},Path('/tmp'),Path('/tmp'),library=SimpleNamespace(text=lambda x:x,saved={}))['question']
        self.assertIn(r'\left(5\cdot\frac{\pi}{3}\right)',result[':question/problem'])
        self.assertIn(r'\left\langle',result[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])
        with self.assertRaisesRegex(ValueError,'scalable fences'):validate_math_structure(q[':question/problem'])
        validate_math_structure(result[':question/problem'])

if __name__=='__main__':unittest.main()
