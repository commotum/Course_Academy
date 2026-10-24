import copy
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_investigation import (BANDS, COVERAGE, COUNTS_QUERY, completeness,
    COVERAGE_INPUTS, coverage_inputs_unchanged, coverage_plan, migrate_coverage,
    observed_coverage, prepare_investigation, _transact)
from capture.scripts.database.client import StaleBasis
from capture.scripts.database.edn import dumps, loads


def question(eid=1, band='easy', imported=True):
    answer = {':db/id': eid + 1000, ':answer/id': f'answer-{eid}',
              ':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '2'}
    result = {':db/id': eid, ':question/id': f'question-{eid}', ':question/problem': 'Compute $1+1$.',
              ':question/worked-solution': 'Adding gives $2$.',
              ':question/difficulty': {':db/ident': ':question.difficulty/' + band},
              ':question/answer-fields': [{':answer-field/key': 'answer',
                ':answer-field/type': {':db/ident': ':answer-field.type/blank'},
                ':answer-field/choices': [answer], ':answer-field/correct': answer}]}
    if imported:
        result[':question/math-academy-id'] = f'q-{eid}'
    return result


class References:
    def __init__(self):
        self.calls = []
        self.points = [{':db/id': 20, ':knowledge-point/title': 'Adding One',
                        COVERAGE: [{':db/ident': ':question.difficulty/' + b} for b in BANDS]},
                       {':db/id': 30, ':knowledge-point/title': 'Other Complete Skill',
                        COVERAGE: [{':db/ident': ':question.difficulty/' + b} for b in BANDS]}]
        self.questions = {point[':db/id']: [question(point[':db/id'] * 100 + i, band)
                          for i, band in enumerate(('easy', 'easy', 'moderate', 'moderate', 'hard', 'hard'))]
                          for point in self.points}
        self.excluded = set()
        self.client = self

    def source_exclusions(self, directory, basis, ids):
        return [{':db/id': eid} for eid in ids if eid in self.excluded]

    def query(self, source, inputs, directory, name, basis=None):
        self.calls.append((source, inputs, name, basis))
        if name == 'reference-kp-metadata':
            return [[copy.deepcopy(point)] for point in self.points]
        if name.startswith('candidate-counts-'):
            return [[kp, ':question.difficulty/' + band, 2] for kp in inputs[0] for band in BANDS]
        if name.startswith('reference-question-ids-'):
            return [[q[':db/id']] for q in self.questions[inputs[0]]]
        if name.startswith('reference-questions-'):
            return [[copy.deepcopy(q)] for group in self.questions.values() for q in group if q[':db/id'] in inputs[0]]
        raise AssertionError(name)


def source(questions=None):
    return {'database': 'math', 'lineage': 'one', 'basis': 42, 'kp_id': 10,
            'material': {'kp': {':db/id': 10, ':knowledge-point/title': 'Adding One',
                               ':knowledge-point/questions': questions or []}}}


class InvestigationTests(unittest.TestCase):
    def test_observation_is_independent_of_completeness_and_authorship(self):
        imported = question(band='moderate')
        imported.pop(':question/worked-solution')
        self.assertEqual(observed_coverage([imported, question(band='hard', imported=False)]), ['moderate'])
        self.assertEqual(observed_coverage([question(imported=False)]), ['unobserved'])

    def test_every_field_must_have_valid_key_and_answer_membership(self):
        q = question()
        self.assertEqual(completeness(q), [])
        other = copy.deepcopy(q[':question/answer-fields'][0])
        other[':answer-field/key'] = 'second'
        other[':answer-field/correct'] = {':answer/id': 'not-in-bank'}
        q[':question/answer-fields'].append(other)
        self.assertIn('answer-fields[1].correct', completeness(q))

    def test_reference_selection_rejects_partial_donor_and_preserves_same_basis(self):
        publisher = References()
        publisher.questions[20][-1][':question/answer-fields'][0].pop(':answer-field/correct')
        with tempfile.TemporaryDirectory() as td:
            result = prepare_investigation(publisher, source(), td)
            self.assertEqual(result['reference_kp_id'], 30)
            self.assertTrue(result['needs_exemplars'])
            saved = json.loads(Path(result['reference_file']).read_text())
            self.assertTrue(all(len(saved['questions'][b]) == 2 for b in BANDS))
            self.assertTrue(all(row[3] == 42 for row in publisher.calls))
            count_queries = [row for row in publisher.calls if row[2].startswith('candidate-counts')]
            self.assertTrue(all(len(row[1]) == 1 for row in count_queries))
            calls = len(publisher.calls)
            self.assertEqual(prepare_investigation(publisher, source(), td), result)
            self.assertEqual(len(publisher.calls), calls)

    def test_stored_coverage_and_partial_import_require_construction(self):
        questions = [question(i + 1, b) for i, b in enumerate(BANDS)]
        partial = question(8, 'moderate')
        partial.pop(':question/worked-solution')
        saved = source(questions + [partial])
        saved['material']['kp'][COVERAGE] = [{':db/ident': ':question.difficulty/hard'}]
        with tempfile.TemporaryDirectory() as td:
            result = prepare_investigation(References(), saved, td)
            self.assertEqual(result['observed_coverage'], ['hard'])
            self.assertTrue(result['needs_exemplars'])
            self.assertEqual(result['complete_examples'], dict.fromkeys(BANDS, 1))
            self.assertEqual(len(result['incomplete_imports']), 1)

    def test_complete_three_band_source_does_not_require_new_examples(self):
        with tempfile.TemporaryDirectory() as td:
            result = prepare_investigation(References(), source([question(i + 1, b) for i, b in enumerate(BANDS)]), td)
            self.assertFalse(result['needs_exemplars'])

    def test_retired_and_contained_questions_do_not_qualify_reference(self):
        p = References()
        p.excluded.add(p.questions[20][0][':db/id'])
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(prepare_investigation(p, source(), td)['reference_kp_id'], 30)

    def test_coverage_plan_replaces_sentinel_and_preserves_other_observed_levels(self):
        class Client:
            def status(self): return {'database': 'math', 'lineage': 'test', 'basis': 42}
            def query(self, query, inputs, directory, name, basis):
                if name == 'coverage-kps': return [[1], [2], [3]]
                if name == 'coverage-before': return [[1, ':question.difficulty/unobserved'], [2, ':question.difficulty/easy']]
                if name.startswith('coverage-observed-'):
                    return [[1, ':question.difficulty/moderate'], [2, ':question.difficulty/easy'], [2, ':question.difficulty/hard']]
                raise AssertionError(name)
        with tempfile.TemporaryDirectory() as td:
            forms, expected = coverage_plan(Client(), td, 42)
        self.assertEqual(expected, {'1': [':question.difficulty/moderate'], '2': [':question.difficulty/easy', ':question.difficulty/hard'], '3': [':question.difficulty/unobserved']})
        self.assertEqual(len(forms), 4)
        self.assertIn([':db/retract', 1, COVERAGE, ':question.difficulty/unobserved'], forms)
        self.assertTrue(all(form[2] == COVERAGE for form in forms))

    def test_unknown_outcome_reuses_exact_saved_request_without_new_preview(self):
        class Client:
            def status(self): return {'database': 'math', 'lineage': 'one', 'basis': 42}
            def query(self, query, inputs, *args):
                assert inputs == [':agent/codex']
                return [[8]]
            def command(self, command, *args):
                self.preview_count += 1
                return '{:edb/db-before-t 42}'
            preview_count = 0
        client = Client()
        publisher = SimpleNamespace(client=client, config=SimpleNamespace(database='math', endpoint='/writer', math_root='/math', postgres_url=''))
        requests = []
        def submit(committer, request):
            requests.append(copy.deepcopy(request))
            if len(requests) == 1:
                raise ConnectionError('reply lost')
            return {':edb/committed': True, ':edb/db-before-t': 42, ':edb/db-after-t': 43, ':edb/tx-data': []}
        with tempfile.TemporaryDirectory() as td, patch('generator_investigation.Committer.submit', submit):
            with self.assertRaises(ConnectionError):
                _transact(publisher, td, [[':original', 1]], 42, ':agent/codex', True)
            result = _transact(publisher, td, [[':different', 2]], 999, ':different/source', True)
            self.assertEqual(result['basis'], 43)
            self.assertEqual(requests[0], requests[1])
            self.assertEqual(client.preview_count, 1)

    def test_log_proof_allows_learner_writes_but_rejects_source_retractions(self):
        class Client:
            config = SimpleNamespace(database='math')
            changed_attribute = 999
            def query(self, *args): return [[i + 1, ':' + name] for i, name in enumerate(COVERAGE_INPUTS)]
            def command(self, command, *args):
                flags = dict(zip(args[::2], args[1::2]))
                self.asserted_inputs = loads(Path(flags['--inputs']).read_text())
                return dumps([[200, self.changed_attribute, 100000, False]])
        client = Client()
        with tempfile.TemporaryDirectory() as td:
            self.assertTrue(coverage_inputs_unchanged(client, td, 42, 45))
            self.assertEqual(client.asserted_inputs, [43, 46])
            client.changed_attribute = COVERAGE_INPUTS.index('question/difficulty') + 1
            self.assertFalse(coverage_inputs_unchanged(client, td, 42, 45))

    def test_rebase_keeps_guard_and_rechecks_after_confirmed_stale_rejection(self):
        class Client:
            basis = 43
            config = SimpleNamespace(database='math')
            def status(self): return {'database': 'math', 'lineage': 'one', 'basis': self.basis}
            def query(self, *args): return [[8]]
            def command(self, command, *args): return dumps({':edb/db-before-t': self.basis})
        client = Client()
        publisher = SimpleNamespace(client=client, config=SimpleNamespace(database='math', endpoint='/writer', math_root='/math', postgres_url=''))
        requests = []
        def submit(committer, request):
            requests.append(copy.deepcopy(request))
            if len(requests) == 1:
                client.basis = 44
                raise StaleBasis('learner committed')
            return {':edb/committed': True, ':edb/db-before-t': 44, ':edb/db-after-t': 45, ':edb/tx-data': []}
        with tempfile.TemporaryDirectory() as td, patch('generator_investigation.Committer.submit', submit), \
                patch('generator_investigation.coverage_inputs_unchanged', return_value=True) as proof:
            result = _transact(publisher, td, [[':original', 1]], 42, ':agent/codex', True, coverage_rebase=True)
            self.assertEqual(result['basis'], 45)
            self.assertEqual([r['basis'] for r in requests], [43, 44])
            self.assertNotEqual(requests[0]['request_key'], requests[1]['request_key'])
            self.assertEqual(requests[0]['transaction'], requests[1]['transaction'])
            self.assertEqual([(c.args[-2], c.args[-1]) for c in proof.call_args_list], [(42, 43), (42, 44)])

    def test_changed_coverage_dependency_prevents_submission(self):
        client = SimpleNamespace(status=lambda: {'database': 'math', 'lineage': 'one', 'basis': 43},
                                 command=lambda *args: '{:edb/db-before-t 43}')
        publisher = SimpleNamespace(client=client, config=SimpleNamespace(database='math', endpoint='/writer', math_root='/math', postgres_url=''))
        with tempfile.TemporaryDirectory() as td, patch('generator_investigation.coverage_inputs_unchanged', return_value=False), \
                patch('generator_investigation.Committer.submit') as submit:
            with self.assertRaises(StaleBasis):
                _transact(publisher, td, [[':original', 1]], 42, ':agent/codex', True, coverage_rebase=True)
            submit.assert_not_called()


if __name__ == '__main__':
    unittest.main()
