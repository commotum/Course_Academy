import json,sys,re
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT/'capture'))
from scripts.database.math_content import prose
from scripts.database.text import markdown
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from activities import html_to_markdown
source=BeautifulSoup((ROOT/'reference/mathacademy/question-capture/13989257/tutorial-2993.html').read_text(),'html.parser').select('title')[14].find_parent(class_='mjpage')
report={}
with sync_playwright() as p:
 b=p.chromium.launch(headless=True);page=b.new_page();page.route('**/*',lambda route:route.abort())
 page.set_content('<div id="fixture"><div class="questionWidget-text">'+str(source)+'</div></div>')
 item=page.locator('#fixture').evaluate((ROOT/'capture/scripts/browser/extract.js').read_text())
 report['active_extract']={'errors':item['errors'],'newlines':item['problem'].count('\n'),'percent_count':item['problem'].count('%'),'problem':item['problem']}
 try:
  out=prose(item['problem']);report['active_pipeline']={'newlines':out.count('\n'),'percent_count':out.count('%'),'output':out}
 except Exception as e:report['active_pipeline']={'error':str(e)}
 raw=markdown(str(source));report['raw_html_converter']={'newlines':raw.count('\n'),'percent_count':raw.count('%'),'output':raw}
 try:
  out=prose(str(source));report['raw_html_pipeline']={'newlines':out.count('\n'),'percent_count':out.count('%'),'output':out}
 except Exception as e:report['raw_html_pipeline']={'error':str(e)}
 out=html_to_markdown(str(source));report['legacy_html_converter']={'newlines':out.count('\n'),'percent_count':out.count('%'),'output':out}
 b.close()
expected=next(f['tex'] for f in json.loads((HERE.parent/'17592186050407/source/tutorial-formulas.json').read_text())[0]['formulas'] if f['index']==14)
compact=lambda value:re.sub(r'\s+','',value).strip('$')
before=json.loads((HERE/'active-path-before.json').read_text())
checks={
 'active_browser_output_unchanged':report['active_extract']==before['active_extract'],
 'active_markdown_output_unchanged':report['active_pipeline']==before['active_pipeline'],
 'raw_html_all_source_math_preserved':compact(report['raw_html_pipeline']['output'])==compact(expected),
 'legacy_html_all_source_math_preserved':compact(report['legacy_html_converter']['output'])==compact(expected),
 'raw_html_comments_removed_before_collapse':report['raw_html_pipeline']['percent_count']==0,
 'legacy_html_comments_removed_before_collapse':report['legacy_html_converter']['percent_count']==0,
}
assert all(checks.values()),checks
report['checks']=checks
(HERE/'active-path-after.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:{a:b for a,b in v.items() if a not in ('problem','output')} for k,v in report.items()},indent=2))
