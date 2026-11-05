"""Preserve substitution work without banning source-valid simple cases."""
import copy
import unittest
from tests.test_trig_substitution_models import load_model,evidence
from scripts.trig_substitution_batch_policy import validate_delivery_batch


class LinearTrigGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.g=load_model()

    def test_full_linear_bands_keep_one_bounded_scaling_operation(self):
        kp=17592186068915
        for band in('moderate','hard'):
            rows=self.g.batch(kp,band,8,31,evidence=evidence(kp))
            validate_delivery_batch(rows,kp)
            for row in rows:
                p=row['generation']['parameters'];a=self.g.s.Rational(p['slope']);A=self.g.s.Rational(p['amplitude'])
                self.assertIn(a.q,(1,2,3));self.assertEqual(A.q,1)
                self.assertLessEqual(abs(a),4);self.assertLessEqual(A,4)
                if row['generation']['model']['lower']is not None:
                    self.assertNotIn(r'\sqrt',row['question'][':question/problem'])

    def test_old_compound_hard_template_and_fractional_override_are_not_supported(self):
        kp=17592186068915
        with self.assertRaises(ValueError):
            self.g.generate(kp,'hard',0,'compound_sin_positive',evidence=evidence(kp))
        row=self.g.batch(kp,'hard',1,0,evidence=evidence(kp))[0]
        row=copy.deepcopy(row);row['generation']['parameters']['slope']='4/3';row['generation']['parameters']['amplitude']='3/4'
        with self.assertRaisesRegex(ValueError,'fractional amplitude'):validate_delivery_batch([row],kp)

    def test_whole_antiderivative_has_external_constant_support(self):
        kp=17592186068915
        row=self.g.generate(kp,'moderate',7,'indef_sin',evidence=evidence(kp))
        key=row['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
        self.assertIn('{{answer}} $+C$',row['question'][':question/problem'])
        self.assertNotIn('+C',key)

    def test_canonical_fractional_slope_is_reachable_on_ordinary_path(self):
        kp=17592186068915
        row=self.g.generate(kp,'moderate',28,'indef_sin',evidence=evidence(kp))
        self.assertEqual(row['generation']['parameters'],{'slope':'1/3','shift':'0','amplitude':'2'})
        validate_delivery_batch([row],kp)
        m=row['generation']['model'];s=self.g.s;x=self.g.X
        primitive=s.sympify(m['primitive'],locals={'x':x})
        self.assertEqual(s.trigsimp(s.diff(primitive,x)-2*s.sin(x/3)),0)

    def test_zero_result_survives_all_bands_and_collapsed_bank_uses_exact_entry(self):
        kp=17592186068915
        for band,seed in [('easy',7),('moderate',3),('hard',0)]:
            row=self.g.generate(kp,band,seed,'def_cos',evidence=evidence(kp))
            validate_delivery_batch([row],kp)
            m=row['generation']['model'];s=self.g.s;x=self.g.X
            primitive=s.sympify(m['primitive'],locals={'x':x})
            self.assertEqual(s.simplify(primitive.subs(x,s.sympify(m['upper']))-primitive.subs(x,s.sympify(m['lower']))),0)
            self.assertEqual(m['result'],'0')
            self.assertFalse(row['generation']['provided_substitution'])
            self.assertEqual(row['question'][':question/answer-fields'][0][':answer-field/type'],':answer-field.type/blank')
        outcomes={self.g.generate(kp,'moderate',seed,'def_cos',evidence=evidence(kp))['generation']['model']['result']for seed in range(8)}
        self.assertIn('0',outcomes)
        self.assertGreater(len(outcomes),1,'The family must not always give zero')

    def test_hard_is_not_defined_by_a_negative_sign(self):
        kp=17592186068915
        rows=self.g.batch(kp,'hard',8,31,evidence=evidence(kp))
        self.assertEqual({self.g.s.Rational(r['generation']['parameters']['slope'])>0 for r in rows},{True,False})
        validate_delivery_batch(rows,kp)


if __name__=='__main__':unittest.main()
