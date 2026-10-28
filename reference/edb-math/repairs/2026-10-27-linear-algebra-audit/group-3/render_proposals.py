import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=Path.cwd();D=json.loads((H/'snapshot.json').read_text());Q={q[':db/id']:q for q in D['questions']};P=json.loads((H/'proposals.json').read_text())+json.loads((H/'completion-solutions.json').read_text());fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">');fixture+='''<script type="module">import {blankInput,mountInlineFields,loadMathInputs} from '/ui/question-fields.js';window.controls={blankInput,mountInlineFields,loadMathInputs};</script>'''
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';checks=[];screens=H/'proposed-screens';screens.mkdir(exist_ok=True)
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':950});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready&&window.controls')
 for f in P:
  fs=Q.get(f['entity'],{}).get(':question/answer-fields',[]);fields=[{'id':v[':db/id'],'key':v[':answer-field/key'],'type':'blank','answerType':'math'}for v in fs if v[':answer-field/type'][':db/id']==17592186045492]if f['attribute']=='question/problem'else[]
  if not fields and fs and f['attribute']=='question/problem':
   # Enum lookup is authoritative for blank rather than a hardcoded ID.
   idents=dict(json.loads((H/'idents.json').read_text()));fields=[{'id':v[':db/id'],'key':v[':answer-field/key'],'type':'blank','answerType':'math'}for v in fs if idents[v[':answer-field/type'][':db/id']]==':answer-field.type/blank']
  result=page.evaluate('''async ({value,fields})=>{await controls.loadMathInputs();MathJax.typesetClear([content]);const n=render(value,'prose',fields||[]),list=document.createElement('div');content.replaceChildren(n,list);if(fields?.length)controls.mountInlineFields(n,list,fields,f=>{let x=document.createElement('fieldset');x.append(controls.blankInput(f,f.key,f.id));return x;});await MathJax.typesetPromise([n]);await document.fonts.ready;return {errors:[...n.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error')),raw:n.textContent.includes('$$'),fields:[...n.querySelectorAll('[data-field-key]')].map(c=>({key:c.dataset.fieldKey,id:c.querySelector('math-field')?.getAttribute('name')})),outside:list.childElementCount,matrices:[...n.querySelectorAll('.matrix-answer')].map(m=>[...m.querySelectorAll('tr')].map(tr=>tr.children.length))};}''',{'value':f['after'],'fields':fields})
  result.update({'entity':f['entity'],'attribute':f['attribute']});assert not result['errors']and not result['raw'],result
  if fields:assert not result['outside']and {x['key']:x['id']for x in result['fields']}=={x['key']:str(x['id'])for x in fields},(f['entity'],result)
  page.locator('#content').screenshot(path=str(screens/(str(f['entity'])+'-'+f['attribute'].split('/')[-1]+'.png')))
  if fields:
   page.set_viewport_size({'width':390,'height':900});result['mobile_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1');page.set_viewport_size({'width':1100,'height':950})
  checks.append(result)
 b.close()
server.shutdown();(H/'proposed-render-validation.json').write_text(json.dumps({'fields':len(checks),'checks':checks},indent=2));print('proposed rendered',len(checks),'controls',sum(bool(x['fields'])for x in checks),'overflow',[x['entity']for x in checks if x.get('mobile_overflow')])
