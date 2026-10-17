"""Read-only full-player preview of one authored prompt layout change."""
import copy
import functools
import hashlib
import http.server
import importlib.util
import json
from pathlib import Path
import threading
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CHANGE = HERE.parent / 'change.json'
change = json.loads(CHANGE.read_text())
question = json.loads((HERE.parent / 'question.json').read_text())
spec = importlib.util.spec_from_file_location('preview', ROOT / 'generate/pipeline/render_preview.py')
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)
activities = []
for version in ['before', 'after']:
    q = copy.deepcopy(question)
    q[change['attribute']] = change[version]
    activity = preview.preview({'question': q}, len(activities))
    activity['title'] = 'Line definitions layout review'
    step = activity['steps'][0]
    step['contentId'] = change['entity']
    step['status'] = 'started'
    for field in step['fields']:
        field.pop('response', None)
    activities.append(activity)


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        data = None
        if parsed.path == '/api/developer-mode':
            data = {'enabled': True}
        elif parsed.path == '/api/preview':
            data = activities[int(parse_qs(parsed.query)['activityId'][0])]
        if data is not None:
            body = json.dumps(data).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def translate_path(self, path):
        if urlparse(path).path == '/learn':
            return str(ROOT / 'ui/Learning.html')
        return super().translate_path(path)

    def do_POST(self):
        self.send_error(405, 'Read-only local render fixture')


server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
origin = f'http://127.0.0.1:{server.server_port}'
results = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome')
        for viewport, width, height in [('desktop', 1280, 1000), ('mobile', 390, 844)]:
            for index, version in enumerate(['before', 'after']):
                page = browser.new_page(viewport={'width': width, 'height': height})
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.route('**/*', lambda route: route.continue_() if route.request.url.startswith(origin + '/') else route.abort())
                page.goto(origin + f'/learn?activityId={index}', wait_until='networkidle')
                page.locator('.lesson-content').wait_for()
                page.evaluate('''async () => {
                    await MathJax.startup.promise;
                    await MathJax.typesetPromise();
                    await document.fonts.ready;
                    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
                }''')
                result = page.locator('.lesson-content').evaluate(r'''root => {
                    const tables = [];
                    for (const item of MathJax.startup.document.math) {
                        if (!item.math.includes('alignedat')) continue;
                        item.root.walkTree(n => {
                            if (n.kind === 'mtable') tables.push({display: item.display, tex: item.math,
                                rows: n.childNodes.length,
                                columns: n.childNodes[0]?.childNodes.length,
                                cells: n.childNodes.map(row => row.childNodes.map(c => c.toString()))});
                        });
                    }
                    return {
                        tables,
                        errors: [...root.querySelectorAll('[data-mml-node="merror"],mjx-merror,.math-error,[data-mjx-error]')].map(n=>n.textContent),
                        bodyOverflow: document.body.scrollWidth > window.innerWidth + 2,
                        contentOverflow: root.scrollWidth > root.clientWidth + 2,
                        controls: [...root.querySelectorAll('select,input,textarea,math-field')].map(n=>({
                            tag: n.tagName, type: n.type, name: n.name,
                            options: n.tagName === 'SELECT' ? [...n.options].map(o=>({value:o.value,text:o.textContent,disabled:o.disabled})) : null
                        })),
                        displayEquations: root.querySelectorAll('mjx-container[display="true"]').length,
                        fonts: document.fonts.status
                    };
                }''')
                stem = HERE / f'{version}-{viewport}'
                page.screenshot(path=str(stem) + '.png', full_page=True, animations='disabled')
                Path(str(stem) + '.html').write_text(page.content())
                select = page.locator('.lesson-content select')
                option = select.locator('option:not([disabled])').last.get_attribute('value')
                select.select_option(option)
                result.update({'version': version, 'viewport': viewport, 'javascriptErrors': errors,
                               'selectInteractive': select.input_value() == option,
                               'screenshot': str(stem.relative_to(ROOT)) + '.png'})
                result['passed'] = not errors and not result['errors'] and result['fonts'] == 'loaded' and result['selectInteractive']
                if version == 'after':
                    result['passed'] &= not result['bodyOverflow'] and not result['contentOverflow']
                    result['passed'] &= len(result['tables']) == 1 and result['tables'][0]['display'] and result['tables'][0]['rows'] == 2 and result['tables'][0]['columns'] == 4
                results.append(result)
                page.close()
        browser.close()
finally:
    server.shutdown()
    server.server_close()

comparisons = []
for viewport in ['desktop', 'mobile']:
    before, after = [r for r in results if r['viewport'] == viewport]
    comparisons.append({'viewport': viewport, 'controls_identical': before['controls'] == after['controls']})
summary = {
    'passed': all(r['passed'] for r in results) and all(r['controls_identical'] for r in comparisons),
    'changes_sha256': hashlib.sha256(CHANGE.read_bytes()).hexdigest(),
    'database_writes': 0,
    'renderer': 'Unmodified current Learning.html, learning.js, question-fields.js and MathJax',
    'cases': results,
    'control_comparisons': comparisons,
    'ui_hashes': {name: hashlib.sha256((ROOT / 'ui' / name).read_bytes()).hexdigest()
                  for name in ['Learning.html', 'learning.js', 'question-fields.js', 'mathjax-config.js', 'learning.css']}
}
(HERE / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({'passed': summary['passed'], 'changes_sha256': summary['changes_sha256']}))
assert summary['passed']
