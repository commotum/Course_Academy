"""Render all 44 recoveries, compare table row tokens to retained source MathML."""
import functools
import http.server
import json
import re
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
records = json.loads((HERE / 'evidence.json').read_text())
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
    def translate_path(self,path):
        if path.startswith('/images/'):
            return str(Path('/media/jake/SSD/EDB/math') / path.lstrip('/'))
        return super().translate_path(path)

server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
origin=f'http://127.0.0.1:{server.server_port}'
html='''<!doctype html><html><head><meta charset="utf-8"><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><style>body{font:17px Georgia;background:white;color:#182537;margin:20px}article{margin:12px 0;padding:14px;border:1px solid #ccc}.pair{display:flex;align-items:center;justify-content:space-around;gap:30px}.source{max-width:48%;max-height:350px}h3{font:13px monospace;margin:0 0 14px}h4{font:13px sans-serif;color:#555}.recovered{max-width:50%}mjx-container{max-width:100%}</style></head><body><div id="content"></div><script>MathJax.startup.promise.then(()=>window.ready=true)</script></body></html>'''
def canon(value):
    return re.sub(r'\s+','',value).replace('−','-').replace('∗','*').replace('⁡','')

try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome')
        page=browser.new_page(viewport={'width':1600,'height':1100})
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.route('**/*',lambda route:route.fulfill(body=html,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort())
        page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
        results=page.evaluate(r'''async records=>{
          const results=[];
          const rawText=node=>node.kind==='text'?node.getText():node.childNodes.map(rawText).join('');
          for(let index=0;index<records.length;index++){
            const r=records[index],article=document.createElement('article');article.id='r'+index;
            const h=document.createElement('h3');h.textContent=index+': '+r.path;article.append(h);
            const pair=document.createElement('div');pair.className='pair';
            const img=document.createElement('img');img.className='source';img.src='/'+r.path;pair.append(img);
            const recovered=document.createElement('div');recovered.className='recovered';recovered.textContent='$$'+r.tex+'$$';pair.append(recovered);article.append(pair);content.append(article);
            const previous=[...MathJax.startup.document.math].length;
            await MathJax.typesetPromise([recovered]);
            const tables=[];
            for(const item of [...MathJax.startup.document.math].slice(previous))item.root.walkTree(n=>{
              if(n.kind==='mtable')tables.push({rows:n.childNodes.map(row=>row.childNodes.map(cell=>rawText(cell))),columnlines:n.attributes.get('columnlines')});
            });
            results.push({path:r.path,tables,errors:[...recovered.querySelectorAll('[data-mml-node="merror"],[data-mjx-error],[data-mml-node="mtext"][fill="red"]')].map(n=>n.getAttribute('data-mjx-error')||n.textContent)});
          }
          await Promise.all([...document.images].map(i=>i.decode()));
          return results;
        }''',records)
        verification=[]
        failures=[]
        for r,v in zip(records,results):
            expected=[t for f in r.get('fragments',[]) for t in f['tables']]
            issues=[]
            if v['errors']:issues.append({'render_errors':v['errors']})
            if expected:
                if len(expected)!=len(v['tables']):issues.append({'table_count':[len(expected),len(v['tables'])]})
                for old,new in zip(expected,v['tables']):
                    source=[canon(''.join(row)) for row in old['rows']]
                    rendered=[canon(''.join(row)) for row in new['rows']]
                    if source!=rendered:issues.append({'source_rows':source,'rendered_rows':rendered})
                    if old.get('columnlines') and old['columnlines']!=new['columnlines']:
                        issues.append({'source_columnlines':old['columnlines'],'rendered_columnlines':new['columnlines']})
            else:
                expected_shapes=[(len(r['rows']),len(r['rows'][0]))]
                if r['paired_rows']:expected_shapes.append((len(r['paired_rows']),len(r['paired_rows'][0])))
                actual_shapes=[(len(t['rows']),len(t['rows'][0])) for t in v['tables']]
                if expected_shapes!=actual_shapes:issues.append({'expected_shapes':expected_shapes,'actual_shapes':actual_shapes})
            verification.append({**v,'source_table_count':len(expected),'source_row_tokens_match':not issues,'issues':issues})
            if issues:failures.append({'path':r['path'],'issues':issues})
        (HERE/'render-verification.json').write_text(json.dumps({'page_errors':errors,'records':verification,'failures':failures},indent=2)+'\n')
        # Side-by-side source/render evidence, every formula asset, 7 per sheet.
        for start in range(0,len(records),7):
            page.evaluate('(range)=>{for(const a of document.querySelectorAll("article")){const i=Number(a.id.slice(1));a.style.display=i>=range[0]&&i<range[1]?"block":"none"}}',[start,start+7])
            page.screenshot(path=str(HERE/f'comparison-{start//7:02}.png'),full_page=True)
        browser.close()
        print(json.dumps({'rendered':len(results),'page_errors':errors,'failures':failures},indent=2))
        assert not errors and not failures
finally:
    server.shutdown();server.server_close()
