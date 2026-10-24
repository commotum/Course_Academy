"""Read-only rendering and original-MathML importer comparison."""
import functools,http.server,json,threading,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def main():
 fields=json.loads((H/'fields.json').read_text());changes=json.loads((H/'preview-changes.json').read_text());proof=json.loads((H/'source-table-proof.json').read_text());server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();errors=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page(viewport={'width':1100,'height':900});page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html') if r.request.url==origin+'/fixture' else r.continue_() if r.request.url.startswith(origin+'/') else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
  reports=page.evaluate(r'''async rows=>{const out=[];for(const row of rows){const n=render(row.value,'prose',[]);content.replaceChildren(n);const rawHtml=n.innerHTML;let thrown=null;try{await MathJax.typesetPromise([n])}catch(e){thrown=String(e)}const math=[...MathJax.startup.document.math].filter(m=>n.contains(m.typesetRoot));const tables=[];for(const m of math)m.root.walkTree(node=>{if(node.kind==='mtable')tables.push({tex:m.math,rows:node.childNodes.length,columns:node.childNodes.map(r=>r.childNodes.length),columnalign:node.attributes.get('columnalign'),rowspacing:node.attributes.get('rowspacing'),frame:node.attributes.get('frame'),columnlines:node.attributes.get('columnlines'),rowlines:node.attributes.get('rowlines')})});const walker=document.createTreeWalker(n,NodeFilter.SHOW_TEXT);let node;const leaks=[];while(node=walker.nextNode()){if(node.parentElement.closest('mjx-container,math,script,style,textarea,math-field'))continue;if(/\\(?:begin|end|frac|sqrt)\b|\[\/?math\]/.test(node.textContent))leaks.push(node.textContent)}const problems=[...n.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(e=>({text:e.textContent,error:e.getAttribute('data-mjx-error')}));const widths=[...n.querySelectorAll('mjx-container')].map(e=>({width:e.getBoundingClientRect().width,available:e.parentElement.getBoundingClientRect().width,scrollWidth:e.scrollWidth}));out.push({entity:row.entity,attribute:row.attribute,kind:row.kind,math_items:math.length,math_errors:problems,raw_tex_leaks:leaks,thrown,tables,widths});MathJax.typesetClear([n])}return out}''',fields)
  for c in changes:
   for side in ['before','after']:
    page.evaluate("async text=>{MathJax.typesetClear([content]);content.replaceChildren(render(text,'prose',[]));await MathJax.typesetPromise([content]);await document.fonts.ready}",c[side]);page.screenshot(path=str(H/f"{c['entity']}-{side}.png"),full_page=True)
  imports=[];scratch=browser.new_page();scratch.route('**/*',lambda r:r.abort())
  for row in proof:
   markup='<div id="fixture"><div class="questionWidget-text"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block">'+row['source_mathml']+'</math></div></div>';scratch.set_content(markup);result={'entity':row['entity']}
   for name,path in [('question_capture_dom',R/'scripts/question_capture/dom.js'),('capture_browser_extract',R/'capture/scripts/browser/extract.js')]:
    q=scratch.locator('#fixture').evaluate(path.read_text());result[name]={'problem':q['problem'],'errors':q['errors']}
   imports.append(result)
  scratch.close();browser.close()
 server.shutdown();(H/'render-results.json').write_text(json.dumps(reports,indent=2)+'\n');(H/'importer-reproduction.json').write_text(json.dumps(imports,indent=2)+'\n');summary={'fields':len(reports),'entities':len({r['entity'] for r in reports}),'math_errors':sum(len(r['math_errors']) for r in reports),'raw_tex_leaks':sum(len(r['raw_tex_leaks']) for r in reports),'thrown':[r for r in reports if r['thrown']],'page_errors':errors,'borders_lost_in_all_current_limit_tables':all(t['frame']=='none' and t['columnlines']=='none' and t['rowlines']=='none' for r in reports for t in r['tables'] if t['tex'].startswith(r'\begin{aligned}x &'))};(H/'render-verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2));print(json.dumps(imports,indent=2))
if __name__=='__main__':main()
