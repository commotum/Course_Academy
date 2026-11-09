import json
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=Path('/home/jake/Developer/Course_Academy');extractor=(ROOT/'capture/scripts/browser/extract.js').read_text()
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page();page.route('**/*',lambda r:r.abort())
 for out in sorted(HERE.glob('175*')):
  results=[]
  for row in json.loads((out/'source-manifest.json').read_text()):
   rr={'entity':row['entity'],'mid':row['mid']}
   for role in ['prompt_sources','solution_sources']:
    if not row[role]:continue
    s=next((s for s in row[role]if s['role']=='saved original DOM'),row[role][0]);page.set_content('<div id="audit-source">'+s['html']+'</div>')
    try:rr[role]={'source':s['path'],**{k:v for k,v in page.locator('#audit-source > *').first.evaluate(extractor).items()if k not in ['html','assets']}}
    except Exception as e:rr[role]={'error':str(e)}
   results.append(rr)
  (out/'reextracted.json').write_text(json.dumps(results,indent=2));print(out.name,len(results),flush=True)
 b.close()
