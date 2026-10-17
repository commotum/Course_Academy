"""Read-only layout verification using the application's current Markdown and full player."""
import argparse,copy,functools,hashlib,http.server,importlib.util,json,re,sys,threading
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs,urlparse
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
AUDIT=ROOT/'reference/mathacademy/audits/2026-10-16-system-equations-display'
BROWSER='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome'
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import loads
spec=importlib.util.spec_from_file_location('preview',ROOT/'generate/pipeline/render_preview.py')
preview=importlib.util.module_from_spec(spec);spec.loader.exec_module(preview)
p=argparse.ArgumentParser();p.add_argument('--changes',type=Path,default=HERE.parent/'changes.json');p.add_argument('--fields',type=Path);p.add_argument('--output',type=Path,default=HERE/'preview');p.add_argument('--tutorials-only',action='store_true');args=p.parse_args()
OUT=args.output.resolve();OUT.mkdir(parents=True,exist_ok=True)
changes=json.loads(args.changes.read_text())
if isinstance(changes,dict):changes=changes['changes']
if args.tutorials_only:changes=[f for f in changes if f['attribute']==':tutorial/content']
current={(f['entity'],f['attribute']):f['value'] for f in json.loads(args.fields.read_text())} if args.fields else {}
for c in changes:
 if args.fields:
  assert current[c['entity'],c['attribute']]==c['after'],('readback changed',c['entity'],c['attribute'])
entities=json.loads((ROOT/'reference/mathacademy/audits/2026-10-16-mth341/entities.json').read_text())
for path in (AUDIT/'content').glob('*-entities.json'):entities.update(json.loads(path.read_text()))
snapshot=json.loads((HERE.parent/'snapshot.json').read_text())
for group in ['questions','tutorials']:
 for row in snapshot[group]:entities[str(row[0][':db/id'])]=row[0]
types={r[0][':db/id']:r[0][':db/ident'] for r in loads((ROOT/'reference/mathacademy/audits/2026-10-16-mth341/types.edn').read_text())}
lookup={(f['entity'],f['attribute']):f for f in json.loads((AUDIT/'content/fields.json').read_text())}
lookup.update({(f['entity'],f['attribute']):f for f in json.loads((AUDIT/'wide-mth341/findings.json').read_text())})
for f in changes:
 f['topic']=f.get('topic',lookup.get((f['entity'],f['attribute']),{}).get('topic'))
 e=entities.get(str(f['entity']),{})
 f['answerFields']=[{'key':a[':answer-field/key'],'id':a[':db/id'],'type':types.get(a.get(':answer-field/type',{}).get(':db/id'),a.get(':answer-field/type',{}).get(':db/ident'))} for a in e.get(':question/answer-fields',[])]
fixture=(ROOT/'reference/mathacademy/audits/2026-10-16-mth341/render-fixture.html').read_text()
representatives=[17592186529306,17592186505001,17592186508249,17592186199637,17592186097842]
representatives=[eid for eid in representatives if any(c['entity']==eid for c in changes)]
records=[]
for eid in representatives:
 for version in ['before','after']:
  q=copy.deepcopy(entities.get(str(eid),{}));fs=[c for c in changes if c['entity']==eid]
  for f in fs:q[f['attribute']]=f[version]
  if ':tutorial/content' in q:
   activity={'activityId':str(len(records)),'title':'System formatting verification','type':'lesson','steps':[{'kind':'tutorial','contentId':eid,'title':q.get(':tutorial/title','Tutorial'),'markdown':q[':tutorial/content'],'fields':[]}],'courseId':'review','learner':{'id':1,'name':'Offline review'}}
  else:
   for af in q[':question/answer-fields']:
    if ':db/ident' not in af[':answer-field/type']:af[':answer-field/type']={':db/ident':types[af[':answer-field/type'][':db/id']]}
    af[':answer-field/correct']=next(a for a in af[':answer-field/choices'] if a[':db/id']==af[':answer-field/correct'][':db/id'])
   activity=preview.preview({'question':q},len(records));activity['title']='System formatting verification'
   activity['steps'][0]['contentId']=eid;activity['steps'][0]['status']='started'
   for field in activity['steps'][0]['fields']:field.pop('response',None)
  records.append({'entity':eid,'version':version,'activity':activity})
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  parsed=urlparse(self.path)
  data=None
  if parsed.path=='/api/developer-mode':data={'enabled':True}
  elif parsed.path=='/api/preview':data=records[int(parse_qs(parsed.query)['activityId'][0])]['activity']
  if data is not None:
   body=json.dumps(data).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body);return
  return super().do_GET()
 def do_POST(self):self.send_error(405,'Read-only verification fixture')
 def translate_path(self,path):
  parsed=urlparse(path)
  if parsed.path=='/learn':return str(ROOT/'ui/Learning.html')
  if parsed.path=='/api/asset':return str(Path('/media/jake/SSD/EDB/math')/parse_qs(parsed.query)['path'][0])
  return super().translate_path(path)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
