import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4];fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';fields=json.loads((H/'proposals.json').read_text());samples=json.loads((H/'generator-samples.json').read_text());fields += [{'entity':r['question'][':question/id'],'attribute':'generator/solution','after':r['question'][':question/worked-solution']}for r in samples];checks=[];screens=H/'screens';screens.mkdir(exist_ok=True)
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':950});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready')
 for i in range(0,len(fields),15):
  batch=fields[i:i+15];out=page.evaluate('''async fields=>{MathJax.typesetClear([content]);content.replaceChildren();for (const f of fields){let box=document.createElement('div');box.append(render(f.after,'prose'));content.append(box);}await MathJax.typesetPromise([content]);return [...content.children].map(n=>({errors:[...n.querySelectorAll('[data-mml-node="merror"]')].map(x=>x.getAttribute('data-mjx-error')),raw:n.textContent.includes('$$'),blue:n.querySelectorAll('svg [fill="#4169E1"]').length,red:n.querySelectorAll('svg [fill="red"]').length}));}''',batch)
  for f,v in zip(batch,out):assert not v['errors'] and not v['raw'],(f['entity'],v);checks.append({'entity':f['entity'],'attribute':f['attribute'],**v})
 for eid in [17592186602424,17592186642471]:
  f=next(f for f in fields if f['entity']==eid);page.evaluate('''async f=>{MathJax.typesetClear([content]);content.replaceChildren(render(f.after,'prose'));await MathJax.typesetPromise([content]);await document.fonts.ready;}''',f)
  for w in [1100,390]:
   page.set_viewport_size({'width':w,'height':950});page.locator('#content').screenshot(path=str(screens/(str(eid)+'-'+str(w)+'.png')))
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),(eid,w)
  page.set_viewport_size({'width':1100,'height':950})
 b.close()
server.shutdown();(H/'render-validation.json').write_text(json.dumps({'passed':True,'fields':len(checks),'checks':checks},indent=2)+'\n');print('Rendered',len(checks),'repaired/generated fields; flagged solutions checked at desktop and mobile.')
