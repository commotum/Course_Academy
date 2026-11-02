import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from generate.pipeline import render_preview as r
mode=sys.argv[1];rows=[r for r in json.loads((H/'render-input.json').read_text()) if r['question'][':db/id'] in (17592186233915,17592186315109)]
if mode.startswith('phone'):r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace('width:1280,height:1000','width:390,height:844')
if 'active' in mode:r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace("config.origin + '/learn?activityId=' + index,", "config.origin + '/learn?activityId=' + index + '-active',")
r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace('state.index=index;',"state.fractions=await page.locator('.answer-fraction').evaluateAll(nodes=>nodes.map(n=>({numeratorBottom:n.querySelector('.answer-fraction-numerator').getBoundingClientRect().bottom,denominatorTop:n.querySelector('.answer-fraction-denominator').getBoundingClientRect().top,bar:getComputedStyle(n.querySelector('.answer-fraction-denominator')).borderTopWidth,fields:[...n.querySelectorAll('[data-field-key]')].map(f=>({key:f.dataset.fieldKey,position:f.closest('.answer-fraction-numerator')?'numerator':'denominator',mounted:!!f.querySelector('math-field,.answer-saved-value')}))})));state.index=index;")
r.render(rows,H/('render-'+mode),[])
