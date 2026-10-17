"""Reconstruct all source tutorial formulas without discarding mixed SVG title fragments."""
import hashlib,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup,NavigableString
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import normalize_tex
SOURCE=ROOT/'reference/mathacademy/question-capture/13989257'
JS=(ROOT/'scripts/question_capture/dom.js').read_text()
records=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True);page=browser.new_page();page.route('**/*',lambda route:route.abort())
 for mid in (2993,2994,4406,4407,5885):
  p=SOURCE/(f'tutorial-{mid}.html' if mid<4000 else f'example-{mid}.json');raw=p.read_text();soup=BeautifulSoup(raw if mid<4000 else json.loads(raw)['html'],'html.parser');formulas=[]
  for i,title in enumerate(soup.select('svg > title')):
   reconstructed=BeautifulSoup(str(title),'html.parser').find('title')
   for fragment in list(reconstructed.select('mjx-container')):
    assert len(fragment.select('math'))==1
    page.set_content('<div id="fixture"><div class="questionWidget-text">'+str(fragment.select_one('math'))+'</div></div>')
    result=page.locator('#fixture').evaluate(JS);assert not result['errors'] and not result['assets'],result
    tex=result['problem'].strip().strip('$').strip();fragment.replace_with(NavigableString(tex))
   text=reconstructed.get_text().strip();comments=re.findall(r'(?m)^\s*%.*$',text)
   text=re.sub(r'(?m)^\s*%.*$','',text)
   tex=normalize_tex(text)
   field='tutorial/content' if mid<4000 else ('question/problem' if title.find_parent(class_='exampleQuestion') else 'question/worked-solution')
   formulas.append({'index':i,'field':field,'tex':tex,'title':str(title),'mathml_fragments':len(title.select('math')),'source_comment_lines_removed':comments})
  records.append({'mid':mid,'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(raw.encode()).hexdigest(),'formulas':formulas})
 browser.close()
(HERE/'tutorial-formulas.json').write_text(json.dumps([r for r in records if r['mid']<4000],indent=2)+'\n')
(HERE/'canonical-formulas.json').write_text(json.dumps([r for r in records if r['mid']>=4000],indent=2)+'\n')
print([(r['mid'],len(r['formulas'])) for r in records])
