"""Recover exact formula content from retained SVG MathML and inspected PNGs."""
import json
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from math_format import matrix_tex, normalize_tex

ASSETS = Path('/media/jake/SSD/EDB/math')
images = [x for x in json.loads((ROOT / 'reference/mathacademy/audits/2026-10-16-mth341/images.json').read_text())
          if x['classification'] == 'formula']
svg = [{**x, 'svg': (ASSETS / x['path']).read_text()} for x in images if x['path'].endswith('.svg')]
dom_source = (ROOT / 'scripts/question_capture/dom.js').read_text()
converter = ('const errors=[];' + dom_source[dom_source.index('  const greek ='):dom_source.index('  function render(n)')]
             + '; return {convert:m,errors};')
# Preserve source distinctions the capture extractor intentionally flattens.
# This is an isolated recovery extension; the shared capture code is unchanged.
converter = converter.replace(
    "    return value;\n  }\n  // A system",
    r"""    const variant=n.getAttribute('mathvariant');
    if(variant==='double-struck')value='\\mathbb{'+value+'}';
    else if(variant==='bold')value='\\mathbf{'+value+'}';
    else if(variant)errors.push('Unsupported mathvariant: '+variant);
    if(n.getAttribute('style')==='border: 2px solid Silver')value='\\bbox[2pt,border:2px solid Silver]{'+value+'}';
    return value;
  }
  // A system""")
converter = converter.replace("if (t === 'mphantom') return '';", r"if (t === 'mphantom') return '\\phantom{'+[...n.children].map(child=>m(child)).join('')+'}';")
converter = converter.replace("case 'mo': return ops[n.textContent]", r"case 'mo': if(['{','}'].includes(n.textContent))return '\\'+n.textContent; if(n.textContent==='∗')return '\\ast '; return ops[n.textContent]")
converter = converter.replace("case 'mspace': return '\\\\,';", r"case 'mspace': return ({'2em':'\\qquad ','0.222em':'\\:','0.167em':'\\,'})[n.getAttribute('width')] || '\\,';")

