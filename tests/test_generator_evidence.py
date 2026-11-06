"""Tool evidence must describe real nonempty inputs, not just a success label."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import shutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.generator_evidence import record_sha256, sha256_file, validate_tool_report
from generator_review_fixtures import write_tool_evidence


class ToolEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.paths = write_tool_evidence(self.root, [{'fixture': True, 'actual_prompt': 'Square 2.'}])

    def report(self, kind):
        path = self.root / self.paths[kind]
        return path, json.loads(path.read_text())

    def test_record_identity_includes_solution_and_grader_contract(self):
        record = {'question': {':question/problem': 'Square 2.', ':question/worked-solution': '2×2=4.',
                              ':question/answer-fields': [{'key': 'answer', 'value': '4'}]}}
        original = record_sha256(record)
        record['question'][':question/worked-solution'] = '2×2=5.'
        self.assertNotEqual(original, record_sha256(record))

    def test_tampered_test_response_and_rendered_record_are_rejected(self):
        path, report = self.report('grading')
        report['records'][0]['checks'][0]['submitted_input'] = 'wrong input'
        path.write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError, 'response differs'):
            validate_tool_report(path, self.root)
        path, report = self.report('rendering')
        report['cases'][0]['record_sha256'] = '0' * 64
        path.write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError, 'mismatched input'):
            validate_tool_report(path, self.root)

    def test_failed_tools_and_stale_current_implementation_are_rejected(self):
        path, original = self.report('rendering')
        failed = copy.deepcopy(original); failed['passed'] = False
        path.write_text(json.dumps(failed))
        with self.assertRaisesRegex(ValueError, 'not passed'):
            validate_tool_report(path, self.root)
        original['implementation_sha256'] = {'generate/pipeline/render_preview.py': '0' * 64}
        path.write_text(json.dumps(original))
        with self.assertRaisesRegex(ValueError, 'implementation changed'):
            validate_tool_report(path, self.root)

    def test_zero_checked_records_and_changed_capture_cannot_pass(self):
        path, report = self.report('grading')
        report['checked_record_sha256'] = []
        path.write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError, 'coverage is empty'):
            validate_tool_report(path, self.root)
        path, report = self.report('delivery')
        (self.root / report['captured_inputs']['inventory']['file']).write_text('{"different":true}')
        with self.assertRaisesRegex(ValueError, 'inventory hash mismatch'):
            validate_tool_report(path, self.root)

    def test_native_harness_rejects_zero_input_and_zero_checks(self):
        binary = ROOT / 'generate/runs/current/check-engine'
        if not binary.is_file():
            self.skipTest('Native grading executable must be built for this integration check')
        for value, message in (([], 'nonempty records'), ([{'record': {}, 'checks': []}], 'nonempty checks')):
            source = self.root / 'native-input.json'; source.write_text(json.dumps(value))
            result = subprocess.run([str(binary), str(source), str(self.root / 'native.json')],
                                    capture_output=True, text=True, timeout=20)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(message, result.stderr)

    def test_grading_requires_compiled_source_and_dependency_provenance(self):
        path, report = self.report('grading')
        validate_tool_report(path, self.root)
        report['compiled_inputs_sha256'] = 'f' * 64
        path.write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError, 'native build provenance'):
            validate_tool_report(path, self.root)
        report['compiled_inputs_sha256'] = report['native_build']['inputs_sha256']
        report['native_build']['dependencies'] = {}
        path.write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError, 'native build provenance'):
            validate_tool_report(path, self.root)

    def test_native_executable_rejects_unrelated_build_sidecar(self):
        original = ROOT / 'generate/runs/current/check-engine'
        if not original.with_suffix('.build.json').is_file():
            self.skipTest('Build the native grader before its integration controls')
        binary = self.root / 'check-engine'; shutil.copy2(original, binary)
        metadata = json.loads(original.with_suffix('.build.json').read_text())
        metadata['inputs_sha256'] = '0' * 64
        binary.with_suffix('.build.json').write_text(json.dumps(metadata))
        source = self.root / 'input.json'; source.write_text('[]')
        result = subprocess.run([str(binary), str(source), str(self.root / 'report.json')],
                                capture_output=True, text=True, timeout=20)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('provenance does not identify this compiled binary', result.stderr)


if __name__ == '__main__':
    unittest.main()
