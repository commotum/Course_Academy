"""Read-only replay of this question's prompt through the actual player renderer."""
import functools,http.server,json,re,sys,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts/question_capture'));from edn import loads
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def main():
 q=loads((HERE/'question.edn').read_text())[0][0];fields=[{'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident']} for f in q[':question/answer-fields']];server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page(viewport={'width':900,'height':500});page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready === true')
  report=page.evaluate('''async ({problem,fields})=>{const out={};for(const [name,text] of [['stored',problem],['without_stray_radio_marker',problem.replace(/\\s*\\{\\{selection\\}\\}\\s*$/,'')]]){const a=render(text,'prose',fields);content.replaceChildren(a);await MathJax.typesetPromise([a]);out[name]={field_locations:[...a.querySelectorAll('.field-location')].map(n=>({text:n.textContent,key:n.dataset.fieldKey||null})),inline_answer_slots:a.querySelectorAll('[data-field-key]').length,math_errors:a.querySelectorAll('[data-mml-node="merror"]').length};MathJax.typesetClear([a])}return out}''',{'problem':q[':question/problem'],'fields':fields});browser.close()
 server.shutdown();assert report['stored']['field_locations']==[{'text':'Answer','key':None}];assert report['stored']['inline_answer_slots']==0;assert report['without_stray_radio_marker']['field_locations']==[];(HERE/'renderer-reproduction.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
