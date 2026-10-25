"""Verify all imported prompts, solutions, answer feedback and instructions."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def main():
 entities=json.loads((H/'entities.json').read_text());cases=[]
 for e in entities:
  for a in [':question/problem',':question/worked-solution',':answer/value',':answer/feedback',':tutorial/content']:
   if a in e:cases.append({'id':e[':db/id'],'attribute':a,'text':e[a]})
 fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';errors=[]
 with sync_playwright()as p:
  b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':900});page.on('pageerror',lambda e:errors.append(str(e)));page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true');results=page.evaluate('''async cases=>{let out=[];for(let c of cases){MathJax.typesetClear([content]);const n=render(c.text);content.replaceChildren(n);await MathJax.typesetPromise([n]);out.push({id:c.id,attribute:c.attribute,errors:[...n.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(x=>x.textContent),math:n.querySelectorAll('mjx-container').length,tableCount:n.querySelectorAll('table').length})}return out}''',cases);b.close()
 server.shutdown();report={'passed':not errors and all(not r['errors']for r in results),'questions':sum(':question/id'in e for e in entities),'rendered_fields':len(results),'page_errors':errors,'cases':results};(H/'render-verification.json').write_text(json.dumps(report,indent=2)+'\n');assert report['passed'];print('Rendered',len(results),'fields across',report['questions'],'questions without errors')
if __name__=='__main__':main()
