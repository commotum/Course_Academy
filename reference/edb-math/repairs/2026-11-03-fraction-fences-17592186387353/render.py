"""Compare actual fence heights, then render every changed lesson question."""
import json,statistics,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
import generate.pipeline.render_preview as r
old_audit=r.VISIBLE_DOM_AUDIT
audit=old_audit.replace('fonts:document.fonts.status',r'''
        displayFences:[...root.querySelectorAll('mjx-container[display="true"] [data-mml-node="mo"]')]
          .map(node=>({codes:[...node.querySelectorAll('use[data-c]')].map(g=>g.getAttribute('data-c')),height:node.getBoundingClientRect().height})),
        fonts:document.fonts.status''')
base=r.BROWSER_SCRIPT.replace(old_audit,audit);r.BROWSER_SCRIPT=base
before=json.loads((H/'capture.json').read_text())['question'];meta={'title':'Evaluating a Vector-Valued Function'}
r.render([{'knowledge_point':meta,'question':before}],H/'before-ui',[Path('/media/jake/SSD/EDB/math')])
rows=json.loads((H/'render-input.json').read_text());r.render(rows,H/'desktop',[Path('/media/jake/SSD/EDB/math')])
index=next(i for i,row in enumerate(rows) if row['question'][':db/id']==17592186387353)
old=json.loads((H/'before-ui/rendering.json').read_text())['cases'][0]
new=json.loads((H/'desktop/rendering.json').read_text())['cases'][index]
def parentheses(case):return [x['height'] for x in case['displayFences'] if any(code in ('28','29') for code in x['codes'])]
b,a=parentheses(old),parentheses(new)
assert b and a,(b,a)
assert statistics.median(a)>statistics.median(b)*1.2,(b,a)
r.BROWSER_SCRIPT=base.replace('width:1280,height:1000','width:390,height:844')
r.render([rows[index]],H/'phone',[Path('/media/jake/SSD/EDB/math')])
result={'passed':True,'questions_rendered':len(rows),'reported_question_index':index,
        'parenthesis_heights_before':b,'parenthesis_heights_after':a,
        'median_before':statistics.median(b),'median_after':statistics.median(a),
        'phone_render_passed':True,'reported_screenshot':f'desktop/question-{index+1:03}.png'}
(H/'render-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
