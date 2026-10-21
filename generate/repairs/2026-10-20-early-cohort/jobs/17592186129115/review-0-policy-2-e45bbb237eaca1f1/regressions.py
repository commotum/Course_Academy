import sys,json,pathlib,unittest
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(E.parent/'workspace'));import generator
class SourceContract(unittest.TestCase):
 def test_complete_q73149_bank_accepts_already_zero_distractor(self):
  case=next(x for x in json.loads((E/'source-replay.json').read_text()) if x['source_id']=='5da4a360-a207-5df6-9d38-99e7b8b5a765')
  generator.generate('moderate',9100,parameters=case['parameters'])
 def test_valid_offered_operation_need_not_be_globally_minimum(self):
  case=json.loads((E/'nonminimum-case.json').read_text());generator.generate('moderate',case['seed'],parameters=case['parameters'])
 def test_prompt_does_not_add_optimization(self):
  r=generator.generate('moderate',702311);self.assertNotIn('fewest replacements',r['question'][':question/problem'])
if __name__=='__main__':unittest.main()
