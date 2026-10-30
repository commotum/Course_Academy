"""Real study UI + generalized admission, replaying native projection fixtures.

The fixture is emitted by native study_interaction tests. Projection results and
answer keys are never authored in this browser test. No live learner or EDB writes.
"""
import copy
import http.server
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from serve_graph_explorer import handler

fixture = json.loads(Path(os.environ.get('STUDY_BROWSER_FIXTURE', '/tmp/study-browser-fixture.json')).read_text())
sequence = fixture['sequence']
assert sequence and sequence[0]['input']['action'] in {'queue', 'study-topic'}
source = (ROOT / 'ui/learning.js').read_text()
controllers = source[source.index('const $'):source.index("$('retryButton').addEventListener")]
html = '''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><script src="/ui/vendor/dompurify/purify.min.js"></script></head><body>
<main id="main"></main><div id="learnerName"></div><a id="courseLink"></a><div id="errorBanner" hidden><span id="errorText"></span><button id="retryButton">Retry</button></div><div id="announcement"></div>
<script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';import {decorateSourceTables} from '/ui/content-tables.js';import {decorateEquationGroups} from '/ui/equation-groups.js';import {protectMath} from '/ui/math-protection.js';import {romanLists} from '/ui/prose-lists.js';
import {loadMathInputs,inlinePrompt,mountInlineFields,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput,questionFeedback,feedbackHeading,responsesComplete} from '/ui/question-fields.js';
const isDeveloperMode=()=>false,attachStepMenu=()=>{},createStudySidebar=()=>document.createElement('aside');
''' + controllers + '''
typeset=async()=>{};loadMath=async()=>{};
async function syncAfterVisibility(){}
window.currentState=()=>({status:task?.status||'home',taskId:task?.taskId,itemId:task?.step?.itemId,contentId:task?.step?.contentId,stepStatus:task?.step?.status,busy});
const params=new URL(location.href).searchParams;
if(params.has('topicId'))await studyTopic(params.get('topicId'));
else if(params.has('taskId'))await openTask(params.get('taskId'));
else if(FIXTURE_STARTS_WITH_QUEUE)await home();
else {const page=el('section','study-activities');renderHome(FIXTURE_INITIAL,page,targetRevision);$('main').append(page);setBusy(false);}
window.ready=true;
</script></body></html>'''

html=html.replace('FIXTURE_STARTS_WITH_QUEUE',json.dumps(sequence[0]['input']['action']=='queue')).replace('FIXTURE_INITIAL',json.dumps(fixture.get('initial',{})))

released = threading.Event()
projected = []
write_started = []
write_finished = []
last_view = None

class Worker:
    def __init__(self, name): self.name = name
    def request(self, body):
        global last_view
        action = body['action']
        if action == 'study-project':
            expected = sequence[len(projected)]
            operation = body['operation']
            for key in ('action', 'activityId', 'taskId', 'itemId', 'responses'):
                if key in expected['input']:
                    assert operation.get(key) == expected['input'][key], (key, operation, expected['input'])
            data = copy.deepcopy(expected['data'])
            for key in ('requestId', 'submissionId', 'submittedAt'):
                if key in operation: data['operation'][key] = operation[key]
            projected.append(copy.deepcopy(operation))
            last_view = copy.deepcopy(data['view'])
            return {'ok': True, 'data': data}
        if action == 'persist-study':
            index = len(write_started)
            write_started.append(copy.deepcopy(body['operation']))
            released.wait()
            write_finished.append(copy.deepcopy(body['operation']))
            return {'ok': True, 'data': {'view': copy.deepcopy(sequence[index]['data']['view']), 'aliases': {}}}
        if action == 'task': return {'ok': True, 'data': copy.deepcopy(last_view)}
        if action == 'study-read':
            operation = body['operation']
            if operation['action'] == 'task': return {'ok': True, 'data': copy.deepcopy(last_view)}
            if operation['action'] in {'home', 'queue'}: return {'ok': True, 'data': copy.deepcopy(sequence[0]['data']['view'])}
        raise AssertionError(('Unexpected fixture worker request', self.name, body))
    def close(self): pass

