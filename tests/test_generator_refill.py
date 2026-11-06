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

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from generator_publish import content_fingerprint
from generator_refill import native_cases, validate_survivors, check_catalog_membership
from generator_refill_plan import validate_refill_plan, validate_reviewed_refill, PLAN, FORMAT
from test_generator_pipeline import write_package
from test_generator_publish import record

ROOT = Path(__file__).resolve().parents[1]

class RefillValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.package = self.root / 'package'
        self.manifest = write_package(self.package)
        # Start with an actual legacy package; individual tests add the new
        # reviewed plan explicitly instead of inheriting the build fixture's plan.
        if PLAN in self.manifest['files']:
            self.manifest['files'].remove(PLAN)
            (self.package/PLAN).unlink()
            (self.package/'package.json').write_text(json.dumps(self.manifest))
        self.env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}

    def tearDown(self): self.temp.cleanup()

    def validate(self, records, inventory=None, name='check'):
        return validate_survivors(records, inventory or {'fingerprints': [], 'questions': []}, self.root / name,
            root=self.package, manifest=self.manifest, band='easy', python=sys.executable,
            repo_root=ROOT, environment=self.env)

    def checker(self, records, body='', *, check_results=None):
        fingerprints=sorted(content_fingerprint(row['question']) for row in records)
        report={'status':'passed','checked_fingerprints':fingerprints}
        if check_results is not None:report['check_results']=check_results
        path=self.package/'check_refill.py'
        path.write_text('import argparse,json,os\nfrom pathlib import Path\np=argparse.ArgumentParser()\np.add_argument("--records")\np.add_argument("--inventory")\np.add_argument("--output")\na=p.parse_args()\nr=json.load(open(a.records))\ni=json.load(open(a.inventory))\n'+body+'\njson.dump('+repr(report)+',open(a.output,"w"))\n')
        (self.package/'refill-validation.json').write_text(json.dumps({
            'format':'course-academy-refill-check-v1','script':path.name,'args':[],'files':[]}))
        for name in (path.name,'refill-validation.json'):
            if name not in self.manifest['files']:self.manifest['files'].append(name)

    def plan(self, *, required=False, findings=(), exemptions=()):
        evidence=self.root/'evidence';evidence.mkdir(exist_ok=True)
        (evidence/'source-analysis.json').write_text('{"learner_operation":"Compute the displayed sum independently."}')
        value={'format':FORMAT,'status':'checks' if required else 'not_applicable',
               'reason':'Check sums on survivors.' if required else 'No retained semantic survivor condition; contextual checks were separately reviewed.',
               'source_refs':['fixture-source'],'evidence_paths':['source-analysis.json'],
               'checks':[{'id':'sum','purpose':'Recompute the answer from the displayed operands.',
                          'finding_ids':list(findings)}] if required else [],
               'finding_exemptions':list(exemptions)}
        (self.package/PLAN).write_text(json.dumps(value))
        if PLAN not in self.manifest['files']:self.manifest['files'].append(PLAN)
        return evidence

    def test_new_approval_requires_explicit_applicability_and_every_retained_finding(self):
        with self.assertRaisesRegex(ValueError,'New approval requires'):
            validate_refill_plan(self.package,self.manifest,[],self.root)
        evidence=self.plan()
        binding=validate_refill_plan(self.package,self.manifest,[],evidence)
        self.assertEqual(binding['status'],'not_applicable')
        with self.assertRaisesRegex(ValueError,'every retained finding'):
            validate_refill_plan(self.package,self.manifest,[{'id':'old-sum-defect'}],evidence)
        evidence=self.plan(exemptions=[{'id':'old-sum-defect','reason':'Old defect concerned a removed display layout, not surviving arithmetic.',
            'source_refs':['fixture-source'],'evidence_paths':['source-analysis.json']}])
        self.assertEqual(validate_refill_plan(self.package,self.manifest,[{'id':'old-sum-defect'}],evidence)['finding_ids'],['old-sum-defect'])

    def test_applicable_retained_check_is_bound_and_runs_on_actual_survivors(self):
        item=record(11)
        fingerprint=content_fingerprint(item['question'])
        self.checker([item],body='assert int(r[0]["question"][":question/answer-fields"][0][":answer-field/choices"][0][":answer/value"]) == int(r[0]["question"][":question/problem"].split()[1].split("+")[0])+1',
            check_results=[{'id':'sum','status':'passed','checked_fingerprints':[fingerprint]}])
        evidence=self.plan(required=True,findings=['old-sum-defect'])
        binding=validate_refill_plan(self.package,self.manifest,[{'id':'old-sum-defect'}],evidence)
        result = self.validate([item])
        self.assertEqual(result['refill_plan'],binding)
        self.assertEqual(result['status'], 'passed')
        self.assertFalse(result['exhausted'])
        self.assertIn('Validated actual surviving records', result['scope'])
        self.assertNotIn('No distinct catalog question remains', result['scope'])
        wrong=copy.deepcopy(item)
        wrong['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='999'
        with self.assertRaisesRegex(ValueError,'declared-file isolation'):
            self.validate([wrong],name='wrong')
        self.checker([item])
        with self.assertRaisesRegex(ValueError,'approved check_results'):
            self.validate([item],name='missing-check')

    def test_undeclared_data_and_imports_cannot_supply_refill_evidence(self):
        item=record(2)
        self.checker([item],body='Path("scratch-only.txt").read_text()')
        with self.assertRaisesRegex(ValueError,'declared-file isolation'):
            self.validate([item],name='undeclared-data')
        (self.package/'secret_support.py').write_text('VALUE=42\n')
        self.env['PYTHONPATH']=str(self.package)
        self.env['COURSE_ACADEMY_WORKSPACE']=str(self.package)
        self.checker([item],body='import secret_support')
        with self.assertRaisesRegex(ValueError,'declared-file isolation'):
            self.validate([item],name='undeclared-import')
        self.manifest['files'].append('secret_support.py')
        self.checker([item],body='import secret_support,sympy\nassert secret_support.VALUE==42\nassert sympy.Integer(2)+1==3\nassert "PYTHONPATH" not in os.environ\nassert "COURSE_ACADEMY_WORKSPACE" not in os.environ\nassert Path.cwd()!=Path('+repr(str(self.package))+')')
        self.assertEqual(self.validate([item],name='declared-import')['status'],'passed')

    def test_checker_receives_usable_inventory_questions_and_content_hashes(self):
        survivor,old,retired=record(8),record(2),record(3)
        retired['question'][':question/retired']=True
        inventory={'fingerprints':[content_fingerprint(row['question']) for row in (old,retired)],
                   'questions':[old['question'],retired['question'],{':question/problem':'incomplete'}]}
        self.checker([survivor],body='assert len(i["questions"])==1\nassert i["questions"][0][":question/problem"]=="Compute 2+1."\nassert len(i["questions_sha256"])==64\nassert len(i["usable_fingerprints"])==1\nassert len(i["fingerprints"])==2')
        self.assertEqual(self.validate([survivor],inventory)['status'],'passed')

    def test_contextual_equivalent_and_wrong_controls_run_through_native_grader(self):
        item=record(2);fingerprint=content_fingerprint(item['question'])
        self.checker([item],check_results=[{'id':'sum','status':'passed','checked_fingerprints':[fingerprint]}])
        self.plan(required=True)
        checker=self.package/'check_refill.py'
        text=checker.read_text()
        extra=[{'fingerprint':fingerprint,'checks':[
            {'field_index':0,'submitted':'3.0','expected':'accepted','purpose':'Same exact integer in decimal notation.'},
            {'field_index':0,'submitted':'4','expected':'rejected','purpose':'Off-by-one sum.'}]}]
        checker.write_text(text.replace('json.dump({','json.dump({"native_checks":'+repr(extra)+','))
        result=self.validate([item])
        native=json.loads(Path(result['native_report']).read_text())
        self.assertEqual((native['accepted_checks'],native['rejected_checks']),(2,1))
        checker.write_text(checker.read_text().replace("'submitted': '3.0'","'submitted': '4'"))
        with self.assertRaisesRegex(ValueError,'Native refill grading failed'):
            self.validate([item],name='failed-native-control')

    def test_legacy_fallback_is_explicit_and_approved_plan_cannot_disappear(self):
        self.assertTrue(self.validate([record(2)])['legacy_fallback'])
        evidence=self.plan();binding=validate_refill_plan(self.package,self.manifest,[],evidence)
        self.manifest['files'].remove(PLAN)
        with self.assertRaisesRegex(ValueError,'Approved refill plan is missing'):
            validate_survivors([record(2)],{'fingerprints':[],'questions':[]},self.root/'missing-plan',
                root=self.package,manifest=self.manifest,band='easy',python=sys.executable,
                repo_root=ROOT,environment=self.env,expected_plan=binding)

    def test_new_approval_executes_retained_checks_after_real_three_band_deduplication(self):
        from generator_source_policy import POLICY_VERSION
        batches,old_rows,expected={},{},{}
        for index,band in enumerate(('easy','moderate','hard')):
            old,new=record(2+index),record(8)
            for row in (old,new):
                row['knowledge_point']=123
                row['question'][':question/difficulty']=':question.difficulty/'+band
            old_rows[band]=old
            expected[':question.difficulty/'+band]=content_fingerprint(new['question'])
            path=self.root/(band+'.json');path.write_text(json.dumps([old,new]))
            batches[band]={'batch_file':str(path),'assets_directory':str(self.root)}
        self.checker([record(8)])
        checker=self.package/'check_refill.py'
        before=checker.read_text().split('json.dump(')[0]
        checker.write_text(before+'\nassert len(r)==1 and r[0]["question"][":question/problem"]=="Compute 8+1."\nassert len(i["questions"])==3\nf='+repr(expected)+'[r[0]["question"][":question/difficulty"]]\njson.dump({"status":"passed","checked_fingerprints":[f],"check_results":[{"id":"sum","status":"passed","checked_fingerprints":[f]}]},open(a.output,"w"))\n')
        evidence=self.plan(required=True,findings=['old-sum-defect'])
        source={'database':'fixture','lineage':'fixture','kp_id':123,'material':{
            'kp':{':knowledge-point/id':'00000000-0000-4000-8000-000000000123'},
            'source_eligibility':{'policy_version':POLICY_VERSION,'excluded_questions':[]}}}
        inventory={key:source[key] for key in ('database','lineage','kp_id')}
        inventory.update(basis=1,questions=[row['question'] for row in old_rows.values()],
                         fingerprints=[content_fingerprint(row['question']) for row in old_rows.values()])
        result=validate_reviewed_refill(self.package,self.manifest,[{'id':'old-sum-defect'}],evidence,
            batches=batches,source=source,inventory=inventory,math_root=self.root/'math',
            repo_root=ROOT,python=sys.executable,environment=self.env)
        self.assertEqual(set(result['bands']),{'easy','moderate','hard'})
        for band in result['bands'].values():
            delivery=json.loads(Path(band['delivery']).read_text())
            self.assertEqual((delivery['input_count'],delivery['accepted_count']),(2,1))
            self.assertEqual(json.loads(Path(band['report']).read_text())['package_check_scope'],'survivors')

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
        self.assertIn('No distinct catalog question remains', result['scope'])
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
