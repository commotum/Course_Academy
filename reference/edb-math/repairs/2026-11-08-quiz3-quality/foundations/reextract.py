import json
from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/foundations');ex=Path('capture/scripts/browser/extract.js').read_text()
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page();page.route('**/*',lambda r:r.abort())
 for d in sorted(out.glob('175*')):
  results=[]
  for r in json.loads((d/'source-manifest.json').read_text()):
   x={'entity':r['entity'],'mid':r['mid']}
   for role in ['prompt_sources','solution_sources']:
    ss=r[role]
    if not ss:continue
    s=next((s for s in ss if s['path'].endswith('-before.json')),next((s for s in ss if s['role']=='saved DOM'),ss[0]))
    page.set_content('<div id="audit-source">'+s['html']+'</div>')
    try:
     value=page.locator('#audit-source > *').first.evaluate(ex)
     x[role]={'source':s['path'],**{k:v for k,v in value.items()if k not in ['html','assets']}}
    except Exception as e:x[role]={'source':s['path'],'error':str(e)}
   results.append(x)
  (d/'reextracted.json').write_text(json.dumps(results,indent=2));print(d.name,len(results),flush=True)
 b.close()
