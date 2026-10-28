import functools,http.server,json,mimetypes,threading
from urllib.parse import urlparse,parse_qs
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4];MROOT=Path('/media/jake/SSD/EDB/math')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  u=urlparse(self.path)
  if u.path=='/api/asset':
   value=parse_qs(u.query).get('path',[''])[0];p=MROOT/value
   if not p.exists():p=R/value
   if p.is_file():
    self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(p.name)[0]or'application/octet-stream');self.end_headers();self.wfile.write(p.read_bytes());return
  return super().do_GET()
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
fixture+='''<script type="module">import {blankInput,mountInlineFields,loadMathInputs,checkboxControl,richSelect} from '/ui/question-fields.js';window.controls={blankInput,mountInlineFields,loadMathInputs,checkboxControl,richSelect};</script>'''
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';D=json.loads((H/'proposed.json').read_text());items=[];images={a[':db/id']for q in D['questions']for f in q.get(':question/answer-fields',[])for a in f.get(':answer-field/choices',[])if a[':answer/type'][':db/ident']==':answer.type/image'};out=[];interactions=[];screens=H/'proposed-screens';screens.mkdir(exist_ok=True)
for patch in json.loads((H/'duplicate-membership-proposals.json').read_text()):
 q=next(q for q in D['questions']if q[':db/id']==patch['entity']);q[':question/answer-fields']=[f for f in q[':question/answer-fields']if f[':db/id']in patch['after']]
changed={p['entity']for p in json.loads((H/'proposals.json').read_text())}|{p['entity']for p in json.loads((H/'duplicate-membership-proposals.json').read_text())}
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':1000});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready&&window.controls')
 for i in range(0,len(items),100):
  batch=[[e,a,'![]('+v+')'if e in images and a=='answer/value'else v,bare]for e,a,v,bare in items[i:i+100]]
  out+=page.evaluate('''async(items)=>{let rs=[];for(let[e,a,v,bare]of items){MathJax.typesetClear([content]);let n=render(bare?'$'+v+'$':v,'prose');content.replaceChildren(n);await MathJax.typesetPromise([n]);rs.push({entity:e,attribute:a,errors:[...n.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error')),rawDelimiters:n.textContent.includes('$$'),undefinedCommands:[...n.querySelectorAll('[data-mml-node="mtext"]')].map(x=>x.textContent).filter(x=>x.includes('\\\\')),images:n.querySelectorAll('img').length});}return rs;}''',batch);print('rendered',len(out),flush=True)
 (H/'proposed-rendering-values.json').write_text(json.dumps(out,indent=2))
 for q in D['questions']:
  if q.get(':question/math-academy-id')not in['q-132983','q-132779','q-133003']:continue
  fs=q.get(':question/answer-fields',[])
  if q[':db/id']not in changed:continue
  if not any(f[':answer-field/type'][':db/ident']in[':answer-field.type/blank',':answer-field.type/select',':answer-field.type/checkbox']for f in fs):continue
  fields=[]
  for f in fs:
   kind=f[':answer-field/type'][':db/ident'].split('/')[-1];a=f.get(':answer-field/correct');choices=[{'id':a[':db/id'],'type':a[':answer/type'][':db/ident'].split('/')[-1],'value':a[':answer/value']}for a in f.get(':answer-field/choices',[])];fields.append({'id':f[':db/id'],'key':f[':answer-field/key'],'type':kind,'answerType':a[':answer/type'][':db/ident'].split('/')[-1]if a else None,'choices':choices})
  result=page.evaluate('''async({v,fields})=>{await controls.loadMathInputs();MathJax.typesetClear([content]);let n=render(v,'prose',fields),list=document.createElement('div');content.replaceChildren(n,list);controls.mountInlineFields(n,list,fields,f=>{let x=document.createElement('fieldset');if(f.type==='blank')x.append(controls.blankInput(f,f.key,f.id));else if(f.type==='checkbox')x.append(controls.checkboxControl(f,key=>render(key,'prose')));else if(f.type==='select'){let s=document.createElement('select');s.name=String(f.id);let empty=document.createElement('option');empty.value='';empty.textContent='Select…';s.append(empty);for(let a of f.choices){let o=document.createElement('option');o.value=String(a.id);o.textContent=a.value;s.append(o);}x.append(controls.richSelect(s,f.choices,a=>render(a.type==='math'?'$'+a.value+'$':a.value,'prose'),a=>a.id,node=>MathJax.typesetPromise([node])));}return x;});await MathJax.typesetPromise([content]);await document.fonts.ready;let states=[];for(let label of content.querySelectorAll('label.choice')){let c=label.querySelector('input[type="checkbox"]'),h=label.querySelector('input[type="hidden"]');let before=h.value;c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}));states.push({name:c.name,unchecked:before,checked:h.value});}return{control_ids:[...content.querySelectorAll('math-field,input.answer-input,select,input[type="checkbox"]')].map(x=>x.getAttribute('name')),placements:[...n.querySelectorAll('.answer-inline')].map(x=>({fieldId:x.dataset.fieldId,key:x.closest('[data-field-key]')?.dataset.fieldKey})),checkboxes:states,unmounted:list.childElementCount,raw_fields:/\{\{[^}]+\}\}/.test(n.textContent),errors:[...content.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error'))};}''',{'v':q[':question/problem'],'fields':fields});result.update({'question':q[':db/id'],'source':q.get(':question/math-academy-id'),'expected_ids':[str(f['id'])for f in fields if f['type']in['blank','select','checkbox']]})
  page.set_viewport_size({'width':390,'height':900});page.locator('#content').screenshot(path=str(screens/f"mobile-{q[':db/id']}.png"));result['mobile_page_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1');page.set_viewport_size({'width':1100,'height':1000});interactions.append(result)
  if len(interactions)<=4 or q.get(':question/math-academy-id')in['q-334056','q-334554','q-317821','q-320435','q-50099']:page.locator('#content').screenshot(path=str(screens/f"question-{q[':db/id']}.png"))
 for c in []:
  if ':tutorial/content'not in c:continue
  page.evaluate('''async(v)=>{MathJax.typesetClear([content]);content.replaceChildren(render(v,'prose'));await MathJax.typesetPromise([content]);await document.fonts.ready;}''',c[':tutorial/content']);page.locator('#content').screenshot(path=str(screens/f"tutorial-{c[':db/id']}.png"))
 b.close()
server.shutdown();report={'content_items':len(out),'checks':out,'interactive':interactions,'errors':[x for x in out if x['errors']or x['rawDelimiters']or x.get('undefinedCommands')],'control_issues':[x for x in interactions if set(x['control_ids'])!=set(x['expected_ids'])or x['raw_fields']or x['errors']]};(H/'log-cloze-mobile-rendering.json').write_text(json.dumps(report,indent=2));print('done',len(out),'rendererrors',len(report['errors']),'interactive',len(interactions),'controlissues',len(report['control_issues']))
