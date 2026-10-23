"""Verify exact-field formatting repairs in the actual player renderer."""
import base64,collections,functools,hashlib,http.server,json,re,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
JS=r'''async rows=>{
 const results=[];
 const normalize=s=>s.replace(/\\displaystyle\b/g,'').replace(/\s/g,'');
 for(const row of rows){const versions={};
  for(const version of ['before','after']){
   const a=document.createElement('article');a.className='lesson-content content-card';a.append(render(row[version],'prose',row.fields));content.append(a);
   const skeleton={};for(const sel of ['li','ul','ol','table','tr','td','th','h1','h2','h3','blockquote','a','img'])skeleton[sel]=a.querySelectorAll(sel).length;
   const slots=[...a.querySelectorAll('[data-field-key]')].map(n=>n.dataset.fieldKey);
   let thrown=null;try{await MathJax.typesetPromise([a])}catch(e){thrown=String(e)}
   const items=[...MathJax.startup.document.math].filter(m=>a.contains(m.typesetRoot));
   const errors=items.map(m=>[...m.typesetRoot.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.textContent));
   const unknown=items.map(m=>[...m.typesetRoot.querySelectorAll('[data-mml-node="mtext"]')].filter(n=>[...n.querySelectorAll('path[data-c],use[data-c]')][0]?.getAttribute('data-c')==='5C').length);
   versions[version]={math:items.length,display:items.filter(m=>m.display).length,errors,unknown,thrown,skeleton,slots};
   MathJax.typesetClear([a]);a.remove();
  }
  const failures=[];const b=versions.before,c=versions.after;
  if(c.thrown)failures.push('after-threw');
  if(c.math!==b.math)failures.push('math-count');
  if(JSON.stringify(b.skeleton)!==JSON.stringify(c.skeleton))failures.push('document-structure');
  if(JSON.stringify(b.slots)!==JSON.stringify(c.slots))failures.push('answer-slots');
  if(c.display-b.display!==row.edits.filter(e=>e.action==='display').length)failures.push('display-count');
  for(let i=0;i<Math.min(b.math,c.math);i++){
   if(c.errors[i].length>b.errors[i].length)failures.push('new-math-error:'+i);
   if(c.unknown[i]>b.unknown[i])failures.push('new-undefined-command:'+i);
  }
  results.push({entity:row.entity,attribute:row.attribute,before_sha256:row.before_sha256,after_sha256:row.after_sha256,failures,...versions});
 }
 return results;
}'''
def main():
 fields=json.loads((HERE/'fields.json').read_text());cache={}
 path=HERE/'render-checks.jsonl'
 if path.exists():
  for r in map(json.loads,path.open()):cache[r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']]=r
 pending=[f for f in fields if (f['entity'],f['attribute'],f['before_sha256'],f['after_sha256']) not in cache]
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();page_errors=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page(viewport={'width':1000,'height':1000});page.on('pageerror',lambda e:page_errors.append(str(e)))
  def route(req):
   if req.request.resource_type=='image':return req.fulfill(body=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jk1kAAAAASUVORK5CYII='),content_type='image/png')
   if req.request.url==origin+'/fixture':return req.fulfill(body=fixture,content_type='text/html')
   return req.continue_() if req.request.url.startswith(origin+'/') else req.abort()
  page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready === true',timeout=20000)
  print('New full-field render checks',len(pending),'cached',len(fields)-len(pending),flush=True)
  with path.open('a') as output:
   for i in range(0,len(pending),25):
    rows=page.evaluate(JS,pending[i:i+25])
    for r in rows:cache[r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']]=r;output.write(json.dumps(r,ensure_ascii=False)+'\n')
    output.flush()
    if i%250==0:print('Rendered',min(i+25,len(pending)),'/',len(pending),flush=True)
    (HERE/'render-progress.json').write_text(json.dumps({'checked':len(fields)-len(pending)+min(i+25,len(pending)),'total':len(fields)})+'\n')
  # Inspect the actual reported examples in both layouts without submitting answers.
  sample_ids=[17592186319332,17592186582385,17592186582346,17592186250233,17592186582344,17592186250225,17592186064099,17592186055964]
  for width,label in [(1000,'desktop'),(375,'mobile')]:
   page.set_viewport_size({'width':width,'height':1000})
   for eid in sample_ids:
    selected=[f for f in fields if f['entity']==eid and f['attribute'] in ('question/problem','tutorial/content')]
    if not selected:continue
    for version in ['before','after']:
     page.evaluate('''async ({rows,version})=>{MathJax.typesetClear([content]);content.innerHTML='';for(const row of rows){const a=document.createElement('article');a.className='lesson-content content-card';a.append(render(row[version],'prose',row.fields));content.append(a)}await MathJax.typesetPromise([content])}''',{'rows':selected,'version':version})
     (HERE/'review').mkdir(exist_ok=True);page.screenshot(path=str(HERE/'review'/f'{eid}-{version}-{label}.png'),full_page=True)
  browser.close()
 server.shutdown();records=[cache[f['entity'],f['attribute'],f['before_sha256'],f['after_sha256']] for f in fields];bad=[r for r in records if r['failures']];report={'fields':len(records),'failed_fields':len(bad),'page_errors':page_errors,'display_expressions_added':sum(r['after']['display']-r['before']['display'] for r in records),'existing_math_errors':sum(len(e) for r in records for e in r['before']['errors']),'after_math_errors':sum(len(e) for r in records for e in r['after']['errors']),'failures':bad,'verified_field_hashes':[[r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']] for r in records]};(HERE/'render-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('failures','verified_field_hashes')}));assert not bad and not page_errors
if __name__=='__main__':main()
