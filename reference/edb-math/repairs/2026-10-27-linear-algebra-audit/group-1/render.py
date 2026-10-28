import functools,http.server,json,threading,collections
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
fixture+='''<script type="module">import {blankInput,mountInlineFields,loadMathInputs} from '/ui/question-fields.js';window.controls={blankInput,mountInlineFields,loadMathInputs};</script>'''
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
D=json.loads((H/'current.json').read_text());items=json.loads((H/'items.json').read_text());out=[];interactions=[];screens=H/'screens';screens.mkdir(exist_ok=True)
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':1000});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready&&window.controls')
 for i in range(0,len(items),100):
  batch=items[i:i+100]
  result=page.evaluate('''async (items)=>{let results=[];for(let[e,a,v,bare]of items){MathJax.typesetClear([content]);let node=render(bare?'$'+v+'$':v,'prose');content.replaceChildren(node);await MathJax.typesetPromise([node]);results.push({entity:e,attribute:a,errors:[...node.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error')),mathItems:[...MathJax.startup.document.math].filter(m=>node.contains(m.typesetRoot)).length,rawDelimiters:node.textContent.includes('$$'),text:node.textContent.slice(0,150),overflow:node.scrollWidth>1100});}return results;}''',batch)
  out+=result;print('rendered',len(out),flush=True)
  (H/'rendering-progress.json').write_text(json.dumps(out,indent=2))
 for c in D['contents']:
  if ':tutorial/content'not in c:continue
  page.evaluate('''async(v)=>{MathJax.typesetClear([content]);content.replaceChildren(render(v,'prose'));await MathJax.typesetPromise([content]);await document.fonts.ready;}''',c[':tutorial/content']);page.locator('#content').screenshot(path=str(screens/f"tutorial-{c[':db/id']}.png"))
 for q in D['questions']:
  fs=q.get(':question/answer-fields',[])
  if not any(f[':answer-field/type'][':db/ident']==':answer-field.type/blank'for f in fs):continue
  fields=[{'id':f[':db/id'],'key':f[':answer-field/key'],'type':'blank','answerType':'math'}for f in fs];ptext=q[':question/problem']
  r=page.evaluate('''async({v,fields})=>{await controls.loadMathInputs();MathJax.typesetClear([content]);let n=render(v,'prose',fields),list=document.createElement('div');content.replaceChildren(n,list);controls.mountInlineFields(n,list,fields,f=>{let x=document.createElement('fieldset');x.append(controls.blankInput(f,f.key,f.id));return x;});await MathJax.typesetPromise([n]);await document.fonts.ready;return{inputs:[...content.querySelectorAll('math-field')].map(x=>({id:x.getAttribute('name')})),rows:[...n.querySelectorAll('.matrix-answer tr')].map(tr=>[...tr.querySelectorAll('[data-field-key]')].map(c=>({key:c.dataset.fieldKey,id:c.querySelector('math-field')?.getAttribute('name'),x:c.getBoundingClientRect().x}))),outside:list.childElementCount};}''',{'v':ptext,'fields':fields});r['entity']=q[':db/id'];r['expected_field_ids']=[f['id']for f in fields]
  page.set_viewport_size({'width':390,'height':900});r['mobile_page_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1');page.set_viewport_size({'width':1100,'height':1000});interactions.append(r)
  if len(interactions)<=5 or 'matrix-answer'in ptext:page.locator('#content').screenshot(path=str(screens/f"question-{q[':db/id']}.png"))
 b.close()
server.shutdown();(H/'rendering.json').write_text(json.dumps({'content_items':len(out),'checks':out,'interactive':interactions,'errors':[x for x in out if x['errors']or x['rawDelimiters']]},indent=2));print('done',len(out),'issues',sum(bool(x['errors']or x['rawDelimiters'])for x in out),'interactive',len(interactions))
