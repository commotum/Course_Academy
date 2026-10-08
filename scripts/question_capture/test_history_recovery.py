"""Recover six broken history aliases using their actual saved live graphics."""
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import Mock
from browser import CaptureBrowser, history_asset_bindings
from capture import superseded_before_start

ROOT = Path(__file__).resolve().parents[2]/'reference/mathacademy'
CASES = [('question-capture', '13956996', 'q-249864'),
         ('question-capture', '13965374', 'q-270802'),
         ('question-capture', '14004892', 'q-277261'),
         ('question-capture', '14013930', 'q-278239'),
         ('question-capture', '13980994', 'q-211004'),
         ('question-capture-workers/linear', '14035971', 'q-181522')]


class HistoryRecoveryTests(unittest.TestCase):
    def test_only_empty_prestart_capture_can_be_closed_as_superseded(self):
        state = {'questions':{}, 'examples':{}, 'source_recovery':{
            'resolution':'verified_superseded_before_start', 'superseded_by_captured_task':2}}
        self.assertTrue(superseded_before_start(state))
        for key in ('questions', 'examples'):
            changed = copy.deepcopy(state)
            changed[key]['q-1'] = {'problem':'captured evidence'}
            self.assertFalse(superseded_before_start(changed))
        state['source_recovery'].pop('resolution')
        self.assertFalse(superseded_before_start(state))

    def test_closed_prestart_diagnostic_is_not_repaired_again(self):
        import tempfile
        from types import SimpleNamespace
        from capture_repair import next_failure
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            directory = root/'captures/1'
            error = directory/'diagnostics/1/error.json'
            error.parent.mkdir(parents=True)
            error.write_text(json.dumps({'phase':'start','exception_type':'TimeoutError','task_id':1}))
            (directory/'state.json').write_text(json.dumps({'questions':{},'examples':{},'source_recovery':{
                'resolution':'verified_superseded_before_start','superseded_by_captured_task':2}}))
            args = SimpleNamespace(output=root/'captures',state_dir=root/'state',edb_bin='unused')
            self.assertIsNone(next_failure(args, {}))

    def examples(self):
        for root, task, mid in CASES:
            directory = ROOT/root/task
            record = json.loads((directory/'state.json').read_text())['questions'][mid]
            saved = directory/'history-recovery'/('history-'+mid+'.json')
            incoming = json.loads((saved if saved.exists() else directory/('history-'+mid+'.json')).read_text())
            yield mid, incoming, record

    def test_actual_history_aliases_reuse_original_question_assets(self):
        for mid, incoming, record in self.examples():
            with self.subTest(question=mid):
                binding = history_asset_bindings(incoming, record, mid)
                self.assertEqual(len(binding), 1)
                self.assertTrue(Path(binding[0][1]['path']).is_file())

    def test_different_question_solution_and_missing_bytes_do_not_match(self):
        mid, incoming, record = next(self.examples())
        self.assertEqual(history_asset_bindings(incoming, record, 'q-999'), [])
        changed = copy.deepcopy(incoming)
        changed['worked_solution'] += ' A different result.'
        self.assertEqual(history_asset_bindings(changed, record, mid), [])
        changed = copy.deepcopy(record)
        changed['after']['assets'][0]['sha256'] = 'bad'
        self.assertEqual(history_asset_bindings(incoming, changed, mid), [])

    def test_route_callback_accepts_playwright_request_argument(self):
        mid, incoming, record = next(self.examples())
        player = Mock()
        explanation = Mock()
        explanation.evaluate.return_value = incoming
        registered = []
        player.page.route.side_effect = lambda url, handler: registered.append(handler)
        directory = ROOT/'question-capture'/'13956996'
        import tempfile
        with tempfile.TemporaryDirectory() as temporary:
            CaptureBrowser.read_history(player, explanation, record, Path(temporary), mid)
        route = Mock()
        registered[0](route, Mock())
        self.assertTrue(route.fulfill.call_args.kwargs['body'])
        player.page.unroute.assert_called_once()
