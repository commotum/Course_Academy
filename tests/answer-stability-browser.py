"""Exercise real question layout and scrolling; no live API or learner writes."""
from pathlib import Path
import http.server
import json
import subprocess
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'ui/learning.js').read_text()
controllers = source[source.index('const $'):source.index("$('retryButton').addEventListener")]
html = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css">
<script src="/ui/vendor/dompurify/purify.min.js"></script>
<script>window.MathJax={tex:{inlineMath:[['$','$'],['\\\\(','\\\\)']]},svg:{fontCache:'none'}};</script>
</head><body><main id="main"></main><div id="learnerName"></div><a id="courseLink"></a>
<div id="errorBanner" hidden><span id="errorText"></span></div><div id="announcement"></div>
<script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';
import {decorateSourceTables} from '/ui/content-tables.js';
import {decorateEquationGroups} from '/ui/equation-groups.js';
import {protectMath} from '/ui/math-protection.js';import {romanLists} from '/ui/prose-lists.js';
import {loadMathInputs,inlinePrompt,mountInlineFields,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput,questionFeedback,feedbackHeading,responsesComplete} from '/ui/question-fields.js';
const isDeveloperMode=()=>false,attachStepMenu=()=>{},createStudySidebar=()=>document.createElement('aside');
''' + controllers + '''
async function syncAfterVisibility(){}
window.render=async data=>{task=data;await renderTask(data);await typesetting;};
window.whenRendered=()=>typesetting;
window.ready=true;
</script></body></html>'''

javascript = r'''
const assert=require('assert/strict');
const {chromium}=require('/home/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/home/jake/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell',args:['--disable-dev-shm-usage']});
 try {
  const results=[];
  for(const width of [1200,390]) {
   const page=await browser.newPage({viewport:{width,height:800}}), errors=[];
   page.on('pageerror',e=>errors.push(String(e)));
   await page.goto(ORIGIN+'/fixture');await page.waitForFunction(()=>window.ready);
   const fields=[{id:1,key:'value',type:'blank',answerType:'math'},...Array.from({length:14},(_,n)=>({id:n+10,key:'Statement '+(n+1)+': '+ 'Consider this mathematical statement. '.repeat(3),type:'checkbox',choices:[{id:100+n*2,type:'text',value:'true'},{id:101+n*2,type:'text',value:'false'}]}))];
   const initial={taskId:4000000000000001,activityId:200,type:'review',title:'Tall question',status:'started',learner:{id:'fixture'},course:{id:'fixture'},progress:{stepNumber:1,totalSteps:5,presented:1},step:{itemId:4000000000000002,contentId:300,kind:'question',markdown:('Work with $x^2+1$.\n\n'.replaceAll('\\n','\n')).repeat(30)+'\n\nEnter $x=$ {{value}}.',status:'started',canContinue:false,fields}};
   const graded=structuredClone(initial);graded.taskId=501;graded.step.itemId=502;
   graded.saveState={status:'saved',pending:0};graded.idAliases={[initial.taskId]:501,[initial.step.itemId]:502};
   graded.step.status='incorrect';graded.step.canContinue=true;graded.step.solution='The worked solution is $x=2$.\n\n'+'Explanation. '.repeat(300);
   graded.step.fields.reverse();
   for(const f of graded.step.fields) {
    if(f.id===1){f.response={type:'math',value:'2'};f.correctAnswer={type:'math',value:'2'};f.grade='correct';}
    else {f.response={id:f.choices[1].id,choiceId:f.choices[1].id,type:'text',value:'false'};f.correctAnswer=f.choices[0];f.grade='incorrect';}
   }
   await page.route('**/api/answer',route=>route.fulfill({json:graded}));
   await page.evaluate(data=>window.render(data),initial);
   await page.locator('math-field').evaluate(node=>{node.value='2';node.dispatchEvent(new Event('input',{bubbles:true}));});
   await page.locator('.answer-actions button').scrollIntoViewIfNeeded();
   const before=await page.evaluate(()=>{
    window.originalCard=document.querySelector('.lesson-content');window.originalInputs=[...document.querySelectorAll('[data-answer-input]')];window.originalMath=document.querySelector('mjx-container');
    return {y:scrollY,positions:originalInputs.map(n=>({name:n.name,top:n.getBoundingClientRect().top+scrollY}))};
   });
   await page.locator('.answer-actions button').click();
   await page.waitForSelector('.feedback-heading');await page.evaluate(()=>window.whenRendered());
   const after=await page.evaluate(()=>({y:scrollY,sameCard:originalCard===document.querySelector('.lesson-content'),sameInputs:originalInputs.every(n=>n.isConnected),sameMath:originalMath?.isConnected,
    positions:originalInputs.map(n=>({name:n.name,top:n.getBoundingClientRect().top+scrollY})),heading:document.querySelector('.feedback-heading').getBoundingClientRect().toJSON(),disabled:originalInputs.every(n=>n.disabled),badge:document.querySelector('.feedback-badge').textContent}));
   assert.equal(after.sameCard,true);assert.equal(after.sameInputs,true);assert.equal(after.sameMath,true);assert.equal(after.disabled,true);assert.match(after.badge,/Incorrect/);
   assert.deepEqual(after.positions.map(n=>n.name),before.positions.map(n=>n.name));
   for(let i=0;i<before.positions.length;i++)assert.ok(Math.abs(before.positions[i].top-after.positions[i].top)<2,'field moved vertically');
   assert.ok(Math.abs(before.y-after.y)<100,'submission jumped away from the answer area');
   assert.ok(after.heading.top>=0&&after.heading.bottom<=800,'feedback is outside viewport');
   // Re-reading the same graded question must also retain its editors/layout.
   await page.evaluate(data=>window.render(data),graded);
   assert.equal(await page.evaluate(()=>originalCard===document.querySelector('.lesson-content')),true);
   // Enter from a field near the top of a tall answer form reveals its result.
   await page.reload();await page.waitForFunction(()=>window.ready);
   await page.evaluate(data=>window.render(data),initial);
   await page.locator('math-field').evaluate(node=>{node.value='2';node.dispatchEvent(new Event('input',{bubbles:true}));});
   await page.locator('math-field').scrollIntoViewIfNeeded();
   await page.locator('form').evaluate(form=>form.requestSubmit(form.querySelector('button[type="submit"]')));
   await page.waitForSelector('.feedback-heading');await page.evaluate(()=>window.whenRendered());
   const heading=await page.locator('.feedback-heading').boundingBox();assert.ok(heading.y>=0&&heading.y+heading.height<=800,JSON.stringify({width,heading,y:await page.evaluate(()=>scrollY)}));
   assert.deepEqual(errors,[]);results.push({width,stableFields:true,retainedMathAndInputs:true,scrollDelta:after.y-before.y,feedbackVisible:true,enterRevealsFeedback:true});
   await page.close();
  }
  console.log(JSON.stringify({passed:true,results}));
 } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
'''

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=str(ROOT), **kwargs)
    def log_message(self, *args): pass
    def do_GET(self):
        if self.path == '/fixture' or self.path.startswith('/learn?'):
            data=html.encode();self.send_response(200);self.send_header('Content-Type','text/html');self.end_headers();self.wfile.write(data)
        else: super().do_GET()

server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
    with tempfile.TemporaryDirectory(prefix='answer-stability-') as tmp:
        script=Path(tmp)/'test.cjs';script.write_text(javascript.replace('ORIGIN',json.dumps(f'http://127.0.0.1:{server.server_port}')))
        subprocess.run(['/home/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node',str(script)],check=True,timeout=100)
finally: server.shutdown()
