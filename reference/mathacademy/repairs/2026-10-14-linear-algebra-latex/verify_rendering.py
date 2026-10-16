"""Check actual player output for exposed TeX, system braces and equal-sign positions."""
import functools
import hashlib
import http.server
import json
import sys
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[4]
REVIEW = Path(__file__).resolve().parent
HERE = REVIEW
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads
from math_format import ENV, environment, cells
import re
input_file = HERE / 'all-expected.edn'
fields = json.loads((HERE / 'fields.json').read_text())
records = [{'id':str(f['entity']), 'attribute':f['attribute'],
            'value':('$'+f['after']+'$') if f['kind']=='math' else f['after']} for f in fields]
if '--generators' in sys.argv:
    input_file = HERE / 'generator-smoke.json'
    records = []
    for i, item in enumerate(json.loads(input_file.read_text())['records']):
        q=item['question']
        for attr in [':question/problem', ':question/worked-solution']:
            records.append({'id':str(i), 'attribute':attr, 'value':q[attr]})
        for j, field in enumerate(q[':question/answer-fields']):
            for k, answer in enumerate(field[':answer-field/choices']):
                text=answer[':answer/value']
                records.append({'id':str(i), 'attribute':f'answer-{j}-{k}', 'value':'$'+text+'$' if answer[':answer/type']==':answer.type/math' else text})
def matrix_shapes(text):
    shapes=[]
    for opening in ENV.finditer(text):
        if opening[1]!='begin' or opening[2] not in ['bmatrix','pmatrix','vmatrix','Bmatrix','Vmatrix','matrix','array']:continue
        span=environment(text,opening.start())
        if not span:continue
        body=text[span[0]:span[1]]
        if opening[2]=='array':
            spec=re.match(r'\s*\{[clr| ]+\}',body)
            if not spec:continue
            body=body[spec.end():]
        if re.search(r'\\(?:multicolumn|hdotsfor)\b',body):continue
        rows=cells(body)
        if rows and len({len(row) for row in rows})==1:shapes.append([len(rows),len(rows[0])])
    return shapes
for record in records:record['expected_matrices']=matrix_shapes(record['value'])
only = set(sys.argv[sys.argv.index('--only') + 1].split(',')) if '--only' in sys.argv else None
if only: records = [r for r in records if r['id'] in only]
cached = {}
if '--reuse' in sys.argv:
    for item in json.loads((REVIEW / 'render-cache.json').read_text()):
        result = item['result']; text = item['text']
        if result['attribute'] == ':answer/value' and '$' not in text: text = '$' + text + '$'
        cached[result['id'], result['attribute'], text] = result
