import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';items=json.loads((H/'additional-render-items.json').read_text());out=[]
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':1000});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready')
 for i in range(0,len(items),100):
  out+=page.evaluate('''async(items)=>{let r=[];for(let[e,a,v,bare]of items){MathJax.typesetClear([content]);let n=render(bare?'$'+v+'$':v,'prose');content.replaceChildren(n);await MathJax.typesetPromise([n]);r.push({entity:e,attribute:a,errors:[...n.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error')),rawDelimiters:n.textContent.includes('$$')});}return r;}''',items[i:i+100]);print('additional rendered',len(out),flush=True)
 for p in json.loads((H/'proposals.json').read_text()):
  if p['entity']not in [17592186097841,17592186116500,17592186121044,17592186121064,17592186134396,17592186342133]:continue
  page.evaluate('''async(v)=>{MathJax.typesetClear([content]);content.replaceChildren(render(v,'prose'));await MathJax.typesetPromise([content]);await document.fonts.ready;}''',p['after']);page.locator('#content').screenshot(path=str(H/'screens'/f"proposed-{p['entity']}-{p['attribute'].split('/')[-1]}.png"))
 (H/'additional-rendering.json').write_text(json.dumps({'content_items':len(out),'checks':out,'errors':[x for x in out if x['errors']or x['rawDelimiters']]},indent=2))
 # Display archived source steps with their retained SVG/MathJax styles.
 for ma,tid in [(1772,3236),(1731,3169),(1048,3155)]:
  raw=Path('/home/jake/Developer/MA/DATA/Lessons')/str(ma)/'Source'/f'{ma}.html';meta=json.loads(raw.with_suffix('.json').read_text());item=next(i for i in meta['lesson']['items']if str(i.get('content_id'))==str(tid));page.route('**/source-'+str(ma),lambda route,request,path=raw:route.fulfill(body=path.read_text(),content_type='text/html'));page.goto(origin+'/source-'+str(ma));page.evaluate('''id=>{let n=document.getElementById(id);for(let p=n;p;p=p.parentElement){p.style.display='block';p.style.visibility='visible';p.style.position='static';p.style.height='auto';p.style.width='100%';}n.style.padding='20px';}''',item['dom_id']);page.locator('#'+item['dom_id']).screenshot(path=str(H/'screens'/f'source-{ma}-tutorial-{tid}.png'))
 b.close()
server.shutdown();report={'content_items':len(out),'checks':out,'errors':[x for x in out if x['errors']or x['rawDelimiters']]};(H/'additional-rendering.json').write_text(json.dumps(report,indent=2));print('done errors',len(report['errors']))
