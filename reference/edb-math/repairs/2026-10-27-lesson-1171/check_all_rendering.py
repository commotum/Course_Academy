import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text().replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">');fixture+='''<script type="module">import {blankInput,mountInlineFields,loadMathInputs} from '/ui/question-fields.js';window.controls={blankInput,mountInlineFields,loadMathInputs};</script>'''
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';D=json.loads((H/'proposed.json').read_text());shapes={d['entity']:d['shape']for d in json.loads((H/'math-audit.json').read_text())};out=[];interactions=[];screens=H/'screens';screens.mkdir(exist_ok=True)
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':950});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready&&window.controls')
 def check(e,a,v,fields=None):
  r=page.evaluate('''async ({value,fields})=>{await controls.loadMathInputs();MathJax.typesetClear([content]);const n=render(value,'prose',fields||[]),list=document.createElement('div');content.replaceChildren(n,list);if(fields?.length)controls.mountInlineFields(n,list,fields,f=>{let x=document.createElement('fieldset');x.append(controls.blankInput(f,f.key,f.id));return x;});await MathJax.typesetPromise([n]);await document.fonts.ready;return {errors:[...n.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error')),math:[...MathJax.startup.document.math].filter(m=>n.contains(m.typesetRoot)).map(m=>m.math),rawDelimiters:n.textContent.includes('$$'),images:[...n.querySelectorAll('img')].map(n=>n.getAttribute('src')),rows:[...n.querySelectorAll('.matrix-answer tr')].map(tr=>[...tr.querySelectorAll('[data-field-key]')].map(c=>({key:c.dataset.fieldKey,id:c.querySelector('math-field')?.getAttribute('name'),x:c.getBoundingClientRect().x}))),outside:list.childElementCount};}''',{'value':v,'fields':fields});r.update({'entity':e,'attribute':a});assert not r['errors']and not r['rawDelimiters'],(e,a,r['errors']);out.append(r);return r
 for act in D['structure']:
  for s in act[':activity/steps']:
   c=s[':step/content']
   if':tutorial/content'in c:check(c[':db/id'],'tutorial/content',c[':tutorial/content']);page.locator('#content').screenshot(path=str(screens/(str(c[':db/id'])+'.png')))
 for q in D['questions']:
  fs=q.get(':question/answer-fields',[]);blank=bool(fs and fs[0][':answer-field/type'][':db/ident']==':answer-field.type/blank');fields=[{'id':f[':db/id'],'key':f[':answer-field/key'],'type':'blank','answerType':'math'}for f in fs]if blank else[]
  r=check(q[':db/id'],'question/problem',q[':question/problem'],fields)
  if blank:
   nr,nc=shapes[q[':db/id']];assert len(r['rows'])==nr and all(len(row)==nc for row in r['rows'])and not r['outside'];assert {c['key']:c['id']for row in r['rows']for c in row}=={f['key']:str(f['id'])for f in fields}
   for col in range(nc):assert max(row[col]['x']for row in r['rows'])-min(row[col]['x']for row in r['rows'])<1
   page.locator('#content').screenshot(path=str(screens/(str(q[':db/id'])+'.png')));page.set_viewport_size({'width':390,'height':900});assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),q[':db/id'];page.set_viewport_size({'width':1100,'height':950});interactions.append({'entity':q[':db/id'],'shape':[nr,nc],'field_ids_verified':True,'column_alignment_verified':True,'mobile_overflow':False})
  if q.get(':question/worked-solution'):check(q[':db/id'],'question/worked-solution',q[':question/worked-solution'])
  for f in fs:
   for a in f.get(':answer-field/choices',[]):
    v=a[':answer/value'];kind=a[':answer/type'][':db/ident'];v=('$'+v+'$')if kind==':answer.type/math'and not v.lstrip().startswith('$')else v;check(a[':db/id'],'answer/value',v)
    if a.get(':answer/feedback'):check(a[':db/id'],'answer/feedback',a[':answer/feedback'])
 b.close()
server.shutdown();report={'passed':True,'content_items':len(out),'questions':len(D['questions']),'tutorials':3,'interactive_matrix_questions':len(interactions),'checks':out,'interactive_checks':interactions};(H/'all-rendering.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k not in {'checks','interactive_checks'}})
