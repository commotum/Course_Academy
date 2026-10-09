"""The nine archived blockers recover without hiding math or inventing MA grades.

Feedback below is synthetic: these offline tests exercise control flow, not live keys.
"""
import copy
import json
import tempfile
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from answer_policy import BEST_EFFORT, SOURCE_ANSWER, best_effort, binding, soften_sequence
from browser import CaptureBrowser
from capture import queued_resume
from capture_repair import deferred_failure, evidence_version, failure_key, source_version
from core import atomic_json
from provenance import source_records
from solver import Solver

CASES = json.loads((Path(__file__).parent/'fixtures/blocked-nine.json').read_text())


class AnswerRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.args = SimpleNamespace(solver_command=None, solver_timeout=5,
            state_dir=self.root/'worker', output=self.root/'captures', edb_bin=None)
        self.calls = []
        self.sid = str(uuid.uuid4())

    def setup_case(self, case):
        activity = self.args.output/str(case['task_id']); directory = activity/case['question_id']
        directory.mkdir(parents=True, exist_ok=True)
        state = {k:case[k] for k in ('task_id','topic_id','task_type')}
        state.update(questions={}, examples={}, kps={'kp':{'id':'kp','title':'Saved KP','sequence':'CWCWC'}},
                     current_kp='kp', review_sequence='WCWCC')
        item = copy.deepcopy(case['item'])
        atomic_json(activity/'state.json', state)
        atomic_json(directory/'solve-input.json', {**item, 'mode':'solve',
            'choice_confidence_policy':'equivalent-choices-v1', 'uncertainty_retry':1})
        atomic_json(directory/'solve-answer.json', case['mathematical_assessment'])
        atomic_json(activity/'solver-session/state.json', {'session_id':self.sid, 'context_keys':[],
            'activity':{k:state[k] for k in ('task_id','task_type','topic_id')}})
        return activity, directory, state, item

    def response(self, item, value, confident=False):
        field = item['fields'][0]
        choice = next((c for c in field['choices'] if c['value'] == value), None)
        return {'confident':confident, 'explanation':'Synthetic response: keep mathematical criticism separate from submission/source identification.',
            'answers':[{'key':field['key'], 'correct_option':choice['option'] if choice else None,
                'correct_value':value, 'value_type':choice['type'] if choice else ('math' if field['type']=='blank' else 'text'),
                'wrong_value':'gt-4.6' if field['type']=='blank' else None,
                'correct_keys':[{'text':value,'key':None}] if field['type']=='blank' else [],
                'wrong_keys':[{'text':'gt-4.6','key':None}] if field['type']=='blank' else []}]}

    def recover(self, case, directory, item):
        def turn(payload, screenshot, directory, phase, session_file, session, keys):
            self.calls.append(copy.deepcopy(payload))
            self.assertEqual(phase, 'best-effort')
            self.assertEqual(session['session_id'], self.sid)
            self.assertEqual(payload['submission_policy']['mathematical_assessment'], case['mathematical_assessment'])
            return self.response(payload, case['best_guess_value'])
        with patch.object(Solver, 'codex_turn', side_effect=turn):
            return Solver(self.args).solve(item, None, directory)

    def test_all_nine_recover_once_and_survive_shuffled_controls(self):
        for case in CASES:
            with self.subTest(activity=case['task_id']):
                activity, directory, state, item = self.setup_case(case)
                original = (directory/'solve-answer.json').read_bytes()
                result = self.recover(case, directory, item)
                self.assertFalse(result['confident']); self.assertTrue(best_effort(result, item))
                Solver.validate(item, result)
                self.assertEqual((directory/'solve-answer.json').read_bytes(), original)
                record = {'before':item, 'decision':result, 'intended':'W'}
                soften_sequence(record)
                self.assertEqual((record['desired_intended'],record['intended']), ('W','C'))
                self.assertEqual(record['mathematical_assessment'], case['mathematical_assessment'])
                with patch.object(Solver,'codex_turn') as model:
                    self.assertEqual(Solver(self.args).solve(item, None, directory), result)
                    model.assert_not_called()
                shuffled = copy.deepcopy(item)
                shuffled['fields'][0]['choices'].reverse()
                for index, choice in enumerate(shuffled['fields'][0]['choices']): choice['option']=str(index)
                restored = Solver.reuse_answer(shuffled, result, item)
                self.assertEqual(restored['answers'][0]['correct_value'], case['best_guess_value'])
        self.assertEqual(len(self.calls), 9)

    def test_all_nine_finalize_and_reach_activity_completion_for_each_grade(self):
        for case in CASES:
            for grade in ('Correct', 'Incorrect', 'Partial Credit'):
                with self.subTest(activity=case['task_id'], grade=grade):
                    activity, directory, state, item = self.setup_case(case)
                    result = self.recover(case, directory, item)
                    record = {'kp_id':'kp','before':item,'decision':result,'intended':'W','status':'graded'}
                    soften_sequence(record)
                    item['fields'][0].update(submitted_value=case['best_guess_value'],
                        submitted_option=result['answers'][0]['correct_option'])
                    record.update(actual_result=grade, after={'worked_solution':'Synthetic MA feedback declares '+case['best_guess_value'], 'result':grade})
                    def source_turn(payload, screenshot, directory, phase, session_file, session, keys):
                        self.assertEqual(phase,'verify')
                        self.assertEqual(payload['source_answer_policy']['version'], SOURCE_ANSWER)
                        return self.response(payload, case['best_guess_value'], confident=True)
                    reader = object.__new__(CaptureBrowser); reader.solver=Solver(self.args)
                    with patch.object(Solver,'codex_turn',side_effect=source_turn):
                        reader.finalize_question(state, activity, case['question_id'], record)
                    self.assertTrue(record['finalized'])
                    self.assertEqual(record['content']['problem'], item['problem'])
                    self.assertEqual(record['content']['mathematical_assessment'], case['mathematical_assessment'])
                    self.assertEqual(record['content']['worked_solution'], record['after']['worked_solution'])
                    state['questions']={case['question_id']:record}
                    atomic_json(activity/'state.json', state)
                    evidence = source_records({'questions':[record['content']]}, activity)
                    category = 'ma_successful_grade' if grade=='Correct' else 'reviewed_ma_solution'
                    self.assertTrue(any(e['attribute']=='answer-field/correct' and e['category']==category for e in evidence))
                    reader.page=Mock(); reader.args=SimpleNamespace(cwcwc_weight=.7)
                    reader.pacer=Mock(); reader.check=Mock(); reader.wait_activity_ready=Mock(); reader.knowledge_snapshot=Mock()
                    reader.page.locator.return_value.is_visible.return_value=True
                    reader.page.locator.return_value.inner_text.return_value='You completed the '+state['task_type']+'. You earned 10 XP.'
                    reader.activity(state, activity, {})
                    self.assertTrue(state['activity_complete'])
                    self.assertEqual(state['activity_outcome'], 'passed')

    def test_missing_choice_can_be_preserved_from_feedback_but_never_clicked(self):
        case=next(c for c in CASES if c['question_id']=='q-94772')
        activity, directory, state, item=self.setup_case(case)
        result=self.recover(case,directory,item)
        record={'kp_id':'kp','before':item,'decision':result,'intended':'C','status':'graded',
            'actual_result':'Incorrect','after':{'worked_solution':'Synthetic source: I and III only.'}}
        soften_sequence(record)
        def source_turn(payload, *args):return self.response(payload,'I and III only',confident=True)
        reader=object.__new__(CaptureBrowser);reader.solver=Solver(self.args)
        with patch.object(Solver,'codex_turn',side_effect=source_turn):
            reader.finalize_question(state,activity,case['question_id'],record)
        field=record['content']['answer_fields'][0]
        self.assertEqual(field['correct_value'],'I and III only')
        self.assertEqual(len(field['choices']),6)
        self.assertEqual(len(record['before']['fields'][0]['choices']),5)
        self.assertTrue(record['finalized'])
        Solver.reuse_answer({**item,'worked_solution':record['after']['worked_solution']},record['verification'],item)
        # Source-key metadata does not make an absent option a valid submission.
        with self.assertRaisesRegex(ValueError,'exact displayed choice'):
            Solver.validate(item,dict(record['verification'],source_answer_policy={}))
        with self.assertRaisesRegex(ValueError,'exact displayed choice'):
            Solver.validate({**item,'worked_solution':'Changed feedback'},record['verification'])

    def test_old_permanent_deferrals_reopen_all_nine_without_resetting_budget(self):
        ledger={}
        for case in CASES:
            activity, directory, state, item=self.setup_case(case)
            diagnostic=activity/'diagnostics/1/error.json'
            atomic_json(diagnostic, {'task_id':case['task_id'],'phase':'activity','exception_type':'ValueError',
                'message':'Solver is uncertain; question saved for review'})
            state['deferred_error']={'diagnostics':str(diagnostic.parent)};atomic_json(activity/'state.json',state)
            ledger[failure_key(json.loads(diagnostic.read_text()))]={'status':'blocked','attempts':2,
                'retry_on_source_change':False,'evidence_version':evidence_version(diagnostic)}
            atomic_json(self.args.state_dir/'capture-repair/failures.json',ledger)
            snapshot=copy.deepcopy(ledger)
            self.assertEqual(queued_resume(self.args,[{'task_id':case['task_id']}],set()),activity.resolve())
            self.assertTrue(deferred_failure(self.args,diagnostic,ledger,source_version()))
            self.assertEqual(ledger,snapshot)
            # A failed recovery is not an excuse for an unbounded budget reset.
            atomic_json(directory/'best-effort-input.json',item)
            ledger[failure_key(json.loads(diagnostic.read_text()))]['evidence_version']=evidence_version(diagnostic)
            self.assertTrue(deferred_failure(self.args,diagnostic,ledger,source_version(),resume=True))

    def test_best_effort_cannot_bypass_controls_or_diagnostic_coverage(self):
        case=CASES[0];_,directory,_,item=self.setup_case(case)
        result=self.recover(case,directory,item)
        for bad in (dict(result,submission_policy={}),
                    dict(result,submission_policy={**result['submission_policy'],'question_sha256':'bad'})):
            with self.assertRaisesRegex(ValueError,'uncertain'):Solver.validate(item,bad)
        bad=copy.deepcopy(result);bad['answers'][0]['correct_option']='missing'
        with self.assertRaisesRegex(ValueError,'exact displayed choice'):Solver.validate(item,bad)
        with self.assertRaisesRegex(ValueError,'uncertain'):
            Solver.validate(dict(item,diagnostic_policy={'mode':'other'}),result)

    def test_stopped_status_reports_recovery_readiness_without_starting_workers(self):
        import fleet
        case=CASES[0];activity,directory,state,item=self.setup_case(case)
        diagnostic=activity/'diagnostics/1/error.json'
        atomic_json(diagnostic,{'message':'Solver is uncertain; question saved for review'})
        state['deferred_error']={'diagnostics':str(diagnostic.parent)};atomic_json(activity/'state.json',state)
        worker={'id':'test','window':'Test','state_dir':self.args.state_dir,'output':self.args.output,
            'supervision':self.root/'supervision','auth_file':self.root/'auth.json'}
        atomic_json(worker['supervision']/'fleet-worker.json',{'stop_requested':True})
        with patch('fleet.capture_running',return_value=False),patch('fleet.supervisor_running',return_value=False),\
             patch('fleet.ready',return_value=True),patch('fleet.queue_wait_status',return_value={'tasks':[{'task_id':case['task_id']}]}):
            result=fleet.worker_status(worker)
        self.assertEqual(result['status'],'STOPPED')
        self.assertFalse(result['process_running'])
        self.assertIn('ready for best-effort recovery',result['detail'])


