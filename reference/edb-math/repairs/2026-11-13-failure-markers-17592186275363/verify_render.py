"""Render the saved solution from the live read-only preview API."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
proposal = json.loads((HERE / 'proposal.json').read_text())
fixture = (ROOT / 'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
fixture = fixture.replace('<!doctype html>', '<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width':1100,'height':1000})
    response = page.request.get('http://127.0.0.1:8765/api/preview?topicId=17592186051046')
    assert response.ok
    data = response.json()
    step = next(s for s in data['steps'] if s.get('contentId') == proposal['entity'])
    assert step['solution'] == proposal['after']
    page.route('**/math-repair-verification', lambda r:r.fulfill(body=fixture,content_type='text/html'))
    page.goto('http://127.0.0.1:8765/math-repair-verification')
    page.wait_for_function('window.ready')
    page.evaluate('''async solution=>{
      const card=document.createElement('article');card.className='content-card';
      card.append(render(solution));content.append(card);await MathJax.typesetPromise([card]);
    }''', step['solution'])
    checks=[]
    for theme in ['light','dark']:
        page.evaluate('theme=>document.documentElement.dataset.theme=theme',theme)
        result=page.evaluate('''()=>({
          colors:[...content.querySelectorAll('svg g[fill="red"] [data-c="D7"]')].map(n=>getComputedStyle(n).fill),
          sourceSpacedMarkers:[...content.querySelectorAll('mjx-assistive-mml math')].filter(n=>n.querySelector('mspace[width="1em"]')&&n.querySelector('mstyle[mathcolor="red"]')).length,
          errors:content.querySelectorAll('[data-mml-node="merror"]').length
        })''')
        assert result['colors']==(['rgb(192, 0, 0)'] if theme=='light' else ['rgb(255, 119, 119)'])*2,result
        assert result['sourceSpacedMarkers']==2 and result['errors']==0,result
        page.locator('.content-card').screenshot(path=str(HERE/f'corrected-{theme}.png'))
        checks.append(dict(theme=theme,**result))
    (HERE/'live-render-verification.json').write_text(json.dumps(dict(passed=True,basis=data['basis'],checks=checks),indent=2)+'\n')
    browser.close()
print('Live solution matches repair; both red, spaced crosses render correctly in light and dark themes.')
