import unittest

from scripts.prepare_topic_difficulty import legacy_base, validate_definition


class DifficultyCaptureEvidenceTests(unittest.TestCase):
    def content(self):
        return {
            'lesson_definition': {'complete': True, 'steps': [
                {'type': 'tutorial', 'content_id': 1},
                {'type': 'example', 'content_id': 2},
                {'type': 'example', 'content_id': 3}]},
            'canonical_examples': [{'math_academy_id': 'e-2'}, {'math_academy_id': 'e-3'}],
            'tutorials': [{'math_academy_id': 1, 'content': 'Full tutorial'}]}

    def test_uses_task_denominator_instead_of_awarded_xp(self):
        self.assertEqual(legacy_base("You've been awarded 15 of the task's 25 XP."), 25)
        self.assertEqual(legacy_base('9 / 7 XP'), 7)

    def test_cannot_use_an_award_without_a_denominator(self):
        with self.assertRaisesRegex(ValueError, 'denominator'):
            legacy_base('You earned 25 XP')

    def test_full_definition_is_accepted(self):
        validate_definition(self.content())

    def test_missing_whole_kp_cannot_pass_as_a_smaller_lesson(self):
        content = self.content()
        content['canonical_examples'].pop()
        with self.assertRaisesRegex(ValueError, 'Canonical examples'):
            validate_definition(content)

    def test_missing_tutorial_cannot_silently_lower_score(self):
        content = self.content()
        content['tutorials'] = []
        with self.assertRaisesRegex(ValueError, 'Tutorials'):
            validate_definition(content)

    def test_empty_tutorial_is_not_complete(self):
        content = self.content()
        content['tutorials'][0]['content'] = ' '
        with self.assertRaisesRegex(ValueError, 'Empty captured tutorial'):
            validate_definition(content)


if __name__ == '__main__':
    unittest.main()
