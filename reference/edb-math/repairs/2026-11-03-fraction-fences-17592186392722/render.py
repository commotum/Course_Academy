"""Render all affected examples, answers, solutions and actual tutorial steps."""
import copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
import generate.pipeline.render_preview as r
old_preview=r.preview
def preview(record,index,*,active=False):
    result=old_preview(record,index,active=active)
    if 'tutorial' in record:
        t=record['tutorial'];result['steps']=[{'kind':'tutorial','contentId':t[':db/id'],'markdown':t[':tutorial/content'],'title':t[':tutorial/title'],'status':'completed','fields':[]}]
    return result
r.preview=preview
old_audit=r.VISIBLE_DOM_AUDIT
audit=old_audit.replace('fonts:document.fonts.status',r'''
        vectorFences:[...root.querySelectorAll('mjx-container[display="true"] [data-mml-node="mo"]')]
          .filter(node=>[...node.querySelectorAll('use[data-c]')].some(g=>['27E8','27E9'].includes(g.getAttribute('data-c'))))
          .map(node=>node.getBoundingClientRect().height),
        fonts:document.fonts.status''')
base=r.BROWSER_SCRIPT.replace(old_audit,audit);r.BROWSER_SCRIPT=base
source=H.parent/'2026-11-03-fraction-fences-17592186387353/followup-17592186392722/capture.json'
before=json.loads(source.read_text())['question'][0][0]
r.render([{'question':before}],H/'before-ui',[Path('/media/jake/SSD/EDB/math')])
rows=json.loads((H/'render-input.json').read_text());proposals=json.loads((H/'proposals.json').read_text())
for item in json.loads((H/'lessons.json').read_text()):
    for step in item[0][':activity/steps']:
        t=copy.deepcopy(step[':step/content'])
        if ':tutorial/content' not in t:continue
        t[':tutorial/content']=next(p['after'] for p in proposals if p['entity']==t[':db/id'] and p['attribute']=='tutorial/content')
        rows.append({'tutorial':t,'question':{':question/problem':t[':tutorial/content'],':question/answer-fields':[]}})
r.render(rows,H/'desktop',[Path('/media/jake/SSD/EDB/math')])
index=next(i for i,row in enumerate(rows) if row['question'].get(':db/id')==17592186392722)
b=json.loads((H/'before-ui/rendering.json').read_text())['cases'][0]['vectorFences']
a=json.loads((H/'desktop/rendering.json').read_text())['cases'][index]['vectorFences']
assert a and b and max(a)>max(b)*1.2,(a,b)
r.BROWSER_SCRIPT=base.replace('width:1280,height:1000','width:390,height:844')
r.render([rows[index]],H/'phone',[Path('/media/jake/SSD/EDB/math')])
result={'passed':True,'questions_and_canonical_examples_rendered':len(rows)-2,'tutorials_rendered':2,'phone_render_passed':True,'display_vector_heights_before':b,'display_vector_heights_after':a,'reported_screenshot':f'desktop/question-{index+1:03}.png'}
(H/'render-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
