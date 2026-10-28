import functools,http.server,json,sys,threading
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT,IMAGE_TYPES
D=json.loads((H/'staged-current.json').read_text());qs=D['questions'];chosen={17592186698391,17592186408112,17592186233804,17592186134135};chosen.update(q[':db/id']for q in qs if q.get(':question/math-academy-id')in['q-59676','q-6827','q-18040','q-125716'])
for predicate in [lambda q:any(f[':answer-field/type'][':db/ident'].endswith('/checkbox')for f in q.get(':question/answer-fields',[])),lambda q:'{{'in q[':question/problem']and'<table'in q[':question/problem'],lambda q:'{{'in q[':question/problem']and r'\begin{bmatrix}'in q[':question/problem'],lambda q:'{{'in q[':question/problem']and r'\begin{vmatrix}'in q[':question/problem']]:
 found=next((q for q in qs if predicate(q)),None)
 if found:chosen.add(found[':db/id'])
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">');fixture+='''<script type="module">import * as controls from '/ui/question-fields.js';window.controls=controls;await controls.loadMathInputs();window.controlsReady=true;</script>'''
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';out=[];screens=H/'screens';screens.mkdir(exist_ok=True)
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page()
 def route(req):
  u=urlsplit(req.request.url)
  if req.request.url==origin+'/fixture':req.fulfill(body=fixture,content_type='text/html')
  elif u.path=='/api/asset':
   f=image_path(parse_qs(u.query).get('path',[''])[0],DEFAULT_MATH_ROOT)
   if f:req.fulfill(body=f.read_bytes(),content_type=IMAGE_TYPES[f.suffix.lower()])
   else:req.fulfill(status=404,body='unavailable')
  elif req.request.url.startswith(origin+'/'):req.continue_()
  else:req.abort()
 page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready&&window.controlsReady')
 for width in[390,1100]:
  page.set_viewport_size({'width':width,'height':1000})
  for q in qs:
   if q[':db/id']not in chosen:continue
   fields=[]
   for f in q.get(':question/answer-fields',[]):
    right=f[':answer-field/correct'];fields.append({'id':f[':db/id'],'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'answerType':right[':answer/type'][':db/ident'].split('/')[-1],'correctAnswer':{'id':right.get(':db/id',right[':answer/id']),'type':right[':answer/type'][':db/ident'].split('/')[-1],'value':right[':answer/value']},'choices':[{'id':a.get(':db/id',a[':answer/id']),'type':a[':answer/type'][':db/ident'].split('/')[-1],'value':a[':answer/value']}for a in f[':answer-field/choices']]})
   result=page.evaluate('''async ({problem,fields})=>{
    MathJax.typesetClear([content]);let prompt=render(problem,'prose',fields),list=document.createElement('div');content.replaceChildren(prompt,list);
    const value=a=>render(a.type==='math'?'$'+a.value+'$':a.type==='image'?'![]('+a.value+')':a.value,'prose');
    controls.mountInlineFields(prompt,list,fields,f=>{let set=document.createElement('fieldset');set.dataset.fieldId=f.id;
     if(f.type==='blank')set.append(controls.blankInput(f,f.key,f.id));
     else if(f.type==='checkbox')set.append(controls.checkboxControl(f,label=>render(label,'prose')));
     else if(f.type==='select'){let select=document.createElement('select');select.name=f.id;let none=document.createElement('option');none.value='';none.textContent='Select…';select.append(none);for(let a of f.choices){let o=document.createElement('option');o.value=a.id;o.textContent=a.value;select.append(o);}set.append(controls.richSelect(select,f.choices,value,a=>a.id,node=>MathJax.typesetPromise([node])));}
     else for(let a of f.choices){let label=document.createElement('label');label.className='choice';let input=document.createElement('input');input.type='radio';input.name=f.id;input.value=a.id;label.append(controls.choiceIndicator(input),value(a));set.append(label);}return set;});
    await MathJax.typesetPromise([content]);await document.fonts.ready;
    return {overflow:document.documentElement.scrollWidth>innerWidth+1,width:innerWidth,scroll:document.documentElement.scrollWidth,math_fields:content.querySelectorAll('math-field').length,checkboxes:content.querySelectorAll('input[type=checkbox]').length,selects:content.querySelectorAll('select').length,unmounted:[...prompt.querySelectorAll('[data-field-key]')].filter(n=>!n.children.length).map(n=>n.dataset.fieldKey),errors:[...content.querySelectorAll('[data-mml-node=merror]')].map(n=>n.textContent),controls:[...content.querySelectorAll('.answer-inline')].map(n=>({field:n.dataset.fieldId,type:n.dataset.type,top:n.getBoundingClientRect().top,left:n.getBoundingClientRect().left,right:n.getBoundingClientRect().right}))};
   }''',{'problem':q[':question/problem'],'fields':fields})
   assert result['math_fields']==sum(f['type']=='blank'for f in fields),(q[':db/id'],result)
   assert result['checkboxes']==sum(f['type']=='checkbox'for f in fields),(q[':db/id'],result)
   assert not result['unmounted']and not result['errors'],(q[':db/id'],result)
   page.locator('#content').screenshot(path=str(screens/f"controls-{q[':db/id']}-{width}.png"))
   if any(f['type']=='select'for f in fields):
    page.locator('.answer-select-trigger').first.click();page.wait_for_timeout(30);result['open_select_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1');page.locator('#content').screenshot(path=str(screens/f"controls-{q[':db/id']}-{width}-open.png"));page.locator('.answer-select-menu [role=option]').first.click()
   for i,f in enumerate(fields):
    if f['type']=='blank':
     n=page.locator('math-field').nth(sum(g['type']=='blank'for g in fields[:i]));n.evaluate('(n,v)=>{n.value=v}',f['correctAnswer']['value']);assert n.evaluate('n=>n.value')
   result['filled_control_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1');out.append({'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'width':width,**result})
 b.close()
server.shutdown();(H/'control-rendering.json').write_text(json.dumps({'basis_t':9837,'actual_native_controls':True,'questions':len(chosen),'checks':out,'database_writes':0},indent=2)+'\n');print('questions',len(chosen),'width checks',len(out),'overflows',[(r['question'],r['width'],r['overflow'],r.get('open_select_overflow'),r['filled_control_overflow'])for r in out if r['overflow']or r.get('open_select_overflow')or r['filled_control_overflow']])
