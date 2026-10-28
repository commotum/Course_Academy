#!/usr/bin/env python3
"""Read-only actual-player rendering QA with strict undefined-command errors.

Run with the local Playwright Python environment. Input is a JSON list of
{entity, attribute, value, bare_math?} records; output retains every result.
No application API, database write, or learner event is used.
"""
import argparse,functools,http.server,json,sys,threading
from pathlib import Path
from urllib.parse import parse_qs,urlsplit
from playwright.sync_api import sync_playwright
from serve_graph_explorer import image_path,DEFAULT_MATH_ROOT,IMAGE_TYPES
ROOT=Path(__file__).resolve().parents[1]
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def check(items):
    fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
    fixture=fixture.replace('<!doctype html>','<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
    fixture=fixture.replace('<script src="/ui/vendor/mathjax/tex-svg.js">',
        '<script>MathJax.tex.packages=MathJax.tex.packages.filter(name=>name!=="noundefined");</script><script src="/ui/vendor/mathjax/tex-svg.js">')
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();origin=f'http://127.0.0.1:{server.server_port}';out=[]
    try:
        with sync_playwright()as p:
            browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1100,'height':950})
            def route(r):
                u=urlsplit(r.request.url)
                if r.request.url==origin+'/fixture':r.fulfill(body=fixture,content_type='text/html')
                elif u.path=='/api/asset':
                    path=image_path(parse_qs(u.query).get('path',[''])[0],DEFAULT_MATH_ROOT)
                    if path:r.fulfill(body=path.read_bytes(),content_type=IMAGE_TYPES[path.suffix.lower()])
                    else:r.fulfill(status=404,body='Unavailable')
                elif r.request.url.startswith(origin+'/'):r.continue_()
                else:r.abort()
            page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready')
            for offset in range(0,len(items),30):
                batch=items[offset:offset+30]
                checks=page.evaluate('''async fields=>{
                  MathJax.typesetClear([content]);content.replaceChildren();
                  for(const f of fields){let node=render(f.bare_math?'$'+f.value+'$':f.value,'prose',f.fields||[]);content.append(node);}
                  await MathJax.typesetPromise([content]);
                  return [...content.children].map(n=>({
                    errors:[...n.querySelectorAll('[data-mml-node="merror"]')].map(e=>e.getAttribute('data-mjx-error')||e.textContent),
                    raw_display_delimiters:n.textContent.includes('$$'),math_blocks:n.querySelectorAll('mjx-container').length
                  }));}''',batch)
                out.extend({'entity':f.get('entity'),'attribute':f.get('attribute'),**v}for f,v in zip(batch,checks))
            browser.close()
    finally:server.shutdown();server.server_close()
    failures=[v for v in out if v['errors']or v['raw_display_delimiters']]
    return {'passed':not failures,'strict_undefined_commands':True,'actual_player_renderer':True,'fields':len(out),'failures':failures,'checks':out,'database_writes':0}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('input',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args()
    result=check(json.loads(args.input.read_text()));args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(f"Strict actual-renderer checks: {result['fields']} fields; {len(result['failures'])} failures.")
    return int(not result['passed'])
if __name__=='__main__':raise SystemExit(main())
