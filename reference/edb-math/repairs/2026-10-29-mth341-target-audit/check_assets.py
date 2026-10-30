"""Decode all scoped images through the player's asset resolution and CSS."""
import functools,http.server,json,sys,threading
from pathlib import Path
from urllib.parse import parse_qs,urlsplit
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT,IMAGE_TYPES
rows=json.loads((H/'assets/inventory.json').read_text())['records'];unique={r['resolved']:r for r in rows};checks=[]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
fixture='<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><main class="lesson-main"><article class="content-card"><div id="content" class="prose"></div></article></main>'
try:
 with sync_playwright()as p:
  browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1000,'height':950})
  def route(r):
   u=urlsplit(r.request.url)
   if u.path=='/fixture':r.fulfill(body=fixture,content_type='text/html')
   elif u.path=='/api/asset':
    local=image_path(parse_qs(u.query).get('path',[''])[0],DEFAULT_MATH_ROOT)
    if local:r.fulfill(body=local.read_bytes(),content_type=IMAGE_TYPES[local.suffix.lower()])
    else:r.fulfill(status=404,body='Unavailable')
   elif r.request.url.startswith(origin+'/'):r.continue_()
   else:r.abort()
  page.route('**/*',route);page.goto(origin+'/fixture')
  for width in[1000,390]:
   page.set_viewport_size({'width':width,'height':950})
   for row in unique.values():
    value=page.evaluate('''async path=>{content.replaceChildren();const img=new Image();img.src='/api/asset?path='+encodeURIComponent(path);content.append(img);try{await img.decode()}catch(e){return {error:String(e)}}await document.fonts.ready;const r=img.getBoundingClientRect();return {naturalWidth:img.naturalWidth,naturalHeight:img.naturalHeight,renderWidth:r.width,renderHeight:r.height,overflow:content.scrollWidth>content.clientWidth+1}}''',row['resolved']);checks.append({'viewport':width,'reference':row['reference'],'entity':row['entity'],**value})
  browser.close()
finally:server.shutdown();server.server_close()
failures=[c for c in checks if c.get('error')or not c.get('naturalWidth')or not c.get('naturalHeight')or c.get('overflow')];report={'passed':not failures,'unique_images':len(unique),'checks':checks,'failures':failures,'database_writes':0};(H/'assets/render-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('Images:',len(unique),'; decode/viewport checks:',len(checks),'; failures:',len(failures));assert report['passed']
