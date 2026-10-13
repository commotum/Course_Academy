import json, tempfile, unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import apply_reviewed_archive_packages as consumer
from scripts.storage import atomic_json

class PreparedArchiveGuards(unittest.TestCase):
    def setUp(self):
        self.temporary=tempfile.TemporaryDirectory();self.addCleanup(self.temporary.cleanup)
        root=Path(self.temporary.name);directory=root/'capture'/'123';directory.mkdir(parents=True)
        repair=directory/'repairs'/'own-review';repair.mkdir(parents=True)
        state=root/'state';state.mkdir();spool=root/'spool';spool.mkdir()
        self.config=SimpleNamespace(output_root=directory.parent,state_root=state,spool_root=spool,database_lock=root/'db.lock',
                                    capture_only=False,math_root=root/'math',database='test',endpoint='test',postgres_url=None,source=':org/Math-Academy')
        for name in ['checkpoint.json','capture-complete.json','post-activity.json']:atomic_json(directory/name,{'preserved':name})
        for name in ['xp.json','daily-xp.json','completed.json','active.json','xp-ledger.json','retakes.json']:atomic_json(state/name,{'preserved':name})
        atomic_json(directory/'content.json',{'authored':'old'})
        atomic_json(repair/'content.json',{'authored':'reviewed','questions':[]})
        atomic_json(repair/'checkpoint.json',{'history':{'questions':[]}})
        target=consumer.target_id(self.config)
        item={'capture_directory':str(directory),'target_id':target,'status':'verified','capture_only':False}
        atomic_json(consumer.spool_for(self.config,directory),item);atomic_json(directory/'import-status.json',item)
        self.entry={'account':'test','task_id':'123','directory':str(directory),'repair':str(repair),
                    'review_version':'trusted-version','review_method':'retained exact source',
                    'immutable_stage_files':{str(repair/name):consumer.sha(repair/name) for name in ['content.json','checkpoint.json']},
                    'protected_files':consumer.protected_files(self.config,directory),
                    'original_content_sha256':consumer.sha(directory/'content.json'),
                    'staged_content_sha256':consumer.sha(repair/'content.json'),'target_id':target}
    def assert_refused(self):
        with patch.object(consumer,'DatabasePipeline') as pipeline:
            with self.assertRaises(ValueError):consumer.apply_one(self.entry,self.config)
            pipeline.assert_not_called()
    def test_valid_completed_inactive_source_passes_guards(self):
        consumer.guard(self.entry,self.config)
    def test_staged_content_tampering_is_rejected_before_pipeline(self):
        atomic_json(Path(self.entry['repair'])/'content.json',{'forged':'source'});self.assert_refused()
    def test_checkpoint_and_ledger_changes_are_rejected(self):
        for path in self.entry['protected_files']:
            original=Path(path).read_bytes();Path(path).write_text('changed')
            self.assert_refused();Path(path).write_bytes(original)
    def test_actual_xp_json_drift_blocks_before_pipeline(self):
        atomic_json(self.config.state_root/'xp.json',{'changed':'actual current engine XP ledger'});self.assert_refused()
    def test_capture_only_authorization_cannot_be_overridden(self):
        directory=Path(self.entry['directory']);spool=consumer.spool_for(self.config,directory)
        item=json.loads(spool.read_text());item['capture_only']=True;atomic_json(spool,item);self.assert_refused()
    def test_another_target_or_active_capture_is_rejected(self):
        self.config.database='other';self.assert_refused();self.config.database='test'
        atomic_json(self.config.state_root/'active.json',{'directory':self.entry['directory']});self.assert_refused()
    def test_unclassified_pending_outbox_is_rejected(self):
        directory=Path(self.entry['directory']);spool=consumer.spool_for(self.config,directory)
        item=json.loads(spool.read_text());item['status']='pending';atomic_json(spool,item);self.assert_refused()
    def test_unresolved_request_is_not_replaced(self):
        directory=Path(self.entry['directory']);(directory/'database').mkdir();request=directory/'database/request.json'
        atomic_json(request,{'immutable':'existing'});source=consumer.sha(directory/'content.json')
        with patch.object(consumer,'DatabasePipeline') as pipeline:
            pipeline.return_value.process.return_value={'status':'pending'}
            with self.assertRaises(ValueError):consumer.apply_one(self.entry,self.config)
            pipeline.return_value.process.assert_called_once_with(directory,apply=True)
        self.assertEqual(source,consumer.sha(directory/'content.json'))
        self.assertEqual({'immutable':'existing'},json.loads(request.read_text()))
        self.assertFalse((Path(self.entry['repair'])/'prepared-apply-original-outbox.json').exists())
    def test_normal_pipeline_verified_result_reconciles_exact_original_target(self):
        with patch.object(consumer,'DatabasePipeline') as pipeline:
            pipeline.return_value.process.return_value={'status':'no_changes','basis':123,'omissions':[]}
            result=consumer.apply_one(self.entry,self.config)
            pipeline.return_value.process.assert_called_once()
        directory=Path(self.entry['directory']);item=json.loads((directory/'import-status.json').read_text())
        self.assertEqual(result['status'],'verified');self.assertEqual(item['target_id'],self.entry['target_id'])
        self.assertFalse(item['capture_only']);self.assertEqual(item['status'],'no_changes')
        for path,digest in self.entry['protected_files'].items():self.assertEqual(digest,consumer.sha(path))

if __name__=='__main__':unittest.main()
