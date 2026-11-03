import importlib.util
from pathlib import Path
import sys
import unittest
from bs4 import BeautifulSoup
from scripts.question_capture.math_format import (
    normalize_inverse_trig_operators as fix, normalize_prose, normalize_tex,
    validate_math_structure, normalize_function_operators,
)
from capture.scripts.database.math_content import question as normalize_import

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from import_historical_question_content import Renderer


class InverseOperatorNotationTests(unittest.TestCase):
    def test_missing_and_unsupported_legacy_operators(self):
        for source in ('arccscx',r'\arccscx',r'arccsc\,x',r'\arccsc x'):
            result=fix(source)
            self.assertIn(r'\operatorname{arccsc}',result)
            self.assertEqual(fix(result),result)
        self.assertIn(r'\operatorname{arcsec}',fix(r'{arcsec}^{2}x'))
        self.assertIn(r'\operatorname{arccot}',fix(r'\textrm {arccot } x'))

    def test_adjacent_factor_and_power_scope(self):
        result=fix(r'\operatorname{ln}⁡xarccot{x}^{3}')
        self.assertEqual(result,r'\operatorname{ln}⁡x\operatorname{arccot} {x}^{3}')
        self.assertEqual(fix(r'\arccot^{2}x'),r'\operatorname{arccot} ^{2}x')

    def test_existing_operators_literal_text_and_identifiers_are_preserved(self):
        for source in (r'\operatorname{arccot}x',r'\operatorname{xarccot}x',
                       r'\text{arccot x is a function}',r'\text{arccotangent}',
                       'arcsection','varccotx',r'\arcsection x',r'\text{an {arccot} label}'):
            self.assertEqual(fix(source),source)

    def test_math_only_prose_and_answer_imports(self):
        self.assertEqual(normalize_prose('The arccsc function is $-7arccscx$.'),
                         r'The arccsc function is $-7\operatorname{arccsc} x$.')
        q={'problem':'Find $arccotx$.','worked_solution':'Use $arccotx$.','answer_fields':[
            {'type':'blank','correct_type':'math','correct_value':'arccotx',
             'choices':[{'type':'math','value':'arccotx'}]}]}
        normalize_import(q)
        self.assertEqual(q['answer_fields'][0]['correct_value'],r'\operatorname{arccot} x')
        with self.assertRaisesRegex(ValueError,'operator notation'):
            validate_math_structure('$arccotx$')
        validate_math_structure(normalize_prose('$arccotx$'))

    def test_mathml_node_boundary_without_application_marker(self):
        for name in ('arcsec','arccsc','arccot'):
            renderer=Renderer(1721)
            node=BeautifulSoup('<math><mi>'+name+'</mi><mi>x</mi></math>','html.parser').math
            self.assertEqual(renderer.m(node),'\\operatorname{'+name+'} x')
            self.assertEqual(renderer.errors,[])
        renderer=Renderer(1721)
        node=BeautifulSoup('<mi>xarccot</mi>','html.parser').mi
        self.assertEqual(renderer.m(node),'xarccot')

    def test_other_operator_losses_keep_factors_domains_and_powers(self):
        cases={
            'xln⁡x':r'x\ln ⁡x',
            '{sin}^{2}⁡x':r'{\sin }^{2}⁡x',
            'det(A)':r'\det (A)',
            'max(|x|,|y|)':r'\max (|x|,|y|)',
            'xmod2':r'x\bmod 2',
            r'\siny':r'\sin y',
            r'arsech(x)':r'\operatorname{arsech} (x)',
            'rcis(θ)':r'r\operatorname{cis} (θ)',
        }
        for source,expected in cases.items():
            self.assertEqual(normalize_function_operators(source),expected)
            self.assertEqual(normalize_function_operators(expected),expected)
        for unchanged in (r'\coth x',r'\sech x',r'\csch x',r'\text{min}',r'\lambda_{min}',
                          'log10(x)','atan2(y,x)','maximum','model','xlnvalue',r'\text{sin(x)}'):
            self.assertEqual(normalize_function_operators(unchanged),unchanged)


if __name__=='__main__':unittest.main()
