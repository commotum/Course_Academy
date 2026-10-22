"""Instrument the shared actual-UI renderer to verify wide math is reachable."""
import importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parents[1];E=W/'evidence'
s=importlib.util.spec_from_file_location('actual_renderer','/home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.BROWSER_SCRIPT=m.BROWSER_SCRIPT.replace('const stem = config.output', '''state.horizontalScroll=await page.evaluate(() => [...document.querySelectorAll('mjx-container[display="true"]')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>{const before=e.scrollLeft;e.scrollLeft=e.scrollWidth;return {scrollWidth:e.scrollWidth,clientWidth:e.clientWidth,before,after:e.scrollLeft,overflowX:getComputedStyle(e).overflowX,text:e.textContent};}));
      const stem = config.output''')
records=json.loads((E/'render-records.json').read_text())[6:8]
m.render(records,E/'render-scroll',[])
report=json.loads((E/'render-scroll/rendering.json').read_text())
checks=[c for r in report['cases'] for c in r['horizontalScroll']]
assert checks and all(c['overflowX']=='auto' and c['after']>0 for c in checks)
(E/'scroll-results.json').write_text(json.dumps({'passed':True,'cases':checks,'method':'Same shared renderer and unmodified actual UI. Only added geometry/scroll observation; no custom math stack.'},indent=2)+'\n')
print('Wide solution equations scroll to their rightmost content in both cases.')
