import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
f=next(f for f in json.loads((H/'fields.json').read_text())if f['entity']==17592186314749 and f['attribute']=='question/problem');fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';report={}
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':850,'height':700});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
 for side in ['before','after']:
  report[side]=page.evaluate('''async value=>{MathJax.typesetClear([content]);const n=render(value);content.replaceChildren(n);await MathJax.typesetPromise([n]);const under=n.querySelector('[data-mml-node="munder"]');if(!under)return{under:false};const [base,condition]=[...under.children].map(n=>n.getBoundingClientRect());return{under:true,centerDifference:Math.abs(base.x+base.width/2-condition.x-condition.width/2),conditionTop:condition.top,baseBottom:base.bottom};}''',f[side]);page.locator('#content').screenshot(path=str(H/('target-'+side+'.png')))
 b.close()
server.shutdown();assert not report['before']['under'];assert report['after']['under']and report['after']['centerDifference']<2;report['passed']=True;(H/'target-geometry.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
