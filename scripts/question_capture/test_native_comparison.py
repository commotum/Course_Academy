"""Real bounded native helper and reconciliation integration, entirely offline."""
import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core import build_transaction, compare_answers
import native_comparison as native
from provenance import Reconciler, value_hash
import test_replacement


class NativeComparisonTests(unittest.TestCase):
    def test_saved_native_comparison_cases(self):
        cases=json.loads((Path(__file__).parent/'fixtures/native-comparison-cases.json').read_text())['cases']
        for case in cases:
            titles=[]
            if case.get('symbolic_i'):titles.append('Vector')
            if case.get('integer_indices'):titles.append('Sequence')
            with self.subTest(case=case['name']):
                result=native.compare(case['canonical'],case['submitted'],kp_titles=titles)
                self.assertEqual(result['outcome'],{'unsupported':'unresolved'}.get(case['expected'],case['expected']),result)
                if result['outcome']=='unresolved':self.assertTrue(result['reason'])

    def test_context_and_domains_and_form_sensitive_prompts(self):
        self.assertEqual(native.compare('i^2','-1')['outcome'],'equivalent')
        self.assertEqual(native.compare('i^2','-1',kp_titles=['Vectors'])['outcome'],'different')
        self.assertEqual(native.compare('(-1/2)^n','(-1/2)^n')['outcome'],'unresolved')
        self.assertEqual(native.compare('(-1/2)^n','(-1/2)^n',kp_titles=['Sequences'])['outcome'],'equivalent')
        for a,b in [('x/x','1'),('sqrt(x)^2','x')]:
            self.assertEqual(compare_answers(a,b)['outcome'],'unresolved')
        self.assertEqual(native.compare('1/2','0.5',prompt='Round to one decimal place')['outcome'],'different')
        self.assertEqual(compare_answers('2/4','1/2',prompt='Express in lowest terms')['outcome'],'different')
        self.assertNotEqual(value_hash('x+x'),value_hash('2*x'))

    def test_execution_failures_and_resource_limits_are_explicit_and_cached(self):
        with patch.dict(os.environ,{'COURSE_ACADEMY_MATH_COMPARE_BIN':'/missing/native-helper'}):
            result=native.compare('x+x','2*x')
        self.assertEqual(result['outcome'],'unresolved');self.assertIn('execution failed',result['reason'])
        self.assertEqual(native.compare('x'*4097,'x')['outcome'],'unresolved')
        with tempfile.TemporaryDirectory() as directory:
            script=Path(directory)/'hang';script.write_text('#!/usr/bin/env python3\nimport time\ntime.sleep(60)\n');script.chmod(0o700)
            with patch.dict(os.environ,{'COURSE_ACADEMY_MATH_COMPARE_BIN':str(script)}),patch.object(native,'TIMEOUT',0.05):
                result=native.compare('x','y')
                self.assertIn('exceeded',result['reason'])
        native._compare.cache_clear()
        native.compare('x+x','2*x');info=native._compare.cache_info()
        native.compare('x+x','2*x')
        self.assertEqual(native._compare.cache_info().hits,info.hits+1)

    def test_text_and_images_never_use_symbolic_checker(self):
        with patch('native_comparison.compare') as compare:
            self.assertEqual(compare_answers('x+x','2*x','text')['outcome'],'different')
            self.assertEqual(compare_answers('one.png','two.png','image')['outcome'],'different')
        compare.assert_not_called()

    def fixture(self):
        fixture=test_replacement.ReplacementTests();fixture.setUp();self.addCleanup(fixture.tearDown)
        fixture.q['problem']=fixture.old[':question/problem']='Simplify the expression.'
        fixture.field[':answer-field/type'][':db/ident']=':answer-field.type/blank'
        fixture.field[':answer-field/correct'][':answer/value']='x+x'
        fixture.field[':answer-field/choices']=[fixture.field[':answer-field/correct']]
        fixture.q['answer_fields']=[{'key':'selection','type':'blank','correct_value':'2*x',
                                     'choices':[{'type':'math','value':'2*x'}]}]
        return fixture

    def test_equivalent_capture_is_noop_without_replacement_authority_or_llm(self):
        f=self.fixture()
        reconciler=Reconciler([],[],656,{f.mid:True})
        with patch('import_repair.repair') as repair:
            transaction,_=build_transaction(f.content,f.topic,{f.mid:f.old},reconciler)
        repair.assert_not_called()
        self.assertEqual(transaction,[])
        self.assertFalse(reconciler.needs_review)
        self.assertEqual(f.field[':answer-field/correct'][':answer/value'],'x+x')

    def test_different_unresolved_and_changed_identity_remain_reviews(self):
        for new in ('3*x','ln(x^2)'):
            f=self.fixture();field=f.q['answer_fields'][0]
            field['correct_value']=field['choices'][0]['value']=new
            reconciler=Reconciler([],[],656,{f.mid:False})
            build_transaction(f.content,f.topic,{f.mid:f.old},reconciler)
            self.assertTrue(reconciler.needs_review)
        f=self.fixture();f.q['answer_fields'][0]['key']='different-field'
        with self.assertRaisesRegex(ValueError,'omitted existing fields'):
            build_transaction(f.content,f.topic,{f.mid:f.old},Reconciler([],[],656,{f.mid:False}))

    def test_equivalence_does_not_bypass_other_provenance_conflicts(self):
        f=self.fixture();f.q['worked_solution']='Contradictory new solution'
        reconciler=Reconciler([],[],656,{f.mid:False})
        build_transaction(f.content,f.topic,{f.mid:f.old},reconciler)
        self.assertTrue(reconciler.needs_review)
        self.assertEqual(reconciler.decisions[0]['attribute'],'question/worked-solution')

    def test_native_execution_failure_remains_visible_in_reconciliation_review(self):
        f=self.fixture()
        with patch.dict(os.environ,{'COURSE_ACADEMY_MATH_COMPARE_BIN':'/missing/native-review-helper'}):
            reconciler=Reconciler([],[],656,{f.mid:False})
            build_transaction(f.content,f.topic,{f.mid:f.old},reconciler)
        self.assertTrue(reconciler.needs_review)
        decision=next(d for d in reconciler.decisions if d['attribute']=='answer-field/correct')
        self.assertEqual(decision['comparison']['outcome'],'unresolved')
        self.assertIn('execution failed',decision['comparison']['reason'])

    def test_authorized_prompt_replacement_applies_new_form_requirements(self):
        f=self.fixture()
        f.field[':answer-field/correct'][':answer/value']='1/2'
        field=f.q['answer_fields'][0];field['correct_value']=field['choices'][0]['value']='0.5'
        f.q['problem']='Round to one decimal place.'
        old={'question':f.mid,'field':None,'attribute':'question/problem',
             'value':f.old[':question/problem'],'category':'local_authored','file':'authoring.json'}
        new={**old,'value':f.q['problem'],'category':'ma_capture','file':'capture.json'}
        reconciler=Reconciler([old],[new],656,{f.mid:False})
        build_transaction(f.content,f.topic,{f.mid:f.old},reconciler)
        self.assertTrue(reconciler.needs_review)
        self.assertTrue(any(d['attribute']=='answer-field/correct' for d in reconciler.decisions))

    def test_new_valid_symbolic_blank_does_not_require_supported_comparison(self):
        f=self.fixture();field=f.q['answer_fields'][0]
        field['correct_value']=field['choices'][0]['value']='arctan(x)'
        transaction,_=build_transaction(f.content,f.topic,{},Reconciler([],[],656,{}))
        self.assertTrue(transaction)


if __name__ == '__main__':unittest.main()