pending = [r for r in records if (r['id'], r['attribute'], r['value']) not in cached]
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
origin = f'http://127.0.0.1:{server.server_port}'
html = (REVIEW / 'renderer-fixture.html').read_text()
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 810, 'height': 1050})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.route('**/*', lambda route: route.abort() if route.request.resource_type == 'image' else route.fulfill(body=html, content_type='text/html')
                   if route.request.url == origin + '/fixture' else route.continue_()
                   if route.request.url.startswith(origin + '/') else route.abort())
        page.goto(origin + '/fixture')
        page.wait_for_function('window.ready === true', timeout=10000)
        result = page.evaluate(r'''async ({records,batched}) => {
          const results=[];
          for(const record of records) {
            const article=document.createElement('article');
            article.dataset.id=record.id;article.dataset.attribute=record.attribute;
            article.append(render(record.value));content.append(article);
            const previous=[...MathJax.startup.document.math].length;
            await MathJax.typesetPromise([article]);
            const systems=[];
            for(const table of article.querySelectorAll('[data-mml-node="mtable"]')) {
              const brace=[...table.parentElement.children].find(n=>n.dataset.mmlNode==='mo');
              if(!brace?.querySelector('[data-c="7B"],[data-c="23A7"],[data-c="23A8"],[data-c="23A9"]'))continue;
              const equals=[...table.children].filter(n=>n.dataset.mmlNode==='mtr').map(row=>
                (row.children[1]||row).querySelector('use[data-c="3D"],path[data-c="3D"]'))
                .filter(Boolean).map(n=>n.getBoundingClientRect().x);
              if(!equals.length)continue;
              systems.push({equals,braceHeight:brace.getBoundingClientRect().height,
                            tableHeight:table.getBoundingClientRect().height});
            }
            const tables=[...article.querySelectorAll('[data-mml-node="mtable"]')].map(t=> {
              const rows=[...t.children].filter(n=>n.dataset.mmlNode==='mtr');
              return [rows.length,Math.max(0,...rows.map(r=>[...r.children].filter(n=>n.dataset.mmlNode==='mtd').length))];
            });
            let cursor=0;
            const missingMatrices=[];
            for(const shape of record.expected_matrices) {
              while(cursor<tables.length && (tables[cursor][0]!==shape[0] || tables[cursor][1]!==shape[1]))cursor++;
              if(cursor===tables.length)missingMatrices.push(shape);else cursor++;
            }
            const outside=article.cloneNode(true);
            outside.querySelectorAll('mjx-container,math-field').forEach(n=>n.remove());
            const exposed=outside.textContent.match(/(?<!\\)\$|\\(?:begin|end)\{[^}]+\}/g)||[];
            results.push({id:record.id,attribute:record.attribute,systems,exposed,tables,missingMatrices,
              outside_text:exposed.length?outside.textContent:'',
              formulas:[...MathJax.startup.document.math].length-previous,
              errors:[...article.querySelectorAll('[data-mml-node="merror"],mjx-merror')]
                .map(n=>n.getAttribute('data-mjx-error')||n.textContent)});
            if(batched && results.length%25===0) {
              MathJax.typesetClear([content]);content.replaceChildren();
            }
          }
          return results;
        }''', {'records': pending, 'batched': '--lesson-all' not in sys.argv})
        rendered = {(r['id'], r['attribute']): r for r in result}
        result = [cached.get((r['id'], r['attribute'], r['value'])) or rendered[r['id'], r['attribute']] for r in records]
        report = {'records': result, 'page_errors': errors,
                  'input_sha256': hashlib.sha256(input_file.read_bytes()).hexdigest()}
        filename = ('generator-' if '--generators' in sys.argv else '') + ('lesson-' if '--lesson-all' in sys.argv else '') + ('committed-' if '--committed' in sys.argv else '') + 'rendering-validation.json'
        if only: filename = 'partial-' + filename
        (HERE / filename).write_text(json.dumps(report, indent=2) + '\n')
        bad = [r for r in result if r['errors'] or r['exposed'] or r['missingMatrices']]
        if bad:
            page.unroute_all(behavior='wait'); browser.close()
        assert not errors, errors
        assert not bad, [(r['id'], r['attribute'], r['errors'], r['exposed'], r['missingMatrices']) for r in bad][:15]
        target = [r for r in result if r['id'] in ['17592186240971', '17592186338974']]
        all_systems = [s for r in result for s in r['systems']]
        for system in all_systems:
            assert system['braceHeight'] >= system['tableHeight'] * .9, system
            assert len(system['equals']) >= 1, system
            assert max(system['equals']) - min(system['equals']) < .5, system
        if '--lesson-all' in sys.argv:
            for eid in ['17592186240971', '17592186338974']:
                page.locator(f'article[data-id="{eid}"]').first.screenshot(path=str(HERE / (eid + '-problem.png')))
                page.locator(f'article[data-id="{eid}"]').last.screenshot(path=str(HERE / (eid + '-solution.png')))
            # Include the later reports' choice blocks in visual review.
            for eid in ['17592186337159', '17592186422777']:
                page.locator(f'article[data-id="{eid}"]').screenshot(path=str(HERE / (eid + '-choice.png')))
        print(f'Verified {len(result)} fields, {len(all_systems)} system braces, aligned equals, and no exposed TeX or collapsed matrices')
        browser.close()
finally:
    server.shutdown()
    server.server_close()
