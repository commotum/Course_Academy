// Read-only fixture using actual UI Markdown/MathJax. No learner API calls.
const fs=require('fs'),os=require('os'),path=require('path'),{spawn}=require('child_process');
const root='/home/jake/Developer/Course_Academy', origin='http://127.0.0.1:8765';
const caseFile=process.env.CASE_FILE || __dirname+'/changes.json';
const outputDirectory=process.env.OUTPUT_DIRECTORY || __dirname;
const cases=JSON.parse(fs.readFileSync(caseFile,'utf8'));
fs.mkdirSync(outputDirectory,{recursive:true});
fs.writeFileSync(outputDirectory+'/browser-inputs.json',JSON.stringify(cases));
const learning=fs.readFileSync(root+'/ui/learning.js','utf8');
const renderers=learning.slice(learning.indexOf('function markdown('),learning.indexOf('function loadMath('));
const html=`<!doctype html><html data-theme="light"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="img-src 'none'; connect-src 'none'"><link rel="stylesheet" href="/ui/learning.css"><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><body><main class="lesson-main" id="main"></main><script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {romanLists} from '/ui/prose-lists.js';
import {inlinePrompt} from '/ui/question-fields.js';
const el=(tag,className='',text='')=>{const n=document.createElement(tag);n.className=className;n.textContent=text;return n;};
const assetURL=x=>'',escapeHTML=text=>String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
${renderers}
await MathJax.startup.promise;
window.renderBatch=async(entries,stage)=>{MathJax.typesetClear([main]);main.replaceChildren();const exceptions=[];
for(const c of entries){const a=el('article','content-card');a.dataset.entity=c.entity;a.dataset.attribute=c.attribute;main.append(a);try{a.append(markdown(c.attribute===':answer/value' ? '$$'+String.fromCharCode(10)+c[stage]+String.fromCharCode(10)+'$$' : c[stage]));for(const img of a.querySelectorAll('img'))img.remove();}catch(e){exceptions.push({entity:c.entity,attribute:c.attribute,error:e.message});}}
await MathJax.typesetPromise([main]);await document.fonts.ready;
return {exceptions,items:[...main.children].map(a=>({entity:Number(a.dataset.entity),attribute:a.dataset.attribute,mathCount:a.querySelectorAll('mjx-container').length,errors:[...a.querySelectorAll('[data-mjx-error],mjx-merror,[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),overflow:a.scrollWidth>a.clientWidth+1,proseOverflow:[...a.querySelectorAll('.prose')].some(n=>n.scrollWidth>n.clientWidth+1),literalBraceText:[...a.querySelectorAll('svg text')].filter(n=>/[⏟⏞]/.test(n.textContent)).map(n=>n.textContent),semanticBraces:[...a.querySelectorAll('mjx-assistive-mml mo')].filter(n=>/^[⏟⏞]$/.test(n.textContent)&&n.getAttribute('stretchy')!=='false').length}))};};window.ready=true;
</script>`;
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'hat-repair-'));const child=spawn('/usr/bin/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--remote-debugging-pipe','--user-data-dir='+profile,'about:blank'],{stdio:['ignore','ignore','ignore','pipe','pipe']});
let id=0,buf='',session;const pending=new Map(),errors=[];
child.stdio[4].on('data',chunk=>{buf+=chunk;let i;while((i=buf.indexOf('\0'))>=0){const msg=JSON.parse(buf.slice(0,i));buf=buf.slice(i+1);if(msg.id){const p=pending.get(msg.id);pending.delete(msg.id);msg.error?p.reject(new Error(JSON.stringify(msg.error))):p.resolve(msg.result);}if(msg.method==='Fetch.requestPaused')void send('Fetch.fulfillRequest',{requestId:msg.params.requestId,responseCode:200,responseHeaders:[{name:'Content-Type',value:'text/html'}],body:Buffer.from(html).toString('base64')});if(msg.method==='Runtime.exceptionThrown')errors.push(msg.params.exceptionDetails.text);}});
const send=(method,params={},sid=session)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});child.stdio[3].write(JSON.stringify({id:n,method,params,...(sid?{sessionId:sid}:{})})+'\0');});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
(async()=>{try{
const target=await send('Target.createTarget',{url:'about:blank'},null);session=(await send('Target.attachToTarget',{targetId:target.targetId,flatten:true},null)).sessionId;await send('Runtime.enable');await send('Page.enable');await send('Fetch.enable',{patterns:[{urlPattern:origin+'/__hat-repair-check',requestStage:'Request'}]});await send('Page.navigate',{url:origin+'/__hat-repair-check'});
for(let n=0;n<200;n++){if(await evaluate('window.ready === true'))break;await new Promise(r=>setTimeout(r,100));}if(!await evaluate('window.ready === true'))throw new Error('Fixture not ready: '+JSON.stringify(errors));
const report=[];
for(const width of [893,375]){await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});for(const stage of ['before','after'])for(let i=0;i<cases.length;i+=20){const result=await evaluate('renderBatch('+JSON.stringify(cases.slice(i,i+20))+','+JSON.stringify(stage)+')');report.push({width,stage,...result});if(i%400===0)console.log(JSON.stringify({width,stage,processed:i+result.items.length,total:cases.length}));}}
fs.writeFileSync(outputDirectory+'/browser-report.json',JSON.stringify({errors,report},null,2));
const issue=b=>b.items.filter(x=>x.errors.length||x.overflow||x.proseOverflow||x.literalBraceText.length).map(x=>({width:b.width,stage:b.stage,...x}));
const summary={cases:cases.length,renders:report.reduce((n,b)=>n+b.items.length,0),errors,exceptions:report.flatMap(b=>b.exceptions),issuesBefore:report.filter(b=>b.stage==='before').flatMap(issue),issuesAfter:report.filter(b=>b.stage==='after').flatMap(issue),mathCountAfterDesktop:report.filter(b=>b.width===893&&b.stage==='after').reduce((n,b)=>n+b.items.reduce((v,x)=>v+x.mathCount,0),0),semanticBracesAfterDesktop:report.filter(b=>b.width===893&&b.stage==='after').reduce((n,b)=>n+b.items.reduce((v,x)=>v+x.semanticBraces,0),0)};
fs.writeFileSync(outputDirectory+'/browser-summary.json',JSON.stringify(summary,null,2));console.log(JSON.stringify({cases:summary.cases,renders:summary.renders,errors:summary.errors,exceptions:summary.exceptions,issuesBefore:summary.issuesBefore.length,issuesAfter:summary.issuesAfter.length,mathCountAfterDesktop:summary.mathCountAfterDesktop,semanticBracesAfterDesktop:summary.semanticBracesAfterDesktop}));
await send('Emulation.setDeviceMetricsOverride',{width:1000,height:1000,deviceScaleFactor:1,mobile:false});
const flattened=cases.filter(c=>c.repair_kind==='flattened');const samples=[cases.find(c=>c.entity===17592186172337),flattened.find(c=>c.attribute!==':answer/value'),flattened.find(c=>c.attribute===':answer/value')];
for(let i=0;i<samples.length;i++){if(!samples[i])continue;await evaluate('renderBatch('+JSON.stringify([samples[i]])+',"after")');const size=await evaluate('({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight})');const s=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:size.width,height:Math.min(size.height,12000),scale:1}});fs.writeFileSync(outputDirectory+'/sample-'+i+'.png',Buffer.from(s.data,'base64'));}
}catch(e){console.error(e);process.exitCode=1;}finally{child.kill();}})();
