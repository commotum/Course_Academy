"""Test source-backed table presentation through the current player renderer."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3];A=R/'reference/edb-math/audits/2026-10-24-html-table-fidelity';W=R/'.local/edb/html-table-fidelity'
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def main():
 cases=json.loads((A/'prototype-cases.json').read_text());byid={r[0][':db/id']:r[0][':question/answer-fields']for r in json.loads((A/'prototype-fields.json').read_text())}
 for c in cases:
  c['fields']=[]
  for f in byid.get(c['entity'],[]):
   c['fields'].append({'id':f[':db/id'],'key':f[':answer-field/key'],'type':str(f[':answer-field/type'][':db/ident']).split('/')[-1],'answerType':'math','choices':[{'id':a[':db/id'],'value':a[':answer/value'],'type':str(a[':answer/type'][':db/ident']).split('/')[-1]}for a in f.get(':answer-field/choices',[])]})
 fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
 # Exercise production CSS and its shared decorator, without prototype styles.
 fixture=fixture.replace('html{color-scheme:light}body{background:white;color:#171717}.content-card{background:white}','')
 fixture=fixture.replace('import {inlinePrompt}', 'import {inlinePrompt,mountInlineFields,blankInput,richSelect,loadMathInputs}')
 extra="""
import {sourceTable} from '/reference/edb-math/repairs/2026-10-24-html-table-fidelity/build-table.js';
await loadMathInputs();await MathJax.startup.promise;
window.sourceTable=sourceTable;
window.show=async(c,after=true)=>{
 MathJax.typesetClear([content]);content.replaceChildren();
 const article=document.createElement('article');article.className='lesson-content';const card=document.createElement('div');card.className='content-card';
 const prompt=render(after?sourceTable(c.source,c.prototype_rows):c.old_table,'prose',c.fields),list=document.createElement('div');
 card.append(prompt,list);article.append(card);content.append(article);
 mountInlineFields(prompt,list,c.fields,f=>{let set=document.createElement('fieldset');set.dataset.fieldId=String(f.id);if(f.type==='blank')set.append(blankInput(f,f.key,f.id));else if(f.type==='select'){let select=document.createElement('select');select.name=String(f.id);select.setAttribute('aria-label',f.key);for(let a of [{id:'',value:'Select…'},...f.choices]){let option=document.createElement('option');option.value=String(a.id);option.textContent=a.value;select.append(option)}set.append(richSelect(select,f.choices,a=>render(a.type==='math'?'$'+a.value+'$':a.value),a=>a.id,async n=>MathJax.typesetPromise([n])))}return set});
 await MathJax.typesetPromise([content]);await document.fonts.ready;decorateSourceTables(content);await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
 const tokens=[];for(let m of MathJax.startup.document.math){if(!content.contains(m.typesetRoot))continue;let t=[];m.root.walkTree(n=>{if(['mi','mn','mo','mtext','ms'].includes(n.kind))t.push(n.getText())});tokens.push(t)}
 const table=prompt.querySelector('table'),box=table.getBoundingClientRect(),p=prompt.getBoundingClientRect(),wrap=table.parentElement;
 const l=rgb=>{let c=rgb.slice(0,3).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4});return c[0]*.2126+c[1]*.7152+c[2]*.0722};
 return {tokens,cells:[...table.querySelectorAll('td,th')].map(n=>{let style=getComputedStyle(n),bg=style.backgroundColor.match(/[\\d.]+/g).map(Number),fg=style.color.match(/[\\d.]+/g).map(Number),a=l(bg),b=l(fg);return {tag:n.tagName,rowspan:n.rowSpan,colspan:n.colSpan,align:style.textAlign,fill:style.backgroundColor,shade:n.hasAttribute('data-fill'),contrast:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)}}),mathErrors:prompt.querySelectorAll('[data-mjx-error],mjx-merror').length,editors:[...prompt.querySelectorAll('input,select,math-field')].map(n=>({name:n.getAttribute('name'),value:n.value})),pageOverflow:document.documentElement.scrollWidth>innerWidth+1,tableWidth:box.width,promptWidth:p.width,horizontalScroll:wrap.scrollWidth>wrap.clientWidth+1,verticalScroll:wrap.scrollHeight>wrap.clientHeight+1,centered:Math.abs((box.left+box.right-p.left-p.right)/2)<2};
};window.ready=true;
"""
 fixture=fixture.replace('await MathJax.startup.promise; window.ready=true;',extra)
 matches=json.loads((H/'compiled.json').read_text())
 for c in cases:
  m=next(m for m in matches if m['entity']==c['entity']and m['attribute']==c['attribute']);c.update(source=m['source'],prototype_rows=m['prototype_rows'],old_table=m['before_table'])
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';reports=[];errors=[]
 try:
  with sync_playwright()as p:
   browser=p.chromium.launch(headless=True,ignore_default_args=['--hide-scrollbars']);page=browser.new_page(viewport={'width':1100,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)))
   page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html')if route.request.url==origin+'/fixture'else route.continue_()if route.request.url.startswith(origin+'/')else route.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
   compiled=json.loads((H/'compiled.json').read_text())
   for theme in ['light','dark']:
    page.evaluate('t=>document.documentElement.dataset.theme=t',theme)
    for width in [1100,768,390]:
     page.set_viewport_size({'width':width,'height':1000})
     for c in cases:
      before=page.evaluate('c=>show(c,false)',c);after=page.evaluate('c=>show(c,true)',c)
      assert before['tokens']==after['tokens'],('Math changed',c['label'],before['tokens'],after['tokens'])
      assert after['mathErrors']==0 and not after['pageOverflow']and not after['verticalScroll'],(c['label'],theme,width,after)
      def expected_cells(spec,rows):
       out=[]
       for i,row in enumerate(spec['cells']):
        for j,cell in enumerate(row):
         out.append(cell);value=rows[i][j]
         if isinstance(value,dict):
          for part in value.get('parts',[value]):
           if isinstance(part,dict):out.extend(expected_cells(part['table'],part['rows']))
       return out
      expected=expected_cells(c['source'],c['prototype_rows']);assert len(expected)==len(after['cells'])
      assert all(actual['tag'].lower()==source['tag']and actual['rowspan']==int(source['attrs'].get('rowspan',1))and actual['colspan']==int(source['attrs'].get('colspan',1))for source,actual in zip(expected,after['cells']))
      assert all(cell['contrast']>=4.5 for cell in after['cells']if cell['shade']),(c['label'],theme,'contrast')
      assert [x['name']for x in before['editors']]==[x['name']for x in after['editors']],('Field IDs changed',c['label'])
      if c['label']=='limits-table':assert after['centered']and all(cell['tag']=='TD'and cell['align']=='center'for cell in after['cells'])
      if width in [1100,390]and c['label']in ['limits-table','merged-direction-labels','editable-sign-chart','wide-degree-radian-table','nested-statistical-tables']:page.locator('.content-card').screenshot(path=str(H/f"{c['label']}-{theme}-{width}.png"))
      reports.append({'label':c['label'],'entity':c['entity'],'theme':theme,'width':width,'before':before,'after':after})
   browser.close()
 finally:server.shutdown();server.server_close()
 assert not errors,errors
 report={'passed':True,'cases':len(reports),'representative_tables':len(cases),'compiled_source_backed_replacements':len(compiled),'page_errors':errors,'database_writes':0,'checks':reports};(H/'layout-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('Passed production layout cases',len(reports),'compiled replacements',len(compiled),'database writes 0')
if __name__=='__main__':main()
