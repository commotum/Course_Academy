"""Verify real Activity UI and shared CSS; requests never submit learner work."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent / 'post-fix'
HERE.mkdir(exist_ok=True)
MEASURE = r'''id => {
 const card=document.querySelector(`[data-step-db-id="${id}"]`);
 return [...card.querySelectorAll('mjx-container')].filter(n=>n.getBoundingClientRect().width).map(n=>{
   const svg=n.querySelector('svg'),a=n.querySelector('mjx-assistive-mml');
   n.scrollLeft=n.scrollWidth;const range=n.scrollLeft;n.scrollLeft=0;
   return {choice:!!n.closest('.choice'),range,client:n.clientWidth,scroll:n.scrollWidth,
      svgWidth:svg.getBoundingClientRect().width,assistiveWidth:a?.getBoundingClientRect().width,
      accessible:!!a?.querySelector('math'),error:!!n.querySelector('[data-mml-node="merror"]')};
 });
}'''

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,ignore_default_args=['--hide-scrollbars'])
    page=browser.new_page(viewport={'width':1133,'height':926})
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.add_init_script("localStorage.setItem('course-academy.theme','light')")
    response=page.request.get('http://127.0.0.1:8765/ui/math-content.css')
    assert response.status==200
    page.goto('http://127.0.0.1:8765/activity')
    row=page.locator('.activity-row[data-task-id="17592186619060"]')
    row.locator(':scope > summary').click()
    card=page.locator('[data-step-db-id="17592186640784"]')
    page.wait_for_function('document.querySelectorAll(\'[data-step-db-id="17592186640784"] .choice mjx-container\').length===4')
    reports=[]
    for theme in ['light','dark']:
        page.evaluate('theme=>document.documentElement.dataset.theme=theme',theme)
        for width in [1133,768,390]:
            page.set_viewport_size({'width':width,'height':926})
            measurements={str(i):page.evaluate(MEASURE,str(i)) for i in [17592186640784,17592186640734]}
            assert len([n for n in measurements['17592186640784'] if n['choice']])==4
            assert all(not n['range'] and n['accessible'] and n['assistiveWidth']<=1.02 and not n['error']
                       for nodes in measurements.values() for n in nodes)
            card.screenshot(path=str(HERE/f'17592186640784-{theme}-{width}.png'))
            reports.append(dict(theme=theme,width=width,nodes=measurements))
    # Isolate the old hidden-layout behavior in this browser, then remove it.
    page.set_viewport_size({'width':1133,'height':926})
    page.evaluate("document.documentElement.dataset.theme='light'")
    diagnostic=page.add_style_tag(content='''
      mjx-container[jax="SVG"] > mjx-assistive-mml {width:auto!important;height:auto!important;padding:1px 0 0!important}
      mjx-container[jax="SVG"] > mjx-assistive-mml[display="block"] {width:100%!important}
      .prose mjx-container:not([display="true"]) {padding-inline-end:.3em}
    ''')
    before=page.evaluate(MEASURE,'17592186640784')
    assert len([n for n in before if n['choice'] and n['range']])==2
    diagnostic.evaluate('(style)=>style.remove()')
    # Open explanations through the real UI, covering dynamically rendered math.
    for identifier in ['17592186640784','17592186640734']:
        target=page.locator(f'[data-step-db-id="{identifier}"]')
        target.locator('.history-solution > summary').click()
        page.wait_for_function('''id=>document.querySelectorAll(`[data-step-db-id="${id}"] .history-explanation mjx-container[display="true"]`).length>=2''',arg=identifier)
        after=page.evaluate(MEASURE,identifier)
        assert all(not n['range'] and n['accessible'] and n['assistiveWidth']<=1.02 and not n['error'] for n in after)
        reports.append(dict(explanation=identifier,nodes=after))
    assert not errors,errors
    (HERE/'live-verification.json').write_text(json.dumps(dict(passed=True,origin='http://127.0.0.1:8765',
        shared_stylesheet_status=response.status,database_writes=0,page_errors=errors,
        diagnostic_before=before,cases=reports),indent=2)+'\n')
    browser.close()
print('Live Activity verified: both reported questions; 4 choices; 3 widths; 2 themes; opened explanations.')
