import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
fields=json.loads((H/'fields.json').read_text());fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
with sync_playwright()as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1050,'height':1300});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true');report=page.evaluate('''async f=>{const n=render(f.after);content.replaceChildren(n);await MathJax.typesetPromise([n]);return {entity:f.entity,attribute:f.attribute,before_sha256:f.before_sha256,after_sha256:f.after_sha256,errors:[...n.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.textContent),images:n.querySelectorAll('img').length,math:[...MathJax.startup.document.math].map(m=>m.math),diagonals:n.querySelectorAll('[data-mml-node="menclose"]').length};}''',fields[0]);page.locator('#content').screenshot(path=str(H/'after.png'));page.locator('mjx-container[display="true"]').last.screenshot(path=str(H/'diagram.png'));browser.close()
server.shutdown();assert not report['errors']and report['images']==0 and report['diagonals']==2,report;report['passed']=True;(H/'render-verification.json').write_text(json.dumps({'passed':True,'fields':1,'checks':[report]},indent=2)+'\n');print('Native LaTeX verified: no image, two diagonal strokes, zero MathJax errors')
