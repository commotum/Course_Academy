#!/usr/bin/env python3
"""Real editor geometry: compact values, longer statements, typing and restore.

Uses the shared player renderer and controls; never calls learner APIs.
"""
import argparse,functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--artifacts',type=Path);args=parser.parse_args()
if args.artifacts:args.artifacts.mkdir(parents=True,exist_ok=True)
fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
fixture=fixture.replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
fixture=fixture.replace("import {inlinePrompt}","import {inlinePrompt,loadMathInputs,blankInput,mountInlineFields}")
fixture=fixture.replace('await MathJax.startup.promise; window.ready=true;',r'''
await loadMathInputs();await MathJax.startup.promise;
window.makeField=blankInput;
window.show=async(problem,fields)=>{
 MathJax.typesetClear([content]);content.replaceChildren();
 const article=document.createElement('article');article.className='lesson-content';
 const card=document.createElement('div');card.className='content-card';
 const form=document.createElement('form');form.addEventListener('submit',e=>e.preventDefault());
 const prompt=render(problem,'prose',fields),list=document.createElement('div');list.className='answer-fields';
 form.append(prompt,list);card.append(form);article.append(card);content.append(article);
 mountInlineFields(prompt,list,fields,field=>{let set=document.createElement('fieldset');set.className='answer-field';set.append(blankInput(field,field.key,field.id,!!field.readOnly));return set});
 await MathJax.typesetPromise([prompt]);await document.fonts.ready;
 await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
};
window.measure=()=>[...content.querySelectorAll('.answer-input,.answer-math')].map(n=>{
 const r=n.getBoundingClientRect(),s=getComputedStyle(n),inner=n.shadowRoot?.querySelector('.ML__content');
 return {name:n.getAttribute('name'),value:n.value,width:r.width,height:r.height,size:n.dataset.inputSize,disabled:n.disabled,
  minWidth:s.minWidth,clipped:!!inner&&inner.scrollWidth>inner.clientWidth+1,
  pageOverflow:document.documentElement.scrollWidth>innerWidth+1};
});window.setValue=async(value,index=0)=>{let n=content.querySelectorAll('.answer-input,.answer-math')[index];n.value=value;n.dispatchEvent(new Event('input',{bubbles:true}));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))};
window.ready=true;
''')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
inequality='Find the solution to the inequality $2<x+5<7.$\n\n{{field-1}}{{field-2}}\n$x\\,<$\n{{field-3}}'
fields=[{'id':i,'key':f'field-{i}','type':'blank','answerType':'math'}for i in range(1,4)]
reports=[];errors=[]
try:
 with sync_playwright()as p:
  browser=p.chromium.launch(headless=True,ignore_default_args=['--hide-scrollbars']);page=browser.new_page(viewport={'width':1100,'height':900});page.on('pageerror',lambda e:errors.append(str(e)))
  page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html')if route.request.url==origin+'/fixture'else route.continue_()if route.request.url.startswith(origin+'/')else route.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
  for width in [1100,768,390,320]:
   page.set_viewport_size({'width':width,'height':900});page.evaluate('([p,f])=>show(p,f)',[inequality,fields]);empty=page.evaluate('measure()')
   assert all(n['size']=='value'and n['width']>=45 and not n['pageOverflow']for n in empty),empty
   for i,value in enumerate(['-3','<','2']):page.evaluate('([v,i])=>setValue(v,i)',[value,i])
   small=page.evaluate('measure()');assert [n['value']for n in small]==['-3','<','2']
   assert all(n['width']<95 and not n['clipped']and not n['pageOverflow']for n in small),small
   if args.artifacts and width in [1100,390]:page.locator('.content-card').screenshot(path=str(args.artifacts/f'inequality-{width}.png'))
   page.evaluate("()=>{const n=content.querySelector('math-field');n.value='';n.focus();for(let s of ['6','p','+','2','q','-','4','p'])n.insert(s)}")
   page.evaluate('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');grown=page.evaluate('measure()')[0]
   assert grown['value']=='6p+2q-4p'and grown['width']>empty[0]['width']+20 and not grown['clipped']and not grown['pageOverflow'],grown
   page.evaluate("setValue('')");cleared=page.evaluate('measure()')[0];assert cleared['width']<grown['width']-20,cleared
   # Fractions and exact solutions grow vertically; a hidden correct answer
   # is never needed to choose either initial width.
   exact=r'\frac{-3+\sqrt{13}}{2}'
   page.evaluate('([p,f])=>show(p,f)',['Give the exact solution.',[{'id':9,'key':'Solution','type':'blank','answerType':'math','response':{'value':exact}}]])
   statement=page.evaluate('measure()')[0];assert statement['size']=='statement'and statement['value']==exact and statement['width']>empty[0]['width']*1.7 and not statement['clipped']and not statement['pageOverflow'],statement
   if args.artifacts and width==1100:page.locator('.content-card').screenshot(path=str(args.artifacts/'exact-solution.png'))
   page.evaluate('([p,f])=>show(p,f)',['Explain {{text}}.',[{'id':10,'key':'text','type':'blank','answerType':'text'}]])
   page.evaluate("setValue('x'.repeat(32))");medium=page.evaluate('measure()')[0];page.evaluate("setValue('x'.repeat(45))");long=page.evaluate('measure()')[0]
   if width==1100:assert long['width']>medium['width']+80,(medium,long)
   assert not long['pageOverflow'],long
   page.evaluate("setValue('a')");short=page.evaluate('measure()')[0];assert short['width']<long['width']-20
   page.evaluate('([p,f])=>show(p,f)',['Saved {{answer}}.',[{'id':11,'key':'answer','type':'blank','answerType':'math','readOnly':True,'response':{'value':'6p+2q-4p'}}]])
   saved=page.evaluate('measure()')[0];assert saved['disabled']and saved['width']>empty[0]['width']+20 and not saved['clipped']and not saved['pageOverflow'],saved
   reports.append({'viewport_width':width,'empty':empty,'short_values':small,'typed_math':grown,'cleared_math':cleared,'restored_exact_solution':statement,'text_medium':medium,'text_long':long,'text_short':short,'read_only':saved})
  assert not errors,errors
  browser.close()
finally:server.shutdown();server.server_close()
if args.artifacts:(args.artifacts/'verification.json').write_text(json.dumps({'passed':True,'page_errors':errors,'cases':reports},indent=2)+'\n')
print('Blank sizing: compact values, growing/shrinking math and text, exact fractions, saved responses and read-only state pass at 4 viewport widths.')
