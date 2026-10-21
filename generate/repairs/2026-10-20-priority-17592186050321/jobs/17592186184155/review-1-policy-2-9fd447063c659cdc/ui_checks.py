from audit import *
from html.parser import HTMLParser
class Inputs(HTMLParser):
 def __init__(self):super().__init__();self.ids=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='input' and a.get('type')=='radio':self.ids.append(a['value'])
def h(s):
 n=2166136261
 for c in s:n=((n^ord(c))*16777619)&0xffffffff
 return n
def ordered(r,itemid):
 import copy
 out=copy.deepcopy(r);f=out['question'][':question/answer-fields'][0];seed=f'{itemid}:{f[":answer-field/id"]}'
 f[':answer-field/choices'].sort(key=lambda c:h(seed+':'+c[':answer/id']));return out
records=json.loads((E/'render-input.json').read_text());render_report=json.loads((E/'render-all/rendering.json').read_text())
res=[]
for i,r in enumerate(records):
 dom=Inputs();dom.feed((E/f'render-all/question-{i+1:03}.html').read_text());expected=[c[':answer/id'] for c in qparts(ordered(r,i+1))[1]]
 assert dom.ids==expected,(i,dom.ids,expected)
 res.append({'render_record_index':i,'actual_dom_choice_ids':dom.ids,'matches_actual_learning_js_choiceOrder':True,'correct_dom_position':dom.ids.index(qparts(r)[1][qparts(r)[2]][':answer/id'])})
raw=json.loads((E/'delivery-sampled/accepted.json').read_text());ui=[ordered(r,f'review-item-{i}') for i,r in enumerate(raw)]
save('ui-ordered-samples.json',ui)
ns={};s=(E/'decision_tests.py').read_text();exec(s[s.index('def probes('):s.index('survived=json.loads')],globals(),ns)
save('ui-shortcut-results.json',{'command':f'{PY} ui_checks.py','item_id_basis':'Synthetic stable review-item-N; actual learner task-item IDs are unavailable. Rendering fixture uses its numeric contentId; exact algorithm checked against all 14 actual DOM radio orders.','results':ns['probes'](ui,'actual-ui-order-algorithm')})
save('visual-inspection.json',{'renderer_report':'render-all/rendering.json','command':f'{PY} {REPO}/generate/pipeline/render_preview.py --input render-input.json --output render-all --limit 14 --asset-root {W} --math-root /media/jake/SSD/EDB/math','passed':render_report['passed'],'reviewed_screenshots':[f'render-all/question-{i:03}.png' for i in range(1,15)],'contact_sheet':'render-contact.png','full_resolution_inspections':['render-all/question-007.png','render-all/question-012.png','render-all/question-014.png'],'observations':['All 14 prompts, five-choice radio banks, constants, fractional exponents, radical degrees, reciprocal denominators and solutions display without clipped math or exposed TeX in the inspected desktop layout.','Cases 6 and 7 show the same mathematical bank with changed sign evidence and changed correct answer; case 8 reorders terms and preserves the antiderivative.','All four complete source replay banks render. Supplied solutions are mathematically unchanged; missing q-2250 and q-29830 solutions are explicitly authored.','No diagrams or image choices occur; images and mobile layouts are not claimed.'],'dom_choice_order':res})
print(json.dumps({'rendered':len(records),'ui_order_matches':len(res),'ui_shortcut_overall':[x for x in ns['probes'](ui,'actual-ui-order-algorithm') if x['subgroup']=='overall']}))
