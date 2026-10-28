import functools,http.server,json,threading,re,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=Path.cwd();tutorial=json.loads((H/'tutorial-3170-original.json').read_text());fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">');fixture+='''<script type="module">import {protectMath} from '/ui/math-protection.js';window.protectMath=protectMath;</script>'''
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';out=[];screens=H/'aligned-guard-screens';screens.mkdir(exist_ok=True)
cases=[{'name':'minimal-visible-brackets','value':r'$$\begin{aligned}[A\,|\,I_3]&=B\end{aligned}$$','visible':True},{'name':'whitespace-visible-brackets','value':r'$$\begin{aligned} [ A\,|\,I_3]&=B\end{aligned}$$','visible':True}]+[{'name':'genuine-option-'+k,'value':r'$$\begin{aligned}['+k+r']x&=1\\y&=2\end{aligned}$$','option':k}for k in 'tbc']+[{'name':'tutorial-3170-original','value':tutorial[':tutorial/content'],'visible':True}]
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':950});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready&&!!window.protectMath')
 for case in cases:
  r=page.evaluate('''async value=>{MathJax.typesetClear([content]);content.replaceChildren(render(value,'prose'));await MathJax.typesetPromise([content]);await document.fonts.ready;return {protected:protectMath(value,x=>x),errors:[...content.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error')),math:[...MathJax.startup.document.math].filter(m=>content.contains(m.typesetRoot)).map(m=>({input:m.math,root:m.root.toString(),alignment:(function find(n){if(n.kind==='mtable')return n.attributes.get('align');for(const c of n.childNodes||[]){const a=find(c);if(a!==undefined)return a;}})(m.root)})),svgText:[...content.querySelectorAll('svg [data-c]')].map(n=>n.getAttribute('data-c')),bars:[...content.querySelectorAll('svg [data-c="7C"]')].length};}''',case['value']);r['name']=case['name'];r['screenshot']=str(screens/(case['name']+'.png'));assert not r['errors'],r
  if case.get('visible'):
   assert r'\begin{aligned}{}['in r['protected']or r'\begin{aligned} {}['in r['protected'],r
   target=next(x for x in r['math']if r'\begin{aligned}'in x['input']);assert all(x in target['root']for x in ('mo([)','mi(A)','mi(I)','mo(])')),target
   assert '|'in target['root']and'I'in target['root'],target
   assert r['bars']>=1,r
  if 'option'in case:
   assert r['protected']==case['value'],r
   assert r'\begin{aligned}['+case['option']+']'in r['math'][0]['input'],r
   assert 'mi('+case['option']+')'not in r['math'][0]['root'],r
   assert r['math'][0]['alignment'],r
  page.locator('#content').screenshot(path=r['screenshot']);out.append(r)
 # Demonstrate the original MathJax behavior independently of the UI protection.
 raw=page.evaluate(r'''async()=>{const tex=String.raw`\begin{aligned}[A\,|\,I_3]&=B\end{aligned}`;const n=await MathJax.tex2svgPromise(tex,{display:true});content.replaceChildren(n);return {tex,text:n.outerHTML,visibleGlyphs:[...n.querySelectorAll('[data-c]')].map(n=>n.getAttribute('data-c'))};}''');page.locator('#content').screenshot(path=str(screens/'unguarded-MathJax.png'));assert '1D434'not in raw['visibleGlyphs']and'1D43C'not in raw['visibleGlyphs'],raw
 b.close()
server.shutdown();report={'passed':True,'actual_ui_module':'ui/math-protection.js','ui_guard_sha256':hashlib.sha256((R/'ui/math-protection.js').read_bytes()).hexdigest(),'mathjax':'ui/vendor/mathjax/tex-svg.js','tutorial_entity':tutorial[':db/id'],'tutorial_source_id':3170,'cases':out,'unguarded_mathjax':raw,'group3_stored_pattern_hits':json.loads((H/'aligned-leading-bracket-membership.json').read_text())};(H/'aligned-guard-regression.json').write_text(json.dumps(report,indent=2));print('guard cases passed',len(out),'group3hits',len(report['group3_stored_pattern_hits']))
