"""Offline replacement policies with documented authoring and saved MA DOM."""
import copy
import hashlib
import json
import tempfile
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from core import ROOT, build_transaction, build_content_transaction, atomic_json, stable_id
from database import Database
from edn import dumps, loads, kw
from import_repair import import_with_repair
from provenance import Reconciler, ReconciliationReview, authoring_records, source_records, value_hash

EVIDENCE = Path(__file__).parent/'fixtures/replacement-evidence'

class ReplacementTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.directory = Path(self.work.name)
        self.mid = 'q-5370'
        self.kp = uuid.UUID('1652eebf-b779-5f49-80cf-530bc3257006')
        authored = json.loads((EVIDENCE/'factorials-13831129/authored-worked-solutions.json').read_text())
        solution = next(q['worked_solution'] for q in authored['questions'] if q['math_academy_id'] == self.mid)
        self.answers = [{':db/id':i, ':answer/id':uuid.uuid4(), ':answer/type':{':db/ident':kw('answer.type/math')},
                         ':answer/value':v} for i,v in [(20,'120'),(21,'25'),(22,'24')]]
        self.field = {':db/id':10, ':answer-field/id':uuid.uuid4(), ':answer-field/key':'selection',
                      ':answer-field/type':{':db/ident':kw('answer-field.type/radio')},
                      ':answer-field/choices':self.answers, ':answer-field/correct':self.answers[0]}
        self.old = {':db/id':1, ':question/id':uuid.uuid4(), ':question/math-academy-id':self.mid,
                    ':question/problem':'Evaluate $5!$.', ':question/worked-solution':solution,
                    ':question/difficulty':{':db/id':99, ':db/ident':kw('question.difficulty/easy')},
                    ':question/answer-fields':[self.field], ':knowledge-point/_questions':[{':knowledge-point/id':self.kp}]}
        self.topic = {':topic/math-academy-id':774, ':topic/knowledge-points':[
            {':knowledge-point/id':self.kp, ':knowledge-point/title':'Evaluating Factorials',
             ':knowledge-point/questions':[{':question/math-academy-id':self.mid}]}]}
        self.q = {'math_academy_id':self.mid, 'knowledge_point_id':str(self.kp),
                  'problem':self.old[':question/problem'], 'worked_solution':solution, 'difficulty':'easy',
                  'answer_fields':[{'key':'selection','type':'radio','correct_value':'120',
                                    'choices':[{'type':'math','value':a[':answer/value']} for a in self.answers]}]}
        self.content = {'topic_id':774, 'questions':[self.q], 'canonical_examples':[]}
        self.authored = authoring_records(EVIDENCE, {self.mid})
        self.source = []
        self.reconciler = Reconciler(self.authored, self.source, 656, {self.mid:[]})

    def tearDown(self):
        self.work.cleanup()

    def evidence(self, attribute, value, category='ma_capture', key=None, local=False):
        record = dict(question=self.mid, field=key, attribute=attribute, value=value,
                      category=category, file='offline-fixture.json')
        (self.reconciler.authored if local else self.reconciler.sources).append(record)
        return record

    def plan(self):
        before = copy.deepcopy(self.old)
        result = build_transaction(self.content, self.topic, {self.mid:self.old}, self.reconciler)
        self.assertEqual(self.old, before)
        return result[0]

    def authentic_choices(self, values):
        f = self.q['answer_fields'][0]
        f['choices'] = [{'type':'math', 'value':v} for v in values]
        self.evidence('answer-field/choices', sorted(('math',v) for v in values), 'ma_complete_choices', 'selection')

    def test_duplicate_visible_choices_keep_capture_but_write_one_answer(self):
        self.authentic_choices(['120', '60', '60'])
        original = copy.deepcopy(self.q)
        tx = self.plan()
        created = [m for m in tx if isinstance(m, dict) and ':answer/value' in m]
        self.assertEqual([m[':answer/value'] for m in created], ['120', '60'])
        self.assertEqual(self.q, original)
        field = next(m for m in tx if isinstance(m, dict) and ':answer-field/choices' in m)
        self.assertEqual(len(field[':answer-field/choices']), 2)

    def test_missing_stored_correct_answer_is_filled(self):
        self.field.pop(':answer-field/correct')
        tx = self.plan()
        field = next(m for m in tx if isinstance(m, dict) and ':answer-field/correct' in m)
        self.assertEqual(field[':db/id'], 10)
        self.assertEqual(field[':answer-field/correct'], 20)
        self.assertFalse(self.reconciler.needs_review)

    def test_missing_historical_choices_and_correct_are_filled(self):
        for kind in ('blank', 'radio'):
            with self.subTest(kind=kind):
                self.field[':answer-field/type'][':db/ident'] = kw('answer-field.type/'+kind)
                self.field.pop(':answer-field/choices', None)
                self.field.pop(':answer-field/correct', None)
                incoming = self.q['answer_fields'][0]
                incoming.update(type=kind, choices=[{'type':'math', 'value':'120'}])
                tx = self.plan()
                created = [m for m in tx if isinstance(m, dict) and ':answer/value' in m]
                self.assertEqual([m[':answer/value'] for m in created], ['120'])
                field = next(m for m in tx if isinstance(m, dict) and ':answer-field/correct' in m)
                self.assertEqual(field[':db/id'], 10)
                self.assertEqual(field[':answer-field/correct'], created[0][':db/id'])
                self.assertEqual(field[':answer-field/choices'], [created[0][':db/id']])
                self.assertFalse(any(isinstance(m, list) and m[0] == kw('db/retract') for m in tx))
                self.assertFalse(self.reconciler.needs_review)

    def test_missing_choices_do_not_authorize_correct_answer_replacement(self):
        self.field.pop(':answer-field/choices')
        incoming = self.q['answer_fields'][0]
        incoming.update(type='blank', correct_value='121', choices=[{'type':'math', 'value':'121'}])
        self.field[':answer-field/type'][':db/ident'] = kw('answer-field.type/blank')
        self.assertEqual(self.plan(), [])
        self.assertTrue(self.reconciler.needs_review)
        self.assertTrue(any(d['attribute'] == 'answer-field/correct' for d in self.reconciler.decisions))

    def test_missing_choices_do_not_authorize_field_type_replacement(self):
        self.field.pop(':answer-field/choices')
        self.field.pop(':answer-field/correct')
        self.q['answer_fields'][0]['type'] = 'blank'
        self.assertEqual(self.plan(), [])
        self.assertTrue(self.reconciler.needs_review)
        self.assertTrue(any(d['attribute'] == 'answer-field/type' for d in self.reconciler.decisions))

    def test_missing_correct_with_new_source_choices_versions_field(self):
        self.field.pop(':answer-field/correct')
        self.authentic_choices(['120', '60'])
        tx = self.plan()
        self.assertIn([kw('db/retract'), 1, kw('question/answer-fields'), 10], tx)
        self.assertFalse(self.reconciler.needs_review)

    def test_documented_authored_solution_and_estimate_replaced_independently(self):
        self.q.update(worked_solution='By the definition, $5!=120$.', difficulty='hard')
        self.evidence('question/worked-solution', self.q['worked_solution'])
        self.evidence('question/difficulty', kw('question.difficulty/hard'))
        tx = self.plan()
        update = next(m for m in tx if ':question/worked-solution' in m)
        self.assertEqual(update[':question/worked-solution'], self.q['worked_solution'])
        self.assertEqual(update[':question/difficulty'], kw('question.difficulty/hard'))
        self.assertFalse(self.reconciler.needs_review)
        self.assertTrue(all(d['authoring'][0]['transaction'].endswith('transaction.edn') for d in self.reconciler.decisions))

    def test_missing_source_values_retain_authored_content_and_canonical_membership(self):
        self.old[':knowledge-point/_canonical-example'] = self.old.pop(':knowledge-point/_questions')
        point = self.topic[':topic/knowledge-points'][0]
        point[':knowledge-point/canonical-example'] = point.pop(':knowledge-point/questions')[0]
        self.content['canonical_examples'] = self.content.pop('questions')
        self.content['questions'] = []
        self.q.update(difficulty=None, answer_fields=[])
        self.q.pop('worked_solution')
        self.assertEqual(self.plan(), [])
        self.assertFalse(self.reconciler.needs_review)

    def test_partial_practice_content_does_not_erase_existing_values(self):
        self.q.update(difficulty=None, answer_fields=[])
        self.q.pop('worked_solution')
        self.assertEqual(self.plan(), [])

    def test_complete_choices_version_unused_field_and_keep_old_components(self):
        self.authentic_choices(['120','30','60'])
        for a in self.answers[1:]:
            self.evidence('answer/value', [kw('answer.type/math'),a[':answer/value']], 'local_authored', 'selection', True)
        tx = self.plan()
        self.assertEqual(tx[0], [kw('db/retract'),1,kw('question/answer-fields'),10])
        self.assertEqual(sorted(m[':answer/value'] for m in tx if isinstance(m,dict) and ':answer/value' in m), ['120','30','60'])
        self.assertFalse(any(isinstance(m,dict) and m[':db/id'] in (10,20,21,22) for m in tx))
        self.assertFalse(self.reconciler.needs_review)
        self.assertEqual(loads(dumps(tx)), tx)

    def test_observed_prompt_replaces_unknown_origin_without_calling_it_authored(self):
        self.authentic_choices(['120','25','60'])
        self.evidence('answer/value', [kw('answer.type/math'),'24'], 'local_authored','selection',True)
        self.q['problem'] = 'New MA wording for the same problem'
        self.evidence('question/problem', self.q['problem'])
        tx = self.plan()
        self.assertTrue(any(':question/problem' in m for m in tx if isinstance(m,dict)))
        self.assertFalse(self.reconciler.needs_review)
        decision=next(d for d in self.reconciler.decisions if d['attribute']=='question/problem')
        self.assertEqual(decision['authoring'],[])
        self.assertEqual(decision['category'],'ma_capture')

    def test_complete_observed_choices_replace_unknown_distractors(self):
        self.authentic_choices(['120','60'])
        self.assertTrue(self.plan())
        self.assertFalse(self.reconciler.needs_review)
        self.reconciler.decisions.clear()
        self.evidence('question/worked-solution', self.old[':question/worked-solution'], 'ma_capture', local=True)
        self.q['worked_solution'] = 'Different source solution'
        self.evidence('question/worked-solution', self.q['worked_solution'])
        self.plan()
        self.assertTrue(any(d['attribute']=='question/worked-solution' and d.get('action')=='replace'
                            for d in self.reconciler.decisions))
        self.assertTrue(any(d['attribute']=='answer/value' and d['category']=='ma_complete_choices'
                            for d in self.reconciler.decisions))

    def test_model_inference_cannot_replace_conflicting_key_but_grade_can(self):
        self.q['answer_fields'][0]['correct_value'] = '25'
        old = [kw('answer.type/math'),'120']; new = [kw('answer.type/math'),'25']
        self.evidence('answer-field/correct', old, 'local_interpretation','selection',True)
        r = self.evidence('answer-field/correct',new,'model_interpretation','selection')
        self.authentic_choices(['120','25','24'])
        self.assertEqual(self.plan(), [])
        self.assertTrue(self.reconciler.needs_review)
        self.reconciler.decisions.clear(); r['category'] = 'ma_successful_grade'
        self.assertTrue(self.plan())
        self.assertFalse(self.reconciler.needs_review)
        self.reconciler.decisions.clear()
        self.evidence('answer-field/correct',old,'ma_explicit_answer','selection',True)
        self.assertEqual(self.plan(),[])
        self.assertTrue(any('Contradiction' in d['reason'] for d in self.reconciler.decisions))

    def test_historically_referenced_fields_and_answers_survive_field_versioning(self):
        self.authentic_choices(['120','60'])
        for a in self.answers[1:]:
            self.evidence('answer/value', [kw('answer.type/math'),a[':answer/value']], 'local_authored','selection',True)
        for usage in ([{'kind':'presentations','entity':30}], [{'kind':'responses','entity':31}]):
            self.reconciler.usage[self.mid] = usage
            tx=self.plan()
            self.assertIn([kw('db/retract'),1,kw('question/answer-fields'),10],tx)
            self.assertFalse(any(isinstance(d,list) and d[0]==kw('db/retractEntity') for d in tx))
            self.assertFalse(any(isinstance(d,dict) and d.get(':db/id') in (10,20,21,22,30,31) for d in tx))
            self.assertFalse(self.reconciler.needs_review)
            self.assertTrue(any(d.get('historical_usage')==usage for d in self.reconciler.decisions))

    def test_incomplete_choices_only_merge_and_semantic_option_shuffling_is_noop(self):
        self.q['answer_fields'][0]['choices'] = [{'type':'math','value':'120'}]
        self.assertEqual(self.plan(), [])
        self.assertFalse(self.reconciler.needs_review)
        self.authentic_choices(['24','25','120.0'])
        self.q['answer_fields'][0]['correct_value'] = '120.0'
        self.assertEqual(self.plan(), [])
        self.assertFalse(self.reconciler.needs_review)

    def test_observed_solution_replaces_later_edit_with_exact_current_retraction(self):
        self.old[':question/worked-solution'] += '\nEdited later.'
        self.q['worked_solution'] = 'Recovered source solution'
        self.evidence('question/worked-solution',self.q['worked_solution'])
        tx=self.plan()
        guards=Database(SimpleNamespace()).replacement_guards(self.reconciler,{self.mid:self.old})
        self.assertIn([1,kw('question/worked-solution'),self.old[':question/worked-solution']],guards)
        self.assertTrue(any(isinstance(m,dict) and m.get(':question/worked-solution')==self.q['worked_solution'] for m in tx))
        self.assertFalse(self.reconciler.needs_review)

    def test_unknown_origin_metadata_requires_direct_source_evidence(self):
        self.reconciler.authored=[]
        for attr,new in [('question/problem','Updated MA problem'),
                         ('question/worked-solution','Updated MA solution'),
                         ('question/difficulty',kw('question.difficulty/hard'))]:
            self.reconciler.decisions.clear();self.reconciler.sources=[]
            self.assertFalse(self.reconciler.replace(self.mid,None,attr,'old',new,{'ma_capture'}))
            self.assertTrue(self.reconciler.needs_review)
            self.reconciler.decisions.clear()
            self.evidence(attr,new,'model_interpretation')
            self.assertFalse(self.reconciler.replace(self.mid,None,attr,'old',new,{'ma_capture'}))
            self.reconciler.sources=[];self.reconciler.decisions.clear()
            self.evidence(attr,new)
            self.assertTrue(self.reconciler.replace(self.mid,None,attr,'old',new,{'ma_capture'}))
            self.assertFalse(self.reconciler.needs_review)

    def test_field_type_conflict_versions_only_documented_unused_type(self):
        self.q['answer_fields'][0]['type'] = 'select'
        self.evidence('answer-field/type',kw('answer-field.type/radio'),'local_reconstruction','selection',True)
        self.evidence('answer-field/type',kw('answer-field.type/select'),'ma_widget','selection')
        self.authentic_choices(['120','25','24'])
        tx = self.plan()
        self.assertTrue(any(isinstance(m,dict) and m.get(':answer-field/type') == ':answer-field.type/select' for m in tx))

    def test_protected_facts_and_only_exact_retractions_allowed(self):
        db = Database(SimpleNamespace())
        attrs = [(1,kw('question/problem')),(2,kw('task-item/responses')),(3,kw('answer/value')),(4,kw('engine/settings'))]
        receipt = {':edb/tx-data':[[10,1,'old',100,False],[10,1,'new',100,True]]}
        db.validate_datoms(receipt,attrs,[[10,kw('question/problem'),'old']])
        for row in ([11,1,'old',100,False],[10,2,20,100,True],[20,3,'changed',100,True],[30,4,'changed',100,True]):
            with self.assertRaises(ValueError):
                db.validate_datoms({':edb/tx-data':[row]},attrs,[[10,kw('question/problem'),'old']], [20])
        db.query = Mock(return_value=[])
        db.protected(attrs,self.directory,'protected',656)
        self.assertEqual([call.args[1] for call in db.query.call_args_list], [[2],[4]])

    def test_pending_intent_keeps_exact_transaction_and_evidence(self):
        db = Database(SimpleNamespace(database='test', endpoint='socket'))
        tx = self.directory/'transaction.edn'; tx.write_text('[{:db/id 1 :question/problem "new"}]\n')
        evidence = self.directory/'reconciliation.edn'; evidence.write_text('{}\n')
        intent = {'database':'test','endpoint':'socket','basis':656,'request_key':'stable',
                  'sha256':hashlib.sha256(tx.read_bytes()).hexdigest(),
                  'content_sha256':hashlib.sha256(json.dumps(self.content,sort_keys=True,default=str).encode()).hexdigest(),
                  'reconciliation_sha256':hashlib.sha256(evidence.read_bytes()).hexdigest()}
        atomic_json(self.directory/'commit-intent.json',intent)
        original = {p.name:p.read_bytes() for p in self.directory.iterdir()}
        db.reconciliation = Mock(side_effect=AssertionError('Must not replan'))
        self.assertEqual(db.import_content(self.content,self.directory,False),intent)
        changed = copy.deepcopy(self.content); changed['questions'][0]['worked_solution'] = 'altered'
        with self.assertRaisesRegex(ValueError,'original captured content'):
            db.import_content(changed,self.directory,False)
        self.assertEqual(original,{p.name:p.read_bytes() for p in self.directory.iterdir()})
        evidence.write_text('{"changed" true}')
        with self.assertRaisesRegex(ValueError,'original intent'):
            db.import_content(self.content,self.directory,False)

    def test_reconciliation_notation_error_can_invoke_comparison_repair(self):
        db = Mock(); db.import_content.side_effect = ReconciliationReview('Needs provenance')
        with patch('import_repair.repair',return_value=False) as repair, self.assertRaises(ReconciliationReview):
            import_with_repair(db,self.content,self.directory,{'activity_complete':True,'history_complete':True},
                               SimpleNamespace(preview=True,no_import_repair=False))
        repair.assert_called_once()

    def test_legacy_single_radio_key_versions_instead_of_mutating_old_key(self):
        for key in ('answer','y'):
            with self.subTest(key=key):
                self.setUp_radio_rename(key)

    def setUp_radio_rename(self, key):
        self.field[':answer-field/key']=key
        self.authentic_choices(['120','30','60'])
        self.evidence('answer-field/type',kw('answer-field.type/radio'),'ma_widget','selection')
        tx=self.plan()
        self.assertIn([kw('db/retract'),1,kw('question/answer-fields'),10],tx)
        self.assertEqual(self.field[':answer-field/key'],key)
        self.assertFalse(self.reconciler.needs_review)
        guards=Database(SimpleNamespace()).replacement_guards(self.reconciler,{self.mid:self.old})
        self.assertIn([1,kw('question/answer-fields'),10],guards)

    def test_radio_rename_still_requires_observed_widget_and_complete_choices(self):
        self.field[':answer-field/key']='y'
        self.assertEqual(self.plan(),[])
        self.assertTrue(self.reconciler.needs_review)
        self.assertEqual(self.field[':answer-field/key'],'y')

    def test_radio_rename_does_not_collapse_multiple_existing_fields(self):
        self.field[':answer-field/key']='y'
        self.old[':question/answer-fields'].append({**self.field, ':answer-field/key':'x', ':db/id':11})
        with self.assertRaisesRegex(ValueError,'omitted existing fields'):
            self.plan()

    def test_saved_real_capture_grade_and_complete_dom_not_model_labels(self):
        capture = EVIDENCE/'capture-13934288'
        content = json.loads((capture/'content.json').read_text())
        records = source_records(content,capture)
        self.assertTrue(any(r['category']=='ma_complete_choices' for r in records))
        self.assertTrue(any(r['category']=='ma_successful_grade' for r in records))
        self.assertTrue(any(r['category']=='model_interpretation' for r in records))
        state = json.loads((capture/'state.json').read_text())
        q = content['questions'][0]; mid = q['math_academy_id']
        state['questions'][mid]['before']['fields'][0]['choices_complete'] = False
        atomic_json(self.directory/'state.json',state)
        atomic_json(self.directory/'activity-metadata.json',json.loads((capture/'activity-metadata.json').read_text()))
        self.assertFalse(any(r['question']==mid and r['category']=='ma_complete_choices' for r in source_records(content,self.directory)))

    def test_replaced_scalar_and_versioned_field_reimport_are_noops(self):
        self.authentic_choices(['120','30','60'])
        for a in self.answers[1:]:
            self.evidence('answer/value',[kw('answer.type/math'),a[':answer/value']],'local_authored','selection',True)
        self.q.update(worked_solution='Captured factorial solution',difficulty='moderate')
        self.evidence('question/worked-solution',self.q['worked_solution'])
        self.evidence('question/difficulty',kw('question.difficulty/moderate'))
        self.assertTrue(self.plan())
        after = copy.deepcopy(self.old)
        after[':question/worked-solution'] = self.q['worked_solution']
        after[':question/difficulty'] = {':db/id':100, ':db/ident':kw('question.difficulty/moderate')}
        field = after[':question/answer-fields'][0]
        field[':db/id'] = 50
        field[':answer-field/choices'] = [
            {':db/id':i, ':answer/type':{':db/ident':kw('answer.type/math')}, ':answer/value':v}
            for i,v in [(51,'120'),(52,'30'),(53,'60')]]
        field[':answer-field/correct'] = field[':answer-field/choices'][0]
        # Old entities still exist independently; changing ownership does not
        # permit changing their values or old response references.
        self.assertEqual(self.old[':question/answer-fields'][0][':db/id'],10)
        self.assertEqual([a[':answer/value'] for a in self.answers],['120','25','24'])
        again = Reconciler(self.reconciler.authored,self.reconciler.sources,657,{self.mid:[]})
        tx,_ = build_content_transaction(self.content,{774:self.topic},{self.mid:after},again)
        self.assertEqual(tx,[])
        self.assertFalse(again.needs_review)

    def test_database_basis_readback_attests_only_matching_component_identity(self):
        db = Database(SimpleNamespace())
        record = self.evidence('answer-field/type',kw('answer-field.type/radio'),'local_authored','selection',True)
        record = {**record,'basis':303}
        historical = copy.deepcopy(self.old)
        db.questions = Mock(return_value={self.mid:historical})
        db.query = Mock(return_value=[])
        with patch('database.authoring_records',return_value=[record]), patch('database.source_records',return_value=[]), patch('database.ROOT',self.directory):
            reconciler = db.reconciliation(self.content,self.directory,{self.mid:self.old},656)
            self.assertEqual(reconciler.authored,[record])
            historical[':question/answer-fields'][0][':db/id'] = 888
            reconciler = db.reconciliation(self.content,self.directory,{self.mid:self.old},656)
            self.assertEqual(reconciler.authored,[])
        historical_calls = [c for c in db.query.call_args_list if c.args[3].startswith('historical-')]
        self.assertTrue(historical_calls)
        self.assertTrue(all(c.kwargs.get('history') is True for c in historical_calls))
        self.assertTrue(all(c.args[4] == 656 for c in db.query.call_args_list))

    def test_verified_other_worker_capture_is_authoritative_evidence(self):
        other=self.directory/'other-worker-captures'
        capture=other/'123'
        atomic_json(capture/'content.json',self.content)
        atomic_json(capture/'edb-import/verification.json',{'committed':True,'basis_after':303})
        # Unverified content from another worker must not become an attestation.
        atomic_json(other/'124/content.json',self.content)
        record={'question':self.mid,'field':None,'attribute':'question/worked-solution',
                'value':self.old[':question/worked-solution'],'category':'ma_capture','file':'saved.json'}
        db=Database(SimpleNamespace(capture_root=[other,other],output=other))
        db.questions=Mock(return_value={self.mid:self.old});db.query=Mock(return_value=[])
        def records(content,directory):
            return [record] if directory==capture else []
        with patch('database.ROOT',self.directory),patch('database.authoring_records',return_value=[]), \
             patch('database.source_records',side_effect=records) as sources:
            reconciler=db.reconciliation(self.content,self.directory,{self.mid:self.old},656)
        self.assertEqual(len(reconciler.authored),1)
        self.assertEqual(reconciler.authored[0]['basis'],303)
        self.assertEqual(reconciler.authored[0]['verification'],str(capture/'edb-import/verification.json'))
        self.assertEqual([c.args[1] for c in sources.call_args_list],[capture,self.directory.parent])

    def test_explicit_historical_correction_is_authoritative_not_an_invented_key(self):
        records = authoring_records(EVIDENCE,{'q-23188'})
        repaired = [r for r in records if r['basis']==653 and r['attribute']=='answer-field/correct']
        self.assertEqual([r['category'] for r in repaired],['ma_explicit_answer'])

    def test_image_identity_uses_bytes_and_preserves_missing_source_feedback(self):
        one = self.directory/'first.png'; two = self.directory/'shuffled-option.png'
        pixels = (ROOT/'reference/mathacademy/review-13925710/assets/q-28197-a-1.png').read_bytes()
        one.write_bytes(pixels); two.write_bytes(pixels)
        for a in self.answers:
            a[':answer/type'][':db/ident'] = kw('answer.type/image')
            a[':answer/value'] = str(one) if a[':db/id']==20 else str(a[':db/id'])
        self.q['answer_fields'][0].update(correct_value=str(two),choices=[{'type':'image','value':str(two)}])
        # No completeness assertion: missing alternatives cannot remove values.
        self.assertEqual(self.plan(),[])
        self.answers[0][':answer/type'][':db/ident'] = kw('answer.type/math')
        self.answers[0][':answer/value'] = '120'
        self.answers[0][':answer/feedback'] = 'Retained authored feedback'
        for a in self.answers[1:]:
            a[':answer/type'][':db/ident'] = kw('answer.type/math')
            self.evidence('answer/value',[kw('answer.type/math'),a[':answer/value']],'local_authored','selection',True)
        self.q['answer_fields'][0]['correct_value'] = '120'
        self.authentic_choices(['120','30','60'])
        tx = self.plan()
        answer = next(m for m in tx if isinstance(m,dict) and m.get(':answer/value') == '120')
        self.assertEqual(answer[':answer/feedback'],'Retained authored feedback')

    def test_post_commit_verification_uses_frozen_evidence_and_checks_reimport(self):
        self.q['worked_solution'] = 'Recovered solution'
        self.evidence('question/worked-solution',self.q['worked_solution'])
        self.plan()
        db = Database(SimpleNamespace(database='test'))
        after = copy.deepcopy(self.old); after[':question/worked-solution'] = self.q['worked_solution']
        frozen = {'authored':self.reconciler.authored,'sources':self.reconciler.sources,'usage':{self.mid:[]},
                  'retractions':[[1,kw('question/worked-solution'),self.old[':question/worked-solution']]],
                  'immutable_answers':[20,21,22]}
        (self.directory/'reconciliation.edn').write_text(dumps(frozen))
        atomic_json(self.directory/'commit-intent.json',{'basis':656,'reconciliation_sha256':'saved-hash'})
        atomic_json(self.directory/'replacement-report.json',{'decisions':self.reconciler.decisions})
        db.attributes = Mock(return_value=[(5,kw('question/worked-solution'))])
        db.protected = Mock(side_effect=AssertionError('Do not scan the database during an import'))
        db.content_topics = Mock(return_value={774:self.topic})
        db.questions = Mock(return_value={self.mid:after})
        receipt = {':edb/db-before-t':656,':edb/db-after-t':657,':edb/tx-data':[
            [1,5,self.old[':question/worked-solution'],999,False],[1,5,self.q['worked_solution'],999,True]]}
        result = db._verify(receipt,self.content,self.directory)
        self.assertTrue(result['reimport_is_noop'])
        self.assertTrue(result['learner_and_engine_facts_unchanged'])
        self.assertEqual(result['verification_method'],'committed_transaction_and_content')
        self.assertNotIn('protected_fact_count',result)
        self.assertNotIn('protected_facts_sha256',result)
        db.protected.assert_not_called()
        db.attributes.assert_called_once_with(self.directory,656)
        db.questions.assert_called_once()
        report = json.loads((self.directory/'replacement-report.json').read_text())
        self.assertTrue(report['committed'])
        self.assertTrue(all(d['transaction_receipt'].endswith('commit.edn') for d in report['decisions']))

    def test_no_history_and_existing_field_definitions_block_unsafe_replacement(self):
        self.q['worked_solution'] = 'Recovered solution'
        self.evidence('question/worked-solution',self.q['worked_solution'])
        self.reconciler.no_history.add(kw('question/worked-solution'))
        self.assertEqual(self.plan(),[])
        self.assertTrue(any('db/noHistory' in d['reason'] for d in self.reconciler.decisions))
        db = Database(SimpleNamespace())
        with self.assertRaisesRegex(ValueError,'preexisting field'):
            db.validate_datoms({':edb/tx-data':[[10,5,88,100,True]]},[(5,kw('answer-field/correct'))],
                               immutable_fields=[[10,kw('answer-field/correct')]])

    def test_fast_post_commit_verification_rejects_learner_effects(self):
        db = Database(SimpleNamespace())
        db.attributes = Mock(return_value=[(5,kw('question/problem')),(6,kw('learner/name'))])
        db.protected = Mock(side_effect=AssertionError('Do not scan the database'))
        db.questions = Mock()
        for added in (True,False):
            receipt = {':edb/db-before-t':656,':edb/db-after-t':657,
                       ':edb/tx-data':[[30,6,'Changed learner',999,added]]}
            with self.assertRaisesRegex(ValueError,'non-content attribute'):
                db._verify(receipt,self.content,self.directory)
        db.protected.assert_not_called()
        db.questions.assert_not_called()


if __name__ == '__main__':
    unittest.main()
