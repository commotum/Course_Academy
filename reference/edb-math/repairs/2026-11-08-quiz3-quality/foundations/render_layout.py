import json,sys,threading,functools,http.server
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
from playwright.sync_api import sync_playwright
ROOT=Path.cwd();H=Path(__file__).resolve().parent;sys.path.insert(0,'scripts')
from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT,IMAGE_TYPES
fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
fixture+='''<script type="module">
import {checkboxControl,choiceIndicator,fieldFeedback,freeInput,blankInput,mountInlineFields,richSelect,loadMathInputs} from '/ui/question-fields.js';
const src=await(await fetch('/ui/learning.js')).text();
const a=src.slice(src.indexOf('function answerValue('),src.indexOf('function loadMath('));
const f=src.slice(src.indexOf('function fieldControl('),src.indexOf('function collectResponses('));
const label=src.slice(src.indexOf('function fieldLabel('),src.indexOf('function announce('));
const order=src.slice(src.indexOf('function choiceOrder('),src.indexOf('// EDB membership'));
const maker=new Function('el','markdown','short','checkboxControl','choiceIndicator','fieldFeedback','freeInput','blankInput','richSelect','typeset','studyChoiceId','assetURL',a+label+order+f+';return fieldControl');
const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text)n.textContent=text;return n};
window.control=maker(el,(value)=>render(value,'prose'),v=>String(v||'').split('/').pop(),checkboxControl,choiceIndicator,fieldFeedback,freeInput,blankInput,richSelect,()=>{},v=>v,v=>'/api/asset?path='+encodeURIComponent(v));
window.mount=(prompt,list,fields)=>mountInlineFields(prompt,list,fields,f=>control(f,false,'audit'));
await loadMathInputs();window.layoutReady=true;
</script>'''
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
items=[]
for d in sorted(H.glob('175*')):
 for q in json.loads((d/'questions-after.json').read_text()):
  fs=[{'id':f[':db/id'],'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'response':{'choiceId':f[':answer-field/correct'][':db/id']},'choices':[{'id':a[':db/id'],'type':a[':answer/type'][':db/ident'].split('/')[-1],'value':a[':answer/value']}for a in f[':answer-field/choices']]}for f in q.get(':question/answer-fields',[])]
  items.append({'entity':q[':db/id'],'label':q.get(':question/math-academy-id',str(q[':db/id'])),'value':q[':question/problem'],'fields':fs})
 for ar in json.loads((d/'lessons-after.json').read_text()):
  for s in ar[0][':activity/steps']:
   c=s[':step/content']
   if c.get(':tutorial/content'):items.append({'entity':c[':db/id'],'label':c[':tutorial/title'],'value':c[':tutorial/content'],'fields':[]})
rows=[];(H/'visual').mkdir(exist_ok=True)
try:
 with sync_playwright()as p:
  browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1100,'height':1000})
  def route(r):
   u=urlsplit(r.request.url)
   if r.request.url==origin+'/fixture':r.fulfill(body=fixture,content_type='text/html')
   elif u.path=='/api/asset':
    file=image_path(parse_qs(u.query).get('path',[''])[0],DEFAULT_MATH_ROOT)
    if file:r.fulfill(body=file.read_bytes(),content_type=IMAGE_TYPES[file.suffix.lower()])
    else:r.fulfill(status=404,body='Unavailable')
   elif r.request.url.startswith(origin+'/'):r.continue_()
   else:r.abort()
  page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready&&window.layoutReady')
  for width in [1100,390]:
   page.set_viewport_size({'width':width,'height':1000})
   for item in items:
    result=page.evaluate('''async item=>{MathJax.typesetClear([content]);content.replaceChildren();const card=document.createElement('article');card.className='content-card';const h=document.createElement('h2');h.textContent=item.label;card.append(h);const prompt=render(item.value,'prose',item.fields);const list=document.createElement('div');list.className='answer-fields';card.append(prompt,list);content.append(card);mount(prompt,list,item.fields);await MathJax.typesetPromise([content]);await document.fonts.ready;await Promise.all([...content.querySelectorAll('img')].map(i=>{i.loading='eager';return new Promise(resolve=>{if(i.complete)resolve();else{i.onload=resolve;i.onerror=resolve}})}));return {errors:[...content.querySelectorAll('[data-mjx-error]')].map(n=>n.getAttribute('data-mjx-error')),rawMarkers:content.textContent.includes('{{field-'),controls:content.querySelectorAll('[data-field-id]').length,images:[...content.querySelectorAll('img')].map(i=>({source:i.src,loaded:i.complete&&i.naturalWidth>0})),cardClientWidth:card.clientWidth,cardScrollWidth:card.scrollWidth,inlineSlots:[...content.querySelectorAll('[data-field-key]')].map(n=>n.dataset.fieldKey)}}''',item)
    rows.append({'entity':item['entity'],'width':width,'expected_controls':len(item['fields']),**result})
    if item['entity']in[17592186124899,17592186311877,17592186152571,17592186088920,17592186088057]:page.locator('.content-card').screenshot(path=str(H/'visual'/f"{item['entity']}-{width}.png"))
  browser.close()
finally:server.shutdown();server.server_close()
failed=[r for r in rows if r['errors']or r['rawMarkers']or r['controls']!=r['expected_controls']or any(not i['loaded']for i in r['images'])]
report={'layouts':len(rows),'questions_and_tutorials':len(items),'actual_player_fieldControl':True,'widths':[1100,390],'failures':failed,'checks':rows};(H/'layout-report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'layouts':len(rows),'failures':len(failed)},indent=2))
