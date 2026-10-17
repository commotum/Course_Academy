"""Audit only extra flat-system candidate fields through the application's actual renderer."""
import functools, http.server, json, sys, threading
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from playwright.sync_api import sync_playwright
ROOT=Path('/home/jake/Developer/Course_Academy');HERE=Path(__file__).resolve().parent/'wide';HERE.mkdir(exist_ok=True)
CONTENT=HERE.parent.parent/'wide-mth341'
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import loads
fields=[f for f in json.loads((CONTENT/'findings.json').read_text()) if f['topic'] in [17592186048826,17592186050190]]
entities=json.loads((ROOT/'reference/mathacademy/audits/2026-10-16-mth341/entities.json').read_text())
types={r[0][':db/id']:r[0][':db/ident'] for r in loads((ROOT/'reference/mathacademy/audits/2026-10-16-mth341/types.edn').read_text())}
for f in fields:
 e=entities[str(f['entity'])]
 f['answerFields']=[{'key':a[':answer-field/key'],'id':a[':db/id'],'type':types[a[':answer-field/type'][':db/id']]} for a in e.get(':question/answer-fields',[])]
 f['kind']='math' if f['attribute']==':answer/value' and e.get(':answer/type',{}).get(':db/ident')==':answer.type/math' else 'prose'
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def translate_path(self,path):
  if path.startswith('/api/asset?'):return str(Path('/media/jake/SSD/EDB/math')/parse_qs(urlparse(path).query)['path'][0])
  return super().translate_path(path)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
fixture=(ROOT/'reference/mathacademy/audits/2026-10-16-mth341/render-fixture.html').read_text()
(HERE/'all-fields-fixture.html').write_text(fixture)
result=[];errors=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome')
  page=browser.new_page(viewport={'width':1060,'height':1100});page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort())
  page.goto(origin+'/fixture');page.wait_for_function('window.ready===true',timeout=20000)
  for start in range(0,len(fields),100):
   records=[dict(f,value='$'+f['value']+'$' if f['kind']=='math' else f['value']) for f in fields[start:start+100]]
   result.extend(page.evaluate(r'''async records=>{const results=[];
    for(const record of records){
     MathJax.typesetClear();content.replaceChildren();const article=document.createElement('article');article.append(render(record.value,'prose',record.answerFields));content.append(article);
     await MathJax.typesetPromise([article]);const math=[];
     for(const item of MathJax.startup.document.math){const tables=[];item.root.walkTree(n=>{if(n.kind==='mtable')tables.push({rows:n.childNodes.length,columns:n.childNodes[0]?.childNodes.length,alignment:n.attributes.get('columnalign')});});math.push({tex:item.math,tables,flatSystem:/^\s*\\\{/.test(item.math)&&item.math.includes(';')&&item.math.includes('=')&&!tables.length,duplicateOperationBars:/\\mid\s*\\mid\s*\\cdot/.test(item.math)});}
     const plain=article.cloneNode(true);plain.querySelectorAll('mjx-container,pre,code').forEach(n=>n.remove());
     results.push({topic:record.topic,entity:record.entity,attribute:record.attribute,kind:record.kind,math,residualText:/\$|\\(?:begin|end|left|right|text|frac)\b/.test(plain.textContent)?plain.textContent:null,mathCount:article.querySelectorAll('mjx-container').length,codeBlocks:[...article.querySelectorAll('pre')].map(n=>n.textContent),errors:[...article.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),undefinedMacros:[...article.querySelectorAll('[data-mjx-error], [data-mml-node="mtext"][fill="red"]')].map(n=>({text:n.textContent,detail:n.getAttribute('data-mjx-error')}))});
    }return results;}''',records))
   print('Rendered',len(result),'of',len(fields),'fields',flush=True)
  for eid in [17592186505001,17592186508249]:
   fs=[f for f in fields if f['entity']==eid]
   if not fs:continue
   awaitable=page.evaluate('''async fs=>{MathJax.typesetClear();content.replaceChildren();for(const f of fs){const article=document.createElement('article');article.append(Object.assign(document.createElement('h3'),{textContent:f.attribute}),render(f.value,'prose',f.answerFields));content.append(article);}await MathJax.typesetPromise([content]);}''',fs)
   page.locator('img').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>{i.loading="eager";return i.decode().catch(()=>{});} ))')
   page.screenshot(path=str(HERE/f'question-{eid}.png'),full_page=True)
   (HERE/f'question-{eid}.html').write_text(page.content())
  browser.close()
finally:server.shutdown();server.server_close()
summary={'fields':len(result),'page_errors':errors,'parse_error_fields':sum(bool(r['errors']) for r in result),'raw_tex_fields':sum(bool(r['residualText']) for r in result),'red_command_fields':sum(bool(r['undefinedMacros']) for r in result),'code_block_fields':sum(bool(r['codeBlocks']) for r in result),'flat_system_fields':sum(any(m['flatSystem'] for m in r['math']) for r in result),'flat_system_expressions':sum(m['flatSystem'] for r in result for m in r['math']),'double_operation_bar_fields':sum(any(m['duplicateOperationBars'] for m in r['math']) for r in result),'topics':[]}
for tid in sorted({r['topic'] for r in result}):
 rs=[r for r in result if r['topic']==tid]
 summary['topics'].append({'topic':tid,'fields':len(rs),'flat_system_fields':sum(any(m['flatSystem'] for m in r['math']) for r in rs),'flat_system_expressions':sum(m['flatSystem'] for r in rs for m in r['math']),'double_operation_bar_fields':sum(any(m['duplicateOperationBars'] for m in r['math']) for r in rs)})
(HERE/'all-fields-rendering.json').write_text(json.dumps({'snapshot':json.loads((CONTENT/'snapshot.json').read_text()),'renderer':'actual learning.js markdown function, current MathJax configuration and SVG engine','database_mutations':0,'scope_note':'Only 130 additional flat-system candidate fields from two topics; field text is fresh at recorded basis, answer-field labels/types supplied by prior full audit snapshot for placeholder rendering only.','fields':result,'page_errors':errors},indent=2)+'\n')
(HERE/'all-fields-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
