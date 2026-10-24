"""Original source and MathML-token regression across all ingestion converters."""
import json,sys
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from import_historical_question_content import Renderer
sys.path.insert(0,str(R/'scripts/question_capture'));from math_format import normalize_prose,normalize_capture_question
source=R/'reference/mathacademy/capture/linear/14195578/observations/step-q85526-7a7c74f995b9f5aa8ae3.json';record=json.loads(source.read_text());reports=[]
with sync_playwright()as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page();page.route('**/*',lambda route:route.abort())
 for token in ['mi','mo','mtext']:
  m=f'<math><mn>30</mn><{token}>%</{token}></math>';node=BeautifulSoup(m,'html.parser').find('math');legacy=Renderer(None).m(node);assert r'\%'in legacy
  page.set_content('<div id="fixture"><div class="questionWidget-text">30% in prose: '+m+'</div></div>')
  report={'token':token,'python_tex':legacy}
  for name,path in [('question_capture',R/'scripts/question_capture/dom.js'),('capture',R/'capture/scripts/browser/extract.js')]:
   r=page.locator('#fixture').evaluate(path.read_text());assert not r['errors'];assert r'\%'in r['problem'] and r['problem'].startswith('30% in prose:');assert normalize_prose(r['problem']).count(r'\%')==1;report[name]=r['problem']
  reports.append(report)
 page.set_content('<div id="fixture">'+record['html']+'</div>')
 originals=[]
 for name,path in [('question_capture',R/'scripts/question_capture/dom.js'),('capture',R/'capture/scripts/browser/extract.js')]:
  r=page.locator('#step-q85526').evaluate(path.read_text());assert not r['errors'];choices=r['fields'][0]['choices'];assert sum(c['value'].count(r'\%')for c in choices)==4;originals.append({'extractor':name,'values':[c['value']for c in choices]})
 browser.close()
result={'passed':True,'token_cases':reports,'authentic_source':str(source.relative_to(R)),'authentic_capture_results':originals,'plain_prose_percent_unchanged':True,'already_escaped_math_not_double_escaped':True}
(H/'importer-verification.json').write_text(json.dumps(result,indent=2)+'\n');print('All 3 converters preserve literal mi/mo/mtext percentages; both browser extractors preserve all 4 authentic percent choices.')
