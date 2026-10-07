"""Source evidence and repaired code reopen import diagnosis without DB mutations."""
import json
import unittest
from unittest.mock import patch

import test_import_repair as fixtures
from core import atomic_json
from import_repair import conflicting_pair, repair, repair_generation


class ImportJudgmentTests(unittest.TestCase):
    def fixture(self):
        fixture=fixtures.ImportRepairTests();fixture.setUp();self.addCleanup(fixture.tearDown)
        directory=fixture.root/'1';directory.mkdir()
        return fixture,directory

    def test_conflicting_pair_ignores_native_checker_diagnostic_suffix(self):
        for suffix in ('','; comparison unresolved: no native proof','; comparison different: powers differ'):
            pair=conflicting_pair(ValueError("Correct answer conflict: q-1/selection; stored 'x^2', captured 'x^{2}'"+suffix))
            self.assertEqual(pair,{'x^2','x^{2}'})
        self.assertIsNone(conflicting_pair(ValueError('Question metadata needs review')))

    def test_attempt_limit_applies_to_current_repair_generation_only(self):
        fixture,directory=self.fixture()
        with patch('import_repair.repair_generation',side_effect=['old','old','old','new']), \
             patch('import_repair.run_cli',side_effect=fixture.fake_cli) as model:
            for _ in range(4):self.assertFalse(repair(fixture.args,directory,ValueError('Conflict')))
        self.assertEqual(model.call_count,3)
        record=json.loads((directory/'import-repair.json').read_text())
        self.assertEqual([attempt['generation'] for attempt in record['attempts']],['old','old','new'])

    def test_new_authentic_content_reopens_previously_exhausted_activity(self):
        fixture,directory=self.fixture()
        atomic_json(directory/'content.json',{'task_id':1,'questions':[{'worked_solution':'Old evidence'}]})
        generation=repair_generation(directory)
        with patch('import_repair.run_cli',side_effect=fixture.fake_cli) as model:
            for _ in range(3):self.assertFalse(repair(fixture.args,directory,ValueError('Conflict')))
            self.assertEqual(model.call_count,2)
            atomic_json(directory/'content.json',{'task_id':1,'questions':[{'worked_solution':'Authentic complete worked solution'}]})
            self.assertNotEqual(repair_generation(directory),generation)
            self.assertFalse(repair(fixture.args,directory,ValueError('Conflict')))
            self.assertEqual(model.call_count,3)

    def test_interrupted_repair_without_session_identity_restarts_read_only_diagnosis(self):
        fixture,directory=self.fixture();root=fixture.args.state_dir/'import-repair';root.mkdir(parents=True)
        atomic_json(root/'session.json',{'session_id':None,'pending_turn':{'events':str(root/'missing-events.jsonl')}})
        with patch('import_repair.run_cli',side_effect=fixture.fake_cli):
            self.assertFalse(repair(fixture.args,directory,ValueError('Conflict')))
        state=json.loads((root/'session.json').read_text())
        self.assertEqual(state['session_id'],fixture.sid)
        self.assertEqual(len(state['interrupted_turns']),1)
        self.assertEqual(fixture.commands[0][fixture.commands[0].index('--sandbox')+1],'read-only')


if __name__=='__main__':unittest.main()
