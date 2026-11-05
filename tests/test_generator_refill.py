"""Exercise finite-domain and refill controls through the real native grader."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import uuid
from unittest.mock import patch

from generator_publish import content_fingerprint
from generator_refill import native_cases, validate_survivors, check_catalog_membership
from test_generator_pipeline import write_package
from test_generator_publish import record

ROOT = Path(__file__).resolve().parents[1]

class RefillValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.package = self.root / 'package'
        self.manifest = write_package(self.package)
        self.env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}

    def tearDown(self): self.temp.cleanup()

    def validate(self, records, inventory=None, name='check'):
        return validate_survivors(records, inventory or {'fingerprints': [], 'questions': []}, self.root / name,
            root=self.package, manifest=self.manifest, band='easy', python=sys.executable,
            repo_root=ROOT, environment=self.env)

    def catalog(self, records):
        (self.package / 'catalog.json').write_text(json.dumps(records))
        (self.package / 'generation-limits.json').write_text(json.dumps({
            'format': 'course-academy-generator-limits-v1', 'maximum_distinct_batch': {'easy': len(records)},
            'finite_catalogs': {'easy': 'catalog.json'}}))
        self.manifest['files'] += ['catalog.json', 'generation-limits.json']

    def test_native_blank_and_checkbox_controls_use_actual_answer_inputs(self):
        blank = record(4)
        checkbox = record(7)
        field = checkbox['question'][':question/answer-fields'][0]
        field[':answer-field/type'] = ':answer-field.type/checkbox'
        field[':answer-field/key'] = 'The statement is true.'
        true_id, false_id = str(uuid.uuid4()), str(uuid.uuid4())
        field[':answer-field/choices'] = [{':answer/id': aid, ':answer/type': ':answer.type/text', ':answer/value': value}
            for aid, value in [(true_id, 'true'), (false_id, 'false')]]
        field[':answer-field/correct'] = [':answer/id', true_id]
        result = self.validate([blank, checkbox])
        self.assertEqual(result['status'], 'passed')
        native = json.loads(Path(result['native_report']).read_text())
        self.assertEqual((native['accepted_checks'], native['rejected_checks']), (2, 1))
        self.assertEqual(len(result['limitations']), 1)
        self.assertTrue(all('submitted_answer_id' in row for row in native_cases([checkbox])[0]['checks']))

    def test_blank_solution_family_has_no_invented_wrong_constant_control(self):
        item = record(2)
        item['question'][':question/problem'] = 'Complete the integral with an arbitrary constant.'
        self.assertEqual(len(native_cases([item])[0]['checks']), 1)

    def test_only_nonretired_complete_native_usable_catalog_proves_exhaustion(self):
        records = [record(2), record(3)]
        self.catalog(records)
        inventory = {'fingerprints': [content_fingerprint(row['question']) for row in records],
                     'questions': [row['question'] for row in records]}
        result = self.validate([], inventory)
        self.assertTrue(result['exhausted'])
        self.assertEqual(result['status'], 'finite-limit')
        inventory['questions'][0][':question/retired'] = True
        rejected = self.validate([], inventory, 'retired')
        self.assertFalse(rejected['exhausted'])
        self.assertEqual(rejected['reason'], 'catalog_contains_retired_or_unusable_inventory')

    def test_duplicate_sample_is_not_domain_exhaustion_and_outside_domain_rejected(self):
        a, b = record(2), record(3)
        self.catalog([a, b])
        result = self.validate([], {'fingerprints': [content_fingerprint(a['question'])], 'questions': [a['question']]})
        self.assertFalse(result['exhausted'])
        self.assertEqual(result['status'], 'no-new-records')
        with self.assertRaisesRegex(ValueError, 'outside'):
            check_catalog_membership(self.package, self.manifest, 'easy', [record(99)])

    def test_package_hook_receives_survivors_and_cannot_claim_empty_coverage(self):
        item = record(2)
        fingerprint = content_fingerprint(item['question'])
        checker = self.package / 'check_refill.py'
        checker.write_text('import argparse,json\np=argparse.ArgumentParser()\np.add_argument("--records")\np.add_argument("--inventory")\np.add_argument("--output")\na=p.parse_args()\nr=json.load(open(a.records))\nassert len(r)==1 and r[0]["question"][":question/problem"]=="Compute 2+1."\njson.dump({"status":"passed","checked_fingerprints":'+repr([fingerprint])+'},open(a.output,"w"))\n')
        descriptor = self.package / 'refill-validation.json'
        descriptor.write_text(json.dumps({'format': 'course-academy-refill-check-v1', 'script': checker.name, 'args': [], 'files': []}))
        self.manifest['files'] += [checker.name, descriptor.name]
        self.assertEqual(self.validate([item])['status'], 'passed')
        checker.write_text(checker.read_text().replace(repr([fingerprint]), '[]'))
        with self.assertRaisesRegex(ValueError, 'cover every'):
            self.validate([item], name='empty-coverage')

    def test_refill_contract_cannot_execute_undeclared_file(self):
        descriptor = self.package / 'refill-validation.json'
        descriptor.write_text(json.dumps({'format': 'course-academy-refill-check-v1', 'script': '../escape.py', 'args': []}))
        self.manifest['files'].append(descriptor.name)
        with self.assertRaisesRegex(ValueError, 'declared'):
            self.validate([record(2)])

if __name__ == '__main__': unittest.main()
