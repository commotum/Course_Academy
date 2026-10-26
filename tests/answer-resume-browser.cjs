// Real lesson renderer and answer controls with mocked resume requests. No EDB.
const assert = require('node:assert/strict');
const fs = require('node:fs'), http = require('node:http'), path = require('node:path'), os = require('node:os');
const root = path.resolve(__dirname, '..');
const { chromium } = require(process.env.COURSE_ACADEMY_PLAYWRIGHT_MODULE || path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));
const cache = path.join(os.homedir(), '.cache/ms-playwright');
const executablePath = fs.readdirSync(cache).filter(n => n.startsWith('chromium_headless_shell-')).sort().reverse().map(n => path.join(cache,n,'chrome-headless-shell-linux64/chrome-headless-shell')).find(fs.existsSync);
const source = fs.readFileSync(path.join(root,'ui/learning.js'),'utf8');
const controllers = source.slice(source.indexOf('const $'), source.indexOf("$('retryButton').addEventListener"));
const visibility = source.slice(source.indexOf('async function syncAfterVisibility()'), source.indexOf("document.addEventListener('visibilitychange'"));
const html = `<!doctype html><html><head><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><script src="/ui/vendor/dompurify/purify.min.js"></script></head><body>
<main id="main"></main><div id="learnerName"></div><a id="courseLink"></a><div id="errorBanner" hidden><span id="errorText"></span><button id="retryButton">Retry</button></div><div id="announcement"></div>
<script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {decorateSourceTables} from '/ui/content-tables.js';import {protectMath} from '/ui/math-protection.js';import {romanLists} from '/ui/prose-lists.js';
import {loadMathInputs,inlinePrompt,mountInlineFields,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput,questionFeedback,feedbackHeading,responsesComplete} from '/ui/question-fields.js';
let developer=false;const isDeveloperMode=()=>developer,attachStepMenu=()=>{},createStudySidebar=()=>document.createElement('aside');
${controllers}
${visibility}
typeset=async()=>{};loadMath=async()=>{};
window.calls=[];window.pending=[];window.hold=false;window.failNext=false;window.nextTask=null;
window.fetch=async(path,options)=>{
 const body=options.body?JSON.parse(options.body):null;calls.push({path,body});
 if(path!=='/api/resume')throw Error('Unexpected API request: '+path);
 if(hold)await new Promise(resolve=>pending.push(resolve));
 if(failNext){failNext=false;return {ok:false,status:503,json:async()=>({error:'Resume reply unavailable'})};}
 const result=structuredClone(window.nextTask||window.server);result.status='started';result.step.status='started';
 return {ok:true,json:async()=>result};
};
document.getElementById('retryButton').addEventListener('click',()=>retryOperation?.());
window.configure=async(kind,type='lesson',options={})=>{
 document.activeElement?.blur();seenTaskSteps.clear();
 calls.length=0;pending.length=0;hold=false;failNext=false;window.nextTask=null;answerResume=null;developer=!!options.preview;
 drafts.clear();manuallyPausedTasks.clear();sessionStorage.clear();lessonView=null;task=null;busy=false;retryOperation=null;timerPausePending=false;
 const field={id:30,key:'value',type:kind,choices:[]};
 if(kind==='math'){field.type='blank';field.answerType='math';}
 if(kind==='blank')field.answerType='text';
 if(kind==='radio'||kind==='select'){field.key=kind==='radio'?'selection':'value';field.choices=[{id:41,type:'text',value:'First option'},{id:42,type:'text',value:'Second option'}];}
 if(kind==='checkbox'){field.key='A checkbox statement';field.choices=[{id:41,type:'text',value:'true'},{id:42,type:'text',value:'false'}];}
 const step={itemId:10,contentId:101,kind:'question',status:options.answered?'correct':'paused',title:'Question',markdown:'Answer this question.',fields:[field],canContinue:!!options.answered};
 const data={taskId:123,activityId:456,type,status:'paused',title:'Paused activity',learner:{id:'test',name:'Learner'},course:{id:'course'},elapsedSeconds:10,step,progress:{stepNumber:1,totalSteps:2,presented:1},history:[]};
 if(options.archived){data.history=[{order:1,number:1,total:2,step:structuredClone({...step,itemId:9,status:'correct'})}];data.progress.stepNumber=2;data.progress.presented=2;}
 window.server=structuredClone(data);task=data;
 if(developer){task={...data,steps:[step]};previewStepIndex=0;await renderPreview();}
 else{setManualPause(data.taskId,true);await renderTask(data);}
 setBusy(false);
};
window.state=()=>({status:task.status,item:task.step?.itemId,running:clock.running,manual:isManuallyPaused(task.taskId),responses:drafts.get(task.step?.itemId),busy,elapsed:clock.elapsed});
window.release=()=>pending.splice(0).forEach(resolve=>resolve());
window.responses=()=>collectResponses(lessonView.current.querySelector('form'),task.step.fields);
window.ready=true;
</script></body></html>`;
const server=http.createServer((req,res)=>{
 const url=new URL(req.url,'http://localhost');if(url.pathname==='/fixture'){res.setHeader('content-type','text/html');res.end(html);return;}
 const file=path.resolve(root,'.'+url.pathname);if(!file.startsWith(root+'/ui/')||!fs.existsSync(file)){res.statusCode=404;res.end();return;}
 const ext=path.extname(file);res.setHeader('content-type',({'.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.woff2':'font/woff2'})[ext]||'application/octet-stream');res.end(fs.readFileSync(file));
});
(async()=>{let browser;const checks=[];try{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));browser=await chromium.launch({headless:true,executablePath,args:['--disable-dev-shm-usage']});
 const page=await browser.newPage({viewport:{width:1100,height:900}});page.setDefaultTimeout(10000);const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 const origin='http://127.0.0.1:'+server.address().port;await page.route('**/*',route=>new URL(route.request().url()).origin===origin?route.continue():route.abort());
 await page.goto(origin+'/fixture');await page.waitForFunction(()=>window.ready);
 const configure=async(kind,type='lesson',options={})=>page.evaluate(args=>configure(...args),[kind,type,options]);
 const started=async()=>{await page.waitForFunction(()=>state().status==='started'&&!state().busy);assert.equal(await page.evaluate(()=>calls.length),1);assert.equal((await page.evaluate(()=>state())).running,true);assert.equal((await page.evaluate(()=>state())).manual,false);};
 for(const type of ['lesson','review'])for(const kind of ['blank','free','math','radio','checkbox','select']){
  await configure(kind,type);assert.equal(await page.evaluate(()=>calls.length),0);await page.evaluate(()=>hold=true);
  if(kind==='radio'||kind==='checkbox')await page.locator('.lesson-feed .choice').first().click();
  else if(kind==='select'){await page.locator('.answer-select-trigger').click();await page.waitForFunction(()=>pending.length===1);await page.locator('.answer-select-option').filter({hasText:'Second option'}).click();}
  else{const input=page.locator(kind==='free'?'textarea':kind==='math'?'math-field':'input:not([type=hidden])');await input.click();await page.waitForFunction(()=>pending.length===1);if(kind==='math')await page.waitForFunction(()=>document.querySelector('math-field').shadowRoot.activeElement);await page.keyboard.type(kind==='math'?'2+3':'typed answer');}
  await page.waitForFunction(()=>pending.length===1);assert.equal((await page.evaluate(()=>state())).running,false);
  const before=await page.evaluate(()=>JSON.stringify(responses()));
  await page.evaluate(()=>release());await started();assert.equal(await page.evaluate(()=>JSON.stringify(state().responses)),before);
  await page.waitForFunction(()=>document.activeElement?.closest('.answer-field'));
  const focused=await page.evaluate(()=>{const node=document.activeElement;return {tag:node.tagName,type:node.type,value:node.value,checked:node.checked};});
  if(kind==='blank'){assert.equal(focused.value,'typed answer');await page.keyboard.type('!');assert.equal(await page.locator('input:not([type=hidden])').inputValue(),'typed answer!');}
  if(kind==='free')assert.equal(focused.value,'typed answer');
  if(kind==='math'){assert.equal(focused.tag,'MATH-FIELD');assert.equal(focused.value,'2+3');}
  if(kind==='radio'||kind==='checkbox')assert.equal(focused.checked,true);
  if(kind==='select')assert.match(await page.locator('.answer-select-trigger').textContent(),/Second option/);
  checks.push(type+' '+kind+': first interaction and focus survive resume');
 }
 // A response that arrives before pointer-up must not eat the selected choice.
 for(const kind of ['radio','checkbox']){
  await configure(kind,'review');const input=page.locator('.choice input:not([type=hidden])').first();const box=await input.boundingBox();await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();await page.waitForTimeout(60);assert.equal(await page.evaluate(()=>calls.length),0);await page.mouse.up();await started();assert.equal(await page.locator('.choice input:not([type=hidden])').first().isChecked(),true,kind+' '+JSON.stringify(await page.evaluate(()=>({responses:state().responses,inputs:[...document.querySelectorAll('input')].map(n=>({value:n.value,checked:n.checked,type:n.type})),calls}))));
 }
 checks.push('fast resume cannot consume the first radio or checkbox click');
 await configure('blank');await page.locator('input').focus();await started();assert.equal(await page.locator('input').evaluate(n=>n===document.activeElement),true);checks.push('keyboard focus resumes and restores the field');
 await configure('select');await page.locator('.answer-select-trigger').click();await started();await page.locator('.answer-select-menu').waitFor({state:'visible'});checks.push('select choices stay open after resume');
 await configure('blank');await page.locator('input').click({button:'right'});assert.equal(await page.evaluate(()=>calls.length),0);checks.push('native editing context menu does not resume');
 await configure('blank');await page.evaluate(()=>{hold=true;failNext=true;});await page.locator('input').click();await page.waitForFunction(()=>pending.length===1);await page.keyboard.type('keep my draft');await page.evaluate(()=>{hold=false;release();});await page.locator('#errorBanner').waitFor({state:'visible'});assert.equal((await page.evaluate(()=>state())).running,false);
 const original=await page.evaluate(()=>calls[0].body);await page.locator('input').press('End');await page.keyboard.type('!');await page.waitForFunction(()=>state().status==='started'&&!state().busy);assert.deepEqual(await page.evaluate(()=>calls[1].body),original);assert.equal(await page.locator('input').inputValue(),'keep my draft!');checks.push('failed resume preserves draft and retries the same request');
 await configure('radio');await page.evaluate(()=>{hold=true;nextTask=structuredClone(server);nextTask.step.itemId=11;nextTask.step.contentId=102;});await page.locator('.choice').first().click();await page.waitForFunction(()=>pending.length===1);await page.evaluate(()=>release());await page.waitForFunction(()=>state().item===11&&!state().busy);assert.equal(await page.locator('.choice input:checked').count(),0);checks.push('another tab advancing cannot apply the old choice to a new question');
 for(const options of [{answered:true},{archived:true},{preview:true}]){
  await configure('blank','lesson',options);const inputs=page.locator('[data-answer-input]');assert.equal(await inputs.first().isDisabled(),!options.preview);
  if(options.archived){await inputs.first().dispatchEvent('focusin');assert.equal(await page.evaluate(()=>calls.length),0);}else{await page.locator('.content-card').first().click();assert.equal(await page.evaluate(()=>calls.length),0);}
 }
 await configure('blank','assessment');assert.equal(await page.locator('[data-answer-input]').first().isDisabled(),true);await page.locator('.content-card').click();assert.equal(await page.evaluate(()=>calls.length),0);checks.push('answered and archived content, previews and assessments do not auto-resume');
 assert.deepEqual(errors,[]);console.log(JSON.stringify({checks,pageErrors:errors},null,2));
 }finally{await browser?.close();server.closeAllConnections();server.close();}})().catch(error=>{console.error(error);process.exitCode=1;});
