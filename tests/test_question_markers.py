import copy
import unittest

from scripts.question_markers import misplaced_markers, repair_problem, validate_prompt_markers


def field(key, kind):
    return {':answer-field/key': key, ':answer-field/type': ':answer-field.type/' + kind}


class QuestionMarkerTests(unittest.TestCase):
    def test_separate_control_paragraphs_disappear(self):
        for kind in ('radio', 'checkbox', 'free'):
            for label in ('', 'Written response: ', 'Your response: ', 'Your selections: ',
                          'List all applicable choices: '):
                self.assertEqual(repair_problem('Solve this.\n\n' + label + '{{answer}}',
                                                [field('answer', kind)]), 'Solve this.')

    def test_embedded_unknown_retains_its_coordinate(self):
        before = '$$f(z,y)=⟨{{selection}},\\,y,\\,z⟩$$'
        self.assertEqual(repair_problem(before, [field('selection', 'radio')]),
                         '$$f(z,y)=⟨?,\\,y,\\,z⟩$$')

    def test_mixed_inline_controls_and_tex_remain_exact(self):
        before = 'Use ${{x}}$; {{entry}} {{answer-field:menu}} {{unknown}}.\n\n{{choice}}'
        fields = [field('entry', 'blank'), field('menu', 'select'), field('choice', 'radio')]
        self.assertEqual(repair_problem(before, fields), before.removesuffix('\n\n{{choice}}'))
        self.assertEqual(len(misplaced_markers(before, fields)), 1)

    def test_validation_rejects_regressions_without_mutating_answers(self):
        q = {':question/problem': 'Solve. {{choice}}', ':question/answer-fields': [field('choice', 'radio')]}
        saved = copy.deepcopy(q)
        with self.assertRaisesRegex(ValueError, 'Only blank/select'):
            validate_prompt_markers(q)
        self.assertEqual(q, saved)
        q[':question/problem'] = repair_problem(q[':question/problem'], q[':question/answer-fields'])
        validate_prompt_markers(q)

    def test_repair_is_idempotent_with_multiple_separate_fields(self):
        fields = [field('a', 'free'), field('b', 'radio')]
        once = repair_problem('Task.\n\n{{a}}\n\n{{b}}', fields)
        self.assertEqual(once, 'Task.')
        self.assertEqual(repair_problem(once, fields), once)
