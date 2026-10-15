const fs=require('fs'),crypto=require('crypto'),{spawn}=require('child_process');
const [origin,dir]=process.argv.slice(2);const profile=fs.mkdtempSync('/tmp/trig-parts-browser-');
const exe='/home/jake/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell';
const browser=spawn(exe,['--no-sandbox','--disable-gpu','--remote-debugging-port=0',`--user-data-dir=${profile}`,'about:blank']);
const endpoint=new Promise((ok,no)=>{browser.stderr.on('data',b=>{const m=b.toString().match(/DevTools listening on (ws:\/\/\S+)/);if(m)ok(m[1]);});browser.on('error',no);browser.on('exit',code=>{if(code)no(Error('browser exited '+code));});});
const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
(async()=>{
 const ws=new WebSocket(await endpoint);await new Promise(r=>ws.addEventListener('open',r));let n=0;const pending=new Map();ws.addEventListener('message',e=>{const d=JSON.parse(e.data);if(d.id&&pending.has(d.id)){const [ok,no]=pending.get(d.id);pending.delete(d.id);d.error?no(Error(JSON.stringify(d.error))):ok(d.result);}});
 const send=(method,params={},sessionId)=>new Promise((ok,no)=>{const id=++n;pending.set(id,[ok,no]);ws.send(JSON.stringify({id,method,params,sessionId}));});
 const browserVersion=await send('Browser.getVersion');
 const {targetId}=await send('Target.createTarget',{url:origin+'/'+dir+'/render-harness.html'});const {sessionId}=await send('Target.attachToTarget',{targetId,flatten:true});const call=(m,p)=>send(m,p,sessionId);
 await call('Runtime.enable');await call('Page.enable');await call('Emulation.setDeviceMetricsOverride',{width:1250,height:1100,deviceScaleFactor:1,mobile:false});
 const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
 for(let i=0;i<150;i++){if(await evaluate('Boolean(window.renderRecord)'))break;await new Promise(r=>setTimeout(r,100));if(i===149)throw Error('harness not initialized');}
 const records=process.argv[4]?JSON.parse(fs.readFileSync(dir+'/'+process.argv[4])):[...JSON.parse(fs.readFileSync(dir+'/review.json')),...JSON.parse(fs.readFileSync(dir+'/boundary-records.json'))];const results=[];const screenshots=[];fs.mkdirSync(dir+'/renders',{recursive:true});
 for(let i=0;i<records.length;i++){
  const {label,record}=records[i];const result=await evaluate('window.renderRecord('+JSON.stringify(record)+')');
  if(result.errors||result.exposed||result.overflow||result.expected_math!==result.rendered_math||result.radios!==5||!result.visible_radio_indicators||!result.mathlive_loaded||!result.tone_token||!result.complete_solution)throw Error(label+' '+JSON.stringify(result));
  const bytes=Buffer.from(JSON.stringify(record));const recordhash=hash(bytes);
  // Full page capture includes prompt, complete bank, all solution rows and controls.
  if(label.startsWith('Generated normal')||label.startsWith('Original-profile')||label.startsWith('Boundary')){
   const metrics=await call('Page.getLayoutMetrics');const size=metrics.cssContentSize;const file=`renders/${String(i).padStart(2,'0')}-${record.generation.template}-${recordhash.slice(0,12)}.png`;
   const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:1250,height:Math.ceil(size.height),scale:1}});const image=Buffer.from(shot.data,'base64');fs.writeFileSync(dir+'/'+file,image);screenshots.push({label,file,record_sha256:recordhash,question_id:record.question[':question/id'],png_sha256:hash(image),width:1250,height:Math.ceil(size.height)});
  }
  results.push({label,record_sha256:recordhash,...result});
 }
 fs.writeFileSync(dir+'/render-report.json',JSON.stringify({passed:true,renderer_versions:{chromium:browserVersion.product,javascript:browserVersion.jsVersion,mathjax:await evaluate('MathJax.version'),mathlive_loaded:await evaluate("Boolean(customElements.get('math-field'))")},pipeline:'Frozen actual learning.js markdown/answerValue/fieldControl/choiceOrder/el/fieldLabel/escapeHTML/assetURL; actual marked, question-fields, MathLive, DOMPurify, MathJax3, navigation and learning CSS with real theme tokens. Local static fixture, no API writes.',hash_encoding:'SHA256 UTF8 JSON.stringify(record) in review.json row order',records:records.length,screenshots,checks:results},null,2)+'\n');console.log('PASS: '+records.length+' complete renders, '+screenshots.length+' full screenshots, zero math/delimiter/overflow/control errors.');await send('Browser.close');ws.close();
})().catch(e=>{console.error(e.stack);process.exitCode=1;browser.kill();}).finally(()=>{browser.kill();});
