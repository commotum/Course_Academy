"""Observe current long solution equations in the shared, unmodified UI."""
import importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('actual_renderer','/home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
needle='const stem = config.output'
assert needle in m.BROWSER_SCRIPT
m.BROWSER_SCRIPT=m.BROWSER_SCRIPT.replace(needle,'''state.horizontalScroll=await page.evaluate(() => [...document.querySelectorAll('mjx-container[display="true"]')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>{const before=e.scrollLeft;e.scrollLeft=e.scrollWidth;return {scrollWidth:e.scrollWidth,clientWidth:e.clientWidth,before,after:e.scrollLeft,overflowX:getComputedStyle(e).overflowX,text:e.textContent};}));
      const stem = config.output''')
rs=json.loads((E/'render-records.json').read_text());records=[rs[i] for i in [12,15]]
(E/'scroll-records.json').write_text(json.dumps(records,indent=2)+'\n');m.render(records,E/'render-scroll',[])
r=json.loads((E/'render-scroll/rendering.json').read_text());checks=[c for row in r['cases'] for c in row['horizontalScroll']]
assert r['passed'] and checks and all(c['overflowX']=='auto' and c['after']>0 for c in checks)
(E/'scroll-results.json').write_text(json.dumps({'passed':True,'cases':checks,'method':'Only geometry and scroll observation injected into shared renderer; actual UI, MathJax, question controls and solutions unmodified. Source q-79350 five-component three-parameter expansion and controlled four-component case inspected.'},indent=2)+'\n')
print(json.dumps({'scrollable_cases':len(checks),'passed':True}))