STATE=r'''root=>{
 const math=[];
 for(const item of MathJax.startup.document.math){const tables=[];item.root.walkTree(n=>{if(n.kind==='mtable')tables.push({rows:n.childNodes.length,columns:n.childNodes[0]?.childNodes.length,alignment:n.attributes.get('columnalign'),cells:n.childNodes.map(row=>row.childNodes.map(cell=>cell.toString()))});});math.push({tex:item.math,display:item.display,tables,flatSystem:/^\s*\\\{/.test(item.math)&&item.math.includes(';')&&item.math.includes('=')&&!tables.length,duplicateOperationBars:/\\mid\s*\\mid\s*\\cdot/.test(item.math),badSystemRows:/\\left\s*\\\{/.test(item.math)&&(!tables.length||tables[0].rows<2)});}
 const plain=root.cloneNode(true);plain.querySelectorAll('mjx-container,pre,code').forEach(n=>n.remove());
 return {math,residualText:/\$|\\(?:begin|end|left|right|text|frac)\b/.test(plain.textContent)?plain.textContent:null,mathCount:root.querySelectorAll('mjx-container').length,displayMath:root.querySelectorAll('mjx-container[display="true"]').length,codeBlocks:[...root.querySelectorAll('pre')].map(n=>n.textContent),errors:[...root.querySelectorAll('[data-mml-node="merror"],mjx-merror,.math-error')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),undefinedMacros:[...root.querySelectorAll('[data-mjx-error], [data-mml-node="mtext"][fill="red"]')].map(n=>({text:n.textContent,detail:n.getAttribute('data-mjx-error')})),orderedLists:[...root.querySelectorAll('.prose > ol')].map(n=>({start:n.start,items:n.querySelectorAll(':scope > li').length,nested:n.querySelectorAll(':scope > li > ul > li').length})),topUnorderedItems:root.querySelectorAll('.prose > ul > li').length,images:[...root.querySelectorAll('img')].map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0})),controls:[...root.querySelectorAll('input,select,textarea,math-field')].map(n=>({tag:n.tagName,type:n.type||n.dataset.answerType||'',name:n.name||n.getAttribute('name')||'',placeholder:n.placeholder||'',disabled:Boolean(n.disabled||n.readOnly),options:n.tagName==='SELECT'?[...n.options].map(o=>({value:o.value,text:o.textContent})):null})),overflow:root.scrollWidth>root.clientWidth+2,bodyOverflow:document.body.scrollWidth>window.innerWidth+2};}'''
results=[];full=[];page_errors=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path=BROWSER)
  for view,width,height in [('desktop',1280,1000),('mobile',390,844)]:
   page=browser.new_page(viewport={'width':width,'height':height});errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort())
   page.goto(origin+'/fixture');page.wait_for_function('window.ready===true',timeout=20000)
   page.evaluate('() => {window.inspectState='+STATE+';}')
   for i,f in enumerate(changes):
    row=page.evaluate(r'''async record=>{MathJax.typesetClear();content.replaceChildren();const article=document.createElement('article');article.append(render(record.after,'prose',record.answerFields));content.append(article);await MathJax.typesetPromise([article]);for(const image of article.querySelectorAll('img')){image.loading='eager';await image.decode().catch(()=>{});}return inspectState(article);}''',f)
    row.update({'entity':f['entity'],'attribute':f['attribute'],'topic':f.get('topic'),'viewport':view})
    row['passed']=not any([row['residualText'],row['codeBlocks'],row['errors'],row['undefinedMacros'],any(m['flatSystem'] or m['duplicateOperationBars'] or m['badSystemRows'] for m in row['math']),any(not image['loaded'] for image in row['images'])])
    if f['entity']==17592186199637:row['passed']=row['passed'] and row['displayMath']==3 and row['topUnorderedItems']==2 and len(row['images'])==2
    if f['entity']==17592186097842:row['passed']=row['passed'] and row['orderedLists']==[{'start':1,'items':6,'nested':3}]
    results.append(row)
    if (i+1)%50==0:print('Rendered',i+1,'of',len(changes),view,'fields',flush=True)
   page_errors.extend(errors);page.close()
   for i,r in enumerate(records):
    page=browser.new_page(viewport={'width':width,'height':height});errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.route('**/*',lambda route:route.continue_() if route.request.url.startswith(origin+'/') else route.abort())
    page.goto(origin+f'/learn?activityId={i}',wait_until='networkidle');page.locator('.lesson-content').wait_for()
    page.evaluate('''async()=>{for(const d of document.querySelectorAll('details.worked-solution'))d.open=true;for(const image of document.images)image.loading='eager';if(MathJax.startup?.promise)await MathJax.startup.promise;await MathJax.typesetPromise();await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));}''')
    row=page.locator('.lesson-content').evaluate(STATE);row.update({'entity':r['entity'],'version':r['version'],'viewport':view,'page_errors':errors})
    stem=OUT/f'{r["entity"]}-{r["version"]}-{view}'
    page.screenshot(path=str(stem)+'.png',full_page=True,animations='disabled');(Path(str(stem)+'.html')).write_text(page.content())
    row['screenshot']=str(stem.relative_to(ROOT))+'.png'
    # Exercise enabled fields locally after the screenshot; never submit responses.
    interactions=[]
    for control in page.locator('.lesson-content select,.lesson-content input:not([type=hidden]),.lesson-content textarea,.lesson-content math-field').all():
     if control.is_disabled():continue
     tag=control.evaluate('n=>n.tagName');kind=control.get_attribute('type')
     if tag=='SELECT':
      options=control.locator('option:not([disabled])').all();option=options[-1];value=option.get_attribute('value');control.select_option(value=value);interactions.append({'tag':tag,'changed':control.input_value()==value})
     elif kind in ['radio','checkbox']:control.locator('xpath=ancestor::label[1]').click();interactions.append({'tag':tag,'changed':control.is_checked()})
     elif tag=='MATH-FIELD':control.click();control.press('2');interactions.append({'tag':tag,'changed':control.evaluate("n=>n.value==='2'")})
     else:control.fill('2');interactions.append({'tag':tag,'changed':control.input_value()=='2'})
    row['interactions']=interactions
    full.append(row);page_errors.extend(errors);page.close()
   print('Finished',view,'verification',flush=True)
  browser.close()
