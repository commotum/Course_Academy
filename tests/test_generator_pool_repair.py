"""Retirement preserves bank ownership used by saved reviews and scheduling."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from generator_pool_repair import eligible, generated_proof, repair_pool
from generator_publish import StaleBasis

class PoolRepairTests(unittest.TestCase):
    def test_duplicate_report_cannot_turn_completed_retirement_into_failure(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);qid='3f9ccaa5-d69c-584d-946e-0c57b3050160'
            (root/'records.json').write_text(json.dumps([{'question':{':question/id':qid},'generation':{'seed':7}}]))
            row={'question_id':qid,'entity_id':7,'finding':'bank shortcut','reproduction':'seed 7'}
            (root/'affected.json').write_text(json.dumps({'affected_questions':[
                row,{**row,'evidence_path':'records.json'},
                {**row,'entity_id':8,'question_id':'c0bfdf88-6b0a-508a-8c07-cd94961f2a33'}]}))
            class Client:
                def status(self):return {'basis':2,'lineage':'test'}
                def query(self,*args):return []  # already absent from the pool
            publisher=SimpleNamespace(client=Client(),config=SimpleNamespace(request_directory=root))
            with patch('generator_pool_repair.GeneratorCommitter') as committer:
                committer.return_value.pending.return_value=None
                result=repair_pool(publisher,123,[root/'affected.json'],root/'repair')
                committer.return_value.preview.assert_not_called()
                committer.return_value.submit.assert_not_called()
            self.assertEqual(result['already_absent'],[7])
            self.assertEqual(result['retired'],[])
            self.assertEqual(len(result['duplicate_reports']),1)
            self.assertEqual(len(result['unresolved']),1)
            self.assertEqual(result['unresolved'][0]['question']['entity_id'],8)

    def test_pool_repair_retires_without_detaching_and_rechecks_after_preview_race(self):
        with tempfile.TemporaryDirectory() as t:
            e=Path(t);qid='3f9ccaa5-d69c-584d-946e-0c57b3050160'
            (e/'records.json').write_text(json.dumps([{'question':{':question/id':qid},'generation':{'seed':7}}]))
            (e/'affected.json').write_text(json.dumps({'affected_questions':[{'question_id':qid,'entity_id':7,'finding':'repeatable bank shortcut','reproduction':'seed 7','evidence_path':'records.json'}]}))
            class Client:
                def status(self):return {'database':'test','lineage':'test-lineage','basis':1}
                def query(self,query,inputs,directory,name,basis):
                    # Reserved review steps exist before the learner sees a
                    # task-item. They must keep their question's bank link.
                    if name=='candidates':return [[{':db/id':7,':question/id':qid,':step/_content':[{':db/id':88}]}]]
                    if name=='entities-preserved':return [[7,qid]]
                    if name in ('membership-readback','retirement-readback'):return [[7]]
                    return []
            class Committer:
                def __init__(self,*args):self.previews=0;self.batch=None
                def pending(self):return None
                def preview(self,batch,snapshot):
                    self.previews+=1;self.batch=batch
                    if self.previews==1:raise StaleBasis('concurrent learner action')
                def save_request(self,*args):return {'saved':'exact'}
                def submit(self,request):return {':edb/db-after-t':2}
                def verify_receipt(self,*args):return {'learner_and_engine_facts_unchanged':True}
                def retire(self,*args):pass
            committer=Committer();publisher=SimpleNamespace(client=Client(),config=SimpleNamespace(request_directory=e,source=':application/ca-engine'))
            with patch('generator_pool_repair.GeneratorCommitter',return_value=committer):
                result=repair_pool(publisher,123,[e/'affected.json'],e/'repair')
            self.assertEqual(committer.previews,2)
            self.assertEqual(result['retired'],[7]);self.assertEqual(result['unresolved'],[])
            self.assertEqual(committer.batch['retractions'],[])
            self.assertEqual([[str(x) for x in row] for row in committer.batch['assertions']],[['7',':question/retired','True']])
            self.assertFalse(any(str(form[0])==':db/retract' for form in committer.batch['forms']))
            self.assertTrue(result['learner_and_engine_facts_unchanged'])

    def test_only_unserved_generated_noncanonical_questions_are_eligible(self):
        self.assertEqual(eligible({':db/id':1}),(True,None))
        for attr,value,reason in [(':question/math-academy-id','q-1','original_source'),
                (':task-item/_content',[{':db/id':5}],'already_served'),
                (':knowledge-point/_canonical-example',{':db/id':6},'canonical_example'),
                (':question/retired',True,'already_retired')]:
            self.assertEqual(eligible({attr:value}),(False,reason))

    def test_legacy_detachment_request_is_preserved_without_submitting(self):
        with tempfile.TemporaryDirectory() as t:
            publisher=SimpleNamespace(client=object(),config=SimpleNamespace(request_directory=Path(t)))
            with patch('generator_pool_repair.GeneratorCommitter') as factory:
                c=factory.return_value
                c.pending.return_value={'snapshot_edn':'{}','batch_edn':'{"assertions" [] "retractions" [[123 :knowledge-point/questions 7]]}'}
                with self.assertRaisesRegex(ValueError,'exact-outcome reconciliation'):
                    repair_pool(publisher,123,[],Path(t)/'repair')
                c.submit.assert_not_called()
                c.retire.assert_not_called()

    def test_proof_must_match_a_reproduced_generated_uuid_and_stay_inside_evidence(self):
        with tempfile.TemporaryDirectory() as t:
            e=Path(t);(e/'records.json').write_text(json.dumps([{'question':{':question/id':'uuid-1'},'generation':{'seed':1}}]))
            row={'question_id':'uuid-1','finding':'bank-only shortcut','reproduction':'seed 1','evidence_path':'records.json'}
            self.assertTrue(generated_proof(row,e))
            self.assertFalse(generated_proof({**row,'question_id':'uuid-2'},e))
            self.assertFalse(generated_proof({**row,'evidence_path':'../records.json'},e))
            self.assertFalse(generated_proof({**row,'reproduction':''},e))

if __name__=='__main__':unittest.main()
