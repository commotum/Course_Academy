"""Verify percent glyph restoration through the actual player and MathJax."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def main():
 fields=json.loads((H/'fields.json').read_text());fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace("source.indexOf('function answerValue(')","source.indexOf('function loadMath(')").replace("labels+';'+renderer+'; return markdown;'","source.match(/^function short\\(.*$/m)[0]+';'+labels+';'+renderer+'; return {markdown,answerValue};'").replace('window.render = make(el,marked,romanLists,inlinePrompt,protectMath);','const f=make(el,marked,romanLists,inlinePrompt,protectMath);window.render=f.markdown;window.renderAnswer=f.answerValue;')
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';errors=[];reports=[]
 with sync_playwright()as p:
  browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1100,'height':900});page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html')if route.request.url==origin+'/fixture'else route.continue_()if route.request.url.startswith(origin+'/')else route.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
  for offset in range(0,len(fields),25):
   checked=page.evaluate(r'''async rows=>{let out=[];for(let row of rows){let r={entity:row.entity,attribute:row.attribute,before_sha256:row.before_sha256,after_sha256:row.after_sha256,percent_edits:row.percent_edits};for(let side of ['before','after']){MathJax.typesetClear([content]);let n=row.attribute==='answer/value'?renderAnswer({type:row.render_type,value:row[side]}):render(row[side],'prose',[]);content.replaceChildren(n);let thrown=null;try{await MathJax.typesetPromise([n])}catch(e){thrown=String(e)}let errors=[...n.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(e=>e.getAttribute('data-mjx-error')||e.textContent);r[side]={percentGlyphs:n.querySelectorAll('svg [data-c="25"]').length,errors,thrown,images:[...n.querySelectorAll('img')].map(e=>e.getAttribute('src')),mathCount:n.querySelectorAll('mjx-container').length}}r.percent_restoration=r.after.percentGlyphs-r.before.percentGlyphs===r.percent_edits;r.no_new_errors=r.after.errors.every(e=>r.before.errors.includes(e))&&r.after.thrown===r.before.thrown;r.same_images=JSON.stringify(r.before.images)===JSON.stringify(r.after.images);r.passed=r.percent_restoration&&r.no_new_errors&&r.same_images&&r.after.mathCount>0;out.push(r)}return out}''',fields[offset:offset+25]);reports.extend(checked)
   print('Player verified',min(offset+25,len(fields)),'/',len(fields),flush=True)
  for side in ['before','after']:
   rows=[{'type':f['render_type'],'value':f[side]}for f in fields if f['entity']in {17592186508429,17592186508515,17592186508617,17592186508679}]
   page.evaluate('async rows=>{MathJax.typesetClear([content]);content.replaceChildren(...rows.map(renderAnswer));await MathJax.typesetPromise([content])}',rows);page.screenshot(path=str(H/f'reported-question-{side}.png'),full_page=True)
  browser.close()
 server.shutdown();(H/'render-checks.json').write_text(json.dumps(reports,indent=2)+'\n');failed=[r for r in reports if not r['passed']];summary={'fields':len(reports),'passed':not failed and not errors,'failures':[{'entity':r['entity'],'attribute':r['attribute'],'percent_restoration':r['percent_restoration'],'no_new_errors':r['no_new_errors']}for r in failed],'page_errors':errors,'restored_percent_glyphs':sum(r['after']['percentGlyphs']-r['before']['percentGlyphs']for r in reports),'verified_hashes':[[r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']]for r in reports]};(H/'render-verification.json').write_text(json.dumps(summary,indent=2)+'\n');print('Render checks:',len(reports),'failures:',len(failed),'page errors:',errors)
if __name__=='__main__':main()
