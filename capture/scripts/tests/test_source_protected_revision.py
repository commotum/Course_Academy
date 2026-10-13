"""MA recaptures must not undo separately attributed authored corrections."""
import copy
import json
import tempfile
import threading
import unittest

from scripts.database.edn import kw
from scripts.database.evidence import UnsupportedContent
from scripts.database.pipeline import DatabasePipeline
from scripts.database.prepare import Plan, Preparation, scalar, source_uuid
from scripts.storage import atomic_json
from scripts.tests import test_database as database_tests
from scripts.tests.test_database import FakeClient, question, source_snapshot

AGENT = ':agent/gpt-6-astra-ultra'


def attributed_snapshot():
    data = source_snapshot()
    answers = [{':db/id': eid, ':answer/id': source_uuid('answer', eid),
                ':answer/type': {':db/id': 902, ':db/ident': kw('answer.type/math')},
                ':answer/value': value} for eid, value in ((20, '2'), (21, '3'))]
    field = {':db/id': 10, ':answer-field/id': source_uuid('field', 10), ':answer-field/key': 'x',
             ':answer-field/type': {':db/id': 901, ':db/ident': kw('answer-field.type/blank')},
             ':answer-field/choices': answers, ':answer-field/correct': answers[0]}
    old = {':db/id': 5, ':question/id': source_uuid('question', 5), ':question/math-academy-id': 'q-11',
           ':question/problem': 'Corrected source wording.', ':question/worked-solution': '$1+1=2$',
           ':question/answer-fields': [field]}
    data['entities'].extend([old, field, *answers])
    data['idents'].extend([[950, kw(AGENT)], [901, kw('answer-field.type/blank')], [902, kw('answer.type/math')]])
    data['facts'] = []
    for entity in [old, field, *answers]:
        for attr, value in entity.items():
            if attr == ':db/id':
                continue
            for member in value if isinstance(value, list) else [value]:
                data['facts'].append([entity[':db/id'], attr[1:], scalar(member), 900])
    return data, old


