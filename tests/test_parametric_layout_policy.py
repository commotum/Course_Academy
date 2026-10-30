import json,unittest
from pathlib import Path
from generate.parametric_layout_policy import TABLE_KP,TRIG_KP,validate_delivery_batch
H=Path(__file__).resolve().parents[1]/'reference/edb-math/repairs/2026-10-30-parametric-other-kps'

class ParametricLayoutPolicyTests(unittest.TestCase):
    def test_repaired_table_pool_passes(self):validate_delivery_batch(json.loads((H/str(TABLE_KP)/'candidate-pool.json').read_text()),TABLE_KP)
    def test_repaired_trig_pool_passes(self):validate_delivery_batch(json.loads((H/str(TRIG_KP)/'candidate-pool.json').read_text()),TRIG_KP)
    def test_wide_table_fails(self):
        q={':question/problem':'| t | -2 | -1 | 0 | 1 | 2 |',':question/worked-solution':'Done.'}
        with self.assertRaisesRegex(ValueError,'small panels'):validate_delivery_batch([{'question':q}],TABLE_KP)
    def test_grouped_formulas_fail(self):
        q={':question/problem':'$$\\begin{gathered}x=3\\cos\\theta,\\quad y=2\\sin\\theta\\end{gathered}$$'}
        with self.assertRaisesRegex(ValueError,'independently'):validate_delivery_batch([{'question':q}],TRIG_KP)
    def test_other_kps_unaffected(self):validate_delivery_batch([{}],17592186087722)

if __name__=='__main__':unittest.main()
