"""Real q-222851 source: an unchanged field key now names another component."""
import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from core import atomic_json, build_transaction, stable_id
from database import Database
from edn import kw, loads, dumps
from provenance import Reconciler, question_layout, source_records, value_hash

FIXTURE=Path(__file__).parent/'fixtures/normal-field-layout'

class FieldLayoutTests(unittest.TestCase):
    def setUp(self):
        self.work=tempfile.TemporaryDirectory();self.addCleanup(self.work.cleanup)
        self.directory=Path(self.work.name)
        for path in FIXTURE.iterdir():shutil.copy2(path,self.directory/path.name)
        self.content=json.loads((self.directory/'content.json').read_text())
        self.q=self.content['questions'][0];self.mid=self.q['math_academy_id']
        self.old=loads((self.directory/'previous-question.edn').read_text())[0][0]
        self.topic={':topic/math-academy-id':self.content['topic_id'],':topic/knowledge-points':[
            {':knowledge-point/id':self.old[':knowledge-point/_questions'][0][':knowledge-point/id'],
             ':knowledge-point/title':self.q['knowledge_point'],
             ':knowledge-point/questions':[{':question/math-academy-id':self.mid}]}]}
        self.state=json.loads((self.directory/'state.json').read_text())
        self.review={'question':self.mid,'confident':True,'rationale':'The complete live DOM asks only for N_y; all three old blank roles belong to the original full-vector prompt.',
            'bindings':{'problem':value_hash(self.q['problem']),'worked_solution':value_hash(self.q['worked_solution']),
                        'fields':value_hash(self.q['answer_fields']),'raw_before':value_hash(self.state['questions'][self.mid]['before'])},
            'previous_readback':'previous-question.edn','previous_layout_sha256':value_hash(question_layout(self.old)),
            'evidence_files':[{'path':'previous-question.edn','sha256':hashlib.sha256((self.directory/'previous-question.edn').read_bytes()).hexdigest()}]}
        self.write_review()

    def write_review(self):atomic_json(self.directory/'field-layout-source-reviews.json',{'reviews':[self.review]})

    def plan(self, usage=None, no_history=(), authored=()):
        self.reconciler=Reconciler(authored,source_records(self.content,self.directory),2308,
            {self.mid:[]} if usage is None else usage,no_history)
        before=copy.deepcopy(self.old);content=copy.deepcopy(self.content)
        tx,_=build_transaction(self.content,self.topic,{self.mid:self.old},self.reconciler)
        self.assertEqual(self.old,before);self.assertEqual(self.content,content)
        return tx

    def test_review_versions_entire_ownership_without_role_or_value_reuse(self):
        tx=self.plan()
        old_ids={f[':db/id'] for f in self.old[':question/answer-fields']}
        removed={m[3] for m in tx if isinstance(m,list) and m[2]==kw('question/answer-fields')}
        self.assertEqual(removed,old_ids)
        fields=[m for m in tx if isinstance(m,dict) and ':answer-field/id' in m]
        self.assertEqual(len(fields),1)
        self.assertIn('/ma-layout-v1/',fields[0][':db/id'])
        self.assertNotIn(fields[0][':answer-field/id'],{f[':answer-field/id'] for f in self.old[':question/answer-fields']})
        self.assertEqual(fields[0][':answer-field/key'],'field-1')
        self.assertEqual([m[':answer/value'] for m in tx if isinstance(m,dict) and ':answer/value' in m],['-\\sin(t)'])
        self.assertFalse(any(isinstance(m,dict) and isinstance(m[':db/id'],int) and m[':db/id'] in old_ids for m in tx))
        self.assertFalse(self.reconciler.needs_review)
        guards=Database(SimpleNamespace()).replacement_guards(self.reconciler,{self.mid:self.old})
        self.assertEqual({g[2] for g in guards if g[1]==kw('question/answer-fields')},old_ids)

    def test_previous_role_values_are_retained_only_on_original_components(self):
        f=self.old[':question/answer-fields'][0]
        a={':db/id':888,':answer/id':stable_id('answer','old-first-component'),
           ':answer/type':{':db/ident':kw('answer.type/math')},':answer/value':'-\\cos(t)'}
        f[':answer-field/choices']=[a];f[':answer-field/correct']=a
        (self.directory/'previous-question.edn').write_text(dumps([[self.old]])+'\n')
        self.review['previous_layout_sha256']=value_hash(question_layout(self.old))
        self.review['evidence_files'][0]['sha256']=hashlib.sha256((self.directory/'previous-question.edn').read_bytes()).hexdigest()
        self.write_review();tx=self.plan()
        self.assertEqual([m[':answer/value'] for m in tx if isinstance(m,dict) and ':answer/value' in m],['-\\sin(t)'])
        self.assertEqual(f[':answer-field/correct'][':answer/value'],'-\\cos(t)')
        self.assertFalse(any(isinstance(m,dict) and m[':db/id']==888 for m in tx))

    def test_no_explicit_review_still_rejects_omitted_fields(self):
        (self.directory/'field-layout-source-reviews.json').unlink()
        with self.assertRaisesRegex(ValueError,'omitted existing fields'):self.plan()

    def test_existing_layout_or_component_mutation_invalidates_review(self):
        for attr in (':answer-field/key',':answer-field/id',':db/id'):
            with self.subTest(attr=attr):
                before=copy.deepcopy(self.old)
                self.old[':question/answer-fields'][0][attr]='changed'
                with self.assertRaisesRegex(ValueError,'omitted existing fields'):self.plan()
                self.old=before

    def test_raw_widget_and_solution_mutations_invalidate_review(self):
        for mutation in ('widget','solution','grade','readback','missing_widget'):
            with self.subTest(mutation=mutation):
                original=copy.deepcopy(self.state);original_content=copy.deepcopy(self.content)
                old_bytes=(self.directory/'previous-question.edn').read_bytes()
                if mutation=='widget':self.state['questions'][self.mid]['before']['fields'][0]['dom_id']='changed'
                if mutation=='solution':self.q['worked_solution']='Changed explanation'
                if mutation=='grade':self.state['questions'][self.mid]['actual_result']='Incorrect';self.state['questions'][self.mid]['after']['result']='Incorrect'
                if mutation=='readback':(self.directory/'previous-question.edn').write_bytes(old_bytes+b'\n')
                if mutation=='missing_widget':self.state['questions'][self.mid]['before']['fields']=[]
                atomic_json(self.directory/'state.json',self.state)
                with self.assertRaisesRegex(ValueError,'omitted existing fields'):self.plan()
                self.state=original;self.content=original_content;self.q=self.content['questions'][0]
                atomic_json(self.directory/'state.json',self.state)
                (self.directory/'previous-question.edn').write_bytes(old_bytes)

    def test_new_field_content_and_unrelated_question_cannot_reuse_review(self):
        original=copy.deepcopy(self.content)
        self.q['answer_fields'][0]['correct_value']='\\sin(t)'
        self.q['answer_fields'][0]['choices'][0]['value']='\\sin(t)'
        with self.assertRaisesRegex(ValueError,'omitted existing fields'):self.plan()
        self.content=original;self.q=self.content['questions'][0]
        self.review['question']='q-999999';self.write_review()
        with self.assertRaisesRegex(ValueError,'omitted existing fields'):self.plan()

    def test_genuine_layout_review_changes_both_retry_fingerprints_once(self):
        from import_repair import repair_generation
        from saved_imports import retry_key
        atomic_json(self.directory/'content.json',self.content)
        args=SimpleNamespace(preview=False,database='fixture',endpoint='/tmp/fixture.sock')
        fingerprints=lambda:(repair_generation(self.directory),retry_key(self.directory,self.state,'fixed-source',args))
        (self.directory/'field-layout-source-reviews.json').unlink();before=fingerprints()
        self.write_review();after=fingerprints()
        self.assertNotEqual(before[0],after[0]);self.assertNotEqual(before[1],after[1])
        self.assertEqual(after,fingerprints())
        self.review['reviewed_at']='later timestamp'
        self.review['rationale']='Same source-based judgment, rewritten prose.'
        shutil.copy2(self.directory/'previous-question.edn',self.directory/'renamed-readback.edn')
        self.review['previous_readback']='renamed-readback.edn'
        self.review['evidence_files'][0]['path']='renamed-readback.edn'
        self.write_review();self.assertEqual(after,fingerprints())

    def test_include_reviews_false_excludes_layout_reviews(self):
        self.assertTrue(any(r['category']=='reviewed_ma_field_layout' for r in source_records(self.content,self.directory)))
        self.assertFalse(any(r['category']=='reviewed_ma_field_layout' for r in source_records(self.content,self.directory,include_reviews=False)))

    def test_history_retention_and_corrections_remain_guarded(self):
        for options in ({'usage':{}},{'usage':{self.mid:[{'kind':'presentations','entity':123}]}},
                        {'no_history':[kw('question/answer-fields')]},
                        {'authored':[{'question':self.mid,'category':'mathematical_correction','field':None,'attribute':'question/problem','value':self.old[':question/problem']}]}):
            with self.subTest(options=options),self.assertRaisesRegex(ValueError,'omitted existing fields'):self.plan(**options)

    def test_stale_full_vector_capture_cannot_reattach_three_fields(self):
        original_problem=self.old[':question/problem']
        self.test_layout_version_reimport_is_noop()
        installed=copy.deepcopy(self.old)
        self.q['problem']=original_problem
        self.q['answer_fields']=[{'key':'field-'+str(i),'type':'blank','choices':[{'type':'math','value':value}],
                                 'correct_value':value} for i,value in enumerate(('-\\cos(t)','-\\sin(t)','0'),1)]
        sources=[dict(question=self.mid,field=None,attribute='question/problem',value=original_problem,category='ma_capture')]
        sources += [dict(question=self.mid,field=f['key'],attribute='answer-field/correct',
                         value=[kw('answer.type/math'),f['correct_value']],category='ma_successful_grade') for f in self.q['answer_fields']]
        reconciler=Reconciler([],sources,2313,{self.mid:[]})
        build_transaction(self.content,self.topic,{self.mid:self.old},reconciler)
        self.assertTrue(reconciler.needs_review)
        self.assertTrue(any(d['attribute']=='answer-field/correct' and d['category']=='review_required' for d in reconciler.decisions))
        self.assertEqual(self.old,installed)

    def test_layout_version_reimport_is_noop(self):
        tx=self.plan()
        fields=[m for m in tx if isinstance(m,dict) and ':answer-field/id' in m]
        answers={m[':db/id']:m for m in tx if isinstance(m,dict) and ':answer/id' in m}
        def answer(token):
            a=copy.deepcopy(answers[token]);a[':answer/type']={':db/ident':a[':answer/type']};return a
        for f in fields:
            f[':answer-field/type']={':db/ident':f[':answer-field/type']}
            f[':answer-field/choices']=[answer(a) for a in f[':answer-field/choices']]
            f[':answer-field/correct']=answer(f[':answer-field/correct'])
        self.old[':question/answer-fields']=fields
        self.old[':question/problem']=self.q['problem'];self.old[':question/worked-solution']=self.q['worked_solution']
        self.old[':question/difficulty']={':db/ident':kw('question.difficulty/'+self.q['difficulty'])}
        self.assertEqual(self.plan(),[])

if __name__=='__main__':unittest.main()
