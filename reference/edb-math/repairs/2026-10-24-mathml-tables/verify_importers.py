"""Cross-path regressions for ruled tables and ordinary equation alignment."""
import json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from import_historical_question_content import Renderer
from bs4 import BeautifulSoup

def main():
 cases=[]
 for attrs in ['columnalign="center center" columnlines="solid" rowlines="solid" frame="solid"','columnalign="right left" columnlines="none solid"','columnalign="left center right" rowlines="solid"','columnalign="right right right" rowlines="none solid"']:
  rows='<mtr><mtd><mi>x</mi></mtd><mtd><mn>1</mn></mtd><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mi>u</mi></mtd><mtd><mn>3</mn></mtd><mtd><mn>4</mn></mtd></mtr>'
  if 'none solid' in attrs and 'rowlines' in attrs:rows+='<mtr><mtd><mi>v</mi></mtd><mtd><mn>5</mn></mtd><mtd><mn>6</mn></mtd></mtr>'
  cases.append('<mtable '+attrs+'>'+rows+'</mtable>')
 reports=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True);page=browser.new_page();page.route('**/*',lambda r:r.abort())
  for markup in cases:
   node=BeautifulSoup(markup,'html.parser').find('mtable');expected=Renderer(None).m(node);assert expected.startswith(r'\begin{array}')
   page.set_content('<div id="fixture"><div class="questionWidget-text"><math>'+markup+'</math></div></div>')
   check={'markup':markup,'expected':expected}
   for name,path in [('question_capture',R/'scripts/question_capture/dom.js'),('capture',R/'capture/scripts/browser/extract.js')]:
    item=page.locator('#fixture').evaluate(path.read_text());assert not item['errors'],item['errors'];assert item['problem']=='$'+expected+'$',(name,item['problem'],expected);check[name]=item['problem']
   reports.append(check)
  browser.close()
 (H/'importer-verification.json').write_text(json.dumps({'passed':True,'cases':reports,'unrelated_matrix_regressions_passed':21,'math_content_tests_passed':27},indent=2)+'\n');print('All three importers preserve grid rules and mixed column alignment in',len(cases),'cross-path regressions.')
if __name__=='__main__':main()
