"""Production table sanitization, theme fills and responsive keyboard access."""
import functools,http.server,threading,unittest
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
HTML='''<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><script src="/ui/vendor/dompurify/purify.min.js"></script><main class="lesson-main"><article class="lesson-content"><div id="content" class="content-card"></div></article></main><script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {romanLists} from '/ui/prose-lists.js';import {inlinePrompt} from '/ui/question-fields.js';import {protectMath} from '/ui/math-protection.js';import {decorateSourceTables} from '/ui/content-tables.js';
const el=(t,c)=>{const n=document.createElement(t);if(c)n.className=c;return n};window.renderers={};
for(const name of ['learning','assignments','activity']){const source=await(await fetch('/ui/'+name+'.js')).text();let code=source.slice(source.indexOf('function escapeHTML('),source.indexOf('function answerValue('));if(name==='learning'){let start=source.indexOf('function fieldLabel(');code=source.slice(start,source.indexOf('\\n}',start)+2)+';'+code}renderers[name]=new Function('el','marked','romanLists','inlinePrompt','protectMath','decorateSourceTables',code+';return markdown')(el,marked,romanLists,inlinePrompt,protectMath,decorateSourceTables)}window.ready=true;
</script>'''
class TableBrowserTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=cls.server.serve_forever,daemon=True).start();cls.origin=f'http://127.0.0.1:{cls.server.server_port}';cls.p=sync_playwright().start();cls.browser=cls.p.chromium.launch(headless=True);cls.page=cls.browser.new_page(viewport={'width':1100,'height':900});cls.errors=[];cls.page.on('pageerror',lambda e:cls.errors.append(str(e)));cls.page.route('**/*',lambda r:r.fulfill(body=HTML,content_type='text/html')if r.request.url==cls.origin+'/fixture'else r.continue_()if r.request.url.startswith(cls.origin+'/')else r.abort());cls.page.goto(cls.origin+'/fixture');cls.page.wait_for_function('window.ready===true')
 @classmethod
 def tearDownClass(cls):cls.browser.close();cls.p.stop();cls.server.shutdown()
 def test_all_renderers_sanitize_and_apply_source_attributes(self):
  for name in ['learning','assignments','activity']:
   for theme in ['light','dark']:
    with self.subTest(renderer=name,theme=theme):
     result=self.page.evaluate('''({name,theme})=>{document.documentElement.dataset.theme=theme;let n=renderers[name]('<div class="source-table-scroll"><table class="source-table" data-rules="all" data-table-align="center"><tr><td data-fill="#D6EAF8" data-cell-align="center" data-border-right="none" style="position:fixed;background:red" onclick="alert(1)">Value</td><td data-fill="url(https://example.invalid/image)">2</td></tr></table></div>');let cell=n.querySelector('td');let detached=cell.style.getPropertyValue('--table-fill-light');content.replaceChildren(n);const s=getComputedStyle(cell);return {detached,align:s.textAlign,border:s.borderRightWidth,fill:s.backgroundColor,color:s.color,position:s.position,handler:cell.getAttribute('onclick'),badFill:n.querySelectorAll('td')[1].style.length}}''',{'name':name,'theme':theme});self.assertTrue(result['detached']);self.assertEqual(result['align'],'center');self.assertEqual(result['border'],'0px');self.assertEqual(result['position'],'static');self.assertIsNone(result['handler']);self.assertEqual(result['badFill'],0)
  self.assertFalse(self.errors)
 def test_keyboard_region_tracks_actual_overflow_after_resize(self):
  self.page.set_viewport_size({'width':1100,'height':900});self.page.evaluate('''()=>{let n=renderers.learning('<div class="source-table-scroll"><table class="source-table" data-rules="none"><tr><td>'+('W'.repeat(65))+'</td></tr></table></div>');content.replaceChildren(n)}''');self.page.wait_for_timeout(60);self.assertIsNone(self.page.locator('.source-table-scroll').get_attribute('tabindex'));self.page.set_viewport_size({'width':390,'height':900});self.page.wait_for_function("document.querySelector('.source-table-scroll').tabIndex===0");self.assertEqual(self.page.locator('.source-table-scroll').get_attribute('role'),'region');self.assertFalse(self.page.evaluate('document.documentElement.scrollWidth>innerWidth+1'));self.page.set_viewport_size({'width':1100,'height':900});self.page.wait_for_function("!document.querySelector('.source-table-scroll').hasAttribute('tabindex')")
if __name__=='__main__':unittest.main()
