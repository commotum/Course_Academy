"""Solved cloze captures retain the enclosing formula and verified answer types."""
import importlib.util,re,sys,unittest
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('historical_control_import',ROOT/'scripts/import_historical_question_content.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
FIXTURES=ROOT/'tests/fixtures/historical-controls'
class HistoricalControlsTests(unittest.TestCase):
 def test_authentic_solved_captures_bind_every_observed_control_once(self):
  for name in ['q-337133','q-318660','q-333756','q-333727','q-337707']:
   with self.subTest(question=name):
    renderer=module.Renderer(6353);out=renderer.text(BeautifulSoup((FIXTURES/(name+'-after.html')).read_text(),'html.parser'),True)
    self.assertEqual(renderer.errors,[]);self.assertEqual(sorted(f['key']for f in renderer.fields),sorted(re.findall(r'\{\{([^}]+)\}\}',out)))
    self.assertNotRegex(out,r'\(S\d+\)')
    for f in renderer.fields:
     for choice in f['choices']:
      if choice['value']in ['is',"isn't",'is not']:self.assertEqual(choice['type'],'text')
    if name=='q-318660':self.assertIn('{{field-1}}=h(y)',out)
    if name=='q-337133':self.assertIn('{{field-1}}=0',out)
 def test_before_capture_default_is_not_answer_key_evidence(self):
  renderer=module.Renderer(6353)
  with self.assertRaisesRegex(AssertionError,'Unverified historical dropdown'):
   renderer.text(BeautifulSoup((FIXTURES/'q-318659-before.html').read_text(),'html.parser'),True)
 def test_mixed_prose_option_remains_text_and_disabled_does_not_prove_correctness(self):
  html='<div class="selectList" id="source-select-0"><span class="selectListFrameDisabled correctSelection">for all <math><mi>x</mi></math></span><span class="selectListOption">for all <math><mi>x</mi></math></span><span class="selectListOption">sometimes</span></div>'
  renderer=module.Renderer(None);renderer.text(BeautifulSoup(html,'html.parser'),True)
  self.assertEqual(renderer.fields[0]['choices'][0],{'type':'text','value':'for all $x$'})
  with self.assertRaisesRegex(AssertionError,'Unverified historical dropdown'):
   module.Renderer(None).text(BeautifulSoup(html.replace(' correctSelection',''),'html.parser'),True)
if __name__=='__main__':unittest.main()
