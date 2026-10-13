import copy
import unittest

from scripts.database.edn import kw, dumps
from scripts.database.evidence import authoritative_question
from scripts.database.prepare import Preparation
from scripts.tests.test_database import question
from scripts.tests.test_source_protected_revision import attributed_snapshot


class ExistingSourceAnswerTests(unittest.TestCase):
    def fixture(self):
        data, old = attributed_snapshot()
        data['lineage']='database-lineage'
        q=question(); q['problem']=old[':question/problem']
        q['worked_solution']='$1+1=9$'
        field=q['answer_fields'][0]
        field.update(type='radio',choices=[{'type':'math','value':'2'}, {'type':'math','value':'3'}],
            correct_value='9',evidence={'kind':'worked_solution','value':'9','source_file':'history.html',
                                      'solution_quote':'$1+1=9$','matches_worked_solution':True})
        old[':question/answer-fields'][0][':answer-field/type'][':db/ident']=kw('answer-field.type/radio')
        data['idents']=[(eid,kw('answer-field.type/radio') if eid==901 else ident) for eid,ident in data['idents']]
        judgment={'status':'source_error','answers':[{'key':'x','value_type':'math','correct_value':'2',
            'ma_value':'9','ma_basis':'worked_solution','ma_evidence':'$1+1=9$','disagrees':True}]}
        return data,q,judgment

    def test_existing_owned_ma_key_repairs_binding_without_changing_original_solution(self):
        data,q,j=self.fixture();proofs=[]
        p=Preparation(data,record_source_evidence=lambda proof:proofs.append(proof) or '/source-proof.edn')
        result=p.existing_ma_answer(q,j)
        self.assertEqual(result['worked_solution'],'$1+1=9$')
        self.assertEqual(result['answer_fields'][0]['correct_value'],'2')
        self.assertEqual(result['answer_fields'][0]['evidence']['source_kind'],'existing_edb_math_academy_answer')
        self.assertEqual(authoritative_question(result)['answer_fields'][0]['correct_value'],'2')
        self.assertEqual(j['answers'][0]['ma_value'],'9')
        self.assertEqual(proofs[0]['basis'],1)
        self.assertEqual(proofs[0]['lineage'],'database-lineage')

    def test_changed_problem_bank_guess_and_foreign_provenance_cannot_be_promoted(self):
        for mutation in ('problem','bank','guess','foreign','value_source','lineage'):
            with self.subTest(mutation=mutation):
                data,q,j=self.fixture()
                if mutation=='problem':q['problem']='Different mathematical problem'
                if mutation=='bank':q['answer_fields'][0]['choices'][1]['value']='4'
                if mutation=='guess':j['answers'][0]['correct_value']='3'
                if mutation=='lineage':data.pop('lineage')
                if mutation in ('foreign','value_source'):
                    target=[10,'answer-field/correct'] if mutation=='foreign' else [20,'answer/value']
                    next(row for row in data['facts'] if row[:2]==target)[3]=950
                proof=[]
                result=Preparation(data,record_source_evidence=lambda p:proof.append(p) or '/proof').existing_ma_answer(q,j)
                self.assertIsNone(result)
                self.assertEqual(proof,[])

    def test_gray_legacy_placeholder_is_only_allowed_presentation_difference(self):
        data,q,j=self.fixture()
        q['problem'] += r'\bbox[2pt,lightgray]{\phantom{a}}'
        p=Preparation(data,record_source_evidence=lambda p:'/proof')
        self.assertIsNotNone(p.existing_ma_answer(q,j))
        q['problem'] += '$2$'
        self.assertIsNone(p.existing_ma_answer(q,j))

    def test_preparation_restores_activity_and_saves_corroboration(self):
        data,q,j=self.fixture()
        q['knowledge_point_id']=str(data['entities'][1][':knowledge-point/id'])
        p=Preparation(data,resolve=lambda *a:j,record_source_evidence=lambda p:'/proof')
        result=p.prepare({'task_id':'77','kind':'review','topic_id':1,'questions':[q],'question_order':['q-11']})
        self.assertEqual(result['omissions'],[])
        self.assertEqual(len(result['source_repairs']),1)
        self.assertEqual(result['source_repairs'][0]['judgment']['answers'][0]['ma_value'],'9')
        self.assertTrue(any(a[1]==':step/content' and a[2]==5 for b in result['batches'] for a in b['assertions']))
