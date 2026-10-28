import functools,http.server,json,threading,re
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4];D=json.loads((H/'current.json').read_text());P=json.loads((H/'proposals.json').read_text());Q={q[':db/id']:q for q in D['questions']};shapes={m['entity']:m['shape']for m in json.loads((H/'math-verification.json').read_text())if'entity'in m};screens=H/'screens';screens.mkdir(exist_ok=True)
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">');fixture+='''<script type="module">import {blankInput,mountInlineFields,loadMathInputs} from '/ui/question-fields.js';window.controls={blankInput,mountInlineFields,loadMathInputs};</script>'''
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';checks=[]
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':1000});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready&&window.controls')
 for change in P:
  e=change['entity'];grid='matrix-answer-brackets'in change['after'];tutorial=change['attribute']=='tutorial/content';chosen=e in [17592186120294,17592186120357,17592186120427,17592186292858,17592186292860,17592186365507,17592186295065,17592186116501,17592186116496,17592186121037]
  if not(grid or tutorial or chosen):continue
  q=Q.get(e,{});fields=[{'id':f[':db/id'],'key':f[':answer-field/key'],'type':'blank','answerType':'math'}for f in q.get(':question/answer-fields',[])if f[':answer-field/type'][':db/ident']==':answer-field.type/blank']
  result=page.evaluate(r'''async({value,fields})=>{await controls.loadMathInputs();MathJax.typesetClear([content]);const n=render(value,'prose',fields),outside=document.createElement('div');content.replaceChildren(n,outside);if(fields.length)controls.mountInlineFields(n,outside,fields,f=>{let d=document.createElement('fieldset');d.append(controls.blankInput(f,f.key,f.id));return d});await MathJax.typesetPromise([n]);await document.fonts.ready;return{errors:[...n.querySelectorAll('[data-mml-node="merror"]')].length,rows:[...n.querySelectorAll('.matrix-answer tr')].map(tr=>[...tr.querySelectorAll('td')].map(c=>({key:c.querySelector('[data-field-key]')?.dataset.fieldKey||c.dataset.fieldKey||null,id:c.querySelector('math-field')?.getAttribute('name')||null,x:c.getBoundingClientRect().x}))),outside:outside.childElementCount,controls:[...n.querySelectorAll('math-field')].map(x=>x.name)}}''',{'value':change['after'],'fields':fields});assert not result['errors']
  if grid:
   shape=shapes[e];assert len(result['rows'])==shape[0]and all(len(row)==shape[1]for row in result['rows']),(e,result,shape);assert result['outside']==0,(e,result)
   actual={c['id']for row in result['rows']for c in row if c['id']};assert actual=={str(f['id'])for f in fields},(e,result,fields)
   for j in range(shape[1]):assert max(row[j]['x']for row in result['rows'])-min(row[j]['x']for row in result['rows'])<1
  if chosen or tutorial:page.locator('#content').screenshot(path=str(screens/f'{e}-{change["attribute"].replace("/","-")}-after.png'))
  if chosen:
   page.evaluate('''async value=>{MathJax.typesetClear([content]);content.replaceChildren(render(value,'prose',[]));await MathJax.typesetPromise([content]);}''',change['before']);page.locator('#content').screenshot(path=str(screens/f'{e}-{change["attribute"].replace("/","-")}-before.png'))
  checks.append({'entity':e,'attribute':change['attribute'],'interactive':grid,'result':result})
 b.close()
server.shutdown();(H/'visual-verification.json').write_text(json.dumps(checks,indent=2)+'\n');print('visual checks',len(checks),'interactive grids',sum(c['interactive']for c in checks))
