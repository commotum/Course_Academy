from copy import deepcopy
import hashlib
from pathlib import Path
import tempfile
import threading
import unittest
from scripts.activity.capture import ActivityCapture
from scripts.config import Config
from scripts.recovery import backfill_progress, archive
from scripts.database.pipeline import DatabasePipeline
from scripts.activity.task_payload import semantic_identity
from scripts.storage import atomic_json, read_json
from scripts.tests.test_database import question, FakeClient
from scripts.tests import test_database as database_tests
from scripts.legacy_recovery import batch_question, batches

class EvidenceReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.config=Config(repo_root=self.root)
        self.calls=[]
        class Agent:
            def request(agent,task,payload):
                self.calls.append(deepcopy(payload))
                return self.answer
        self.capture=ActivityCapture(self.config,None,threading.Event(),solver=Agent())
        self.capture.directory=self.root;self.capture.checkpoint_path=self.root/'checkpoint.json'
        self.capture.state={'judgments':{}}
        self.q=question();self.q['answer_fields'][0].pop('evidence');self.q['source_file']='saved.html'
        self.bad={'status':'confirmed','answers':[{'key':'x','ma_value':'2','ma_basis':'correct_grade'}]}
        self.answer={'status':'confirmed','reasoning':'The source explicitly gives 1+1=2.',
            'answers':[{'key':'x','ma_value':'2','ma_basis':'worked_solution','ma_evidence':'1+1=2','value_type':'math'}]}
    def check(self):
        return self.capture._validate_final_answers(self.q,[],self.bad,{'question':self.q},'questions','questions:q-11',{'source_limitations':[]})
    def test_failed_grade_attribution_gets_checked_quote_and_is_persisted(self):
        result=self.check()
        self.assertEqual(result['answer_validation']['status'],'supported')
        self.assertEqual(result['answer_fields'][0]['evidence']['solution_quote'],'1+1=2')
        self.assertEqual(len(self.calls),1)
        self.assertIn('confirmed Math Academy evidence',self.calls[0]['gap'])
        self.assertTrue(read_json(self.capture.checkpoint_path)['answer_evidence_reviews'])
    def test_unavailable_evidence_stops_bounded_repair_and_reuses_final_finding(self):
        self.answer=self.bad
        result=self.check();self.check()
        self.assertEqual(len(self.calls),1)
        self.assertEqual(result['answer_validation']['status'],'unavailable')
        self.assertNotIn('correct_value',result['answer_fields'][0])

class HistoricalProgressTests(unittest.TestCase):
    def test_backfill_preserves_source_times_xp_and_account_ledgers(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);c=Config(repo_root=root);d=c.output_root/'1';d.mkdir(parents=True)
            page=d/'learn.html';page.write_text('<a href="/courses/76/progress">Methods of Proof</a><div id="coursePercentComplete">37%</div>')
            before={'observed_at':10,'progress':[{'course_id':'76','topics':[{'topic_id':'1','color':'white'}]}]}
            obs={'observed_at':20,'dashboard':{'html_path':str(page)},'progress':[{'course_id':'76','topics':[{'topic_id':'1','color':'rgb(210, 231, 249)'}]}]}
            post={'observed_at':20,'completion':{'earned_xp':7},'observations':obs}
            atomic_json(d/'post-activity.json',post);atomic_json(d/'progress-before.json',before)
            atomic_json(c.state_root/'xp.json',{'unchanged':True});ledger=(c.state_root/'xp.json').read_bytes()
            result=backfill_progress(c,d);after=read_json(d/'post-activity.json')
            self.assertEqual(result['course_progress']['displayed_progress'],'37%')
            self.assertEqual(after['observed_at'],20);self.assertEqual(after['completion'],post['completion'])
            self.assertEqual(after['progress_comparison']['changes'][0]['before_band'],0)
            self.assertEqual(after['progress_comparison']['changes'][0]['after_band'],1)
            self.assertEqual((c.state_root/'xp.json').read_bytes(),ledger)
            self.assertEqual(read_json(d/'repairs/historical-progress-v1/originals/post-activity.json'),post)
            backfill_progress(c,d)
            self.assertEqual(read_json(d/'repairs/historical-progress-v1/originals/post-activity.json'),post)

class PreparationRepairPersistenceTests(unittest.TestCase):
    def test_preview_no_changes_does_not_rewrite_capture(self):
        with tempfile.TemporaryDirectory() as temp:
            d,c=database_tests.PipelineTests().setup(temp)
            content=read_json(d/'content.json');q=content['questions'][0]
            q['answer_fields'][0].pop('evidence');atomic_json(d/'content.json',content)
            repair={'record_kind':'questions','capture_key':'q-11','source_evidence_hash':semantic_identity('preparation_source',q),'question':question(),'judgment':{'status':'confirmed'}}
            class PreparedPipeline(DatabasePipeline):
                def _prepare(self,content,directory,basis):
                    return {'batches':[],'omissions':[],'calibration':None,'source_repairs':[repair]},{}
            pipeline=PreparedPipeline(c,threading.Event(),client=FakeClient())
            self.assertEqual(pipeline.process(d,apply=False)['status'],'no_changes')
            self.assertEqual(read_json(d/'content.json'),content)
            pipeline.process(d,apply=True)
            self.assertIn('evidence',read_json(d/'content.json')['questions'][0]['answer_fields'][0])

    def test_verified_repair_updates_capture_preserves_original_and_rejects_stale_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);c=Config(repo_root=root);d=c.output_root/'1';db=d/'database';db.mkdir(parents=True)
            q=question();q['answer_fields'][0].pop('evidence');q['answer_validation']={'status':'unavailable'};content={'questions':[q]}
            atomic_json(d/'content.json',content)
            repair={'record_kind':'questions','capture_key':'q-11','source_evidence_hash':semantic_identity('preparation_source',q),'question':question(),'judgment':{'status':'confirmed'}}
            pipeline=DatabasePipeline(c,threading.Event(),client=object())
            atomic_json(db/'request.json',{'unknown_outcome':True})
            pipeline._persist_source_repairs(d,db,[repair]);self.assertEqual(read_json(d/'content.json'),content)
            (db/'request.json').unlink();pipeline._persist_source_repairs(d,db,[{**repair,'source_evidence_hash':'wrong'}])
            self.assertEqual(read_json(d/'content.json'),content)
            pipeline._persist_source_repairs(d,db,[repair])
            self.assertEqual(read_json(d/'content.json')['questions'][0]['answer_fields'][0]['evidence'],question()['answer_fields'][0]['evidence'])
            self.assertEqual(read_json(d/'content.json')['questions'][0]['answer_validation']['status'],'supported')
            originals=list((db/'source-repairs').glob('*/original-content.json'));self.assertEqual(len(originals),1)
            self.assertEqual(read_json(originals[0]),content)

class LegacyReviewContractTests(unittest.TestCase):
    def test_batch_preserves_owning_question_keys_and_image_attachments(self):
        a=question();b=deepcopy(a);b['math_academy_id']='q-12'
        a['assets']=[{'path':'/source/diagram.png','sha256':'source-hash'}]
        payload=batch_question([{'question':a},{'question':b}])
        self.assertEqual([f['key'] for f in payload['answer_fields']],['q-11/x','q-12/x'])
        self.assertEqual(payload['assets'],a['assets'])
        self.assertEqual(a['answer_fields'][0]['key'],'x')

    def test_batches_limit_image_payloads(self):
        q=question();q['assets']=[{'path':str(i)} for i in range(16)]
        self.assertEqual([len(group) for group in batches([{'question':q},{'question':q}])],[1,1])
