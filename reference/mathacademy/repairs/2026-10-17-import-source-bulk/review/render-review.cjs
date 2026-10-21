// Offline review through the application's Markdown, sanitization, fields and MathJax.
// Usage: node render-review.cjs input.json report.json [893,375]
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),os=require('node:os'),{spawn}=require('node:child_process');
const root=path.resolve(__dirname,'../../../../..'),input=path.resolve(process.argv[2]),output=path.resolve(process.argv[3]);
const widths=(process.argv[4]||'893,375').split(',').map(Number),cases=JSON.parse(fs.readFileSync(input));
const digest=b=>require('node:crypto').createHash('sha256').update(b).digest('hex');
const uiHashes=()=>Object.fromEntries(['ui/learning.js','ui/learning.css','ui/question-fields.js','ui/mathjax-config.js','ui/prose-lists.js'].map(p=>[p,digest(fs.readFileSync(path.join(root,p)))]));
const initialUI=uiHashes(),inputSHA=digest(fs.readFileSync(input));
const learning=fs.readFileSync(path.join(root,'ui/learning.js'),'utf8');
const renderer=learning.slice(learning.indexOf('function markdown('),learning.indexOf('function loadMath('));
const controls=learning.slice(learning.indexOf('function choiceOrder('),learning.indexOf('function collectResponses('));
const html=`<!doctype html><html data-theme="light"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css">
<script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script>
<body><main class="lesson-main" id="main"></main><script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {romanLists} from '/ui/prose-lists.js';
import {inlinePrompt,mountInlineFields,loadMathInputs,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput} from '/ui/question-fields.js';
const el=(tag,className='',text='')=>{const n=document.createElement(tag);n.className=className;n.textContent=text;return n;};
const short=x=>String(x||'').split('/').at(-1),fieldLabel=k=>k,assetURL=x=>'/assets/'+x,typeset=()=>{};
const escapeHTML=text=>String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
${renderer}
${controls}
await loadMathInputs();await MathJax.startup.promise;
const serialize=n=>({kind:n.kind,...(n.kind==='text'?{text:n.text}:{}),attributes:n.attributes?.getAllAttributes?.()||{},children:(n.childNodes||[]).map(serialize)});
window.render=async cases=>{MathJax.typesetClear([main]);main.replaceChildren();
 for(const q of cases){const card=el('article','content-card');card.dataset.id=q.id;card.dataset.omitTrees=q.omitTrees?'true':'false';card.append(el('h2','',q.label||q.id));
  if(q.source_svg){const holder=el('div','source-svg'),img=el('img');img.src='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(q.source_svg)));img.style.maxWidth='100%';holder.append(img);card.append(holder);}
  const prompt=markdown(q.problem,'prose',q.fields||[]),fields=el('div','answer-fields');card.append(prompt,fields);
  mountInlineFields(prompt,fields,q.fields||[],f=>fieldControl(f,false,q.id,q.problem,''));
  if(q.solution)card.append(markdown(q.solution,'prose worked-solution'));main.append(card);}
 await MathJax.typesetPromise([main]);await document.fonts.ready;await Promise.all([...main.querySelectorAll('.source-svg img')].map(i=>i.decode().catch(()=>{})));
 const items=[...MathJax.startup.document.math];
 return [...main.children].map(card=>({id:card.dataset.id,width:card.clientWidth,scrollWidth:card.scrollWidth,
  controls:{checkbox:card.querySelectorAll('input[type=checkbox]').length,radio:card.querySelectorAll('input[type=radio]').length,math:card.querySelectorAll('math-field').length,select:card.querySelectorAll('[role=combobox]').length},
  slots:card.querySelectorAll('[data-field-key]').length,code:[...card.querySelectorAll('pre code')].map(n=>n.textContent),
  errors:[...card.querySelectorAll('[data-mjx-error],mjx-merror,.math-error')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),
  math:items.filter(m=>card.contains(m.typesetRoot)).map(m=>({tex:m.math,...(card.dataset.omitTrees==='true'?{}:{tree:serialize(m.root)})})),
  overflow:[...card.querySelectorAll('mjx-container,.choice,table')].filter(n=>n.scrollWidth>n.clientWidth+1).map(n=>({tag:n.tagName,width:n.clientWidth,scrollWidth:n.scrollWidth,scrollable:getComputedStyle(n).overflowX,tex:n.querySelector('title')?.textContent})),
  clipped:[...card.querySelectorAll('mjx-container')].filter(n=>{const r=n.getBoundingClientRect(),c=card.getBoundingClientRect();if(r.right<=c.right+1&&r.left>=c.left-1)return false;for(let p=n.parentElement;p&&p!==card;p=p.parentElement)if(['auto','scroll'].includes(getComputedStyle(p).overflowX))return false;return true;}).length,
 }));};window.ready=true;
</script>`;
const mime={'.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.woff2':'font/woff2','.woff':'font/woff','.json':'application/json','.png':'image/png','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>{if(req.url==='/probe'){res.setHeader('Content-Type','text/html');res.end(html);return;}
 const url=decodeURIComponent(req.url.split('?')[0]),asset=url.startsWith('/assets/'),base=asset?'/media/jake/SSD/EDB/math':root;
 const file=path.resolve(base,asset?url.slice(8):'.'+url);if(!file.startsWith(base+path.sep)){res.writeHead(404);res.end();return;}
 try{res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.writeHead(404);res.end();}});
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'source-bulk-review-'));let browser,session,id=0,buf='';const pending=new Map(),errors=[];
const send=(method,params={},sid=session)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});browser.stdio[3].write(JSON.stringify({id:n,method,params,...(sid?{sessionId:sid}:{})})+'\0');});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
(async()=>{try{await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 browser=spawn('/usr/bin/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--remote-debugging-pipe','--user-data-dir='+profile,'about:blank'],{stdio:['ignore','ignore','ignore','pipe','pipe']});
 browser.stdio[4].on('data',chunk=>{buf+=chunk;let i;while((i=buf.indexOf('\0'))>=0){const m=JSON.parse(buf.slice(0,i));buf=buf.slice(i+1);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);}if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.text);}});
 const target=await send('Target.createTarget',{url:'about:blank'},null);session=(await send('Target.attachToTarget',{targetId:target.targetId,flatten:true},null)).sessionId;
 await send('Runtime.enable');await send('Page.enable');await send('Page.navigate',{url:'http://127.0.0.1:'+server.address().port+'/probe'});
 for(let n=0;n<150;n++){if(await evaluate('window.ready===true'))break;await new Promise(r=>setTimeout(r,100));}
 if(!await evaluate('window.ready===true'))throw new Error('Renderer unavailable: '+JSON.stringify(errors));
 const report={input,input_sha256:inputSHA,ui_sha256:initialUI,errors,measurements:[]};
 for(const width of widths){await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});
  for(let i=0;i<cases.length;i+=10){const batch=cases.slice(i,i+10);const items=await evaluate('render('+JSON.stringify(batch)+')');
   report.measurements.push({width,items});if(i%100===0)console.log(JSON.stringify({width,processed:i+batch.length,total:cases.length}));}
  for(const q of cases.filter(q=>q.screenshot)){await evaluate('render('+JSON.stringify([q])+')');const size=(await send('Page.getLayoutMetrics')).cssContentSize;
   const shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:size.width,height:Math.min(size.height,16000),scale:1}});
   fs.writeFileSync(path.join(path.dirname(output),'render-'+q.id.replace(/[^a-z0-9_-]/ig,'_')+'-'+width+'.png'),Buffer.from(shot.data,'base64'));}}
 report.ui_unchanged=JSON.stringify(initialUI)===JSON.stringify(uiHashes());fs.writeFileSync(output,JSON.stringify(report)+'\n');const bad=report.measurements.flatMap(r=>r.items.filter(x=>x.errors.length));console.log(JSON.stringify({cases:cases.length,widths,errors,renderErrors:bad.length,firstErrorIds:bad.slice(0,10).map(x=>x.id),clipped:report.measurements.flatMap(r=>r.items.filter(x=>x.clipped)).length}));
}finally{browser?.kill();server.close();await new Promise(r=>setTimeout(r,250));fs.rmSync(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100});}})().catch(e=>{console.error(e);process.exitCode=1;});
