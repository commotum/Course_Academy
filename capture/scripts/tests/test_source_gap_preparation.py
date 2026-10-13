"""Final omissions bind to the current source gap; supported imports continue."""
from copy import deepcopy
from pathlib import Path
import tempfile
import threading
import unittest

from scripts.config import Config
from scripts.activity.task_payload import task_payload
from scripts.database.evidence import UnsupportedContent, authoritative_question
from scripts.database.pipeline import DatabasePipeline
from scripts.database.prepare import Preparation
from scripts.storage import atomic_json, read_json
from scripts.tests.test_database import FakeClient, question, source_snapshot


def unavailable(task, payload):
    return {'status': 'unavailable', 'reasoning': payload['gap'], 'answers': []}


class SourceGapPreparationTests(unittest.TestCase):
    def test_explicit_partial_fields_are_not_authoritative_even_with_valid_answers(self):
        for flags in ({'answer_fields_complete': False}, {'fields_complete': False},
                      {'answer_fields_complete': True, 'fields_complete': False}):
            with self.subTest(flags=flags), self.assertRaisesRegex(UnsupportedContent, 'explicitly incomplete'):
                authoritative_question({**question(), **flags})

    def test_missing_extractor_placeholder_is_detected_without_guessing_from_tex(self):
        q = question()
        q['answer_fields'][0]['key'] = 'field-0'
        q.update(problem='Enter {{field-0}} and {{field-1}}.', answer_fields_complete=True)
        with self.assertRaisesRegex(UnsupportedContent, 'field-1'):
            authoritative_question(q)
        q['problem'] = r'Compute ${{x}}$ and enter {{field-0}}.'
        self.assertEqual(len(authoritative_question(q)['answer_fields']), 1)

    def test_control_in_an_omitted_authored_body_is_not_a_complete_prompt(self):
        q=question();q['answer_fields'][0]['key']='field-1'
        q.update(problem='Select the correct reasoning below.',problem_field_keys=['field-1'])
        with self.assertRaisesRegex(UnsupportedContent,'Authored problem positions'):
            authoritative_question(q)

    def test_new_gap_and_changed_source_require_new_judgments_but_exact_retries_reuse(self):
        calls = []
        def resolve(task, payload):
            calls.append(deepcopy(payload))
            return unavailable(task, payload)
        preparation = Preparation(source_snapshot(), resolve=resolve)
        q = question()
        content = {'judgments': [{'question_id': 'q-11', 'status': 'confirmed', 'answers': []}]}
        first = preparation.final_judgment(content, q, UnsupportedContent('First gap'))
        self.assertEqual(len(calls), 1)
        saved = {'judgments': [first]}
        self.assertEqual(Preparation(source_snapshot()).final_judgment(saved, q, UnsupportedContent('First gap')), first)
        second = preparation.final_judgment(saved, q, UnsupportedContent('New gap'))
        self.assertNotEqual(first['evidence_hash'], second['evidence_hash'])
        q['worked_solution'] += ' More source explanation.'
        changed = preparation.final_judgment(saved, q, UnsupportedContent('First gap'))
        self.assertNotEqual(first['evidence_hash'], changed['evidence_hash'])
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0]['evidence_contract'], 'judge_question:1')
        self.assertEqual(task_payload('judge_question', calls[0]), calls[0])

    def test_missing_ids_and_record_kinds_have_separate_judgments(self):
        calls = []
        def resolve(task, payload):
            calls.append((payload['capture_key'], payload['record_kind']))
            return unavailable(task, payload)
        prep = Preparation(source_snapshot(), resolve=resolve)
        q = {'problem': 'Same source text', 'source_id': 'unreconciled:first'}
        first = prep.final_judgment({}, q, UnsupportedContent('Missing identity'))
        second = prep.final_judgment({'judgments': [first]}, {**q, 'source_id': 'unreconciled:second'},
                                    UnsupportedContent('Missing identity'))
        example = prep.final_judgment({'judgments': [first]}, q, UnsupportedContent('Missing identity'),
                                     record_kind='canonical_examples')
        self.assertEqual(len(calls), 3)
        self.assertEqual(second['capture_key'], 'unreconciled:second')
        self.assertEqual(example['record_kind'], 'canonical_examples')
        self.assertIsNone(second['question_id'])

    def test_answer_repair_exposing_a_new_gap_gets_its_own_final_finding(self):
        q = question()
        q['answer_fields'][0].pop('evidence')
        q.update(source_file='history.html', difficulty='Unsupported')
        calls = []
        def resolve(task, payload):
            calls.append(payload['gap'])
            if len(calls) == 1:
                return {'status': 'confirmed', 'reasoning': 'Source solution states 2.', 'answers': [
                    {'key': 'x', 'ma_value': '2', 'ma_basis': 'worked_solution', 'ma_evidence': '1+1=2'}]}
            return unavailable(task, payload)
        result = Preparation(source_snapshot(), resolve=resolve).prepare({'questions': [q]})
        self.assertEqual(len(calls), 2)
        self.assertIn('confirmed Math Academy evidence', calls[0])
        self.assertIn('difficulty', calls[1])
        self.assertEqual(result['omissions'][0]['judgment']['gap'], calls[1])
        self.assertEqual(result['omissions'][0]['judgment']['status'], 'unavailable')
        self.assertFalse(result['batches'])

    def test_normal_solver_solution_quote_repairs_answer_without_inventing_source_evidence(self):
        q = question()
        q['answer_fields'][0].pop('evidence')
        q['source_file'] = 'history.html'
        original = deepcopy(q)
        for quote, accepted in (('1+1=2', True), ('The answer is 2.', False)):
            with self.subTest(quote=quote):
                def resolve(task, payload):
                    return {'status': 'confirmed', 'reasoning': 'Read the solution.', 'answers': [
                        {'key': 'x', 'correct_value': '2', 'ma_value': '2', 'ma_basis': 'worked_solution',
                         'ma_evidence': quote}]}
                result = Preparation(source_snapshot(), resolve=resolve).prepare({'questions': [q]})
                self.assertEqual(bool(result['batches']), accepted)
                self.assertEqual(bool(result['omissions']), not accepted)
                if accepted:
                    field = result['content']['questions'][0]['answer_fields'][0]
                    self.assertEqual(field['evidence']['solution_quote'], quote)
                    self.assertEqual(field['evidence']['source_file'], 'history.html')
        self.assertEqual(q, original)

    def test_durable_omission_retry_and_changed_graphic_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = Config(repo_root=root, math_root=root / 'math')
            capture = root / 'capture'
            capture.mkdir()
            graphic = capture / 'original.png'
            graphic.write_bytes(b'original image bytes')
            partial = question('q-12')
            partial.update(answer_fields_complete=False, assets=[{'path': str(graphic)}])
            content = {'questions': [question(), partial], 'judgments': [
                {'question_id': 'q-12', 'status': 'confirmed', 'answers': []}]}
            original = deepcopy(content)
            atomic_json(capture / 'content.json', content)
            atomic_json(capture / 'capture-complete.json', {'complete': True})
            calls = []
            def resolve(task, payload):
                calls.append(payload)
                return unavailable(task, payload)
            client = FakeClient()
            def pipeline():
                return DatabasePipeline(config, threading.Event(), client=client, resolver=resolve)
            first = pipeline().process(capture)
            self.assertEqual(first['status'], 'verified', first)
            self.assertEqual(first['omissions'][0]['id'], 'q-12')
            self.assertEqual(first['omissions'][0]['judgment']['status'], 'unavailable')
            self.assertEqual(pipeline().process(capture)['status'], 'no_changes')
            self.assertEqual(len(calls), 1)
            graphic.write_bytes(b'recovered original image bytes')
            self.assertEqual(pipeline().process(capture)['status'], 'no_changes')
            self.assertEqual(len(calls), 2)
            self.assertEqual(read_json(capture / 'content.json'), original)
            stored = {value for (entity, attr), values in client.facts.items()
                      if attr == 'question/math-academy-id' for value, source in values}
            self.assertIn('q-11', stored)
            self.assertNotIn('q-12', stored)

    def test_unflagged_partial_update_preserves_existing_fields_and_uuid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = Config(repo_root=root, math_root=root / 'math')
            capture = root / 'capture'
            q = question()
            q['answer_fields'].append({**deepcopy(q['answer_fields'][0]), 'key': 'y'})
            atomic_json(capture / 'content.json', {'questions': [q]})
            atomic_json(capture / 'capture-complete.json', {'complete': True})
            client = FakeClient()
            pipeline = DatabasePipeline(config, threading.Event(), client=client)
            self.assertEqual(pipeline.process(capture)['status'], 'verified')
            previous = {key: deepcopy(value) for key, value in client.facts.items()
                        if key[1] in ('question/id', 'question/answer-fields')}
            q['answer_fields'].pop()
            q['problem'] += ' Updated original wording.'
            atomic_json(capture / 'content.json', {'questions': [q]})
            self.assertEqual(pipeline.process(capture)['status'], 'verified')
            self.assertTrue(all(client.facts[key] == value for key, value in previous.items()))


if __name__ == '__main__':
    unittest.main()
