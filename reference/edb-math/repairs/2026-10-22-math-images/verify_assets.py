"""Render each selected recovery; roundtrip reconstructed math to its source tree."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
from match import JS
from resolve import key
from player_tex import normalize_asset
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];RAW=ROOT/'.local/edb/math-image-import-audit-2026-10-22'
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def main():
 targets=json.loads((RAW/'repair-target-fingerprints.json').read_text());source=json.loads((RAW/'repair-source-svgs.json').read_text());rows=json.loads((HERE/'replacements.json').read_text());rows.update(json.loads((HERE/'reconstructed-candidates.json').read_text()))
 for file in ['manual-recoveries.json']:
  if (HERE/file).exists():rows.update(json.loads((HERE/file).read_text()))
 for path,v in rows.items():v['tex']=normalize_asset(path,v['tex'],source[path])
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
 previous=json.loads((HERE/'validated-replacements.json').read_text()) if (HERE/'validated-replacements.json').exists() else {}
 # Retain successful unchanged render checks; rerender all new/changed formulas.
 prior={r['path']:r for r in json.loads((HERE/'asset-validation.json').read_text())} if (HERE/'asset-validation.json').exists() else {}
 results=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page(viewport={'width':1600,'height':1200})
  page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort())
  page.goto(origin+'/fixture');page.wait_for_function('window.ready === true');page.evaluate('() => {window.fingerprint='+JS+';}')
  targets={}
  for i in range(0,len(source),100):targets.update(page.evaluate('rows=>Object.fromEntries(rows.map(([p,s])=>[p,fingerprint(s)]))',list(source.items())[i:i+100]))
  (RAW/'repair-target-fingerprints.json').write_text(json.dumps(targets))
  pending=[]
  for path,row in rows.items():
   if path in prior and path in previous and previous[path]['tex']==row['tex']:results.append(prior[path])
   else:pending.append((path,row))
  print('new or changed render checks',len(pending),flush=True)
  for i in range(0,len(pending),100):
   result=page.evaluate('''async rows=>{const out=[];for(const [path,r] of rows){try{const n=await MathJax.tex2svgPromise(r.tex,{display:true});out.push({path,fp:fingerprint(n.outerHTML),errors:[...n.querySelectorAll('[data-mml-node="merror"], [data-mjx-error]')].map(n=>n.textContent),svg:n.outerHTML})}catch(e){out.push({path,error:String(e)})}}return out}''',pending[i:i+100]);results.extend(result)
  failed=[];accepted={}
  for r in results:
   path=r['path'];method=rows[path]['method'];r['tree_matches']=bool(r.get('fp') and key(r['fp'])==key(targets[path]))
   okay=not(r.get('error') or r.get('errors') or '5C:red' in r.get('fp','')) and (not targets[path] or r['tree_matches'])
   if okay:accepted[path]=rows[path]
   else:failed.append(r)
  for e in json.loads((HERE/'remaining-title-errors.json').read_text()):
   path=e['path'];page.evaluate('s=>{document.body.innerHTML=s;document.body.style.background="white";document.querySelector("svg").style.fontSize="18px"}',source[path]);page.locator('svg').screenshot(path=str(RAW/(Path(path).stem+'.png')))
  browser.close()
 server.shutdown()
 (HERE/'asset-validation.json').write_text(json.dumps([{k:v for k,v in r.items() if k!='svg'} for r in results],indent=2)+'\n');(RAW/'repair-failed-renders.json').write_text(json.dumps(failed,ensure_ascii=False,indent=2)+'\n');(HERE/'validated-replacements.json').write_text(json.dumps(accepted,ensure_ascii=False,indent=2)+'\n');(HERE/'remaining-assets.json').write_text(json.dumps([p for p in targets if p not in accepted],indent=2)+'\n')
 print('validated',len(accepted),'remaining',len(targets)-len(accepted),'failed',len(failed))
if __name__=='__main__':main()
