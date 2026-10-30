"""Check recovered arrows against original SVG and render repaired content."""
import importlib.util,json,sys,functools,http.server,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'2026-10-22-math-images'
sys.path[:0]=[str(OLD),str(ROOT/'scripts')]
from match import JS,Quiet
from resolve import key
from check_math_rendering import check
proof=json.loads((HERE/'source-proof.json').read_text());sources=json.loads((ROOT/'.local/edb/math-image-import-audit-2026-10-22/repair-source-svgs.json').read_text())
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1000,'height':1000})
  page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html') if r.request.url==origin+'/fixture' else r.continue_() if r.request.url.startswith(origin+'/') else r.abort())
  page.goto(origin+'/fixture');page.wait_for_function('window.ready');page.evaluate('window.fingerprint='+JS)
  results=[]
  for row in proof:
   result=page.evaluate('''async r=>{let a=await MathJax.tex2svgPromise(r.after),b=await MathJax.tex2svgPromise(r.before);return {original:fingerprint(r.svg),after:fingerprint(a.outerHTML),before:fingerprint(b.outerHTML)}}''',{**row,'svg':sources[row['asset']]})
   assert key(result['original'])==key(result['after']),row['asset']
   assert key(result['original'])!=key(result['before']),row['asset']
   results.append({'asset':row['asset'],'corrected_matches_source':True,'malformed_rejected':True})
  page.evaluate('''async ()=>{content.replaceChildren();for(const [label,tex] of [['Before','\\\\overset{\\\\to -}{A X}'],['After','\\\\overrightarrow{AX}']]){let p=document.createElement('p');p.textContent=label;content.append(p,await MathJax.tex2svgPromise(tex));}}''')
  page.screenshot(path=str(HERE/'arrow-comparison.png'),full_page=True)
  browser.close()
finally:server.shutdown();server.server_close()
(HERE/'source-render-verification.json').write_text(json.dumps(results,indent=2))
result=check(json.loads((HERE/'render-input.json').read_text()));(HERE/'render-verification.json').write_text(json.dumps(result,indent=2));assert result['passed'],result['failures']
print('Verified',len(results),'source formulas; rejected all malformed versions;',result['fields'],'content fields render without errors')
