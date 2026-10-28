import functools,http.server,json,threading,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">');fixture+='''<script type="module">import {blankInput,mountInlineFields,loadMathInputs} from '/ui/question-fields.js';window.controls={blankInput,mountInlineFields,loadMathInputs};</script>'''
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';out=[]
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':950});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready&&window.controls')
 fields=json.loads((H/'proposed-fields.json').read_text());props=json.loads((H/'proposals.json').read_text())if(H/'proposals.json').exists()else[];changes={(x['entity'],x['attribute']):x['after']for x in props}
 for i,(e,a,v,ident,bare)in enumerate(fields):
  v=changes.get((e,a),v)
  r=page.evaluate(r'''async ({value,bare})=>{MathJax.typesetClear([content]);const n=render(bare?'$'+value+'$':value,'prose',[]);content.replaceChildren(n);await MathJax.typesetPromise([n]);return {errors:[...n.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error')),rawDollars:n.textContent.includes('$$'),quoteInMath:[...MathJax.startup.document.math].filter(m=>n.contains(m.typesetRoot)&&/(?:^|\n)\s*>/.test(m.math)).map(m=>m.math),tables:n.querySelectorAll('table').length,width:n.scrollWidth};}''',{'value':v,'bare':bare});r.update({'entity':e,'attribute':a,'identity':ident});out.append(r)
  if i%200==0:print(i,flush=True)
 (H/'proposed-rendering.json').write_text(json.dumps(out,indent=2)+'\n');b.close()
server.shutdown();print('rendered',len(out),'errors',sum(bool(r['errors'])or r['rawDollars']or bool(r['quoteInMath'])for r in out))
