import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';items=[]
for record in json.loads((H/'generator-validation-records.json').read_text()):
 q=record['question'];items.extend([q[':question/problem'],q[':question/worked-solution']])
 for f in q[':question/answer-fields']:
  for a in f[':answer-field/choices']:
   v=a[':answer/value'];items.append('$'+v+'$'if a[':answer/type']==':answer.type/math'and not v.startswith('$')else v)
checks=[]
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page();page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready')
 for start in range(0,len(items),20):
  results=page.evaluate('''async items=>{let out=[];for(const value of items){MathJax.typesetClear([content]);content.replaceChildren(render(value));await MathJax.typesetPromise([content]);out.push({errors:[...content.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error')),raw:content.textContent.includes('$$')});}return out}''',items[start:start+20]);checks.extend(results)
 b.close()
server.shutdown();assert all(not c['errors']and not c['raw']for c in checks);(H/'generator-rendering.json').write_text(json.dumps({'passed':True,'items':len(items),'errors':0},indent=2)+'\n');print('Rendered',len(items),'generated content items without errors.')
