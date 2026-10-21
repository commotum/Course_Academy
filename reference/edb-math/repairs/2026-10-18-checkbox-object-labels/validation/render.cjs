// Read-only replay through the application's actual Markdown and checkbox UI.
// Usage: node render.cjs VALIDATION_OUTPUT [--widths=893,375] [--sample-only]
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const os=require('node:os'),{spawn}=require('node:child_process'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'../../../../..');
const output=path.resolve(process.argv[2]||'');
const widths=(process.argv.find(x=>x.startsWith('--widths='))?.split('=')[1]||'893,375').split(',').map(Number);
let cases=JSON.parse(fs.readFileSync(path.join(output,'render-cases.json')));
if(process.argv.includes('--after-only'))cases=cases.filter(q=>q.stage==='after');
if(process.argv.includes('--sample-only'))cases=cases.slice(0,2);
const learning=fs.readFileSync(path.join(root,'ui/learning.js'),'utf8');
const renderer=learning.slice(learning.indexOf('function assetURL('),learning.indexOf('function loadMath('));
const controls=learning.slice(learning.indexOf('function choiceOrder('),learning.indexOf('async function openPreview('));
const labelFunction=learning.slice(learning.indexOf('function fieldLabel('),learning.indexOf('function announce('));
const html=`<!doctype html><html data-theme="light"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'none'; font-src 'self' data:;">
<link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css">
<script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script>
<body><main class="lesson-main" id="main"></main><script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {romanLists} from '/ui/prose-lists.js';
import {inlinePrompt,mountInlineFields,loadMathInputs,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput} from '/ui/question-fields.js';
const el=(tag,className='',text='')=>{const n=document.createElement(tag);n.className=className;n.textContent=text;return n;};
const short=x=>String(x||'').split('/').at(-1),typeset=()=>{};
const escapeHTML=text=>String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
${labelFunction}
${renderer}
${controls}
await MathJax.startup.promise;
window.render=async q=>{
  MathJax.typesetClear([main]);main.replaceChildren();
  const card=el('article','content-card'),title=el('h2','',q.label);card.dataset.id=q.id;
  const prompt=markdown(q.problem,'prose',q.fields),fields=el('div','answer-fields');card.append(title,prompt,fields);
  mountInlineFields(prompt,fields,q.fields,f=>fieldControl(f,false,q.id,q.problem,''));
  if(q.solution)card.append(markdown(q.solution,'prose worked-solution'));main.append(card);
  const imagePromises=[...card.querySelectorAll('img')].map(img=>{
    img.loading='eager';return new Promise(resolve=>{if(img.complete)return resolve();img.addEventListener('load',resolve,{once:true});img.addEventListener('error',resolve,{once:true});setTimeout(resolve,10000);});
  });
  await MathJax.typesetPromise([main]);await Promise.all(imagePromises);await document.fonts.ready;
  const responseChecks=[];
  for(const field of q.fields){
    const set=[...card.querySelectorAll('[data-field-id]')].find(n=>n.dataset.fieldId===String(field.id));
    const input=set?.querySelector('input[type=checkbox]');if(!input){responseChecks.push({field:field.id,error:'No checkbox input'});continue;}
    const no=field.choices.find(a=>a.value==='false'),yes=field.choices.find(a=>a.value==='true');
    const initial=collectResponses(card,q.fields).find(x=>x.fieldId===field.id)?.choiceId;
    input.checked=true;input.dispatchEvent(new Event('change',{bubbles:true}));
    const checked=collectResponses(card,q.fields).find(x=>x.fieldId===field.id)?.choiceId;
    input.checked=false;input.dispatchEvent(new Event('change',{bubbles:true}));
    const unchecked=collectResponses(card,q.fields).find(x=>x.fieldId===field.id)?.choiceId;
    responseChecks.push({field:field.id,initialFalse:initial===no.id,checkedTrue:checked===yes.id,uncheckedFalse:unchecked===no.id});
  }
  return {id:q.id,stage:q.stage,checkboxCount:card.querySelectorAll('input[type=checkbox]').length,expectedCheckboxes:q.fields.length,
    images:[...card.querySelectorAll('img')].map(n=>({source:n.getAttribute('src'),loaded:n.complete&&n.naturalWidth>0,width:n.getBoundingClientRect().width,height:n.getBoundingClientRect().height})),
    imageErrors:[...card.querySelectorAll('.math-error')].map(n=>n.textContent),
    mathErrors:[...card.querySelectorAll('[data-mjx-error],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),
    radioCount:card.querySelectorAll('input[type=radio]').length,cardWidth:card.clientWidth,cardScrollWidth:card.scrollWidth,
    choices:[...card.querySelectorAll('.choice')].map(n=>{const prose=n.querySelector('.prose');return {width:n.clientWidth,scrollWidth:n.scrollWidth,text:n.innerText,math:n.querySelectorAll('mjx-container').length,images:n.querySelectorAll('img').length,
      overflowX:getComputedStyle(n).overflowX,right:n.getBoundingClientRect().right,proseWidth:prose?.clientWidth,proseScrollWidth:prose?.scrollWidth,proseOverflowX:prose?getComputedStyle(prose).overflowX:null,
      svgRights:[...n.querySelectorAll('svg')].map(svg=>svg.getBoundingClientRect().right)};}),
    math:[...card.querySelectorAll('mjx-container')].map(n=>({width:n.clientWidth,scrollWidth:n.scrollWidth,height:n.clientHeight,svgWidth:n.querySelector('svg')?.getBoundingClientRect().width})),
    responseChecks};
};window.ready=true;
</script>`;
const mime={'.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.woff2':'font/woff2','.woff':'font/woff','.json':'application/json','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp'};
const assetOrigin=process.env.CA_ASSET_ORIGIN||'http://127.0.0.1:8765';
const assetFailures=[];
const server=http.createServer((req,res)=>{
  const url=new URL(req.url,'http://localhost');
  if(url.pathname==='/probe'){res.setHeader('Content-Type','text/html');res.end(html);return;}
  if(url.pathname==='/api/asset'){
    // Only this read-only asset endpoint may reach the running application.
    const target=new URL(req.url,assetOrigin);
    const proxy=http.get(target,remote=>{res.writeHead(remote.statusCode,{'Content-Type':remote.headers['content-type']||'application/octet-stream'});remote.pipe(res);if(remote.statusCode!==200)assetFailures.push({path:url.searchParams.get('path'),status:remote.statusCode});});
    proxy.on('error',error=>{assetFailures.push({path:url.searchParams.get('path'),error:String(error)});res.writeHead(502);res.end();});return;
  }
  const file=path.resolve(root,'.'+decodeURIComponent(url.pathname));
  if(!file.startsWith(root+path.sep)){res.writeHead(404);res.end();return;}
  try{res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.writeHead(404);res.end();}
});
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'checkbox-object-render-'));
let browser,session,id=0,buf='';const pending=new Map(),errors=[];
const send=(method,params={},sid=session)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});browser.stdio[3].write(JSON.stringify({id:n,method,params,...(sid?{sessionId:sid}:{})})+'\0');});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
const critical=item=>item.mathErrors.length||item.imageErrors.length||item.images.some(x=>!x.loaded)||item.checkboxCount!==item.expectedCheckboxes||item.radioCount||item.responseChecks.some(x=>x.error||!x.initialFalse||!x.checkedTrue||!x.uncheckedFalse)||item.choices.some(x=>!x.text.trim()&&!x.math&&!x.images);
const overflow=item=>item.cardScrollWidth>item.cardWidth+1||item.choices.some(x=>x.scrollWidth>x.width+1);
const selected=new Set(['17592186272202']);
if(process.argv.includes('--screenshot-all'))for(const q of cases)selected.add(q.id);
for(const predicate of [q=>q.fields.some(f=>/\\begin\{(?:[bp]?matrix|array)\}/.test(f.key)),q=>q.fields.some(f=>/!\[|<img\b/.test(f.key)),q=>q.fields.some(f=>f.key.length>300)]){const q=cases.find(q=>q.stage==='after'&&predicate(q));if(q)selected.add(q.id);}
(async()=>{try{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  browser=spawn('/usr/bin/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--remote-debugging-pipe','--user-data-dir='+profile,'about:blank'],{stdio:['ignore','ignore','ignore','pipe','pipe']});
  browser.stdio[4].on('data',chunk=>{buf+=chunk;let i;while((i=buf.indexOf('\0'))>=0){const m=JSON.parse(buf.slice(0,i));buf=buf.slice(i+1);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);}if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.text);}});
  const target=await send('Target.createTarget',{url:'about:blank'},null);session=(await send('Target.attachToTarget',{targetId:target.targetId,flatten:true},null)).sessionId;
  await send('Runtime.enable');await send('Page.enable');await send('Page.navigate',{url:'http://127.0.0.1:'+server.address().port+'/probe'});
  for(let n=0;n<150;n++){if(await evaluate('window.ready===true'))break;await new Promise(r=>setTimeout(r,100));}
  if(!await evaluate('window.ready===true'))throw new Error('Renderer unavailable: '+JSON.stringify(errors));
  const report={databaseWrites:0,assetOrigin,widths,errors,measurements:[],sourceHashes:{}};
  for(const file of ['ui/learning.js','ui/question-fields.js','ui/learning.css','ui/prose-lists.js','ui/mathjax-config.js'])report.sourceHashes[file]=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,file))).digest('hex');
  let screenshots=0;
  for(const width of widths){
    await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});
    for(const q of cases){
      const item=await evaluate('render('+JSON.stringify(q)+')');const measurement={width,...item};report.measurements.push(measurement);
      if((q.stage==='after'&&selected.has(q.id))||(q.stage==='after'&&critical(item)&&screenshots<25)){
        const size=(await send('Page.getLayoutMetrics')).cssContentSize;
        const shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:size.width,height:Math.min(size.height,16000),scale:1}});
        const name='render-'+q.id+'-'+q.stage+'-'+width+'.png';fs.writeFileSync(path.join(output,name),Buffer.from(shot.data,'base64'));measurement.screenshot=name;screenshots++;
      }
      if(report.measurements.length%20===0)console.log(JSON.stringify({rendered:report.measurements.length,total:widths.length*cases.length}));
    }
  }
  report.assetFailures=assetFailures;
  fs.writeFileSync(path.join(output,'rendering-report.json'),JSON.stringify(report,null,2)+'\n');
  const after=report.measurements.filter(q=>q.stage==='after'),before=report.measurements.filter(q=>q.stage==='before');
  const summary={rendered:report.measurements.length,errors,afterCritical:after.filter(critical).map(q=>({id:q.id,width:q.width,mathErrors:q.mathErrors,imageErrors:q.imageErrors})),
    beforeCritical:before.filter(critical).map(q=>({id:q.id,width:q.width,mathErrors:q.mathErrors,imageErrors:q.imageErrors})),
    afterOverflow:after.filter(overflow).map(q=>({id:q.id,width:q.width})),beforeOverflow:before.filter(overflow).map(q=>({id:q.id,width:q.width})),
    checkboxResponseChecks:after.reduce((n,q)=>n+q.responseChecks.length,0),assetFailures};
  fs.writeFileSync(path.join(output,'rendering-summary.json'),JSON.stringify(summary,null,2)+'\n');
  console.log(JSON.stringify({rendered:summary.rendered,afterCritical:summary.afterCritical.length,beforeCritical:summary.beforeCritical.length,afterOverflow:summary.afterOverflow.length,beforeOverflow:summary.beforeOverflow.length,assetFailures:assetFailures.length}));
}finally{browser?.kill();server.close();await new Promise(r=>setTimeout(r,250));fs.rmSync(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100});}})().catch(e=>{console.error(e);process.exitCode=1;});
