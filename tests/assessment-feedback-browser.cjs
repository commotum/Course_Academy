// Render actual API-test outputs through the study UI; no live learner writes.
// Generate the fixture with COURSE_ACADEMY_ASSESSMENT_FEEDBACK_FIXTURE when
// running the native completed_assessment_reveals_feedback test.
const assert=require('node:assert/strict');
const fs=require('fs'),http=require('http'),path=require('path'),os=require('os');
const root=path.resolve(__dirname,'..');
const fixture=JSON.parse(fs.readFileSync(process.argv[2]||'/tmp/completed-assessment-feedback.json','utf8'));
const {chromium}=require(process.env.COURSE_ACADEMY_PLAYWRIGHT_MODULE||path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));
const executablePath=fs.readdirSync(path.join(os.homedir(),'.cache/ms-playwright')).filter(n=>n.startsWith('chromium_headless_shell-')).sort().reverse().map(n=>path.join(os.homedir(),'.cache/ms-playwright',n,'chrome-headless-shell-linux64/chrome-headless-shell')).find(fs.existsSync);
const source=fs.readFileSync(path.join(root,'ui/learning.js'),'utf8');
const controllers=source.slice(source.indexOf('const $'),source.indexOf("$('retryButton').addEventListener"));
const html=`<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><script src="/ui/vendor/dompurify/purify.min.js"></script></head><body>
<main id="main"></main><div id="learnerName"></div><a id="courseLink"></a><div id="announcement"></div>
<script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {decorateSourceTables} from '/ui/content-tables.js';import {protectMath} from '/ui/math-protection.js';import {romanLists} from '/ui/prose-lists.js';
import {loadMathInputs,inlinePrompt,mountInlineFields,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput,questionFeedback,feedbackHeading,responsesComplete} from '/ui/question-fields.js';
const isDeveloperMode=()=>false,attachStepMenu=()=>{},createStudySidebar=()=>document.createElement('aside');
${controllers}
typeset=async()=>{};loadMath=async()=>{};
window.renderFixture=async(data,reopen=false)=>{
 if(reopen){lessonView=null;seenTaskSteps.clear();sessionStorage.clear();main.replaceChildren();}
 task=data;await renderTask(data);
 return [...document.querySelectorAll('.lesson-content:not(.completion)')].map(content=>({
  number:Number(content.dataset.stepNumber),badge:content.querySelector('.feedback-badge')?.textContent,
  grade:content.querySelector('.feedback-badge')?.dataset.grade,
  badgeColor:content.querySelector('.feedback-badge')?getComputedStyle(content.querySelector('.feedback-badge')).backgroundColor:null,
  solution:content.querySelector('.worked-solution')?.textContent,
  feedback:content.querySelector('.feedback')?.textContent,
  answerInputs:[...content.querySelectorAll('[data-answer-input]')].map(input=>({disabled:input.disabled,readOnly:input.dataset.readOnly})),
 }));
};window.ready=true;
</script></body></html>`;
const server=http.createServer((req,res)=>{
 const url=new URL(req.url,'http://localhost');if(url.pathname==='/fixture'){res.setHeader('content-type','text/html');res.end(html);return;}
 const file=path.resolve(root,'.'+url.pathname);if(!file.startsWith(root+'/ui/')||!fs.existsSync(file)){res.statusCode=404;res.end();return;}
 res.setHeader('content-type',({'.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.woff2':'font/woff2'})[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));
});
(async()=>{let browser;try{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 browser=await chromium.launch({headless:true,executablePath,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1100,height:900}}),errors=[];
 page.on('pageerror',e=>errors.push(String(e)));const origin='http://127.0.0.1:'+server.address().port;
 await page.route('**/*',route=>new URL(route.request().url()).origin===origin?route.continue():route.abort());
 await page.goto(origin+'/fixture');await page.waitForFunction(()=>window.ready);
 const active=await page.evaluate(data=>renderFixture(data),fixture.active);
 assert.equal(active.length,1);assert.equal(active[0].badge,undefined);assert.equal(active[0].solution,undefined);
 const count=fixture.completed.questions.length;
 for(const reopen of [false,true]){
  const cards=await page.evaluate(({data,reopen})=>renderFixture(data,reopen),{data:fixture.completed,reopen});
  assert.equal(cards.length,count);assert.deepEqual(cards.map(card=>card.number),Array.from({length:count},(_,i)=>i+1));
  assert.equal(cards[0].badge,'Correct');assert.equal(cards[1].badge,'Incorrect');
  for(const card of cards){
   assert.match(card.solution,/One plus one is two/);
   assert.ok(card.answerInputs.every(input=>input.disabled&&input.readOnly==='true'));
   if(card.number>=3){
    assert.equal(card.badge,'Incorrect');assert.equal(card.grade,'incorrect');
    assert.equal(card.badgeColor,cards[1].badgeColor);
    assert.match(card.feedback,/Not answered/);assert.match(card.feedback,/correct value:[\s$]*2/);
   }
  }
  assert.equal(await page.locator('.assessment-controls,.answer-actions').count(),0);
 }
 assert.deepEqual(errors,[]);
 if(process.env.ASSESSMENT_FEEDBACK_SCREENSHOT)await page.screenshot({path:process.env.ASSESSMENT_FEEDBACK_SCREENSHOT,fullPage:true});
 console.log(JSON.stringify({passed:true,questions:count,unanswered:fixture.completed.assessmentScore.unanswered,redIncorrectFeedback:true,correctAnswersAndSolutions:true,reopenedResults:true,noPreSubmissionLeak:true}));
}finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}})().catch(error=>{console.error(error);process.exitCode=1;});
