// Read-only replay of live captured content through the actual learning renderer.
const fs = require('node:fs'), path = require('node:path'), http = require('node:http');
const os = require('node:os'), {spawn} = require('node:child_process');
const root = path.resolve(__dirname, '../../../../..');
const review = JSON.parse(fs.readFileSync(path.join(__dirname, 'visual-cases.json')));
const learning = fs.readFileSync(path.join(root, 'ui/learning.js'), 'utf8');
const renderer = learning.slice(learning.indexOf('function markdown('), learning.indexOf('function loadMath('));
const controls = learning.slice(learning.indexOf('function choiceOrder('), learning.indexOf('function collectResponses('));
const cases = review.map(({label,record}, index) => {const q=record.question;return {
  id: index+1, label, problem:q[':question/problem'], solution:q[':question/worked-solution'],
  fields:q[':question/answer-fields'].map((f, fi) => ({
    id:20+fi, key:f[':answer-field/key'], type:f[':answer-field/type'], answerType:'text',
    choices:f[':answer-field/choices'].map((a, ai) => ({id:100+ai,value:a[':answer/value'],type:'text'})),
  })),
};});
const html = `<!doctype html><html data-theme="light"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css">
<script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script>
<body><main class="lesson-main" id="main"></main><script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {romanLists} from '/ui/prose-lists.js';
import {inlinePrompt,mountInlineFields,loadMathInputs,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput} from '/ui/question-fields.js';
const el=(tag,className='',text='')=>{const n=document.createElement(tag);n.className=className;n.textContent=text;return n;};
const short=x=>String(x||'').split('/').at(-1),fieldLabel=k=>k,assetURL=x=>'',typeset=()=>{};
const escapeHTML=text=>String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
${renderer}
${controls}
await loadMathInputs();await MathJax.startup.promise;
window.render=async cases=>{MathJax.typesetClear([main]);main.replaceChildren();
  for(const q of cases){const card=el('article','content-card'), title=el('h2','',q.label);card.dataset.id=q.id;
    const prompt=markdown(q.problem,'prose',q.fields), fields=el('div','answer-fields');card.append(title,prompt,fields);
    mountInlineFields(prompt,fields,q.fields,f=>fieldControl(f,false,q.id,q.problem,''));
    if(q.solution)card.append(markdown(q.solution,'prose worked-solution'));main.append(card);}
  await MathJax.typesetPromise([main]);await document.fonts.ready;
  return [...main.children].map(card=>({id:Number(card.dataset.id),radioCount:card.querySelectorAll('input[type=radio]').length,cardWidth:card.clientWidth,cardScrollWidth:card.scrollWidth,
    code:[...card.querySelectorAll('pre code')].map(n=>n.textContent),
    promptSlots:card.querySelector('.prose').querySelectorAll('[data-field-key]').length,
    inlineEditors:card.querySelector('.prose').querySelectorAll('math-field').length,
    fallbackEditors:card.querySelector('.answer-fields').querySelectorAll('math-field').length,
    mathErrors:[...card.querySelectorAll('[data-mjx-error],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),
    tables:[...card.querySelectorAll('g[data-mml-node="mtable"]')].map(n=>({rows:n.querySelectorAll('g[data-mml-node="mtr"]').length})),
    math:[...card.querySelectorAll('mjx-container')].map(n=>({width:n.clientWidth,scrollWidth:n.scrollWidth,height:n.clientHeight,svgWidth:n.querySelector('svg')?.getBoundingClientRect().width})),
  }));
};window.ready=true;
</script>`;
const mime={'.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.woff2':'font/woff2','.woff':'font/woff','.json':'application/json'};
const server=http.createServer((req,res)=>{
  if(req.url==='/probe'){res.setHeader('Content-Type','text/html');res.end(html);return;}
  const file=path.join(root,decodeURIComponent(req.url.split('?')[0]));
  if(!file.startsWith(root+path.sep)){res.writeHead(404);res.end();return;}
  try{res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.writeHead(404);res.end();}
});
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'triangular-rendering-'));
let browser,session,id=0,buf='';const pending=new Map(),errors=[];
const send=(method,params={},sid=session)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});browser.stdio[3].write(JSON.stringify({id:n,method,params,...(sid?{sessionId:sid}:{})})+'\0');});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
(async()=>{try{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  browser=spawn('/usr/bin/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--remote-debugging-pipe','--user-data-dir='+profile,'about:blank'],{stdio:['ignore','ignore','ignore','pipe','pipe']});
  browser.stdio[4].on('data',chunk=>{buf+=chunk;let i;while((i=buf.indexOf('\0'))>=0){const m=JSON.parse(buf.slice(0,i));buf=buf.slice(i+1);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);}if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.text);}});
  const target=await send('Target.createTarget',{url:'about:blank'},null);session=(await send('Target.attachToTarget',{targetId:target.targetId,flatten:true},null)).sessionId;
  await send('Runtime.enable');await send('Page.enable');await send('Page.navigate',{url:'http://127.0.0.1:'+server.address().port+'/probe'});
  for(let n=0;n<150;n++){if(await evaluate('window.ready===true'))break;await new Promise(r=>setTimeout(r,100));}
  if(!await evaluate('window.ready===true'))throw new Error('Renderer unavailable: '+JSON.stringify(errors));
  const report={errors,measurements:[]};
  for(const width of [893,375]){
    await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});
    for(const level of ['easy','moderate','hard']){
      const data=cases.filter(q=>q.label.startsWith(level+' '));
      const items=await evaluate('render('+JSON.stringify(data)+')');report.measurements.push({width,level,items});
      if(width===893){const size=(await send('Page.getLayoutMetrics')).cssContentSize;const shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:size.width,height:size.height,scale:1}});fs.writeFileSync(path.join(__dirname,'rendering-'+level+'.png'),Buffer.from(shot.data,'base64'));}
    }
  }
  fs.writeFileSync(path.join(__dirname,'rendering-report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));
}finally{browser?.kill();server.close();await new Promise(r=>setTimeout(r,250));fs.rmSync(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100});}})().catch(e=>{console.error(e);process.exitCode=1;});