browser_code = r'''
const fs=require('fs'),assert=require('assert/strict');
const sequence=FIXTURE_SEQUENCE;
const {chromium}=require('/home/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{const browser=await chromium.launch({headless:true,executablePath:'/home/jake/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell',args:['--disable-dev-shm-usage']});try{
const page=await browser.newPage({viewport:{width:1200,height:950}});const errors=[];page.on('pageerror',e=>{errors.push(String(e));console.error('Browser error:',String(e));});page.setDefaultTimeout(15000);
await page.goto(ORIGIN+'/fixture');await page.waitForFunction(()=>window.ready);
const timings=[];let reloadedAnswer=false;
for(const entry of sequence.slice(sequence[0].input.action==='queue'?1:0)){
 const operation=entry.input,expected=entry.data.view;
 if(operation.action==='answer')for(const response of operation.responses){
  const field=page.locator('.lesson-content:not([data-history]) [data-field-id="'+response.fieldId+'"]');
  if('choiceId' in response)await field.locator('input[value="'+response.choiceId+'"]:not([type="hidden"])').check();
  else if(await field.locator('math-field').count())await field.locator('math-field').evaluate((node,value)=>{node.value=value;node.dispatchEvent(new Event('input',{bubbles:true}));},response.value);
  else await field.locator('input,textarea').fill(response.value);
 }
 const before=Date.now();
 if(operation.action==='study-topic')await page.goto(ORIGIN+'/learn?topicId='+operation.topicId);
 else if(operation.action==='start')await page.locator('.queue-card').filter({has:page.getByText(expected.title,{exact:true})}).getByRole('button',{name:'Begin →',exact:true}).click();
 else if(operation.action==='continue')await page.getByRole('button',{name:/Next step →|Continue to next skill →/}).click();
 else if(operation.action==='answer')await page.getByRole('button',{name:'Check answer',exact:true}).click();
 else if(operation.action==='pause')await page.getByRole('button',{name:'Pause lesson working time',exact:true}).click();
 else if(operation.action==='resume')await page.getByRole('button',{name:'Resume lesson working time',exact:true}).click();
 else throw Error('Unsupported UI fixture action '+operation.action);
 await page.waitForFunction(expected=>{if(typeof currentState!=='function')return false;const state=currentState();return !state.busy&&state.taskId===expected.taskId&&state.itemId===expected.step?.itemId&&state.status===expected.status&&state.stepStatus===expected.step?.status;},expected);
 timings.push({operation:operation.action,ms:Date.now()-before});
 assert.equal(await page.locator('#errorBanner').isVisible(),false);
 if(operation.action==='answer'&&!reloadedAnswer){
  await page.reload();await page.waitForFunction(()=>window.ready);const restored=await page.evaluate(()=>currentState());
  assert.equal(restored.itemId,expected.step.itemId);assert.equal(restored.stepStatus,expected.step.status);reloadedAnswer=true;
 }
}
const final=sequence.at(-1).data.view;assert.equal((await page.evaluate(()=>currentState())).status,'completed');
const before=await(await page.request.get(ORIGIN+'/test/state')).json();assert.equal(before.pending,sequence.length);assert.equal(before.started,1);assert.equal(before.finished,0);assert.equal(before.released,false);
assert.equal(await page.locator('#reviewSaveStatus').isVisible(),false);
await page.screenshot({path:OUTPUT+'/study-before-background-save.png',fullPage:true});
await page.reload();await page.waitForFunction(()=>window.ready);assert.equal((await page.evaluate(()=>currentState())).status,final.status);
const reload=await(await page.request.get(ORIGIN+'/test/state')).json();assert.equal(reload.pending,sequence.length);assert.equal(reload.finished,0);
await page.request.get(ORIGIN+'/test/release');let after;for(let n=0;n<300;n++){after=await(await page.request.get(ORIGIN+'/test/state')).json();if(after.pending===0)break;await new Promise(resolve=>setTimeout(resolve,50));}
assert.equal(after.pending,0);assert.equal(after.finished,sequence.length);assert.deepEqual(after.actions,sequence.map(entry=>entry.input.action));assert.deepEqual(errors,[]);
const result={passed:true,fixtureProvenance:PROVENANCE,nativeProjectionResultsReplayed:true,timings,completionBeforeAnyDatabaseSave:true,reloadRetainedQueuedActions:true,reloadRetainedGradedAnswer:reloadedAnswer,orderedWrites:after.actions,javascriptErrors:errors};fs.writeFileSync(OUTPUT+'/browser-verification.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
'''

with tempfile.TemporaryDirectory(prefix='study-ui-test-') as tmp:
    env = {'LEARNING_REQUEST_DIR': tmp, 'EDB_ENDPOINT': '/unused', 'COURSE_ACADEMY_DISABLE_GENERATION': '1'}
    with patch('serve_graph_explorer.InventoryJobs'), patch('serve_graph_explorer.NativeWorker', side_effect=lambda command, environment, name: Worker(name)):
        base = handler(Path('/unused'), 'fixture', 'learner', env, Path('/unused'))
    outbox = next(fn.__self__ for fn in base.background if fn.__name__ == 'loop')
    class Handler(base):
        def log_message(self, *args): pass
        def do_GET(self):
            if self.path == '/fixture' or self.path.startswith('/learn?'):
                self.send_bytes(200, html.encode(), 'text/html'); return
            if self.path == '/test/release':
                released.set(); self.send_bytes(200, b'{}', 'application/json'); return
            if self.path == '/test/state':
                state=outbox.status()
                self.send_bytes(200, json.dumps({'pending':state['pending'],'started':len(write_started),'finished':len(write_finished),'released':released.is_set(),'actions':[operation['action'] for operation in write_finished]}).encode(),'application/json');return
            super().do_GET()
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    threading.Thread(target=outbox.loop,daemon=True).start()
    output=Path(os.environ.get('STUDY_BROWSER_OUTPUT', str(ROOT/'reference/edb-math/repairs/2026-10-30-study-responsiveness')))
    output.mkdir(parents=True,exist_ok=True)
    js=browser_code.replace('ORIGIN',json.dumps(f'http://127.0.0.1:{server.server_port}')).replace('FIXTURE_SEQUENCE',json.dumps(sequence)).replace('PROVENANCE',json.dumps(fixture.get('provenance','retrieval_tests::study_projection_lesson_backlog_replays_exact_route_and_logical_clocks'))).replace('OUTPUT',json.dumps(str(output)))
    script=Path(tmp)/'browser.cjs';script.write_text(js)
    try:
        result=subprocess.run(['/home/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node',str(script)],text=True,timeout=90)
        if result.returncode: raise SystemExit(result.returncode)
    finally:
        released.set();base.scheduler_stop.set();server.shutdown()
