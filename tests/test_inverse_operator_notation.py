import importlib.util
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from bs4 import BeautifulSoup
from scripts.question_capture.math_format import (
    normalize_inverse_trig_operators as fix, normalize_prose, normalize_tex,
    validate_math_structure, normalize_function_operators,
)
from capture.scripts.database.math_content import question as normalize_import
from capture.scripts.database.prepare import choice_signature

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
            r'\sech x':r'\operatorname{sech}  x',
            r'\csch x':r'\operatorname{csch}  x',
            '$ln$':r'$\ln $',
        }
        for source,expected in cases.items():
            self.assertEqual(normalize_function_operators(source),expected)
            self.assertEqual(normalize_function_operators(expected),expected)
        for unchanged in (r'\coth x',r'6\div4',r'a\mod n',r'\text{min}',r'\lambda_{min}',
                          'log10(x)','atan2(y,x)','maximum','model','xlnvalue',r'\text{sin(x)}'):
            self.assertEqual(normalize_function_operators(unchanged),unchanged)

    def test_reimport_matches_operator_aliases_without_merging_arguments(self):
        for left,right in ((r'\sin x',r'\operatorname{sin}x'),
                           ('xln⁡x',r'x\ln x'),
                           (r'\arccscx',r'\operatorname{arccsc}x')):
            self.assertEqual(choice_signature('math',left),choice_signature('math',right))
        self.assertNotEqual(choice_signature('math',r'x\cot x'),choice_signature('math',r'\operatorname{xcot}x'))
        self.assertNotEqual(choice_signature('math',r'\sin x^2'),choice_signature('math',r'\sin^2x'))
        self.assertNotEqual(choice_signature('math',r'6\div4'),choice_signature('math',r'6\operatorname{div}4'))

    def test_delivery_repairs_old_generator_helpers_before_identity_assignment(self):
        from scripts.generator_publish import localize_record
        record={'question':{':question/id':'keep-question',':question/problem':'Find $arccscx$.',
            ':question/worked-solution':'Use ${sin}^{2}⁡x$.',':question/answer-fields':[
                {':answer-field/type':':answer-field.type/checkbox',':answer-field/key':'$det(A)=1$',':answer-field/choices':[]},
                {':answer-field/type':':answer-field.type/blank',':answer-field/key':'field-1',
                 ':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':'arsech(x)'}]}]}}
        result=localize_record(record,Path('/tmp'),Path('/tmp'),library=SimpleNamespace(text=lambda x:x,saved={}))['question']
        self.assertEqual(result[':question/id'],'keep-question')
        self.assertIn(r'\operatorname{arccsc}',result[':question/problem'])
        self.assertIn(r'\sin',result[':question/worked-solution'])
        self.assertIn(r'\det',result[':question/answer-fields'][0][':answer-field/key'])
        self.assertIn(r'\operatorname{arsech}',result[':question/answer-fields'][1][':answer-field/choices'][0][':answer/value'])


if __name__=='__main__':unittest.main()