# Each row was transcribed directly from the source pixels in png-sources-0..3.png.
# Preserve source labels, bold vector x, punctuation, and row/column order.
png_specs = [
    ('A=', [[-2,0],[-1,-1],[3,-1],[-2,9]], ''),
    ('C=', [[1,-2,0],[2,1,1]], ''),
    ('A=', [[-3,1,1],[2,0,0],[-1,-2,5]], ''),
    ('A=', [['a','c'],['b','d']], ''),
    ('A=', [[19,2],[r'\sqrt{2}',-1]], ''),
    ('B=', [[1,2,-1],[-1,1,2]], '.'),
    ('CD=', [[-4,1],[-1,4]], '.'),
    (r'A\mathbf{x}=', [[17],[4]], '.'),
    ('D=', [[0],[1],[0]], '.'),
    ('C=', [[2,1,0],[-1,1,-4],[5,4,-2]], ''),
    ('CD=', [[1],[1],[4]], '.'),
    ('B=', [[2,3,-1],[5,2,7],[0,4,6]], '.'),
    (r'I_3\cdot B=B=', [[2,3,-1],[5,2,7],[0,4,6]], '.'),
    ('D=', [[0,1],[2,0],[-3,2]], '.'),
    (r'\mathbf{x}=', [[2],[5]], '.'),
    ('A=', [[1,2],[-2,0],[1,2]], 'paired'),
    ('A=', [[1,3],[7,-2]], ''),
    ('B=', [[-2,-1,1,-1],[1,0,3,8]], '.'),
    (r'\mathbf{x}=', [[3],[2]], '.'),
    (r'\mathbf{x}=', [[1],[-2],[0]], '.'),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome')
    page = browser.new_page()
    recovered = page.evaluate(r'''({records,converter}) => {
      const {convert,errors}=new Function(converter)();
      return records.map(record => {
        errors.length=0;
        const document=new DOMParser().parseFromString(record.svg,'image/svg+xml');
        if(document.querySelector('parsererror')) throw Error(document.querySelector('parsererror').textContent);
        const title=document.querySelector('title');
        const fragments=[];
        const tex=[...title.childNodes].map(node => {
          if(node.nodeType===3)return node.textContent;
          if(node.localName!=='mjx-container')throw Error('Unexpected title child '+node.localName);
          const math=node.querySelector('math');
          if(!math)throw Error('No retained MathML');
          const tables=[...math.querySelectorAll('mtable')].map(table=>({
            rows:[...table.children].map(row=>[...row.children].map(cell=>cell.textContent)),
            columnalign:table.getAttribute('columnalign'),columnlines:table.getAttribute('columnlines'),
            rowlines:table.getAttribute('rowlines'),frame:table.getAttribute('frame')}));
          const styles=[...math.querySelectorAll('[mathbackground],[mathcolor]')].map(n=>({
            text:n.textContent,background:n.getAttribute('mathbackground'),color:n.getAttribute('mathcolor')}));
          const converted=convert(math);
          fragments.push({mathml:new XMLSerializer().serializeToString(math),tex:converted,tables,styles});
          return converted;
        }).join('');
        return {path:record.path,tex,errors:[...errors],fragments,fields:record.fields};
      });
    }''', {'records': svg, 'converter': converter})
    browser.close()

replacements = {}
evidence = []
colored_systems = {
    r'\begin{cases}3x+4y=2 \\ {\color{blue}2x-4y=8}\end{cases}':
    r'\left\{\begin{aligned}3x+4y &=2 \\ {\color{blue}2x-4y} &{\color{blue}=8}\end{aligned}\right.',
    r'\begin{cases}{\color{blue}-2a-8b=-2} \\ 2a+b=-5\end{cases}':
    r'\left\{\begin{aligned}{\color{blue}-2a-8b} &{\color{blue}=-2} \\ 2a+b &=-5\end{aligned}\right.',
    r'\begin{cases}x+2y=1 \\ {\color{blue}-x+y=2}\end{cases}':
    r'\left\{\begin{aligned}x+2y &=1 \\ {\color{blue}-x+y} &{\color{blue}=2}\end{aligned}\right.',
    r'\begin{cases}{\color{red}2u+9v-6=0}\qquad {\color{red}(1)} \\ {\color{blue}2u+6v-8=0}\qquad {\color{blue}(2)}\end{cases}':
    r'\left\{\begin{aligned}{\color{red}2u+9v-6} &{\color{red}=0} && {\color{red}(1)} \\ {\color{blue}2u+6v-8} &{\color{blue}=0} && {\color{blue}(2)}\end{aligned}\right.',
}
for row in recovered:
    assert not row['errors'], row
    row['tex'] = normalize_tex(re.sub(r'\s+', ' ', row['tex']).strip())
    for old,new in colored_systems.items():
        row['tex']=row['tex'].replace(old,new)
    # Keep relation spacing inside the color-scoped right-hand aligned cell.
    row['tex'] = re.sub(r'(&\{\\color\{(?:blue|red)\})(?==)',r'\1{}',row['tex'])
    assert r'\begin{cases}' not in row['tex'], row['path']
    replacements[row['path']] = row['tex']
    evidence.append({**row,'method':'Retained SVG title text plus every assistive MathML fragment; canonical matrix normalization.'})

pngs = [x for x in images if x['path'].endswith('.png')]
assert len(pngs) == len(png_specs) == 20
for i, (row, (label, entries, punctuation)) in enumerate(zip(pngs,png_specs)):
    tex = label + matrix_tex(entries)
    if punctuation == 'paired':
        tex += r',\qquad B=' + matrix_tex([[3,4,-1],[1,-2,2]]) + '?'
    else:
        tex += punctuation
    replacements[row['path']] = tex
    evidence.append({**row,'tex':tex,'method':'Direct source pixel transcription, visually inspected all entries and labels.',
                     'contact_sheet':f'png-sources-{i//5}.png','contact_index':i,'rows':entries,'label':label,
                     'paired_rows':[[3,4,-1],[1,-2,2]] if punctuation=='paired' else None})

assert len(replacements)==105
(HERE / 'replacements.json').write_text(json.dumps(replacements,indent=2)+'\n')
(HERE / 'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(f'Recovered {len(svg)} SVGs and {len(pngs)} PNGs = {len(replacements)} formula assets.')
for row in recovered:
    print(Path(row['path']).stem[:12],row['tex'])
