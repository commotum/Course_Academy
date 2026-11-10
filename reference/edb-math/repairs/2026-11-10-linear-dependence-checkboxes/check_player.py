"""Exercise actual player checkbox controls and rendering without learner writes."""
import functools
import http.server
import json
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

H=Path(__file__).resolve().parent
ROOT=H.parents[3]
# Reuse the real-renderer fixture and fieldControl extraction from the preceding
# dropdown repair; no application implementation is duplicated here.
prior=(H.parent/'2026-11-10-linear-operator-inline-dropdowns/check_inline.py').read_text()
setup=prior[prior.index('fixture = '):prior.index('\n\nclass Quiet')]
exec(setup)
fixture+='''<script>
window.showCheckboxQuestion=async item=>{
 MathJax.typesetClear([content]);content.replaceChildren();
 const card=document.createElement('article');card.className='lesson-content content-card';
 const form=document.createElement('form');form.append(render(item.problem,'prose',item.fields));
 const list=document.createElement('div');list.className='answer-fields';
 for(const f of item.fields)list.append(realControl(f,!!item.readOnly,item.entity,item.problem,item.status||''));
 form.append(list);card.append(form);
 const solution=render(item.solution);solution.classList.add('worked-solution');card.append(solution);
 content.append(card);await MathJax.typesetPromise([content]);
 const controls=[...form.querySelectorAll('input[type=checkbox]')];
 return {controls:controls.length,dropdowns:form.querySelectorAll('select,.answer-select-trigger').length,
  equations:[...form.querySelectorAll('label.choice')].map(n=>n.textContent),
  math_errors:content.querySelectorAll('[data-mml-node=merror],mjx-merror').length,
  outer_overflow:card.scrollWidth>card.clientWidth+1,
  inner_overflow:[...form.querySelectorAll('mjx-container')].filter(n=>n.scrollWidth>n.clientWidth+1).map(n=>({
   text:n.textContent,width:n.clientWidth,scroll:n.scrollWidth,svg:n.querySelector('svg')?.getBoundingClientRect().width})),
  states:controls.map(n=>({checked:n.checked,disabled:n.disabled,encoded:n.closest('label').querySelector('.answer-choice-value').value}))};
};</script>'''

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*_): pass

questions=json.loads((H/'speculative-questions.json').read_text())
items=[]
for q in questions:
    items.append(dict(entity=q[':db/id'],problem=q[':question/problem'],solution=q[':question/worked-solution'],fields=[dict(
        id=str(f[':db/id']),key=f[':answer-field/key'],type='checkbox',
        choices=[dict(id=str(a[':db/id']),type='text',value=a[':answer/value']) for a in f[':answer-field/choices']],
        correctAnswer=dict(id=str(f[':answer-field/correct'][':db/id']),value=f[':answer-field/correct'][':answer/value'])) for f in q[':question/answer-fields']]))
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
origin=f'http://127.0.0.1:{server.server_port}'
checks=[]
(H/'visual').mkdir(exist_ok=True)
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page()
        page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html') if r.request.url==origin+'/fixture' else r.continue_() if r.request.url.startswith(origin+'/') else r.abort())
        page.goto(origin+'/fixture');page.wait_for_function('window.ready&&window.inlineReady')
        for width in [1100,708,390]:
            page.set_viewport_size(dict(width=width,height=1200))
            for item in items:
                result=page.evaluate('showCheckboxQuestion',item)
                assert result['controls']==3 and not any(result[k] for k in ['dropdowns','math_errors','outer_overflow']),(item['entity'],width,result)
                assert all(n['svg']>n['width'] for n in result['inner_overflow']),(item['entity'],width,result)
                assert all(not s['checked'] and not s['disabled'] for s in result['states'])
                for i,f in enumerate(item['fields']):
                    box=page.locator('input[type=checkbox]').nth(i)
                    box.locator('xpath=ancestor::label').click()
                    assert box.is_checked()
                    encoded=page.locator('.answer-choice-value').nth(i).input_value()
                    assert encoded==next(a['id'] for a in f['choices'] if a['value']=='true')
                    box.locator('xpath=ancestor::label').click()
                    assert not box.is_checked()
                    assert page.locator('.answer-choice-value').nth(i).input_value()==next(a['id'] for a in f['choices'] if a['value']=='false')
                checks.append(dict(question=item['entity'],width=width,**result))
                if item['entity'] in [17592186572667,17592186707089]:
                    page.locator('.content-card').screenshot(path=str(H/'visual'/f"{item['entity']}-{width}.png"))
                saved=dict(item,readOnly=True,status='correct',fields=[dict(f,response=f['correctAnswer']) for f in item['fields']])
                restored=page.evaluate('showCheckboxQuestion',saved)
                assert all(s['disabled'] and s['checked']==(f['correctAnswer']['value']=='true') for s,f in zip(restored['states'],item['fields']))
                assert page.locator('.answer-indicator[data-result=missed],.answer-indicator[data-result=incorrect]').count()==0
        browser.close()
finally:
    server.shutdown();server.server_close()
(H/'player-verification.json').write_text(json.dumps(dict(passed=True,database_writes=0,question_viewports=len(checks),checkbox_toggles=6*len(checks),saved_correct_restorations=len(checks),checks=checks),indent=2)+'\n')
print('Actual player rendering, Boolean submission and saved feedback passed at desktop/tablet/mobile widths.')
