"""Read-only reproduction using stored questions and the current quiz renderer."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
records=[r[0] for r in json.loads((H/'reported-entities.json').read_text())]
records.append({':db/id':'synthetic-wide',':question/answer-fields':[],':question/problem':'<div class="matrix-operands"><div>$A=\\begin{bmatrix}'+ ' & '.join(map(str,range(100,130)))+r'\end{bmatrix}$</div></div>'})
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
variants={'current':'','overflow-y-hidden':'.prose .matrix-operands > div { overflow-y: hidden; }','svg-block':'.prose .matrix-operands > div > mjx-container > svg { display: block; }','math-inline-block':'.prose .matrix-operands > div > mjx-container { display: inline-block; }','no-per-operand-scroll':'.prose .matrix-operands > div { overflow: visible; }','line-height-zero':'.prose .matrix-operands > div > mjx-container {line-height:0;}','no-assistive-layout-experiment':'.prose .matrix-operands mjx-assistive-mml { display:none !important; }','bounded-assistive':'.prose .matrix-operands mjx-assistive-mml {width:1px !important;height:1px !important;}','vertical-padding':'.prose .matrix-operands > div {padding-block:2px;}'}
measure=r'''()=>[...document.querySelectorAll('.matrix-operands > div')].map(n=>{const box=e=>{let c=getComputedStyle(e),r=e.getBoundingClientRect();return {tag:e.tagName,clientWidth:e.clientWidth,scrollWidth:e.scrollWidth,clientHeight:e.clientHeight,scrollHeight:e.scrollHeight,width:r.width,height:r.height,top:r.top,bottom:r.bottom,left:r.left,right:r.right,display:c.display,overflowX:c.overflowX,overflowY:c.overflowY,verticalAlign:c.verticalAlign,lineHeight:c.lineHeight}};n.scrollTop=100;n.scrollLeft=100;let scrolled={x:n.scrollLeft,y:n.scrollTop};n.scrollTop=n.scrollLeft=0;return {wrapper:box(n),math:box(n.querySelector('mjx-container')),svg:box(n.querySelector('svg')),scrolled}})'''
reports=[];errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,ignore_default_args=['--hide-scrollbars']);page=browser.new_page(viewport={'width':1100,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)))
 page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
 page.evaluate("()=>{let s=document.createElement('style');s.id='experiment';document.head.append(s)}")
 for width in [1100,768,390]:
  page.set_viewport_size({'width':width,'height':1000})
  for record in records:
   page.evaluate("async r=>{MathJax.typesetClear([content]);const card=document.createElement('article');card.className='content-card';card.append(render(r[':question/problem'],'prose',r[':question/answer-fields'].map(f=>({key:f[':answer-field/key']}))));content.replaceChildren(card);await MathJax.typesetPromise([card])}",record)
   for variant,css in variants.items():
    page.evaluate("css=>document.querySelector('#experiment').textContent=css",css)
    metrics=page.evaluate(measure);reports.append({'entity':record[':db/id'],'viewport_width':width,'variant':variant,'operands':metrics})
    if width==1100 and record[':db/id']!='synthetic-wide' and variant in ['current','line-height-zero','no-assistive-layout-experiment','bounded-assistive']:
     deep=page.evaluate("()=>[...document.querySelectorAll('.matrix-operands > div')].map(n=>({html:n.innerHTML,descendants:[...n.querySelectorAll('mjx-assistive-mml, math')].map(e=>({tag:e.tagName,css:e.style.cssText,computed:Object.fromEntries(['display','position','height','width','clip','overflow','top','left','padding','margin'].map(k=>[k,getComputedStyle(e)[k]])),rect:e.getBoundingClientRect().toJSON()}))}))")
     (H/f"{record[':db/id']}-{variant}-dom-details.json").write_text(json.dumps(deep,indent=2)+'\n')
    if width==1100 and record[':db/id']!='synthetic-wide' and variant in ['current','svg-block','no-per-operand-scroll','line-height-zero','bounded-assistive']:page.locator('.content-card').screenshot(path=str(H/f"{record[':db/id']}-{variant}.png"))
   page.evaluate("()=>document.querySelector('#experiment').textContent=''")
 browser.close()
server.shutdown();(H/'layout-measurements.json').write_text(json.dumps({'page_errors':errors,'cases':reports},indent=2)+'\n')
for r in reports:
 if r['viewport_width']==1100:print(r['entity'],r['variant'],[(o['wrapper']['clientWidth'],o['wrapper']['scrollWidth'],o['wrapper']['clientHeight'],o['wrapper']['scrollHeight'],o['scrolled']) for o in r['operands']])
assert not errors,errors
actual=[r for r in reports if r['entity']!='synthetic-wide' and r['variant']=='line-height-zero']
assert all(o['wrapper']['scrollHeight']==o['wrapper']['clientHeight'] and o['scrolled']=={'x':0,'y':0} for r in actual for o in r['operands'])
wide=[r for r in reports if r['entity']=='synthetic-wide' and r['variant']=='line-height-zero']
assert all(o['scrolled']['x']>0 and o['scrolled']['y']==0 for r in wide for o in r['operands'])
