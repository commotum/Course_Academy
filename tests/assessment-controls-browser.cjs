// Requires the local app on port 8765. DOM geometry and stubbed actions only; no screenshots or database writes.
const fs=require('fs'),os=require('os'),path=require('path'),{spawn}=require('child_process');
const root=path.resolve(__dirname,'..'),assert=require('node:assert/strict');
const learning=fs.readFileSync(root+'/ui/learning.js','utf8');
const controllers=learning.slice(learning.indexOf('const $'),learning.indexOf("$('retryButton').addEventListener"));
const html=`<!doctype html><html data-theme="light" style="--site-header-height:0px"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="img-src 'none'; connect-src 'none'"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><script src="/ui/vendor/dompurify/purify.min.js"></script><body><main id="main"></main><script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {decorateSourceTables} from '/ui/content-tables.js';
import {romanLists} from '/ui/prose-lists.js';
import {inlinePrompt,mountInlineFields,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput,questionFeedback,feedbackHeading,responsesComplete} from '/ui/question-fields.js';
const isDeveloperMode=()=>false,attachStepMenu=()=>{};
${controllers}
window.requests=[];
mutation=async(path,body)=>requests.push({path,body});
window.renderCase=(index,type='assessment')=>{
 clearTimeout(assessmentSaveTimer);drafts.clear();
 const step={itemId:10,contentId:101+index,kind:'question',status:'started',markdown:'Which value is correct?',fields:[{id:30,key:'selection',type:'radio',choices:[{id:41,type:'text',value:'1'},{id:42,type:'text',value:'2'}]}]};
 const data={taskId:123,type,status:'started',reviewTopic:{uuid:'reference-topic'},course:{id:'test-course'},questions:Array.from({length:8},(_,i)=>({questionId:101+i,number:i+1,active:i===index,answered:i<index}))};
 task=data;lessonView=null;
 const view=lessonShell(data,{number:index+1,total:8});
 const content=taskContent(data,step,index+1,8);view.feed.append(content);
 const card=content.querySelector('.content-card'),controls=content.querySelector('.assessment-controls'),nav=controls?.querySelector('.assessment-navigation');
 const box=n=>{const r=n.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}};
 return {overflow:document.documentElement.scrollWidth>innerWidth,card:box(card),controls:controls?box(controls):null,nav:nav?{...box(nav),scrollWidth:nav.scrollWidth,clientWidth:nav.clientWidth}:null,toolbar:box(document.querySelector('.lesson-toolbar')),inside:!!card.querySelector('.assessment-controls'),buttons:controls?[...controls.querySelectorAll('button')].map(n=>({text:n.textContent,...box(n),navigation:nav.contains(n),answered:n.dataset.answered,current:n.getAttribute('aria-current'),background:getComputedStyle(n).backgroundColor,whiteSpace:getComputedStyle(n).whiteSpace})):[],reference:{hidden:view.reference.hidden,href:view.reviewLink.getAttribute('href'),inside:card.contains(view.reference)}};
};
window.testActions=async()=>{
 renderCase(6);const input=main.querySelector('input[value="42"]');input.checked=true;
 const actions=[...main.querySelectorAll('.assessment-actions button')];
 actions.find(n=>n.textContent==='Next question').click();await Promise.resolve();await Promise.resolve();
 actions.find(n=>n.textContent==='Submit assessment').click();await Promise.resolve();await Promise.resolve();
 return requests;
};
window.testReviewScroll=async()=>{
 renderCase(0,'review');
 main.querySelector('.content-card').style.minHeight='1800px';
 window.scrollTo(0,600);
 await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
 const toolbar=main.querySelector('.lesson-toolbar'),link=main.querySelector('.lesson-reference a');
 const t=toolbar.getBoundingClientRect(),r=link.getBoundingClientRect();
 const hit=document.elementFromPoint((r.left+r.right)/2,(r.top+r.bottom)/2);
 const result={scrollY,sticky:getComputedStyle(toolbar).position,inside:toolbar.contains(link),visible:r.top>=t.top&&r.bottom<=t.bottom&&r.top>=0&&r.bottom<=innerHeight,clickable:hit===link||link.contains(hit),overflow:document.documentElement.scrollWidth>innerWidth};
 window.scrollTo(0,0);
 return result;
};
window.ready=true;
</script>`;
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'assessment-layout-'));const child=spawn('/usr/bin/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--remote-debugging-pipe','--user-data-dir='+profile,'about:blank'],{stdio:['ignore','ignore','ignore','pipe','pipe']});
let id=0,buf='',session;const pending=new Map(),errors=[];
child.stdio[4].on('data',chunk=>{buf+=chunk;let i;while((i=buf.indexOf('\0'))>=0){const msg=JSON.parse(buf.slice(0,i));buf=buf.slice(i+1);if(msg.id){const p=pending.get(msg.id);pending.delete(msg.id);msg.error?p.reject(new Error(JSON.stringify(msg.error))):p.resolve(msg.result);}if(msg.method==='Fetch.requestPaused')void send('Fetch.fulfillRequest',{requestId:msg.params.requestId,responseCode:200,responseHeaders:[{name:'Content-Type',value:'text/html'}],body:Buffer.from(html).toString('base64')});if(msg.method==='Runtime.exceptionThrown')errors.push(msg.params.exceptionDetails.text);}});
const send=(method,params={},sid=session)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});child.stdio[3].write(JSON.stringify({id:n,method,params,...(sid?{sessionId:sid}:{})})+'\0');});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
(async()=>{try{
 const target=await send('Target.createTarget',{url:'about:blank'},null);
 session=(await send('Target.attachToTarget',{targetId:target.targetId,flatten:true},null)).sessionId;
 await send('Runtime.enable');await send('Page.enable');
 await send('Fetch.enable',{patterns:[{urlPattern:'http://127.0.0.1:8765/__assessment-layout-check',requestStage:'Request'}]});
 await send('Page.navigate',{url:'http://127.0.0.1:8765/__assessment-layout-check'});
 for(let n=0;n<150;n++){if(await evaluate('window.ready===true'))break;await new Promise(r=>setTimeout(r,100));}
 assert.equal(await evaluate('window.ready===true'),true,'fixture ready: '+JSON.stringify(errors));
 let checks=0;
 for(const width of [893,375,320]){
  await send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
  for(const index of [0,6,7]){
   const r=await evaluate('renderCase('+index+')');
   assert.equal(r.inside,false);assert.equal(r.overflow,false);
   assert.ok(r.controls.top>=r.card.bottom+16);assert.ok(r.toolbar.bottom<r.card.top,JSON.stringify({width,index,...r}));
   assert.ok(r.nav.left>=r.controls.left&&r.nav.right<=r.controls.right);
   if(width===893)assert.ok(r.nav.scrollWidth<=r.nav.clientWidth,'eight question numbers and full actions must fit one desktop row');
   for(const b of r.buttons){if(!b.navigation)assert.ok(b.left>=r.controls.left&&b.right<=r.controls.right);assert.ok(b.height>=40);}
   assert.ok(r.buttons.every(b=>Math.abs(b.top-r.buttons[0].top)<1),'all controls must share one row');
   assert.ok(r.buttons.filter(b=>b.navigation).every(b=>/^\d+$/.test(b.text)),'numbers must not include checkmarks');
   const answered=r.buttons.find(b=>b.navigation&&b.answered==='true'&&!b.current);
   const unanswered=r.buttons.find(b=>b.navigation&&b.answered==='false'&&!b.current);
   if(answered&&unanswered)assert.notEqual(answered.background,unanswered.background);
   assert.ok(r.controls.height<80,'controls must remain a single compact row');
   const actionButtons=r.buttons.filter(b=>b.text.includes('question')||b.text.includes('assessment'));
   assert.ok(actionButtons.every(b=>b.whiteSpace==='nowrap'&&b.height<50),'action labels should not wrap');
   for(let i=0;i<r.buttons.length;i++)for(let j=i+1;j<r.buttons.length;j++){
    const a=r.buttons[i],b=r.buttons[j];if(a.navigation!==b.navigation)continue;assert.ok(a.right<=b.left+0.1||b.right<=a.left+0.1||a.bottom<=b.top+0.1||b.bottom<=a.top+0.1,'buttons must not overlap');
   }
   checks++;
  }
  const review=await evaluate("renderCase(0,'review')");
  assert.equal(review.reference.hidden,false);assert.equal(review.reference.inside,false);
  assert.equal(review.reference.href,'/topic?topic=reference-topic&course=test-course');
  const scrolled=await evaluate('testReviewScroll()');
  assert.ok(scrolled.scrollY>=500);
  assert.equal(scrolled.sticky,'sticky');assert.equal(scrolled.inside,true);
  assert.equal(scrolled.visible,true);assert.equal(scrolled.clickable,true);assert.equal(scrolled.overflow,false);
 }
 const requests=await evaluate('testActions()');
 assert.deepEqual(requests.map(r=>r.path),['/api/navigate','/api/submit']);
 assert.equal(requests[0].body.questionId,108);
 assert.ok(requests.every(r=>r.body.responses[0].choiceId===42));
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({passed:true,assessmentLayouts:checks,reviewLayouts:3,actions:requests.length}));
}finally{child.kill();await new Promise(r=>setTimeout(r,250));fs.rmSync(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100});}})().catch(e=>{console.error(e);process.exitCode=1;});
