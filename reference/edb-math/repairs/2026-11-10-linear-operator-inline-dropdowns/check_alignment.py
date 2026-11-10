"""Check that all three operators begin at the same list position."""
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


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


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
        page.wait_for_function('window.ready')
        for width in [1100, 708, 390]:
            page.set_viewport_size(dict(width=width, height=1000))
            for phase in ['before', 'after']:
                q = json.loads((H / 'alignment' / f'question-{phase}.json').read_text())
                result = page.evaluate('''async value=>{
                    MathJax.typesetClear([content]);content.className='content-card';content.replaceChildren(render(value));
                    await MathJax.typesetPromise([content]);
                    const nodes=[...content.querySelectorAll('li mjx-container')];
                    return{count:nodes.length,left_edges:nodes.map(n=>n.querySelector('svg').getBoundingClientRect().left),
                      math_errors:content.querySelectorAll('[data-mml-node="merror"]').length,
                      outer_overflow:content.scrollWidth>content.clientWidth+1};
                }''', q[':question/problem'])
                assert result['count'] == 3 and not result['math_errors'] and not result['outer_overflow'], result
                spread = max(result['left_edges']) - min(result['left_edges'])
                if phase == 'after':
                    assert spread < 1, result
                checks.append(dict(width=width, phase=phase, left_edge_spread=spread, **result))
                page.locator('#content').screenshot(path=str(H / 'visual' / f'operator-alignment-{phase}-{width}.png'))
        browser.close()
finally:
    server.shutdown()
    server.server_close()
(H / 'alignment-layout.json').write_text(json.dumps(dict(passed=True, database_writes=0, checks=checks), indent=2) + '\n')
print(json.dumps(checks, indent=2))
