"""Actual-player dropdown sizing, pointer, keyboard, and resize checks; no API writes."""
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
import {richSelect} from '/ui/question-fields.js';
window.showDropdown=async field=>{
  MathJax.typesetClear([content]);content.replaceChildren();content.className='content-card';
  const prompt=document.createElement('div');prompt.className='prose';
  prompt.append(render('For any linear differential operator $L$, we have the linearity condition.'));
  const row=document.createElement('div');row.className='question-equation';
  const select=document.createElement('select');select.setAttribute('aria-label','Proof step');
  const empty=document.createElement('option');empty.value='';select.append(empty);
  for(const a of field.choices){const option=document.createElement('option');option.value=a.id;option.textContent=a.value;select.append(option);}
  const make=a=>render(a.type==='math'?'$'+a.value+'$':a.value);
  const control=richSelect(select,field.choices,make,a=>a.id,host=>MathJax.typesetPromise([host]));
  select.addEventListener('change',()=>{window.changeCount=(window.changeCount||0)+1;});window.changeCount=0;
  row.append(control);prompt.append(row);content.append(prompt);await MathJax.typesetPromise([content]);
};window.dropdownReady=true;</script>'''


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


questions = json.loads((H / 'questions-before.json').read_text())
fields = []
for q in questions:
    for f in q.get(':question/answer-fields', []):
        if f[':answer-field/type'][':db/ident'] == ':answer-field.type/select':
            fields.append(dict(question=q[':db/id'], id=f[':db/id'], choices=[dict(
                id=str(a[':db/id']), type=a[':answer/type'][':db/ident'].split('/')[-1],
                value=a[':answer/value']) for a in f[':answer-field/choices']]))

server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
origin = f'http://127.0.0.1:{server.server_port}'
checks = []
(H / 'visual').mkdir(exist_ok=True)
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.route('**/*', lambda r: r.fulfill(body=fixture, content_type='text/html')
                   if r.request.url == origin + '/fixture' else r.continue_()
                   if r.request.url.startswith(origin + '/') else r.abort())
        page.goto(origin + '/fixture')
        page.wait_for_function('window.ready&&window.dropdownReady')
        for width in [1100, 708, 390]:
            page.set_viewport_size(dict(width=width, height=1000))
            for field in fields:
                page.evaluate('showDropdown', field)
                trigger = page.locator('.answer-select-trigger')
                menu = page.locator('.answer-select-menu')
                trigger.click()
                page.wait_for_function('!document.querySelector(".answer-select-menu[hidden]")&&document.querySelector(".answer-select-menu mjx-container")||document.querySelector(".answer-select-menu").textContent.includes("linear")')
                page.wait_for_timeout(40)
                result = menu.evaluate('''n=>{const r=n.getBoundingClientRect();return {
                  left:r.left,right:r.right,width:r.width,viewport:document.documentElement.clientWidth,
                  horizontal_overflow:n.scrollWidth>n.clientWidth+1,
                  math_errors:n.querySelectorAll('[data-mml-node="merror"]').length,
                  clipped_math:[...n.querySelectorAll('svg')].filter(s=>{
                    const a=s.getBoundingClientRect(),b=s.closest('button').getBoundingClientRect();
                    return a.right>b.right+1||a.left<b.left-1;
                  }).length};}''')
                assert result['left'] >= 15 and result['right'] <= width - 15, result
                assert not result['horizontal_overflow'] and not result['math_errors'] and not result['clipped_math'], result
                # Clicking popup padding must not close it through focusout(null).
                box = menu.bounding_box()
                page.mouse.click(box['x'] + 2, box['y'] + 2)
                assert menu.is_visible()
                page.locator('.answer-select-option').first.click()
                assert not menu.is_visible()
                assert page.locator('select').input_value() == field['choices'][0]['id']
                assert page.evaluate('changeCount') == 1
                page.wait_for_timeout(35)
                selected = trigger.evaluate('''n=>{const r=n.getBoundingClientRect();return {
                  overflow:n.scrollWidth>n.clientWidth+1,
                  clipped:[...n.querySelectorAll('svg')].some(s=>s.getBoundingClientRect().right>r.right+1)
                };}''')
                assert not selected['overflow'] and not selected['clipped'], selected
                trigger.click()
                assert menu.is_visible()
                reopened = menu.bounding_box()
                assert reopened['x'] >= 15 and reopened['x'] + reopened['width'] <= width - 15, reopened
                page.keyboard.press('Escape')
                assert not menu.is_visible()
                checks.append(dict(question=field['question'], field=field['id'], selected=selected, **result))
                if field['question'] == 17592186311880 and field['id'] == 17592186311440:
                    trigger.click()
                    menu.screenshot(path=str(H / 'visual' / f'dropdown-{width}.png'))
                    page.keyboard.press('Escape')
            print(f'Checked {len(fields)} dropdowns at {width}px.', flush=True)
        browser.close()
finally:
    server.shutdown()
    server.server_close()
(H / 'dropdown-verification.json').write_text(json.dumps(dict(passed=True, database_writes=0,
    checks=checks, popup_padding_click_keeps_open=True, keyboard_escape_and_choice_ids_preserved=True), indent=2) + '\n')
print('All dropdown checks passed.', flush=True)
