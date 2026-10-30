import functools,http.server,json,sys,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path.cwd();sys.path.insert(0,str(R/'scripts'));from check_math_rendering import Quiet
D=Path(__file__).resolve().parent;fields=json.loads((D/'render-input.json').read_text());fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">');server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}'
try:
 with sync_playwright()as p:
  b=p.chromium.launch();page=b.new_page(viewport={'width':1000,'height':1200});page.route(url+'/fixture',lambda r:r.fulfill(body=fixture,content_type='text/html'));page.goto(url+'/fixture');page.wait_for_function('window.ready')
  for eid in [17592186125118,17592186272021,17592186272284]:
   f=next(f for f in fields if f['entity']==eid);out=page.evaluate('''async f=>{MathJax.typesetClear([content]);content.replaceChildren(render(f.value,'prose',f.fields||[]));await MathJax.typesetPromise([content]);const info=n=>({type:n.getAttribute('data-mml-node'),cls:n.getAttribute('data-mjx-texclass'),height:n.getBoundingClientRect().height,html:n.getAttribute('data-mml-node')==='mo'?n.outerHTML.slice(0,400):null,codes:[...n.querySelectorAll('[data-c]')].map(x=>x.getAttribute('data-c')).slice(0,12)});return [...content.querySelectorAll('[data-mml-node="mtable"]')].map(t=>({table:info(t),parent:info(t.parentElement),siblings:[...t.parentElement.children].map(info)}));}''',f);(D/(str(eid)+'-dom.json')).write_text(json.dumps(out,indent=2)+'\n');page.locator('#content').screenshot(path=str(D/(str(eid)+'-after.png')));print(eid,json.dumps(out[:3]))
  b.close()
finally:server.shutdown();server.server_close()
