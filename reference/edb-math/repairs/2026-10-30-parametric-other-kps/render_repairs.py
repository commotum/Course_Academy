import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from generate.pipeline import render_preview as r
rows=json.loads((H/'repair-render-input.json').read_text());mode=sys.argv[1]
if mode=='phone':r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace('width:1280,height:1000','width:390,height:844')
r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace('state.index=index;',"state.tableWidths=await page.locator('.lesson-content table').evaluateAll(nodes=>nodes.map(n=>({width:n.getBoundingClientRect().width,scrollWidth:n.scrollWidth,clientWidth:n.clientWidth})));state.index=index;")
r.render(rows,H/('repaired-'+mode),[])
