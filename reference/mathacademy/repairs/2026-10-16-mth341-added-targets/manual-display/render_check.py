"""Render the proposed manual patches using the application's Markdown/MathJax."""
import functools
import http.server
import json
import sys
import threading
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
AUDIT = ROOT / 'reference/mathacademy/audits/2026-10-16-mth341-added-targets'
PRIOR = ROOT / 'reference/mathacademy/audits/2026-10-16-mth341'
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads
import math_format as mf

types = {r[0][':db/id']: r[0][':db/ident'] for r in loads((PRIOR / 'types.edn').read_text())}
entities = json.loads((AUDIT / 'entities.json').read_text())
fields = json.loads((HERE / 'changes.json').read_text())
for field in fields:
    field['value'] = mf.normalize_prose(field['after'])
    field['answerFields'] = [{'key': a[':answer-field/key'], 'id': a[':db/id'], 'type': types[a[':answer-field/type'][':db/id']]} for a in entities[str(field['entity'])].get(':question/answer-fields', [])]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def translate_path(self, path):
        if path.startswith('/api/asset?'):
            return str(Path('/media/jake/SSD/EDB/math') / parse_qs(urlparse(path).query)['path'][0])
        if path.startswith('/images/'):
            return str(Path('/media/jake/SSD/EDB/math') / path.lstrip('/'))
        return super().translate_path(path)


server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
origin = f'http://127.0.0.1:{server.server_port}'
html = (PRIOR / 'render-fixture.html').read_text()
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome')
        page = browser.new_page(viewport={'width': 1060, 'height': 1100})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.route('**/*', lambda route: route.fulfill(body=html, content_type='text/html') if route.request.url == origin + '/fixture' else route.continue_() if route.request.url.startswith(origin + '/') else route.abort())
        page.goto(origin + '/fixture')
        page.wait_for_function('window.ready===true', timeout=20000)
        results = page.evaluate(r'''async records => {
          const results = [];
          for (const record of records) {
            MathJax.typesetClear(); content.replaceChildren();
            const article = document.createElement('article');
            article.append(render(record.value, "prose", record.answerFields));
            content.append(article); await MathJax.typesetPromise([article]);
            const plain = article.cloneNode(true);
            plain.querySelectorAll('mjx-container,pre,code').forEach(n => n.remove());
            results.push({entity: record.entity, attribute: record.attribute,
              residualText: /\$|\\(?:begin|end|left|right|text|frac)\b/.test(plain.textContent) ? plain.textContent : null,
              codeBlocks: [...article.querySelectorAll('pre')].map(n => n.textContent),
              errors: [...article.querySelectorAll('[data-mjx-error], [data-mml-node="mtext"][fill="red"], [data-mml-node="merror"], mjx-merror')].map(n => n.outerHTML),
              inputKeys: [...article.querySelectorAll('.field-location')].map(n => n.getAttribute('data-field-key'))});
          } return results;
        }''', fields)
        (HERE / 'rendering.json').write_text(json.dumps({'fields': results, 'page_errors': errors}, indent=2) + '\n')
        for eid in [17592186069113,17592186069114,17592186069129,17592186203878,17592186204598,17592186508108]:
            selected = [f for f in fields if f['entity'] == eid]
            page.evaluate('''async fs => {MathJax.typesetClear(); content.replaceChildren(); for(const f of fs) {let a=document.createElement('article'); a.append(Object.assign(document.createElement('h3'), {textContent:f.attribute}), render(f.value,"prose",f.answerFields)); content.append(a);} await MathJax.typesetPromise([content]);}''', selected)
            page.locator('img').evaluate_all('(imgs)=>Promise.all(imgs.map(i=>{i.loading="eager";return i.decode().catch(()=>{});} ))')
            page.screenshot(path=str(HERE / f'entity-{eid}.png'), full_page=True)
        browser.close()
finally:
    server.shutdown()
    server.server_close()

issues = [r for r in results if r['residualText'] or r['errors'] or r['codeBlocks']]
print(json.dumps({'rendered': len(results), 'page_errors': errors, 'issues': issues}, indent=2))
assert not errors and not issues
