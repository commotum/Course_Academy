import json
from pathlib import Path
import tempfile
import unittest

from engine.fire.graph_snapshots import parse_saved_graph


class GraphSnapshotTests(unittest.TestCase):
    def parse(self, color, *, root_id="graph", topics=("42",)):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "graph.html"
            nodes = "".join(f'<g class="node"><title>{topic}</title><ellipse fill="{color}" stroke-width="0"/></g>' for topic in topics)
            path.write_text(f'<div id="{root_id}"><svg xmlns="http://www.w3.org/2000/svg">{nodes}</svg></div>')
            return parse_saved_graph(path)

    def test_dark_default_is_not_promoted_to_six_repetitions(self):
        node = self.parse("rgb(23, 107, 181)")["nodes"][0]
        self.assertEqual(node["legacy_display_category"], "truthy-default-not-numeric-1-through-5")
        self.assertNotIn("repetitions", node)

    def test_numeric_switch_case_is_distinct_from_fire_state(self):
        result = self.parse("rgb(165, 207, 243)")
        self.assertTrue(result["legacy_renderer_compatible"])
        self.assertEqual(result["nodes"][0]["legacy_display_category"], "numeric-case-2")

    def test_new_renderer_hsl_is_not_inverted_with_legacy_mapping(self):
        result = self.parse("hsl(208, 77%, 80%)", root_id="knowledgeGraph")
        self.assertFalse(result["legacy_renderer_compatible"])
        self.assertEqual(result["nodes"][0]["legacy_display_category"], "unrecognized-color")

    def test_gray_is_not_invented_zero(self):
        result = self.parse("rgb(242, 242, 242)")
        self.assertEqual(result["nodes"][0]["legacy_display_category"], "gray-no-numeric-constraint")

    def test_duplicate_identity_within_one_snapshot_fails(self):
        with self.assertRaisesRegex(ValueError, "Duplicate topic ID"):
            self.parse("rgb(165, 207, 243)", topics=("42", "42"))

    def test_retained_audit_counts_conflicts_without_resolving_them(self):
        path = Path(__file__).resolve().parents[1] / "engine/fire/fixtures/graph-snapshot-observations.json"
        audit = json.loads(path.read_text())
        self.assertEqual(audit["summary"]["saved_graphs"], 31)
        self.assertEqual(audit["summary"]["node_occurrences"], 6627)
        self.assertEqual(audit["summary"]["conflicting_color_topic_count"], 217)
        self.assertEqual(audit["summary"]["history_topic_overlap_count"], 129)
        self.assertEqual(audit["summary"]["verified_numeric_fire_states"], 0)


if __name__ == "__main__":
    unittest.main()
