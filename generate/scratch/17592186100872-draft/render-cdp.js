const fs=require('fs'),{spawn}=require('child_process'),os=require('os'),path=require('path');
const [origin,dir]=process.argv.slice(2);
const profile=fs.mkdtempSync('/tmp/perpendicular-render-');
const browser=spawn('/home/jake/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell',['--no-sandbox','--disable-gpu','--remote-debugging-port=0',`--user-data-dir=${profile}`,'about:blank']);
const endpoint=new Promise((resolve,reject)=>{browser.stderr.on('data',b=>{const m=b.toString().match(/DevTools listening on (ws:\/\/\S+)/);if(m)resolve(m[1]);});browser.on('error',reject);browser.on('exit',code=>{if(code)reject(new Error('browser exited '+code));});});
(async()=>{
 const ws=new WebSocket(await endpoint);await new Promise(r=>ws.addEventListener('open',r));let sequence=0;const pending=new Map();
 ws.addEventListener('message',e=>{const d=JSON.parse(e.data);if(d.id&&pending.has(d.id)){const [ok,no]=pending.get(d.id);pending.delete(d.id);d.error?no(new Error(JSON.stringify(d.error))):ok(d.result);}});
 const send=(method,params={},sessionId)=>new Promise((ok,no)=>{const id=++sequence;pending.set(id,[ok,no]);ws.send(JSON.stringify({id,method,params,sessionId}));});
 const {targetId}=await send('Target.createTarget',{url:origin+'/'+dir+'/render-harness.html'});const {sessionId}=await send('Target.attachToTarget',{targetId,flatten:true});
 const call=(m,p)=>send(m,p,sessionId);await call('Runtime.enable');await call('Page.enable');await call('Emulation.setDeviceMetricsOverride',{width:1120,height:1100,deviceScaleFactor:1,mobile:false});
 const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
 for(let i=0;i<100;i++){if(await evaluate('Boolean(window.renderRecord)'))break;await new Promise(r=>setTimeout(r,100));if(i===99)throw Error('render harness did not initialize');}
 const records=JSON.parse(fs.readFileSync(dir+'/render-records.json'));const results=[];fs.mkdirSync(dir+'/renders',{recursive:true});
 for(let i=0;i<records.length;i++){
  const record=records[i];const got=await evaluate('window.renderRecord('+JSON.stringify(record)+')');
  if(got.errors||got.exposed||got.documentOverflow||!got.controls_visible)throw Error('render '+i+' '+JSON.stringify(got));
  const fields=record.question[':question/answer-fields'];const blanks=fields.filter(f=>f[':answer-field/type'].endsWith('/blank')).length;const radios=fields.filter(f=>f[':answer-field/type'].endsWith('/radio')).reduce((s,f)=>s+f[':answer-field/choices'].length,0);
  if(got.blank_controls!==blanks||got.radio_controls!==radios)throw Error('control mismatch '+i);
  const label=String(i).padStart(2,'0')+'-'+record.generation.level+'-'+record.generation.template+'-'+record.generation.profile;
  const metrics=await call('Page.getLayoutMetrics');const size=metrics.cssContentSize;
  const screenshot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:1120,height:Math.ceil(size.height),scale:1}});
  const filename=dir+'/renders/'+label+'.png';fs.writeFileSync(filename,Buffer.from(screenshot.data,'base64'));
  const scroll_screens=[];
  if(got.overflow.length){
   await evaluate("[...document.querySelectorAll('mjx-container,table')].forEach(n=>{n.scrollLeft=n.scrollWidth;});true");
   const right=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:1120,height:Math.ceil(size.height),scale:1}});
   const rf=dir+'/renders/'+label+'-scroll-right.png';fs.writeFileSync(rf,Buffer.from(right.data,'base64'));scroll_screens.push({path:rf,sha256:require('crypto').createHash('sha256').update(fs.readFileSync(rf)).digest('hex')});
  }
  results.push({index:i,label,scroll_screens,question_id:record.question[':question/id'],content_fingerprint:record.generation.content_fingerprint,screenshot:filename,screenshot_sha256:require('crypto').createHash('sha256').update(fs.readFileSync(filename)).digest('hex'),...got});
 }
 fs.writeFileSync(dir+'/render-report.json',JSON.stringify({pipeline:'Exact current player learning.js markdown/fieldControl/answerValue/choiceOrder/el/fieldLabel routines with actual question-fields mountInlineFields/blankInput/choiceIndicator/MathLive, actual marked/DOMPurify/MathJax and navigation theme tokens. Private loopback Chromium CDP; 720px actual lesson content frame.',records:records.length,checks:results},null,2)+'\n');
 console.log(`Rendered ${records.length} actual records and full-page screenshots.`);
 await send('Browser.close');ws.close();
})().catch(e=>{console.error(e.stack);browser.kill();process.exitCode=1;}).finally(async()=>{browser.kill();await new Promise(resolve=>{if(browser.exitCode!==null)resolve();else {browser.once('exit',resolve);setTimeout(resolve,2000);}});await new Promise(resolve=>setTimeout(resolve,1000));try{await fs.promises.rm(profile,{recursive:true,force:true,maxRetries:20,retryDelay:200});}catch(error){console.warn('Temporary browser profile cleanup: '+error.message);}});
