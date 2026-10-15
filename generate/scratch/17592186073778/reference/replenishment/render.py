"""Render actual prepared content using the player's Markdown/sanitizer/MathJax."""
import functools,hashlib,http.server,json,sys,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
REVIEW=ROOT/'reference/mathacademy/repairs/2026-10-14-system-equations'
input_file=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051/61879575e632c90fe5ccec930beb4ea063a8d9407e694520a01e8fdd72a7e60e.generated'
instances=json.loads(input_file.read_text())['instances'];records=[]
for r in instances:
    q=r['question']
    text=q[':question/problem']+'\n\n'+'\n\n'.join('$'+a[':answer/value']+'$' for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
    records.append({'id':q[':question/id'],'attribute':'complete-question','value':text})
cached={};pending=records;only=None
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
origin = f'http://127.0.0.1:{server.server_port}'
html = (REVIEW / 'renderer-fixture.html').read_text()
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 810, 'height': 1050})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.route('**/*', lambda route: route.abort() if route.request.resource_type == 'image' else route.fulfill(body=html, content_type='text/html')
                   if route.request.url == origin + '/fixture' else route.continue_()
                   if route.request.url.startswith(origin + '/') else route.abort())
        page.goto(origin + '/fixture')
        page.wait_for_function('window.ready === true', timeout=10000)
        result = page.evaluate(r'''async ({records,batched}) => {
          const results=[];
          for(const record of records) {
            const article=document.createElement('article');
            article.dataset.id=record.id;article.dataset.attribute=record.attribute;
            article.append(render(record.value));content.append(article);
            const previous=[...MathJax.startup.document.math].length;
            await MathJax.typesetPromise([article]);
            const systems=[];
            for(const table of article.querySelectorAll('[data-mml-node="mtable"]')) {
              const brace=[...table.parentElement.children].find(n=>n.dataset.mmlNode==='mo');
              if(!brace?.querySelector('[data-c="7B"],[data-c="23A7"],[data-c="23A8"],[data-c="23A9"]'))continue;
              const equals=[...table.children].filter(n=>n.dataset.mmlNode==='mtr').map(row=>
                (row.children[1]||row).querySelector('use[data-c="3D"],path[data-c="3D"]'))
                .filter(Boolean).map(n=>n.getBoundingClientRect().x);
              if(!equals.length)continue;
              systems.push({equals,braceHeight:brace.getBoundingClientRect().height,
                            tableHeight:table.getBoundingClientRect().height});
            }
            const outside=article.cloneNode(true);
            outside.querySelectorAll('mjx-container,math-field').forEach(n=>n.remove());
            const exposed=outside.textContent.match(/(?<!\\)\$|\\(?:begin|end)\{[^}]+\}/g)||[];
            results.push({id:record.id,attribute:record.attribute,systems,exposed,
              outside_text:exposed.length?outside.textContent:'',
              formulas:[...MathJax.startup.document.math].length-previous,
              errors:[...article.querySelectorAll('[data-mml-node="merror"],mjx-merror')]
                .map(n=>n.getAttribute('data-mjx-error')||n.textContent)});
            if(batched && results.length%25===0) {
              MathJax.typesetClear([content]);content.replaceChildren();
            }
          }
          return results;
        }''', {'records': pending, 'batched': '--lesson-all' not in sys.argv})
        rendered = {(r['id'], r['attribute']): r for r in result}
        result = [cached.get((r['id'], r['attribute'], r['value'])) or rendered[r['id'], r['attribute']] for r in records]
        report = {'records': result, 'page_errors': errors,
                  'input_sha256': hashlib.sha256(input_file.read_bytes()).hexdigest()}
        filename = ('lesson-' if '--lesson-all' in sys.argv else '') + ('committed-' if '--committed' in sys.argv else '') + 'rendering-validation.json'
        if only: filename = 'partial-' + filename
        (HERE / filename).write_text(json.dumps(report, indent=2) + '\n')
        bad = [r for r in result if r['errors'] or r['exposed']]
        if bad:
            page.unroute_all(behavior='wait'); browser.close()
        assert not errors, errors
        assert not bad, [(r['id'], r['attribute'], r['errors'], r['exposed']) for r in bad][:15]
        assert len(result)==len(records)
        systems=[s for r in result for s in r['systems']]
        assert len(systems)==2*len(instances)
        for system in systems:
            assert len(system['equals'])==2
            assert max(system['equals'])-min(system['equals'])<.5
            assert system['braceHeight']>=system['tableHeight']*.9
        for level in ('easy','moderate','hard'):
            record=next(r for r in instances if r['generation']['authored_level']==level)
            page.locator('article[data-id="'+record['question'][':question/id']+'"]').screenshot(path=str(HERE/(level+'-render.png')))
        print('Verified',len(result),'fields and',len(systems),'scalable aligned systems')
        browser.close()
finally:
    server.shutdown();server.server_close()
