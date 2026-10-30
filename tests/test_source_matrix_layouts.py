"""Archived bracket/system layouts keep cells and controls across importers."""
import json,re,sys,unittest
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'scripts'),str(R/'scripts/question_capture')]
from import_historical_question_content import Renderer
from html_tables import source_table_html
FIXTURES=json.loads((R/'tests/fixtures/source-matrix-layouts.json').read_text())
class MatrixLayoutImportTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(headless=True);cls.page=cls.browser.new_page();cls.page.route('**/*',lambda r:r.abort())
 @classmethod
 def tearDownClass(cls):cls.browser.close();cls.p.stop()
 def assert_layout(self,fixture,value):
  soup=BeautifulSoup(value,'html.parser');tables=soup.select('.matrix-answer table')
  self.assertEqual(len(tables),3 if fixture['kind']=='matrix_product'else 1)
  self.assertFalse(soup.select('.source-table'))
  self.assertFalse(any(t.find('table')for t in tables))
  expected=[[re.findall(r'\{\{([^{}]+)\}\}',c)for row in grid for c in row]for grid in fixture['grids']]
  actual=[[re.findall(r'\{\{([^{}]+)\}\}',str(c))for c in t.find_all('td')]for t in tables]
  self.assertEqual(actual,expected)
  if fixture['prefactor_field']:
   self.assertIn('{{'+fixture['prefactor_field']+'}}',str(soup.select_one('.matrix-answer-label')))
   self.assertNotIn('{{'+fixture['prefactor_field']+'}}',str(tables[0]))
  keys=re.findall(r'\{\{([^{}]+)\}\}',value);self.assertEqual(len(keys),len(set(keys)))
 def test_live_and_capture_extractors(self):
  for fixture in FIXTURES:
   self.page.set_content('<div id="fixture"><div class="questionWidget-result">Correct</div><div class="questionWidget-text">'+fixture['html']+'</div></div>')
   for name in['scripts/question_capture/dom.js','capture/scripts/browser/extract.js']:
    with self.subTest(source=fixture['identity'],extractor=name):
     result=self.page.locator('#fixture').evaluate((R/name).read_text());self.assertEqual(result['errors'],[])
     self.assert_layout(fixture,result['problem'])
     self.assertEqual(set(re.findall(r'\{\{([^{}]+)\}\}',result['problem'])),{f['key']for f in result['fields']})
 def test_python_renderer_uses_the_same_semantic_cells(self):
  for fixture in FIXTURES:
   with self.subTest(source=fixture['identity']):
    soup=BeautifulSoup(fixture['html'],'html.parser')
    # Source metadata binds IDs before rendering; never copy an entered value
    # from an unsupported live MathQuill editor into the problem statement.
    for n in soup.select('.freeResponseTextbox,.matheditor-wrapper-answer'):
     n.replace_with('{{field-'+n['id'].rsplit('-',1)[1]+'}}')
    renderer=Renderer(None);value=renderer.render(soup.table);self.assertEqual(renderer.errors,[]);self.assert_layout(fixture,value)
 def test_unsupported_control_cannot_become_a_prefilled_answer(self):
  fixture=next(f for f in FIXTURES if f['identity']=='q-317518')
  soup=BeautifulSoup(fixture['html'],'html.parser')
  with self.assertRaisesRegex(ValueError,'lost source controls'):
   source_table_html(soup.table,lambda n:n.get_text(strip=True))
if __name__=='__main__':unittest.main()
