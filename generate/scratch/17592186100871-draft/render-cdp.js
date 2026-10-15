const fs=require('fs'),crypto=require('crypto'),{spawn}=require('child_process'),os=require('os'),path=require('path');
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
 const records=JSON.parse(fs.readFileSync(dir+'/render-records.json'));const results=[],seen=new Set();fs.mkdirSync(dir+'/renders',{recursive:true});
 for(let i=0;i<records.length;i++){
  const record=records[i];const got=await evaluate('window.renderRecord('+JSON.stringify(record)+')');
  if(got.errors||got.exposed||got.overflow)throw Error('render '+i+' '+JSON.stringify(got));
  const fields=record.question[':question/answer-fields'];
  const blanks=fields.filter(f=>f[':answer-field/type'].endsWith('/blank')).length;
  if(got.blanks!==blanks || got.mathfields!==blanks || !got.visibleControls || got.fieldsets!==fields.length-blanks)throw Error('control count '+i+' '+JSON.stringify(got));
  const matrices=[...record.question[':question/problem'].matchAll(/\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}/g)].map(m=>{const rows=m[1].split('\\\\');return {rows:rows.length,columns:rows[0].split('&').length};});
  if(JSON.stringify(got.tables.slice(0,matrices.length))!==JSON.stringify(matrices))throw Error('matrix dimensions '+i);
  const template=record.generation.template+(record.generation.evidence_only?'-raw':'');let screenshotPath=null;
  if(!seen.has(template)){
   const metrics=await call('Page.getLayoutMetrics');const size=metrics.cssContentSize;
   const screenshot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:1120,height:Math.ceil(size.height),scale:1}});
   screenshotPath=dir+'/renders/'+template+'.png';fs.writeFileSync(screenshotPath,Buffer.from(screenshot.data,'base64'));seen.add(template);
  }
  results.push({index:i,template,question_id:record.question[':question/id'],record_sha256:crypto.createHash('sha256').update(JSON.stringify(record)).digest('hex'),screenshot:screenshotPath,...got});
 }
 fs.writeFileSync(dir+'/render-report.json',JSON.stringify({pipeline:'Exact player learning.js markdown/escapeHTML/assetURL/el/fieldLabel routines; actual marked/romanLists/inlinePrompt/DOMPurify and MathJax config+SVG. Local immutable assets; native Chromium CDP.',records:records.length,errors:0,exposed_delimiters:0,matrix_row_column_checks:true,blank_slot_checks:true,overflow:0,screenshots:[...seen].sort(),checks:results},null,2)+'\n');
 console.log(`Rendered ${records.length} actual records; ${seen.size} template screenshots; zero errors, exposed delimiters or overflow.`);
 await send('Browser.close');ws.close();
})().catch(e=>{console.error(e.stack);browser.kill();process.exitCode=1;}).finally(async()=>{browser.kill();await new Promise(resolve=>{if(browser.exitCode!==null)resolve();else {browser.once('exit',resolve);setTimeout(resolve,2000);}});await new Promise(resolve=>setTimeout(resolve,1000));try{await fs.promises.rm(profile,{recursive:true,force:true,maxRetries:20,retryDelay:200});}catch(error){console.warn('Temporary browser profile cleanup: '+error.message);}});
