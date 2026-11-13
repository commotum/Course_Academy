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
   assistiveStyle:a?Object.fromEntries(['position','width','height','clip','padding','overflow','display'].map(k=>[k,getComputedStyle(a)[k]])):null,
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
        'bounded-assistive': 'mjx-container[jax="SVG"] > mjx-assistive-mml {width:1px!important;height:1px!important;padding:0!important}',
        'svg-clip': '.prose mjx-container > svg {overflow:hidden!important}',
        'no-choice-svg-shrink': '.choice .prose mjx-container > svg {max-width:none!important}',
        'display-edge-padding': '.prose mjx-container[display="true"] {padding-inline:.3em}',
        'display-intrinsic': '.prose mjx-container[display="true"] {width:fit-content;margin-inline:auto}',
        'no-inline-allowance': '.prose mjx-container:not([display="true"]) {padding-inline-end:0}',
        'bounded-without-allowance': 'mjx-container[jax="SVG"] > mjx-assistive-mml {width:1px!important;height:1px!important;padding:0!important}.prose mjx-container:not([display="true"]) {padding-inline-end:0}',
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
            const solution=document.createElement('details');solution.className='worked-solution';
            const summary=document.createElement('summary');summary.textContent='Solution:';solution.append(summary);
            for(const f of r.fields)if(f.correctAnswer){const a=f.correctAnswer;solution.append(render(a.type==='math'?'$'+a.value+'$':a.value));}
            solution.append(render(r.solution));article.append(solution);content.append(article);
          }
          await MathJax.typesetPromise([content]);
          for(const solution of content.querySelectorAll('details'))solution.open=true;
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
        # Exercise the integration boundary independently of either question.
        formulas = [
            r'\left\{\begin{aligned}x &=-2t \\ y &=3t \\ z &=-t\end{aligned}\right.',
            r'\left\{\begin{aligned}x &=t \\ y &=-t \\ z &=2t\end{aligned}\right.',
            r'\begin{bmatrix}2\\6\end{bmatrix}',
            r'\gamma,', r'\frac{1}{1+x^2}',
            '+'.join('x_{'+str(i)+'}' for i in range(1,71)),
        ]
        cases=[dict(formula=f,wide=i==5,role=role,size=size,display=display)
               for i,f in enumerate(formulas) for role in ['prose','choice','solution']
               for size in [14,15,17,24,30] for display in [False,True]]
        page.evaluate('''async cases=>{
          MathJax.typesetClear([content]);content.replaceChildren();
          for(const [i,c] of cases.entries()){
            const article=document.createElement('article');article.className='content-card';article.dataset.entity=i;
            const prose=render((c.display?'$$':'$')+c.formula+(c.display?'$$':'$'));
            prose.style.setProperty('font-size',c.size+'px','important');
            if(c.role==='choice'){
              const field=document.createElement('fieldset');field.className='answer-field';field.dataset.type='radio';
              const label=document.createElement('label');label.className='choice';const input=document.createElement('input');input.type='radio';
              label.append(input,prose);field.append(label);article.append(field);
            }else if(c.role==='solution'){
              const section=document.createElement('section');section.className='worked-solution';section.append(prose);article.append(section);
            }else article.append(prose);
            content.append(article);
          }await MathJax.typesetPromise([content]);
        }''',cases)
        matrix=[]
        for width in [1100,390]:
            page.set_viewport_size({'width':width,'height':1000})
            for variant in ['current','bounded-assistive','no-inline-allowance','bounded-without-allowance']:
                page.evaluate('css=>document.querySelector("#experiment").textContent=css',variants[variant])
                rows=page.evaluate('''()=>[...content.children].map(article=>{
                  const n=article.querySelector('mjx-container'),svg=n.querySelector('svg'),a=n.querySelector('mjx-assistive-mml');
                  const s=getComputedStyle(n);n.scrollLeft=1e6;const range=n.scrollLeft;n.scrollLeft=0;
                  return {index:Number(article.dataset.entity),range,client:n.clientWidth,scroll:n.scrollWidth,
                    svg:svg.getBoundingClientRect().width,accessible:!!a?.querySelector('math'),
                    assistiveWidth:a?.getBoundingClientRect().width,
                    falseOverflow:range>0&&svg.getBoundingClientRect().width<=n.clientWidth,
                    errors:article.querySelectorAll('[data-mml-node="merror"]').length};
                })''')
                failures=[dict(case=cases[r['index']],measurement=r) for r in rows if r['falseOverflow'] or r['errors'] or (cases[r['index']]['wide'] and not r['range']) or not r['accessible']]
                summary=dict(width=width,variant=variant,cases=len(rows),falseOverflow=sum(r['falseOverflow'] for r in rows),
                             wideScrolling=sum(bool(r['range']) for r in rows if cases[r['index']]['wide']),
                             accessible=sum(r['accessible'] for r in rows),errors=sum(r['errors'] for r in rows),failures=failures)
                matrix.append(summary)
                print('matrix',width,variant,{k:v for k,v in summary.items() if k!='failures'},flush=True)
        (HERE/'boundary-regressions.json').write_text(json.dumps(matrix,indent=2)+'\n')
        assert all(not r['failures'] for r in matrix if r['variant']=='bounded-assistive')
        browser.close()
    server.shutdown()

if __name__=='__main__':
    main()
