import copy
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import solver
from solver import Solver, recheck_invalid_choice

ROOT = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/linear/14042906')
QUESTION = ROOT / 'q-108966'


class InvalidMatrixChoiceRecoveryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root/'state.json').write_bytes((ROOT/'state.json').read_bytes())
        self.question = self.root / QUESTION.name
        self.question.mkdir()
        self.item = json.loads((QUESTION / 'solve-before-exact-choice-input.json').read_text())
        self.saved = json.loads((QUESTION / 'solve-before-exact-choice-answer.json').read_text())
        (self.question/'solve-input.json').write_text(json.dumps(self.item))
        (self.question/'solve-answer.json').write_text(json.dumps(self.saved))
        session = self.root/'solver-session'
        session.mkdir()
        (session/'state.json').write_bytes((ROOT/'solver-session/state.json').read_bytes())

    def test_original_failure_and_retry_eligibility(self):
        with self.assertRaisesRegex(ValueError, 'exact displayed choice'):
            Solver.validate(self.item, self.saved)
        self.assertTrue(recheck_invalid_choice(self.item, self.saved))
        self.assertNotIn('exact_choice_retry', self.item)

    def test_one_correction_turn_uses_existing_session_and_archives(self):
        corrected = copy.deepcopy(self.saved)
        choice = next(c for c in self.item['fields'][0]['choices'] if c['option'] == 'b')
        corrected['answers'][0]['correct_value'] = choice['value']
        runner = Solver(SimpleNamespace(solver_command=None))
        session = json.loads((self.root / 'solver-session/state.json').read_text())
        identity = session['activity']
        with patch.object(runner, 'recover_pending'), \
             patch.object(runner, 'activity_context', return_value=(identity, [])), \
             patch.object(runner, 'codex_turn', return_value=corrected) as turn, \
             patch.object(solver, 'atomic_json') as write:
            result = runner.solve(self.item, None, self.question)
        self.assertEqual(result, corrected)
        turn.assert_called_once()
        payload, screenshot, directory, phase, session_file, reused_session, keys = turn.call_args.args
        self.assertEqual(reused_session['session_id'], session['session_id'])
        self.assertEqual(reused_session['context_keys'], session['context_keys'])
        self.assertEqual(payload['exact_choice_retry'], 1)
        self.assertIn('exact displayed choice', payload['validation_feedback'])
        self.assertEqual(payload['fields'], self.item['fields'])
        archives = {str(c.args[0]): c.args[1] for c in write.call_args_list}
        self.assertEqual(archives[str(self.question / 'solve-before-exact-choice-answer.json')], self.saved)
        self.assertEqual(archives[str(self.question / 'solve-before-exact-choice-input.json')], self.item)

    def test_retry_is_bounded(self):
        previous = copy.deepcopy(self.item)
        previous['exact_choice_retry'] = 1
        self.assertFalse(recheck_invalid_choice(previous, self.saved))
        with self.assertRaises(ValueError):
            Solver.reuse_answer(self.item, self.saved)

    def test_uncertainty_is_not_overridden(self):
        uncertain = copy.deepcopy(self.saved)
        uncertain['confident'] = False
        self.assertFalse(recheck_invalid_choice(self.item, uncertain))
        with self.assertRaisesRegex(ValueError, 'Solver is uncertain'):
            Solver.validate(self.item, uncertain)

    def test_incorrect_correction_still_fails_validation(self):
        altered = copy.deepcopy(self.saved)
        altered['answers'][0]['correct_value'] = self.item['fields'][0]['choices'][0]['value']
        with self.assertRaisesRegex(ValueError, 'exact displayed choice'):
            Solver.validate(self.item, altered)


if __name__ == '__main__':
    unittest.main()
