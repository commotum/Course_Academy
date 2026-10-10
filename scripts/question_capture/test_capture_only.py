"""Capture continues across activities without planning or publishing EDB writes."""
import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import fleet
from capture import arguments, run
from core import atomic_json
from database import Database
from import_repair import import_with_repair
from saved_imports import sweep
import test_adaptive_run


class CaptureOnlyTests(unittest.TestCase):
    def test_fleet_default_and_explicit_option_reach_capture_process(self):
        data = fleet.config()
        for worker in data['workers']:
            args = arguments(fleet.worker_command(data,worker)[3:])
            self.assertFalse(args.capture_only)
            self.assertEqual(args.database, 'math')
            self.assertEqual(args.source, ':org/Math-Academy')
            self.assertEqual(args.math_root, Path('/media/jake/SSD/EDB/math'))
        data['capture_only'] = True
        self.assertTrue(arguments(fleet.worker_command(data,data['workers'][0])[3:]).capture_only)
        data['capture_only'] = False
        worker = data['workers'][0]
        self.assertFalse(arguments(fleet.worker_command(data,worker)[3:]).capture_only)
        self.assertTrue(arguments(fleet.worker_command(data,worker,capture_only=True)[3:]).capture_only)

    def test_import_commands_and_preview_cannot_misuse_capture_only(self):
        for argv in (['sweep-saved'], ['import-saved','--content','unused.json'], ['run','--preview']):
            with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
                arguments([*argv,'--capture-only'])

    def test_database_guard_blocks_even_direct_imports_before_artifact_changes(self):
        db = Database(arguments(['run','--capture-only']))
        with patch('database.subprocess.run') as process:
            for command in ('transact','with','create','consolidate'):
                with self.assertRaisesRegex(RuntimeError,'read-only'):
                    db.command(command)
            with self.assertRaisesRegex(RuntimeError,'disabled'):
                db.import_content({},Path('/unused'),True)
            process.assert_not_called()
            db.command('status')
            process.assert_called_once()

    def test_sweep_skips_old_pending_intents_and_all_bookkeeping(self):
        args = arguments(['run','--capture-only'])
        db = Mock()
        with patch('saved_imports.version',side_effect=AssertionError('sweep must not start')):
            self.assertEqual(sweep(db,args,trigger='startup'),[])
        db.import_content.assert_not_called()

    def test_deferred_capture_does_not_modify_existing_commit_intent(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            args = arguments(['run','--capture-only','--state-dir',str(root/'state')])
            directory = root/'capture'
            atomic_json(directory/'content.json',{'task_id':1,'questions':[]})
            atomic_json(directory/'edb-import/commit-intent.json',{'pending':'retain exactly'})
            intent = (directory/'edb-import/commit-intent.json').read_bytes()
            db = Mock()
            state = {'task_id':1,'activity_complete':True,'history_complete':True}
            result = import_with_repair(db,json.loads((directory/'content.json').read_text()),directory,state,args)
            self.assertTrue(result['deferred'])
            self.assertEqual(result['content_sha256'],hashlib.sha256((directory/'content.json').read_bytes()).hexdigest())
            self.assertEqual((directory/'edb-import/commit-intent.json').read_bytes(),intent)
            self.assertTrue(state['import_deferred'])
            self.assertNotIn('import_complete',state)
            db.import_content.assert_not_called()

    def test_two_activities_save_content_and_continue_with_real_deferral_and_sweeps(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            args = arguments(['run','--capture-only','--limit','2','--no-capture-repair',
                              '--lesson-min','0','--lesson-max','0',
                              '--state-dir',str(root/'state'),'--output',str(root/'capture')])
            browser,runtime,db,selected = test_adaptive_run.AdaptiveRunTests().fixture(work,[1,2])
            db.import_content.side_effect = AssertionError('Capture must never import')
            with patch('capture.Database',return_value=db),patch('browser.CaptureBrowser',browser), \
                 patch('playwright.sync_api.sync_playwright',return_value=runtime), \
                 patch('saved_imports.version',side_effect=AssertionError('No backlog sweep')), \
                 contextlib.redirect_stdout(io.StringIO()):
                run(args)
            self.assertEqual(selected,[1,2])
            db.import_content.assert_not_called()
            for task in (1,2):
                directory = args.output/str(task)
                state = json.loads((directory/'state.json').read_text())
                self.assertTrue(state['activity_complete'] and state['history_complete'])
                self.assertTrue(state['import_deferred'])
                self.assertNotIn('import_complete',state)
                self.assertTrue((directory/'content.json').is_file())
                self.assertTrue((directory/'import-deferred.json').is_file())
                self.assertFalse((directory/'edb-import').exists())


if __name__ == '__main__':
    unittest.main()
