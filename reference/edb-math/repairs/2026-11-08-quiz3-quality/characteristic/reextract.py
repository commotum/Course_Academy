import json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path('/home/jake/Developer/Course_Academy');base=root/'reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic';extractor=(root/'capture/scripts/browser/extract.js').read_text()
with sync_playwright()as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page();page.route('**/*',lambda r:r.abort())
 for d in base.glob('175*'):
  rows=[]
  for row in json.loads((d/'source-manifest.json').read_text()):
   items=[]
   for source in row['sources']:
    html=source.get('html',source.get('node',''))
    if not html:continue
    page.set_content('<div id="audit-source">'+html+'</div>')
    try:
     extracted=page.locator('#audit-source > *').first.evaluate(extractor);items.append({'path':source['path'],**{k:v for k,v in extracted.items()if k not in ['html','assets']}})
    except Exception as error:items.append({'path':source['path'],'error':str(error)})
   rows.append({'eid':row['eid'],'mid':row['mid'],'extractions':items})
  (d/'source-extractions.json').write_text(json.dumps(rows,indent=2));print(d.name,len(rows),flush=True)
 browser.close()
