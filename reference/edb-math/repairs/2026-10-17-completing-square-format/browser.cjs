// Requires the local app on port 8765. Uses DOM geometry; no screenshots or image loading.
const fs=require('fs'),os=require('os'),path=require('path'),{spawn}=require('child_process');
const root='/home/jake/Developer/Course_Academy';
const assert=require('node:assert/strict');
const group=(values,stacked=true)=>'<div class="matrix-operands'+(stacked?' matrix-operands-stacked':'')+'">'+values.map(value=>'<div>$'+value+'$</div>').join('')+'</div>';
const matrix=rows=>String.raw`\begin{bmatrix}`+rows.map(row=>row.join(' & ')).join(String.raw` \\ `)+String.raw`\end{bmatrix}`;
const cases=JSON.parse(fs.readFileSync('/home/jake/Developer/Course_Academy/reference/edb-math/repairs/2026-10-17-completing-square-format/render-cases.json','utf8'));
const learning=fs.readFileSync(root+'/ui/learning.js','utf8');
const renderers=learning.slice(learning.indexOf('function markdown('),learning.indexOf('function loadMath('))+learning.slice(learning.indexOf('function choiceOrder('),learning.indexOf('function collectResponses('));
const html=`<!doctype html><html data-theme="light"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="img-src 'none'; connect-src 'none'"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><body><main class="lesson-main" id="main"></main><script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {romanLists} from '/ui/prose-lists.js';
import {inlinePrompt,loadMathInputs,mountInlineFields,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput} from '/ui/question-fields.js';
const el=(tag,className='',text='')=>{const n=document.createElement(tag);n.className=className;n.textContent=text;return n;};
const short=x=>String(x||'').split('/').at(-1),fieldLabel=k=>k,assetURL=x=>'',typeset=()=>{};
const escapeHTML=text=>String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
${renderers}
await loadMathInputs();await MathJax.startup.promise;
window.renderBatch=async(entries,mode)=>{MathJax.typesetClear([main]);main.replaceChildren();let exceptions=[];
for(const data of entries){const article=el('article','content-card');article.dataset.entity=data.entity;main.append(article);
try{const fields=structuredClone(data.fields);if(mode!=='edit')for(const f of fields)if(f.correctAnswer){f.response=mode==='correct'?{...f.correctAnswer,choiceId:f.correctAnswer.id}:{value:'-999999',choiceId:-1};f.grade=mode==='correct'?'correct':'incorrect';}
const prompt=markdown(data.problem,'prose',fields),rest=el('div','answer-fields');article.append(prompt,rest);mountInlineFields(prompt,rest,fields,f=>fieldControl(f,mode!=='edit',data.entity,data.problem,mode==='edit'?'':mode));
if(data.solution)article.append(markdown('**Solution:**\\n\\n'+data.solution));
for(const img of article.querySelectorAll('img'))img.remove();
}catch(e){exceptions.push({entity:data.entity,error:e.message});}}
await MathJax.typesetPromise([main]);await document.fonts.ready;
return {exceptions,items:[...main.children].map(article=>{const prompt=article.querySelector('.prose'),table=prompt?.querySelector('.matrix-answer table'),cells=table?[...table.querySelectorAll('td')]:[],operands=[...(prompt?.querySelectorAll('.matrix-operands > div')||[])],box=prompt?.getBoundingClientRect(),center=box?(box.left+box.right)/2:0;
return {entity:Number(article.dataset.entity),wrappers:operands.map(n=>{const c=getComputedStyle(n),m=n.querySelector('mjx-container'),v=m?.querySelector('svg'),r=n.getBoundingClientRect(),mr=m?.getBoundingClientRect(),vr=v?.getBoundingClientRect();return {width:n.clientWidth,height:n.clientHeight,scrollWidth:n.scrollWidth,scrollHeight:n.scrollHeight,overflowX:c.overflowX,overflowY:c.overflowY,lineHeight:c.lineHeight,wrapperTop:r.top,wrapperBottom:r.bottom,mathTop:mr?.top,mathBottom:mr?.bottom,svgTop:vr?.top,svgBottom:vr?.bottom,mathDisplay:m?getComputedStyle(m).display:null};}),mathCount:article.querySelectorAll('mjx-container').length,unknownGlyphs:[...article.querySelectorAll('[data-mml-node="mtext"]')].filter(n=>n.querySelector('text')).map(n=>n.textContent),mathErrors:[...article.querySelectorAll('[data-mjx-error],mjx-merror')].map(x=>x.getAttribute('data-mjx-error')||x.textContent),overflow:article.scrollWidth>article.clientWidth+1,contentOverflow:prompt?prompt.scrollWidth>prompt.clientWidth+1:false,fields:article.querySelectorAll('[data-answer-input="true"]').length,blankEditors:article.querySelectorAll('math-field').length,bracketed:!!table,borderless:cells.every(c=>getComputedStyle(c).borderTopWidth==='0px'&&getComputedStyle(c).borderLeftWidth==='0px'),givenCount:operands.length,centered:operands.every(n=>{const b=n.getBoundingClientRect();return Math.abs((b.left+b.right)/2-center)<1}),empty:!prompt?.textContent.trim()};})};};window.ready=true;
</script>`;
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'matrix-quality-'));const child=spawn('/usr/bin/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--remote-debugging-pipe','--user-data-dir='+profile,'about:blank'],{stdio:['ignore','ignore','ignore','pipe','pipe']});
let id=0,buf='',session;const pending=new Map(),errors=[];
child.stdio[4].on('data',chunk=>{buf+=chunk;let i;while((i=buf.indexOf('\0'))>=0){const msg=JSON.parse(buf.slice(0,i));buf=buf.slice(i+1);if(msg.id){const p=pending.get(msg.id);pending.delete(msg.id);msg.error?p.reject(new Error(JSON.stringify(msg.error))):p.resolve(msg.result);}if(msg.method==='Fetch.requestPaused')void send('Fetch.fulfillRequest',{requestId:msg.params.requestId,responseCode:200,responseHeaders:[{name:'Content-Type',value:'text/html'}],body:Buffer.from(html).toString('base64')});if(msg.method==='Runtime.exceptionThrown')errors.push(msg.params.exceptionDetails.text);}});
const send=(method,params={},sid=session)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});child.stdio[3].write(JSON.stringify({id:n,method,params,...(sid?{sessionId:sid}:{})})+'\0');});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
(async()=>{try{
 const target=await send('Target.createTarget',{url:'about:blank'},null); session=(await send('Target.attachToTarget',{targetId:target.targetId,flatten:true},null)).sessionId;
 await send('Runtime.enable');await send('Page.enable');await send('Fetch.enable',{patterns:[{urlPattern:'http://127.0.0.1:8765/__matrix-layout-check',requestStage:'Request'}]});await send('Page.navigate',{url:'http://127.0.0.1:8765/__matrix-layout-check'});
 for(let n=0;n<200;n++){if(await evaluate('window.ready === true'))break;await new Promise(r=>setTimeout(r,100));}if(!await evaluate('window.ready === true'))throw new Error('Fixture not ready: '+JSON.stringify(errors));
 const report=[];
 for(const width of [893,375]){await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});
 for(const mode of ['edit','correct']){for(let i=0;i<cases.length;i+=15){const result=await evaluate('renderBatch('+JSON.stringify(cases.slice(i,i+15))+','+JSON.stringify(mode)+')');report.push({width,mode,...result});}}}
 fs.writeFileSync('/home/jake/Developer/Course_Academy/reference/edb-math/repairs/2026-10-17-completing-square-format/browser-report.json',JSON.stringify({errors,report},null,2));
 const samples=cases.filter(x=>[17592186069995,17592186069946,17592186068672,17592186068430,17592186511718].includes(x.entity));
 await send('Emulation.setDeviceMetricsOverride',{width:1000,height:1000,deviceScaleFactor:1,mobile:false});await evaluate('renderBatch('+JSON.stringify(samples)+',"correct")');
 const size=await evaluate('({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})');
 const screenshot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:size.width,height:size.height,scale:1}});fs.writeFileSync('/home/jake/Developer/Course_Academy/reference/edb-math/repairs/2026-10-17-completing-square-format/representative-render.png',Buffer.from(screenshot.data,'base64'));
 console.log(JSON.stringify({cases:cases.length,records:report.reduce((n,b)=>n+b.items.length,0),errors,exceptions:report.flatMap(b=>b.exceptions),mathErrors:report.flatMap(b=>b.items.filter(x=>x.mathErrors.length)),overflow:report.flatMap(b=>b.items.filter(x=>x.overflow||x.contentOverflow).map(x=>({width:b.width,mode:b.mode,...x}))),mathCountAtDesktop:report.filter(b=>b.width===893&&b.mode==='edit').reduce((n,b)=>n+b.items.reduce((n,x)=>n+x.mathCount,0),0)}));
 }catch(e){console.error(e);process.exitCode=1;}finally{child.kill();}})();
