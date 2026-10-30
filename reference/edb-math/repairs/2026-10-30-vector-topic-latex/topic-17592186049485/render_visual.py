import sys,json,http.server,functools,threading
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT/'scripts'))
from playwright.sync_api import sync_playwright
from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT,IMAGE_TYPES
HERE=Path(__file__).resolve().parent
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
fixture=fixture.replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
items=json.loads((HERE/'render-input.json').read_text());out=HERE/'visual';out.mkdir(exist_ok=True)
groups={
 'introduction':[f for f in items if f['entity']==17592186107157],
 'arrows-and-norm':[f for f in items if f['entity']==17592186105465],
 'canonical-segment':[f for f in items if f['entity']==17592186105466],
 'broken-segment':[f for f in items if f['entity']==17592186106065],
 'segment-problem-solution':[f for f in items if f['entity']==17592186281398],
 'segment-tutorial':[f for f in items if f['entity']==17592186107159],
 'matrix-line':[f for f in items if f['entity']==17592186106293],
}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1100,'height':1000},device_scale_factor=1)
 def route(r):
  u=urlsplit(r.request.url)
  if r.request.url==origin+'/fixture':r.fulfill(body=fixture,content_type='text/html')
  elif u.path=='/api/asset':
   path=image_path(parse_qs(u.query).get('path',[''])[0],DEFAULT_MATH_ROOT)
   if path:r.fulfill(body=path.read_bytes(),content_type=IMAGE_TYPES[path.suffix.lower()])
   else:r.fulfill(status=404,body='Unavailable')
  elif r.request.url.startswith(origin+'/'):r.continue_()
  else:r.abort()
 page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready')
 for name,fields in groups.items():
  page.evaluate('''async fields=>{MathJax.typesetClear([content]);content.replaceChildren();for(const f of fields){let h=document.createElement('p');h.textContent=f.entity+' '+f.attribute;content.append(h);content.append(render(f.bare_math?'$'+f.value+'$':f.value,'prose',[]));}await MathJax.typesetPromise([content]);}''',fields)
  page.screenshot(path=str(out/(name+'.png')),full_page=True)
 browser.close()
server.shutdown();server.server_close()
(out/'manifest.json').write_text(json.dumps({k:[{'entity':f['entity'],'attribute':f['attribute']} for f in v] for k,v in groups.items()},indent=2))
