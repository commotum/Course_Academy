"""Render every repaired field using the actual player Markdown and MathJax code."""
import functools
import http.server
import json
import re
import sys
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
if '--lesson-equations' in sys.argv:
    HERE = HERE / 'lesson-equations'
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads
rows = loads((HERE / ('after.edn' if '--committed' in sys.argv else 'expected.edn')).read_text())
if '--lesson-all' in sys.argv:
    entities = {}
    def collect(node):
        if isinstance(node, list):
            for child in node: collect(child)
        elif isinstance(node, dict):
            if ':db/id' in node: entities.setdefault(node[':db/id'], {}).update(node)
            for child in node.values(): collect(child)
    collect(loads((HERE / 'lesson-current.edn').read_text()))
    rows = []
    for eid, entity in entities.items():
        for attr in [':tutorial/content', ':question/problem', ':question/worked-solution',
                     ':answer/value', ':answer/feedback', ':multistep/context']:
            text = entity.get(attr)
            if not isinstance(text, str): continue
            if attr == ':answer/value' and entity.get(':answer/type', {}).get(':db/ident') == ':answer.type/math':
                text = '$' + text + '$'
            rows.append([eid, attr, text])
records = [{'id': str(eid), 'attribute': str(attr), 'value': text} for eid, attr, text in rows]
def shapes(text):
    text = re.sub(r'%[^\n]*', '', text)
    result = []
    for match in re.finditer(r'\\begin\{(matrix|bmatrix|cases|array)\}', text):
        body = text[match.end():text.index('\\end{' + match[1] + '}', match.end())]
        if match[1] == 'array':
            body = body[body.index('}') + 1:]
        body = re.sub(r'\\hline\b', '', body)
        table = [row.strip() for row in body.split('\\\\') if row.strip()]
        widths = [len(row.split('&')) for row in table]
        assert len(set(widths)) == 1, (match[1], table)
        result.append({'rows': len(table), 'columns': widths[0]})
    return result
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
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
        page = browser.new_page(viewport={'width': 1060, 'height': 1100})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.route('**/*', lambda route: route.fulfill(body=html, content_type='text/html')
                   if route.request.url == origin + '/fixture' else route.continue_()
                   if route.request.url.startswith(origin + '/') else route.abort())
        page.goto(origin + '/fixture')
        page.wait_for_function('window.ready === true', timeout=10000)
        result = page.evaluate('''async records => {
          const results=[];
          for(const record of records) {
            const article=document.createElement('article');
            article.dataset.id=record.id;article.dataset.attribute=record.attribute;
            article.append(render(record.value));content.append(article);
            const previous = [...MathJax.startup.document.math].length;
            await MathJax.typesetPromise([article]);
            const tables=[];
            for(const item of [...MathJax.startup.document.math].slice(previous))item.root.walkTree(node=>{
              if(node.kind==='mtable')tables.push({rows:node.childNodes.length,
                columns:node.childNodes[0].childNodes.length,alignment:node.attributes.get('columnalign')});
            });
            results.push({id:record.id,attribute:record.attribute,tables,
              images:article.querySelectorAll('img').length,
              errors:[...article.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent)});
          }
          return results;
        }''', records)
        assert not errors, errors
        report = []
        for record, rendered in zip(records, result):
            expected = shapes(record['value'])
            actual = [{k: table[k] for k in ('rows','columns')} for table in rendered['tables']
                      if set(table['alignment'].split()) == {'center'} or table['alignment'] == 'left left']
            assert not rendered['errors'], rendered
            assert actual == expected, (record['id'], record['attribute'], expected, rendered)
            if record['id'] in ['17592186059576', '17592186059577', '17592186059578', '17592186059579']:
                assert rendered['images'] == 0, rendered
            report.append({**rendered, 'expected': expected})
        example = page.locator('article[data-id="17592186059579"]' if '--lesson-equations' in sys.argv
                               else 'article[data-id="17592186059576"]')
        example.last.screenshot(path=str(HERE / 'coefficient-matrix.png'))
        assert sum(len(r['expected']) for r in report) > 0
        report_file = 'lesson-rendering.json' if '--lesson-all' in sys.argv else (
            'committed-rendering.json' if '--committed' in sys.argv else 'rendering-validation.json')
        (HERE / report_file).write_text(
            json.dumps({'records': report, 'page_errors': errors}, indent=2) + '\n')
        print(f"Verified {len(report)} fields and {sum(len(r['expected']) for r in report)} matrix/system shapes")
        browser.close()
finally:
    server.shutdown()
    server.server_close()
