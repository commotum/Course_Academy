import json
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;S=json.loads((H/'source-records.json').read_text());out=H/'source-screens';out.mkdir(exist_ok=True);checks=[]
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1100,'height':950})
 for e in [17592186060935,17592186061006,17592186107082,17592186116497,17592186121022]:
  s=next(s for s in S if s['entity']==e);html='<html><style>body{width:1000px;padding:24px;font:18px/1.5 serif}mjx-assistive-mml,.MJX_Assistive_MathML,.stepHeader{display:none}svg{overflow:visible;max-width:100%}</style><body>'+s['html']+'</body></html>';page.set_content(html);page.screenshot(path=str(out/(str(e)+'.png')),full_page=True);checks.append({'entity':e,'source_path':s['path'],'raw_svg_count':page.locator('svg').count(),'screen':str(out/(str(e)+'.png'))})
 b.close()
(H/'source-visuals.json').write_text(json.dumps(checks,indent=2));print('source visuals',len(checks))
