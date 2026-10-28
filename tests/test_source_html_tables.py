"""Source table roles, spans, nesting, math and widgets survive all import paths."""
import importlib.util,sys,unittest
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'scripts'),str(R/'scripts/question_capture')]
from import_historical_question_content import Renderer
from activities import html_to_markdown
from html_tables import source_table_html
SOURCE='''<table align="center" rules="all" border="1"><caption>Example</caption><tbody><tr bgcolor="#D6EAF8" align="center"><th scope="col" colspan="2">Values</th></tr><tr><td rowspan="2" style="border-right:none;text-align:right"><math><mi>x</mi><mo>&lt;</mo><mn>2</mn></math></td><td><b>Exact</b> <i>answer</i><ol type="i" start="2"><li>first</li></ol></td></tr><tr><td><table><tr><td>nested</td><td><math><mi>π</mi></math></td></tr></table></td></tr></tbody></table>'''
def shape(value):
 s=BeautifulSoup(value,'html.parser');return [(n.name,n.get('rowspan'),n.get('colspan'),n.get('scope'),n.get('data-cell-align'),n.get('data-fill'),n.get('data-border-right'))for n in s.select('table,tr,td,th')]
class SourceTableTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(headless=True);cls.page=cls.browser.new_page();cls.page.route('**/*',lambda r:r.abort())
 @classmethod
 def tearDownClass(cls):cls.browser.close();cls.p.stop()
 def values(self,html=SOURCE):
  self.page.set_content('<div id="fixture"><div class="questionWidget-text">'+html+'</div></div>');node=self.page.locator('#fixture');before=node.inner_html();out={}
  for name,path in [('dom','scripts/question_capture/dom.js'),('capture','capture/scripts/browser/extract.js')]:
   result=node.evaluate((R/path).read_text());self.assertEqual(result['errors'],[],name);self.assertEqual(node.inner_html(),before,name);out[name]=result['problem']
  renderer=Renderer(None);out['history']=renderer.render(BeautifulSoup(html,'html.parser').find('table'));self.assertEqual(renderer.errors,[])
  soup=BeautifulSoup(html,'html.parser')
  for math in list(soup.find_all('math')):
   tex=Renderer(None).m(math);replacement=BeautifulSoup('<mjx-container><annotation encoding="application/x-tex"></annotation></mjx-container>','html.parser');replacement.annotation.string=tex;math.replace_with(replacement)
  out['activities']=html_to_markdown(str(soup));return out
 def test_structure_math_and_lists(self):
  results=self.values();expected=shape(results['history'])
  for name,value in results.items():
   with self.subTest(importer=name):
    self.assertEqual(shape(value),expected);self.assertIn('$x<2$',value);self.assertRegex(value,r'\$(?:π|\\pi)\s*\$');self.assertIn('<strong>Exact</strong>',value);self.assertIn('<em>answer</em>',value);self.assertIn('<ol type="i" start="2">',value);self.assertIn('<caption>Example</caption>',value);self.assertEqual(value.count('class="source-table"'),2);self.assertNotIn('style=',value)
 def test_no_invented_headers_and_safe_text(self):
  for name,value in self.values('<table><tr><td>A &amp; B</td><td>3 &lt; 4</td></tr></table>').items():
   self.assertNotIn('<th',value,name);self.assertIn('A &amp; B',value);self.assertIn('3 &lt; 4',value)
 def test_literal_dollar_is_not_a_math_delimiter(self):
  for name,value in self.values('<table><tr><td>Price ($)</td><td>Number</td></tr><tr><td><math><mn>50</mn></math></td><td><math><mn>2</mn></math></td></tr></table>').items():
   self.assertIn(r'Price (\$)',value,name);self.assertIn('$50$',value,name)
 def test_widgets_and_assets_preserve_markers(self):
  renderer=Renderer(None);html='<table><tr><td><span class="freeResponseTextbox"><math><mn>2</mn></math></span></td></tr></table>';value=renderer.render(BeautifulSoup(html,'html.parser').find('table'),True);self.assertIn('{{field-1}}',value);self.assertEqual(renderer.fields[0]['correct_value'],'2')
  value=html_to_markdown('<table><tr><td><img src="images/diagram.png" alt="Graph"></td></tr></table>');self.assertIn('<img src="images/diagram.png" alt="Graph">',value)
 def test_unsupported_layout_fails(self):
  with self.assertRaisesRegex(ValueError,'Unsupported table layout'):source_table_html(BeautifulSoup('<table style="display:grid"><tr><td>x</td></tr></table>','html.parser').table,lambda n:'')
 def test_browser_helpers_are_identical(self):
  source=(R/'scripts/question_capture/table_html.js').read_text();function=source[source.index('function sourceHTMLTable'):].strip()
  for path in ['scripts/question_capture/dom.js','capture/scripts/browser/extract.js']:self.assertIn(function,(R/path).read_text())
 def test_live_matrix_editor_fields_keep_rowspan_positions(self):
  saved=R/'reference/mathacademy/question-capture-workers/linear/14043295/q-275522-before.json'
  import json
  source=json.loads(saved.read_text())['html']
  self.page.set_content('<div id="fixture">'+source+'</div>')
  for path in ['scripts/question_capture/dom.js','capture/scripts/browser/extract.js']:
   with self.subTest(extractor=path):
    result=self.page.locator('#fixture').evaluate((R/path).read_text())
    self.assertEqual(result['errors'],[])
    self.assertEqual([f['key']for f in result['fields']],['field-1','field-2','field-3','field-4'])
    table=BeautifulSoup(result['problem'],'html.parser').find('table')
    rows=table.find_all('tr');self.assertEqual(rows[0].find('td')['rowspan'],'2')
    self.assertEqual([td.get_text(strip=True)for td in rows[0].find_all('td',recursive=False)][2:4],['{{field-1}}','{{field-2}}'])
    self.assertEqual([td.get_text(strip=True)for td in rows[1].find_all('td',recursive=False)][1:3],['{{field-3}}','{{field-4}}'])
    for key in ['field-1','field-2','field-3','field-4']:self.assertEqual(result['problem'].count('{{'+key+'}}'),1)
if __name__=='__main__':unittest.main()
