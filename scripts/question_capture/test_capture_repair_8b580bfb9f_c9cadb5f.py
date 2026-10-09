import ast
import copy
import json
import unittest
from fractions import Fraction
from pathlib import Path
from unittest.mock import Mock

import solver
from solver import Solver

ROOT = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/linear/14059591/q-140043')


def determinant(a):
    return (a[0][0] * (a[1][1]*a[2][2] - a[1][2]*a[2][1])
            - a[0][1] * (a[1][0]*a[2][2] - a[1][2]*a[2][0])
            + a[0][2] * (a[1][0]*a[2][1] - a[1][1]*a[2][0]))


class IndependentVerificationRetryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = json.loads((ROOT / 'verify-before-independent-input.json').read_text())
        cls.saved = json.loads((ROOT / 'verify-before-independent-answer.json').read_text())
        tree = ast.parse(Path(solver.__file__).read_text())
        method = next(n for n in ast.walk(tree)
                      if isinstance(n, ast.FunctionDef) and n.name == 'solve')
        branch = next(n for n in ast.walk(method) if isinstance(n, ast.If)
                      and any(isinstance(c, ast.Name) and c.id == 'phase' for c in ast.walk(n.test))
                      and any(isinstance(c, ast.Constant) and c.value == 'verification_retry'
                              for c in ast.walk(n.test)))
        # Isolate the real retry branch: no solver process or filesystem writes.
        branch = copy.deepcopy(branch)
        branch.orelse = []
        cls.code = compile(ast.fix_missing_locations(
            ast.Module(body=[branch], type_ignores=[])), '<verification-retry>', 'exec')

    def test_original_failure_and_independent_arithmetic(self):
        with self.assertRaisesRegex(ValueError, 'Solver is uncertain'):
            Solver.validate(self.original, self.saved)
        self.assertIn('6x+5y-3z=2', self.original['problem'])
        self.assertIn('4x-5y+kz=1', self.original['problem'])
        self.assertIn('-2x+10y-5z=-2', self.original['problem'])
        self.assertIn('160-70k', self.original['problem'])
        for k in (-4, 0, 1, 2, 9, 11):
            self.assertEqual(determinant([[6,5,-3], [4,-5,k], [-2,10,-5]]), 160-70*k)
        x, y, z = Fraction(1,2), Fraction(2,5), Fraction(1)
        self.assertEqual((6*x+5*y-3*z, 4*x-5*y+z, -2*x+10*y-5*z), (2,1,-2))
        self.assertIn('6 & 5 & -2', self.original['worked_solution'])

    def execute_branch(self, original=None, phase='verify', saved=None):
        payload = {}
        write = Mock()
        namespace = {'phase': phase, 'saved': self.saved if saved is None else saved,
                     'original': self.original if original is None else original,
                     'payload': payload, 'directory': ROOT, 'atomic_json': write}
        exec(self.code, namespace)
        return payload, write

    def test_retry_archives_evidence_and_requests_independent_check(self):
        payload, write = self.execute_branch()
        self.assertEqual(payload['verification_retry'], 1)
        self.assertIn('independently', payload['validation_feedback'])
        self.assertIn('Preserve uncertainty', payload['validation_feedback'])
        archived = {str(c.args[0]): c.args[1] for c in write.call_args_list}
        self.assertEqual(archived[str(ROOT / 'verify-before-independent-answer.json')], self.saved)
        self.assertEqual(archived[str(ROOT / 'verify-before-independent-input.json')], self.original)

    def test_retry_is_bounded_and_verify_only(self):
        marked = {**self.original, 'verification_retry': 1}
        for original, phase in ((marked, 'verify'), (self.original, 'solve')):
            payload, write = self.execute_branch(original, phase)
            self.assertEqual(payload, {})
            write.assert_not_called()

    def test_uncertain_retry_result_still_fails(self):
        self.execute_branch()
        with self.assertRaisesRegex(ValueError, 'Solver is uncertain'):
            Solver.validate(self.original, self.saved)

    def test_confident_mismatched_choice_still_fails(self):
        invalid = copy.deepcopy(self.saved)
        invalid['confident'] = True
        invalid['answers'][0].update(correct_option='e', correct_value='k=2', value_type='math')
        with self.assertRaisesRegex(ValueError, 'exact displayed choice'):
            Solver.validate(self.original, invalid)


if __name__ == '__main__':
    unittest.main()
