import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4];items=json.loads((H/'render-input.json').read_text());chosen=[(17592186121063,'tutorial/content'),(17592186153353,'tutorial/content'),(17592186184065,'question/worked-solution'),(17592186351545,'question/worked-solution'),(17592186270666,'answer/value')];fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">');(H/'screens').mkdir(exist_ok=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
try:
 with sync_playwright()as p:
  b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':1800});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready')
  for e,a in chosen:
   item=next(x for x in items if x['entity']==e and x['attribute']==a);page.evaluate('''async x=>{MathJax.typesetClear([content]);content.replaceChildren(render(x.bare_math?'$'+x.value+'$':x.value,'prose',[]));await MathJax.typesetPromise([content]);}''',item);page.locator('#content').screenshot(path=str(H/'screens'/f'{e}.png'))
  b.close()
finally:server.shutdown();server.server_close()
print('Screenshots',len(chosen))
