import functools,http.server,json,mimetypes,sys,threading
from pathlib import Path
from urllib.parse import parse_qs,urlsplit
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT
D=H/'assets';report=json.loads((D/'inventory.json').read_text());refs={r['resolved']:r for r in report['records']if r['available']};items=list(refs.values());fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';checks=[];screens=D/'screens';screens.mkdir(exist_ok=True)
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':900})
 def route(r):
  u=urlsplit(r.request.url)
  if r.request.url==origin+'/fixture':r.fulfill(body=fixture,content_type='text/html')
  elif u.path=='/api/asset':
   path=image_path(parse_qs(u.query).get('path',[''])[0],DEFAULT_MATH_ROOT)
   if path:r.fulfill(body=path.read_bytes(),content_type=mimetypes.guess_type(path)[0]or'application/octet-stream')
   else:r.fulfill(status=404,body='Unavailable')
  elif r.request.url.startswith(origin+'/'):r.continue_()
  else:r.abort()
 page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready')
 for width in [1100,390]:
  page.set_viewport_size({'width':width,'height':900})
  for offset in range(0,len(items),25):
   batch=items[offset:offset+25]
   out=page.evaluate('''async items=>{content.replaceChildren();let imgs=[];for (let item of items){let card=render('![Retained source visual](<'+item.resolved+'>)','prose');content.append(card);let img=card.querySelector('img');if(img){img.loading='eager';imgs.push(img);}else imgs.push(null);}return await Promise.all(imgs.map(async img=>{let error=null;try{await img.decode();}catch(e){error=String(e);}return {loaded:!!img?.naturalWidth,naturalWidth:img?.naturalWidth,naturalHeight:img?.naturalHeight,width:img?.getBoundingClientRect().width,error,overflow:!!img&&img.getBoundingClientRect().width>innerWidth+1};}));}''',batch)
   for item,result in zip(batch,out):checks.append({'path':item['resolved'],'viewport':width,**result})
   if offset==0:page.locator('#content').screenshot(path=str(screens/('first-'+str(width)+'.png')))
 b.close()
server.shutdown();bad=[x for x in checks if not x['loaded']or x['overflow']];(D/'render-validation.json').write_text(json.dumps({'unique_files':len(items),'checks':checks,'failures':bad,'passed':not bad},indent=2)+'\n');print('Decoded/rendered',len(items),'assets in desktop/mobile:',len(checks),'checks,',len(bad),'failures')
assert not bad,bad
