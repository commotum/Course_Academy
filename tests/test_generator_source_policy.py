import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from generator_source_policy import filter_material, source_references, reject_excluded_sources


class SourcePolicyTests(unittest.TestCase):
    def setUp(self):
        self.bad={':db/id':2,':question/id':'bad-uuid',':question/math-academy-id':'q-167637'}
        self.good={':db/id':3,':question/id':'good-uuid',':question/math-academy-id':'q-1853'}

    def test_excluded_payload_cannot_leak_through_lesson_or_prerequisite_examples(self):
        material={'kp':{':knowledge-point/questions':[self.bad,self.good]},
                  'lessons':[{'example':self.bad}], 'prerequisites':[{'example':self.bad}]}
        original=copy.deepcopy(material)
        result=filter_material(material,[self.bad])
        self.assertEqual(result['kp'][':knowledge-point/questions'],[self.good])
        self.assertNotIn('example',result['lessons'][0])
        self.assertNotIn('example',result['prerequisites'][0])
        self.assertEqual(result['source_eligibility']['excluded_questions'],[self.bad])
        self.assertEqual(material,original)

    def test_all_declared_identity_forms_and_template_fallback_are_checked(self):
        for generation in [{'source_ids':['q-167637']},{'source_id':2},
                           {'source_ids':['bad-uuid']},{'template':'q-167637'}]:
            with self.subTest(generation=generation),self.assertRaisesRegex(ValueError,'excluded standalone source'):
                reject_excluded_sources([{'generation':generation}],[self.bad])

    def test_source_basis_seed_and_lineage_are_not_question_references(self):
        record={'generation':{'source':{'database':'math','basis':2,'lineage':'bad-uuid'},'seed':2,
                              'source_ids':['q-1853']}}
        self.assertEqual(source_references(record),{'q-1853'})
        reject_excluded_sources([record],[self.bad])


if __name__=='__main__':unittest.main()
