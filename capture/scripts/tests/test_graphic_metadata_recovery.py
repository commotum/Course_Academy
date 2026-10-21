"""Original diagram aliases require exact owned-question source provenance."""
from copy import deepcopy
import hashlib
from pathlib import Path
import tempfile
import unittest

from PIL import Image
from scripts.recovery import recover_source_graphics
from scripts.storage import atomic_json


class GraphicMetadataRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root/'answers.json'
        self.payload = {'task': {'id': 77, 'answers': [{'question': {'id': 11,
            'explanation': '<img src="/graphics/q-11-e-2">',
            'graphics': [{'id': 1, 'fileId': 'q-11-e-2', 'tex': 'original TeX'},
                         {'id': 2, 'fileId': 'hash', 'tex': 'original TeX'}]}}]}}
        atomic_json(self.source, self.payload)
        self.source_response = {'status': 200, 'url': 'https://mathacademy.com/api/tasks/77/answers'}
        atomic_json(self.source.with_suffix('.response.json'), self.source_response)
        self.path = self.root/'original.png'
        Image.new('RGB', (3, 4), 'white').save(self.path)
        self.receipt = self.root/'image-response.json'
        self.receipt_data = {'url': 'https://mathacademy.com/graphics/hash', 'status': 200,
            'bytes': self.path.stat().st_size, 'sha256': hashlib.sha256(self.path.read_bytes()).hexdigest(),
            'content_type': 'image/png'}
        atomic_json(self.receipt, self.receipt_data)
        self.solution = self.root/'solution.html'
        self.solution.write_text('<div id="questionExplanation-11"><img src="/graphics/q-11-e-2"></div>')
        self.history = {'questions': [{'math_academy_id': 'q-11', 'solution_evidence': str(self.solution),
            'errors': ['Image unavailable: https://mathacademy.com/graphics/q-11-e-2'],
            'assets': [{'tag': 'img', 'source_url': 'https://mathacademy.com/graphics/q-11-e-2',
                'extraction_part': 'solution', 'unavailable': 'empty response', 'render_unavailable': 'broken'}]}]}
        self.recovery = {'question_id': 'q-11', 'task_answers_source': str(self.source),
            'alias': 'q-11-e-2', 'file_id': 'hash', 'path': str(self.path), 'response_file': str(self.receipt)}

    def recover(self):
        return recover_source_graphics(self.history, '77', self.recovery)

    def test_exact_tex_recovers_original_bytes_and_preserves_failed_source_and_errors(self):
        original = deepcopy(self.history)
        result = self.recover()
        self.assertEqual(self.history, original)
        question = result['questions'][0]
        asset = question['assets'][0]
        self.assertEqual(asset['source_url'], self.history['questions'][0]['assets'][0]['source_url'])
        self.assertEqual(asset['original_image_validation']['dimensions'], [3, 4])
        self.assertEqual(asset['recovered_from']['source_url'], 'https://mathacademy.com/graphics/hash')
        self.assertEqual(asset['recovered_from']['previous_asset']['unavailable'], 'empty response')
        self.assertNotIn('unavailable', asset)
        # Re-extraction retires source errors only after the complete solution checks pass.
        self.assertEqual(question['errors'], original['questions'][0]['errors'])

    def test_changed_or_ambiguous_tex_is_rejected(self):
        graphics = self.payload['task']['answers'][0]['question']['graphics']
        for altered in ([{**graphics[0], 'tex': ''}, graphics[1]],
                        [graphics[0], {**graphics[1], 'tex': 'different'}],
                        graphics + [deepcopy(graphics[1])]):
            with self.subTest(graphics=altered):
                payload = deepcopy(self.payload)
                payload['task']['answers'][0]['question']['graphics'] = altered
                atomic_json(self.source, payload)
                with self.assertRaises(ValueError):
                    self.recover()

    def test_other_question_task_or_source_occurrence_is_rejected(self):
        for kind in ('task', 'question', 'source_alias', 'saved_alias', 'saved_question'):
            with self.subTest(kind=kind):
                payload = deepcopy(self.payload)
                self.solution.write_text('<div id="questionExplanation-11"><img src="/graphics/q-11-e-2"></div>')
                if kind == 'task': payload['task']['id'] = 99
                elif kind == 'question': payload['task']['answers'][0]['question']['id'] = 12
                elif kind == 'source_alias': payload['task']['answers'][0]['question']['explanation'] = '<img src="/graphics/other">'
                elif kind == 'saved_alias': self.solution.write_text('<div id="questionExplanation-11"><img src="/graphics/other"></div>')
                else: self.solution.write_text('<div id="questionExplanation-12"><img src="/graphics/q-11-e-2"></div>')
                atomic_json(self.source, payload)
                with self.assertRaises(ValueError): self.recover()

    def test_tampered_bytes_or_wrong_response_origin_is_rejected(self):
        for key, value in [('sha256', 'wrong'), ('status', 404), ('url', 'https://other.invalid/hash')]:
            with self.subTest(key=key):
                atomic_json(self.receipt, {**self.receipt_data, key: value})
                with self.assertRaises(ValueError): self.recover()

    def test_unrelated_task_endpoint_and_invalid_raster_are_rejected(self):
        atomic_json(self.source.with_suffix('.response.json'), {**self.source_response, 'url': 'https://mathacademy.com/api/tasks/88/answers'})
        with self.assertRaises(ValueError): self.recover()
        atomic_json(self.source.with_suffix('.response.json'), self.source_response)
        self.path.write_bytes(b'not a raster')
        atomic_json(self.receipt, {**self.receipt_data, 'bytes': self.path.stat().st_size,
            'sha256': hashlib.sha256(self.path.read_bytes()).hexdigest()})
        with self.assertRaises(OSError): self.recover()


if __name__ == '__main__':
    unittest.main()
