"""Read-only reproduction of Markdown/MathJax stages and an in-memory correction."""
import functools,http.server,json,re,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def main():
 q=json.loads((HERE/'question.json').read_text());s=q[':question/worked-solution']
 # Test the same equations under the supported Markdown math contract only.
 candidate=s.replace(r'\begin{align*}',r'$$'+'\n'+r'\begin{aligned}').replace(r'\end{align*}',r'\end{aligned}'+'\n$$')
 candidate=candidate.replace('\\begin{eqnarray}\n \\eqalign{','$$\n\\begin{aligned}').replace('\\pi\\sqrt{2}.}\n\\end{eqnarray}','\\pi\\sqrt{2}.\n\\end{aligned}\n$$')
 candidate=re.sub(r'\$\$([\s\S]*?)\$\$',lambda m:'$$'+re.sub(r'\n\s*\n','\n',m[1])+'$$',candidate)
 (HERE/'candidate-worked-solution.md').write_text(candidate+'\n')
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();errors=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page(viewport={'width':1200,'height':900});page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
  report=page.evaluate(r'''async ({stored,candidate})=>{const out={};for(const [name,text] of [['stored',stored],['mathjax_without_markdown',stored],['candidate',candidate]]){const a=name==='mathjax_without_markdown'?document.createElement('div'):render(text,'prose',[]);if(name==='mathjax_without_markdown')a.textContent=text;content.replaceChildren(a);const before=a.innerHTML;let thrown=null;try{await MathJax.typesetPromise([a])}catch(e){thrown=String(e)}const items=[...MathJax.startup.document.math].filter(m=>a.contains(m.typesetRoot));out[name]={before_mathjax_html:before,after_mathjax_html:a.innerHTML,thrown,math_items:items.map(m=>({tex:m.math,display:m.display})),errors:[...a.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>({text:n.textContent,title:n.getAttribute('data-mjx-error')})),visible_text:a.textContent,paragraph_count:a.querySelectorAll('p').length};MathJax.typesetClear([a])}return out}''',{'stored':s,'candidate':candidate})
  for name,text in [('stored',s),('candidate',candidate)]:
   page.evaluate("async text=>{MathJax.typesetClear([content]);content.replaceChildren(render(text,'prose',[]));await MathJax.typesetPromise([content])}",text);page.screenshot(path=str(HERE/(name+'.png')),full_page=True)
  browser.close()
 server.shutdown();report['page_errors']=errors;(HERE/'renderer-reproduction.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:{'errors':v.get('errors'),'math_items':v.get('math_items'),'paragraph_count':v.get('paragraph_count'),'visible_text':v.get('visible_text')} for k,v in report.items() if isinstance(v,dict)},indent=2))
if __name__=='__main__':main()
