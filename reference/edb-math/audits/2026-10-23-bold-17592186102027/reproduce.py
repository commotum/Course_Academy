"""Read-only reproduction using the imported source and actual player renderer."""
import functools,http.server,json,sys,threading
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from import_historical_question_content import Renderer
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def main():
 entity=json.loads((HERE/'entity.json').read_text())[0][0]
 stored=entity[':tutorial/content'];candidate=stored.replace('** Step 1**','**Step 1**').replace('** Step 2**','**Step 2**')
 source=ROOT/'reference/mathacademy/question-capture/14004889/tutorial-840.html'
 soup=BeautifulSoup(source.read_text(),'html.parser')
 nodes=[n for n in soup.find_all(['b','strong']) if 'Step' in n.get_text()]
 report={'source':str(source.relative_to(ROOT)),'source_nodes':[str(n) for n in nodes],
  'legacy_converter_output':[Renderer('1159').text(n) for n in nodes]}
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
 threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
 fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page()
  page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html') if r.request.url==origin+'/fixture' else r.continue_() if r.request.url.startswith(origin+'/') else r.abort())
  page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
  report['player']=page.evaluate('''({stored,candidate})=>Object.fromEntries(Object.entries({stored,candidate}).map(([key,text])=>{const node=render(text,'prose',[]);return [key,{bold_labels:[...node.querySelectorAll('strong')].map(n=>n.textContent),step_paragraphs:[...node.querySelectorAll('p')].filter(n=>/Step [123]/.test(n.textContent)).map(n=>n.innerHTML)}]}))''',{'stored':stored,'candidate':candidate})
  browser.close()
 server.shutdown();(HERE/'reproduction.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
