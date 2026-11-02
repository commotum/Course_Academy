"""Verify real Study rendering and cache transitions with the studyGate contract.

Uses a captured read-only home response for card content. No live API requests,
assessment grading, or learner/database writes occur in this presentation test.
"""
import http.server
import json
import os
from pathlib import Path
import subprocess
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]
home_fixture = json.loads(Path(os.environ.get('STUDY_GATE_HOME_FIXTURE', str(ROOT/'tests/fixtures/study-gate-home.json'))).read_text())
required = [activity for activity in home_fixture['activities'] if activity.get('reason') == 'Required practice after assessment']
assert len(required) == 4, 'Fixture must contain four native required reviews'
source = (ROOT/'ui/learning.js').read_text()
controllers = source[source.index('const $'):source.index("$('retryButton').addEventListener")]
html = '''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><script src="/ui/vendor/dompurify/purify.min.js"></script></head><body>
<main id="main"></main><div id="learnerName"></div><a id="courseLink"></a><div id="errorBanner" hidden><span id="errorText"></span><button id="retryButton">Retry</button></div><div id="announcement"></div>
<script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {decorateSourceTables} from '/ui/content-tables.js';import {decorateEquationGroups} from '/ui/equation-groups.js';import {protectMath} from '/ui/math-protection.js';import {romanLists} from '/ui/prose-lists.js';
import {loadMathInputs,inlinePrompt,mountInlineFields,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput,questionFeedback,feedbackHeading,responsesComplete} from '/ui/question-fields.js';
const isDeveloperMode=()=>false,attachStepMenu=()=>{},createStudySidebar=()=>document.createElement('aside');
let nextHome=FIXTURE_HOME,nextSubmit=null,holdHome=false,releaseHome=null;const calls=[];
const fetch=async(path,settings)=>{calls.push({path,method:settings.method});if(holdHome&&['/api/home','/api/queue'].includes(path))await new Promise(resolve=>releaseHome=resolve);return {ok:true,json:async()=>structuredClone(path==='/api/submit'?nextSubmit:nextHome)};};
''' + controllers + '''
typeset=async()=>{};loadMath=async()=>{};async function syncAfterVisibility(){}
window.harness={configure({home,submit,hold}={}){if(home)nextHome=home;if(submit)nextSubmit=submit;if(hold!==undefined)holdHome=hold;},release(){holdHome=false;releaseHome?.();},calls,
 poll:pollHome,back:leaveTask,async submit(){task={...nextSubmit,status:'started'};await mutation('/api/submit',{taskId:task.taskId,itemId:task.step.itemId,responses:[]});}};
await home();window.ready=true;
</script></body></html>'''
html=html.replace('FIXTURE_HOME',json.dumps({**home_fixture,'studyGate':{'active':False,'kind':None,'activityIds':[],'taskIds':[]}}))

