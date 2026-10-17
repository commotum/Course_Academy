"""Render all audited fields through the application's actual Markdown and MathJax."""
import functools,http.server,json,threading,sys
from urllib.parse import urlparse,parse_qs,unquote
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import loads
AUDIT=ROOT/'reference/mathacademy/audits/2026-10-16-mth341'
types={r[0][':db/id']:r[0][':db/ident'] for r in loads((AUDIT/'types.edn').read_text())}
fields=json.loads((HERE/('committed-fields.json' if '--committed' in sys.argv else 'expected-fields.json')).read_text())
OUT=HERE/('committed-render' if '--committed' in sys.argv else 'preview-render');OUT.mkdir(exist_ok=True)
entities=json.loads((AUDIT/'entities.json').read_text())
for f in fields:
 f['answerFields']=[{'key':a[':answer-field/key'],'id':a[':db/id'],'type':types[a[':answer-field/type'][':db/id']]} for a in entities[str(f['entity'])].get(':question/answer-fields',[])]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def translate_path(self,path):
  if path.startswith('/api/asset?'):return str(Path('/media/jake/SSD/EDB/math')/parse_qs(urlparse(path).query)['path'][0])
  if path.startswith('/images/'):return str(Path('/media/jake/SSD/EDB/math')/path.lstrip('/'))
  return super().translate_path(path)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
html=(AUDIT/'render-fixture.html').read_text()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path="/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome");page=browser.new_page(viewport={'width':1060,'height':1100});errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('**/*',lambda route:route.fulfill(body=html,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort())
  page.goto(origin+'/fixture');page.wait_for_function('window.ready===true',timeout=20000)
  result=[]
  for start in range(0,len(fields),100):
   records=[{'entity':f['entity'],'attribute':f['attribute'],'answerFields':f['answerFields'],'value':('$'+f['value']+'$') if f['kind']=='math' else f['value']} for f in fields[start:start+100]]
   result.extend(page.evaluate(r'''async records=>{const results=[];
    for(const record of records){
     MathJax.typesetClear();content.replaceChildren();const article=document.createElement('article');article.append(render(record.value,"prose",record.answerFields));content.append(article);
     await MathJax.typesetPromise([article]);let tables=[];
     for(const item of MathJax.startup.document.math)item.root.walkTree(n=>{if(n.kind==='mtable')tables.push({rows:n.childNodes.length,columns:n.childNodes[0]?.childNodes.length,alignment:n.attributes.get('columnalign')});});
     const plain=article.cloneNode(true);plain.querySelectorAll('mjx-container,pre,code').forEach(n=>n.remove());
     results.push({residualText: /\$|\\(?:begin|end|left|right|text|frac)\b/.test(plain.textContent)?plain.textContent:null,entity:record.entity,attribute:record.attribute,tables,mathCount:article.querySelectorAll('mjx-container').length,codeBlocks:[...article.querySelectorAll('pre')].map(n=>n.textContent),errors:[...article.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),undefinedMacros:[...article.querySelectorAll('[data-mjx-error], [data-mml-node="mtext"][fill="red"]')].map(n=>({text:n.textContent,detail:n.getAttribute('data-mjx-error'),html:n.outerHTML.slice(0,500)}))});
    }return results;}''',records))
   (OUT/'rendering.json').write_text(json.dumps({'fields':result,'page_errors':errors},indent=2))
   print('Rendered',len(result),'fields',flush=True)
  selected=[17592186566216,17592186566219,17592186124903,17592186125757,17592186124791,17592186074030,17592186100741,17592186235392,17592186295249,17592186547216]
  for eid in selected:
   fs=[f for f in fields if f['entity']==eid]
   awaitable=page.evaluate('''async fs=>{MathJax.typesetClear();content.replaceChildren();for(const f of fs){let a=document.createElement('article');a.append(Object.assign(document.createElement('h3'),{textContent:f.attribute}),render(f.value,"prose",f.answerFields));content.append(a);}await MathJax.typesetPromise([content]);}''',fs)
   page.locator('img').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>{i.loading="eager";return i.decode().catch(()=>{});} ))');page.screenshot(path=str(OUT/f'entity-{eid}.png'),full_page=True)
  browser.close()
finally:server.shutdown();server.server_close()
summary={'fields':len(result),'page_errors':errors,'parse_error_fields':sum(bool(r['errors']) for r in result),'raw_tex_fields':sum(bool(r['residualText']) for r in result),'red_command_fields':sum(bool(r['undefinedMacros']) for r in result),'code_block_fields':sum(bool(r['codeBlocks']) for r in result)}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
assert not errors
assert not any(r['errors'] or r['residualText'] or r['undefinedMacros'] or r['codeBlocks'] for r in result), 'Inspect rendering.json failures before commit' 
