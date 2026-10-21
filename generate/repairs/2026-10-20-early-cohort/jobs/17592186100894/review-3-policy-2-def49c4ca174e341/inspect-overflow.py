"""Supplement the actual UI renderer with horizontal-scroll observations."""
from pathlib import Path
import importlib.util,json,sys
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent
path=Path('/home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py')
spec=importlib.util.spec_from_file_location('actual_renderer',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
extra="""
      const overflow = await page.evaluate(() => [...document.querySelectorAll('mjx-container[display="true"]')].filter(n=>n.scrollWidth>n.clientWidth+1).map(n=>{
        const before=n.scrollLeft; n.scrollLeft=n.scrollWidth;
        return {clientWidth:n.clientWidth,scrollWidth:n.scrollWidth,overflowX:getComputedStyle(n).overflowX,before,after:n.scrollLeft,reachable:n.scrollLeft>=n.scrollWidth-n.clientWidth-1};
      }));
"""
m.BROWSER_SCRIPT=m.BROWSER_SCRIPT.replace('      const state = await page.evaluate(',extra+'      const state = await page.evaluate(').replace('state.index=index;', 'state.horizontalMath=overflow; state.index=index;')
rs=json.loads((E/'render-current-records.json').read_text())
m.render([rs[1],rs[4]],E/'render-scroll',[E])
r=json.loads((E/'render-scroll/rendering.json').read_text())
assert r['passed'] and all(c['horizontalMath'] for c in r['cases'])
assert all(o['reachable'] and o['overflowX']=='auto' for c in r['cases'] for o in c['horizontalMath'])
(E/'overflow-inspection.json').write_text(json.dumps({'passed':True,'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python inspect-overflow.py','records':'render-current-records.json indices 1 and 4','observations':[c['horizontalMath'] for c in r['cases']],'conclusion':'Long aligned derivations use the actual UI horizontal scrolling contract; rightmost terms are reachable. This is not missing content.'},indent=2))
