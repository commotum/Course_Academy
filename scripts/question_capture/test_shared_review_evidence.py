"""Shared evidence is bound to raw question content, not mutable capture flags."""
import copy,json,unittest
from unittest.mock import patch

from core import atomic_json
from provenance import source_records
from import_repair import repair
import test_source_judgment as source_fixture
import test_import_repair as repair_fixture

class SharedReviewEvidenceTests(unittest.TestCase):
    def fixture(self):
        fixture=source_fixture.SourceJudgmentTests();fixture.setUp();self.addCleanup(fixture.temp.cleanup)
        fixture.state['questions'][fixture.mid]['content']=copy.deepcopy(fixture.question)
        atomic_json(fixture.directory/'state.json',fixture.state)
        (fixture.directory/'shared-explanation.png').write_bytes(b'original shared activity evidence')
        fixture.review['evidence_files']=['state.json','shared-explanation.png']
        return fixture
    def test_shared_state_evidence_survives_derived_serialization_and_import_flags(self):
        fixture=self.fixture();content=fixture.save()
        state=json.loads((fixture.directory/'state.json').read_text())
        self.assertEqual(state['questions'][fixture.mid]['content']['answer_fields'][0]['correct_origin'],'reviewed_ma_solution')
        state.update(import_complete=True,history_complete=True,activity_complete=True)
        state['questions']['q-other']={'before':{'problem':'Another captured question'}}
        atomic_json(fixture.directory/'state.json',state)
        self.assertTrue(any(r['category']=='reviewed_ma_solution' for r in source_records(content,fixture.directory)))
        proof=json.loads((fixture.directory/'answer-source-reviews.json').read_text())['reviews'][0]
        self.assertEqual(next(f for f in proof['evidence_files'] if f['path']=='state.json')['scope'],'question_raw_state')
    def test_changed_raw_question_or_shared_asset_invalidates_the_review(self):
        fixture=self.fixture();content=fixture.save()
        (fixture.directory/'shared-explanation.png').write_bytes(b'changed original evidence')
        self.assertFalse(any(r['category']=='reviewed_ma_solution' for r in source_records(content,fixture.directory)))
        (fixture.directory/'shared-explanation.png').write_bytes(b'original shared activity evidence')
        state=json.loads((fixture.directory/'state.json').read_text())
        state['questions'][fixture.mid]['history']={'worked_solution':'Changed raw explanation'}
        atomic_json(fixture.directory/'state.json',state)
        self.assertFalse(any(r['category']=='reviewed_ma_solution' for r in source_records(content,fixture.directory)))
    def test_answer_review_validation_feedback_reaches_next_agent_turn(self):
        fixture=repair_fixture.ImportRepairTests();fixture.setUp();self.addCleanup(fixture.tearDown)
        directory=fixture.root/'feedback';directory.mkdir();atomic_json(directory/'content.json',{'task_id':1})
        fixture.result={'status':'retry','summary':'Expert source review','edits':[],'equivalent':[],'distinct':[],
                        'answer_reviews':[{'question':'q-1'}]}
        inputs=[]
        def model(command,**kwargs):inputs.append(kwargs['input']);return fixture.fake_cli(command,**kwargs)
        with patch('import_repair.run_cli',side_effect=model), \
             patch('provenance.save_answer_reviews',side_effect=ValueError('Original choice index does not match')):
            with self.assertRaisesRegex(ValueError,'choice index'):repair(fixture.args,directory,ValueError('Import conflict'))
            record=json.loads((directory/'import-repair.json').read_text())
            self.assertEqual(record['attempts'][-1]['status'],'validation_failed')
            fixture.result={'status':'blocked','summary':'Need corrected review','edits':[],'equivalent':[],'distinct':[],'answer_reviews':[]}
            self.assertFalse(repair(fixture.args,directory,ValueError('Import conflict')))
        self.assertIn('validation_failed',inputs[1]);self.assertIn('Original choice index does not match',inputs[1])

if __name__=='__main__':unittest.main()
