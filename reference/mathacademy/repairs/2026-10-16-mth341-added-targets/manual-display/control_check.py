"""Read-only actual-answer-control checks for the targeted display repairs."""
import functools
import http.server
import json
import re
import sys
import threading
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
AUDIT = ROOT / 'reference/mathacademy/audits/2026-10-16-mth341-added-targets'
PRIOR = ROOT / 'reference/mathacademy/audits/2026-10-16-mth341'
OUT = HERE / 'controls'
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads

types = {r[0][':db/id']: r[0][':db/ident'] for r in loads((PRIOR / 'types.edn').read_text())}
entities = json.loads((AUDIT / 'entities.json').read_text())
manual = json.loads((HERE / 'changes.json').read_text())
expected = json.loads((AUDIT / 'fields.json').read_text())
patches = {(c['entity'],c['attribute']):c['after'] for c in manual}
expected = [dict(c,value=patches.get((c['entity'],c['attribute']),c['normalized'])) for c in expected]
matrix_ids = set()
selected_ids = {c['entity'] for c in expected if 17592186049869 in c['topics'] and '{{field-' in c['value']}

cases = []
for item in expected:
    if item['entity'] not in selected_ids or item['attribute'] != ':question/problem':
        continue
    fields = []
    for field in entities[str(item['entity'])][':question/answer-fields']:
        choices = [{'id': a[':db/id'], 'type': a[':answer/type'][':db/ident'], 'value': a[':answer/value']} for a in field.get(':answer-field/choices', [])]
        correct = next((a for a in choices if a['id'] == field.get(':answer-field/correct', {}).get(':db/id')), None)
        fields.append({'id': field[':db/id'], 'key': field[':answer-field/key'], 'type': types[field[':answer-field/type'][':db/id']], 'choices': choices, 'correctAnswer': correct, 'answerType': correct['type'] if correct else None})
    cases.append({'entity': item['entity'], 'problem': item['value'], 'fields': fields, 'matrix': item['entity'] in matrix_ids, 'placeholderKeys': re.findall(r'\{\{(?:answer-field:)?([^}]+)\}\}', item['value'])})
assert len(cases) == 10

