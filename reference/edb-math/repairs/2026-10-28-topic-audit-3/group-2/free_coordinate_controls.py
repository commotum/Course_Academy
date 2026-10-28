import json,functools,http.server,threading,sys
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT,IMAGE_TYPES
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">');fixture=fixture.replace('<script src="/ui/vendor/mathjax/tex-svg.js">','<script>MathJax.tex.packages=MathJax.tex.packages.filter(x=>x!=="noundefined");</script><script src="/ui/vendor/mathjax/tex-svg.js">');fixture+='''<script type="module">import * as c from '/ui/question-fields.js';window.controls=c;await c.loadMathInputs();window.controlReady=true;</script>'''
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
D=json.loads((H/'free-coordinate-prospective.json').read_text());targets=[q for q in D if q[':db/id']==17592186365398];targets.append(next(q for q in D if any(f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox'for f in q.get(':question/answer-fields',[]))))
records=[]
for q in targets:
 fields=[]
 for f in q[':question/answer-fields']:
  right=f.get(':answer-field/correct');fields.append({'id':str(f[':db/id']),'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].lstrip(':'),'answerType':right[':answer/type'][':db/ident'].lstrip(':')if right else'answer.type/math','correctAnswer':{'id':right[':answer/id'],'type':right[':answer/type'][':db/ident'].lstrip(':'),'value':right[':answer/value']}if right else None,'choices':[{'id':a[':answer/id'],'type':a[':answer/type'][':db/ident'].lstrip(':'),'value':a[':answer/value']}for a in f.get(':answer-field/choices',[])]})
 records.append({'id':q[':db/id'],'identity':q.get(':question/math-academy-id'),'problem':q[':question/problem'],'fields':fields})
out=[]
with sync_playwright()as p:
 browser=p.chromium.launch(headless=True)
 for width in[1100,390]:
  page=browser.new_page(viewport={'width':width,'height':950})
  def route(r):
   u=urlsplit(r.request.url)
   if r.request.url==origin+'/fixture':r.fulfill(body=fixture,content_type='text/html')
   elif u.path=='/api/asset':
    path=image_path(parse_qs(u.query).get('path',[''])[0],DEFAULT_MATH_ROOT)
    if path:r.fulfill(body=path.read_bytes(),content_type=IMAGE_TYPES[path.suffix.lower()])
    else:r.fulfill(status=404,body='Unavailable')
   elif r.request.url.startswith(origin+'/'):r.continue_()
   else:r.abort()
  page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready&&window.controlReady')
  for q in records:
   result=page.evaluate(r'''async q=>{
     MathJax.typesetClear([content]);const form=document.createElement('form');form.addEventListener('submit',e=>e.preventDefault());
     const prompt=render(q.problem,'prose',q.fields),list=document.createElement('div');form.className='lesson-main';list.className='answer-fields';form.append(prompt,list);content.replaceChildren(form);
     function make(f){const host=document.createElement('fieldset');host.dataset.field=f.id;host.className='answer-field';host.dataset.type=f.type.split('/').at(-1);
       const kind=f.type.split('/').at(-1);
       if(kind==='select') {const select=document.createElement('select');select.name=f.id;select.setAttribute('aria-label',f.key);let opt=document.createElement('option');opt.value='';select.append(opt);for(const a of f.choices){let o=document.createElement('option');o.value=a.id;o.textContent=a.value;select.append(o)}host.append(controls.richSelect(select,f.choices,a=>render(a.type.endsWith('/math')?'$'+a.value+'$':a.value,'prose'),a=>a.id,n=>MathJax.typesetPromise([n])));}
       else if(kind==='blank')host.append(controls.blankInput(f,f.key,f.id));
       else if(kind==='radio'){for(const a of f.choices){const label=document.createElement('label');label.className='choice';const input=document.createElement('input');input.type='radio';input.name=f.id;input.value=a.id;label.append(controls.choiceIndicator(input),render(a.type.endsWith('/math')?'$'+a.value+'$':a.type.endsWith('/image')?'![]('+a.value+')':a.value,'prose'));host.append(label)}}
       else if(kind==='checkbox')host.append(controls.checkboxControl(f,k=>render(k,'prose')));
       return host;}
     controls.mountInlineFields(prompt,list,q.fields,make);await MathJax.typesetPromise([form]);
     const before=[...form.querySelectorAll('math-field')].map(n=>({name:n.getAttribute('name'),blank:n.value==='',tag:n.tagName}));
     for(const f of q.fields){const kind=f.type.split('/').at(-1);const input=[...form.querySelectorAll('input,select,math-field')].find(n=>n.name===f.id||n.getAttribute('name')===f.id);
       if(kind==='blank'){input.value=f.correctAnswer.value;input.dispatchEvent(new Event('input',{bubbles:true}));}
       if(kind==='select'){const wrapper=input.closest('.answer-dropdown');wrapper.querySelector('.answer-select-trigger').click();wrapper.querySelectorAll('.answer-select-option')[f.choices.findIndex(a=>a.id===f.correctAnswer.id)].click();}}
     await MathJax.typesetPromise([form]);
     const boxes=[...form.querySelectorAll('input[type=checkbox]')];const toggles=[];
     for(const box of boxes){let hidden=box.closest('label').querySelector('input[type=hidden]');const before=hidden.value;box.checked=!box.checked;box.dispatchEvent(new Event('change',{bubbles:true}));toggles.push({before,after:hidden.value,changed:before!==hidden.value});}
     return {errors:[...form.querySelectorAll('[data-mml-node=merror]')].map(n=>n.textContent),beforeMathInputs:before,
       locations:[...form.querySelectorAll('[data-field-key]')].map(n=>({key:n.dataset.fieldKey,controls:n.querySelectorAll('select,math-field,input:not([type=hidden])').length})),
       selects:[...form.querySelectorAll('select')].map(n=>({id:n.name,value:n.value,options:n.options.length})),checkboxToggles:toggles,
       mathInputs:[...form.querySelectorAll('math-field')].map(n=>({id:n.name,value:n.value})),
       rawMarkers:/\{\{field-/.test(form.textContent),bodyOverflow:document.documentElement.scrollWidth>innerWidth+1,
       images:[...form.querySelectorAll('img')].map(n=>({src:n.getAttribute('src'),loaded:n.complete&&n.naturalWidth>0})),tables:form.querySelectorAll('table').length};}''',q)
   page.wait_for_timeout(150)
   if q['id']in[17592186235496,17592186637312]:
    field=page.locator('math-field').first;field.evaluate('(n)=>{n.value=""}');field.click();pieces=['(x-3)','^','2','ArrowRight','+y','^','2','ArrowRight','=9']if q['id']==17592186235496 else['(x-0)','^','2','ArrowRight','+(y-6)','^','2','ArrowRight','=36']
    before_width=field.evaluate('(n)=>n.getBoundingClientRect().width')
    for piece in pieces:
     if piece in['ArrowRight','^']:field.press(piece)
     else:field.press_sequentially(piece)
    page.wait_for_timeout(180)
    result['actualKeyboardTyping']=field.evaluate('''n=>({value:n.value,width:n.getBoundingClientRect().width,scrollWidth:n.scrollWidth,clientWidth:n.clientWidth,pageWidth:innerWidth,pageScroll:document.documentElement.scrollWidth,shadowScroll:[...n.shadowRoot.querySelectorAll('[class]')].filter(x=>!x.classList.contains('ML__sr-only')&&x.clientWidth>0&&x.scrollWidth>x.clientWidth+2).map(x=>({class:x.className,scrollWidth:x.scrollWidth,clientWidth:x.clientWidth}))})''');result['actualKeyboardTyping']['initialWidth']=before_width
   result.update({'question':q['id'],'identity':q['identity'],'viewport':width});out.append(result)
   assert not result['errors']and not result['rawMarkers'],result
   assert all(n['controls']==1 for n in result['locations']),result
   if True:
    page.screenshot(path=str(H/(q['identity']+'-'+str(width)+'.png')),full_page=True)
  page.close()
 browser.close()
server.shutdown();(H/'free-coordinate-controls.json').write_text(json.dumps(out,indent=2)+'\n');print('controls',len(out),'overflow',sum(r['bodyOverflow']for r in out))
