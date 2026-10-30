"""Read-only before/after proof using actual player CSS/Markdown/MathJax."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path.cwd();D=Path(__file__).resolve().parent
q=json.loads((D/'question.json').read_text());before=q[':question/worked-solution'];after=before.replace(r'[\begin{array}',r'\left[\begin{array}').replace(r'\end{array}]',r'\end{array}\right]');assert after.count(r'\left[')-before.count(r'\left[')==2
(D/'preview.json').write_text(json.dumps({'before':before,'after':after,'database_writes':0},indent=2)+'\n')
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();fixture=fixture.replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">');fixture=fixture.replace('<script src="/ui/vendor/mathjax/tex-svg.js">','<script>MathJax.tex.packages=MathJax.tex.packages.filter(name=>name!=="noundefined");</script><script src="/ui/vendor/mathjax/tex-svg.js">')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';out=[]
try:
 with sync_playwright()as p:
  browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':760,'height':1100});page.route(origin+'/fixture',lambda r:r.fulfill(body=fixture,content_type='text/html'));page.goto(origin+'/fixture');page.wait_for_function('window.ready')
  for label,text in [('before',before),('after',after)]:
   result=page.evaluate('''async text=>{MathJax.typesetClear([content]);content.replaceChildren(render(text,'prose'));await MathJax.typesetPromise([content]);const metrics=[];for(const t of content.querySelectorAll('[data-mml-node="mtable"]')){const parent=t.parentElement;const fences=[...parent.children].filter(e=>e.getAttribute('data-mml-node')==='mo'&&['[',']'].includes(e.getAttribute('data-mjx-texclass')||e.textContent)||e.getAttribute('data-mml-node')==='mo'&&e.querySelector('[data-c="5B"],[data-c="5D"]'));if(fences.length>=2)metrics.push({tableHeight:t.getBoundingClientRect().height,fenceHeights:fences.map(e=>e.getBoundingClientRect().height)});}return {errors:[...content.querySelectorAll('[data-mml-node="merror"]')].map(e=>e.textContent),metrics};}''',text)
   page.locator('#content').screenshot(path=str(D/(label+'.png')));out.append({'variant':label,**result})
  browser.close()
finally:server.shutdown();server.server_close()
assert all(not r['errors']for r in out);(D/'render-proof.json').write_text(json.dumps({'same_player_same_CSS':True,'only_change':'Two plain array bracket pairs replaced with scalable left/right delimiters','variants':out,'database_writes':0},indent=2)+'\n');print(json.dumps(out))
