"""Renderer runtime selection must work in the service's minimal PATH."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'generate/pipeline'))
from render_preview import resolve_node


class RendererRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.playwright = self.root / 'runtime/node_modules/playwright'
        self.playwright.mkdir(parents=True)
        self.home = patch('render_preview.Path.home', return_value=self.root / 'home')
        self.home.start()

    def tearDown(self):
        self.home.stop()
        self.temp.cleanup()

    def node(self, path, version):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'#!/bin/sh\nprintf "{version}\\n"\n')
        path.chmod(0o755)
        return path

    def test_bundled_runtime_avoids_old_system_node(self):
        bundled = self.node(self.root / 'runtime/bin/node', 'v22.19.0')
        self.node(self.root / 'system/node', 'v18.19.1')
        self.assertEqual(resolve_node(self.playwright, environment={'PATH': str(self.root / 'system')}), str(bundled))

    def test_current_path_node_is_a_valid_fallback(self):
        node = self.node(self.root / 'system/node', 'v20.19.0')
        self.assertEqual(resolve_node(self.playwright, environment={'PATH': str(node.parent)}), str(node))

    def test_explicit_override_is_checked_and_honored(self):
        self.node(self.root / 'runtime/bin/node', 'v22.19.0')
        chosen = self.node(self.root / 'chosen/node', 'v24.1.0')
        self.assertEqual(resolve_node(self.playwright, environment={'COURSE_ACADEMY_NODE_EXECUTABLE': str(chosen)}), str(chosen))
        old = self.node(self.root / 'old/node', 'v18.19.1')
        with self.assertRaisesRegex(RuntimeError, 'Node >=20'):
            resolve_node(self.playwright, node=str(old), environment={})

    def test_missing_or_old_runtime_fails_before_browser_work(self):
        self.node(self.root / 'system/node', 'v18.19.1')
        with self.assertRaisesRegex(RuntimeError, 'v18.19.1'):
            resolve_node(self.playwright, environment={'PATH': str(self.root / 'system')})
