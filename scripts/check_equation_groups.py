#!/usr/bin/env python3
"""Exercise responsive groups through all four real page renderers, read-only."""
import functools,http.server,json,sys,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];H=R/'reference/edb-math/repairs/2026-10-30-parametric-layout'
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def main():
 items=json.loads((H/'render-input.json').read_text());fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';checks=[];examples=[]
 try:
  with sync_playwright()as p:
   browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1100,'height':1100})
   page.route('**/fixture',lambda r:r.fulfill(body=fixture,content_type='text/html'));page.goto(origin+'/fixture');page.wait_for_function('window.ready')
   page.evaluate('''async()=>{
    const {marked}=await import('/ui/vendor/marked/marked.esm.js');
    const {romanLists}=await import('/ui/prose-lists.js');
    const {inlinePrompt}=await import('/ui/question-fields.js');
    const {protectMath}=await import('/ui/math-protection.js');
    const {decorateEquationGroups}=await import('/ui/equation-groups.js');
    window.renderers={};
    const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
    for(const name of ['learning','topic','course','activity']){
      const source=await(await fetch('/ui/'+name+'.js')).text();
      let code=source.slice(source.indexOf('function escapeHTML('),source.indexOf(name==='topic'||name==='course'?'function loadMath(':'function answerValue('));
      if(name==='learning'){const i=source.indexOf('function fieldLabel(');code=source.slice(i,source.indexOf('\\n}',i)+2)+';'+code;}
      const fn=new Function('el','marked','romanLists','inlinePrompt','protectMath','decorateSourceTables','decorateEquationGroups',code+';return markdown;');
      const render=fn(el,marked,romanLists,inlinePrompt,protectMath,window.decorateSourceTables,decorateEquationGroups);
      renderers[name]=value=>name==='activity'?render(value):render(value,'prose');
    }
   }''')
   for surface in['learning','topic','course','activity']:
    # Each page shares the exact same responsive decorator, but has its own Markdown path.
    for off in range(0,len(items),35):
     batch=items[off:off+35]
     page.evaluate('''async ({items,surface})=>{MathJax.typesetClear([content]);content.replaceChildren();for(const item of items)content.append(renderers[surface](item.value));await MathJax.typesetPromise([content]);}''',{'items':batch,'surface':surface})
     for width,font in[(760,17),(500,17),(320,17),(240,17),(320,25.5),(760,17)]:
      result=page.evaluate('''async ({width,font})=>{content.style.width=width+'px';for(const child of content.children)child.style.fontSize=font+'px';await new Promise(requestAnimationFrame);const groups=[...content.querySelectorAll('.equation-group')];return {groups:groups.length,items:groups.reduce((s,g)=>s+g.children.length,0),errors:content.querySelectorAll('[data-mml-node="merror"]').length,group_overflows:groups.filter(g=>g.scrollWidth>g.clientWidth+1).length,broken_items:groups.flatMap(g=>[...g.children]).filter(n=>n.querySelectorAll('mjx-container').length!==1).length,local_scroll_fallbacks:groups.flatMap(g=>[...g.children]).filter(n=>n.scrollWidth>n.clientWidth+1).length};}''',{'width':width,'font':font})
      assert not any(result[k]for k in['errors','group_overflows','broken_items']),(surface,off,width,font,result)
      checks.append({'surface':surface,'offset':off,'fields':len(batch),'width':width,'font_px':font,**result})
    print(surface,'passed',len(items),'fields at six width/font states',flush=True)
   for eid in[17592186335959,17592186535273,17592186557691]:
    item=next(i for i in items if i['entity']==eid and i['attribute']=='question/problem')
    page.evaluate('''async value=>{MathJax.typesetClear([content]);content.replaceChildren(renderers.learning(value));content.firstChild.style.fontSize='17px';await MathJax.typesetPromise([content]);window.savedGroupItems=[...content.querySelectorAll('.equation-group-item')];}''',item['value'])
    states=[]
    for width in[760,240,760]:
     r=page.evaluate('''async width=>{content.style.width=width+'px';await new Promise(requestAnimationFrame);let g=content.querySelector('.equation-group');let nodes=[...g.children],rects=nodes.map(n=>n.getBoundingClientRect());return {width,one_row:Math.max(...rects.map(r=>r.top))<Math.min(...rects.map(r=>r.bottom)),same_nodes:nodes.every((n,i)=>n===savedGroupItems[i]),group_overflow:g.scrollWidth>g.clientWidth+1,individual_overflow:nodes.some(n=>n.scrollWidth>n.clientWidth+1),gap:rects[1].left-rects[0].right};}''',width)
     assert r['same_nodes']and not r['group_overflow']and not r['individual_overflow'];assert r['one_row']==(width==760)
     if width==760:assert r['gap']>=33
     states.append(r)
     if eid==17592186557691 and width in[240,760]:page.locator('#content').screenshot(path=str(H/f'responsive-{width}.png'))
    examples.append({'entity':eid,'states':states})
   negative=page.evaluate(r'''async()=>{const {decorateEquationGroups}=await import('/ui/equation-groups.js');let host=document.createElement('div');host.innerHTML='<pre>$$x=1,y=2$$</pre><code>$$x=1,y=2$$</code><math-field>$$x=1,y=2$$</math-field>';host.append(document.createTextNode('\\$\\$x=1,y=2\\$\\$'));decorateEquationGroups(host);return host.querySelectorAll('.equation-group').length;}''');assert negative==0
   browser.close()
 finally:server.shutdown();server.server_close()
 result={'passed':True,'production_renderers':['learning','topic','course','activity'],'fields_per_renderer':len(items),'width_font_checks':checks,'example_resize_checks':examples,'code_mathlive_escaped_literals_preserved':True,'database_writes':0};(H/'responsive-verification.json').write_text(json.dumps(result,indent=2)+'\n');print('All responsive renderers and example resize/spacing checks passed.')
if __name__=='__main__':main()
