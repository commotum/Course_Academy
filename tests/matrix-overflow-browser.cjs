// Requires the local app/static UI server on port 8765, or COURSE_ACADEMY_TEST_ORIGIN.
// Uses DOM geometry; no learner APIs, screenshots or image loading.
const fs=require('fs'),os=require('os'),path=require('path'),{spawn}=require('child_process');
const root=path.resolve(__dirname,'..');
const origin=process.env.COURSE_ACADEMY_TEST_ORIGIN || 'http://127.0.0.1:8765';
const assert=require('node:assert/strict');
const group=(values,stacked=true)=>'<div class="matrix-operands'+(stacked?' matrix-operands-stacked':'')+'">'+values.map(value=>'<div>$'+value+'$</div>').join('')+'</div>';
const matrix=rows=>String.raw`\begin{bmatrix}`+rows.map(row=>row.join(' & ')).join(String.raw` \\ `)+String.raw`\end{bmatrix}`;
const cases=[
 {entity:1,fields:[],problem:group(['U='+matrix([[1,0,1],[2,3,1]]),'W='+matrix([[1,-1,0],[1,0,-4],[5,0,1]]),'Z='+matrix([[String.raw`\sqrt{3}`,0],[1,String.raw`-\sqrt{2}`]])])},
 {entity:2,fields:[],problem:group(['A='+matrix([[1,2],[3,4]]),'B='+matrix([[1,0,2,3]])],false)},
 {entity:3,fields:[],problem:group(['C='+matrix(Array.from({length:3},(_,i)=>Array.from({length:16},(_,j)=>i+j+1)))])},
];
const learning=fs.readFileSync(root+'/ui/learning.js','utf8');
const renderers=learning.slice(learning.indexOf('function markdown('),learning.indexOf('function loadMath('))+learning.slice(learning.indexOf('function choiceOrder('),learning.indexOf('function collectResponses('));
const html=`<!doctype html><html data-theme="light"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="img-src 'none'; connect-src 'none'"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><body><main class="lesson-main" id="main"></main><script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {decorateSourceTables} from '/ui/content-tables.js';import {romanLists} from '/ui/prose-lists.js';import {protectMath} from '/ui/math-protection.js';
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
return {entity:Number(article.dataset.entity),wrappers:operands.map(n=>{const c=getComputedStyle(n),m=n.querySelector('mjx-container'),v=m?.querySelector('svg'),r=n.getBoundingClientRect(),mr=m?.getBoundingClientRect(),vr=v?.getBoundingClientRect();return {width:n.clientWidth,height:n.clientHeight,scrollWidth:n.scrollWidth,scrollHeight:n.scrollHeight,overflowX:c.overflowX,overflowY:c.overflowY,lineHeight:c.lineHeight,wrapperTop:r.top,wrapperBottom:r.bottom,mathTop:mr?.top,mathBottom:mr?.bottom,svgTop:vr?.top,svgBottom:vr?.bottom,mathDisplay:m?getComputedStyle(m).display:null};}),mathErrors:[...article.querySelectorAll('[data-mjx-error],mjx-merror')].map(x=>x.getAttribute('data-mjx-error')||x.textContent),overflow:article.scrollWidth>article.clientWidth+1,contentOverflow:prompt?prompt.scrollWidth>prompt.clientWidth+1:false,fields:article.querySelectorAll('[data-answer-input="true"]').length,blankEditors:article.querySelectorAll('math-field').length,bracketed:!!table,borderless:cells.every(c=>getComputedStyle(c).borderTopWidth==='0px'&&getComputedStyle(c).borderLeftWidth==='0px'),givenCount:operands.length,centered:operands.every(n=>{const b=n.getBoundingClientRect();return Math.abs((b.left+b.right)/2-center)<1}),empty:!prompt?.textContent.trim()};})};};window.ready=true;
</script>`;
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'matrix-quality-'));const child=spawn('/usr/bin/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--remote-debugging-pipe','--user-data-dir='+profile,'about:blank'],{stdio:['ignore','ignore','ignore','pipe','pipe']});
let id=0,buf='',session;const pending=new Map(),errors=[];
child.stdio[4].on('data',chunk=>{buf+=chunk;let i;while((i=buf.indexOf('\0'))>=0){const msg=JSON.parse(buf.slice(0,i));buf=buf.slice(i+1);if(msg.id){const p=pending.get(msg.id);pending.delete(msg.id);msg.error?p.reject(new Error(JSON.stringify(msg.error))):p.resolve(msg.result);}if(msg.method==='Fetch.requestPaused')void send('Fetch.fulfillRequest',{requestId:msg.params.requestId,responseCode:200,responseHeaders:[{name:'Content-Type',value:'text/html'}],body:Buffer.from(html).toString('base64')});if(msg.method==='Runtime.exceptionThrown')errors.push(msg.params.exceptionDetails.text);}});
const send=(method,params={},sid=session)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});child.stdio[3].write(JSON.stringify({id:n,method,params,...(sid?{sessionId:sid}:{})})+'\0');});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
(async()=>{try{const target=await send('Target.createTarget',{url:'about:blank'},null);session=(await send('Target.attachToTarget',{targetId:target.targetId,flatten:true},null)).sessionId;await send('Runtime.enable');await send('Page.enable');await send('Fetch.enable',{patterns:[{urlPattern:origin+'/__matrix-layout-check',requestStage:'Request'}]});await send('Page.navigate',{url:origin+'/__matrix-layout-check'});
for(let n=0;n<200;n++){if(await evaluate('window.ready === true'))break;await new Promise(r=>setTimeout(r,100));}if(!await evaluate('window.ready === true'))throw new Error('Fixture not ready: '+JSON.stringify(errors));
const report=[];const widths=[893,375,320],modes=['edit'];
for(const width of widths){await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});for(const mode of modes){for(let i=0;i<cases.length;i+=20){const result=await evaluate('renderBatch('+JSON.stringify(cases.slice(i,i+20))+','+JSON.stringify(mode)+')');report.push({width,mode,...result});if(i%200===0)console.log(JSON.stringify({width,mode,processed:i+result.items.length,total:cases.length}));}}}
for(const batch of report){
 assert.equal(batch.exceptions.length,0,'all matrix fixtures must render');
 assert.equal(batch.items.length,cases.length,'all fixtures must be measured');
 for(const item of batch.items){
 assert.equal(item.wrappers.length,({1:3,2:2,3:1})[item.entity],'all matrix wrappers must exist');
 assert.equal(item.mathErrors.length,0,'MathJax errors');
 assert.equal(item.overflow,false,'matrix must not expand the question card');
 for(const wrapper of item.wrappers){
  assert.ok(wrapper.scrollHeight<=wrapper.height+1,`Unnecessary vertical scroll: ${JSON.stringify(wrapper)}`);
  assert.ok(wrapper.svgTop>=wrapper.wrapperTop-1 && wrapper.svgBottom<=wrapper.wrapperBottom+1,'matrix glyphs must fit vertically');
 }
 if(item.entity!==3)assert.ok(item.wrappers.every(w=>w.scrollWidth<=w.width+1),'ordinary matrices must not scroll horizontally');
 if(item.entity===3 && batch.width===320)assert.ok(item.wrappers.some(w=>w.scrollWidth>w.width+1),'wide matrices must retain horizontal scrolling');
 }
}
assert.equal(errors.length,0,'browser errors');

// Full checkbox objects can include an inline 4x4 matrix. These two actual
// choices previously escaped their labels by 24px at a 320px viewport.
const checkboxMatrices = [
 {entity:17592186479914,tex:'A='+matrix([[-11,0,-3,0],[0,0,0,9],[0,0,4,-10],[0,0,0,5]])},
 {entity:17592186571387,tex:'C='+matrix([[1,.65,1,8],[0,2,3,.89],[0,0,-2,9.87],[0,0,0,0]])},
];
const matrixChoices = checkboxMatrices.map(({entity,tex})=>({entity,problem:'Select the upper triangular matrices.',fields:[{
 id:entity,key:'$'+tex+'$',type:'checkbox',choices:[{id:1,type:'text',value:'false'},{id:2,type:'text',value:'true'}],correctAnswer:{id:2,type:'text',value:'true'},
}]}));
const matrixMeasures=[];
// Long worked solutions leave a desktop scrollbar at phone widths, which
// consumes another 15px in the browser and was the most constrained case.
await evaluate("main.style.minHeight='1200px'");
for (const width of widths) {
 await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
 for (const mode of ['edit','correct']) {
  await evaluate('renderBatch('+JSON.stringify(matrixChoices)+','+JSON.stringify(mode)+')');
  const items=await evaluate(`([...main.children].map(article=>{
   const label=article.querySelector('.choice'),prose=label.querySelector('.prose'),svg=prose.querySelector('mjx-container > svg');
   const r=svg.getBoundingClientRect(),p=prose.getBoundingClientRect(),l=label.getBoundingClientRect(),v=svg.viewBox.baseVal;
   return {entity:Number(article.dataset.entity),labelWidth:label.clientWidth,labelScroll:label.scrollWidth,
    cardWidth:article.clientWidth,cardScroll:article.scrollWidth,proseWidth:p.width,svgWidth:r.width,svgHeight:r.height,
    aspect:r.width/r.height,viewBoxAspect:v.width/v.height,inside:r.left>=p.left-1&&r.right<=p.right+1&&r.top>=l.top-1&&r.bottom<=l.bottom+1,
    mathErrors:article.querySelectorAll('[data-mjx-error],mjx-merror').length,
    disabled:label.querySelector('input[type=checkbox]').disabled};
  }))`);
  for (const item of items) {
   assert.equal(item.mathErrors,0,'checkbox matrix must typeset');
   assert.ok(item.labelScroll<=item.labelWidth+1,'checkbox matrix must fit its label: '+JSON.stringify({width,...item}));
   assert.ok(item.cardScroll<=item.cardWidth+1,'checkbox matrix must fit its card');
   assert.equal(item.inside,true,'all matrix glyphs must stay inside the label');
   assert.ok(Math.abs(item.aspect-item.viewBoxAspect)<.02,'matrix must retain its aspect ratio');
   assert.equal(item.disabled,mode!=='edit','responsive sizing must preserve read-only state');
   const natural=matrixMeasures.find(m=>m.width===893&&m.mode===mode&&m.entity===item.entity);
   if(natural){
    assert.ok(item.svgWidth>=natural.svgWidth*.8,'matrix text must remain readable');
    if(width===375)assert.ok(Math.abs(item.svgWidth-natural.svgWidth)<1,'fitting matrices must keep their natural size');
   }
   matrixMeasures.push({width,mode,...item});
  }
 }
}
await evaluate("main.style.minHeight=''");
// Matrix fitting is specific to checkbox choices, not radio alternatives.
const radio={entity:4,problem:'Choose a matrix.',fields:[{id:4,key:'selection',type:'radio',choices:[{id:4,type:'text',value:'$'+checkboxMatrices[0].tex+'$'}]}]};
await evaluate('renderBatch('+JSON.stringify([radio])+',"edit")');
assert.equal(await evaluate("getComputedStyle(main.querySelector('.choice mjx-container > svg')).maxWidth"),'none','radio SVG sizing remains unchanged');

// Question 17592186536065: scalar SVG answers must not become tiny scrollboxes.
const scalarRadio={entity:17592186536065,problem:'If $y=(4e^x)(x+1)$, calculate the tangent slope at $x=0$.',fields:[{
 id:20,key:'selection',type:'radio',choices:[5,3,8,-8,4].map((value,index)=>({id:index+1,type:'math',value:String(value)})),correctAnswer:{id:3,type:'math',value:'8'},
}]};
const tallRadio={entity:6,problem:'Choose a value.',fields:[{id:21,key:'selection',type:'radio',choices:[
 {id:1,type:'math',value:String.raw`\frac{1+\sqrt{x^2+1}}{\sqrt[3]{x+2}}`},
 {id:2,type:'math',value:matrix([[1,2],[3,4],[5,6],[7,8]])},
]}]};
const wideRadio={entity:7,problem:'Choose a formula.',fields:[{id:22,key:'selection',type:'radio',choices:[
 {id:1,type:'math',value:Array.from({length:25},(_,i)=>'x_{'+i+'}').join('+')},
]}]};
let radioChecks=0;
for(const width of widths){
 await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
 for(const mode of ['edit','correct']){
  await evaluate('renderBatch('+JSON.stringify([scalarRadio,tallRadio,wideRadio])+','+JSON.stringify(mode)+')');
  const choices=await evaluate(`([...main.querySelectorAll('.choice')].map(label=>{
   const prose=label.querySelector('.prose'),box=prose.getBoundingClientRect(),svg=prose.querySelector('mjx-container > svg'),math=svg.getBoundingClientRect();
   return {entity:Number(label.closest('article').dataset.entity),width:prose.clientWidth,scrollWidth:prose.scrollWidth,
    height:prose.clientHeight,scrollHeight:prose.scrollHeight,overflowY:getComputedStyle(prose).overflowY,
    glyphsInside:math.top>=box.top-1 && math.bottom<=box.bottom+1,
    cardOverflow:label.closest('article').scrollWidth>label.closest('article').clientWidth+1,
    disabled:label.querySelector('input').disabled};
  }))`);
  for(const choice of choices){
   assert.ok(choice.overflowY==='hidden' || choice.scrollHeight<=choice.height+1,'radio answer must not scroll vertically: '+JSON.stringify({viewportWidth:width,mode,...choice}));
   assert.equal(choice.glyphsInside,true,'tall formulas must fit vertically without clipping');
   assert.equal(choice.cardOverflow,false,'radio answer must not expand its question card');
   assert.equal(choice.disabled,mode!=='edit','radio read-only state is preserved');
   if(choice.entity===scalarRadio.entity)assert.ok(choice.scrollWidth<=choice.width+1,'scalar answers must not scroll horizontally');
   if(choice.entity===wideRadio.entity && width===320)assert.ok(choice.scrollWidth>choice.width+1,'wide radio formulas retain horizontal scrolling');
   radioChecks++;
  }
 }
}

// Question 17592186299692: a narrow column vector must grow while entering
// polynomial expressions, including after restoring a saved response.
const vector = {
 entity:17592186299692,
 fields:[1,2].map(id=>({id,key:'field-'+id,type:'blank',answerType:'math',choices:[]})),
 problem:'<div class="matrix-answer"><span class="matrix-answer-label">$By=$</span><div class="matrix-answer-brackets"><table aria-label="Answer matrix"><tbody><tr><td>{{field-1}}</td></tr><tr><td>{{field-2}}</td></tr></tbody></table></div></div>',
};
const measureVector = () => evaluate(`(() => {
 const field=main.querySelector('math-field'), brackets=main.querySelector('.matrix-answer-brackets');
 const content=field.shadowRoot.querySelector('.ML__content');
 return {value:field.value, width:field.getBoundingClientRect().width, matrix:brackets.getBoundingClientRect().width,
   clipped:content.scrollWidth>content.clientWidth+1, overflow:main.scrollWidth>main.clientWidth+1};
})()`);
for (const width of widths) {
 await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
 await evaluate('renderBatch('+JSON.stringify([vector])+',"edit")');
 const empty=await measureVector();
 await evaluate("main.querySelector('math-field').focus()");
 await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
 // Use the editor's insertion API so this geometry check does not depend on
 // a headless browser's OS keyboard mapping.
 for (const key of ['6','p','+','2','q','-','4','p']) {
  await evaluate("main.querySelector('math-field').insert("+JSON.stringify(key)+")");
 }
 await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
 const typed=await measureVector();
 assert.equal(typed.value,'6p+2q-4p','input must reach the matrix editor');
 assert.ok(typed.width>empty.width+20,'matrix entry must grow during typing: '+JSON.stringify({empty,typed}));
 assert.ok(typed.matrix>empty.matrix+20,'vector brackets must expand with the entry');
 assert.equal(typed.clipped,false,'typed expression must remain fully visible');
 assert.equal(typed.overflow,false,'expanded vector must fit the page');
 await evaluate("main.querySelector('math-field').value=''");
 await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
 assert.ok((await measureVector()).width<typed.width-20,'clearing an entry must restore its compact width');
 const restored=structuredClone(vector);
 restored.fields[0].response={value:String.raw`6p^2-4q^2`};
 restored.fields[1].response={value:String.raw`-5p^2+2q^2`};
 await evaluate('renderBatch('+JSON.stringify([restored])+',"edit")');
 await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
 const saved=await measureVector();
 assert.ok(saved.width>empty.width+20,'restored polynomial must size to its rendered content');
 assert.equal(saved.clipped,false,'restored polynomial must remain fully visible');
 assert.equal(saved.overflow,false,'restored vector must fit the page');
}
assert.equal(errors.length,0,'browser errors after editing');

console.log(JSON.stringify({passed:true,cases:cases.length,checks:report.flatMap(x=>x.items).length,checkboxMatrixChecks:matrixMeasures.length,radioChecks,vectorEditWidths:widths,errors:report.flatMap(x=>x.items).filter(x=>x.mathErrors.length).length,overflow:report.flatMap(x=>x.items).filter(x=>x.overflow).length,exceptions:report.flatMap(x=>x.exceptions).length}));
}finally{child.kill();await new Promise(r=>setTimeout(r,250));fs.rmSync(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100});}})().catch(e=>{console.error(e);process.exitCode=1;});