learning = (ROOT / 'ui/learning.js').read_text()
renderers = learning[learning.index('function markdown('):learning.index('function loadMath(')] + learning[learning.index('function choiceOrder('):learning.index('function collectResponses(')] + learning[learning.index('function fieldLabel('):learning.index('function announce(')]
html = r'''<!doctype html><html data-theme="light"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="connect-src 'none'"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><body><main class="lesson-main" id="main"></main><script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js'; import {romanLists} from '/ui/prose-lists.js';
import {inlinePrompt,loadMathInputs,mountInlineFields,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput} from '/ui/question-fields.js';
const el=(tag,className='',text='')=>{const n=document.createElement(tag);n.className=className;n.textContent=text;return n;};
const short=x=>String(x||'').split('/').at(-1),typeset=()=>{};
const assetURL=x=>'/api/asset?path='+encodeURIComponent(x);
const escapeHTML=text=>String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
__RENDERERS__
await loadMathInputs(); await MathJax.startup.promise;
window.renderCase=async data=>{
 MathJax.typesetClear([main]); main.replaceChildren();
 const article=el('article','content-card'), fields=structuredClone(data.fields);
 article.dataset.entity=data.entity; main.append(article);
 const prompt=markdown(data.problem,'prose',fields),rest=el('div','answer-fields'); article.append(prompt,rest);
 mountInlineFields(prompt,rest,fields,f=>fieldControl(f,false,data.entity,data.problem,''));
 await MathJax.typesetPromise([main]);
 await Promise.all([...article.querySelectorAll('img')].map(i=>{i.loading='eager';return i.decode().catch(()=>{});}));
 await document.fonts.ready; await new Promise(requestAnimationFrame);
 const controls=[...article.querySelectorAll('[data-answer-input="true"]')];
 const initial=controls.map(n=>{const r=n.getBoundingClientRect();return {id:Number(n.getAttribute('name')),key:n.closest('[data-field-key]')?.dataset.fieldKey,label:n.getAttribute('aria-label'),tag:n.localName,width:r.width,height:r.height,left:r.left,right:r.right,visible:getComputedStyle(n).display!=='none'&&getComputedStyle(n).visibility!=='hidden',enabled:!n.disabled,tabIndex:n.tabIndex};});
 let access=[];
 for(const n of controls){
   n.scrollIntoView({block:'center',inline:'nearest'}); n.focus(); await new Promise(requestAnimationFrame);
   const r=n.getBoundingClientRect(),x=(r.left+r.right)/2,y=(r.top+r.bottom)/2,hit=document.elementFromPoint(x,y);
   access.push({id:Number(n.getAttribute('name')),focused:document.activeElement===n||n.matches(':focus-within')||Boolean(n.hasFocus?.()),activeTag:document.activeElement?.localName,activeClass:document.activeElement?.className,mathFocus:n.hasFocus?.(),centerInViewport:x>=0&&x<innerWidth&&y>=0&&y<innerHeight,pointerReachable:hit===n||n.contains(hit),rect:{left:r.left,right:r.right,top:r.top,bottom:r.bottom}});
   n.blur();
 }
 window.scrollTo(0,0); await new Promise(requestAnimationFrame);
 const plain=prompt.cloneNode(true);plain.querySelectorAll('mjx-container,pre,code,math-field').forEach(n=>n.remove());
 return {entity:data.entity,expectedFields:fields.length,expectedKeys:fields.map(f=>f.key).sort(),expectedIds:fields.map(f=>f.id).sort(),placeholderKeys:data.placeholderKeys,controls:initial,access,
  actualKeys:initial.map(x=>x.key).sort(),actualIds:initial.map(x=>x.id).sort(),matrix:data.matrix,tableControls:prompt.querySelectorAll('.matrix-answer td [data-answer-input="true"]').length,
  detachedControls:rest.querySelectorAll('[data-answer-input="true"]').length,remainingPlaceholders:[...prompt.querySelectorAll('[data-field-key]')].filter(n=>!n.querySelector('[data-answer-input="true"]')).map(n=>n.dataset.fieldKey),
  contentOverflow:prompt.scrollWidth>prompt.clientWidth+1,articleOverflow:article.scrollWidth>article.clientWidth+1,pageOverflow:document.documentElement.scrollWidth>innerWidth+1,
  mathErrors:[...article.querySelectorAll('[data-mjx-error],mjx-merror,[data-mml-node="mtext"][fill="red"]')].map(n=>n.outerHTML),
  codeBlocks:[...article.querySelectorAll('pre')].map(n=>n.textContent),rawTex:/\$|\\(?:begin|end|left|right|text|frac)\b/.test(plain.textContent)?plain.textContent:null};
};window.ready=true;
</script>'''.replace('__RENDERERS__', renderers)
(OUT / 'fixture.html').write_text(html)
(OUT / 'cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=2) + '\n')


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def translate_path(self, path):
        if path.startswith('/api/asset?'):
            return str(Path('/media/jake/SSD/EDB/math') / parse_qs(urlparse(path).query)['path'][0])
        return super().translate_path(path)


server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
origin = f'http://127.0.0.1:{server.server_port}'
report = []
errors = []
requests = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome')
        page = browser.new_page(viewport={'width': 893, 'height': 900})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('request', lambda request: requests.append({'url': request.url, 'method': request.method}))
        page.route('**/*', lambda route: route.fulfill(body=html, content_type='text/html') if route.request.url == origin + '/fixture' else route.continue_() if route.request.url.startswith(origin + '/') and route.request.method == 'GET' else route.abort())
        page.goto(origin + '/fixture')
        page.wait_for_function('window.ready===true', timeout=20000)
        for width in (893, 375):
            page.set_viewport_size({'width': width, 'height': 900})
            for case in cases:
                result = page.evaluate('data=>renderCase(data)', case)
                result['viewportWidth'] = width
                report.append(result)
                page.screenshot(path=str(OUT / f'{case["entity"]}-{width}.png'), full_page=True)
        browser.close()
finally:
    server.shutdown()
    server.server_close()

issues = []
for item in report:
    problems = []
    for key in ('contentOverflow', 'articleOverflow', 'pageOverflow', 'mathErrors', 'codeBlocks', 'rawTex', 'remainingPlaceholders', 'detachedControls'):
        if item[key]:
            problems.append({key: item[key]})
    if item['expectedKeys'] != item['actualKeys'] or item['expectedIds'] != item['actualIds']:
        problems.append({'fieldMapping': 'Keys or IDs differ'})
    if item['matrix'] and item['tableControls'] != item['expectedFields']:
        problems.append({'tableControls': item['tableControls']})
    for control in item['controls']:
        if not control['visible'] or not control['enabled'] or control['tabIndex'] < 0 or not control['label'] or control['width'] < 1 or control['height'] < 1:
            problems.append({'control': control})
    for control in item['access']:
        if not all(control[k] for k in ('focused', 'centerInViewport', 'pointerReachable')):
            problems.append({'access': control})
    if problems:
        issues.append({'entity': item['entity'], 'viewportWidth': item['viewportWidth'], 'issues': problems})
summary = {'cases': len(cases), 'viewportWidths': [893, 375], 'questionViewportChecks': len(report), 'controlsChecked': sum(len(r['controls']) for r in report), 'pageErrors': errors, 'requestsOtherThanGet': [r for r in requests if r['method'] != 'GET'], 'issues': issues}
(OUT / 'measurements.json').write_text(json.dumps(report, indent=2) + '\n')
(OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({**summary, 'issues': [{'entity': i['entity'], 'viewportWidth': i['viewportWidth'], 'issueKinds': [list(x) for x in i['issues']]} for i in issues]}, indent=2))
