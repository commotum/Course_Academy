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
images = [x for x in json.loads((HERE / 'images.json').read_text())
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

# Each row was transcribed directly from the source pixels in png-sources-2.png.
# Preserve source labels, bold vector x, punctuation, and row/column order.
png_specs = [
    ('B=', [[3,9],[-1,-3]], '.'),
    ('C=', [[r'\frac{1}{2}',0,r'\frac{1}{2}'],[0,1,0],[r'\frac{1}{2}',0,r'\frac{1}{2}']], '.'),
    ('C^5=', [[r'\frac{1}{2}',0,r'\frac{1}{2}'],[0,1,0],[r'\frac{1}{2}',0,r'\frac{1}{2}']], '.'),
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
for row in recovered:
    assert not row['errors'], row
    row['tex'] = normalize_tex(re.sub(r'\s+', ' ', row['tex']).strip())
    # Keep relation spacing inside the color-scoped right-hand aligned cell.
    row['tex'] = re.sub(r'(&\{\\color\{(?:blue|red)\})(?==)',r'\1{}',row['tex'])
    # All aligned linear systems are normalized by shared format code.
    replacements[row['path']] = row['tex']
    evidence.append({**row,'method':'Retained SVG title text plus every assistive MathML fragment; canonical matrix normalization.'})

pngs = [x for x in images if x['path'].endswith('.png')]
assert len(pngs) == len(png_specs) == 3
for i, (row, (label, entries, punctuation)) in enumerate(zip(pngs,png_specs)):
    tex = label + matrix_tex(entries)
    tex += punctuation
    replacements[row['path']] = tex
    evidence.append({**row,'tex':tex,'method':'Direct source pixel transcription, visually inspected all entries and labels.',
                     'contact_sheet':'png-sources-2.png','contact_index':i,'rows':entries,'label':label,
                     'paired_rows':None})

assert len(replacements)==44
(HERE / 'replacements.json').write_text(json.dumps(replacements,indent=2)+'\n')
(HERE / 'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(f'Recovered {len(svg)} SVGs and {len(pngs)} PNGs = {len(replacements)} formula assets.')
for row in recovered:
    print(Path(row['path']).stem[:12],row['tex'])
