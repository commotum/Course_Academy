#!/usr/bin/env python3
"""Read-only live preview and actual player-renderer verification; no learner events."""
import json
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ORIGIN = 'http://127.0.0.1:8765'
QUESTION = 17592186376068

def entities(value):
    if isinstance(value, dict):
        if ':db/id' in value:
            yield value
        for child in value.values():
            yield from entities(child)
    elif isinstance(value, list):
        for child in value:
            yield from entities(child)

snapshot = json.loads((HERE / 'snapshot.json').read_text())
expected = next(q for q in entities(snapshot)
                if q[':db/id'] == QUESTION and ':question/problem' in q)
expected_by_id = {e[':db/id']: e for e in entities(expected)}
for change in json.loads((HERE / 'proposal.json').read_text())['proposals']:
    if change['entity'] in expected_by_id:
        expected_by_id[change['entity']][change['attribute']] = change['after']

# /api/preview maps to developer_preview::preview, an inspection-only read.
api_url = ORIGIN + '/api/preview?topicId=17592186051046'
with urlopen(api_url, timeout=120) as response:
    preview = json.load(response)
assert preview['preview'] is True
question = next(q for q in preview['steps'] if q['contentId'] == QUESTION)
assert question['markdown'] == expected[':question/problem']
assert question['solution'] == expected[':question/worked-solution']
assert {f['id']: f['key'] for f in question['fields']} == {
    f[':db/id']: f[':answer-field/key'] for f in expected[':question/answer-fields']}

fixture = (ROOT / 'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
fixture = fixture.replace('<!doctype html>', '<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
fixture = fixture.replace('<script src="/ui/vendor/mathjax/tex-svg.js">',
    '<script>MathJax.tex.packages=MathJax.tex.packages.filter(n=>n!=="noundefined");</script><script src="/ui/vendor/mathjax/tex-svg.js">')
errors, requests = [], []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1100, 'height': 950})
    page.on('pageerror', lambda error: errors.append(str(error)))
    def route(request):
        url = request.request.url
        requests.append({'method': request.request.method, 'url': url})
        if url == ORIGIN + '/__subspaces-live-render':
            request.fulfill(body=fixture, content_type='text/html')
        elif request.request.method == 'GET' and url.startswith(ORIGIN + '/ui/'):
            request.continue_()
        else:
            request.abort()
    page.route('**/*', route)
    page.goto(ORIGIN + '/__subspaces-live-render')
    page.wait_for_function('window.ready')
    checks = page.evaluate('''async q => {
      const article=document.createElement('article');article.className='content-card';content.append(article);
      const append=(value,kind)=>{const node=render(value,'prose');node.dataset.kind=kind;article.append(node);};
      append(q.markdown,'prompt');
      for(const f of q.fields)append('☐ '+f.key,'choice-'+f.id);
      append('**Worked solution**\\n\\n'+q.solution,'solution');
      await MathJax.typesetPromise([content]);await document.fonts.ready;
      return [...article.children].map(node=>({kind:node.dataset.kind,
        errors:[...node.querySelectorAll('[data-mml-node="merror"],[data-mjx-error]')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),
        rawDelimiters:node.textContent.includes('$$'),
        glyphs:[...node.querySelectorAll('svg [data-c]')].map(n=>({code:n.getAttribute('data-c'),fill:getComputedStyle(n).fill}))
      }));
    }''', question)
    screenshot = HERE / 'live-question-17592186376068.png'
    page.screenshot(path=str(screenshot), full_page=True)
    browser.close()

glyphs = [g for check in checks for g in check['glyphs']]
codes = {g['code'] for g in glyphs}
(HERE / 'live-glyphs.json').write_text(json.dumps(checks, indent=2) + '\n')
assert not errors and all(not c['errors'] and not c['rawDelimiters'] for c in checks)
assert '3A0' in codes and '1D6F1' not in codes, 'Pi must use the upright source glyph'
assert '211D' in codes, 'Real-number space must retain blackboard bold'
assert {'1D42F', '1D7CE', '1D41A', '1D41B'} <= codes, 'Vector v, zero, a and b must remain bold'
# math-content.css maps source red to #c00000 for the light theme.
assert sum(g['code'] == 'D7' and g['fill'] == 'rgb(192, 0, 0)' for g in glyphs) == 2
assert all(r['method'] == 'GET' and not urlsplit(r['url']).path.startswith('/api/') for r in requests)
report = {'passed': True, 'api': api_url, 'basis': preview['basis'], 'question': QUESTION,
          'exact_live_prompt_solution_labels': True, 'actual_player_renderer': True,
          'strict_undefined_commands': True, 'upright_pi': True, 'blackboard_R': True,
          'bold_vectors': True, 'red_crosses': 2, 'errors': errors, 'checks': checks,
          'screenshot': str(screenshot), 'database_writes': 0, 'learner_events': 0,
          'browser_requests': requests}
(HERE / 'live-verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k not in ('checks', 'browser_requests')}))
