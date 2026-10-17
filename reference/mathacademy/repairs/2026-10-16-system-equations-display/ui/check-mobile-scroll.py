"""Verify long equation labels remain accessible in current UI's scroll container."""
import functools,http.server,json,threading
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];OUT=HERE/'preview'
files={}
for eid in [17592186529306,17592186505001,17592186508249,17592186097842]:
 path=OUT/f'{eid}-after-mobile.html';s=BeautifulSoup(path.read_text(),'html.parser')
 for script in s.select('script'):script.decompose()
 files[f'/{eid}']=str(s).encode()
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  if self.path in files:
   body=files[self.path];self.send_response(200);self.send_header('Content-Type','text/html');self.end_headers();self.wfile.write(body)
  else:super().do_GET()
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
results=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome')
  page=browser.new_page(viewport={'width':390,'height':844})
  for route in files:
   page.goto(f'http://127.0.0.1:{server.server_port}'+route,wait_until='networkidle')
   result=page.evaluate('''()=>({bodyOverflow:document.body.scrollWidth>innerWidth+2,containers:[...document.querySelectorAll('mjx-container')].filter(n=>n.scrollWidth>n.clientWidth+2).map(n=>{const start=n.scrollLeft;n.scrollLeft=n.scrollWidth;return {display:n.getAttribute('display'),clientWidth:n.clientWidth,scrollWidth:n.scrollWidth,overflowX:getComputedStyle(n).overflowX,initialScrollLeft:start,finalScrollLeft:n.scrollLeft,scrollable:n.scrollLeft>start};})})''')
   result['entity']=int(route[1:]);results.append(result)
   if result['entity']==17592186505001:page.screenshot(path=str(OUT/'17592186505001-after-mobile-scroll-right.png'),full_page=True)
  browser.close()
finally:server.shutdown();server.server_close()
report={'passed':all(not r['bodyOverflow'] and all(c['scrollable'] and c['overflowX']=='auto' for c in r['containers']) for r in results),'method':'Saved full-player rendered DOM and unchanged current learning.css at 390px; no content or UI modifications.','results':results}
(OUT/'mobile-scroll-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert report['passed']
