"""Exact q330826 domain correction and persistent-session safety boundaries."""
import copy,json,tempfile,unittest,uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from core import ROOT,atomic_json
from solver import Solver
from source_interpretation import reviewed_laplace_domain,unresolved_study_clarifications,LAPLACE_TOPIC,LAPLACE_KP
CAP=ROOT/'reference/mathacademy/question-capture-workers/differential/14073261'
CORRECTION=ROOT/'reference/mathacademy/mathematical-corrections/q-330826'
class LaplaceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.activity=self.root/'capture';self.directory=self.activity/'q-330826';self.directory.mkdir(parents=True)
  self.item=json.loads((CAP/'diagnostics/1791548758910350122/current-question.json').read_text());self.state={'task_id':14073261,'topic_id':LAPLACE_TOPIC,'task_type':'lesson','current_kp':LAPLACE_KP,'questions':{},'examples':{}};atomic_json(self.activity/'state.json',self.state)
  self.correction=self.root/'reference/mathacademy/mathematical-corrections/q-330826';self.correction.mkdir(parents=True)
  for name in ('review.json','verification.json','transaction.edn'):(self.correction/name).write_bytes((CORRECTION/name).read_bytes())
  scope=patch('source_interpretation.ROOT',self.root);scope.start();self.addCleanup(scope.stop)
 def meta(self,item=None,state=None,directory=None):return reviewed_laplace_domain(item or self.item,state or self.state,directory or self.directory)
 def test_exact_domain_and_random_choice_order(self):
  m=self.meta();self.assertIsNotNone(m);self.assertEqual(m['interpreted_problem'],self.item['problem'].replace('for $s>-3.$','for $s>0.$'));self.assertIn('diverges',m['confidence_scope']);changed=copy.deepcopy(self.item);changed['fields'][0]['choices'].reverse()
  for option,c in zip('abcde',changed['fields'][0]['choices']):c['option']=option
  self.assertIsNotNone(self.meta(item=changed))
 def test_missing_mutated_and_out_of_scope_fail_closed(self):
  self.assertIsNone(self.meta(state={**self.state,'topic_id':1}));self.assertIsNone(self.meta(state={**self.state,'current_kp':'wrong'}));self.assertIsNone(self.meta(directory=self.activity/'q-330827'));self.assertIsNone(self.meta(item={**self.item,'problem':self.item['problem']+' '}))
  for key,value in [('value','another value'),('type','text')]:
   changed=copy.deepcopy(self.item);changed['fields'][0]['choices'][0][key]=value;self.assertIsNone(self.meta(item=changed))
  proof=self.correction/'verification.json';original=proof.read_bytes()
  for bad in ({'committed':False},{'mathematical_check_passed':False},{'review_sha256':'bad'},{'transaction_sha256':'bad'}):
   d=json.loads(original);d.update(bad);atomic_json(proof,d);self.assertIsNone(self.meta())
  proof.write_bytes(original);(self.correction/'transaction.edn').write_text('[changed]');self.assertIsNone(self.meta());(self.correction/'transaction.edn').unlink();self.assertIsNone(self.meta())
 def test_same_session_uncertainty_archive_and_strict_choices(self):
  inp=json.loads((CAP/'q-330826/solve-before-reviewed-source-error-input.json').read_text());prior=json.loads((CAP/'q-330826/solve-before-reviewed-source-error-answer.json').read_text());atomic_json(self.directory/'solve-input.json',inp);atomic_json(self.directory/'solve-answer.json',prior);sid=str(uuid.uuid4());sf=self.activity/'solver-session/state.json';atomic_json(sf,{'session_id':sid,'context_keys':[],'activity':{'task_id':14073261,'task_type':'lesson','topic_id':LAPLACE_TOPIC}});calls=[]
  def turn(payload,*args):
   calls.append(copy.deepcopy(payload));c=next(c for c in payload['fields'][0]['choices'] if c['value']==r'\frac{1}{s(s+3)}');return {'confident':True,'explanation':'Domain s>0 only.','answers':[{'key':'selection','correct_option':c['option'],'correct_value':c['value'],'value_type':'math','wrong_value':None,'correct_keys':[],'wrong_keys':[]}]}
  before=copy.deepcopy(self.item)
  with patch.object(Solver,'codex_turn',side_effect=turn):
   solver=Solver(SimpleNamespace(solver_command=None,solver_timeout=5));result=solver.solve(self.item,None,self.directory);solver.solve(self.item,None,self.directory)
  self.assertEqual(len(calls),1);self.assertEqual(json.loads(sf.read_text())['session_id'],sid);self.assertEqual(self.item,before);self.assertEqual(json.loads((self.directory/'solve-before-laplace-domain-policy-answer.json').read_text()),prior);self.assertEqual(calls[0]['source_problem'],before['problem']);self.assertTrue(calls[0]['problem'].endswith('for $s>0.$'))
  with self.assertRaisesRegex(ValueError,'uncertain'):Solver.validate(self.item,{**result,'confident':False})
  bad=copy.deepcopy(result);bad['answers'][0]['correct_value']+=', s>0'
  with self.assertRaisesRegex(ValueError,'exact displayed choice'):Solver.validate(self.item,bad)
  q=json.loads((self.correction/'review.json').read_text())['original_content'];q['source_feedback_interpretation']=result['source_feedback_interpretation'];self.assertEqual(unresolved_study_clarifications({'questions':[q]}, {},self.correction.parent),[]);self.assertEqual(len(unresolved_study_clarifications({'questions':[q]}, {},self.root/'absent')),1)
if __name__=='__main__':unittest.main()
