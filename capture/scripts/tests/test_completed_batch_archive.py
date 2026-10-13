import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.database.archive import compact_completed_batch, content_digest, read_manifest
from scripts.database.batch import ActivityBatch
from scripts.storage import atomic_json


class CompletedBatchArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.directory = self.root / 'batch'
        self.directory.mkdir()
        receipt = {'status': 'verified', 'request_key': 'one-request', 'reimport_is_noop': True}
        members, outcomes = [], {}
        for number in range(4):
            directory = self.root / 'captures' / str(number)
            content = {'task_id': number, 'questions': [{'problem': 'kept source'}], 'attempts': ['large duplicate']}
            atomic_json(directory / 'content.json', content)
            members.append({'directory': str(directory), 'content': content})
            outcomes[str(directory)] = {'status': 'verified', 'basis': 42, 'receipts': [receipt],
                                        'omissions': [{'reason': 'retain me'}] if number == 1 else [],
                                        'calibration': None, 'batch_directory': str(self.directory),
                                        'batch_activities': 4, 'content_sha256': content_digest(content)}
        self.manifest = {'members': members, 'boundary': 'question_minimum', 'questions': 201,
                         'status': 'verified', 'source_repairs': {m['directory']: [] for m in members},
                         'result': {'status': 'verified', 'activities': outcomes,
                                    'batch_directory': str(self.directory), 'questions': 201,
                                    'boundary': 'question_minimum'}}
        previous = {k: copy.deepcopy(v) for k, v in self.manifest.items() if k != 'result'}
        previous['status'] = 'pending'
        atomic_json(self.directory / 'manifest.json', previous)
        atomic_json(self.directory / 'manifest.json', self.manifest)
        atomic_json(self.directory / 'verification.json', receipt)

    def test_two_halves_preserve_results_remove_duplicates_and_remain_readable(self):
        originals = {m['directory']: (Path(m['directory']) / 'content.json').read_bytes()
                     for m in self.manifest['members']}
        summary = compact_completed_batch(self.directory)
        raw = json.loads((self.directory / 'manifest.json').read_text())
        self.assertEqual([p['members'] for p in raw['parts']], [2, 2])
        self.assertEqual(len(raw['receipts']), 1)
        self.assertNotIn('members', raw)
        self.assertFalse((self.directory / 'manifest.json.previous').exists())
        restored = read_manifest(self.directory / 'manifest.json')
        self.assertEqual(restored['result'], self.manifest['result'])
        self.assertEqual(restored['source_repairs'], self.manifest['source_repairs'])
        for member in restored['members']:
            self.assertNotIn('content', member)
            self.assertEqual((self.directory / member['content_ref']).read_bytes(), originals[member['directory']])
        self.assertEqual(summary['members'], 4)
        # Existing callers get the exact completed outcome without invoking preparation.
        batch = ActivityBatch.__new__(ActivityBatch)
        batch.manifest_path = self.directory / 'manifest.json'
        self.assertEqual(batch.process([]), self.manifest['result'])

    def test_changed_source_is_not_discarded(self):
        member = self.manifest['members'][0]
        atomic_json(Path(member['directory']) / 'content.json', {'different': True})
        before = (self.directory / 'manifest.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'differs'):
            compact_completed_batch(self.directory)
        self.assertEqual((self.directory / 'manifest.json').read_bytes(), before)
        self.assertTrue((self.directory / 'manifest.json.previous').exists())

    def test_pending_request_or_active_batch_cannot_be_compacted(self):
        atomic_json(self.directory / 'request.json', {'intent': 'still pending'})
        with self.assertRaisesRegex(ValueError, 'pending exact request'):
            compact_completed_batch(self.directory)
        (self.directory / 'request.json').unlink()
        atomic_json(self.root / 'active.json', {'directory': str(self.directory)})
        with self.assertRaisesRegex(ValueError, 'still active'):
            compact_completed_batch(self.directory)

    def test_distinct_previous_data_is_retained(self):
        path = self.directory / 'manifest.json.previous'
        previous = json.loads(path.read_text())
        previous['members'][0]['content']['attempts'] = ['unique prior evidence']
        path.write_text(json.dumps(previous))
        with self.assertRaisesRegex(ValueError, 'distinct capture data'):
            compact_completed_batch(self.directory)
        self.assertTrue(path.exists())
        self.assertFalse((self.directory / 'manifest.part-1.json').exists())

    def test_pending_manifest_reader_is_unchanged_and_compaction_refuses(self):
        self.manifest['status'] = 'pending'
        (self.directory / 'manifest.json').write_text(json.dumps(self.manifest))
        self.assertEqual(read_manifest(self.directory / 'manifest.json'), self.manifest)
        with self.assertRaisesRegex(ValueError, 'Only completed'):
            compact_completed_batch(self.directory)

    def test_corrupt_or_missing_part_cannot_be_treated_as_completed(self):
        compact_completed_batch(self.directory)
        part = self.directory / 'manifest.part-2.json'
        before = part.read_bytes()
        part.write_bytes(before + b' ')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            read_manifest(self.directory / 'manifest.json')
        part.unlink()
        with self.assertRaises(FileNotFoundError):
            read_manifest(self.directory / 'manifest.json')

    def test_compaction_is_idempotent(self):
        compact_completed_batch(self.directory)
        before = {p.name: p.read_bytes() for p in self.directory.iterdir() if p.is_file()}
        self.assertTrue(compact_completed_batch(self.directory)['already_compact'])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.directory.iterdir() if p.is_file()})

    def test_nonempty_source_repairs_are_preserved(self):
        member = self.manifest['members'][0]
        self.manifest['source_repairs'][member['directory']] = [{'repair': 'unique evidence'}]
        (self.directory / 'manifest.json').write_text(json.dumps(self.manifest))
        (self.directory / 'manifest.json.previous').unlink()
        compact_completed_batch(self.directory)
        self.assertEqual(read_manifest(self.directory / 'manifest.json')['source_repairs'], self.manifest['source_repairs'])


if __name__ == '__main__':
    unittest.main()
