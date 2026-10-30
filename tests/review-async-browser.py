"""Actual review UI + HTTP admission/outbox, with blocked persistence. No live EDB writes.
Native read-only cards/grades and stopping decisions come from the isolated Rust fixture.
"""
import copy
import fcntl
import http.server
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from serve_graph_explorer import handler
from review_outbox import ReviewOutbox

fixture = json.loads(Path('/tmp/review-browser-fixture.json').read_text())
source = (ROOT / 'ui/learning.js').read_text()
controllers = source[source.index('const $'):source.index("$('retryButton').addEventListener")]
# Keep the real renderer/controls; asynchronous correctness comes from the native
# fixture, while this test focuses on interaction latency rather than MathJax.
html = '''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><script src="/ui/vendor/dompurify/purify.min.js"></script></head><body>
<main id="main"></main><div id="learnerName"></div><a id="courseLink"></a><div id="errorBanner" hidden><span id="errorText"></span><button id="retryButton">Retry</button></div><div id="announcement"></div>
<script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {decorateEquationGroups} from '/ui/equation-groups.js';import {decorateSourceTables} from '/ui/content-tables.js';import {protectMath} from '/ui/math-protection.js';import {romanLists} from '/ui/prose-lists.js';
import {loadMathInputs,inlinePrompt,mountInlineFields,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput,questionFeedback,feedbackHeading,responsesComplete} from '/ui/question-fields.js';
const isDeveloperMode=()=>false,attachStepMenu=()=>{},createStudySidebar=()=>document.createElement('aside');
''' + controllers + '''
typeset=async()=>{};loadMath=async()=>{};
async function syncAfterVisibility(){}
task=await api('/api/task?taskId=TASK');await renderTask(task);setBusy(false);window.ready=true;
window.currentState=()=>({status:task.status,itemId:task.step.itemId,contentId:task.step.contentId,busy});
</script></body></html>'''.replace('TASK', str(fixture['session']['view']['taskId']))

released = threading.Event()
writer_entered = threading.Event()
writes = []

class Worker:
    def __init__(self, name): self.name = name
    def request(self, body):
        action = body['action']
        if self.name == 'feedback-worker':
            if action == 'review-session': return {'ok': True, 'data': copy.deepcopy(fixture['session'])}
            if action == 'review-grade':
                q = body['questionId']
                correct = next(a for a in fixture['answers'] if a['questionId'] == q)['choiceId']
                result = 'correct' if body['responses'][0]['choiceId'] == correct else 'incorrect'
                return {'ok': True, 'data': copy.deepcopy(fixture['feedback'][str(q)][result])}
            if action == 'review-decision':
                return {'ok': True, 'data': copy.deepcopy(fixture['decisions'][len(body['outcomes'])-1])}
        if self.name == 'review-save-worker':
            writes.append(copy.deepcopy(body));writer_entered.set();released.wait(30)
            return {'ok': True, 'data': {}}
        if action == 'task': return {'ok': True, 'data': copy.deepcopy(fixture['session']['view'])}
        return {'ok': True, 'data': {}}
    def close(self): pass

