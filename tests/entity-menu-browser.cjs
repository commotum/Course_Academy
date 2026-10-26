// Offline integration checks: real page modules and DOM, mocked HTTP/clipboard.
// No learner database or writer is opened by this test.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const { chromium } = require(process.env.COURSE_ACADEMY_PLAYWRIGHT_MODULE || path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));
const cache = path.join(os.homedir(), '.cache/ms-playwright');
const executablePath = fs.readdirSync(cache).filter(name => name.startsWith('chromium_headless_shell-')).sort().reverse()
  .map(name => path.join(cache, name, 'chrome-headless-shell-linux64/chrome-headless-shell')).find(fs.existsSync);
const fixture = `<!doctype html><html><head><link rel="stylesheet" href="/ui/navigation.css"><style>body{background:#222;color:white}article,section{padding:12px;border:1px solid gray;margin:8px}dialog{padding:30px}#dialog-topic{padding:20px}</style></head><body>
<section id="course-topic">Course topic</section><section id="assignment-topic">Assignment preparation topic</section><section id="other-topic">Other topic</section>
<article id="question"><h2 id="kp">Knowledge point</h2><p id="prompt">Question text</p><input id="answer" value="editable answer"><textarea id="text-answer">Text answer</textarea><math-field id="math-answer">x</math-field></article>
<div id="spoof" data-step-db-id="999">Unregistered content</div><dialog id="dialog"><h2 id="dialog-topic">Topic in dialog</h2></dialog>
<script type="module">
import {attachStepMenu} from '/ui/step-menu.js';import {attachTopicMenu} from '/ui/topic-menu.js';import {attachEntityMenu,closeEntityMenu,copyText} from '/ui/entity-menu.js';
const topic={id:20,uuid:'topic-uuid',title:'Topic twenty',mathAcademyId:123};
for(const id of ['course-topic','assignment-topic','dialog-topic'])attachTopicMenu(document.getElementById(id),topic);
attachTopicMenu(document.getElementById('other-topic'),{id:25,uuid:'other-uuid',title:'Other topic'});
attachStepMenu(document.getElementById('question'),22,'e-9',{kind:'question'});attachStepMenu(document.getElementById('kp'),33,null,{kind:'knowledge point'});
window.register=attachStepMenu;window.closeMenu=closeEntityMenu;window.ready=true;
</script></body></html>`;
let state;
const server = http.createServer((req,res) => {
 const url = new URL(req.url,'http://localhost');
 if(url.pathname==='/fixture'){res.setHeader('Content-Type','text/html');res.end(fixture);return;}
 if(url.pathname==='/' || url.pathname==='/targets'){res.setHeader('Content-Type','text/html');res.end(fs.readFileSync(path.join(root,'ui/Math-Academy-Graph-Explorer.html')));return;}
 if(url.pathname.startsWith('/api/')){
  state.reads.push(url.pathname + url.search);
  const reply = body => {res.setHeader('Content-Type','application/json');res.end(JSON.stringify(body));};
  if(url.pathname==='/api/developer-mode'){reply({enabled:state.dev,pausedTasks:[]});return;}
  if(url.pathname==='/api/learner'){reply({basis:42,learner:state.learner});return;}
  if(url.pathname==='/api/topic-study-availability'){
   const topicId=Number(url.searchParams.get('topicId'));
   const respond=()=>reply({basis:42,topicId,available:true,resumable:false,completed:false,review:{available:true,resumable:false},...state.availability[topicId]});
   if(state.holdAvailability) state.pending.push(respond);else respond();return;
  }
  if(url.pathname==='/api/queue-topic' || url.pathname==='/api/target'){
   let body='';req.on('data',chunk=>body+=chunk);req.on('end',()=>{
    const operation=JSON.parse(body),collection=url.pathname==='/api/target'?'targets':'queue';state.writes.push({path:url.pathname,body:operation});
    const values=new Set(state.learner[collection]);if(operation.selected)values.add(operation.topicId);else values.delete(operation.topicId);state.learner[collection]=[...values];
    if(state.failWrite){state.failWrite=false;res.statusCode=503;reply({error:'Reply unavailable after saving. Retry to confirm this change.'});return;}reply({basis:43,learner:state.learner});
   });return;
  }
  if(url.pathname==='/api/graph-explorer') {reply({basis:42,learner:state.learner,courses:[{id:'course',title:'Course',topicIds:[20,25,30]}],nodes:[{id:20,uuid:'topic-uuid',name:'Topic twenty',mathAcademyId:123},{id:25,uuid:'other-uuid',name:'Other topic'},{id:30,uuid:'third-uuid',name:'Third topic'}],links:[{source:20,target:25},{source:20,target:30}],repetitions:{20:1},learned:{20:true},targetSchedule:[]});return;}
  reply({});return;
 }
 const file=path.resolve(root,'.'+url.pathname);
 if(!file.startsWith(root+'/ui/')||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.statusCode=404;res.end();return;}
 res.setHeader('Content-Type',file.endsWith('.css')?'text/css':file.endsWith('.svg')?'image/svg+xml':'text/javascript');res.end(fs.readFileSync(file));
});
function reset(){state={dev:false,learner:{id:'test',name:'Test learner',courseId:'course',selfDirected:true,queue:[],targets:[30]},availability:{},reads:[],writes:[],pending:[]};}
(async()=>{let browser;const checks=[];const record=checks.push.bind(checks);checks.push=value=>{console.log(value);return record(value);};try{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const origin='http://127.0.0.1:'+server.address().port;
 browser=await chromium.launch({headless:true,executablePath,args:['--disable-dev-shm-usage']});const context=await browser.newContext({viewport:{width:1000,height:900}});
 await context.addInitScript(()=>{window.copied=[];window.clipboardBlocked=false;Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{if(window.clipboardBlocked)throw Error('blocked');window.copied.push(text);}}});});
 const page=await context.newPage();page.setDefaultTimeout(10000);const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.route('**/*',route=>new URL(route.request().url()).origin===origin?route.continue():route.abort());
 const menu=page.locator('.entity-context-menu');const item=id=>menu.locator(`[data-action="${id}"]`);
 const open=async selector=>{await page.locator(selector).click({button:'right'});await menu.waitFor({state:'visible'});};
 const settle=async()=>{await page.waitForFunction(()=>!document.querySelector('.entity-context-menu [data-action="study-topic"]') || document.querySelector('.entity-context-menu [data-action="study-topic"]').title!=='Checking lesson availability…');};
 reset();await page.goto(origin+'/fixture');await page.waitForFunction(()=>window.ready);
 await open('#course-topic');await settle();await menu.getByRole('menuitem',{name:'Add to queue: Topic twenty',exact:true}).waitFor();
 assert.equal(await item('copy-topic').count(),0);
 const labels=await menu.getByRole('menuitem').allTextContents();
 assert.deepEqual(labels.map(s=>s.replace('↗','')),['Copy topic :db/id','Study now','Review Topic','Go to topic','View in graph','Add to queue','Add to targets']);
 await page.keyboard.press('Escape');await open('#assignment-topic');await settle();
 assert.deepEqual((await menu.getByRole('menuitem').allTextContents()).map(s=>s.replace('↗','')),labels.map(s=>s.replace('↗','')));
 assert.equal(state.writes.length,0);checks.push('topic actions match across surfaces; opening is read only');
 await item('copy-db-id').click();await page.waitForFunction(()=>copied.length===1);assert.equal(await page.evaluate(()=>copied[0]),':db/id=20');
 await open('#prompt');assert.equal(await item('study-topic').count(),0);assert.equal(await item('copy-db-id').textContent(),'Copy question :db/id');
 await item('copy-db-id').click();await page.waitForFunction(()=>copied.length===2);assert.equal(await page.evaluate(()=>copied[1]),':db/id=22');
 await open('#kp');assert.equal(await item('copy-db-id').textContent(),'Copy knowledge point :db/id');assert.equal(await item('copy-ma-id').count(),0);await page.keyboard.press('Escape');
 assert.equal(await page.locator('.entity-actions-trigger,.entity-menu-tools').count(),0);await page.locator('#question').focus();await page.keyboard.press('Shift+F10');assert.equal(await item('copy-ma-id').count(),0);await item('copy-db-id').click();await page.waitForFunction(()=>copied.length===3);assert.equal(await page.evaluate(()=>copied[2]),':db/id=22');checks.push('nested question and knowledge point identities; keyboard access without added UI');
 for(const selector of ['#answer','#text-answer','#math-answer','#spoof']){await page.locator(selector).click({button:'right'});assert.equal(await menu.isVisible(),false);}
 await page.keyboard.down('Shift');await page.locator('#course-topic').click({button:'right'});await menu.waitFor({state:'visible'});await settle();
 assert.equal(await item('open-topic').getAttribute('aria-label'),'Go to topic · Opens in a new tab');
 await page.keyboard.up('Shift');assert.equal(await item('open-topic').getAttribute('aria-label'),'Go to topic');await page.keyboard.press('Escape');
 await page.keyboard.down('Shift');await page.locator('#prompt').click({button:'right'});await menu.waitFor({state:'visible'});
 assert.equal(await item('copy-db-id').textContent(),'Copy question :db/id');await page.keyboard.up('Shift');await page.keyboard.press('Escape');
 checks.push('Shift-right-click opens topic and question menus; native editing and untrusted attribute handling remain intact');
 state.availability[20]={available:false,reason:'Not enough fresh questions',review:{available:false,reason:'Not enough fresh questions for review'}};
 await open('#course-topic');await settle();assert.equal(await item('study-topic').getAttribute('aria-disabled'),'true');assert.equal(await item('study-topic').getAttribute('href'),null);
 await item('study-topic').dispatchEvent('click');assert.equal(await menu.isVisible(),true);assert.equal(await item('study-topic').getAttribute('aria-describedby')!==null,true);
 await page.keyboard.press('Home');await page.keyboard.press('ArrowDown');assert.equal(await item('study-topic').evaluate(n=>n===document.activeElement),true);
 await page.keyboard.press('Escape');assert.equal(await page.locator('#course-topic').evaluate(n=>n===document.activeElement),true);
 state.availability[20]={completed:true};await open('#course-topic');await settle();assert.match(await item('study-topic').textContent(),/Study now/);await page.keyboard.press('Escape');
 state.availability[20]={resumable:true,review:{available:true,resumable:true}};await open('#course-topic');await settle();assert.match(await item('study-topic').textContent(),/Resume Study/);assert.match(await item('review-topic').textContent(),/Review Topic/);await page.keyboard.press('Escape');checks.push('unavailable actions explain reasons; completed and resumed labels; keyboard focus');
 state.holdAvailability=true;state.availability={};await open('#course-topic');await page.waitForFunction(()=>document.querySelector('[data-action="study-topic"]').getAttribute('aria-disabled')==='true');
 await page.waitForTimeout(50);await page.keyboard.press('Escape');await open('#other-topic');await page.waitForTimeout(50);assert.equal(state.pending.length,2);
 state.pending[0]();await page.waitForTimeout(30);assert.equal(await item('study-topic').getAttribute('aria-disabled'),'true');state.pending[1]();await settle();assert.equal(await item('study-topic').getAttribute('href'),'/learn?topicId=25');state.holdAvailability=false;await page.keyboard.press('Escape');checks.push('stale async response cannot enable another topic');
 await open('#course-topic');await settle();await menu.getByRole('menuitem',{name:'Add to queue: Topic twenty',exact:true}).click();await menu.waitFor({state:'hidden'});assert.deepEqual(state.learner.queue,[20]);
 await open('#course-topic');await menu.getByRole('menuitem',{name:'Remove from queue: Topic twenty',exact:true}).waitFor();state.failWrite=true;
 await menu.getByRole('menuitem',{name:'Remove from queue: Topic twenty',exact:true}).click();await menu.getByRole('menuitem',{name:/Retry: Remove from queue/}).waitFor();
 const failed=state.writes.at(-1).body;await menu.getByRole('menuitem',{name:/Retry: Remove from queue/}).click();await menu.waitFor({state:'hidden'});assert.deepEqual(state.writes.at(-1).body,failed);assert.deepEqual(state.learner.queue,[]);checks.push('queue add/remove and uncertain save exact retry');
 await page.evaluate(()=>document.getElementById('dialog').showModal());await open('#dialog-topic');assert.equal(await menu.evaluate(n=>n.parentElement.id),'dialog');await page.keyboard.press('Escape');await page.evaluate(()=>document.getElementById('dialog').close());
 await page.evaluate(()=>{const p=document.createElement('p');p.id='large-id';p.textContent='Large ID';document.body.append(p);register(p,'18446744073709551615',null,{kind:'question'});});await open('#large-id');await item('copy-db-id').click();await page.waitForFunction(()=>copied.includes(':db/id=18446744073709551615'));
 await page.evaluate(()=>window.clipboardBlocked=true);await open('#course-topic');await item('copy-db-id').click();await page.locator('.entity-manual-copy').waitFor({state:'visible'});assert.equal(await page.locator('.entity-manual-copy textarea').inputValue(),':db/id=20');await page.locator('.entity-manual-copy button').click();checks.push('top-layer dialogs; lossless IDs; manual clipboard fallback');
 await open('#course-topic');await settle();const popupPromise=context.waitForEvent('page');await item('open-topic').click({modifiers:['Shift']});const popup=await popupPromise;await popup.waitForLoadState();assert.match(popup.url(),/\/topic\?topic=topic-uuid$/);await popup.close();checks.push('Shift navigation opens a new tab');
 reset();state.dev=true;state.learner.selfDirected=false;await page.goto(origin+'/fixture');await page.waitForFunction(()=>window.ready);await open('#course-topic');await settle();assert.match(await item('study-topic').textContent(),/Study now/);assert.equal(await item('review-topic').getAttribute('aria-disabled'),'true');assert.equal(await menu.getByRole('menuitem',{name:/Add to targets/}).count(),0);assert.equal(await menu.getByRole('menuitem',{name:/Add to queue/}).isDisabled(),true);assert.equal(state.writes.length,0);checks.push('developer preview and mutation gating; target mode gating');
 reset();await page.goto(origin+'/?course=all');await page.locator('#nodes .node').first().waitFor();
 await page.locator('#topic-20 .node-hit').dispatchEvent('contextmenu',{clientX:500,clientY:400,shiftKey:true});await menu.waitFor({state:'visible'});await settle();assert.equal(await menu.count(),1);assert.equal(await page.locator('#nodeContextMenu').count(),0);assert.equal(await item('copy-node').count(),0);assert.equal(await item('copy-ma-id').count(),0);assert.equal(await item('review-topic').count(),1);await page.screenshot({path:'/tmp/course-academy-unified-menu.png'});await page.keyboard.press('Escape');
 await page.locator('#svg').dispatchEvent('contextmenu',{clientX:500,clientY:400,shiftKey:true});await menu.waitFor({state:'visible'});assert.equal(await item('study-topic').count(),0);await item('copy-canvas-ids').click();await page.waitForFunction(()=>copied.length===1);assert.deepEqual(new Set((await page.evaluate(()=>copied[0])).split('\n')),new Set(['20','25','30']));
 await page.locator('#topic-20 .node-hit').dispatchEvent('click');await open('#infoTitle');assert.equal(await item('study-topic').count(),1);await page.keyboard.press('Escape');await page.locator('#svg').focus();await page.keyboard.press('Shift+F10');await item('copy-canvas-ids').waitFor();await page.keyboard.press('Escape');checks.push('actual graph nodes, selected title and canvas use one component; canvas keyboard and complete copy');
 assert.deepEqual(errors,[]);console.log(JSON.stringify({checks,pageErrors:errors},null,2));
 }finally{await browser?.close();server.closeAllConnections();server.close();}})().catch(error=>{console.error(error);process.exitCode=1;});
