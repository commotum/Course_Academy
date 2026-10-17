"""Render all audited fields through the application's actual Markdown and MathJax."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
fields=json.loads((HERE/'fields.json').read_text())
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def translate_path(self,path):
  if path.startswith('/images/'):return str(Path('/media/jake/SSD/EDB/math')/path.lstrip('/'))
  return super().translate_path(path)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
html=(HERE/'render-fixture.html').read_text()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path="/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome");page=browser.new_page(viewport={'width':1060,'height':1100});errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('**/*',lambda route:route.fulfill(body=html,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort())
  page.goto(origin+'/fixture');page.wait_for_function('window.ready===true',timeout=20000)
  result=[]
  for start in range(0,len(fields),100):
   records=[{'entity':f['entity'],'attribute':f['attribute'],'value':('$'+f['value']+'$') if f['kind']=='math' else f['value']} for f in fields[start:start+100]]
   result.extend(page.evaluate('''async records=>{const results=[];
    for(const record of records){
     MathJax.typesetClear();content.replaceChildren();const article=document.createElement('article');article.append(render(record.value));content.append(article);
     await MathJax.typesetPromise([article]);let tables=[];
     for(const item of MathJax.startup.document.math)item.root.walkTree(n=>{if(n.kind==='mtable')tables.push({rows:n.childNodes.length,columns:n.childNodes[0]?.childNodes.length,alignment:n.attributes.get('columnalign')});});
     results.push({entity:record.entity,attribute:record.attribute,tables,mathCount:article.querySelectorAll('mjx-container').length,codeBlocks:[...article.querySelectorAll('pre')].map(n=>n.textContent),errors:[...article.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),undefinedMacros:[...article.querySelectorAll('[data-mjx-error], [data-mml-node="mtext"][fill="red"]')].map(n=>n.textContent)});
    }return results;}''',records))
   (HERE/'rendering.json').write_text(json.dumps({'fields':result,'page_errors':errors},indent=2))
   print('Rendered',len(result),'fields',flush=True)
  selected=[17592186566216,17592186566219,17592186124903,17592186125757,17592186124791,17592186074030,17592186100741]
  for eid in selected:
   fs=[f for f in fields if f['entity']==eid]
   awaitable=page.evaluate('''async fs=>{MathJax.typesetClear();content.replaceChildren();for(const f of fs){let a=document.createElement('article');a.append(Object.assign(document.createElement('h3'),{textContent:f.attribute}),render(f.value));content.append(a);}await MathJax.typesetPromise([content]);}''',fs)
   page.screenshot(path=str(HERE/f'entity-{eid}.png'),full_page=True)
  browser.close()
finally:server.shutdown();server.server_close()
print('Finished',len(result),'fields; errors',sum(bool(r['errors']) for r in result),'code blocks',sum(bool(r['codeBlocks']) for r in result))
