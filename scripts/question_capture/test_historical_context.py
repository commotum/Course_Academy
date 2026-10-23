import json
import tempfile
import unittest
from pathlib import Path

from core import build_transaction
from historical_context import historical_task_type, require_activity_context
from math_content import build_math_content


class HistoricalContextTests(unittest.TestCase):
    def test_old_export_recovers_multistep_type_from_saved_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'history.json').write_text(json.dumps({'task_text': ' Multistep\n13/10 XP\nMotion'}))
            question = {'provenance': {'source_file': 'history.json',
                                      'source_kind': 'completed historical activity'}}
            self.assertEqual(historical_task_type(question, root), 'multistep')
            (root / 'history.json').write_text(json.dumps({'task_text': 'Lesson\nMotion'}))
            self.assertEqual(historical_task_type(question, root), 'lesson')

    def test_both_transaction_builders_reject_flattened_multistep_parts(self):
        content = {'topic_id': 285, 'questions': [{'math_academy_id': 'q-143522',
                    'provenance': {'task_type': 'multistep'}}]}
        for builder, args in [(build_transaction, ({}, {})), (build_math_content, ({}, {}))]:
            with self.assertRaisesRegex(ValueError, 'complete activity: q-143522'):
                builder(content, *args)

    def test_legacy_payload_without_type_also_cannot_bypass_guard(self):
        question = {'math_academy_id': 'q-143522', 'provenance': {
            'source_file': 'reference/mathacademy/progress-history-2026-10-04/13408988.json',
            'source_kind': 'completed historical activity'}}
        with self.assertRaisesRegex(ValueError, 'complete activity'):
            require_activity_context({'questions': [question]})

    def test_complete_multistep_keeps_parts_for_structural_import(self):
        require_activity_context({'task_type': 'multistep', 'questions': [
            {'math_academy_id': 'q-143522', 'provenance': {'task_type': 'multistep'}}]})
        require_activity_context({'task_type': 'lesson', 'questions': [
            {'math_academy_id': 'q-1', 'provenance': {'task_type': 'lesson'}}]})

    def test_unavailable_historical_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'cannot be verified'):
                historical_task_type({'provenance': {'source_file': 'missing.json',
                    'source_kind': 'completed historical activity'}}, Path(directory))


if __name__ == '__main__':
    unittest.main()
