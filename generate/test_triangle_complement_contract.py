import copy
import unittest
from generate.triangle_complement_contract import inspect_record, validate_delivery_batch


def example(a=4, b=8, angle=30, given=3, key=5):
    return {'question': {
        ':question/difficulty': ':question.difficulty/easy',
        ':question/problem': f'The sides $AB={a}$ and $AD={b}$ meet at ${angle}^\\circ$. '
                            f'The area of the quadrilateral $ABCD$ is ${given}$. '
                            'What is the area of $\\triangle BCD$, rounded to the nearest integer?',
        ':question/worked-solution': 'Calculate the outer triangle area and subtract the quadrilateral area.',
        ':question/answer-fields': [{
            ':answer-field/type': ':answer-field.type/blank',
            ':answer-field/choices': [{':answer/id': 'a', ':answer/value': str(key)}],
            ':answer-field/correct': [':answer/id', 'a'],
        }],
    }}


class TriangleComplementContractTests(unittest.TestCase):
    def test_simple_special_angles_and_source_measurements_are_eligible(self):
        for r in (example(), example(5, 6.5, 90, 13, 3), example(24, 18, 115, 130, 66)):
            for band in ('easy', 'moderate', 'hard'):
                r['question'][':question/difficulty'] = ':question.difficulty/' + band
                inspect_record(r)

    def test_source_style_diagram_measurements_and_adjacent_options(self):
        r = example()
        r['question'][':question/problem'] = '![](diagram.png)\n\nThe area of $ABCD$ is $17$. What is the area of $\\triangle BCD$, rounded to the nearest integer?'
        f = r['question'][':question/answer-fields'][0]
        f[':answer-field/type'] = {':db/ident': ':answer-field.type/radio'}
        f[':answer-field/choices'] = [{':answer/id': str(n), ':answer/value': str(n)} for n in (4, 5, 6, 7, 8)]
        f[':answer-field/correct'] = {':answer/id': '6'}
        self.assertIn('diagram', inspect_record(r)['measurements'])

    def test_wrong_textual_key_and_impossible_geometry_still_fail(self):
        for r in (example(key=6), example(given=20), example(angle=180), example(a=0)):
            with self.assertRaises(ValueError):
                inspect_record(r)

    def test_missing_geometry_and_duplicate_options_still_fail(self):
        r = example()
        r['question'][':question/problem'] = 'Find the area rounded to the nearest integer.'
        with self.assertRaises(ValueError):
            inspect_record(r)
        r = example()
        f = r['question'][':question/answer-fields'][0]
        f[':answer-field/type'] = ':answer-field.type/radio'
        f[':answer-field/choices'] *= 5
        with self.assertRaises(ValueError):
            inspect_record(r)

    def test_guided_practice_is_not_accepted_as_independent(self):
        for support in ('Hint: calculate another triangle first.', 'First use the area formula.',
                        'Then subtract the quadrilateral area.', 'The enclosing triangle has area 8.',
                        r'Use $\sin 30^\circ=1/2$.'):
            r = example()
            r['question'][':question/problem'] += support
            with self.assertRaises(ValueError):
                inspect_record(r)

    def test_other_kps_are_unaffected(self):
        validate_delivery_batch([{}], 1)


if __name__ == '__main__':
    unittest.main()
