"""Read-only original-source conversion and player render comparison."""
import functools,http.server,json,sys,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
source=R/'reference/mathacademy/capture/linear/14195578/observations/step-q85526-7a7c74f995b9f5aa8ae3.json'
captured=json.loads(source.read_text());question=json.loads((H/'question.json').read_text())[0][0];choices=question[':question/answer-fields'][0][':answer-field/choices']
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace("source.indexOf('function answerValue(')","source.indexOf('function loadMath(')").replace("labels+';'+renderer+'; return markdown;'","source.match(/^function short\\(.*$/m)[0]+';'+labels+';'+renderer+'; return {markdown,answerValue};'").replace('window.render = make(el,marked,romanLists,inlinePrompt,protectMath);','const f=make(el,marked,romanLists,inlinePrompt,protectMath);window.render=f.markdown;window.renderAnswer=f.answerValue;')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
reports=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1000,'height':800})
 page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
 for side in ['stored','escaped-percent-preview']:
  rows=[{'id':c[':db/id'],'type':'text','value':c[':answer/value'] if side=='stored' else c[':answer/value'].replace('%',r'\%')} for c in choices]
  report=page.evaluate(r'''async rows=>{MathJax.typesetClear([content]);content.replaceChildren();for(let row of rows){let n=renderAnswer(row);n.dataset.answerId=row.id;content.append(n)}await MathJax.typesetPromise([content]);return [...content.children].map(n=>({entity:Number(n.dataset.answerId),mathml:[...n.querySelectorAll('mjx-assistive-mml math')].map(m=>m.textContent),percentGlyphs:n.querySelectorAll('svg [data-c="25"]').length,errors:[...n.querySelectorAll('[data-mml-node="merror"]')].map(m=>m.textContent)}))}''',rows)
  reports.append({'variant':side,'answers':report});page.screenshot(path=str(H/f'{side}.png'),full_page=True)
 page.set_content('<div id="source"></div>');page.locator('#source').evaluate('(n,html)=>n.innerHTML=html',captured['html'])
 extraction=page.locator('#source #step-q85526').evaluate((R/'scripts/question_capture/dom.js').read_text())
 browser.close()
server.shutdown()
(H/'current-dom-extraction.json').write_text(json.dumps(extraction,indent=2)+'\n')
source_choices=[{'option':c['option'],'captured_value':c['value'],'source_mathml_contains_percent':'>%<' in c['html']} for c in captured['fields'][0]['choices']]
(H/'source-comparison.json').write_text(json.dumps({'source':str(source.relative_to(R)),'choices':source_choices},indent=2)+'\n')
(H/'render-comparison.json').write_text(json.dumps(reports,indent=2)+'\n')
assert all(not a['errors'] for r in reports for a in r['answers'])
assert sum(a['percentGlyphs'] for a in reports[0]['answers'])==0
assert sum(a['percentGlyphs'] for a in reports[1]['answers'])==4
print(json.dumps(reports,indent=2));print('Current extraction choice values:',[c['value'] for c in extraction['fields'][0]['choices']])
