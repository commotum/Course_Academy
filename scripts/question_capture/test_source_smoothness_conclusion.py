"""The exact committed conclusion correction keeps source choices and solver identity."""
import copy,json,tempfile,unittest,uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from core import ROOT,atomic_json
from solver import Solver
from source_interpretation import reviewed_smoothness_conclusion,unresolved_study_clarifications,SMOOTHNESS_TOPIC,SMOOTHNESS_KP,SMOOTHNESS_RIGHT
CAP=ROOT/'reference/mathacademy/question-capture-workers/differential/14074297'
CORRECTION=ROOT/'reference/mathacademy/mathematical-corrections/q-340850'

class SmoothnessTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.activity=self.root/'capture';self.directory=self.activity/'q-340850';self.directory.mkdir(parents=True)
  self.item=json.loads((CAP/'q-340850-proof-observed-2.json').read_text())
  self.state={'task_id':14074297,'topic_id':SMOOTHNESS_TOPIC,'task_type':'review','questions':{},'examples':{}};atomic_json(self.activity/'state.json',self.state)
  self.correction=self.root/'reference/mathacademy/mathematical-corrections/q-340850';self.correction.mkdir(parents=True)
  for name in ('review.json','verification.json','transaction.edn'):(self.correction/name).write_bytes((CORRECTION/name).read_bytes())
  scope=patch('source_interpretation.ROOT',self.root);scope.start();self.addCleanup(scope.stop)
 def meta(self,item=None,state=None,directory=None):return reviewed_smoothness_conclusion(item or self.item,state or self.state,directory or self.directory)
 def test_exact_typo_and_random_options(self):
  m=self.meta();self.assertIsNotNone(m);self.assertEqual(m['interpreted_problem'],self.item['problem'].replace('L{{t}^{2}{e}^{4t}}={{field-4}}',SMOOTHNESS_RIGHT))
  changed=copy.deepcopy(self.item)
  for f in changed['fields']:
   f['choices'].reverse()
   for i,c in enumerate(f['choices']):c['option']='option-'+str(i)
  self.assertIsNotNone(self.meta(item=changed));self.assertIn('authentic final grade',m['confidence_scope'])
 def test_stage_and_scope_boundaries(self):
  self.assertIsNone(self.meta(item={**self.item,'fields':self.item['fields'][:3]}))
  self.assertIsNone(self.meta(directory=self.activity/'q-340844'));self.assertIsNone(self.meta(state={**self.state,'topic_id':1}))
  self.assertIsNone(self.meta(state={**self.state,'current_kp':'wrong'}));self.assertIsNotNone(self.meta(state={**self.state,'current_kp':SMOOTHNESS_KP}))
  self.assertIsNone(self.meta(item={**self.item,'problem':self.item['problem']+' '}))
  for key,value in [('value','another value'),('type','text')]:
   changed=copy.deepcopy(self.item);changed['fields'][3]['choices'][0][key]=value;self.assertIsNone(self.meta(item=changed))
  changed=copy.deepcopy(self.item);changed['fields'][3]['choices_complete']=False;self.assertIsNone(self.meta(item=changed))
 def test_uncommitted_or_changed_attestation_fails_closed(self):
  p=self.correction/'verification.json';original=p.read_bytes()
  for bad in ({'committed':False},{'mathematical_check_passed':False},{'answer_fields_choices_and_answer_identities_unchanged':False},{'review_sha256':'bad'},{'transaction_sha256':'bad'}):
   d=json.loads(original);d.update(bad);atomic_json(p,d);self.assertIsNone(self.meta())
  p.write_bytes(original);tx=self.correction/'transaction.edn';original_tx=tx.read_bytes();tx.write_text('[changed]');self.assertIsNone(self.meta());tx.write_bytes(original_tx)
  review=self.correction/'review.json';review.write_bytes(review.read_bytes()+b' ');self.assertIsNone(self.meta())
 def test_same_session_rechecks_uncertainty_once_with_strict_validation(self):
  prior=json.loads((CAP/'q-340850/proof-solve-3-before-reviewed-source-error-answer.json').read_text());inp=json.loads((CAP/'q-340850/proof-solve-3-before-reviewed-source-error-input.json').read_text())
  atomic_json(self.directory/'proof-solve-3-input.json',inp);atomic_json(self.directory/'proof-solve-3-answer.json',prior)
  sid=str(uuid.uuid4());sf=self.activity/'solver-session/state.json';atomic_json(sf,{'session_id':sid,'context_keys':[],'activity':{'task_id':14074297,'task_type':'review','topic_id':SMOOTHNESS_TOPIC}});calls=[]
  observed=json.loads((CAP/'q-340850/proof-solve-3-answer.json').read_text());self.assertTrue(observed['confident'])
  def turn(payload,*args):calls.append(copy.deepcopy(payload));return copy.deepcopy(observed)
  before=copy.deepcopy(self.item)
  with patch.object(Solver,'codex_turn',side_effect=turn):
   s=Solver(SimpleNamespace(solver_command=None,solver_timeout=5));result=s.solve(self.item,None,self.directory,'proof-solve-3');s.solve(self.item,None,self.directory,'proof-solve-3')
  self.assertEqual(len(calls),1);self.assertEqual(self.item,before);self.assertEqual(json.loads(sf.read_text())['session_id'],sid)
  self.assertEqual(json.loads((self.directory/'proof-solve-3-before-smoothness-conclusion-policy-answer.json').read_text()),prior)
  self.assertEqual(calls[0]['source_problem'],before['problem']);self.assertIn(SMOOTHNESS_RIGHT,calls[0]['problem'])
  with self.assertRaisesRegex(ValueError,'uncertain'):Solver.validate(self.item,{**result,'confident':False})
  bad=copy.deepcopy(result);bad['answers'][3]['correct_value']=r'\frac{2}{(s-4)^3}'
  with self.assertRaisesRegex(ValueError,'exact displayed choice'):Solver.validate(self.item,bad)
  q=json.loads((self.correction/'review.json').read_text())['original_content'];q['source_feedback_interpretation']=result['source_feedback_interpretation']
  self.assertEqual(unresolved_study_clarifications({'questions':[q]}, {},self.correction.parent),[])
  self.assertEqual(len(unresolved_study_clarifications({'questions':[q]}, {},self.root/'absent')),1)

if __name__=='__main__':unittest.main()
