"""Actual player Markdown, answer-value and MathJax before/after verification."""
import functools,hashlib,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def main():
 fields=json.loads((H/'fields.json').read_text());known={}
 if (H/'render-checks.jsonl').exists():
  for line in (H/'render-checks.jsonl').read_text().splitlines():
   r=json.loads(line);known[r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']]=r
 pending=[r for r in fields if (r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']) not in known]
 fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
 fixture=fixture.replace("source.indexOf('function answerValue(')","source.indexOf('function loadMath(')")
 fixture=fixture.replace("labels+';'+renderer+'; return markdown;'", "source.match(/^function short\\(.*$/m)[0]+';'+labels+';'+renderer+'; return {markdown,answerValue};'")
 fixture=fixture.replace('window.render = make(el,marked,romanLists,inlinePrompt,protectMath);','const functions=make(el,marked,romanLists,inlinePrompt,protectMath);window.render=functions.markdown;window.renderAnswer=functions.answerValue;')
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';errors=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page(viewport={'width':1100,'height':900});page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
  for offset in range(0,len(pending),20):
   reports=page.evaluate(r'''async rows=>{let results=[];for(const row of rows){const result={entity:row.entity,attribute:row.attribute,before_sha256:row.before_sha256,after_sha256:row.after_sha256};for(const side of ['before','after']){const n=row.attribute==='answer/value'?renderAnswer({type:'math',value:row[side]}):render(row[side],'prose',[]);content.replaceChildren(n);let thrown=null;try{await MathJax.typesetPromise([n])}catch(e){thrown=String(e)}const math=[...MathJax.startup.document.math].filter(m=>n.contains(m.typesetRoot));const tokens=[];for(const m of math){const t=[];m.root.walkTree(node=>{if(node.kind==='text'){const v=node.getText();if(!['[',']','(',')','{','}','|','‖',''].includes(v))t.push(v)}});tokens.push(t)}const errors=[...n.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(e=>e.getAttribute('data-mjx-error')||e.textContent);const walker=document.createTreeWalker(n,NodeFilter.SHOW_TEXT),leaks=[];let text;while(text=walker.nextNode()){if(text.parentElement.closest('mjx-container,math,script,style,textarea,math-field'))continue;if(/\\(?:begin|end|frac|dfrac|sqrt)\b|\[\/?math\]/.test(text.textContent))leaks.push(text.textContent)}result[side]={math_count:math.length,tokens,errors,raw_tex_leaks:leaks,thrown,images:[...n.querySelectorAll('img')].map(e=>e.getAttribute('src'))};MathJax.typesetClear([n]);}result.same_math_values=JSON.stringify(result.before.tokens)===JSON.stringify(result.after.tokens);result.no_new_errors=result.after.errors.every(e=>result.before.errors.includes(e))&&result.after.thrown===result.before.thrown;result.no_new_raw_tex=result.after.raw_tex_leaks.every(e=>result.before.raw_tex_leaks.includes(e));result.same_images=JSON.stringify(result.before.images)===JSON.stringify(result.after.images);result.passed=result.same_math_values&&result.no_new_errors&&result.no_new_raw_tex&&result.same_images&&result.after.math_count>0;results.push(result)}return results}''',pending[offset:offset+20])
   with (H/'render-checks.jsonl').open('a') as out:
    for report in reports:out.write(json.dumps(report)+'\n');known[report['entity'],report['attribute'],report['before_sha256'],report['after_sha256']]=report
   print('Player checked',min(offset+20,len(pending)),'/',len(pending),'new fields',flush=True)
  for row in fields:
   if row['entity'] not in {17592186100705,17592186261594}:continue
   for side in ['before','after']:
    page.evaluate("async ({text,answer})=>{MathJax.typesetClear([content]);content.replaceChildren(answer?renderAnswer({type:'math',value:text}):render(text,'prose',[]));await MathJax.typesetPromise([content])}",{'text':row[side],'answer':row['attribute']=='answer/value'});page.screenshot(path=str(H/f"{row['entity']}-{side}.png"),full_page=True)
  browser.close()
 server.shutdown();current=[known[r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']] for r in fields];failed=[{'entity':r['entity'],'attribute':r['attribute'],'same_math_values':r['same_math_values'],'no_new_errors':r['no_new_errors'],'no_new_raw_tex':r['no_new_raw_tex']} for r in current if not r['passed']];summary={'fields':len(current),'passed':not failed and not errors,'failures':failed,'page_errors':errors,'verified_hashes':[[r['entity'],r['attribute'],r['before_sha256'],r['after_sha256']] for r in current]};(H/'render-verification.json').write_text(json.dumps(summary,indent=2)+'\n');print('Render verification: fields',len(current),'failed',len(failed),'page errors',errors)
if __name__=='__main__':main()
