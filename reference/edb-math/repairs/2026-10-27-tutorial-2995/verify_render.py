"""Render every before/after through the actual player and MathJax, read-only."""
import concurrent.futures,functools,http.server,json,threading,time
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
fields=json.loads((H/'fields.json').read_text());fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
def worker(shard):
 out=[];pageerrors=[];part=fields[shard::3]
 with sync_playwright()as p:
  b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':1000});page.on('pageerror',lambda e:pageerrors.append(str(e)));page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
  for offset in range(0,len(part),10):
   checked=page.evaluate(r'''async fields=>{let out=[];for(const f of fields){const r={entity:f.entity,attribute:f.attribute,before_sha256:f.before_sha256,after_sha256:f.after_sha256};for(const side of ['before','after']){MathJax.typesetClear([content]);const value=f.math_answer&&!/^\s*(\$|\\\[|\\\()/.test(f[side])?'$'+f[side]+'$':f[side];let n=render(value);content.replaceChildren(n);await MathJax.typesetPromise([n]);r[side]={errors:[...n.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),images:[...n.querySelectorAll('img')].map(n=>n.getAttribute('src')),math:[...MathJax.startup.document.math].filter(m=>n.contains(m.typesetRoot)).map(m=>m.math),tables:n.querySelectorAll('[data-mml-node="mtable"]').length};}r.formula_regrouping_reviewed=(f.reasons||[]).some(x=>['source-formula-recovery','source-evaluation-bar-recovery','duplicate-display-wrapper','flattened-system'].includes(x));r.passed=r.after.errors.length===0&&JSON.stringify(r.before.images)===JSON.stringify(r.after.images)&&(r.after.math.length===r.before.math.length||r.formula_regrouping_reviewed);out.push(r)}return out}''',part[offset:offset+10]);out.extend(checked)
   if offset%100==0:print('shard',shard,'rendered',offset+len(checked),'of',len(part),flush=True)
  b.close()
 result={'checks':out,'page_errors':pageerrors};(H/f'render-shard-{shard}.json').write_text(json.dumps(result,indent=2)+'\n');return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:results=list(pool.map(worker,range(3)))
server.shutdown();checks={(x['entity'],x['attribute']):x for r in results for x in r['checks']};checks=[checks[f['entity'],f['attribute']]for f in fields];errors=[x for r in results for x in r['page_errors']];report={'passed':not errors and all(x['passed']for x in checks),'fields':len(fields),'page_errors':errors,'checks':checks,'remaining_fields_with_preexisting_render_errors':sum(bool(x['after']['errors'])for x in checks)};(H/'render-verification.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k!='checks'},flush=True);assert report['passed']
