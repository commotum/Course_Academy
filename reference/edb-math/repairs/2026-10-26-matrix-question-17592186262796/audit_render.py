import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
questions=json.loads((H/'questions.json').read_text());activities=json.loads((H/'activities.json').read_text());fields=[]
for q in questions:
 for a in ['question/problem','question/worked-solution']:
  if ':'+a in q:fields.append({'entity':q[':db/id'],'attribute':a,'value':q[':'+a]})
 for f in q.get(':question/answer-fields',[]):
  for ans in f.get(':answer-field/choices',[]):
   if ':answer/value'in ans:fields.append({'entity':ans[':db/id'],'attribute':'answer/value','value':('$'+ans[':answer/value']+'$')if ans.get(':answer/type',{}).get(':db/ident')==':answer.type/math'and'$'not in ans[':answer/value']else ans[':answer/value']})
for row in activities:
 for s in row[0].get(':activity/steps',[]):
  c=s[':step/content']
  for a in ['tutorial/content','multistep/content']:
   if ':'+a in c:fields.append({'entity':c[':db/id'],'attribute':a,'value':c[':'+a]})
fields=list({(f['entity'],f['attribute']):f for f in fields}.values());(H/'audited-fields.json').write_text(json.dumps(fields,indent=2)+'\n')
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';checks=[];errors=[]
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1050,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)));page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
 for start in range(0,len(fields),20):
  checks.extend(page.evaluate('''async fields=>{const out=[];for(const f of fields){MathJax.typesetClear([content]);const n=render(f.value);content.replaceChildren(n);await MathJax.typesetPromise([n]);out.push({entity:f.entity,attribute:f.attribute,errors:[...n.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),math:[...MathJax.startup.document.math].filter(m=>n.contains(m.typesetRoot)).map(m=>m.math),tables:[...n.querySelectorAll('svg [data-mml-node="mtable"]')].map(t=>({rows:[...t.children].filter(n=>['mtr','mlabeledtr'].includes(n.getAttribute('data-mml-node'))).map(r=>r.children.length),text:t.textContent}))});}return out;}''',fields[start:start+20]))
 target=next(f for f in fields if f['entity']==17592186262796 and f['attribute']=='question/problem');page.evaluate('''async value=>{MathJax.typesetClear([content]);content.replaceChildren(render(value));await MathJax.typesetPromise([content]);}''',target['value']);page.locator('#content').screenshot(path=str(H/'target-before.png'));b.close()
server.shutdown();(H/'initial-render.json').write_text(json.dumps({'fields':len(fields),'checks':checks,'page_errors':errors},indent=2)+'\n');print('Rendered',len(fields),'fields');print('Errors',[(r['entity'],r['attribute'],r['errors'])for r in checks if r['errors']]);print('target',next(r for r in checks if r['entity']==17592186262796 and r['attribute']=='question/problem'))
