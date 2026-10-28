import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=Path.cwd();D=json.loads((H/'snapshot.json').read_text());banks={f[':db/id']:f for q in D['questions']for f in q.get(':question/answer-fields',[])};C=json.loads((H/'checkbox-labels-current.json').read_text());P=json.loads((H/'checkbox-label-proposals.json').read_text());fields=[]
for f in C['labels']:
 fields.append({'entity':f['entity'],'question':f['question'],'attribute':'answer-field/key','value':f['value'],'phase':'current'})
for p in P:fields.append({'entity':p['entity'],'question':next(f['question']for f in C['labels']if f['entity']==p['entity']),'attribute':'answer-field/key','value':p['after'],'phase':'proposed'})
for f in fields:
 f['choices']=[{'id':a[':db/id'],'entityId':a[':db/id'],'type':'text','value':a[':answer/value']}for a in banks[f['entity']][':answer-field/choices']];f['false_id']=str(next(a['id']for a in f['choices']if a['value']=='false'))
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">');fixture+='''<script type="module">import {checkboxControl} from '/ui/question-fields.js';window.checkboxControl=checkboxControl;</script>'''
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';checks=[];screens=H/'checkbox-label-screens';screens.mkdir(exist_ok=True)
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':950});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready&&!!window.checkboxControl')
 def render(batch):
  return page.evaluate('''async fields=>{MathJax.typesetClear([content]);content.replaceChildren();for(const f of fields){const box=document.createElement('div');box.dataset.entity=f.entity;const row=checkboxControl({id:f.entity,type:'checkbox',key:f.value,choices:f.choices},label=>render(label,'answer-value'));box.append(row);content.append(box);}await MathJax.typesetPromise([content]);await document.fonts.ready;return [...content.children].map(n=>({entity:Number(n.dataset.entity),errors:[...n.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error')),raw:n.textContent.includes('$$'),math:n.querySelectorAll('mjx-container').length,checkboxName:n.querySelector('input[type="checkbox"]').name,encoded:n.querySelector('.answer-choice-value').value}));}''',batch)
 for n in range(0,len(fields),60):
  batch=fields[n:n+60];rs=render(batch)
  for f,r in zip(batch,rs):
   assert not r['errors']and not r['raw']and r['checkboxName']==str(f['entity'])and r['encoded']==f['false_id'],r;checks.append({**r,'phase':f['phase'],'question':f['question']})
 # Compare actual controls before and after for every changed statement.
 for phase in ('current','proposed'):
  chosen=[f for f in fields if f['phase']==phase and f['entity']in {p['entity']for p in P}];render(chosen);page.locator('#content').screenshot(path=str(screens/(phase+'.png')))
 b.close()
server.shutdown();(H/'checkbox-label-render-validation.json').write_text(json.dumps({'basis_t':C['basis_t'],'passed':True,'current_labels':len(C['labels']),'proposed_labels':len(P),'rendered_controls':len(checks),'checks':checks},indent=2));print('actual checkbox controls',len(checks),'current',len(C['labels']),'proposed',len(P),'all pass')