finally:server.shutdown();server.server_close()
comparisons=[]
for eid in representatives:
 for view in ['desktop','mobile']:
  before=next(r for r in full if r['entity']==eid and r['viewport']==view and r['version']=='before');after=next(r for r in full if r['entity']==eid and r['viewport']==view and r['version']=='after')
  comparison={'entity':eid,'viewport':view,'controls':len(after['controls']),'controls_identical':before['controls']==after['controls'],'interactions_passed':all(i['changed'] for i in after['interactions']),'math_errors':after['errors'],'overflow_after':after['bodyOverflow'],'before_system_tables':sum(len(m['tables']) for m in before['math'] if r'\{' in m['tex']),'after_system_tables':sum(len(m['tables']) for m in after['math'] if r'\{' in m['tex'])}
  comparison['passed']=comparison['controls_identical'] and comparison['interactions_passed'] and not comparison['math_errors'];comparisons.append(comparison)
summary={'passed':all(r['passed'] for r in results) and all(r['passed'] for r in comparisons) and not page_errors,'fields':len(changes),'rendered_field_viewports':len(results),'renderer':'Unmodified current learning.js Markdown, marked, MathJax SVG, and full Learning.html preview player','database_writes':0,'question_metadata_basis':snapshot['basis'],'readback_verified':bool(args.fields),'changes_sha256':hashlib.sha256(args.changes.read_bytes()).hexdigest(),'page_errors':page_errors,'parse_error_fields':sum(bool(r['errors']) for r in results),'raw_tex_fields':sum(bool(r['residualText']) for r in results),'code_block_fields':sum(bool(r['codeBlocks']) for r in results),'flat_system_expressions':sum(m['flatSystem'] for r in results for m in r['math']),'double_operation_bar_expressions':sum(m['duplicateOperationBars'] for r in results for m in r['math']),'bad_system_row_expressions':sum(m['badSystemRows'] for r in results for m in r['math']),'systems_with_two_rows':sum(r'\left\{' in m['tex'] and m['tables'] and m['tables'][0]['rows']==2 for r in results for m in r['math']),'control_comparisons':comparisons,'ui_hashes':{name:hashlib.sha256((ROOT/'ui'/name).read_bytes()).hexdigest() for name in ['Learning.html','learning.js','question-fields.js','mathjax-config.js','learning.css']}}
summary['table_shapes_per_viewport']={view:[{'rows':shape[0],'columns':shape[1],'count':count} for shape,count in sorted(Counter((table['rows'],table['columns']) for r in results if r['viewport']==view for m in r['math'] for table in m['tables']).items())] for view in ['desktop','mobile']}
summary['topics']=[{'topic':tid,'fields':sum(f.get('topic')==tid for f in changes),'entities':len({f['entity'] for f in changes if f.get('topic')==tid})} for tid in sorted({f['topic'] for f in changes if f.get('topic')})]
(OUT/'fields-rendering.json').write_text(json.dumps(results,indent=2)+'\n');(OUT/'full-ui-rendering.json').write_text(json.dumps(full,indent=2)+'\n');(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2));assert summary['passed'],'Inspect render report failures'
