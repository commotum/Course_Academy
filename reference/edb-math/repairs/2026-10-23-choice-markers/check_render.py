"""Replay all repaired statements through the actual question player renderer."""
import base64,functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
JS=r'''async rows=>{const out=[];for(const row of rows){const versions={};for(const v of ['before','after']){const a=render(row[v],'prose',row.fields);content.replaceChildren(a);await MathJax.typesetPromise([a]);versions[v]={bogus:[...a.querySelectorAll('.field-location')].filter(n=>!n.dataset.fieldKey).length,slots:[...a.querySelectorAll('[data-field-key]')].map(n=>n.dataset.fieldKey),errors:a.querySelectorAll('[data-mml-node="merror"]').length};MathJax.typesetClear([a]);a.remove()}out.push({entity:row.entity,...versions})}return out}'''
def main():
 rows=json.loads((HERE/'fields.json').read_text())
 for row in rows:row['fields']=[{'key':f[':answer-field/key'],'type':f[':answer-field/type']} for f in row['answer_fields']]
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();errors=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page(viewport={'width':950,'height':800});page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if r.request.resource_type=='image':return r.fulfill(body=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jk1kAAAAASUVORK5CYII='),content_type='image/png')
   if r.request.url==origin+'/fixture':return r.fulfill(body=fixture,content_type='text/html')
   return r.continue_() if r.request.url.startswith(origin+'/') else r.abort()
  page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready === true');results=[]
  for i in range(0,len(rows),20):results+=page.evaluate(JS,rows[i:i+20])
  for eid in [17592186491432,17592186551486,17592186484418]:
   row=next(r for r in rows if r['entity']==eid)
   for version in ['before','after']:
    page.evaluate("async ({row,version})=>{MathJax.typesetClear([content]);content.replaceChildren(render(row[version],'prose',row.fields));await MathJax.typesetPromise([content])}",{'row':row,'version':version})
    (HERE/'review').mkdir(exist_ok=True);page.screenshot(path=str(HERE/'review'/f'{eid}-{version}.png'),full_page=True)
  browser.close()
 server.shutdown()
 failed=[r for r in results if r['after']['bogus'] or r['before']['slots']!=r['after']['slots'] or r['after']['errors']>r['before']['errors']]
 report={'questions':len(results),'bogus_labels_before':sum(r['before']['bogus'] for r in results),'bogus_labels_after':sum(r['after']['bogus'] for r in results),'new_math_errors':sum(max(0,r['after']['errors']-r['before']['errors']) for r in results),'failed_questions':len(failed),'page_errors':errors,'results':results}
 (HERE/'render-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='results'}));assert not errors and not failed
if __name__=='__main__':main()
