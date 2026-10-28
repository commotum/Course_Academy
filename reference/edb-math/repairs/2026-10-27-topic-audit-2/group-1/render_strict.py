import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
fixture=fixture.replace('<script src="/ui/vendor/mathjax/tex-svg.js"></script>','<script>MathJax.tex.packages=MathJax.tex.packages.filter(x=>x!=="noundefined");</script><script src="/ui/vendor/mathjax/tex-svg.js"></script>')
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';items=json.loads((H/'items.json').read_text());out=[]
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':1000});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready')
 for i in range(0,len(items),100):
  out+=page.evaluate('''async(items)=>{let r=[];for(let[e,a,v,bare]of items){MathJax.typesetClear([content]);let n=render(bare?'$'+v+'$':v,'prose');content.replaceChildren(n);await MathJax.typesetPromise([n]);r.push({entity:e,attribute:a,errors:[...n.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error')),rawDelimiters:n.textContent.includes('$$')});}return r;}''',items[i:i+100]);print('additional rendered',len(out),flush=True)
 b.close()
server.shutdown();report={'content_items':len(out),'checks':out,'errors':[x for x in out if x['errors']or x['rawDelimiters']]};(H/'strict-rendering.json').write_text(json.dumps(report,indent=2));print('done errors',len(report['errors']))
