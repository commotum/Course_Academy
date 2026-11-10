#!/usr/bin/env python3
"""Check real-player math for scrollbars on expressions that already fit.

Uses only a local fixture and read-only content snapshots. Real wide formulas
must still scroll. With --input, inspect every supplied visible content field.
"""
import argparse
import functools
import http.server
import json
from pathlib import Path
import threading
from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import sync_playwright
from serve_graph_explorer import image_path, DEFAULT_MATH_ROOT, IMAGE_TYPES

ROOT = Path(__file__).resolve().parents[1]


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


def regressions():
    items = []
    for size in [14, 15, 16, 17, 20]:
        for role in ['prose', 'choice', 'feedback']:
            for coords in ['2\\\\6', '3\\\\6', '6\\\\3', '-1\\\\3', '12\\\\-6']:
                items.append(dict(entity=f'vector-{size}-{role}-{coords}', attribute='regression',
                                  value=r'\begin{bmatrix}' + coords + r'\end{bmatrix}',
                                  bare_math=True, role=role, font_size=size))
    items.append(dict(entity='genuinely-wide-inline-formula', attribute='regression', role='prose',
                      value='+'.join('x_{' + str(i) + '}' for i in range(1, 71)),
                      bare_math=True, must_scroll=True))
    return items


SHOW = r'''async items => {
  MathJax.typesetClear([content]); content.replaceChildren();
  for (const f of items) {
    const card=document.createElement('article');card.className='content-card';
    card.dataset.entity=String(f.entity);card.dataset.attribute=f.attribute;
    const prose=render(f.bare_math?'$'+f.value+'$':f.value,'prose',f.fields||[]);
    if(f.font_size)prose.style.fontSize=f.font_size+'px';
    if(f.role==='choice') {
      const field=document.createElement('fieldset');field.className='answer-field';field.dataset.type='radio';
      const choice=document.createElement('label');choice.className='choice';
      const input=document.createElement('input');input.type='radio';input.disabled=true;
      choice.append(input,prose);field.append(choice);card.append(field);
    } else if(f.role==='solution'||f.role==='feedback') {
      const section=document.createElement('section');section.className=f.role==='solution'?'worked-solution':'feedback';
      section.append(prose);card.append(section);
    } else card.append(prose);
    content.append(card);
  }
  await MathJax.typesetPromise([content]);
  return [...content.children].map((card,i)=>{
    const nodes=[...card.querySelectorAll('mjx-container')];
    const scrolls=nodes.flatMap(n=>{
      const svg=n.querySelector(':scope > svg');if(!svg)return [];
      const style=getComputedStyle(n),r=svg.getBoundingClientRect();
      const available=n.clientWidth-parseFloat(style.paddingLeft)-parseFloat(style.paddingRight);
      const over=n.scrollWidth>n.clientWidth;
      return over?[{inline:n.getAttribute('display')!=='true',client:n.clientWidth,scroll:n.scrollWidth,
        svg_width:r.width,available,spurious:r.width<=available+.51,
        text:n.textContent.slice(0,180)}]:[];
    });
    const errors=[...card.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.textContent);
    return {entity:items[i].entity,attribute:items[i].attribute,topics:items[i].topics||[],
      math_nodes:nodes.length,errors,scrolls,
      must_scroll_failed:!!items[i].must_scroll&&!scrolls.some(n=>!n.spurious),
      outer_overflow:card.scrollWidth>card.clientWidth+1};
  });
}'''


def check(items, baseline=False, screenshot_dir=None):
    fixture = (ROOT / 'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
    fixture = fixture.replace('<!doctype html>', '<!doctype html><html data-theme="light"><link rel="stylesheet" href="/ui/navigation.css">')
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    results = []
    screenshots = []
    try:
        with sync_playwright() as runtime:
            browser = runtime.chromium.launch(headless=True)
            page = browser.new_page()

            def route(request):
                u = urlsplit(request.request.url)
                if request.request.url == origin + '/fixture':
                    request.fulfill(body=fixture, content_type='text/html')
                elif u.path == '/api/asset':
                    path = image_path(parse_qs(u.query).get('path', [''])[0], DEFAULT_MATH_ROOT)
                    if path:
                        request.fulfill(body=path.read_bytes(), content_type=IMAGE_TYPES[path.suffix.lower()])
                    else:
                        request.fulfill(status=404, body='Unavailable')
                elif request.request.url.startswith(origin + '/'):
                    request.continue_()
                else:
                    request.abort()

            page.route('**/*', route)
            page.goto(origin + '/fixture')
            page.wait_for_function('window.ready')
            if baseline:
                page.add_style_tag(content='.prose mjx-container:not([display="true"]){padding-inline-end:0}')
            for width in [1100, 390]:
                page.set_viewport_size(dict(width=width, height=1000))
                for offset in range(0, len(items), 24):
                    batch = items[offset:offset + 24]
                    checks = page.evaluate(SHOW, batch)
                    for row in checks:
                        row['width'] = width
                        if screenshot_dir and str(row['entity']) in ['17592186088928', '17592186088149']:
                            screenshot_dir.mkdir(parents=True, exist_ok=True)
                            filename = f'{row["entity"]}-{row["attribute"].replace(":", "").replace("/", "-")}-{width}.png'
                            page.locator(f'article[data-entity="{row["entity"]}"][data-attribute="{row["attribute"]}"]').first.screenshot(path=str(screenshot_dir / filename))
                            screenshots.append(filename)
                        results.append(row)
                print(f'Checked {len(items)} fields at {width}px.', flush=True)
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    failures = [r for r in results if r['errors'] or r['must_scroll_failed']
                or any(n['spurious'] for n in r['scrolls'])]
    return dict(passed=not failures, baseline=baseline, database_writes=0,
                field_layout_checks=len(results), math_nodes=sum(r['math_nodes'] for r in results),
                spurious_scrollbars=sum(n['spurious'] for r in results for n in r['scrolls']),
                genuine_wide_formulas=sum(not n['spurious'] for r in results for n in r['scrolls']),
                failures=failures, checks=results, screenshots=screenshots)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--screenshots', type=Path)
    args = parser.parse_args()
    items = json.loads(args.input.read_text()) if args.input else regressions()
    report = check(items, args.baseline, args.screenshots)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('failures', 'checks', 'screenshots')}, indent=2))
    return int(not report['passed'] and not args.baseline)


if __name__ == '__main__':
    raise SystemExit(main())
