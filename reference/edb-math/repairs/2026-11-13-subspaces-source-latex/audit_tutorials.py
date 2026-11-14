"""Compare all tutorial formula glyphs, font variants, colors and matrix shapes."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from bs4 import BeautifulSoup, NavigableString
from import_historical_question_content import Renderer
from question_capture.math_format import normalize_source_tex
from playwright.sync_api import sync_playwright


def tutorials(value):
    if isinstance(value, dict):
        if ':tutorial/content' in value:
            yield value
        for child in value.values():
            yield from tutorials(child)
    elif isinstance(value, list):
        for child in value:
            yield from tutorials(child)


class SourceRenderer(Renderer):
    def math_node(self, node):
        if getattr(node, 'name', None) == 'mspace':
            space = {'1em': r'\quad ', '2em': r'\qquad '}.get(node.get('width'))
            if space:
                return space
        return super().math_node(node)


snapshot = json.loads((HERE / 'snapshot.json').read_text())
capture = json.loads((ROOT / 'reference/mathacademy/capture/differential/14246322/content.json').read_text())
renderer = SourceRenderer(None)
records = []
for tutorial in tutorials(snapshot):
    source = next(t for t in capture['tutorials'] if int(t['math_academy_id']) == tutorial[':tutorial/math-academy-id'])
    original = []
    for title in BeautifulSoup(source['html'], 'html.parser').select('svg > title'):
        # Python's HTMLParser versions differ in treating title as raw text.
        # These historic captures really contain MathJax DOM inside SVG titles.
        fragment = BeautifulSoup(title.decode_contents(formatter=None), 'html.parser')
        parts = []
        for child in fragment.children:
            if isinstance(child, NavigableString):
                parts.append(str(child))
            else:
                assert child.name == 'mjx-container' and child.find('math')
                parts.append(renderer.m(child.find('math')))
        original.append(normalize_source_tex(''.join(parts).strip()))
    current = [a or b for a, b in re.findall(r'\$\$([\s\S]*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$', tutorial[':tutorial/content'])]
    assert len(current) == len(original)
    path = Path(source['html_path'])
    records.append({'entity': tutorial[':db/id'], 'source': str(path.relative_to(ROOT)),
                    'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'original_formulas': original, 'current_formulas': current})
assert not renderer.errors, renderer.errors

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://127.0.0.1:8765')
    page.add_script_tag(url='http://127.0.0.1:8765/ui/mathjax-config.js')
    page.evaluate('MathJax.tex.packages=MathJax.tex.packages.filter(n=>n!=="noundefined")')
    page.add_script_tag(url='http://127.0.0.1:8765/ui/vendor/mathjax/tex-svg.js')
    page.evaluate('MathJax.startup.promise')
    for record in records:
        checks = page.evaluate('''async record => {
          const fingerprint=async tex=>{
            const node=await MathJax.tex2svgPromise(tex,{display:true});
            document.body.append(node);
            const result={
              errors:[...node.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.textContent),
              glyphs:[...node.querySelectorAll('svg [data-c]')].map(n=>[n.getAttribute('data-c'),getComputedStyle(n).fill]),
              matrices:[...node.querySelectorAll('[data-mml-node="mtable"]')].map(n=>[...n.querySelectorAll(':scope > g > [data-mml-node="mtr"], :scope > [data-mml-node="mtr"]')].map(row=>row.querySelectorAll(':scope > [data-mml-node="mtd"]').length))
            };
            node.remove();return result;
          };
          const out=[];
          for(let i=0;i<record.original_formulas.length;i++){
            const original=await fingerprint(record.original_formulas[i]);
            const current=await fingerprint(record.current_formulas[i]);
            out.push({formula:i,passed:!original.errors.length&&!current.errors.length&&JSON.stringify(original)===JSON.stringify(current),original,current});
          }
          return out;
        }''', record)
        record['checks'] = checks
        record['passed'] = all(check['passed'] for check in checks)
    browser.close()
result = {'passed': all(r['passed'] for r in records), 'tutorials': len(records),
          'formulas_checked': sum(len(r['checks']) for r in records),
          'comparison': 'Rendered glyph identities (including font variants), inherited color and matrix row/cell structure; equivalent TeX grouping and matrix notation accepted.',
          'records': records}
(HERE / 'tutorial-audit.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'passed': result['passed'], 'tutorials': result['tutorials'], 'formulas': result['formulas_checked'],
                  'failures': [{'entity': r['entity'], 'formula': c['formula']} for r in records for c in r['checks'] if not c['passed']]}))
assert result['passed']
