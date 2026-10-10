"""Offline backlog recovery, immutable intents and durable retry limits."""
import copy
import contextlib
import io
import hashlib
import json
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from capture import arguments, run, unfinished_run
from core import atomic_json
from database import Database, StaleBasis
from edn import dumps, kw
from import_repair import import_with_repair
from provenance import ReconciliationReview
from saved_imports import complete, eligible, read_json, sweep, verified, version


class RetryVersionTests(unittest.TestCase):
    def test_only_running_importer_or_installed_checker_resets_retries(self):
        with tempfile.TemporaryDirectory() as work:
            root=Path(work);package=root/'scripts/question_capture';package.mkdir(parents=True)
            (root/'engine/rust').mkdir(parents=True)
            source=root/'engine/rust/symbolic.rs';source.write_text('unbuilt v1')
            (package/'core.py').write_text('importer v1')
            sweep_source=package/'saved_imports.py';sweep_source.write_text('logging v1')
            with patch('saved_imports.ROOT',root),patch('saved_imports.PACKAGE',package), \
                 patch('saved_imports.availability',return_value=('checker','installed-v1',10,493)) as checker:
                first=version()
                source.write_text('unbuilt v2');sweep_source.write_text('logging v2')
                self.assertEqual(first,version())
                checker.return_value=('checker','installed-v2',10,493)
                self.assertNotEqual(first,version())
                checker.return_value=('checker','installed-v1',10,493)
                (package/'core.py').write_text('importer v2')
                self.assertNotEqual(first,version())
                current=version()
                (package/'import_repair.py').write_text('updated repair judgment')
                self.assertNotEqual(current,version())


class SavedImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.args = arguments(['run','--state-dir',str(self.root/'state'),
                               '--output',str(self.root/'captures')])
        self.args.source = None  # Frozen receipts below belong to the legacy importer.
        self.args.no_import_repair=True  # These offline fixtures never launch a CLI.
        self.db = Mock()
        self.db.import_content.return_value = {'already_complete':True,'database_writes':0}
        self.generation = patch('saved_imports.version',return_value='v1').start()
        self.addCleanup(patch.stopall)
        self.addCleanup(self.temp.cleanup)

    def capture(self, task, **changes):
        directory = self.args.output/str(task)
        q = {'math_academy_id':'q-'+str(task),'problem':'P','worked_solution':'S'}
        content = {'task_id':task,'task_type':'lesson','content_only':True,
                   'questions':[q],'canonical_examples':[]}
        state = {'task_id':task,'topic_id':1,'task_type':'lesson','activity_complete':True,
                 'lesson_complete':True,'completion':"You've completed the lesson.",
                 'history_complete':True,'questions':{q['math_academy_id']:{
                     'finalized':True,'history':{'worked_solution':'S'},'content':q}},
                 'examples':{},'deferred_error':{'phase':'queue-after','message':'Offline'}}
        state.update(changes)
        atomic_json(directory/'state.json',state)
        atomic_json(directory/'content.json',content)
        atomic_json(directory/'activity-metadata.json',[{'id':'question-'+str(task)}])
        return directory, state, content

    def migrated_capture(self,task=1):
        directory,state,content=self.capture(task,import_complete=True,
            deferred_error={'phase':'import','message':'Content provenance needs review'})
        historical=copy.deepcopy(content);historical['questions'][0]['is_example']=False
        self.intent(directory,historical,committed=True)
        target=directory/'edb-import';archive=target/'committed-before-capture-format-migration';archive.mkdir()
        for name in ('transaction.edn','commit.edn','commit-intent.json','reconciliation.edn'):
            (target/name).rename(archive/name)
        atomic_json(target/'verification.json',{'committed':True,'reimport_is_noop':True,
            'learner_and_engine_facts_unchanged':True,'basis_before':656,'basis_after':657,
            'content_sha256':hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest(),
            'original_content_sha256':hashlib.sha256(json.dumps(historical,sort_keys=True).encode()).hexdigest(),
            'receipt_archive':archive.name})
        return directory,state,content

    def test_audited_archived_receipt_skips_import_and_clears_false_deferral(self):
        directory,state,content=self.migrated_capture()
        self.assertTrue(verified(directory,content))
        sweep(self.db,self.args,trigger='startup')
        self.db.import_content.assert_not_called()
        self.assertNotIn('deferred_error',read_json(directory/'state.json'))

    def test_archived_receipt_never_attests_new_content_or_changed_transaction(self):
        directory,state,content=self.migrated_capture()
        content['questions'][0]['worked_solution']='New evidence'
        proof=read_json(directory/'edb-import/verification.json')
        proof['content_sha256']=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
        atomic_json(directory/'edb-import/verification.json',proof)
        self.assertFalse(verified(directory,content))
        directory,state,content=self.migrated_capture(2)
        (directory/'edb-import/committed-before-capture-format-migration/transaction.edn').write_text('[]')
        self.assertFalse(verified(directory,content))

    def test_archived_receipt_requires_matching_basis_and_audited_location(self):
        directory,state,content=self.migrated_capture()
        proof=read_json(directory/'edb-import/verification.json')
        proof['basis_after']=999;atomic_json(directory/'edb-import/verification.json',proof)
        self.assertFalse(verified(directory,content))
        proof['basis_after']=657;proof['receipt_archive']='../other';atomic_json(directory/'edb-import/verification.json',proof)
        self.assertFalse(verified(directory,content))

    def test_repair_of_current_b_also_unblocks_older_a(self):
        older,_,_ = self.capture(1)
        current,state,content = self.capture(2)
        self.db.import_content.side_effect=ValueError('notation conflict')
        sweep(self.db,self.args,trigger='startup',exclude=[current])
        self.args.no_import_repair=False
        self.db.import_content.reset_mock()
        self.db.import_content.side_effect = [ValueError('notation conflict'),
            {'previewed':True}, {'already_complete':True,'database_writes':0}]
        def repair_comparison(*args):
            self.generation.return_value='v2'
            return True
        with patch('import_repair.repair',side_effect=repair_comparison) as repair:
            import_with_repair(self.db,content,current,state,self.args)
        repair.assert_called_once()
        self.assertEqual([c.args[1].parent for c in self.db.import_content.call_args_list],
                         [current,current,older])
        self.assertTrue(read_json(older/'state.json')['import_complete'])
        self.assertNotIn('deferred_error',read_json(older/'state.json'))

    def test_saved_import_failure_runs_repair_and_commits_on_success(self):
        self.args.no_import_repair=False
        directory,_,_=self.capture(1)
        self.db.import_content.side_effect=[ReconciliationReview('notation mismatch'),
                                           {'already_complete':True,'database_writes':0}]
        with patch('import_repair.repair',return_value=True) as repair:
            result=sweep(self.db,self.args,trigger='startup')
        repair.assert_called_once()
        self.assertEqual(result[0]['status'],'complete')
        self.assertTrue(read_json(directory/'state.json')['import_complete'])

    def test_skip_verified_and_unfinished_and_repair_stale_checkpoint(self):
        committed,_,_ = self.capture(1,import_complete=False)
        atomic_json(committed/'edb-import/verification.json',{'committed':True,'reimport_is_noop':True,
                    'learner_and_engine_facts_unchanged':True})
        (committed/'edb-import/commit.edn').write_text(dumps({kw('edb/committed'):True}))
        noop,_,_ = self.capture(2)
        atomic_json(noop/'edb-import/verification.json',{'already_complete':True,'database_writes':0})
        self.capture(3,activity_complete=False)
        self.capture(4,history_complete=False)
        self.capture(5,completion='Working...')
        directory,state,content = self.capture(6)
        state['questions']['q-6']['history']={}
        atomic_json(directory/'state.json',state)
        sweep(self.db,self.args,trigger='startup')
        self.db.import_content.assert_not_called()
        self.assertTrue(read_json(committed/'state.json')['import_complete'])
        self.assertNotIn('deferred_error',read_json(noop/'state.json'))

    def test_flags_alone_do_not_prove_import_or_capture_completion(self):
        self.capture(1,import_complete=True)
        directory,state,content = self.capture(2)
        state['questions']['q-2']['finalized']=False
        atomic_json(directory/'state.json',state)
        sweep(self.db,self.args,trigger='startup')
        self.assertEqual(self.db.import_content.call_count,1)

    def test_partial_assessment_history_and_dry_run_are_not_imported(self):
        directory,state,content=self.capture(1,task_type='assessment',assessment_complete=True,
            assessment_question_count=2,test_submission_status='completed',completion='You answered 1 of 2 questions correctly.')
        content['task_type']='assessment';atomic_json(directory/'content.json',content)
        self.assertFalse(eligible(directory,state,content))
        sweep(self.db,self.args,trigger='startup');self.db.import_content.assert_not_called()
        directory,_,_=self.capture(2)
        self.args.resume=directory;self.args.dry_run=True
        with patch('capture.Database',return_value=self.db),contextlib.redirect_stdout(io.StringIO()):
            run(self.args)
        self.db.import_content.assert_not_called()

    def test_failures_continue_and_do_not_launch_repairs_or_change_selection_state(self):
        bad,_,_ = self.capture(1)
        good,_,_ = self.capture(2)
        self.db.import_content.side_effect=[ReconciliationReview('historical learner use'),
                                          {'already_complete':True,'database_writes':0}]
        policy = self.args.state_dir/'perfect-retakes.json'
        atomic_json(policy,{'pending':{'lesson:1':{'task_id':1}}})
        original=policy.read_bytes()
        with patch('import_repair.repair') as repair:
            results=sweep(self.db,self.args,trigger='batch-end')
        repair.assert_not_called()
        self.assertEqual([r['status'] for r in results],['deferred','complete'])
        self.assertTrue(read_json(good/'state.json')['import_complete'])
        self.assertIn('historical',read_json(bad/'state.json')['deferred_error']['message'])
        self.assertEqual(policy.read_bytes(),original)

    def test_retries_survive_restart_and_reset_only_for_code_or_evidence(self):
        directory,state,_ = self.capture(1)
        self.db.import_content.side_effect=ValueError('unchanged conflict')
        sweep(self.db,self.args,trigger='startup')
        sweep(self.db,self.args,trigger='batch-end')
        restarted=arguments(['run','--state-dir',str(self.args.state_dir),'--output',str(self.args.output)])
        restarted.source = None  # Resume the same legacy import mode across restarts.
        sweep(self.db,restarted,trigger='startup')
        self.assertEqual(self.db.import_content.call_count,1)
        state=read_json(directory/'state.json');state['preview_complete']=False
        state['deferred_error']['message']='different diagnostics';atomic_json(directory/'state.json',state)
        sweep(self.db,self.args,trigger='batch-end')
        self.assertEqual(self.db.import_content.call_count,1)
        self.generation.return_value='native-v2'
        sweep(self.db,self.args,trigger='startup')
        self.assertEqual(self.db.import_content.call_count,2)
        (directory/'activity-metadata.json').write_text('[{"id":"question-1","difficulty":"M"}]')
        sweep(self.db,self.args,trigger='batch-end')
        self.assertEqual(self.db.import_content.call_count,3)

    def test_only_prior_source_evidence_for_matching_questions_resets_retries(self):
        self.capture(1)
        self.db.import_content.side_effect=ReconciliationReview('unknown provenance')
        sweep(self.db,self.args,trigger='startup')
        other,state,content=self.capture(2)
        proof={'committed':True,'reimport_is_noop':True,'learner_and_engine_facts_unchanged':True}
        atomic_json(other/'edb-import/verification.json',proof)
        (other/'edb-import/commit.edn').write_text(dumps({kw('edb/committed'):True}))
        sweep(self.db,self.args,trigger='batch-end')
        self.assertEqual(self.db.import_content.call_count,1)
        record=state['questions'].pop('q-2');record['content']['math_academy_id']='q-1'
        state['questions']['q-1']=record
        content['questions'][0]['math_academy_id']='q-1'
        atomic_json(other/'state.json',state);atomic_json(other/'content.json',content)
        atomic_json(other/'activity-metadata.json',[{'id':'question-1'}])
        sweep(self.db,self.args,trigger='batch-end')
        self.assertEqual(self.db.import_content.call_count,2)

    def test_changed_frozen_intent_is_deferred_without_commit_or_replan(self):
        directory,_,content=self.capture(1)
        self.intent(directory,content)
        target=directory/'edb-import'
        (target/'reconciliation.edn').write_text('{:altered true}')
        originals={p:p.read_bytes() for p in target.iterdir()}
        db=Database(self.args)
        with patch.object(db,'_commit') as commit,patch.object(db,'basis') as plan:
            result=sweep(db,self.args,trigger='startup')
        commit.assert_not_called();plan.assert_not_called()
        self.assertIn('reconciliation differs',result[0]['error'])
        for p,data in originals.items():self.assertEqual(p.read_bytes(),data)

    def test_created_intent_does_not_reset_unchanged_failure(self):
        directory,_,_ = self.capture(1)
        def fail(content,target,apply):
            atomic_json(target/'commit-intent.json',{'request_key':'frozen'})
            raise ValueError('commit unconfirmed')
        self.db.import_content.side_effect=fail
        sweep(self.db,self.args,trigger='startup')
        original=(directory/'edb-import/commit-intent.json').read_bytes()
        sweep(self.db,self.args,trigger='batch-end')
        self.assertEqual(self.db.import_content.call_count,1)
        self.assertEqual((directory/'edb-import/commit-intent.json').read_bytes(),original)

    def test_contention_retries_next_sweep_while_other_imports_continue(self):
        first,_,_=self.capture(1)
        self.capture(2)
        self.args.no_import_repair=False
        self.db.import_content.side_effect=[StaleBasis('busy database'),
            {'already_complete':True}, {'already_complete':True}]
        with patch('import_repair.repair') as repair:
            results=sweep(self.db,self.args,trigger='startup',repair_budget=0)
            self.assertEqual([r['status'] for r in results],['contention_pending','complete'])
            self.assertFalse(read_json(first/'state.json').get('import_complete'))
            results=sweep(self.db,self.args,trigger='batch-end',repair_budget=0)
            self.assertEqual([r['status'] for r in results],['complete'])
            self.assertTrue(read_json(first/'state.json')['import_complete'])
            repair.assert_not_called()
        self.assertEqual(self.db.import_content.call_count,3)

    def test_bound_and_one_attempt_each_per_sweep(self):
        for task in range(1,5):self.capture(task)
        self.db.import_content.side_effect=ValueError('unsupported')
        with patch('saved_imports.MAX_ATTEMPTS',2):
            self.assertEqual(len(sweep(self.db,self.args,trigger='startup')),2)
            self.assertEqual(len(sweep(self.db,self.args,trigger='batch-end')),2)
            self.assertEqual(sweep(self.db,self.args,trigger='startup'),[])
        self.assertEqual(self.db.import_content.call_count,4)

    def intent(self,directory,content,committed=False):
        target=directory/'edb-import';target.mkdir(exist_ok=True)
        tx=target/'transaction.edn';tx.write_text('[]\n')
        reconciliation=target/'reconciliation.edn';reconciliation.write_text('{}\n')
        intent={'database':self.args.database,'endpoint':self.args.endpoint,'basis':656,
                'sha256':hashlib.sha256(tx.read_bytes()).hexdigest(),'request_key':'original-request',
                'content_sha256':hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest(),
                'reconciliation_sha256':hashlib.sha256(reconciliation.read_bytes()).hexdigest()}
        atomic_json(target/'commit-intent.json',intent)
        receipt={kw('edb/committed'):True,kw('edb/db-before-t'):656,kw('edb/db-after-t'):657}
        if committed:(target/'commit.edn').write_text(dumps(receipt))
        return receipt,{p:p.read_bytes() for p in (tx,reconciliation,target/'commit-intent.json')}

    def test_committed_unverified_receipt_uses_existing_commit_path(self):
        directory,_,content=self.capture(1)
        receipt,originals=self.intent(directory,content,committed=True)
        db=Database(self.args)
        with patch.object(db,'command') as command,patch.object(db,'_verify',return_value={
                'committed':True,'reimport_is_noop':True}) as verify,patch.object(db,'basis') as plan:
            result=sweep(db,self.args,trigger='startup')
        self.assertEqual(result[0]['status'],'complete')
        command.assert_not_called();plan.assert_not_called()
        self.assertEqual(verify.call_args.args[0],receipt)
        for p,data in originals.items():self.assertEqual(p.read_bytes(),data)

    def test_unresolved_intent_replays_original_request_and_never_replans(self):
        directory,_,content=self.capture(1)
        receipt,originals=self.intent(directory,content)
        db=Database(self.args)
        with patch.object(db,'command',return_value=dumps(receipt)) as command, \
             patch.object(db,'_verify',return_value={'committed':True}) as verify, \
             patch.object(db,'basis') as plan:
            sweep(db,self.args,trigger='startup')
        plan.assert_not_called();verify.assert_called_once()
        self.assertEqual(command.call_args.args[0],'transact')
        self.assertIn('original-request',command.call_args.args)
        self.assertIn(656,command.call_args.args)
        for p,data in originals.items():self.assertEqual(p.read_bytes(),data)

    def test_preview_of_pending_intent_never_commits_or_marks_verified(self):
        directory,_,content=self.capture(1)
        _,originals=self.intent(directory,content)
        self.args.preview=True
        db=Database(self.args)
        with patch.object(db,'_commit') as commit,patch.object(db,'basis') as plan:
            result=sweep(db,self.args,trigger='startup')
        commit.assert_not_called();plan.assert_not_called()
        self.assertEqual(result[0]['status'],'deferred')
        self.assertFalse(read_json(directory/'state.json').get('preview_complete'))
        for p,data in originals.items():self.assertEqual(p.read_bytes(),data)

    def test_preview_and_apply_have_separate_retry_keys(self):
        directory,_,_=self.capture(1)
        self.args.preview=True;self.db.import_content.return_value={'previewed':True}
        sweep(self.db,self.args,trigger='startup')
        self.assertFalse(self.db.import_content.call_args.args[2])
        self.assertTrue(read_json(directory/'state.json')['preview_complete'])
        self.assertFalse(read_json(directory/'state.json').get('import_complete'))
        self.args.preview=False;self.db.import_content.return_value={'already_complete':True,'database_writes':0}
        sweep(self.db,self.args,trigger='startup')
        self.assertTrue(self.db.import_content.call_args.args[2])
        self.assertEqual(self.db.import_content.call_count,2)

    def test_active_assessment_and_shutdown_prevent_sweeps(self):
        self.capture(1)
        directory,_,_=self.capture(2,task_type='assessment',assessment_started=True,activity_complete=False)
        self.assertEqual(sweep(self.db,self.args,trigger='startup'),[])
        self.db.import_content.assert_not_called()
        (directory/'state.json').unlink()
        self.args.stop_event=threading.Event();self.args.stop_event.set()
        with self.assertRaises(KeyboardInterrupt):sweep(self.db,self.args,trigger='batch-end')
        self.db.import_content.assert_not_called()

    def test_expired_completed_quiz_does_not_block_other_imports(self):
        pending,_,_=self.capture(1)
        expired,state,content=self.capture(2,task_type='assessment',assessment_started=True,
            assessment_complete=True,assessment_question_count=9,test_submission_status='expired',
            completion='Quiz 7 expired; 0 of 9 answered; -1/15 XP.')
        content['task_type']='assessment';atomic_json(expired/'content.json',content)
        # This partial expired capture is not itself eligible for import, but
        # its terminal state must not hold up the completed lesson's import.
        self.assertFalse(eligible(expired,state,content))
        results=sweep(self.db,self.args,trigger='batch-end')
        self.assertEqual(len(results),1)
        self.assertEqual(self.db.import_content.call_args.args[1].parent,pending)

    def test_expired_status_without_completion_still_blocks_sweep(self):
        self.capture(1)
        self.capture(2,task_type='assessment',assessment_started=True,
            activity_complete=False,assessment_complete=False,test_submission_status='expired',
            assessment_question_count=9,completion='Quiz 7 expired; 0 of 9 answered.')
        self.assertEqual(sweep(self.db,self.args,trigger='startup'),[])
        self.db.import_content.assert_not_called()

    def test_completed_pending_capture_never_resumes_browser_and_startup_runs_at_limit(self):
        self.capture(1)
        self.assertIsNone(unfinished_run(self.args))
        checkpoint=self.root/'batch.json';atomic_json(checkpoint,{'attempted':2,'limit':2})
        self.args.batch_checkpoint=checkpoint;self.args.limit=2
        with patch('capture.Database',return_value=self.db):run(self.args)
        self.assertEqual(self.db.import_content.call_count,1)
        self.assertFalse(self.args.profile.exists())

    def test_queue_after_failure_is_imported_at_batch_end_without_consuming_live_limit(self):
        self.capture(1)
        self.args.limit=2;self.args.preview=True;self.args.rest_every=0
        self.args.lesson_min=self.args.lesson_max=0
        selected=[];queue_reads=[];owner=self
        queue=[{'task_id':i,'topic_id':i,'task_type':'lesson','title':'Lesson',
                'href':'/tasks/'+str(i)+'/topics/'+str(i)+'/lesson'} for i in (2,3)]
        class Browser:
            def __init__(self,page,*args):self.page=page;self.http_block=None
            def queue(self):
                queue_reads.append(1)
                if len(queue_reads)==2:raise ValueError('queue-after unavailable')
                return [q for q in queue if q['task_id'] not in selected]
            def start(self,item):selected.append(item['task_id'])
            def activity(self,state,*args):state['activity_complete']=True
            def history(self,state,directory,*args):
                _,saved,content=owner.capture(state['task_id'])
                state.update(saved);state.pop('deferred_error',None)
                atomic_json(directory/'state.json',state)
                return content
            def current_step(self):return None
        page=Mock();page.url='offline';page.content.return_value='<div>offline fixture</div>'
        page.screenshot.side_effect=lambda **kwargs:Path(kwargs['path']).write_bytes(b'fixture')
        runtime=Mock();runtime.__enter__=Mock(return_value=runtime);runtime.__exit__=Mock(return_value=False)
        runtime.chromium.launch_persistent_context.return_value=SimpleNamespace(pages=[page],route=Mock(),close=Mock())
        self.db.priorities.return_value={};self.db.topic.return_value={}
        def import_content(content,*args):
            if content['task_id']==1:raise ReconciliationReview('unknown provenance')
            return {'previewed':True}
        self.db.import_content.side_effect=import_content
        with patch('capture.Database',return_value=self.db),patch('browser.CaptureBrowser',Browser), \
             patch('playwright.sync_api.sync_playwright',return_value=runtime),contextlib.redirect_stdout(io.StringIO()):
            run(self.args)
        self.assertEqual(selected,[2,3])
        self.assertEqual([call.args[0]['task_id'] for call in self.db.import_content.call_args_list],[1,3,2])
        recovered=read_json(self.args.output/'2/state.json')
        self.assertTrue(recovered['preview_complete']);self.assertNotIn('deferred_error',recovered)

    def test_completed_batch_resume_is_content_only_and_keeps_remaining_activity_limit(self):
        older,_,_=self.capture(1)
        checkpoint=self.root/'batch.json'
        atomic_json(checkpoint,{'attempted':1,'limit':2,'next_resume':str(older),
                    'captured_tasks':[1],'completed_topics':[1]})
        self.args.batch_checkpoint=checkpoint;self.args.limit=2;self.args.preview=True
        selected=[];owner=self
        class Browser:
            def __init__(self,*args):pass
            def queue(self):
                return [] if selected else [{'task_id':2,'topic_id':2,'task_type':'lesson','title':'Lesson',
                                             'href':'/tasks/2/topics/2/lesson'}]
            def start(self,item):selected.append(item['task_id'])
            def activity(self,state,*args):
                self.assert_live(state)
            @staticmethod
            def assert_live(state):
                if state['task_id'] != 2:raise AssertionError('Completed import resumed as an activity')
            def history(self,state,directory,*args):
                _,saved,content=owner.capture(state['task_id']);state.update(saved)
                return content
        runtime=Mock();runtime.__enter__=Mock(return_value=runtime);runtime.__exit__=Mock(return_value=False)
        runtime.chromium.launch_persistent_context.return_value=SimpleNamespace(pages=[Mock()],route=Mock(),close=Mock())
        self.db.priorities.return_value={};self.db.topic.return_value={}
        self.db.import_content.return_value={'previewed':True}
        with patch('capture.Database',return_value=self.db),patch('browser.CaptureBrowser',Browser), \
             patch('playwright.sync_api.sync_playwright',return_value=runtime),contextlib.redirect_stdout(io.StringIO()):
            run(self.args)
        self.assertEqual(selected,[2])
        self.assertEqual([call.args[0]['task_id'] for call in self.db.import_content.call_args_list],[1,2])


if __name__ == '__main__':unittest.main()
