"""Read-only player layout checks and source-backed before/after previews."""
import functools
import http.server
import json
import sys
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from question_capture.math_format import normalize_prose
fields = json.loads((HERE / 'fields.json').read_text())
questions = json.loads((HERE / 'questions.json').read_text())
fresh = {r['entity']: r for r in json.loads((HERE / 'current-extractor-results.json').read_text())}
fixture = (ROOT / 'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
fixture = fixture.replace('<!doctype html>', '<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
fixture += '''<script type="module">
import {mountInlineFields,blankInput,loadMathInputs} from '/ui/question-fields.js';
await loadMathInputs();
window.mountAuditFields=(prompt,fields)=>{
 const list=document.createElement('div');
 mountInlineFields(prompt,list,fields,field=>{
  const box=document.createElement('fieldset');
  if(field.type==='blank') box.append(blankInput(field,field.key,field.id,true));
  return box;
 });
};window.auditReady=true;
</script>'''
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
origin = f'http://127.0.0.1:{server.server_port}'
visual = HERE / 'visual'
visual.mkdir(exist_ok=True)
reports = []
try:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width':1100,'height':900})
        def route(request):
            if request.request.url == origin+'/fixture': request.fulfill(body=fixture,content_type='text/html')
            elif request.request.url.startswith(origin+'/'): request.continue_()
            else: request.abort()
        page.route('**/*',route)
        page.goto(origin+'/fixture')
        page.wait_for_function('window.ready && window.auditReady')
        show = '''async item=>{
          MathJax.typesetClear([content]);content.replaceChildren();
          const article=document.createElement('article');article.className='lesson-content';
          const card=document.createElement('div');card.className='content-card';
          const h=document.createElement('h2');h.textContent=item.label;card.append(h);
          const prompt=render(item.value,'prose',item.fields||[]);card.append(prompt);
          mountAuditFields(prompt,item.fields||[]);article.append(card);content.append(article);
          await MathJax.typesetPromise([content]);await document.fonts.ready;
          return {errors:[...content.querySelectorAll('[data-mjx-error]')].map(n=>n.getAttribute('data-mjx-error')),
           tables:[...prompt.querySelectorAll('table')].map(t=>({canonical:!!t.closest('.matrix-answer'),
             rows:[...t.rows].map(r=>r.cells.length),headers:t.querySelectorAll('th').length})),
           slots:[...prompt.querySelectorAll('[data-field-key]')].map(n=>{const r=n.getBoundingClientRect();return {key:n.dataset.fieldKey,x:r.x,y:r.y,width:r.width,height:r.height}}),
           rawMarkers:prompt.textContent.includes('{{field-'),
           cardScrollWidth:card.scrollWidth,cardClientWidth:card.clientWidth};
        }'''
        for width in [1100,390]:
            page.set_viewport_size({'width':width,'height':900})
            for question in questions:
                entity=question[':db/id']
                field=next(f for f in fields if f['entity']==entity and f['attribute']==':question/problem')
                result=page.evaluate(show,{**field,'label':question[':question/math-academy-id']})
                reports.append({'entity':entity,'width':width,**result})
                if width==1100 and entity in [17592186299639,17592186643141,17592186235515,17592186603024,17592186604599]:
                    page.locator('.content-card').screenshot(path=str(visual/(str(entity)+'-stored.png')))
        page.set_viewport_size({'width':1100,'height':900})
        for entity in [17592186299639,17592186643141]:
            field=next(f for f in fields if f['entity']==entity and f['attribute']==':question/problem')
            value=normalize_prose(fresh[entity]['prompt_sources']['problem'])
            page.evaluate(show,{**field,'value':value,'label':'Source-backed re-extraction preview'})
            page.locator('.content-card').screenshot(path=str(visual/(str(entity)+'-reextracted-preview.png')))
        for field in fields:
            if field['attribute']==':tutorial/content':
                page.evaluate(show,{**field,'label':'Stored tutorial '+str(field['entity'])})
                page.locator('.content-card').screenshot(path=str(visual/(str(field['entity'])+'-tutorial.png')))
        browser.close()
finally:
    server.shutdown();server.server_close()
(HERE/'layout-report.json').write_text(json.dumps(reports,indent=2)+'\n')
print(json.dumps({'prompt_checks':len(reports),'math_errors':sum(bool(r['errors'])for r in reports),
                  'raw_markers':sum(r['rawMarkers']for r in reports),
                  'data_table_questions':sorted({r['entity']for r in reports if any(not t['canonical']for t in r['tables'])}),
                  'screenshots':len(list(visual.glob('*.png')))},indent=2))
