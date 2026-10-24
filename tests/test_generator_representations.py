"""Value-preserving repairs must also preserve a readable instructional path."""
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_generator_representations import calls, candidates


def load(path, name):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vector = load(ROOT / 'generate/scratch/17592186124470.py', 'vector_representation')
        cls.ratio = load(ROOT / 'generate/scratch/17592186198361.py', 'ratio_representation')
        cls.product = load(ROOT / 'reference/edb-math/repairs/2026-10-23-representation-audit/product-log-package/generator.py', 'product_representation')

    def test_scanner_reads_bare_and_parenthesized_source_arguments(self):
        self.assertEqual(calls(r'\operatorname{sin}⁡u+\cos(v)'), [('sin', 'u'), ('cos', 'v')])
        self.assertEqual(calls(r'\sin^{2}(12-2x)'), [('sin', '12-2x')])
        self.assertEqual(calls(r'\sin 2t'), [('sin', '2t')])
        self.assertEqual(calls(r'\cos{\left((t+1)^2\right)}'), [('cos', '(t+1)^2')])

    def test_candidate_scanner_does_not_certify_equivalence(self):
        e = {'1': {'question/problem': ['Differentiate cos(12-2x).'],
                   'question/worked-solution': [r'2\sin(12-2x)'], 'question/answer-fields': [2]},
             '2': {'answer-field/correct': [3]}, '3': {'answer/value': [r'-2\sin(2x-12)']}}
        self.assertEqual(candidates(e)['candidate_count'], 1)
        e['3']['answer/value'] = [r'2\sin(12-2x)']
        self.assertEqual(candidates(e)['candidate_count'], 0)

    def test_translated_vector_chain_rule_keeps_the_inner_square(self):
        g = self.vector
        for c in (-2, 3):
            for h in (-2, 0, 1, 2):
                with self.subTest(c=c, h=h):
                    record = g.generate('hard', 83, template='exponential_cosine', parameters={'c':c,'h':h})
                    q = record['question']; f = q[':question/answer-fields'][0]
                    key = next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
                    self.assertEqual(key, g.final_solution_value(q[':question/worked-solution']))
                    raw_f, raw_r = g.prompt_parts(q)
                    curve = [g.read_scalar(v) for v in g.vector_parts(raw_r)]
                    composition = g.read_scalar(raw_f).subs(dict(zip(g.VARS,curve)), simultaneous=True)
                    self.assertTrue(g.equal(g.read_scalar(key), g.sp.diff(composition,g.T)))
                    allowed = set(calls(q[':question/worked-solution']))
                    for answer in f[':answer-field/choices']:
                        self.assertTrue(set(calls(answer[':answer/value'])).issubset(allowed))

    def test_log_evaluations_share_the_solution_endpoint_for_every_bound_family(self):
        g = self.ratio
        for power, template in [(1, 'ratio_product'), (2, 'ratio_product_squared')]:
            for upper in (4, 9, 16):
                p = {'ul':1,'uh':upper,'vl':2,'vh':5}
                values, correct, recipes = g.bank(template,p,'authored')
                self.assertEqual(values[correct], g.ratio_chain(p,power)[1])
                expected = g.sp.Rational(5**(power+1)-2**(power+1),3*(power+1))*g.sp.log(upper)
                actual = g.integrate_rectangle(recipes[correct][1],p)
                self.assertEqual(g.sp.simplify(actual-expected),0)

    def test_logarithm_bases_survive_radio_and_blank_rendering(self):
        g = self.product
        for template in ('power_log_radio','cos_log_radio','log_log_radio','base_log_left_blank','tan_log_blank'):
            p = g.defaults(template)
            for seed in (13, 37):
                record = g.generate('easy', seed, template=template, parameters=p,
                                    target='left' if not template.endswith('radio') else None)
                f = record['question'][':question/answer-fields'][0]
                for answer in f[':answer-field/choices']:
                    self.assertNotIn(r'\ln_{',answer[':answer/value'])
                    if '\\ln{\\left(x' in answer[':answer/value']:
                        self.fail('Natural-log canonicalization leaked into a source-base contribution')
                key = next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
                self.assertIn(r'\log_{',key)


if __name__ == '__main__':
    unittest.main()
