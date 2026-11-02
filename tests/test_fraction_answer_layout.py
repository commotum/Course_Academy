import json,re,tempfile,unittest
from pathlib import Path
from scripts.question_capture.math_format import normalize_fraction_answer_tables,normalize_prose
from capture.scripts.database.text import markdown
from scripts.generator_publish import localize_record

ROOT=Path(__file__).resolve().parents[1]
H=ROOT/'reference/edb-math/repairs/2026-11-01-reciprocal-derivative-fractions/17592186119939'

class FractionAnswerLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.questions={q[':db/id']:q for q in json.loads((H/'before.json').read_text())[':knowledge-point/questions']}
    def test_reported_denominator_control_stays_in_denominator(self):
        text=normalize_prose(self.questions[17592186315109][':question/problem'])
        self.assertIn('answer-fraction-numerator">${y}^{3}$',text)
        self.assertIn('answer-fraction-denominator">{{field-1}}',text)
        self.assertNotIn('| ---',text)
        self.assertEqual(normalize_prose(text),text)
    def test_two_control_positions_and_fixed_addend_survive(self):
        text=normalize_prose(self.questions[17592186233915][':question/problem'])
        self.assertIn('answer-fraction-numerator">{{field-1}}',text)
        self.assertIn('answer-fraction-denominator">$2\\sqrt{y}\\,+${{field-2}}',text)
        self.assertEqual(re.findall(r'\{\{field-\d+\}\}',text),['{{field-1}}','{{field-2}}'])
    def test_legacy_html_converter_reproduces_and_repairs_styled_source_layout(self):
        source='<table><tr><td>$\\text{d}y$</td><td>$=$</td><td style="border-bottom:1px solid">$y^3$</td></tr><tr><td>$\\text{d}x$</td><td></td><td>{{field-1}}</td></tr></table>'
        result=markdown(source)
        self.assertIn('answer-fraction-numerator">$y^3$',result)
        self.assertIn('answer-fraction-denominator">{{field-1}}',result)
        self.assertEqual(markdown(result),result)
    def test_ordinary_data_table_is_unchanged(self):
        source='| t | x | y |\n| --- | --- | --- |\n| 1 | 2 | {{field-1}} |'
        self.assertEqual(normalize_fraction_answer_tables(source),source)
    def test_longer_derivative_table_is_not_guessed(self):
        source='| $dy$ | $=$ | $y^3$ |\n| --- | --- | --- |\n| $dx$ | | {{field-1}} |\n| extra | | data |'
        self.assertEqual(normalize_fraction_answer_tables(source),source)
    def test_code_examples_are_unchanged(self):
        source='```\n'+self.questions[17592186315109][':question/problem']+'\n```'
        self.assertEqual(normalize_fraction_answer_tables(source),source)
    def test_generator_delivery_also_repairs_old_table_markup(self):
        q=self.questions[17592186315109]
        with tempfile.TemporaryDirectory() as d:result=localize_record({'question':q},Path(d),Path(d))
        self.assertIn('answer-fraction',result['question'][':question/problem'])
        self.assertEqual(result['question'][':question/answer-fields'],q[':question/answer-fields'])

if __name__=='__main__':unittest.main()
