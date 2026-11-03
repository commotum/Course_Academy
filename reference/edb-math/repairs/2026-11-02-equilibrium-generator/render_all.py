"""Render final generated stock and the repaired historical solution."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
import generate.pipeline.render_preview as r

rows=json.loads((H/'candidate-pool.json').read_text())+json.loads((H/'reported-question-repaired.json').read_text())
r.VISIBLE_DOM_AUDIT=r.VISIBLE_DOM_AUDIT.replace('fonts:document.fonts.status', '''
        overflowingMath:[...root.querySelectorAll('mjx-container[display="true"]')]
          .filter(node=>node.querySelector('svg')?.getBoundingClientRect().width > node.clientWidth+2)
          .map(node=>({math:node.textContent,width:node.querySelector('svg').getBoundingClientRect().width,available:node.clientWidth})),
        fonts:document.fonts.status''')
base=r.BROWSER_SCRIPT
for mode in ('desktop','phone','phone-active'):
    r.BROWSER_SCRIPT=base
    if mode!='desktop':r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace('width:1280,height:1000','width:390,height:844')
    if mode=='phone-active':
        r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace("config.origin + '/learn?activityId=' + index,", "config.origin + '/learn?activityId=' + index + '-active',")
    selected=rows if mode!='phone-active' else [rows[3],rows[8],rows[11]]
    r.render(selected,H/mode,[Path('/media/jake/SSD/EDB/math')])
    report=json.loads((H/mode/'rendering.json').read_text())
    assert report['passed']
    reports=report.get('questions',report.get('records',report.get('results',[])))
    # The renderer retains each DOM audit in the per-question JSON as well.
    overflow=[]
    for path in sorted((H/mode).glob('question-*.json')):
        audit=json.loads(path.read_text())
        if audit.get('overflowingMath'):overflow.append({'file':path.name,'math':audit['overflowingMath']})
    (H/mode/'geometry.json').write_text(json.dumps({'passed':not overflow,'overflow':overflow},indent=2)+'\n')
    assert not overflow, (mode,overflow)