browser_code=r'''
const fs=require('fs'),assert=require('assert/strict');const fixture=FIXTURE_HOME,required=REQUIRED;
const {chromium}=require('/home/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const gate=(kind,activities)=>({active:true,kind,activityIds:activities.map(activity=>activity.activityId),taskIds:activities.map(activity=>activity.taskId)});
(async()=>{const browser=await chromium.launch({headless:true,executablePath:'/home/jake/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell',args:['--disable-dev-shm-usage']});try{
const page=await browser.newPage({viewport:{width:1200,height:1000}}),errors=[];page.on('pageerror',error=>errors.push(String(error)));page.setDefaultTimeout(10000);
await page.goto(ORIGIN+'/fixture');await page.waitForFunction(()=>window.ready);assert.equal(await page.locator('.queue-card').count(),5);
const retake={...required[0],taskId:99901,activityId:99902,type:'assessment',title:'Optional retake fixture',reason:'Optional retake',status:'unlocked'};
const completed={taskId:99903,activityId:99904,type:'assessment',title:'Completed quiz fixture',status:'completed',course:fixture.course,learner:fixture.learner,progress:{stepNumber:1,totalSteps:1},step:{itemId:99905,kind:'tutorial',markdown:'Assessment finished.',status:'completed',fields:[]},studyGate:gate('repairs',[])};
await page.evaluate(({home,submit})=>harness.configure({home,submit,hold:true}),{home:{...fixture,activities:[retake,...fixture.activities],studyGate:completed.studyGate},submit:completed});
await page.evaluate(()=>harness.submit());await page.evaluate(()=>{void harness.back();});await page.locator('.study-activities').waitFor();
assert.equal(await page.locator('.queue-card').count(),0);assert.equal(await page.getByText('Optional retake fixture',{exact:true}).count(),0);
const repairsHome={...fixture,activities:[retake,...fixture.activities],studyGate:gate('repairs',required)};
await page.evaluate(home=>harness.configure({home}),repairsHome);await page.evaluate(()=>harness.release());
await page.waitForFunction(()=>document.querySelectorAll('.queue-card').length===4);
assert.deepEqual(await page.locator('.queue-card h2').allTextContents(),required.map(activity=>activity.title));
assert.equal(await page.getByText('Optional retake fixture',{exact:true}).count(),0);
await page.evaluate(()=>harness.poll());assert.equal(await page.evaluate(()=>harness.calls.at(-1).path),'/api/home');
assert.deepEqual(await page.locator('.queue-card h2').allTextContents(),required.map(activity=>activity.title));
const quiz={...retake,title:'Required assessment fixture',reason:'Required assessment'};
await page.evaluate(home=>harness.configure({home}),{...repairsHome,activities:[...fixture.activities,quiz],studyGate:gate('assessment',[quiz])});await page.evaluate(()=>harness.poll());
assert.deepEqual(await page.locator('.queue-card h2').allTextContents(),['Required assessment fixture']);
await page.evaluate(home=>harness.configure({home}),{...fixture,activities:[retake,...fixture.activities.filter(activity=>activity.reason==='Continue your activity')],studyGate:{active:false,kind:null,activityIds:[],taskIds:[]}});await page.evaluate(()=>harness.poll());
assert.equal(await page.getByText('Optional retake fixture',{exact:true}).count(),1);assert.equal(await page.locator('.queue-card').count(),3);assert.deepEqual(errors,[]);
fs.writeFileSync(OUTPUT,JSON.stringify({passed:true,sourceFixture:fixture.provenance||'native captured home fixture',requiredCards:required.map(activity=>({taskId:activity.taskId,title:activity.title})),immediateCachedQueueHidden:true,readOnlyPollShowsOnlyRequiredReviews:true,requiredAssessmentExclusive:true,retakeOnlyAfterGateClears:true,javascriptErrors:errors},null,2));console.log(fs.readFileSync(OUTPUT,'utf8'));
}finally{await browser.close();}})().catch(error=>{console.error(error);process.exitCode=1;});
'''
with tempfile.TemporaryDirectory(prefix='study-gate-browser-') as tmp:
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
        def log_message(self,*args): pass
        def do_GET(self):
            if self.path=='/fixture':
                content=html.encode();self.send_response(200);self.send_header('Content-Type','text/html');self.send_header('Content-Length',str(len(content)));self.end_headers();self.wfile.write(content);return
            super().do_GET()
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
    output=Path(os.environ.get('STUDY_GATE_BROWSER_OUTPUT','/tmp/course-academy-queue-priority/browser-gate-verification.json'));output.parent.mkdir(parents=True,exist_ok=True)
    js=browser_code.replace('FIXTURE_HOME',json.dumps(home_fixture)).replace('REQUIRED',json.dumps(required)).replace('ORIGIN',json.dumps(f'http://127.0.0.1:{server.server_port}')).replace('OUTPUT',json.dumps(str(output)))
    script=Path(tmp)/'browser.cjs';script.write_text(js)
    try: subprocess.run(['/home/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node',str(script)],check=True,timeout=60)
    finally: server.shutdown()
