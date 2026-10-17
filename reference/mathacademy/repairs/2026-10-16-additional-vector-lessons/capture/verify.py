"""Verify current extractors preserve every mixed-title formula as a complete asset."""
import hashlib,json
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4]
source=ROOT/'reference/mathacademy/question-capture'
reports=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome')
 context=browser.new_context();context.route('**/*',lambda route:route.abort());page=context.new_page()
 for filename in ('13989257/tutorial-2993.html','13989257/tutorial-2994.html','13979047/tutorial-2990.html','13979047/tutorial-3800.html'):
  raw=(source/filename).read_text();page.set_content(raw)
  selector=page.locator('.step').first
  if not selector.count():raise AssertionError('Source step missing')
  expected=selector.evaluate(r'''e=>[...e.querySelectorAll('svg')].filter(n=>!n.parentElement.closest('svg')).filter(n=>{const t=n.querySelector('title');return t?.querySelector('math')&&[...t.childNodes].some(c=>c.nodeType===3&&c.textContent.trim());}).map(n=>({html:n.outerHTML,math:n.querySelectorAll('title math').length}))''')
  for script in ('capture/scripts/browser/extract.js',):
   parsed=selector.evaluate((ROOT/script).read_text());assert not parsed['errors'],parsed['errors']
   actual=[asset['html'] for asset in parsed['assets']]
   assert all(e['html'] in actual for e in expected)
   # The active capture extractor supports tutorial steps. The older question
   # extractor scans the same intact assets but requires a question prompt node.
   active=script=='capture/scripts/browser/extract.js'
   if active:
    assert all(f'@asset-{asset["index"]}@' in parsed['problem'] for asset in parsed['assets'])
   reports.append({'source':str((source/filename).relative_to(ROOT)),'source_sha256':hashlib.sha256(raw.encode()).hexdigest(),'extractor':script,'extractor_sha256':hashlib.sha256((ROOT/script).read_bytes()).hexdigest(),'complete_mixed_formula_assets':len(expected),'nested_math_fragments_preserved':sum(e['math'] for e in expected),'rendered_tutorial_placeholders_verified':active,'scope':'Full tutorial extraction' if active else 'Legacy asset collection only; tutorial step is not its prompt selector','errors':parsed['errors'],'passed':True})
 browser.close()
summary={'passed':True,'scope':'Current capture extractor on all four retained tutorial documents from the two additional lessons','result':'Every mixed TeX/MathML title is preserved as the complete formula asset; no partial first-matrix extraction. The mixed-title asset check required no browser-extractor change. The separate pure-title HTML comment repair and worker reload are recorded in html-converter-verification.json and workers/after.json.','checks':reports}
(HERE/'verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
