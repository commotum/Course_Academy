"""Verify the original illustration and the retained equations in the player."""
import functools,http.server,json,threading
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3];asset='images/25/2594f99e0f02241dc6d01f85c82923103df1d6fb4dda5ca03d438637f5178a28.png';imagebytes=(Path('/media/jake/SSD/EDB/math')/asset).read_bytes()
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
fields=json.loads((H/'fields.json').read_text());fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';errors=[]
def route(r):
 url=r.request.url
 if '/api/asset' in url or '/images/' in url:print('Asset request',url,flush=True)
 if url==origin+'/fixture':r.fulfill(body=fixture,content_type='text/html')
 elif urlparse(url).path=='/api/asset'and parse_qs(urlparse(url).query).get('path')==[asset] or urlparse(url).path=='/'+asset:r.fulfill(body=imagebytes,content_type='image/png')
 elif url.startswith(origin+'/'):r.continue_()
 else:r.abort()
with sync_playwright()as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1050,'height':1300});page.on('pageerror',lambda e:errors.append(str(e)));page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready===true');check=page.evaluate('''async f=>{const out={entity:f.entity,attribute:f.attribute,before_sha256:f.before_sha256,after_sha256:f.after_sha256};for(const side of ['before','after']){MathJax.typesetClear([content]);const n=render(f[side]);content.replaceChildren(n);await MathJax.typesetPromise([n]);await Promise.all([...n.querySelectorAll('img')].map(async i=>{i.loading='eager';try{await i.decode()}catch(e){throw Error(JSON.stringify({src:i.src,complete:i.complete,width:i.naturalWidth,error:String(e)}))}}));out[side]={errors:[...n.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.textContent),images:[...n.querySelectorAll('img')].map(i=>({src:i.getAttribute('src'),width:i.naturalWidth,height:i.naturalHeight})),math:[...MathJax.startup.document.math].filter(m=>n.contains(m.typesetRoot)).map(m=>m.math)};}return out;}''',fields[0]);page.locator('#content').screenshot(path=str(H/'after.png'));page.locator('#content img').screenshot(path=str(H/'restored-diagram.png'));browser.close()
server.shutdown();assert not errors and not check['before']['errors']and not check['after']['errors'];assert not check['before']['images']and len(check['after']['images'])==1;assert check['after']['images'][0]['width']>0;assert[len(check['before']['math'])-len(check['after']['math'])]==[1];assert[m for m in check['before']['math']if'downdiagonalstrike'not in m]==check['after']['math'];check['passed']=True;report={'passed':True,'fields':1,'checks':[check],'other_math_unchanged':True,'source_image_decoded':True};(H/'render-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('Source illustration rendered; all other math unchanged; zero MathJax errors')
