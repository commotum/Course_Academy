"""Regressions for source-number coupling, hidden prerequisites, and degenerate banks."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'generate'))
from inverse_trig import Generator


class InverseTrigGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)

    def generator(self,kind):
        p = Path(self.temp.name)/(kind+'.json')
        p.write_text(json.dumps({'kind':kind,'kp_id':123,'kp_uuid':'227abe29-6e31-5afd-b0ca-3b8ed7d8c287','title':'Integration',
            'excluded_task_fingerprints':[],'anchors':{b:['e-471'] for b in ('easy','moderate','hard')},
            'basis':1,'lineage':'test','band_contract':{b:'test' for b in ('easy','moderate','hard')},'originals':[]}))
        return Generator(p)

    def test_unit_numerator_tangent_family_varies_its_substitution(self):
        g = self.generator('tangent');rows = [g.generate('moderate',s,'unit-numerator') for s in range(12)]
        self.assertEqual({r['generation']['parameters']['N'] for r in rows},{'1'})
        self.assertGreater(len({r['generation']['parameters']['A'] for r in rows}),4)
        self.assertGreater(len({r['question'][':question/problem'] for r in rows}),4)

    def test_sine_numerator_does_not_change_when_inner_factor_changes(self):
        g = self.generator('sine');p = dict(family='sine',A=1,B=9,N=3,D=1,lower_u=None,upper_u=None)
        a = g.build('easy','integer-inner',p);p['B']=25;b = g.build('easy','integer-inner',p)
        self.assertEqual(a['generation']['parameters']['N'],b['generation']['parameters']['N'])
        self.assertNotEqual(a['question'][':question/problem'],b['question'][':question/problem'])
        self.assertNotEqual(a['question'][':question/worked-solution'],b['question'][':question/worked-solution'])
        self.assertNotEqual(a['question'][':question/answer-fields'][0][':answer-field/correct'],b['question'][':question/answer-fields'][0][':answer-field/correct'])

    def test_singular_endpoints_and_easy_work_relabelled_hard_are_rejected(self):
        g = self.generator('definite');p = dict(family='sine',A=9,B=2,N=4,D=1,lower_u=-1,upper_u=1)
        with self.assertRaisesRegex(ValueError,'improper'):g.build('hard','sine-cross-zero',p,response='blank')
        p.update(A=1,lower_u='1/2',upper_u='sqrt(2)/2')
        with self.assertRaisesRegex(ValueError,'Hard requires'):g.build('hard','sine-two-positive',p,response='blank')

    def test_secant_normalization_is_visible_on_both_domain_components(self):
        g = self.generator('secant');p = dict(family='secant',A=1,B=7,N=3,D=1,lower_u=None,upper_u=None)
        r = g.build('hard','radical-normalization',p)
        self.assertIn(r'\frac{\sqrt{7}}{|u|}',r['question'][':question/worked-solution'])
        self.assertIn('either interval',r['question'][':question/worked-solution'])

    def test_inapplicable_endpoint_banks_fail_before_sampling(self):
        g = self.generator('definite')
        for band,case in [('easy','tangent-special'),('hard','tangent-two-positive')]:
            with self.assertRaisesRegex(ValueError,'inapplicable'):
                g.generate(band,17,case,bank_profile='endpoint-and-factor')

    def test_option_reordering_preserves_identity_and_key(self):
        g = self.generator('tangent');p = dict(family='tangent',A=1,B=25,N=3,D=1,lower_u=None,upper_u=None)
        a = g.build('easy','integer-inner',p,seed=1)['question'];b = g.build('easy','integer-inner',p,seed=4)['question']
        self.assertEqual(a[':question/id'],b[':question/id'])
        fa,fb = (r[':question/answer-fields'][0] for r in (a,b))
        self.assertEqual(fa[':answer-field/correct'],fb[':answer-field/correct'])
        position = lambda f:next(i for i,x in enumerate(f[':answer-field/choices']) if x[':answer/id']==f[':answer-field/correct'][1])
        self.assertEqual((position(fa),position(fb)),(1,4))


if __name__ == '__main__':unittest.main()
