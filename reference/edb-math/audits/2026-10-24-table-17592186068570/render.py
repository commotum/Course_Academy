"""Compare the original HTML table with the actual stored-table renderer."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
question=json.loads((H/'entity.json').read_text())[0][0];reports=[]
with sync_playwright()as p:
 browser=p.chromium.launch(headless=True,ignore_default_args=['--hide-scrollbars']);page=browser.new_page(viewport={'width':1100,'height':1000})
 page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html')if route.request.url==origin+'/fixture'else route.continue_()if route.request.url.startswith(origin+'/')else route.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
 for variant in ['source-html','stored-markdown']:
  page.evaluate('()=>{MathJax.typesetClear([content]);content.replaceChildren()}')
  if variant=='source-html':page.evaluate("html=>{let n=document.createElement('div');n.style.cssText='font-size:24px;line-height:1.8';n.innerHTML=html;content.append(n)}",(H/'original-table.html').read_text())
  else:page.evaluate("async text=>{let article=document.createElement('article');article.className='lesson-content';let card=document.createElement('div');card.className='content-card';card.append(render(text));article.append(card);content.append(article);await MathJax.typesetPromise([article])}",question[':question/worked-solution'])
  metrics=page.evaluate("()=>{let t=content.querySelector('table'),box=t.getBoundingClientRect();return {table:{width:box.width,display:getComputedStyle(t).display,marginLeft:getComputedStyle(t).marginLeft,marginRight:getComputedStyle(t).marginRight},cells:[...t.querySelectorAll('th,td')].map(c=>({tag:c.tagName,text:c.querySelector('mjx-assistive-mml math')?.textContent||c.querySelector('title')?.textContent||c.textContent,align:getComputedStyle(c).textAlign,background:getComputedStyle(c).backgroundColor,fontWeight:getComputedStyle(c).fontWeight})),mathErrors:content.querySelectorAll('[data-mjx-error],mjx-merror').length}}")
  reports.append({'variant':variant,**metrics});page.screenshot(path=str(H/f'{variant}.png'),full_page=True)
 browser.close()
server.shutdown();(H/'render-comparison.json').write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps(reports,indent=2))
