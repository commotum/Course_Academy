import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tests'))
from test_generator_publish import FakeClient, KP, KP_UUID, PACKAGE, SCRIPT, record
from scripts.generator_publish import Publisher, content_fingerprint, stable_identities

spec = importlib.util.spec_from_file_location('check_delivery', ROOT / 'generate/pipeline/check_delivery.py')
delivery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(delivery)


class DeliveryTests(unittest.TestCase):
    def test_legacy_raw_equation_rows_are_normalized_before_delivery_identity(self):
        original = record(3)
        original['question'][':question/worked-solution'] = '\\begin{align*}x&=3+1\\\\[5pt]\n\n&=4\\end{align*}'
        saved = copy.deepcopy(original)
        report = self.run_audit([original])
        self.assertEqual(report['accepted_count'], 1)
        accepted = json.loads((self.root / 'evidence/accepted.json').read_text())[0]['question']
        self.assertIn('$$\n\\begin{aligned}', accepted[':question/worked-solution'])
        self.assertIn('\\\\[5pt]', accepted[':question/worked-solution'])
        self.assertEqual(original, saved)
        self.assertEqual(accepted[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'],
                         original['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.math = self.root / 'math'
        self.source = {'database': 'math', 'lineage': 'fixture', 'kp_id': KP,
                       'material': {'kp': {':knowledge-point/id': str(KP_UUID)},
                                    'source_eligibility': {'policy_version':1,'excluded_questions':[]}}}
        self.inventory = {'database': 'math', 'lineage': 'fixture', 'kp_id': KP,
                          'basis': 12, 'fingerprints': [content_fingerprint(record(2)['question'])]}

    def run_audit(self, records):
        return delivery.audit(records, self.inventory, self.source, 'easy',
                              self.root / 'evidence', self.root, self.math)

    def test_shared_filter_matches_publication_and_leaves_inputs_unchanged(self):
        records = [record(2), record(3), record(3), record(4)]
        original = copy.deepcopy(records)
        with patch('scripts.generator_publish.EDBClient', side_effect=AssertionError('No database connection')):
            report = self.run_audit(records)
        accepted = json.loads((self.root / 'evidence/accepted.json').read_text())
        self.assertEqual(records, original)
        self.assertEqual((report['accepted_count'], report['duplicate_count']), (2, 2))
        self.assertEqual(accepted[0]['question'], stable_identities(records[1]['question'], KP_UUID))
        self.assertFalse(self.math.exists())
        client = FakeClient()
        client.kp[':knowledge-point/questions'] = [records[0]['question']]
        client.initial_kp = copy.deepcopy(client.kp)
        from types import SimpleNamespace
        publisher = Publisher(SimpleNamespace(math_root=self.math, source=':application/ca-engine'), client=client)
        preparation = publisher.prepare(KP, records, SCRIPT, PACKAGE, self.root / 'publication')
        self.assertEqual(preparation['records'], accepted)

    def test_canonical_and_generated_image_bytes_are_staged_only_under_evidence(self):
        image = b'<svg xmlns="http://www.w3.org/2000/svg" width="2" height="2"><rect width="2" height="2"/></svg>'
        canonical = self.math / 'images/old.svg'
        canonical.parent.mkdir(parents=True)
        canonical.write_bytes(image)
        (self.root / 'generated.svg').write_bytes(image)
        a, b = record(3), record(3)
        a['question'][':question/problem'] += ' ![](images/old.svg)'
        b['question'][':question/problem'] += ' ![](generated.svg)'
        before = {str(p): p.read_bytes() for p in self.math.rglob('*') if p.is_file()}
        report = self.run_audit([a, b])
        self.assertEqual((report['accepted_count'], report['duplicate_count']), (1, 1))
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.math.rglob('*') if p.is_file()})
        staged = list((self.root / 'evidence/assets/images').rglob('*.svg'))
        self.assertEqual([p.read_bytes() for p in staged], [image])

    def test_invalid_records_and_wrong_difficulty_fail_instead_of_disappearing(self):
        invalid = record(3)
        invalid['question'][':question/answer-fields'][0][':answer-field/correct'] = [':answer/id', 'missing']
        with self.assertRaisesRegex(ValueError, 'Canonical answer'):
            self.run_audit([invalid])
        wrong_band = record(3)
        wrong_band['question'][':question/difficulty'] = ':question.difficulty/hard'
        with self.assertRaisesRegex(ValueError, 'outside the requested difficulty'):
            self.run_audit([wrong_band])
        wrong_kp = record(3)
        wrong_kp['knowledge_point'] = KP + 1
        with self.assertRaisesRegex(ValueError, 'another knowledge point'):
            self.run_audit([wrong_kp])

    def test_canonical_image_manifest_integrity_is_preserved(self):
        canonical = self.math / 'images/source.svg'
        canonical.parent.mkdir(parents=True)
        canonical.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"/>')
        (self.root / 'asset-map.json').write_text(json.dumps(
            {'path': 'images/source.svg', 'sha256': '0' * 64}))
        r = record(3)
        r['question'][':question/problem'] += ' ![](images/source.svg)'
        with self.assertRaisesRegex(ValueError, 'differs from its source manifest'):
            self.run_audit([r])

    def test_mismatched_snapshot_and_published_output_are_rejected(self):
        self.inventory['lineage'] = 'other'
        with self.assertRaisesRegex(ValueError, 'Inventory/source mismatch'):
            self.run_audit([record(3)])
        with self.assertRaisesRegex(ValueError, 'outside the published math root'):
            delivery.audit([], self.inventory, self.source, 'easy', self.math / 'audit', self.root, self.math)


if __name__ == '__main__':
    unittest.main()