class RecoveryControlTests(unittest.TestCase):
    """Real Chromium and MA's MathQuill distribution; no Math Academy requests."""
    import test_capture as existing
    setUpClass = classmethod(existing.DOMTests.setUpClass.__func__)
    tearDownClass = classmethod(existing.DOMTests.tearDownClass.__func__)
    setUp = existing.DOMTests.setUp
    tearDown = existing.DOMTests.tearDown
    mathquill_fixture = existing.DOMTests.mathquill_fixture

    def test_all_nine_best_effort_responses_enter_real_visible_controls_once(self):
        import random
        from core import Pacer
        args=SimpleNamespace(timeout_ms=3000,event_min=0,event_max=0)
        reader=CaptureBrowser(self.page,args,Pacer(args,random.Random(42)),None)
        for case in CASES:
            with self.subTest(activity=case['task_id']):
                item=copy.deepcopy(case['item'])
                if item['fields'][0]['type']=='blank':
                    scope, fixture=self.mathquill_fixture()
                    item['fields']=fixture['before']['fields']
                else:
                    self.page.set_content('<div id="test">'+''.join(
                        '<button id="choice-'+c['option']+'" class="questionWidget-choiceLetterCircle">'+c['option']+'</button>'
                        for c in item['fields'][0]['choices'])+'<button id="submit">Submit</button></div>'
                        '<script>window.submissions=0;document.querySelectorAll(".questionWidget-choiceLetterCircle").forEach('
                        'b=>b.onclick=()=>{document.querySelectorAll(".selectedChoice").forEach(n=>n.classList.remove("selectedChoice"));'
                        'b.classList.add("selectedChoice");});document.querySelector("#submit").onclick=()=>window.submissions++;</script>')
                    scope=self.page.locator('#test')
                    for c in item['fields'][0]['choices']:c['dom_id']='choice-'+c['option']
                decision=AnswerRecoveryTests.response(self,item,case['best_guess_value'])
                decision['submission_policy']={'version':BEST_EFFORT,'question_sha256':binding(item),
                    'mathematical_assessment':case['mathematical_assessment']}
                record={'before':item,'decision':decision,'intended':'W'}
                soften_sequence(record)
                reader.enter(scope,record)
                reader.verify_entered(scope,record)
                self.assertEqual(item['fields'][0]['submitted_value'],case['best_guess_value'])
                self.assertEqual(self.page.evaluate('window.submissions'),0)
                scope.locator('.questionWidget-submitButton' if item['fields'][0]['type']=='blank' else '#submit').click()
                self.assertEqual(self.page.evaluate('window.submissions'),1)


if __name__=='__main__':unittest.main()