browser_code = r'''
const fs=require('fs'),assert=require('assert/strict');
const {chromium}=require('/home/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{const browser=await chromium.launch({headless:true,executablePath:'/home/jake/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell',args:['--disable-dev-shm-usage']});try{
const page=await browser.newPage({viewport:{width:1200,height:950}});const errors=[];page.on('pageerror',e=>{errors.push(String(e));console.error('Browser error:',String(e));});page.setDefaultTimeout(15000);
await page.goto(ORIGIN+'/fixture');await page.waitForFunction(()=>window.ready);
await page.request.get(ORIGIN+'/test/hold');
const timings=[];
for(let n=0;n<3;n++){
 const state=await page.evaluate(()=>currentState());const answer=ANSWERS.find(a=>a.questionId===state.contentId);
 await page.locator('.lesson-content:not([data-history]) label.choice').filter({has:page.locator('input[value="'+answer.choiceId+'"]')}).click();
 let t=Date.now();await page.getByRole('button',{name:'Check answer',exact:true}).click();
 await page.waitForFunction(()=>!currentState().busy&&document.querySelector('.lesson-content:not([data-history]) .feedback-badge')?.textContent==='Correct');
 timings.push({operation:'answer',ms:Date.now()-t});
 t=Date.now();await page.getByRole('button',{name:'Next step →',exact:true}).click();
 await page.waitForFunction(old=>!currentState().busy&&(currentState().itemId!==old||currentState().status==='completed'),state.itemId);
 timings.push({operation:'continue',ms:Date.now()-t});
}
assert.equal((await page.evaluate(()=>currentState())).status,'completed');
const before=await (await page.request.get(ORIGIN+'/test/state')).json();assert.equal(before.writes,1);assert.equal(before.pending,6);assert.equal(before.released,false);
assert.equal(await page.locator('#reviewSaveStatus').isVisible(),false);
await page.screenshot({path:OUTPUT+'/review-before-background-save.png',fullPage:true});
await page.reload();await page.waitForFunction(()=>window.ready);assert.equal((await page.evaluate(()=>currentState())).status,'completed');
const reloadState=await (await page.request.get(ORIGIN+'/test/state')).json();assert.equal(reloadState.pending,6);assert.equal(reloadState.writes,1);
await page.request.get(ORIGIN+'/test/release');
let after;for(let n=0;n<300;n++){after=await(await page.request.get(ORIGIN+'/test/state')).json();if(after.pending===0)break;await new Promise(resolve=>setTimeout(resolve,50));}
assert.equal(after.pending,0);assert.equal(after.writes,6);
assert.deepEqual(after.actions,['answer','continue','answer','continue','answer','continue']);assert.deepEqual(errors,[]);
const result={passed:true,timings,completionBeforeAnyDatabaseSave:true,reloadRetainedQueuedAnswers:true,orderedWrites:after.actions,javascriptErrors:errors};fs.writeFileSync(OUTPUT+'/browser-verification.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
'''

# Keep this fixture on the old replay protocol to cover journals accepted before
# the generalized study outbox upgrade. New study interactions have a separate
# native-projection browser regression.
class LegacyReviewFixture(ReviewOutbox):
    def __init__(self, *args, learner=None, planner=None, publication=None, **kwargs):
        # This isolated journal contains one native fixture learner; the HTTP
        # handler uses a dummy learner name rather than a live profile identity.
        super().__init__(*args, **kwargs)
    def overlay_view(self, action, body):
        return self.task_view(body['taskId']) if action == 'task' else None
    def resolve_ids(self, body): return body
    def decorate(self, view): return view

with tempfile.TemporaryDirectory(prefix='review-ui-test-') as tmp:
    env = {'LEARNING_REQUEST_DIR': tmp, 'EDB_ENDPOINT': '/unused', 'COURSE_ACADEMY_DISABLE_GENERATION': '1'}
    with patch('serve_graph_explorer.CompatibleStudyOutbox', LegacyReviewFixture), patch('serve_graph_explorer.InventoryJobs'), patch('serve_graph_explorer.NativeWorker', side_effect=lambda command, environment, name: Worker(name)):
        base = handler(Path('/unused'), 'fixture', 'learner', env, Path('/unused'))
    outbox = next(fn.__self__ for fn in base.background if fn.__name__ == 'loop')
    class Handler(base):
        held = None
        def log_message(self, *args): pass
        def do_GET(self):
            if self.path == '/fixture' or self.path.startswith('/learn?taskId='): self.send_bytes(200,html.encode(),'text/html');return
            if self.path == '/test/hold':
                Handler.held = (Path(tmp)/'api.lock').open('a');fcntl.flock(Handler.held,fcntl.LOCK_EX)
                self.send_bytes(200,b'{}','application/json');return
            if self.path == '/test/release':
                if Handler.held: Handler.held.close();Handler.held=None
                released.set();self.send_bytes(200,b'{}','application/json');return
            if self.path == '/test/state':
                state=outbox.status(fixture['session']['view']['taskId'])
                self.send_bytes(200,json.dumps({'pending':state['pending'],'writes':len(writes),'released':released.is_set(),'actions':[w['operation']['action'] for w in writes]}).encode(),'application/json');return
            super().do_GET()
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    threading.Thread(target=outbox.loop,daemon=True).start()
    output=ROOT/'reference/edb-math/repairs/2026-10-28-review-feedback-latency';output.mkdir(parents=True,exist_ok=True)
    js=browser_code.replace('ORIGIN',json.dumps(f'http://127.0.0.1:{server.server_port}')).replace('ANSWERS',json.dumps(fixture['answers'])).replace('OUTPUT',json.dumps(str(output)))
    script=Path(tmp)/'browser.cjs';script.write_text(js)
    try:
        result=subprocess.run(['/home/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node',str(script)],text=True,timeout=90)
        if result.returncode: raise SystemExit(result.returncode)
    finally:
        released.set()
        if Handler.held: Handler.held.close()
        base.scheduler_stop.set();server.shutdown()
