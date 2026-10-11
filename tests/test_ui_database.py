"""Database image resolution and connection isolation for the local UI."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from serve_graph_explorer import database_environment, image_path


class DatabaseImages(unittest.TestCase):
    def test_relative_and_absolute_images_resolve_to_same_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = root / "images/ab/example.png"
            image.parent.mkdir(parents=True)
            image.write_bytes(b"image")
            self.assertEqual(image_path("images/ab/example.png", root), image)
            self.assertEqual(image_path(str(image), root), image)

    def test_database_files_and_escaping_symlinks_are_not_served(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "images").mkdir()
            private = root / "postgres/private.png"
            private.parent.mkdir()
            private.write_bytes(b"private")
            (root / "images/escape.png").symlink_to(private)
            for path in ("images/../postgres/private.png", "images/escape.png",
                         str(private), "postgres/private.png", "images/missing.png", ""):
                with self.subTest(path=path):
                    self.assertIsNone(image_path(path, root))

    def test_explicit_connection_overrides_and_request_journals(self):
        with patch.dict(os.environ, {
            "EDB_POSTGRES_URL": "custom peer connection",
            "EDB_ENDPOINT": "/tmp/custom-writer.sock",
            "EDB_MATH_ROOT": "/tmp/custom-math",
        }, clear=True):
            math = database_environment("math")
            legacy = database_environment("course-academy-v2")
            self.assertEqual(math["EDB_POSTGRES_URL"], "custom peer connection")
            self.assertEqual(math["EDB_ENDPOINT"], "/tmp/custom-writer.sock")
            self.assertEqual(math["EDB_MATH_ROOT"], "/tmp/custom-math")
            self.assertNotEqual(math["LEARNING_REQUEST_DIR"], legacy["LEARNING_REQUEST_DIR"])


if __name__ == "__main__":
    unittest.main()
