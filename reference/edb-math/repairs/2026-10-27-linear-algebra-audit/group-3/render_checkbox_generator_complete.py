import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=Path.cwd();F=json.loads((H/'checkbox-generator-render-fields.json').read_text());fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';checks=[];screens=H/'screens';screens.mkdir(exist_ok=True)
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':950});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready')
 for n in range(0,len(F),80):
  batch=F[n:n+80];out=page.evaluate('''async fields=>{MathJax.typesetClear([content]);content.replaceChildren();for (const f of fields){let box=document.createElement('div');box.dataset.entity=f.entity;box.append(render(f.bare?'$'+f.value+'$':f.value,'prose'));content.append(box);}await MathJax.typesetPromise([content]);return [...content.children].map(n=>({errors:[...n.querySelectorAll('[data-mml-node="merror"]')].map(x=>x.getAttribute('data-mjx-error')),raw:n.textContent.includes('$$'),math:n.querySelectorAll('mjx-container').length}));}''',batch)
  for f,r in zip(batch,out):checks.append({'entity':f['entity'],'attribute':f['attribute'],**r})
  if n%800==0:print(n,flush=True)
 for f in [f for f in F if f['attribute']=='tutorial/content']:
  page.evaluate('''async f=>{MathJax.typesetClear([content]);content.replaceChildren(render(f.value,'prose'));await MathJax.typesetPromise([content]);await document.fonts.ready;}''',f);page.locator('#content').screenshot(path=str(screens/(str(f['entity'])+'.png')))
 b.close()
server.shutdown();(H/'checkbox-generator-complete-render-validation.json').write_text(json.dumps({'fields':len(checks),'errors':[r for r in checks if r['errors']or r['raw']],'checks':checks},indent=2));print('rendered',len(checks),'errors',sum(bool(r['errors']or r['raw'])for r in checks))
