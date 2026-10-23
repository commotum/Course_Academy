"""Selection, certificate and mechanical-adoption regressions; no agents or DB."""
from datetime import datetime
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from generator_cohort import CohortPipeline, build_cohort, first_seen, in_cohort, mechanical_package, current_approval, capacity_failure
from generator_pipeline import Pipeline, digest
from generator_review import CHECKS
from inventory_jobs import save


class CohortTests(unittest.TestCase):
    def inventory_pipeline(self, directory, pipeline_type=CohortPipeline):
        directory=Path(directory)
        publisher=Mock()
        pipeline=pipeline_type(directory,{'kp':123,'difficulty':'easy','count':5},publisher,session=Mock())
        source={'database':'fixture','lineage':'lineage','kp_id':123}
        publisher.client.status.return_value={**source,'basis':1}
        save(directory/'source/source.json',source)
        before={**source,'basis':1,'questions':[{':db/id':7,':question/retired':False}]}
        after={**source,'basis':2,'questions':[{':db/id':7,':question/retired':True}]}
        save(directory/'source/inventory.json',before)
        def extract(kp,path):
            save(path/'inventory.json',after)
            return after
        publisher.extract_inventory.side_effect=extract
        review=directory/'review-1-policy-2-test';review.mkdir()
        finding={'kind':'inventory','description':'Stored generated question has a shortcut.',
                 'reproduction':'Replay historical seed 7','requested_change':'Retire the unused generated record.',
                 'source_refs':[]}
        result={'verdict':'revise','summary':'Stored pool requires repair.','source_analysis':{
            'skill':'Calculate a square.','reasoning_steps':[],'invariants':[],
            'permitted_variations':[],'source_refs':[],'evidence_paths':[]},
            'checks':{name:{'status':'not_applicable','details':'Inventory-only fixture.',
                'evidence_paths':[]} for name in CHECKS},'findings':[finding]}
        save(review/'result.json',result)
        save(review/'affected-inventory.json',{'affected_questions':[{
            'question_id':'3f9ccaa5-d69c-584d-946e-0c57b3050160','entity_id':7,
            'finding':'shortcut','reproduction':'seed 7','evidence_path':'records.json'}]})
        save(review/'records.json',[{'question':{':question/id':'3f9ccaa5-d69c-584d-946e-0c57b3050160'},
                                    'generation':{'seed':7}}])
        pipeline.persist(source_hash=digest(source),inventory_hash=digest(before),stage='validate',
            previous_review={'directory':str(review),'binding':{'source_hash':digest(source)}})
        return pipeline,review,result,before,after

    def test_inventory_only_defect_is_repaired_before_fresh_review_without_an_author(self):
        with tempfile.TemporaryDirectory() as t:
            pipeline,review,result,before,after=self.inventory_pipeline(t)
            with patch('generator_pool_repair.repair_pool',return_value={'retired':[7],'unresolved':[]}) as repair, \
                    patch.object(pipeline,'check_repair_regressions') as regressions, \
                    patch.object(pipeline,'sample') as sample, \
                    patch.object(pipeline,'candidate_hash',return_value='unchanged-runtime'):
                pipeline.repair(result)
            repair.assert_called_once()
            self.assertEqual(repair.call_args.args[2],[review/'affected-inventory.json'])
            pipeline.session.assert_not_called()
            regressions.assert_called_once();sample.assert_called_once()
            self.assertEqual(pipeline.state['stage'],'validate')
            self.assertEqual(pipeline.state['inventory_hash'],digest(after))
            self.assertEqual(json.loads(Path(pipeline.state['pool_repair']['baseline']).read_text()),before)
            history=json.loads((Path(t)/'repair-history.json').read_text())
            self.assertEqual(history['findings'][0]['finding']['kind'],'inventory')
            with patch('generator_pool_repair.repair_pool') as repeated:
                pipeline.repair(result)
            repeated.assert_not_called()
            self.assertEqual(pipeline.state['stage'],'blocked')

    def test_mixed_inventory_and_generator_findings_send_only_generator_work_to_author(self):
        with tempfile.TemporaryDirectory() as t:
            pipeline,_,result,_,_=self.inventory_pipeline(t)
            math={**result['findings'][0],'kind':'math','description':'Generator computes the wrong square.'}
            result={**result,'findings':[*result['findings'],math]}
            with patch('generator_pool_repair.repair_pool',return_value={'retired':[7],'unresolved':[]}), \
                    patch.object(pipeline,'engine_identity',return_value='fixture-engine'):
                pipeline.repair(result)
            self.assertEqual(pipeline.state['stage'],'generate')
            self.assertEqual(json.loads((Path(t)/'feedback.json').read_text())['findings'],[math])

    def test_unresolved_inventory_blocks_before_author_or_publication(self):
        with tempfile.TemporaryDirectory() as t:
            pipeline,_,result,_,_=self.inventory_pipeline(t)
            with patch('generator_pool_repair.repair_pool',return_value={
                    'retired':[],'unresolved':[{'question':7,'reason':'canonical_example'}]}):
                pipeline.repair(result)
            self.assertEqual(pipeline.state['stage'],'blocked')
            self.assertEqual(pipeline.state['error']['code'],'inventory_repair_blocked')
            pipeline.session.assert_not_called()
            pipeline.publisher.publish.assert_not_called()

    def test_inventory_repair_requires_valid_bound_review_and_preserves_publication_intent(self):
        with tempfile.TemporaryDirectory() as t:
            pipeline,review,_,_,_=self.inventory_pipeline(t)
            with patch('generator_pool_repair.repair_pool') as repair:
                save(review/'result.json',{'verdict':'accepted'})
                with self.assertRaises(ValueError):pipeline.repair_inventory(review)
                repair.assert_not_called()
        with tempfile.TemporaryDirectory() as t:
            pipeline,review,_,_,_=self.inventory_pipeline(t)
            save(Path(t)/'publication/request.json',{'request':'exact-saved-bytes'})
            with patch('generator_pool_repair.repair_pool') as repair:
                with self.assertRaisesRegex(ValueError,'saved publication request'):
                    pipeline.repair_inventory(review)
                repair.assert_not_called()
            self.assertEqual(json.loads((Path(t)/'publication/request.json').read_text()),
                             {'request':'exact-saved-bytes'})

    def test_inventory_repair_checks_database_identity_before_any_mutation(self):
        with tempfile.TemporaryDirectory() as t:
            pipeline,review,_,_,_=self.inventory_pipeline(t)
            pipeline.publisher.client.status.return_value={'database':'other','lineage':'wrong-lineage'}
            with patch('generator_pool_repair.repair_pool') as repair:
                with self.assertRaisesRegex(ValueError,'reviewed database and lineage'):
                    pipeline.repair_inventory(review)
                repair.assert_not_called()

    def test_accepted_report_with_new_pool_repairs_requires_fresh_independent_review(self):
        from test_generator_pipeline import FakeSession
        with tempfile.TemporaryDirectory() as t:
            pipeline,review,_,_,_=self.inventory_pipeline(t)
            result=FakeSession()('review',{},review)
            pipeline.session.return_value=result
            pipeline.persist(previous_review={'directory':str(review),'binding':pipeline.review_binding()})
            with patch.object(pipeline,'context',return_value={}), \
                    patch.object(pipeline,'verify_approval_inputs'), \
                    patch.object(pipeline,'repair_inventory',return_value={'inventory_changed':True,'unresolved':[]}):
                self.assertIsNone(pipeline.review_candidate(review))
            self.assertEqual(pipeline.state['stage'],'validate')
            pipeline.publisher.publish.assert_not_called()

    def test_plain_pipeline_routes_inventory_findings_to_runner_without_author(self):
        with tempfile.TemporaryDirectory() as t:
            pipeline,_,result,_,_=self.inventory_pipeline(t,pipeline_type=Pipeline)
            with patch('generator_pool_repair.repair_pool',return_value={'retired':[7],'unresolved':[]}), \
                    patch.object(pipeline,'check_repair_regressions'), \
                    patch.object(pipeline,'sample'), \
                    patch.object(pipeline,'candidate_hash',return_value='unchanged-runtime'):
                pipeline.repair(result)
            self.assertEqual(pipeline.state['stage'],'validate')
            pipeline.session.assert_not_called()

    def test_equivalent_report_in_new_directory_does_not_repeat_inventory_work(self):
        with tempfile.TemporaryDirectory() as t:
            pipeline,review,_,_,_=self.inventory_pipeline(t)
            with patch('generator_pool_repair.repair_pool',return_value={'retired':[7],'unresolved':[]}) as repair:
                self.assertTrue(pipeline.repair_inventory(review)['inventory_changed'])
                another=Path(t)/'review-2-policy-2-new-binding'
                shutil.copytree(review,another)
                pipeline.persist(previous_review={'directory':str(another),
                    'binding':{'source_hash':pipeline.state['source_hash']}})
                self.assertFalse(pipeline.repair_inventory(another)['inventory_changed'])
            repair.assert_called_once()
            pipeline.publisher.extract_inventory.assert_called_once()

    def test_unrelated_basis_change_does_not_replace_reviewed_inventory_or_loop_reviews(self):
        with tempfile.TemporaryDirectory() as t:
            pipeline,review,_,before,_=self.inventory_pipeline(t)
            fresh={**before,'basis':999}
            def extract(kp,path):
                save(path/'inventory.json',fresh)
                return fresh
            pipeline.publisher.extract_inventory.side_effect=extract
            with patch('generator_pool_repair.repair_pool',return_value={'retired':[],'unresolved':[]}):
                result=pipeline.repair_inventory(review)
            self.assertFalse(result['inventory_changed'])
            self.assertEqual(pipeline.state['inventory_hash'],digest(before))
            self.assertEqual(json.loads((Path(t)/'source/inventory.json').read_text()),before)
            self.assertEqual(json.loads(Path(result['fresh_inventory']).read_text()),fresh)

    def test_repair_retains_the_source_calibrated_default_without_another_author_session(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);(root/'workspace').mkdir();path=root/'workspace/package.json'
            path.write_text(json.dumps({'entrypoint':'generator.py','files':['generator.py']}))
            pipeline=object.__new__(CohortPipeline);pipeline.directory=root
            pipeline.state={'request':{'difficulty':'unclassified'},'manifest':'package.json','adopted_default_difficulty':'easy'}
            with patch.object(Pipeline,'sample',return_value='sampled'):
                self.assertEqual(pipeline.sample(),'sampled')
            self.assertEqual(json.loads(path.read_text())['default_difficulty'],'easy')

    def test_unchanged_archived_package_does_not_publish_new_questions(self):
        with tempfile.TemporaryDirectory() as t:
            directory=Path(t);(directory/'source').mkdir()
            sha='a'*64
            (directory/'source/source.json').write_text(json.dumps({'registered_generator':{':question-generator/script':f'generators/aa/{sha}/generator.py'}}))
            records=[{'question':'reviewed local sample'}];(directory/'samples.json').write_text(json.dumps(records))
            pipeline=object.__new__(CohortPipeline);pipeline.directory=directory;pipeline.state={'package_hash':sha}
            self.assertEqual(pipeline.publication_records(),[])
            pipeline.state['package_hash']='b'*64
            self.assertEqual(pipeline.publication_records(),records)

    def test_provider_capacity_stops_the_campaign_without_matching_ordinary_failures(self):
        self.assertTrue(capacity_failure('{"code":"usage_limit_reached"}'))
        self.assertTrue(capacity_failure("You've hit your usage limit"))
        self.assertFalse(capacity_failure('Generator rejected ambiguous answer banks'))

    def test_cutoff_uses_earliest_evidence_and_includes_unknown_age(self):
        dates=first_seen('DATE 2026-10-17T01:00:00+00:00\ngenerate/scratch/a.py\nDATE 2026-10-15T01:00:00+00:00\ngenerate/scratch/a.py\n')
        cutoff=datetime.fromisoformat('2026-10-16T21:51:26+00:00').timestamp()
        self.assertTrue(in_cohort(dates['generate/scratch/a.py'],cutoff))
        self.assertTrue(in_cohort(None,cutoff))
        self.assertFalse(in_cohort(cutoff,cutoff))

    def test_subject_priority_does_not_exclude_other_old_generators(self):
        rows=[[1,'Old algebra',11,'Matrix','a.py'],[2,'Old other',22,'Trig','b.py'],[3,'New DEQ',33,'ODE','c.py'],[4,'Unknown',44,'Other','d.py']]
        subjects=[[90,'Linear Algebra',11],[91,'Differential Equations',33]]
        items=build_cohort(rows,subjects,[{'kp_id':2},{'kp_id':1}],{'a.py':1,'b.py':1,'c.py':20},10)
        self.assertEqual([i['kp'] for i in items],[1,2,4])
        self.assertEqual(items[-1]['age_evidence'],'unknown_included')

    def test_legacy_adoption_preserves_bytes_resources_and_local_imports(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);script=root/'old.py';source=b'import json\nfrom pathlib import Path\nfrom helper import value\nprint(json.loads(Path(__file__).with_suffix("").joinpath("source.json").read_text()))\n'
            script.write_bytes(source);(root/'helper.py').write_text('value=3\n')
            resources=root/'old';resources.mkdir();(resources/'source.json').write_text('{"a":1}')
            # A retained evidence script is data, not a runtime dependency.
            (resources/'old_test.py').write_text('import nonexistent_test_dependency\n')
            manifest=mechanical_package(script,root/'workspace',{'available_difficulties':['easy']})
            self.assertEqual((root/'workspace/old.py').read_bytes(),source)
            self.assertIn('old/source.json',manifest['files']);self.assertIn('helper.py',manifest['files'])
            self.assertEqual(manifest['dependencies']['packages'],{})
            self.assertEqual(manifest['default_difficulty'],'easy')

    def test_package_or_registration_without_a_current_certificate_is_not_a_skip(self):
        with tempfile.TemporaryDirectory() as t:
            for script in ['generate/scratch/1.py','generators/aa/'+('a'*64)+'/generator.py']:
                self.assertIsNone(current_approval({'kp_id':1,'registered_generator':{':question-generator/script':script}},Path(t)))


if __name__=='__main__':unittest.main()
