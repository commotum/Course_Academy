"""Compare all proposed changes through the actual player and MathJax."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def main():
 fields=json.loads((H/'fields.json').read_text());server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();errors=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html') if r.request.url==origin+'/fixture' else r.continue_() if r.request.url.startswith(origin+'/') else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
  reports=json.loads((H/'render-checks.json').read_text()) if (H/'render-checks.json').exists() else []
  keys={(r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']) for r in reports}
  fields=[r for r in fields if (r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']) not in keys]
  for offset in range(0,len(fields),30):
   chunk=page.evaluate(r'''async rows=>{let reports=[];for(const row of rows){let r={entity:row.entity,attribute:row.attribute,before_sha256:row.before_sha256,after_sha256:row.after_sha256};for(const side of ['before','after']){const n=render(row[side],'prose',[]);content.replaceChildren(n);const plain=n.textContent;const emphasis=[...n.querySelectorAll('strong,em')].map(e=>({tag:e.tagName,text:e.textContent}));const images=[...n.querySelectorAll('img')].map(e=>e.src);const cells=n.querySelectorAll('td,th').length;let thrown=null;try{await MathJax.typesetPromise([n])}catch(e){thrown=String(e)}const math=[...MathJax.startup.document.math].filter(m=>n.contains(m.typesetRoot)).map(m=>({tex:m.math,display:m.display}));const errors=[...n.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(e=>e.textContent);r[side]={plain,emphasis,images,cells,math,errors,thrown};MathJax.typesetClear([n]);}r.same_words=r.before.plain.replace(/\*/g,'').replace(/\s+/g,' ').trim()===r.after.plain.replace(/\*/g,'').replace(/\s+/g,' ').trim();r.same_math=JSON.stringify(r.before.math)===JSON.stringify(r.after.math);r.same_layout=r.before.cells===r.after.cells&&JSON.stringify(r.before.images)===JSON.stringify(r.after.images);r.emphasis_gain=r.after.emphasis.length-r.before.emphasis.length;r.no_new_math_errors=JSON.stringify(r.before.errors)===JSON.stringify(r.after.errors)&&r.after.thrown===r.before.thrown;reports.push(r)}return reports}''',fields[offset:offset+30]);reports.extend(chunk)
   print('Rendered',len(reports),'/',len(fields),flush=True)
  browser.close()
 server.shutdown();(H/'render-checks.json').write_text(json.dumps(reports,indent=2)+'\n');failed=[{k:r[k] for k in ('entity','attribute','same_words','same_math','same_layout','emphasis_gain','no_new_math_errors')} for r in reports if not all(r[k] for k in ('same_words','same_math','same_layout','no_new_math_errors')) or (r['emphasis_gain']<=0 and r['before']['plain'].count('*')<=r['after']['plain'].count('*'))];result={'fields':len(reports),'passed':not failed and not errors,'failed':failed,'page_errors':errors,'emphasis_gain':sum(r['emphasis_gain'] for r in reports)};(H/'render-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
