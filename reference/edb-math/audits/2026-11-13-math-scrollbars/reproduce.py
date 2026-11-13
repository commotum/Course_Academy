"""Read-only layout experiments using current player renderer and local assets."""
import functools
import http.server
import json
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

MEASURE = r'''() => [...content.querySelectorAll('mjx-container, .choice .prose, .worked-solution > .prose')].map(n => {
 const rect=e=>e?.getBoundingClientRect().toJSON();
 const svg=n.querySelector('svg'), a=n.querySelector('mjx-assistive-mml'), s=getComputedStyle(n);
 n.scrollLeft=10000;const range=n.scrollLeft;n.scrollLeft=0;
 return {tag:n.tagName,display:n.getAttribute('display'),class:n.className,
   choice:n.closest('.choice')?.dataset.choice,entity:n.closest('article').dataset.entity,
   client:n.clientWidth,scroll:n.scrollWidth,range,overflow:s.overflowX,
   rect:rect(n),svg:rect(svg),assistive:rect(a),
   svgAttributes:svg?Object.fromEntries([...svg.attributes].map(a=>[a.name,a.value])):null,
   html:n.outerHTML.slice(0,1200)};
})'''

def main():
    fixture = (ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
    fixture = fixture.replace('<!doctype html>', '<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
    records = json.loads((HERE/'reported-questions.json').read_text())['steps']
    server = http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    origin=f'http://127.0.0.1:{server.server_port}'
    variants = {
        'current': '',
        'no-assistive-layout': 'mjx-assistive-mml {display:none!important}',
        'bounded-assistive': 'mjx-assistive-mml {width:1px!important;height:1px!important}',
        'svg-clip': '.prose mjx-container > svg {overflow:hidden!important}',
        'no-choice-svg-shrink': '.choice .prose mjx-container > svg {max-width:none!important}',
        'display-edge-padding': '.prose mjx-container[display="true"] {padding-inline:.3em}',
        'display-intrinsic': '.prose mjx-container[display="true"] {width:fit-content;margin-inline:auto}',
    }
    reports=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,ignore_default_args=['--hide-scrollbars'])
        page=browser.new_page(viewport={'width':1100,'height':1000})
        page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html') if r.request.url==origin+'/fixture' else r.continue_() if r.request.url.startswith(origin+'/') else r.abort())
        page.goto(origin+'/fixture');page.wait_for_function('window.ready')
        page.evaluate('''async records=>{
          for(const r of records){
            const article=document.createElement('article');article.className='content-card';article.dataset.entity=r.contentId;
            article.append(render(r.markdown,'prose',r.fields));
            for(const f of r.fields){if(f.type!=='radio')continue;
              const field=document.createElement('fieldset');field.className='answer-field';field.dataset.type=f.type;
              for(const c of f.choices){const label=document.createElement('label');label.className='choice';label.dataset.choice=c.id;
                const input=document.createElement('input');input.type='radio';
                label.append(input,render(c.type==='math'?'$'+c.value+'$':c.value));field.append(label);
              }article.append(field);
            }
            const solution=document.createElement('section');solution.className='worked-solution';solution.append(render(r.solution));article.append(solution);content.append(article);
          }
          await MathJax.typesetPromise([content]);
          const style=document.createElement('style');style.id='experiment';document.head.append(style);
        }''', records)
        for width in [1100,768,390]:
            page.set_viewport_size({'width':width,'height':1000})
            for name,css in variants.items():
                page.evaluate('css=>document.querySelector("#experiment").textContent=css',css)
                rows=page.evaluate(MEASURE)
                reports.append(dict(width=width,variant=name,nodes=rows))
                print(width,name,[(r['entity'],r['tag'],r['choice'],r['client'],r['scroll'],r['range'],round(r['svg']['width'],2) if r['svg'] else None) for r in rows if r['range']],flush=True)
                if name=='current':page.screenshot(path=str(HERE/f'current-{width}.png'),full_page=True)
        (HERE/'measurements.json').write_text(json.dumps(reports,indent=2)+'\n')
        (HERE/'rendered.html').write_text(page.content())
        browser.close()
    server.shutdown()

if __name__=='__main__':
    main()
