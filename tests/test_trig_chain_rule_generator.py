"""Answer notation must not add an untaught identity after the solution ends."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'trig_validation', ROOT / 'generate/scratch/17592186064281/validate.py')
validation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validation)
generator = validation.g


class TrigAnswerPresentationTests(unittest.TestCase):
    def test_reported_question_keeps_the_solution_form(self):
        question = generator.generate('moderate', 0, 'q-31163', 12)['question']
        self.assertEqual(question[':question/id'], 'edc669f2-8811-573d-b7ea-ebf03a0592e1')
        field = question[':question/answer-fields'][0]
        correct = next(a for a in field[':answer-field/choices']
                       if a[':answer/id'] == field[':answer-field/correct'][1])
        self.assertEqual(correct[':answer/id'], 'ef497264-895e-54be-869a-0733bc78f89e')
        self.assertEqual(correct[':answer/value'], r'2\sin(12-2x)-18x^{2}')
        validation.solution_check(question)
        validation.representation_check(question)

    def test_equivalent_but_unexplained_rewrite_fails(self):
        question = generator.generate('moderate', 0, 'q-31163', 12)['question']
        field = question[':question/answer-fields'][0]
        for answer in field[':answer-field/choices']:
            if answer[':answer/id'] == field[':answer-field/correct'][1]:
                answer[':answer/value'] = r'-18x^{2}-2\sin(2x-12)'
        # This is the old blind spot: the mathematical solution check passes.
        validation.solution_check(question)
        with self.assertRaisesRegex(AssertionError, 'Unexplained trig argument rewrite'):
            validation.representation_check(question)

    def test_unchanged_argument_but_unshown_final_conversion_fails(self):
        question = generator.generate('moderate', 0, 'q-31163', 12)['question']
        field = question[':question/answer-fields'][0]
        for answer in field[':answer-field/choices']:
            if answer[':answer/id'] == field[':answer-field/correct'][1]:
                answer[':answer/value'] = r'2(\sin(12-2x)-9x^{2})'
        validation.solution_check(question)
        with self.assertRaisesRegex(AssertionError, 'Keyed choice differs from final solution form'):
            validation.representation_check(question)


if __name__ == '__main__':
    unittest.main()
