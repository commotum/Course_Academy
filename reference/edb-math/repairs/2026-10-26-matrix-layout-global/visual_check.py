import functools,http.server,json,re,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
blocks=json.loads((H/'blocks.json').read_text());selected=[]
for name,fence,n,m in [('2x2 determinant','|',2,2),('3x3 determinant','|',3,3),('2x2 matrix','[',2,2),('column vector','[',3,1)]:
 b=next(x for x in blocks if x['old'][0]==fence and len(x['rows'])==n and all(len(row)==m for row in x['rows'])and re.fullmatch(r'[\d\s+.,-]+',''.join(c for row in x['rows']for c in row)))
 selected.append({'name':name,**b})
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1050,'height':1000});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true');report=page.evaluate('''async rows=>{content.style.display='grid';content.style.gridTemplateColumns='1fr 1fr';content.style.gap='18px';let out=[];for(const r of rows){for(const side of ['old','new']){const box=document.createElement('section');box.style.padding='15px';box.style.border='1px solid #ccc';const title=document.createElement('p');title.textContent=r.name+' — '+(side==='old'?'before':'after');box.append(title,render('$$'+r[side]+'$$'));content.append(box);await MathJax.typesetPromise([box]);const row=box.querySelector('[data-mml-node="mtr"]');let gap=null;if(row&&row.children.length>1){const a=row.children[0].getBoundingClientRect(),b=row.children[1].getBoundingClientRect();gap=b.left-a.right;}out.push({entity:r.e,name:r.name,side,columnGap:gap,errors:box.querySelectorAll('[data-mml-node="merror"]').length});}}return out}''',selected);page.locator('#content').screenshot(path=str(H/'matrix-layout-before-after.png'));b.close()
server.shutdown();assert all(not r['errors']for r in report)
for i in range(0,len(report),2):
 old,new=report[i:i+2]
 if old['columnGap']is not None:assert new['columnGap']>old['columnGap']+5,(old,new)
(H/'visual-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
