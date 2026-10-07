"""Expert worked-solution reviews are derived evidence, with raw captures retained."""
import copy,json,tempfile,unittest,uuid
from pathlib import Path
from unittest.mock import Mock,patch
from types import SimpleNamespace

from core import atomic_json
from edn import kw
from provenance import Reconciler,save_answer_reviews,source_records
from import_repair import import_with_repair,repair
import test_import_repair as repairs

class SourceJudgmentTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.directory=Path(self.temp.name);self.addCleanup(self.temp.cleanup)
        self.mid='q-32595';self.solution=r'dx/dy=7/18, so dy/dx=18/7.'
        self.field={'key':'selection','type':'radio','correct_value':r'\frac{18}{7}',
                    'choices':[{'type':'math','value':v} for v in (r'\frac{18}{7}',r'\frac{54}{7}',r'\frac{9}{5}')],
                    'correct_origin':'model_interpretation'}
        self.question={'math_academy_id':self.mid,'problem':'Find dy/dx at (5,9).','worked_solution':self.solution,'answer_fields':[self.field]}
        self.content={'task_id':1,'questions':[self.question],'canonical_examples':[]}
        self.raw={'key':'selection','type':'radio','choices':copy.deepcopy(self.field['choices']),'choices_complete':True}
        self.state={'questions':{self.mid:{'before':{'problem':self.question['problem'],'fields':[self.raw]},
                     'after':{'worked_solution':self.solution},'actual_result':'Incorrect'}}}
        atomic_json(self.directory/'state.json',self.state);atomic_json(self.directory/'content.json',self.content)
        (self.directory/(self.mid+'-after.png')).write_bytes(b'original saved image')
        self.result=self.directory/'review-result.json';atomic_json(self.result,{'status':'retry','answer_reviews':[]})
        self.review={'question':self.mid,'field':'selection','value_type':'math','correct_value':r'\frac{18}{7}',
                     'option_index':0,'confident':True,'rationale':'Differentiate x(y) and take the reciprocal: 18/7.',
                     'evidence_files':[self.mid+'-after.png'],'choice_corrections':[]}
    def save(self,review=None):
        save_answer_reviews(self.content,self.directory,[review or self.review],str(uuid.uuid4()),self.result)
        return json.loads((self.directory/'content.json').read_text())
    def test_unknown_old_key_can_be_replaced_using_derived_judgment(self):
        raw=(self.directory/'state.json').read_bytes();content=self.save()
        sources=source_records(content,self.directory)
        source=next(r for r in sources if r['category']=='reviewed_ma_solution')
        self.assertFalse(source['category'].startswith('ma_'))
        reconciler=Reconciler([],sources,10,{self.mid:[]})
        self.assertTrue(reconciler.replace(self.mid,'selection','answer-field/correct',
            [kw('answer.type/math'),r'\frac{54}{7}'],[kw('answer.type/math'),r'\frac{18}{7}'],{'reviewed_ma_solution'}))
        self.assertEqual((self.directory/'state.json').read_bytes(),raw)
        self.assertEqual(len(list(self.directory.glob('content-before-source-review-*.json'))),1)
    def test_serialized_choice_correction_keeps_original_option_identity(self):
        review={**self.review,'correct_value':'(i+2j)m/s^2',
                'choice_corrections':[{'option_index':0,'value_type':'math','value':'(i+2j)m/s^2'}]}
        content=self.save(review)
        self.assertEqual(content['questions'][0]['answer_fields'][0]['correct_value'],'(i+2j)m/s^2')
        sources=source_records(content,self.directory)
        self.assertTrue(any(r['category']=='reviewed_ma_choices' for r in sources))
        archive=json.loads(next(self.directory.glob('content-before-source-review-*.json')).read_text())
        self.assertEqual(archive['questions'][0]['answer_fields'][0]['correct_value'],r'\frac{18}{7}')
    def test_blank_worked_solution_review_can_correct_derived_answer(self):
        self.field.update(type='blank',choices=[{'type':'math','value':'arcsec(x^2)'}],correct_value='arcsec(x^2)')
        self.raw.update(type='blank',choices=[])
        atomic_json(self.directory/'state.json',self.state)
        review={**self.review,'correct_value':'arcsec(x)*x','option_index':-1}
        content=self.save(review)
        self.assertEqual(content['questions'][0]['answer_fields'][0]['correct_value'],'arcsec(x)*x')
        self.assertTrue(any(r['category']=='reviewed_ma_solution' for r in source_records(content,self.directory)))
    def test_stale_solution_or_changed_asset_invalidates_review(self):
        content=self.save();(self.directory/(self.mid+'-after.png')).write_bytes(b'changed evidence')
        self.assertFalse(any(r['category']=='reviewed_ma_solution' for r in source_records(content,self.directory)))
    def test_pending_intent_and_unobserved_choice_are_not_changed(self):
        review={**self.review,'correct_value':'invented','option_index':8}
        with self.assertRaises(ValueError):self.save(review)
        (self.directory/'edb-import').mkdir();atomic_json(self.directory/'edb-import/commit-intent.json',{'basis':4})
        with self.assertRaisesRegex(ValueError,'Pending commit'):self.save()
        self.assertFalse((self.directory/'answer-source-reviews.json').exists())
    def test_original_grade_prevents_switching_to_known_wrong_option(self):
        self.raw['choices'][0]['option']='a';self.raw['submitted_option']='a'
        atomic_json(self.directory/'state.json',self.state)
        with self.assertRaisesRegex(ValueError,'observed choice grade'):self.save()
    def test_import_retry_reloads_reviewed_content_and_mutates_same_caller_object(self):
        content=copy.deepcopy(self.content);db=Mock();db.import_content.side_effect=[ValueError('Conflict'),{'committed':True}]
        def fix(*args):self.save();return True
        args=SimpleNamespace(preview=False,no_import_repair=False)
        with patch('import_repair.repair',side_effect=fix):
            result=import_with_repair(db,content,self.directory,{'activity_complete':True,'history_complete':True},args,revisit=False)
        self.assertTrue(result['committed']);self.assertTrue(all(c.args[0] is content for c in db.import_content.call_args_list))
        self.assertEqual(content['questions'][0]['answer_fields'][0]['correct_origin'],'reviewed_ma_solution')
    def test_caller_state_keeps_corrected_derived_content_eligible_after_import(self):
        from saved_imports import eligible
        self.content.update(task_type='lesson',content_only=True)
        self.state.update(task_id=1,task_type='lesson',activity_complete=True,lesson_complete=True,
                          history_complete=True,completion="You've completed the lesson.",examples={})
        self.state['questions'][self.mid].update(finalized=True,content=copy.deepcopy(self.question),history={'worked_solution':self.solution})
        atomic_json(self.directory/'state.json',self.state);atomic_json(self.directory/'content.json',self.content)
        atomic_json(self.directory/'activity-metadata.json',[{'id':'question-32595'}])
        content=copy.deepcopy(self.content);state=copy.deepcopy(self.state)
        db=Mock();db.import_content.side_effect=[ValueError('Conflict'),{'committed':True}]
        def fix(*args):self.save();return True
        with patch('import_repair.repair',side_effect=fix):
            import_with_repair(db,content,self.directory,state,SimpleNamespace(preview=False,no_import_repair=False),revisit=False)
        state['import_complete']=True;atomic_json(self.directory/'state.json',state)
        self.assertTrue(eligible(self.directory,json.loads((self.directory/'state.json').read_text()),content))
        self.assertEqual(state['questions'][self.mid]['before'],self.state['questions'][self.mid]['before'])
    def test_failed_candidate_validation_reaches_the_next_diagnosis(self):
        fixture=repairs.ImportRepairTests();fixture.setUp();self.addCleanup(fixture.tearDown)
        directory=fixture.root/'feedback';directory.mkdir()
        fixture.result={'status':'repair','summary':'Candidate','edits':[{'old':'without algebra.','new':'without guessing algebra.'}],
                        'equivalent':[{'left':'x','right':'x'}],'distinct':[],'answer_reviews':[]}
        captured=[]
        def model(command,**kwargs):captured.append(kwargs['input']);return fixture.fake_cli(command,**kwargs)
        with patch('import_repair.run_cli',side_effect=model), \
             patch('import_repair.subprocess.run',return_value=SimpleNamespace(returncode=1,stdout='FAIL: preserves function scope',stderr='')):
            with self.assertRaisesRegex(ValueError,'offline regression'):repair(fixture.args,directory,ValueError('Conflict'))
            fixture.result={'status':'blocked','summary':'Need another correction','edits':[],'equivalent':[],'distinct':[],'answer_reviews':[]}
            self.assertFalse(repair(fixture.args,directory,ValueError('Conflict')))
        self.assertIn('validation_failed',captured[1]);self.assertIn('preserves function scope',captured[1])

if __name__=='__main__':unittest.main()
