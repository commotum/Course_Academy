#!/usr/bin/env python3
"""Headless editor regression test; no screenshots, APIs, or learner writes.
Run with a Python environment containing Playwright and its Chromium browser.
"""
import threading, functools, http.server
from pathlib import Path
from playwright.sync_api import sync_playwright
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(Path(__file__).resolve().parents[1])))
threading.Thread(target=server.serve_forever,daemon=True).start()
origin=f'http://127.0.0.1:{server.server_port}'
html='''<!doctype html><link rel="stylesheet" href="/ui/learning.css"><form id="form"><span id="host"></span><button id="check" type="submit" disabled>Check answer</button></form><script type="module">
import { blankInput, responsesComplete } from '/ui/question-fields.js';
window.events=[]; window.submissions=[]; window.busy=false;
form.addEventListener('input', e => events.push([e.target.tagName,e.target.value]));
window.makeBlank=blankInput;
window.editor=blankInput({answerType:'math'},'Derivative','field-1');
host.append(editor);
const refresh=()=>{check.disabled=busy || !responsesComplete([{type:'blank',answerType:'math'}],[{value:editor.value}]);};
form.addEventListener('input',refresh);
form.addEventListener('submit', e => {
  e.preventDefault(); refresh(); if (!check.disabled) submissions.push(editor.value);
});
window.ready=true;
</script>'''
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  page=browser.new_page();errors=[];page.on('pageerror',lambda e:(errors.append(str(e)),print('PAGE ERROR:',e,flush=True)))
  page.route('**/*',lambda route: route.fulfill(body=html,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort())
  page.goto(origin+'/fixture');page.wait_for_function('window.ready === true',timeout=5000)
  assert page.evaluate('editor.value')==''
  assert page.evaluate('editor.placeholder')==''
  assert page.evaluate("getComputedStyle(editor.shadowRoot.querySelector('[part~=virtual-keyboard-toggle]')).display")== 'none'
  page.locator('math-field').focus();page.keyboard.press('Enter');
  assert page.evaluate('submissions.length')==0
  page.keyboard.type('11/');page.keyboard.press('Enter')
  assert page.evaluate('submissions.length')==0 # unfinished fraction
  page.keyboard.type('4x')
  result=page.evaluate('({value:editor.value,events,parts:!!editor.shadowRoot,fonts:document.fonts.status})')
  assert result['value']==r'\frac{11}{4x}',result
  assert result['events'] and result['events'][-1][0]=='MATH-FIELD',result
  page.keyboard.press('Enter')
  assert page.evaluate('submissions')==[r'\frac{11}{4x}']
  page.locator('math-field').dispatch_event('keydown', {'key':'Enter','repeat':True})
  page.keyboard.press('Shift+Enter')
  assert page.evaluate('submissions.length')==1
  page.evaluate("editor.value=''; events=[]")
  page.keyboard.type('-7/3x')
  assert page.evaluate('editor.value')==r'-\frac{7}{3x}'
  page.keyboard.press('Enter')
  assert page.evaluate('submissions')==[r'\frac{11}{4x}',r'-\frac{7}{3x}']
  page.evaluate('busy=true;check.disabled=true');page.keyboard.press('Enter')
  assert page.evaluate('submissions.length')==2
  page.evaluate('editor.disabled=true');before=page.evaluate('editor.value');page.keyboard.type('9')
  assert page.evaluate('editor.value')==before
  page.evaluate('''
    window.textForm=document.createElement('form');
    window.text=makeBlank({answerType:'text'},'Text answer','text');
    window.textSubmit=document.createElement('button');textSubmit.type='submit';
    textForm.append(text,textSubmit);document.body.append(textForm);
    textForm.addEventListener('submit',e=>{e.preventDefault();submissions.push(text.value)});
  ''' )
  page.locator('input').focus();page.keyboard.type('typed answer');page.keyboard.press('Enter')
  assert page.evaluate('submissions.at(-1)')=='typed answer'
  assert not errors,errors
  print('Math blanks: typing, Enter submission, incomplete and busy guards, text blanks, and disabled state pass; no screenshots.')
  browser.close()
finally:server.shutdown();server.server_close()
