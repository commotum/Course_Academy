"""Compare every full repaired field through the original and corrected player."""
import base64,functools,hashlib,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
JS=r'''async rows=>{const results=[];for(const row of rows){const versions={};for(const version of ['before','after']){const a=(version==='before'?renderOriginal:render)(row[version],'prose',row.fields);content.replaceChildren(a);const slots=[...a.querySelectorAll('[data-field-key]')].map(n=>n.dataset.fieldKey);let thrown=null;try{await MathJax.typesetPromise([a])}catch(e){thrown=String(e)}const items=[...MathJax.startup.document.math].filter(m=>a.contains(m.typesetRoot));const errors=[...a.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent);const raw=[];const walker=document.createTreeWalker(a,NodeFilter.SHOW_TEXT);let n;while(n=walker.nextNode()){if(n.parentElement.closest('mjx-container,math,script,style'))continue;if(/\\(?:begin|end)\{|\\(?:eqalign|frac|dfrac|sqrt)\b|\[\/?math\]/.test(n.textContent))raw.push(n.textContent.slice(0,200))}versions[version]={slots,thrown,math:items.length,display:items.filter(m=>m.display).length,rows:a.querySelectorAll('[data-mml-node="mtr"]').length,errors,raw,codeMath:[...a.querySelectorAll('pre,code')].filter(n=>/\$|\\(?:begin|frac|dfrac)/.test(n.textContent)).length,math_sources:items.map(m=>m.math)};MathJax.typesetClear([a]);a.remove()}const b=versions.before,c=versions.after,failures=[];if(c.thrown)failures.push('after-threw');if(c.errors.length>b.errors.length)failures.push('new-math-errors');if(c.raw.length)failures.push('raw-tex-leak');if(c.codeMath)failures.push('math-in-code');for(const key of new Set(b.slots)){if(c.slots.filter(k=>k===key).length<b.slots.filter(k=>k===key).length)failures.push('lost-inline-control:'+key)}results.push({entity:row.entity,attribute:row.attribute,before_sha256:row.before_sha256,after_sha256:row.after_sha256,failures,...versions})}return results}'''
def main():
 fields=json.loads((HERE/'fields.json').read_text());path=HERE/'render-checks.jsonl';cache={}
 if path.exists():
  for r in map(json.loads,path.open()):cache[r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']]=r
 pending=[f for f in fields if (f['entity'],f['attribute'],f['before_sha256'],f['after_sha256']) not in cache]
 current=(ROOT/'ui/learning.js').read_text();original=current.replace('let source = protectMath(inlinePrompt(value, fields), match => {',r"let source = inlinePrompt(value, fields).replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g, match => {")
 assert original!=current;(HERE/'original-learning.js').write_text(original)
 fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();fixture=fixture.replace('window.render = make(el,marked,romanLists,inlinePrompt,protectMath);',"window.render = make(el,marked,romanLists,inlinePrompt,protectMath); const oldSource = await (await fetch('/original-learning.js')).text(); const oldRenderer = oldSource.slice(oldSource.indexOf('function escapeHTML('),oldSource.indexOf('function answerValue(')); window.renderOriginal = new Function('el','marked','romanLists','inlinePrompt', labels+';'+oldRenderer+'; return markdown;')(el,marked,romanLists,inlinePrompt);")
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';errors=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page(viewport={'width':1100,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if r.request.resource_type=='image':return r.fulfill(body=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jk1kAAAAASUVORK5CYII='),content_type='image/png')
   if r.request.url==origin+'/fixture':return r.fulfill(body=fixture,content_type='text/html')
   if r.request.url==origin+'/original-learning.js':return r.fulfill(body=original,content_type='application/javascript')
   return r.continue_() if r.request.url.startswith(origin+'/') else r.abort()
  page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready===true');print('Pending full-field renders',len(pending),flush=True)
  with path.open('a') as out:
   for i in range(0,len(pending),12):
    for r in page.evaluate(JS,pending[i:i+12]):cache[r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']]=r;out.write(json.dumps(r,ensure_ascii=False)+'\n')
    out.flush()
    if i%120==0:print('Rendered',min(i+12,len(pending)),'/',len(pending),flush=True)
  for eid in [17592186233932,17592186124792,17592186147850,17592186055388,17592186161864]:
   selected=[f for f in fields if f['entity']==eid]
   if not selected:continue
   (HERE/'review').mkdir(exist_ok=True)
   for version in ['before','after']:
    page.evaluate("async ({rows,version})=>{MathJax.typesetClear([content]);content.replaceChildren();for(const row of rows)content.append((version==='before'?renderOriginal:render)(row[version],'prose',row.fields));await MathJax.typesetPromise([content])}",{'rows':selected,'version':version});page.screenshot(path=str(HERE/'review'/f'{eid}-{version}.png'),full_page=True)
  browser.close()
 server.shutdown();records=[cache[f['entity'],f['attribute'],f['before_sha256'],f['after_sha256']] for f in fields];bad=[r for r in records if r['failures']];report={'fields':len(records),'failed_fields':len(bad),'page_errors':errors,'existing_math_errors':sum(len(r['before']['errors']) for r in records),'after_math_errors':sum(len(r['after']['errors']) for r in records),'raw_tex_before':sum(len(r['before']['raw']) for r in records),'raw_tex_after':sum(len(r['after']['raw']) for r in records),'failures':bad,'verified_field_hashes':[[r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']] for r in records]};(HERE/'render-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('failures','verified_field_hashes')}));assert not bad and not errors
if __name__=='__main__':main()
