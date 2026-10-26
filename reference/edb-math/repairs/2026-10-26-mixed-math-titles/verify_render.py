"""Validate repaired fields through the actual player; never writes EDB."""
import functools,http.server,json,sys,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def main(folder):
 fields=json.loads((folder/'fields.json').read_text());fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';errors=[];reports=[]
 with sync_playwright()as p:
  b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)));page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
  for offset in range(0,len(fields),20):
   checked=page.evaluate('''async fields=>{let out=[];for(const f of fields){const result={entity:f.entity,attribute:f.attribute,before_sha256:f.before_sha256,after_sha256:f.after_sha256};for(const side of ['before','after']){MathJax.typesetClear([content]);let n=render(f[side]);content.replaceChildren(n);await MathJax.typesetPromise([n]);result[side]={errors:[...n.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),images:[...n.querySelectorAll('img')].map(n=>n.getAttribute('src')),math:[...MathJax.startup.document.math].filter(m=>n.contains(m.typesetRoot)).map(m=>m.math)};}result.passed=result.after.errors.every(e=>result.before.errors.includes(e))&&JSON.stringify(result.before.images)===JSON.stringify(result.after.images);out.push(result)}return out}''',fields[offset:offset+20]);reports.extend(checked)
   if len(fields)==1:page.locator('#content').screenshot(path=str(folder/'after.png'))
  b.close()
 server.shutdown();report={'passed':not errors and all(r['passed']for r in reports),'fields':len(fields),'page_errors':errors,'checks':reports};(folder/'render-verification.json').write_text(json.dumps(report,indent=2)+'\n');assert report['passed'];print('Player rendering verified',len(fields),'fields')
if __name__=='__main__':main(Path(sys.argv[1]))
