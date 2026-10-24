"""Frontend module imports must be reachable through the real asset routes."""
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import Mock, patch
from urllib.parse import urljoin, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from serve_graph_explorer import handler


class UIAssets(unittest.TestCase):
    def setUp(self):
        with patch("serve_graph_explorer.InventoryJobs"), patch("serve_graph_explorer.NativeWorker"):
            self.request_class = handler(Path("/unused"), "test", "learner", {
                "LEARNING_REQUEST_DIR": "/tmp/ui-assets-test",
            })

    def get(self, path):
        request = self.request_class.__new__(self.request_class)
        request.path = path
        request.trusted = lambda: True
        request.send_bytes = Mock()
        request.do_GET()
        return request.send_bytes.call_args.args

    def test_graph_lesson_and_forecast_module_dependencies_are_served_as_javascript(self):
        pending = ["/ui/Math-Academy-Graph-Explorer.html", "/ui/learning.js", "/ui/forecast-worker.js", "/ui/study-stats.js"]
        visited = set()
        while pending:
            path = pending.pop()
            if path in visited:
                continue
            visited.add(path)
            with self.subTest(path=path):
                status, body, content_type = self.get(path)
                self.assertEqual(status, 200)
                if path.endswith(".js"):
                    self.assertIn(content_type, {"text/javascript", "application/javascript"})
                source = body.decode()
                imports = re.findall(r'''(?m)^\s*import\s+(?:[^;]*?\sfrom\s+)?['"]([^'"]+)['"]\s*;''', source)
                for specifier in imports:
                    url = urlsplit(urljoin("http://example.test" + path, specifier))
                    if url.netloc == "example.test":
                        pending.append(url.path)
        self.assertIn("/ui/target-scope.js", visited)
        self.assertIn("/ui/target-weeks.js", visited)
        self.assertIn("/ui/requests.js", visited)
        self.assertIn("/ui/forecast-sidebar.js", visited)
        self.assertIn("/ui/math-protection.js", visited)

    def test_non_asset_files_remain_private(self):
        for path in ["/ui/../scripts/serve_graph_explorer.py", "/ui/../course-academy-forecast-prd.md"]:
            with self.subTest(path=path):
                self.assertEqual(self.get(path)[0], 404)

    def test_graph_does_not_depend_on_forecast_modules(self):
        status, body, _ = self.get("/ui/Math-Academy-Graph-Explorer.html")
        self.assertEqual(status, 200)
        self.assertNotIn(b"/ui/forecast.js", body)
        self.assertNotIn(b"/ui/target-scope.js", body)


if __name__ == "__main__":
    unittest.main()
