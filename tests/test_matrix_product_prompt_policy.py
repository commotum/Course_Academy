import copy,json,unittest
from pathlib import Path
from generate.matrix_product_prompt_policy import KP,SUPPLIED_ENTRIES_KP,validate_delivery_batch
from scripts.generator_publish import prepare_records
ROOT=Path(__file__).resolve().parents[1]
H=ROOT/'reference/edb-math/repairs/2026-10-27-matrix-product-recognition'

class MatrixPromptPolicyTests(unittest.TestCase):
    def setUp(self):self.rows=json.loads((H/'candidate-pool.json').read_text())

    def test_partial_matrices_remain_valid(self):
        validate_delivery_batch(self.rows,KP)
        for r in self.rows:
            self.assertEqual(len(r['question'][':question/answer-fields']),3)
            self.assertEqual(r['question'][':question/problem'].count('<td>$'),6)

    def test_original_question_is_rejected(self):
        q=next(q for q in json.loads((H/'before.json').read_text())[':knowledge-point/questions'] if q[':db/id']==17592186695793)
        with self.assertRaisesRegex(ValueError,'process'):validate_delivery_batch([{'question':q}],KP)

    def test_process_reminder_is_rejected_without_worked_expression(self):
        r=copy.deepcopy(self.rows[0]);r['question'][':question/problem']+=' Use each row of A and column of B.'
        with self.assertRaisesRegex(ValueError,'process'):validate_delivery_batch([r],KP)

    def test_worked_expression_is_rejected_without_process_reminder(self):
        r=copy.deepcopy(self.rows[0]);r['question'][':question/problem']+=r' Calculate $0\cdot(-3)+2\cdot4$.'
        with self.assertRaisesRegex(ValueError,'entry calculation'):validate_delivery_batch([r],KP)

    def test_publisher_checks_the_delivered_prompt(self):
        r=copy.deepcopy(self.rows[0]);r['question'][':question/problem']+=' Hint: use a row of A.'
        with self.assertRaisesRegex(ValueError,'process'):
            prepare_records([r],KP,r['knowledge_point']['id'],set(),ROOT,ROOT,localizer=lambda r,*args:r)

    def test_target_positions_are_allowed(self):
        r=copy.deepcopy(self.rows[0]);r['question'][':question/problem']+=' Find the entry in row 2, column 3.'
        validate_delivery_batch([r],KP)

    def test_other_kps_are_unaffected(self):validate_delivery_batch([{}],KP+1)

class SuppliedMatrixEntriesTests(unittest.TestCase):
    def setUp(self):
        self.h=ROOT/'reference/edb-math/repairs/2026-10-29-matrix-supplied-entries'
        self.records=json.loads((self.h/'fresh-samples.json').read_text())

    def test_source_style_numerical_cells_pass(self):
        validate_delivery_batch(self.records,SUPPLIED_ENTRIES_KP)

    def test_original_asterisk_layout_fails(self):
        q=next(q for q in json.loads((self.h/'before.json').read_text())[':knowledge-point/questions'] if q[':db/id']==17592186717716)
        with self.assertRaisesRegex(ValueError,'actual unrequested entries'):
            validate_delivery_batch([{'question':q}],SUPPLIED_ENTRIES_KP)

    def test_asterisk_without_legend_fails(self):
        for marker in (r'$\ast$',r'$\star$','*'):
            with self.subTest(marker=marker),self.assertRaises(ValueError):
                validate_delivery_batch([{'question':{':question/problem':'<td>'+marker+'</td>'}}],SUPPLIED_ENTRIES_KP)

    def test_publisher_rejects_marker_even_without_metadata(self):
        r=copy.deepcopy(self.records[0]);r.pop('generation');r['question'][':question/problem']+='<td>$\\ast$</td>'
        with self.assertRaisesRegex(ValueError,'actual unrequested entries'):
            prepare_records([r],SUPPLIED_ENTRIES_KP,r['knowledge_point']['id'],set(),ROOT,ROOT,localizer=lambda r,*args:r)

if __name__=='__main__':unittest.main()
