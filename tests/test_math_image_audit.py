"""Formula-image auditing must distinguish formulas from labeled diagrams."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import hashlib
import contextlib
import io

spec = importlib.util.spec_from_file_location("math_image_audit", Path(__file__).parents[1] / "scripts/audit_math_image_imports.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

FORMULA = '<svg width="2ex" height="1ex"><g><g data-mml-node="math"><path data-c="78" d="M0 0"/></g></g></svg>'


class MathImageAuditTests(unittest.TestCase):
    def test_formula_signatures_do_not_flag_a_diagram_just_for_having_math_labels(self):
        self.assertEqual(audit.svg_kind(FORMULA)[0], "math-svg")
        self.assertEqual(audit.svg_kind('<svg width="300" height="100"><path d="M0 0 L5 5"/></svg>')[0], "non-math-svg")
        labeled = FORMULA.replace('width="2ex" height="1ex"', 'width="300" height="100"').replace('</svg>', '<circle r="4"/></svg>')
        self.assertEqual(audit.svg_kind(labeled)[0], "mixed-math-graphic")
        self.assertEqual(audit.svg_kind('<svg width="2ex" height="1ex"><use href="#MJX-TEX-I-78"/></svg>')[0], "math-svg")

    def test_raster_metadata_and_repeated_uses_are_preserved_with_topic_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            png = b'captured-formula-pixels'
            digest = hashlib.sha256(png).hexdigest()
            relative = f'images/{digest[:2]}/{digest}.png'
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_bytes(png)
            evidence = root / 'capture.json'
            evidence.write_text(json.dumps({'assets':[{'tag':'svg','html':FORMULA,'sha256':digest,'representation':'rendered'}]}))
            snapshot = root / 'facts.jsonl'
            rows = [(1,'topic/math-academy-id',1036), (1,'topic/knowledge-points',2),
                    (2,'knowledge-point/canonical-example',3), (3,'question/math-academy-id','e-731'),
                    (3,'question/problem',f'If ![]({relative}), find ![]({relative}).'),
                    (4,'answer/feedback',f'![]({relative})')]
            snapshot.write_text(''.join(json.dumps({'e':e,'a':a,'v':v,'tx':99,'t':9,'source':8})+'\n' for e,a,v in rows))
            snapshot.with_suffix('.manifest.json').write_text('{"basis_t":9}')
            with contextlib.redirect_stdout(io.StringIO()):
                audit.run(snapshot, root, [evidence], root / 'report')
            summary = json.loads((root / 'report/summary.json').read_text())
            self.assertEqual(summary['confirmed_math_image_occurrences'], 3)
            self.assertEqual(summary['confirmed_affected_attributes'], 2)
            self.assertEqual(summary['noncanonical_image_facts'], 0)
            findings = json.loads((root / 'report/findings.json').read_text())
            question = next(f for f in findings if f['e'] == 3)
            self.assertEqual(len(question['math_images']), 2)
            self.assertTrue(any(c.get('topic/math-academy-id') == 1036 for c in question['context']))

    def test_unknown_rasters_and_noncanonical_images_are_not_silently_cleared(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = b'unknown-pixels'; digest = hashlib.sha256(raw).hexdigest()
            relative = f'images/{digest[:2]}/{digest}.png'; path = root / relative
            path.parent.mkdir(parents=True); path.write_bytes(raw)
            snapshot = root / 'facts.jsonl'
            snapshot.write_text(json.dumps({'e':1,'a':'multistep/context','v':f'![]({relative}) ![](https://example.org/formula.png)','t':1,'tx':1,'source':2})+'\n')
            snapshot.with_suffix('.manifest.json').write_text('{"basis_t":1}')
            with contextlib.redirect_stdout(io.StringIO()):
                audit.run(snapshot, root, [], root / 'report')
            summary = json.loads((root / 'report/summary.json').read_text())
            self.assertEqual(summary['assets_by_kind']['unclassified-raster'], 1)
            self.assertEqual(summary['noncanonical_image_facts'], 1)
            self.assertEqual(summary['confirmed_affected_entities'], 0)


if __name__ == '__main__':
    unittest.main()
