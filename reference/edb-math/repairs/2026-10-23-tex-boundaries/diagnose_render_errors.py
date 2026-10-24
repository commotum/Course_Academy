import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
fs={(f['entity'],f['attribute']):f for f in json.loads((H/'fields.json').read_text())};cache={}
for line in (H/'render-checks.jsonl').open():
 r=json.loads(line);cache[r['entity'],r['attribute']]=r
rows=[fs[k] for k,v in cache.items() if v['after']['errors']]
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,timeout=15000);page=b.new_page();page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html') if r.request.url==origin+'/fixture' else r.continue_() if r.request.url.startswith(origin+'/') else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true');out=page.evaluate(r'''async rows=>{const out=[];for(const row of rows){const a=render(row.after);content.replaceChildren(a);await MathJax.typesetPromise([a]);const math=[...MathJax.startup.document.math].filter(m=>a.contains(m.typesetRoot)&&m.typesetRoot.querySelector('[data-mml-node="merror"]')).map(m=>m.math);out.push({entity:row.entity,attribute:row.attribute,math});MathJax.typesetClear([a])}return out}''',rows);b.close()
server.shutdown();(H/'math-error-items.json').write_text(json.dumps(out,indent=2)+'\n')
for r in out:print(r['entity'],r['attribute'],[x[:450] for x in r['math']])
