"""Verify the repaired proof rows with real player controls, without study writes."""
import functools
import http.server
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
fixture = (ROOT / 'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
fixture = fixture.replace('<!doctype html>', '<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
fixture += '''<script type="module">
import {mountInlineFields,richSelect,checkboxControl,choiceIndicator,fieldFeedback,blankInput,freeInput} from '/ui/question-fields.js';
const source=await(await fetch('/ui/learning.js')).text();
const functionText=(name,next)=>source.slice(source.indexOf('function '+name+'('),source.indexOf('function '+next+'('));
const code=functionText('fieldControl','collectResponses');
const short=v=>String(v||'').split('/').at(-1), studyChoiceId=id=>id;
const el=(tag,cls='',text)=>{const n=document.createElement(tag);n.className=cls;if(text!==undefined)n.textContent=text;return n;};
const fieldLabel=key=>'Answer '+key.replace('field-','');
const choiceOrder=(choices)=>choices;
const answerValue=a=>render(a.type==='math'?'$'+a.value+'$':a.value);
const typeset=host=>MathJax.typesetPromise([host]);
window.realControl=new Function('el','short','fieldLabel','choiceOrder','studyChoiceId','markdown','answerValue','typeset',
 'richSelect','checkboxControl','choiceIndicator','fieldFeedback','blankInput','freeInput',code+';return fieldControl;')
 (el,short,fieldLabel,choiceOrder,studyChoiceId,render,answerValue,typeset,richSelect,checkboxControl,choiceIndicator,fieldFeedback,blankInput,freeInput);
window.showQuestion=async item=>{
 MathJax.typesetClear([content]);content.replaceChildren();
 const card=el('article','lesson-content content-card');card.dataset.question=item.entity;
 const form=el('form'),prompt=render(item.problem,'prose',item.fields),list=el('div','answer-fields');
 mountInlineFields(prompt,list,item.fields,f=>realControl(f,false,item.entity,item.problem,''));
 form.append(prompt,list);card.append(form);content.append(card);await MathJax.typesetPromise([content]);
 return{controls:prompt.querySelectorAll('.answer-inline').length,expected:item.fields.length,
  trailing:list.childElementCount,hidden:list.hidden,math_errors:content.querySelectorAll('[data-mml-node="merror"]').length,
  ghost_blanks:content.querySelectorAll('[data-mml-node="mphantom"]').length,
  missing_slots:item.fields.filter(f=>!prompt.querySelector('[data-field-key="'+f.key+'"]')).map(f=>f.key),
  misplaced_terms:item.fields.filter(f=>['field-2','field-3','field-4'].includes(f.key)&&!prompt.querySelector('[data-field-key="'+f.key+'"]')?.closest('.question-equation')).map(f=>f.key),
  outer_overflow:card.scrollWidth>card.clientWidth+1};
};window.inlineReady=true;</script>'''


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


items = []
for q in json.loads((H / 'questions-after.json').read_text()):
    fs = q.get(':question/answer-fields', [])
    if any(f[':answer-field/type'][':db/ident'] == ':answer-field.type/select' for f in fs):
        items.append(dict(entity=q[':db/id'], problem=q[':question/problem'], fields=[dict(
            id=str(f[':db/id']), key=f[':answer-field/key'], type='select',
            choices=[dict(id=str(a[':db/id']), type=a[':answer/type'][':db/ident'].split('/')[-1], value=a[':answer/value'])
                     for a in f[':answer-field/choices']]) for f in fs]))
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
origin = f'http://127.0.0.1:{server.server_port}'
checks = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.route('**/*', lambda r: r.fulfill(body=fixture, content_type='text/html')
                   if r.request.url == origin + '/fixture' else r.continue_()
                   if r.request.url.startswith(origin + '/') else r.abort())
        page.goto(origin + '/fixture')
        page.wait_for_function('window.ready&&window.inlineReady')
        for width in [1100, 708, 390]:
            page.set_viewport_size(dict(width=width, height=1000))
            for item in items:
                result = page.evaluate('showQuestion', item)
                assert result['controls'] == result['expected'] and result['hidden'] and not result['trailing'], result
                assert not any(result[k] for k in ['math_errors', 'ghost_blanks', 'missing_slots', 'misplaced_terms', 'outer_overflow']), result
                for trigger in page.locator('.answer-select-trigger').all():
                    trigger.click()
                    page.wait_for_timeout(35)
                    popup = page.locator('.answer-select-menu:not([hidden])')
                    metrics = popup.evaluate('''n=>{const r=n.getBoundingClientRect();return{left:r.left,right:r.right,overflow:n.scrollWidth>n.clientWidth+1};}''')
                    assert metrics['left'] >= 15 and metrics['right'] <= width - 15 and not metrics['overflow'], metrics
                    page.keyboard.press('Escape')
                checks.append(dict(question=item['entity'], width=width, **result))
                if item['entity'] == 17592186311880:
                    page.locator('.content-card').screenshot(path=str(H / 'visual' / f'inline-proof-{width}.png'))
            print(f'Checked all proof placements at {width}px.', flush=True)
        browser.close()
finally:
    server.shutdown()
    server.server_close()
(H / 'inline-verification.json').write_text(json.dumps(dict(passed=True, database_writes=0, checks=checks), indent=2) + '\n')
print('Inline placement checks passed.')
