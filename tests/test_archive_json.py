import gzip
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('archive_json',Path(__file__).resolve().parents[1]/'scripts/archive_json.py')
archive=importlib.util.module_from_spec(spec);spec.loader.exec_module(archive)


class ArchiveJsonTests(unittest.TestCase):
    def test_compression_preserves_bytes_and_subsequent_updates_stay_compressed(self):
        with tempfile.TemporaryDirectory()as directory:
            path=Path(directory)/'sources.json';original='["source", "π"]\n'
            path.write_text(original)
            row=archive.compress(path)
            self.assertFalse(path.exists());self.assertTrue(archive.exists(path))
            self.assertEqual(archive.read_text(path),original)
            self.assertEqual(gzip.decompress(Path(row['compressed']).read_bytes()),original.encode())
            archive.write_text(path,'["new version"]\n')
            self.assertFalse(path.exists());self.assertEqual(archive.read_text(path),'["new version"]\n')

    def test_distinct_existing_compressed_data_does_not_replace_original(self):
        with tempfile.TemporaryDirectory()as directory:
            path=Path(directory)/'sources.json';path.write_text('original')
            path.with_name(path.name+'.gz').write_bytes(gzip.compress(b'different'))
            with self.assertRaisesRegex(ValueError,'Distinct'):archive.compress(path)
            self.assertEqual(path.read_text(),'original')
