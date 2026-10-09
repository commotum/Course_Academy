"""Exact authentic q335252 theorem clarification, evidence and restart guards."""
import copy,json,tempfile,unittest,uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from core import ROOT,atomic_json
from solver import Solver
from source_interpretation import reviewed_integral_theorem,unresolved_study_clarifications,INTEGRAL_TOPIC
CAP=ROOT/'reference/mathacademy/question-capture-workers/multivariable/14073413'
CORRECTION=ROOT/'reference/mathacademy/mathematical-corrections/q-335252'
class IntegralTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.activity=self.root/'capture';self.directory=self.activity/'q-335252';self.directory.mkdir(parents=True)
  self.item=json.loads((CAP/'q-335252-before.json').read_text());self.state={'task_id':14073413,'topic_id':INTEGRAL_TOPIC,'task_type':'review','questions':{},'examples':{}};atomic_json(self.activity/'state.json',self.state)
  self.correction=self.root/'reference/mathacademy/mathematical-corrections/q-335252';self.correction.mkdir(parents=True)
  for name in ('review.json','verification.json','transaction.edn'):(self.correction/name).write_bytes((CORRECTION/name).read_bytes())
  self.scope=patch('source_interpretation.ROOT',self.root);self.scope.start();self.addCleanup(self.scope.stop)
 def meta(self,item=None,state=None,directory=None):return reviewed_integral_theorem(item or self.item,state or self.state,directory or self.directory)
 def test_source_context_and_mathematical_distinction(self):
  prior=json.loads((ROOT/'reference/mathacademy/question-capture-workers/differential/14071891/q-335252-after.json').read_text());self.assertEqual(prior['result'],'Correct');self.assertIn('I and III only',prior['worked_solution'])
  meta=self.meta();self.assertIn('sufficient theorem',meta['interpreted_problem']);self.assertEqual(meta['source_problem'],self.item['problem']);self.assertIn('dominated convergence',meta['confidence_scope'])
  # Exact integration, derivative and a Lipschitz bound distinguish the two claims.
  for t in (0.25,0.5,0.75):
   h=1e-5;F=lambda u:u*u-u+0.5
   self.assertAlmostEqual((F(t+h)-F(t-h))/(2*h),2*t-1,places=8)
   for x in (0,0.3,0.5,1):self.assertLessEqual(abs(abs(x-t-h)-abs(x-t))/h,1.000001)
 def test_scope_missing_or_mutated_evidence_fail_closed(self):
  self.assertIsNone(self.meta(state={**self.state,'topic_id':1}));self.assertIsNone(self.meta(directory=self.activity/'q-335253'))
  self.assertIsNone(self.meta(item={**self.item,'problem':self.item['problem']+' '}));changed=copy.deepcopy(self.item);changed['fields'][0]['choices'][0]['value']='Another choice';self.assertIsNone(self.meta(item=changed))
  changed=copy.deepcopy(self.item);changed['fields'][0]['type']='blank';self.assertIsNone(self.meta(item=changed))
  proof=self.correction/'verification.json';original=proof.read_bytes()
  for bad in ({'committed':False},{'review_sha256':'bad'},{'transaction_sha256':'bad'}):
   d=json.loads(original);d.update(bad);atomic_json(proof,d);self.assertIsNone(self.meta())
  proof.write_bytes(original);(self.correction/'review.json').write_bytes((self.correction/'review.json').read_bytes()+b' ');self.assertIsNone(self.meta())
 def test_same_session_recheck_archives_uncertainty_and_preserves_widgets(self):
  inp={'problem':self.item['problem'],'fields':self.item['fields'],'choice_confidence_policy':'equivalent-choices-v1'}
  choice=next(c for c in self.item['fields'][0]['choices'] if c['value']=='I and III only')
  prior={'confident':False,'explanation':'Unresolved theorem scope before authentic context.','answers':[{'key':'selection','correct_option':choice['option'],'correct_value':choice['value'],'value_type':'text','wrong_value':'None','correct_keys':[],'wrong_keys':[]}]}
  atomic_json(self.directory/'solve-input.json',inp);atomic_json(self.directory/'solve-answer.json',prior);sid=str(uuid.uuid4());sf=self.activity/'solver-session/state.json';atomic_json(sf,{'session_id':sid,'context_keys':[],'activity':{'task_id':14073413,'task_type':'review','topic_id':6682}});calls=[]
  def turn(payload,*args):
   calls.append(copy.deepcopy(payload));choice=next(c for c in payload['fields'][0]['choices'] if c['value']=='I and III only');return {'confident':True,'explanation':'Sufficient theorem applies to I/III; II still admits DCT interchange.','answers':[{'key':'selection','correct_option':choice['option'],'correct_value':choice['value'],'value_type':'text','wrong_value':'None','correct_keys':[],'wrong_keys':[]}]}
  before=copy.deepcopy(self.item)
  with patch.object(Solver,'codex_turn',side_effect=turn):
   solver=Solver(SimpleNamespace(solver_command=None,solver_timeout=5));result=solver.solve(self.item,None,self.directory);solver.solve(self.item,None,self.directory)
  self.assertEqual(len(calls),1);self.assertEqual(json.loads(sf.read_text())['session_id'],sid);self.assertEqual(self.item,before);self.assertEqual(json.loads((self.directory/'solve-before-integral-theorem-policy-answer.json').read_text()),prior)
  self.assertEqual(calls[0]['source_problem'],before['problem']);self.assertEqual(result['answers'][0]['correct_value'],'I and III only')
  with self.assertRaisesRegex(ValueError,'uncertain'):Solver.validate(self.item,{**result,'confident':False})
  q=json.loads((CORRECTION/'review.json').read_text())['original_content'];q['source_feedback_interpretation']=result['source_feedback_interpretation']
  self.assertEqual(unresolved_study_clarifications({'questions':[q]}, {},self.correction.parent),[])
  self.assertEqual(len(unresolved_study_clarifications({'questions':[q]}, {},self.root/'absent')),1)
if __name__=='__main__':unittest.main()
