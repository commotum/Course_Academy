"""Recover full source SVG-title formulas, preserving all MathML fragments."""
import hashlib
import json
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from activities import html_to_markdown
SOURCE=ROOT/'reference/mathacademy/question-capture/13977620'
JS=(ROOT/'scripts/question_capture/dom.js').read_text()
records=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True)
 page=browser.new_page()
 page.route('**/*',lambda route:route.abort())
 for mid in (2987,2988):
  path=SOURCE/f'tutorial-{mid}.html'
  raw=path.read_text();soup=BeautifulSoup(raw,'html.parser')
  formulae=[]
  for node in soup.select('.mjpage'):
   title=node.select_one('svg > title');assert title is not None
   reconstructed=BeautifulSoup(str(title),'html.parser').find('title')
   for fragment in reconstructed.select('mjx-container'):
    assert len(fragment.select('math')) == 1
    page.set_content('<div id="fixture"><div class="questionWidget-text">'+str(fragment.select_one('math'))+'</div></div>')
    result=page.locator('#fixture').evaluate(JS)
    assert not result['errors'] and not result['assets'], result
    value=result['problem'].strip(); assert value[0]=='$' and value[-1]=='$'
    value=value.strip('$').strip()
    fragment.replace_with(NavigableString(value))
   assert not reconstructed.find('math')
   tex=reconstructed.get_text().strip()
   display='mjpage__block' in node.get('class',[])
   formulae.append({'title_index':len(formulae),'original_title':str(title),'reconstructed_tex':tex,'display':display,'mathml_fragments':len(title.select('math'))})
   node.replace_with(NavigableString(('\n\n$$\n'+tex+'\n$$\n\n') if display else ('$'+tex+'$')))
  rendered=html_to_markdown(str(soup))
  (HERE/f'tutorial-{mid}-source-reconstructed.md').write_text(rendered+'\n')
  records.append({'math_academy_id':mid,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(raw.encode()).hexdigest(),'formulas':formulae})
 browser.close()
(HERE/'source-formulas.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k!='formulas'}|{'formula_count':len(r['formulas'])} for r in records],indent=2))
