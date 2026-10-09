"""The original MA menu must stay open when replacing a selected formula."""
import copy,json,random,tempfile,unittest
from pathlib import Path
from playwright.sync_api import sync_playwright
from browser import CaptureBrowser,EXTRACT,click_select_frame
from capture import arguments
from core import Pacer

FIXTURE=Path(__file__).parent/'fixtures/laplace-select'
class LaplaceSelectTargetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(headless=True)
    @classmethod
    def tearDownClass(cls):cls.browser.close();cls.pw.stop()
    def setUp(self):
        self.page=self.browser.new_page();self.page.route('**/*',lambda r:r.abort());self.page.set_default_timeout(500)
        self.record=json.loads((FIXTURE/'record.json').read_text())
        self.page.set_content('''<style>
        .selectListFrame {display:inline-block;position:relative;padding:8px;border:1px solid gray;cursor:pointer;}
        .selectListOptions {position:absolute;visibility:hidden;background:white;}
        .selectListOption {padding:8px;min-width:180px;}
        mjx-container {display:inline-block;min-width:110px;min-height:28px;}
        </style><div id="step-q340719"></div>''')
        self.page.add_script_tag(content='''const Core={findLeft:n=>n.getBoundingClientRect().left+scrollX,findTop:n=>n.getBoundingClientRect().top+scrollY,getHeight:n=>n.getBoundingClientRect().height};''')
        self.page.add_script_tag(content=(FIXTURE/'select-list.js').read_text())
        # Initialize the actual saved choices using the site's unmodified widget.
        self.page.evaluate('''choices=>{
          const w=new SelectList(document.getElementById('step-q340719'),null,340719,
            {index:0,margin:{left:0,right:0,top:0,bottom:0},options:choices,selectedIndex:1});
          w.init();w.frame.style.width='180px';w.frame.style.height='44px';
          w.onSelect=()=>window.selections=(window.selections||0)+1;
          window.fixtureWidget=w;
        }''',[c['html'] for c in self.record['before']['fields'][0]['choices']])
        self.scope=self.page.locator('#step-q340719');self.frame=self.scope.locator('#selectListFrame-340719-0')
    def tearDown(self):self.page.close()
    def test_real_saved_choices_are_unchanged(self):
        item=json.loads((FIXTURE/'rejected.json').read_text());self.page.set_content(item['html'])
        captured=self.page.locator('#step-q340719').evaluate(EXTRACT)
        self.assertEqual(captured['errors'],[])
        self.assertEqual([(c['type'],c['value']) for c in captured['fields'][0]['choices']],[(c['type'],c['value']) for c in item['fields'][0]['choices']])
    def test_center_click_original_handler_immediately_hides_selected_formula_menu(self):
        self.frame.click()
        self.assertFalse(self.scope.locator('.selectListOptions').is_visible())
        self.assertEqual(self.page.evaluate('window.selections||0'),0)
    def test_retry_enters_correct_choice_using_original_mouse_handlers(self):
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work,'--event-min','0','--event-max','0','--timeout-ms','500'])
            b=CaptureBrowser(self.page,args,Pacer(args,random.Random(1)),None)
            b.enter(self.scope,self.record);b.verify_entered(self.scope,self.record)
            self.assertEqual(self.page.evaluate('window.fixtureWidget.getSelectedIndex()'),2)
            self.assertEqual(self.page.evaluate('window.selections'),1)
            self.assertEqual(self.record['before']['fields'][0]['submitted_option'],'2')
            self.assertTrue(self.record['wrong_submission_used'])
    def test_frame_covered_by_other_element_defers_without_click(self):
        self.page.evaluate('''()=>{const r=document.getElementById('selectListFrame-340719-0').getBoundingClientRect();const o=document.createElement('div');o.style.cssText=`position:fixed;left:${r.left}px;top:${r.top}px;width:${r.width}px;height:${r.height}px;background:gray;z-index:2000`;document.body.appendChild(o);}''')
        with self.assertRaisesRegex(ValueError,'no visible direct click target'):click_select_frame(self.frame)
        self.assertEqual(self.page.evaluate('window.selections||0'),0)
