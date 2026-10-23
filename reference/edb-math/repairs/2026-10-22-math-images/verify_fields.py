"""Exercise complete before/after fields in the actual player Markdown/MathJax pipeline."""
import base64,collections,functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
JS=r'''async rows=>{
 const results=[];
 for(const r of rows){
  const checks={};
  for(const version of ['before','after']){
   const article=document.createElement('article');article.className='lesson-content content-card';article.append(render(r[version]));content.append(article);
   let thrown=null;try{await MathJax.typesetPromise([article])}catch(e){thrown=String(e)}
   const errors=[...article.querySelectorAll('[data-mml-node="merror"]')].map(x=>x.textContent);
   const unknown=[...article.querySelectorAll('svg [data-mml-node="mtext"]')].filter(n=>[...n.querySelectorAll('path[data-c],use[data-c]')][0]?.getAttribute('data-c')==='5C').length;
   checks[version]={math:[...MathJax.startup.document.math].filter(m=>article.contains(m.typesetRoot)).length,errors,unknown,thrown,images:article.querySelectorAll('img').length};
   MathJax.typesetClear([article]);article.remove();
  }
  results.push({entity:r.entity,attribute:r.attribute,expected_added_math:r.edits.length,...checks});
 }
 return results;
}'''
def main():
 fields=json.loads((HERE/'fields.json').read_text());prior={}
 if (HERE/'field-render-verification.json').exists():
  old=json.loads((HERE/'field-render-verification.json').read_text());failed={(r['entity'],r['attribute']) for r in old['failures']};prior={(r['entity'],r['attribute']):r for r in old['records'] if (r['entity'],r['attribute']) not in failed}
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();results=[];page_errors=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page(viewport={'width':1000,'height':1000});page.on('pageerror',lambda e:page_errors.append(str(e)))
  def route(req):
   if req.request.resource_type=='image':return req.fulfill(body=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jk1kAAAAASUVORK5CYII='),content_type='image/png')
   if req.request.url==origin+'/fixture':return req.fulfill(body=fixture,content_type='text/html')
   return req.continue_() if req.request.url.startswith(origin+'/') else req.abort()
  page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready === true')
  pending=[]
  for f in fields:
   old=prior.get((f['entity'],f['attribute']))
   if old and old.get('before_sha256')==f['before_sha256'] and old.get('after_sha256')==f['after_sha256']:results.append(old)
   else:pending.append(f)
  print('new or changed full-field checks',len(pending),flush=True)
  for i in range(0,len(pending),40):
   results.extend(page.evaluate(JS,pending[i:i+40]));(HERE/'field-render-progress.json').write_text(json.dumps({'verified':len(results),'total':len(fields)})+'\n')
   if i%200==0:print('fields rendered',len(results),'/',len(fields),flush=True)
  failures=[]
  by_key={(f['entity'],f['attribute']):f for f in fields}
  for r in results:
   f=by_key[r['entity'],r['attribute']];r['before_sha256']=f['before_sha256'];r['after_sha256']=f['after_sha256']
   b,a=r['before'],r['after'];reasons=[]
   if a['thrown']:reasons.append('after-render-threw')
   if a['math']-b['math']!=r['expected_added_math']:reasons.append('math-count-delta')
   if collections.Counter(a['errors'])-collections.Counter(b['errors']):reasons.append('new-mathjax-error')
   if a['unknown']>b['unknown']:reasons.append('new-undefined-command')
   if reasons:failures.append({**r,'reasons':reasons})
  for width,label in [(1000,'desktop'),(375,'mobile')]:
   page.set_viewport_size({'width':width,'height':1000})
   sample=[f for f in fields if f['entity']==17592186092122]
   page.evaluate('''async rows=>{content.innerHTML='';for(const r of rows){const a=document.createElement('article');a.className='lesson-content content-card';a.append(render(r.after));content.append(a)}await MathJax.typesetPromise([content])}''',sample)
   (HERE/'review').mkdir(exist_ok=True);page.screenshot(path=str(HERE/'review'/f'example-731-{label}.png'),full_page=True);page.evaluate('MathJax.typesetClear([content])')
  browser.close()
 server.shutdown();report={'fields':len(results),'page_errors':page_errors,'failures':failures,'records':results,'new_math_expressions':sum(r['after']['math']-r['before']['math'] for r in results),'baseline_math_errors':sum(len(r['before']['errors']) for r in results),'after_math_errors':sum(len(r['after']['errors']) for r in results)}
 (HERE/'field-render-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='records'}));assert not failures and not page_errors
if __name__=='__main__':main()
