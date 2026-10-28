import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">');fixture+='''<script type="module">import {mountInlineFields,richSelect} from '/ui/question-fields.js';window.controls={mountInlineFields,richSelect};</script>''';server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';D=json.loads((H/'current.json').read_text());ids=[17592186147766,17592186147769,17592186299693,17592186299852,17592186645710,17592186645758];out=[]
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':390,'height':900});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready&&window.controls')
 for q in D['questions']:
  if q[':db/id']not in ids:continue
  fields=[{'id':f[':db/id'],'key':f[':answer-field/key'],'type':'select','choices':[{'id':a[':db/id'],'type':a[':answer/type'][':db/ident'].split('/')[-1],'value':a[':answer/value']}for a in f[':answer-field/choices']]}for f in q[':question/answer-fields']]
  page.evaluate('''async({v,fields})=>{MathJax.typesetClear([content]);let n=render(v,'prose',fields),list=document.createElement('div');content.replaceChildren(n,list);controls.mountInlineFields(n,list,fields,f=>{let set=document.createElement('fieldset'),s=document.createElement('select');s.name=String(f.id);let empty=document.createElement('option');empty.value='';empty.textContent='Select…';s.append(empty);for(let a of f.choices){let o=document.createElement('option');o.value=String(a.id);o.textContent=a.value;s.append(o);}set.append(controls.richSelect(s,f.choices,a=>render(a.type==='math'?'$'+a.value+'$':a.value,'prose'),a=>a.id,node=>MathJax.typesetPromise([node])));return set;});await MathJax.typesetPromise([content]);await document.fonts.ready;}''',{'v':q[':question/problem'],'fields':fields})
  def measure(state):return page.evaluate('''state=>({state,overflow:document.documentElement.scrollWidth>innerWidth+1,viewport:innerWidth,scrollWidth:document.documentElement.scrollWidth,outside:[...content.querySelectorAll('*')].filter(n=>{let r=n.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+1||r.left< -1)}).map(n=>({tag:n.tagName,cls:n.getAttribute('class'),left:n.getBoundingClientRect().left,right:n.getBoundingClientRect().right,text:n.textContent.slice(0,80)})).slice(0,20)})''',state)
  states=[measure('closed-unselected')];page.locator('#content').screenshot(path=str(H/'screens'/f"select-{q[':db/id']}-unselected.png"))
  for i in range(len(fields)):
   trigger=page.locator('.answer-select-trigger').nth(i);trigger.click();page.wait_for_timeout(25);states.append(measure('opened-field-'+str(i)));page.locator('#content').screenshot(path=str(H/'screens'/f"select-{q[':db/id']}-open-{i}.png"));page.locator('.answer-select-menu').nth(i).locator('[role=option]').first.click();page.wait_for_timeout(25);states.append(measure('selected-field-'+str(i)))
  out.append({'question':q[':db/id'],'source':q.get(':question/math-academy-id'),'states':states})
 b.close()
server.shutdown();(H/'rich-select-rendering.json').write_text(json.dumps(out,indent=2));print([(x['source'],[(s['state'],s['scrollWidth'])for s in x['states']if s['overflow']])for x in out])
