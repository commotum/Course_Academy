"""Checks for the explicit-field vault format and additive assignment imports."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from f26_assignment_content import Builder
from import_school_assignments import Import


class CanonicalFields(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.vault = Path(self.directory.name)
        self.path = self.vault / 'assignment.md'
        self.path.write_text('')
        self.builder = Builder(self.vault)

    def convert(self, fields, content='Answer: {{value}}.', **attrs):
        return self.builder.question('source', 'problem-1/question',
            dict(id='q-1', content=content, fields=fields, **attrs), self.path)

    def test_mixed_radio_blank_preserves_keys_and_option_feedback(self):
        qid, audit = self.convert([
            {'key': 'value', 'type': 'blank', 'correct': {'type': 'math', 'value': '0'}},
            {'key': 'decision', 'type': 'radio', 'correct': 'a', 'choices': [
                {'id': 'a', 'type': 'text', 'value': 'Yes', 'feedback': 'Reason.'},
                {'id': 'b', 'type': 'text', 'value': 'No'}]}], feedback='Explanation.')
        self.builder.validate()
        rows = {r[':db/id']: r for r in self.builder.entities}
        question = rows[qid]
        self.assertEqual(question[':question/problem'], 'Answer: {{value}}.')
        self.assertEqual(question[':question/worked-solution'], 'Explanation.')
        self.assertEqual({rows[f][':answer-field/key'] for f in question[':question/answer-fields']}, {'value', 'decision'})
        correct = audit['fields'][1]['correct_answer_id']
        self.assertEqual(rows[correct][':answer/feedback'], 'Reason.')

    def test_free_reference_remains_written_response(self):
        qid, audit = self.convert([
            {'key': 'value', 'type': 'blank', 'correct': {'type': 'math', 'value': '0'}},
            {'key': 'proof', 'type': 'free', 'correct': {'type': 'text', 'value': 'A proof.'}}],
            content='Answer: {{value}}. Explain: {{proof}}.')
        self.builder.validate()
        question = next(r for r in self.builder.entities if r[':db/id'] == qid)
        self.assertEqual(len(question[':question/answer-fields']), 1)
        self.assertIn('A proof.', question[':question/worked-solution'])
        self.assertIn('[proof: written response]', question[':question/problem'])
        self.assertEqual(audit['fields'][1]['field_id'], None)
        self.assertEqual(len(self.builder.audit['grading_limitations']), 1)

    def test_selection_rejects_key_outside_its_choices(self):
        with self.assertRaisesRegex(ValueError, 'outside choices'):
            self.convert([{'key': 'value', 'type': 'radio', 'correct': 'c', 'choices': [
                {'id': 'a', 'type': 'text', 'value': 'Yes'}, {'id': 'b', 'type': 'text', 'value': 'No'}]}])

    def test_existing_assignments_and_targets_are_preserved(self):
        snapshot = {'entities': {'1': {'learner/id': 'learner', 'learner/assignments': [7], 'learner/targets': [8]}}}
        model = Import(self.vault, {})
        forms = model.transaction(snapshot, 'learner', [])
        self.assertEqual(forms, [])
        self.assertEqual(snapshot['entities']['1']['learner/assignments'], [7])
        self.assertEqual(snapshot['entities']['1']['learner/targets'], [8])


if __name__ == '__main__':
    unittest.main()
