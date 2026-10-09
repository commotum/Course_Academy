"""Attested containment interpretation: real source, strict scope, restart safety."""
import copy,hashlib,json,tempfile,unittest,uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from core import atomic_json,ROOT as REPOSITORY
from browser import CaptureBrowser
from solver import Solver
from source_interpretation import reviewed_containment,unresolved_study_clarifications,KP,TOPIC

EVIDENCE=REPOSITORY/'reference/mathacademy/question-capture-workers/multivariable/14050897'
CORRECTION=REPOSITORY/'reference/mathacademy/mathematical-corrections/e-6996'

class ContainmentTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.activity=self.root/'capture';self.directory=self.activity/'q-80266'
        self.directory.mkdir(parents=True)
        self.item=json.loads((EVIDENCE/'q-80266-before.json').read_text())
        self.state={'task_id':99,'task_type':'lesson','topic_id':TOPIC,'current_kp':KP,'examples':{},'questions':{}}
        atomic_json(self.activity/'state.json',self.state)
        correction=self.root/'reference/mathacademy/mathematical-corrections/e-6996';correction.mkdir(parents=True)
        for name in ('review.json','verification.json','transaction.edn'):(correction/name).write_bytes((CORRECTION/name).read_bytes())
        self.correction=correction
        self.scope=patch('source_interpretation.ROOT',self.root);self.scope.start();self.addCleanup(self.scope.stop)
        self.args=SimpleNamespace(solver_command=None,solver_timeout=5)
        self.calls=[]
    def meta(self,item=None,state=None):return reviewed_containment(item or self.item,state or self.state,self.directory)
    def test_actual_literal_contradiction_is_resolved_by_explicit_requirement(self):
        original=json.loads((EVIDENCE/'q-80266/solve-answer.json').read_text())
        self.assertEqual(original['answers'][0]['correct_value'],'I, II, and III')
        self.assertTrue(original['confident'])
        metadata=self.meta();self.assertEqual(metadata['requirement'],r'D\subseteq R')
        self.assertEqual(metadata['source_problem'],self.item['problem'])
        self.assertIn(r'Require $D\subseteq R$',metadata['interpreted_problem'])
        self.assertEqual(metadata['committed_basis'],json.loads((CORRECTION/'verification.json').read_text())['basis_after'])
        rectangles=[(-2,2,-1,1),(-1,1,-2,2),(-2,2,-2,2)]
        self.assertEqual([a<=-1 and b>=1 and c<=-2 and d>=2 for a,b,c,d in rectangles],[False,True,True])
    def test_other_topic_kp_forms_and_widgets_are_untouched(self):
        for state in ({**self.state,'topic_id':1992},{**self.state,'current_kp':'other'}):self.assertIsNone(self.meta(state=state))
        for item in ({**self.item,'problem':self.item['problem'].replace('R\\cap D','D')},
                     {**self.item,'problem':'Which equalities are true?'},
                     {**self.item,'fields':[dict(self.item['fields'][0],type='blank')]}):self.assertIsNone(self.meta(item=item))
    def test_missing_changed_or_uncommitted_attestation_falls_back(self):
        path=self.correction/'verification.json';original=path.read_bytes()
        for bad in ({'committed':False}, {'review_sha256':'bad'},{'transaction_sha256':'bad'}):
            proof=json.loads(original);proof.update(bad);atomic_json(path,proof);self.assertIsNone(self.meta())
        path.write_bytes(original);review=self.correction/'review.json';review.write_bytes(review.read_bytes()+b' ')
        self.assertIsNone(self.meta());path.unlink();self.assertIsNone(self.meta())
    def fake_turn(self,payload,screenshot,directory,phase,session_file,session,keys):
        self.calls.append(copy.deepcopy(payload));session['session_id']=session.get('session_id') or str(uuid.uuid4())
        atomic_json(session_file,session)
        choice=next(c for c in payload['fields'][0]['choices'] if c['value']=='II and III only')
        return {'confident':True,'explanation':'II and III contain D under the explicitly reviewed request; the original equality allows all three.',
                'answers':[{'key':'selection','correct_option':choice['option'],'correct_value':choice['value'],'value_type':choice['type'],'wrong_value':'II only','correct_keys':[],'wrong_keys':[]}]}
    def test_cached_literal_answer_gets_one_same_session_recheck_and_raw_is_retained(self):
        literal=json.loads((EVIDENCE/'q-80266/solve-answer.json').read_text())
        prior={'problem':self.item['problem'],'fields':self.item['fields']};atomic_json(self.directory/'solve-input.json',prior);atomic_json(self.directory/'solve-answer.json',literal)
        sid=str(uuid.uuid4());atomic_json(self.activity/'solver-session/state.json',{'session_id':sid,'context_keys':[],'activity':{'task_id':99,'task_type':'lesson','topic_id':TOPIC}})
        before=copy.deepcopy(self.item)
        with patch.object(Solver,'codex_turn',side_effect=self.fake_turn):
            result=Solver(self.args).solve(self.item,None,self.directory)
            self.assertEqual(result['answers'][0]['correct_value'],'II and III only')
            self.assertEqual(self.item,before)
            self.assertEqual(self.calls[0]['source_problem'],before['problem'])
            self.assertIn(r'D\subseteq R',self.calls[0]['problem'])
            self.assertEqual(json.loads((self.directory/'solve-before-containment-policy-answer.json').read_text()),literal)
            self.assertEqual(json.loads((self.activity/'solver-session/state.json').read_text())['session_id'],sid)
            # A streamed-turn recovery can leave the completed answer without adapter metadata.
            restored=json.loads((self.directory/'solve-answer.json').read_text());restored.pop('source_feedback_interpretation')
            atomic_json(self.directory/'solve-answer.json',restored)
            cached=Solver(self.args).solve(self.item,None,self.directory)
            self.assertEqual(cached['source_feedback_interpretation'],self.calls[0]['source_feedback_interpretation'])
            self.assertEqual(len(self.calls),1)
            Solver(self.args).solve({**self.item,'worked_solution':'Source requires R covers D completely.'},None,self.directory,'verify')
            self.assertEqual(len(self.calls),2)
            self.assertEqual(self.calls[1]['source_feedback_interpretation']['identity_sha256'],self.calls[0]['source_feedback_interpretation']['identity_sha256'])
        wrong=copy.deepcopy(result);wrong['answers'][0]['correct_value']='Unavailable all-three answer'
        with self.assertRaisesRegex(ValueError,'exact displayed choice'):Solver.validate(self.item,wrong)
        with self.assertRaisesRegex(ValueError,'uncertain'):Solver.validate(self.item,dict(result,confident=False))
    def test_metadata_keeps_ordinary_import_prompt_authentic_and_flags_followup(self):
        from provenance import source_records
        metadata=self.meta();decision=self.fake_turn({'fields':self.item['fields']},None,self.directory,'solve',self.activity/'solver-session/state.json',{},[]);decision['source_feedback_interpretation']=metadata
        record={'before':copy.deepcopy(self.item),'decision':decision,'after':{'worked_solution':'Revealed source solution'},'actual_result':'Incorrect'}
        q=CaptureBrowser.question_content('q-80266',record,{'id':KP,'title':'Containing region'})
        self.assertEqual(record['before']['problem'],self.item['problem']);self.assertEqual(q['problem'],self.item['problem']);self.assertEqual(q['source_feedback_interpretation'],metadata)
        self.state['questions']['q-80266']=record;atomic_json(self.activity/'state.json',self.state)
        evidence=source_records({'questions':[q],'canonical_examples':[]},self.activity)
        self.assertTrue(any(e['attribute']=='question/problem' and e['category']=='ma_capture' for e in evidence))
        content={'questions':[q]}
        missing=unresolved_study_clarifications(content,self.state,self.root/'missing')
        self.assertEqual([r['question_id'] for r in missing],['q-80266'])
        self.assertEqual(unresolved_study_clarifications(content,self.state,CORRECTION.parent),[])
        self.assertEqual(unresolved_study_clarifications({'questions':[]},self.state,self.root/'missing'),[])


class FollowupEvidenceTests(unittest.TestCase):
    def test_changed_correction_cannot_clear_specific_followup(self):
        q=json.loads((REPOSITORY/'reference/mathacademy/mathematical-corrections/q-80266/review.json').read_text())['original_content']
        meta={'policy':'zero-extension-containing-rectangle-v1','topic_id':TOPIC,'knowledge_point_id':KP,'requires_study_clarification':True,'source_problem':q['problem'],'requirement':r'D\subseteq R'}
        q=dict(q,source_feedback_interpretation=meta)
        with tempfile.TemporaryDirectory() as name:
            root=Path(name);directory=root/'q-80266';directory.mkdir()
            for file in ('review.json','verification.json','transaction.edn'):(directory/file).write_bytes((CORRECTION.parent/'q-80266'/file).read_bytes())
            self.assertEqual(unresolved_study_clarifications({'questions':[q]}, {},root),[])
            (directory/'review.json').write_bytes((directory/'review.json').read_bytes()+b' ')
            self.assertEqual(len(unresolved_study_clarifications({'questions':[q]}, {},root)),1)


if __name__=='__main__':unittest.main()
