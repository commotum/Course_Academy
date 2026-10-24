"""Linear-trig hard means negative inner derivative, not accumulated arithmetic."""
import copy
import unittest
from tests.test_trig_substitution_models import load_model,evidence
from scripts.trig_substitution_batch_policy import validate_delivery_batch


class LinearTrigGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.g=load_model()

    def test_all_full_linear_bands_keep_small_integer_coefficients(self):
        kp=17592186068915
        for band in('moderate','hard'):
            rows=self.g.batch(kp,band,8,31,evidence=evidence(kp))
            validate_delivery_batch(rows,kp)
            for row in rows:
                p=row['generation']['parameters'];a=self.g.s.Rational(p['slope']);A=self.g.s.Rational(p['amplitude'])
                self.assertEqual(a.q,1);self.assertEqual(A.q,1)
                self.assertLessEqual(abs(a),4);self.assertLessEqual(A,4)
                self.assertEqual(a<0,band=='hard')
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


if __name__=='__main__':unittest.main()
