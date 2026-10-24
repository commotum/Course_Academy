"""Confirm editor selection using the real blankInput and MathLive modules."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def main():
 changes=json.load(open(H/'changes.json'));fixture='''<!doctype html><link rel="stylesheet" href="/ui/learning.css"><main id="content"></main><script type="module">import {blankInput,loadMathInputs} from '/ui/question-fields.js';await loadMathInputs();window.blankInput=blankInput;window.ready=true;</script>''';server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';page_errors=[]
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,timeout=15000);page=b.new_page();page.on('pageerror',lambda e:page_errors.append(str(e)));page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html') if r.request.url==origin+'/fixture' else r.continue_() if r.request.url.startswith(origin+'/') else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
  editors=page.evaluate('''rows=>rows.map(row=>{const out={answer:row.answer};for(const [name,type] of [['before','text'],['after','math']]){const input=blankInput({type:'blank',correctAnswer:{type,value:row.value}},'Answer',row.field);content.replaceChildren(input);out[name]=input.tagName;}return out})''',changes)
  shortcuts={}
  for shortcut in ['pi','sqrt']:
   page.evaluate("()=>content.replaceChildren(blankInput({type:'blank',correctAnswer:{type:'math',value:''}},'Answer','test'))");page.wait_for_timeout(250);page.locator('math-field').evaluate('n=>n.focus()');page.wait_for_timeout(100);page.keyboard.type(shortcut,delay=100);page.keyboard.press('Space');page.wait_for_timeout(100);shortcuts[shortcut]=page.locator('math-field').evaluate('n=>n.value')
  b.close()
 server.shutdown();(H/'ui-diagnostics.json').write_text(json.dumps({'editors':editors,'shortcuts':shortcuts,'errors':page_errors},indent=2)+'\n');print('UI diagnostics',json.dumps({'editors':editors,'shortcuts':shortcuts,'errors':page_errors}));assert all(r['before']=='INPUT' and r['after']=='MATH-FIELD' for r in editors);assert r'\pi' in shortcuts['pi'] and r'\sqrt' in shortcuts['sqrt'];assert not page_errors;report={'editors':editors,'shortcuts':shortcuts,'page_errors':page_errors,'database_writes':0,'passed':True};(H/'ui-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
