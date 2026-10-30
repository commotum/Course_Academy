import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from generate.pipeline import render_preview as r
rows=json.loads((H/'candidate-pool.json').read_text());mode=sys.argv[1]
if mode=='phone':
    easy=min(rows[:5],key=lambda r:r['generation']['plot_plan']['narrow_unit_pixels'])
    rows=[easy,rows[5],rows[10]]
    r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace('width:1280,height:1000','width:390,height:844')
r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace('state.index=index;',"state.imageSizes=await page.locator('.answer-field img').evaluateAll(nodes=>nodes.map(n=>({src:n.getAttribute('src'),width:n.getBoundingClientRect().width,height:n.getBoundingClientRect().height,naturalWidth:n.naturalWidth})));state.index=index;")
r.render(rows,H/('render-'+mode),[H/'assets',ROOT,Path('/media/jake/SSD/EDB/math')])