class SourceProtectedRevisionTests(unittest.TestCase):
    def test_lesson_can_reference_its_existing_corrected_canonical_example(self):
        data, _ = attributed_snapshot()
        data['facts'].append([3,'question/problem','Example',950])
        example=question('e-10');example['answer_fields']=[]
        example['knowledge_point_id']=str(data['entities'][1][':knowledge-point/id'])
        prepared=Preparation(data).prepare({'task_id':'77','kind':'lesson','topic_id':1,
            'questions':[],'canonical_examples':[example],
            'lesson_definition':{'complete':True,'steps':[{'type':'example','content_id':10}]}})
        self.assertFalse(any(o.get('kind')=='lesson' for o in prepared['omissions']))
        assertions=[a for b in prepared['batches'] for a in b['assertions']]
        self.assertTrue(any(a[1]==':step/content' and a[2]==2 for a in assertions))
        self.assertFalse(any(a[1].startswith(':question/')for a in assertions))
    def test_review_can_reference_corrected_question_without_rewriting_it(self):
        data, old = attributed_snapshot()
        next(row for row in data['facts'] if row[:2]==[5,'question/problem'])[3]=950
        before=copy.deepcopy(data)
        q=question();q['knowledge_point_id']=str(data['entities'][1][':knowledge-point/id'])
        prepared=Preparation(data).prepare({'task_id':'77','kind':'review','topic_id':1,
            'title':'Addition review','questions':[q],'question_order':['q-11']})
        self.assertEqual(prepared['omissions'][0]['constraint'],'separately_attributed_correction')
        self.assertFalse(any(o.get('kind')=='review' for o in prepared['omissions']))
        assertions=[a for b in prepared['batches'] for a in b['assertions']]
        self.assertTrue(any(a[1]==':step/content' and a[2]==5 for a in assertions))
        self.assertFalse(any(a[1].startswith((':question/',':answer-field/',':answer/'))for a in assertions))
        self.assertEqual(data,before)
    def test_foreign_authored_question_field_or_owned_answer_refuses_without_plan_mutation(self):
        for eid, attr in [(5, 'question/problem'), (5, 'question/worked-solution'),
                          (5, 'question/answer-fields'), (10, 'answer-field/key'),
                          (10, 'answer-field/type'), (10, 'answer-field/correct'),
                          (10, 'answer-field/choices'), (20, 'answer/type'), (21, 'answer/value')]:
            with self.subTest(attribute=attr):
                data, old = attributed_snapshot()
                for row in data['facts']:
                    if row[0] == eid and row[1] == attr:
                        row[3] = 950
                prep = Preparation(data)
                plan = Plan(prep.snapshot)
                with self.assertRaisesRegex(UnsupportedContent, 'separately attributed content'):
                    prep.question(plan, question(), old, False)
                self.assertEqual(plan.finish()['forms'], [])
                self.assertEqual(plan.local, {})

    def test_equal_ma_and_agent_claims_cannot_be_reattributed(self):
        data, old = attributed_snapshot()
        row = next(row for row in data['facts'] if row[:2] == [5, 'question/problem'])
        data['facts'].append([*row[:3], 950])
        # The observed MA wording can even equal the corrected current value.
        with self.assertRaisesRegex(UnsupportedContent, AGENT):
            Preparation(data).check_source_attribution(old)

    def test_agent_corrected_correct_ref_alone_protects_current_field_graph(self):
        data, old = attributed_snapshot()
        field = old[':question/answer-fields'][0]
        field[':answer-field/correct'] = field[':answer-field/choices'][1]
        for row in data['facts']:
            if row[:2] == [10, 'answer-field/correct']:
                row[2:] = [21, 950]
        before = copy.deepcopy(old)
        prep = Preparation(data)
        plan = Plan(prep.snapshot)
        with self.assertRaisesRegex(UnsupportedContent, 'answer-field/correct'):
            prep.question(plan, question(answer='2'), old, False)
        self.assertEqual(plan.finish()['forms'], [])
        self.assertEqual(old, before)
        self.assertEqual(field[':answer-field/correct'][':answer/value'], '3')

    def test_uuid_only_foreign_provenance_and_unrelated_derived_or_retired_facts_do_not_block(self):
        data, old = attributed_snapshot()
        for row in data['facts']:
            if row[1].endswith('/id'):
                row[3] = 950
        data['facts'].extend([[2, 'knowledge-point/title', 'Agent metadata', 950],
                              [20, 'task-item/responses', 20, 950],
                              [99, 'answer/value', 'Retired correction', 950],
                              [5, 'question/problem', 'A former correction, absent from current content', 950]])
        Preparation(data).check_source_attribution(old)

    def test_ordinary_ma_only_answer_repair_reuses_field_identity_and_owned_values(self):
        data, old = attributed_snapshot()
        prep = Preparation(data)
        plan = Plan(prep.snapshot)
        q = question(answer='3')
        q['answer_fields'][0]['correct_type'] = 'math'
        prep.question(plan, q, old, False)
        self.assertEqual(plan.local[('answer-field', str(old[':question/answer-fields'][0][':answer-field/id']))], 10)
        self.assertIn([10, kw('answer-field/correct'), 21], plan.assertions)
        self.assertFalse(any(row[1] == kw('answer-field/choices') for row in plan.retractions))

    def test_legacy_snapshot_without_fact_provenance_keeps_existing_behavior(self):
        data, old = attributed_snapshot()
        data.pop('facts')
        Preparation(data).check_source_attribution(old)

    def test_pipeline_protects_correction_preserves_original_capture_and_imports_sibling_then_noop(self):
        with tempfile.TemporaryDirectory() as directory:
            capture, config = database_tests.PipelineTests().setup(directory)
            client = FakeClient()
            client.idents[AGENT] = 950
            pipeline = DatabasePipeline(config, threading.Event(), client=client)
            self.assertEqual(pipeline.process(capture)['status'], 'verified')
            qid = next(eid for (eid, attr), values in client.facts.items()
                       if attr == 'question/math-academy-id' and any(value == 'q-11' for value, source in values))
            fid = client.facts[(qid, 'question/answer-fields')][0][0]
            client.facts[(qid, 'question/problem')] = [('Agent-corrected problem.', 950)]
            # Equal canonical-answer claims still preserve the agent's authorship.
            canonical = client.facts[(fid, 'answer-field/correct')][0][0]
            client.facts[(fid, 'answer-field/correct')].append((canonical, 950))
            protected = {(eid, attr): copy.deepcopy(values) for (eid, attr), values in client.facts.items()
                         if eid == qid or eid == fid or (eid, 'answer/id') in client.facts}
            content = json.loads((capture / 'content.json').read_text())
            original = copy.deepcopy(content['questions'][0])
            content['questions'][0]['knowledge_point'] = 'Title from protected question must not be planned'
            sibling = question('q-12')
            sibling['knowledge_point_id'] = original['knowledge_point_id']
            content['questions'].append(sibling)
            atomic_json(capture / 'content.json', content)
            result = pipeline.process(capture)
            self.assertEqual(result['status'], 'verified', result)
            self.assertEqual(len(result['omissions']), 1)
            self.assertEqual(result['omissions'][0]['constraint'], 'separately_attributed_correction')
            self.assertTrue(result['omissions'][0]['final'])
            self.assertTrue(all(client.facts[key] == values for key, values in protected.items()))
            self.assertEqual(json.loads((capture / 'content.json').read_text())['questions'][0], content['questions'][0])
            self.assertIn('q-12', {value for (eid, attr), values in client.facts.items()
                                  if attr == 'question/math-academy-id' for value, source in values})
            self.assertFalse(any(value == content['questions'][0]['knowledge_point']
                                 for (eid, attr), values in client.facts.items()
                                 if attr == 'knowledge-point/title' for value, source in values))
            self.assertEqual(pipeline.process(capture)['status'], 'no_changes')


if __name__ == '__main__':
    unittest.main()
