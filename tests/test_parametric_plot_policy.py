import copy,json,unittest
from pathlib import Path
from generate.parametric_plot_policy import KP,plot_plan,UnreadableBank,validate_delivery_batch
ROOT=Path(__file__).resolve().parents[1]
H=ROOT/'reference/edb-math/repairs/2026-10-30-parametric-plot-readability'

class ParametricPlotPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.pool=json.loads((H/'candidate-pool.json').read_text())

    def test_repaired_complete_banks_pass(self):validate_delivery_batch(self.pool,KP)

    def test_reported_five_checkpoints_are_visible_on_unit_grid(self):
        old=json.loads((ROOT/'reference/edb-math/audits/2026-10-30-parametric-plot-readability/reported-generation.json').read_text())
        plan=plot_plan(old['generation']['plots'],[-2,-1,0,1,2])
        self.assertEqual(plan['checkpoints'][0],[[7,-8],[2,-4],[-1,-2],[-2,-2],[-1,-4]])
        self.assertEqual(plan['minor_step'],1);self.assertEqual(plan['major_step'],2)

    def test_target_selection_cannot_change_the_scale(self):
        r=self.pool[0];plan=plot_plan(r['generation']['bank'],r['generation']['ts'])
        for role in range(5):
            changed=copy.deepcopy(r['generation']);changed['role']=role
            self.assertEqual(plot_plan(changed['bank'],changed['ts']),plan)

    def test_oversized_bank_is_rejected(self):
        bank=copy.deepcopy(self.pool[0]['generation']['bank'])
        for shape in bank:shape['x']='100*('+shape['x']+')'
        with self.assertRaisesRegex(UnreadableBank,'grid is too small'):plot_plan(bank,self.pool[0]['generation']['ts'])

    def test_indistinguishable_curves_are_rejected(self):
        bank=copy.deepcopy(self.pool[0]['generation']['bank']);bank[1]=copy.deepcopy(bank[0]);bank[1]['x']='('+bank[0]['x']+')+0.001'
        with self.assertRaisesRegex(UnreadableBank,'distinguished'):plot_plan(bank,self.pool[0]['generation']['ts'])

    def test_stale_renderer_is_rejected(self):
        r=copy.deepcopy(self.pool[0]);r['generation']['version']='parametric-graphs-2'
        with self.assertRaisesRegex(ValueError,'repaired'):validate_delivery_batch([r],KP)

    def test_changed_scale_metadata_is_rejected(self):
        r=copy.deepcopy(self.pool[0]);r['generation']['plot_plan']['minor_step']=3
        with self.assertRaisesRegex(ValueError,'metadata'):validate_delivery_batch([r],KP)

    def test_swapped_answer_key_is_rejected(self):
        r=copy.deepcopy(self.pool[0]);field=r['question'][':question/answer-fields'][0]
        field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in field[':answer-field/choices'] if a[':answer/id']!=field[':answer-field/correct'][1])]
        with self.assertRaisesRegex(ValueError,'key disagrees'):validate_delivery_batch([r],KP)

    def test_other_kps_are_unaffected(self):validate_delivery_batch([{}],KP+1)

if __name__=='__main__':unittest.main()
