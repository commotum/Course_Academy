"""Render a complete lesson Pull and optional generator samples with the app's renderer.

Run using a Python environment with Playwright and Chromium:
  python verify_rendering.py expected.edn /tmp/matrix-lesson-repair/generated.json
"""
import functools
import http.server
import json
import sys
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads

HERE = Path(__file__).resolve().parent / 'pending-database-wide/refreshed-validation'
HERE.mkdir(exist_ok=True)
records, seen = [], set()

def collect(node):
    if isinstance(node, list):
        for child in node:
            collect(child)
    elif isinstance(node, dict):
        eid = node.get(':db/id')
        if eid and eid not in seen:
            seen.add(eid)
            for attr in (':tutorial/content', ':question/problem', ':question/worked-solution', ':answer/value', ':answer/feedback'):
                if attr in node:
                    value = node[attr]
                    if attr == ':answer/value' and node.get(':answer/type', {}).get(':db/ident') == ':answer.type/math':
                        value = '$' + value + '$'
                    records.append({'id': str(eid), 'attribute': attr, 'value': value})
        for child in node.values():
            collect(child)

pending = HERE.parent
reconciled = json.loads((pending / 'reconciliation.json').read_text())['reconciled']
target = {(r['entity'], r['attribute']) for r in reconciled}
for entity, attr, value in loads((pending / 'expected-fields.edn').read_text()):
    if (entity, attr) not in target:
        continue
    if attr == ':answer/value' and '$' not in value:
        value = '$' + value + '$'
    records.append({'id': str(entity), 'attribute': str(attr), 'value': value})

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
origin = f'http://127.0.0.1:{server.server_port}'
html = r'''<!doctype html><link rel="stylesheet" href="/ui/learning.css">
<style>body{background:#fff;color:#182537;padding:20px}article{max-width:840px;margin:20px auto;border-bottom:1px solid #ddd}</style>
<script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script>
<script src="/ui/vendor/dompurify/purify.min.js"></script><div id="content"></div>
<script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';
import {romanLists} from '/ui/prose-lists.js';
import {inlinePrompt} from '/ui/question-fields.js';
function el(tag, className, text) {const e=document.createElement(tag);if(className)e.className=className;if(text)e.textContent=text;return e;}
const source = await (await fetch('/ui/learning.js')).text();
// Exercise the actual Markdown protection and sanitization used by the player.
const renderer = source.slice(source.indexOf('function escapeHTML('), source.indexOf('function answerValue('));
const labels = source.slice(source.indexOf('function fieldLabel('), source.indexOf('\n}', source.indexOf('function fieldLabel(')) + 2);
const make = new Function('el','marked','romanLists','inlinePrompt', labels+';'+renderer+'; return markdown;');
window.render = make(el,marked,romanLists,inlinePrompt);
await MathJax.startup.promise; window.ready=true;
</script>'''
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1060, 'height': 1150})
        errors = []
        page.on('pageerror', lambda error: (errors.append(str(error)), print('PAGE ERROR:', error, flush=True)))
        page.on('console', lambda message: print('CONSOLE:', message.text, flush=True) if message.type == 'error' else None)
        page.on('requestfailed', lambda request: print('REQUEST FAILED:', request.url, request.failure, flush=True))
        page.route('**/*', lambda route: route.fulfill(body=html, content_type='text/html')
                   if route.request.url == origin + '/fixture' else route.continue_()
                   if route.request.url.startswith(origin + '/') else route.abort())
        page.goto(origin + '/fixture')
        page.wait_for_function('window.ready === true', timeout=10000)
        result = page.evaluate('''async records => {
          for (const record of records) {
            const article=document.createElement('article'); article.dataset.id=record.id; article.dataset.attribute=record.attribute;
            article.append(render(record.value)); content.append(article);
          }
          await MathJax.typesetPromise([content]);
          const tables=[];
          for (const item of MathJax.startup.document.math) item.root.walkTree(node=>{
            if(node.kind==='mtable') tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length,align:node.attributes.get('columnalign')});
          });
          return {records:records.length,tables,errors:[...content.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>({id:n.closest('article').dataset.id,attribute:n.closest('article').dataset.attribute,message:n.getAttribute('data-mjx-error')||n.textContent})),codeBlocks:content.querySelectorAll('pre').length};
        }''', records)
        assert not errors, errors
        (HERE / 'render-errors.json').write_text(json.dumps(result['errors'], indent=2))
        assert not result['errors'], result['errors']
        assert result['codeBlocks'] == 0, result
        report = {**result, 'tables': len(result['tables']), 'refreshed_fields_rendered': len(target),
                  'page_errors': errors, 'renderer': 'ui/learning.js + ui/mathjax-config.js + vendored MathJax'}
        (HERE / 'rendering-validation.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report))
        browser.close()
finally:
    server.shutdown()
    server.server_close()
