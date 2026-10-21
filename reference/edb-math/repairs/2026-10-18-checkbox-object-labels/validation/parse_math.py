"""Read-only fast MathJax parse census of all proposed fields and solutions."""
import asyncio,hashlib,json,re,sys,threading,functools
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
SOURCE=ROOT/'reference/edb-math/repairs/2026-10-18-checkbox-object-labels/mapping/presentation-input.json'
OUT=Path(__file__).resolve().parent/'math-parse';OUT.mkdir(exist_ok=True)
PATTERN=re.compile(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$')
async def main():
    data=json.loads(SOURCE.read_text());formulas={}
    for c in data['cases']:
        q=c['question'];attributes=[(q[':db/id'],k,q.get(k,''))for k in [':question/problem',':question/worked-solution']]
        attributes +=[(f[':db/id'],':answer-field/key',f[':answer-field/key'])for f in q[':question/answer-fields']]
        for eid,attr,value in attributes:
            for match in PATTERN.finditer(value):
                expression=match.group();display=expression.startswith('$$')or expression.startswith(r'\[')
                tex=expression[2:-2]if expression.startswith(('$$',r'\[',r'\('))else expression[1:-1]
                key=(tex,display);formulas.setdefault(key,[]).append({'question':q[':db/id'],'entity':eid,'attribute':attr,'start':match.start(),'expression':expression})
    entries=[{'tex':tex,'display':display,'uses':uses}for(tex,display),uses in formulas.items()]
    class Handler(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    origin='http://127.0.0.1:'+str(server.server_port)
    async with async_playwright()as playwright:
        browser=await playwright.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--no-sandbox','--disable-gpu'])
        page=await browser.new_page();await page.goto(origin+'/ui/')
        await page.route('**/*',lambda route:route.continue_()if route.request.url.startswith(origin+'/')else route.abort())
        await page.add_script_tag(url=origin+'/ui/mathjax-config.js')
        await page.add_script_tag(url=origin+'/ui/vendor/mathjax/tex-svg.js')
        await page.evaluate('MathJax.startup.promise')
        errors=[]
        for offset in range(0,len(entries),100):
            results=await page.evaluate('''async items=>{const results=[];for(const x of items){try{const n=await MathJax.tex2svgPromise(x.tex,{display:x.display});const errors=[...n.querySelectorAll('[data-mjx-error],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent);results.push(errors);}catch(e){results.push([String(e)]);}}return results;}''',entries[offset:offset+100])
            for entry,issues in zip(entries[offset:offset+100],results):
                if issues:errors.append({**entry,'errors':issues})
            if offset%1000==0:print(offset,len(entries),len(errors),flush=True)
        await browser.close()
    server.shutdown();server.server_close()
    report={'questions':len(data['cases']),'unique_formulas':len(entries),'formula_occurrences':sum(len(x['uses'])for x in entries),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'errors':errors,'database_writes':0}
    (OUT/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='errors'}|{'error_formulas':len(errors),'affected_questions':len({u['question']for e in errors for u in e['uses']})}),flush=True)
asyncio.run(main())
