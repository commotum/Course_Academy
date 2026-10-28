import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
sys.path.insert(0,"scripts")
from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT,IMAGE_TYPES
from urllib.parse import urlsplit,parse_qs
H=Path(__file__).resolve().parent;R=Path.cwd();D=json.loads((H/'staged-graph-control-snapshot.json').read_text());idents=dict(json.loads((H/'idents.json').read_text()));qs=D['questions']
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">').replace('<script src="/ui/vendor/mathjax/tex-svg.js">','<script>MathJax.tex.packages=MathJax.tex.packages.filter(p=>p!=="noundefined");</script><script src="/ui/vendor/mathjax/tex-svg.js">');fixture+='''<script type="module">import * as controls from '/ui/question-fields.js';window.controls=controls;await controls.loadMathInputs();window.inputsReady=true;const src=await(await fetch('/ui/learning.js')).text();window.answerValue=new Function('el','short','assetURL','markdown',src.slice(src.indexOf('function answerValue('),src.indexOf('function loadMath('))+';return answerValue;')((tag,cl)=>{let n=document.createElement(tag);if(cl)n.className=cl;return n;},x=>String(x).split('/').at(-1),x=>'/api/asset?path='+encodeURIComponent(x),window.render);</script>'''
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';out=[];screens=H/'staged-graph-control-screens';screens.mkdir(exist_ok=True)
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':1000});
 def route(r):
  u=urlsplit(r.request.url)
  if r.request.url==origin+'/fixture':r.fulfill(body=fixture,content_type='text/html')
  elif u.path=='/api/asset':
   ref=parse_qs(u.query).get('path',[''])[0];path=image_path(ref,DEFAULT_MATH_ROOT)
   if not path and Path(ref).is_absolute() and H.resolve() in Path(ref).resolve().parents:path=Path(ref)
   if path:r.fulfill(body=path.read_bytes(),content_type=IMAGE_TYPES[path.suffix.lower()])
   else:r.fulfill(status=404,body='Unavailable')
  elif r.request.url.startswith(origin+'/'):r.continue_()
  else:r.abort()
 page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready&&window.inputsReady&&!!window.answerValue')
 for q in qs:
  fields=[]
  for f in q[':question/answer-fields']:
   fields.append({'id':f[':db/id'],'key':f[':answer-field/key'],'type':idents[f[':answer-field/type'][':db/id']].split('/')[-1],'answerType':idents[next(a for a in f[':answer-field/choices']if a[':db/id']==f[':answer-field/correct'][':db/id'])[':answer/type'][':db/id']].split('/')[-1],'choices':[{'id':a[':db/id'],'value':a[':answer/value'],'type':idents[a[':answer/type'][':db/id']].split('/')[-1]}for a in f[':answer-field/choices']]})
  result=page.evaluate('''async({value,fields})=>{MathJax.typesetClear([content]);const n=render(value,'prose',fields),list=document.createElement('div');content.replaceChildren(n,list);controls.mountInlineFields(n,list,fields,f=>{const set=document.createElement('fieldset');set.dataset.fieldId=f.id;set.className='answer-field';set.dataset.type=f.type;if(f.type==='checkbox'){set.append(controls.checkboxControl(f,x=>render(x,'prose')));return set;}if(f.type==='blank'){set.append(controls.blankInput(f,'Answer',f.id));return set;}if(f.type==='select'){const select=document.createElement('select');select.name=f.id;let blank=document.createElement('option');blank.value='';blank.textContent='Select an answer';select.append(blank);for(const a of f.choices){let o=document.createElement('option');o.value=a.id;o.textContent=a.value;select.append(o);}set.append(controls.richSelect(select,f.choices,a=>answerValue(a),a=>a.id,()=>MathJax.typesetPromise([content])));return set;}for(const a of f.choices){let label=document.createElement('label');label.className='choice';let inp=document.createElement('input');inp.type='radio';inp.name=f.id;inp.value=a.id;label.append(controls.choiceIndicator(inp),answerValue(a));set.append(label);}return set;});await MathJax.typesetPromise([content]);await document.fonts.ready;await Promise.all([...content.querySelectorAll('img')].map(i=>i.decode().catch(()=>{})));return {errors:[...content.querySelectorAll('[data-mml-node="merror"]')].map(x=>x.getAttribute('data-mjx-error')),raw:content.textContent.includes('$$'),checkboxes:content.querySelectorAll('input[type=checkbox]').length,blanks:content.querySelectorAll('math-field').length,selects:[...content.querySelectorAll('select')].map(s=>({id:s.name,choices:[...s.options].map(o=>o.value).filter(Boolean)})),outside:list.childElementCount,slots:[...n.querySelectorAll('.answer-inline')].map(x=>x.dataset.fieldId),unfilled:[...n.querySelectorAll('[data-field-key]')].filter(x=>!x.children.length).length,images:[...content.querySelectorAll('img')].map(i=>({loaded:i.complete&&i.naturalWidth>0,src:i.src})),tableHTML:[...n.querySelectorAll('table')].map(t=>({html:t.outerHTML,borders:[...t.querySelectorAll('td')].map(c=>({t:getComputedStyle(c).borderTop,b:getComputedStyle(c).borderBottom,l:getComputedStyle(c).borderLeft,r:getComputedStyle(c).borderRight}))})),tableSlots:[...n.querySelectorAll('table.source-table .answer-inline')].map(x=>({field:x.dataset.fieldId,row:x.closest('tr').rowIndex,column:x.closest('td').cellIndex}))};}''',{'value':q[':question/problem'],'fields':fields})
  assert not result['errors']and not result['raw'],(q[':db/id'],result)
  assert result['checkboxes']==sum(f['type']=='checkbox'for f in fields);assert result['blanks']==sum(f['type']=='blank'for f in fields);assert len(result['selects'])==sum(f['type']=='select'for f in fields)
  # Open each actual rich dropdown so every option's rendered math is checked.
  for i in range(len(result['selects'])):
   page.locator('.answer-select-trigger').nth(i).click();page.wait_for_timeout(20);assert page.locator('[data-mml-node="merror"]').count()==0
   if q[':db/id']in[17592186152565,17592186308544]:page.locator('#content').screenshot(path=str(screens/f'{q[":db/id"]}-select-{i}.png'))
   page.keyboard.press('Escape')
  page.locator('#content').screenshot(path=str(screens/f'{q[":db/id"]}-desktop.png'));page.set_viewport_size({'width':390,'height':950});page.wait_for_timeout(10);overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth+1');page.locator('#content').screenshot(path=str(screens/f'{q[":db/id"]}-mobile.png'));page.set_viewport_size({'width':1100,'height':1000});out.append({'question':q[':db/id'],'source':q.get(':question/math-academy-id'),'fields':len(fields),'passed':True,'mobile_overflow':overflow,**result})
  print(q[':db/id'],len(fields),result['checkboxes'],flush=True)
 b.close()
server.shutdown();(H/'staged-graph-controls-validation.json').write_text(json.dumps({'strict_no_noundefined':True,'questions':len(out),'checkbox_labels':sum(r['checkboxes']for r in out),'blank_controls':sum(r['blanks']for r in out),'select_controls':sum(len(r['selects'])for r in out),'checks':out},indent=2));print('UI controls',len(out),'mobile overflows',[r['question']for r in out if r['mobile_overflow']])
