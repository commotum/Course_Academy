"""Read-only local renderer screenshots and source-MathML preview."""
import sys,json,functools,http.server,threading
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(ROOT/'scripts'))
from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT,IMAGE_TYPES
D=Path(__file__).resolve().parent;E=json.loads((D/'entities.json').read_text());fields=json.loads((D/'fields.json').read_text())
fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
visual=D/'visual';visual.mkdir(exist_ok=True)
source=Path('/home/jake/Developer/MA/DATA/Lessons/1106/Source/1106.html');soup=BeautifulSoup(source.read_text(),'html.parser');source_node=soup.select_one('#question-42659');(visual/'source-question-42659-original.html').write_text(str(source_node))
for c in source_node.select('mjx-container'):
 m=c.select_one('mjx-assistive-mml math');c.replace_with(m if m else '')
for x in source_node.select('script,img,button,input'):x.decompose()
for x in source_node.select('[mathvariant=bold]'):x['style']='font-weight:700;font-style:normal'
source_preview='<!doctype html><meta charset="utf-8"><style>body{font:20px sans-serif;padding:24px;max-width:950px}math{font-size:24px}.questionWidget-choices{margin-top:30px}</style><h2>Original capture: q-42659 (underlying MathML)</h2>'+str(source_node)
(visual/'source-question-42659-mathml.html').write_text(source_preview)
try:
 with sync_playwright()as p:
  b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':1000})
  def route(r):
   u=urlsplit(r.request.url)
   if u.path=='/fixture':r.fulfill(body=fixture,content_type='text/html')
   elif u.path=='/source-preview':r.fulfill(body=source_preview,content_type='text/html')
   elif u.path=='/api/asset':
    path=image_path(parse_qs(u.query).get('path',[''])[0],DEFAULT_MATH_ROOT)
    if path:r.fulfill(body=path.read_bytes(),content_type=IMAGE_TYPES[path.suffix.lower()])
    else:r.fulfill(status=404,body='Unavailable')
   elif r.request.url.startswith(origin+'/'):r.continue_()
   else:r.abort()
  page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready')
  groups={
   'pseudo-tex-question-42659':[f for f in fields if f['entity']in [17592186097240,17592186095365,17592186095366,17592186095367,17592186095368,17592186095369]],
   'pseudo-tex-question-12212':[f for f in fields if f['entity']in [17592186094250,17592186094251,17592186094252,17592186094253,17592186094254]],
   'canonical-vector-fonts':[f for f in fields if f['entity']in [17592186096451,17592186096452]],
   'tutorial-repaired-arrows':[f for f in fields if f['entity']==17592186362404],
   'generated-signed-fractions':[f for f in fields if f['entity']in [17592186735419,17592186735252]],
  }
  for name,batch in groups.items():
   page.evaluate('''async fields=>{MathJax.typesetClear([content]);content.replaceChildren();for(const f of fields){const h=document.createElement('h3');h.textContent=f.entity+' '+f.attribute;content.append(h);content.append(render(f.bare_math?'$'+f.value+'$':f.value,'prose',f.fields||[]));}await MathJax.typesetPromise([content]);}''',batch)
   page.locator('body').screenshot(path=str(visual/(name+'.png')))
  page.goto(origin+'/source-preview');page.locator('body').screenshot(path=str(visual/'source-question-42659-mathml.png'));b.close()
finally:server.shutdown();server.server_close()
print('Saved six visual evidence PNGs')
