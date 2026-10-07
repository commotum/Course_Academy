"""Persistent import repair integration without model or website calls."""
import json
import subprocess
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import Mock,patch
from capture import arguments
from core import atomic_json
from import_repair import import_with_repair,repair

class ImportRepairTests(unittest.TestCase):
    def setUp(self):
        self.work=tempfile.TemporaryDirectory();self.root=Path(self.work.name)
        self.args=arguments(['run','--state-dir',str(self.root/'state'),'--output',str(self.root/'captures')])
        self.sid=str(uuid.uuid4());self.commands=[]
        self.result={'status':'blocked','summary':'Genuine answer conflict needs source evidence.',
                     'edits':[],'equivalent':[],'distinct':[]}
    def tearDown(self):self.work.cleanup()
    def test_saved_commit_intent_bypasses_model_repair(self):
        directory=self.root/'1';(directory/'edb-import').mkdir(parents=True)
        atomic_json(directory/'edb-import/commit-intent.json',{'basis':657})
        error=subprocess.CalledProcessError(1,['edb'],stderr='query/value-byte-limit')
        db=Mock();db.import_content.side_effect=error
        with patch('import_repair.repair') as repair:
            with self.assertRaises(subprocess.CalledProcessError):
                import_with_repair(db,{'task_id':1},directory,
                    {'activity_complete':True,'history_complete':True},self.args)
        repair.assert_not_called()
    def fake_cli(self,command,**kwargs):
        self.commands.append(command);kwargs['started'](123456789)
        Path(command[command.index('--output-last-message')+1]).write_text(json.dumps(self.result))
        events='\n'.join(json.dumps(e) for e in ({'type':'thread.started','thread_id':self.sid},{'type':'turn.completed'}))
        kwargs['events_path'].write_text(events)
        return subprocess.CompletedProcess(command,0,stdout=events,stderr='')
    def test_two_failed_activities_reuse_one_read_only_session(self):
        with patch('import_repair.run_cli',side_effect=self.fake_cli):
            for task in ('1','2'):
                directory=self.root/task;directory.mkdir()
                atomic_json(directory/'content.json',{'task_id':int(task)})
                self.assertFalse(repair(self.args,directory,ValueError('Correct answer conflict: q-1')))
        self.assertNotIn('resume',self.commands[0]);self.assertIn('resume',self.commands[1])
        self.assertEqual(self.commands[1][-2],self.sid)
        self.assertTrue(all(c[c.index('--sandbox')+1]=='read-only' for c in self.commands))
    def test_blocked_failure_is_bounded_across_restarts(self):
        directory=self.root/'1';directory.mkdir()
        with patch('import_repair.run_cli',side_effect=self.fake_cli) as cli:
            for _ in range(3):self.assertFalse(repair(self.args,directory,ValueError('Conflict')))
            self.assertEqual(cli.call_count,2)
    def test_success_skips_repair_and_failure_retries_original_content(self):
        db=Mock();content={'task_id':1};state={'activity_complete':True,'history_complete':True}
        with patch('import_repair.repair',return_value=True) as fix:
            db.import_content.return_value={'committed':True}
            self.assertEqual(import_with_repair(db,content,self.root,state,self.args),{'committed':True})
            fix.assert_not_called();db.import_content.reset_mock()
            db.import_content.side_effect=[ValueError('Conflict'),{'committed':True}]
            self.assertEqual(import_with_repair(db,content,self.root,state,self.args),{'committed':True})
            self.assertEqual(db.import_content.call_count,2)
            self.assertTrue(all(c.args[0] is content for c in db.import_content.call_args_list))
    def test_incomplete_captures_disabled_repairs_and_pending_commits_are_not_changed(self):
        db=Mock();db.import_content.side_effect=ValueError('Conflict')
        with patch('import_repair.repair') as fix:
            for state in ({},{'activity_complete':True}):
                with self.assertRaises(ValueError):import_with_repair(db,{},self.root,state,self.args)
            self.args.no_import_repair=True
            with self.assertRaises(ValueError):import_with_repair(db,{},self.root,{'activity_complete':True,'history_complete':True},self.args)
            fix.assert_not_called()
        directory=self.root/'pending';directory.mkdir();(directory/'edb-import').mkdir()
        intent=directory/'edb-import/commit-intent.json';intent.write_text('original intent')
        self.result['status']='retry'
        with patch('import_repair.run_cli',side_effect=self.fake_cli):
            self.assertFalse(repair(self.args,directory,ValueError('Commit unconfirmed')))
        self.assertEqual(intent.read_text(),'original intent')
    def test_repair_failure_preserves_original_import_error(self):
        db=Mock();original=ValueError('Correct answer conflict');db.import_content.side_effect=original
        with patch('import_repair.repair',side_effect=RuntimeError('Codex unavailable')):
            with self.assertRaises(ValueError) as raised:
                import_with_repair(db,{},self.root,{'activity_complete':True,'history_complete':True},self.args)
        self.assertIs(raised.exception,original)
    def test_retry_diagnosis_keeps_source_and_original_commit_checks(self):
        directory=self.root/'retry';directory.mkdir();self.result['status']='retry'
        with patch('import_repair.run_cli',side_effect=self.fake_cli):
            self.assertTrue(repair(self.args,directory,ValueError('Database basis changed')))
        self.assertEqual(json.loads((directory/'import-repair.json').read_text())['attempts'][0]['status'],'retry')

    def test_proposed_patch_is_checked_offline_and_applied_only_to_normalizer(self):
        import import_repair
        directory=self.root/'candidate';directory.mkdir()
        source=self.root/'math_notation.py';source.write_text(import_repair.NORMALIZER.read_text())
        old='Structural identities for common displayed math notation, without algebra.'
        self.result={'status':'repair','summary':'Verified notation fix.',
                     'edits':[{'old':old,'new':old+' Tested.'}],
                     'equivalent':[{'left':r'\sin(x)','right':r'\operatorname{sin}(x)'}],
                     'distinct':[{'left':'x+1','right':'x-1'},{'left':'x^2','right':'x^3'},
                                 {'left':r'\sin(x)','right':r'\cos(x)'}]}
        with patch('import_repair.NORMALIZER',source),patch('import_repair.run_cli',side_effect=self.fake_cli):
            self.assertTrue(repair(self.args,directory,ValueError('Notation conflict')))
        self.assertIn(old+' Tested.',source.read_text())
        record=json.loads((directory/'import-repair.json').read_text())
        self.assertEqual(record['attempts'][0]['status'],'applied')
        count=unittest.defaultTestLoader.loadTestsFromNames(
            ['test_capture.PolicyTests','test_capture.ReconciliationTests']).countTestCases()
        self.assertIn(f'Ran {count} tests',(Path(record['attempts'][0]['job'])/'tests.txt').read_text())

    def test_failing_candidate_is_kept_for_review_and_source_is_not_changed(self):
        import import_repair
        directory=self.root/'bad';directory.mkdir()
        source=self.root/'math_notation.py';original=import_repair.NORMALIZER.read_text();source.write_text(original)
        self.result={'status':'repair','summary':'Unsafe candidate.',
                     'edits':[{'old':"return repr(('math',nodes) if preserve_form else scalar_identity(nodes)", 'new':'return repr(None'}],
                     'equivalent':[{'left':'x','right':'y'}],
                     'distinct':[{'left':str(i),'right':str(i+1)} for i in range(3)]}
        with patch('import_repair.NORMALIZER',source),patch('import_repair.run_cli',side_effect=self.fake_cli):
            with self.assertRaisesRegex(ValueError,'failed offline regression'):
                repair(self.args,directory,ValueError('Notation conflict'))
        self.assertEqual(source.read_text(),original)

if __name__=='__main__':unittest.main()
