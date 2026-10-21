import json,re,collections,hashlib
from pathlib import Path
E=Path(__file__).resolve().parent

def fnv(v):
 n=2166136261
 for c in v:n=((n^ord(c))*16777619)&0xffffffff
 return n

def pos(r,item_id='1'):
 q=r['question'];f=q[':question/answer-fields'][0];choices=sorted(f[':answer-field/choices'],key=lambda c:fnv(f"{item_id}:{f[':answer-field/id']}:{c[':answer/id']}"));cid=f[':answer-field/correct'][1]
 return next(i+1 for i,c in enumerate(choices) if c[':answer/id']==cid)
rr=json.load(open(E/'runner-batch.json'));out={'implementation':'ui/learning.js:690-702; FNV1a sorting by itemId:fieldId:answerId; previewContent uses step.contentId (index+1) and UUID field/answer IDs. Live DB numeric IDs and task item IDs are unavailable.','batch_preview':[{'question_id':r['question'][':question/id'],'template':r['generation']['template'],'shape':'vector' if 'then solve' in r['question'][':question/problem'] else 'matrix','correct_display_position':pos(r,str(i+1))} for i,r in enumerate(rr)],'item_id_counterfactuals':[],'html_checks':[]}
for i,r in enumerate(rr):
 positions=collections.Counter(pos(r,str(item)) for item in range(1001,1101))
 out['item_id_counterfactuals'].append({'question_id':r['question'][':question/id'],'item_id_range':[1001,1100],'counts':dict(positions),'all_positions_observed':len(positions)==5})
inputs=json.load(open(E/'render/input.json'))
for i,r in enumerate(inputs):
 html=(E/f'render/question-{i+1:03}.html').read_text();inputs_in_html=re.findall(r'<input[^>]*type="radio"[^>]*>',html);order=[re.search(r'value="([^"]+)"',x)[1] for x in inputs_in_html];correct=r['question'][':question/answer-fields'][0][':answer-field/correct'][1]
 observed=order.index(correct)+1
 out['html_checks'].append({'render_index':i,'expected_position':pos(r,str(i+1)),'observed_position':observed,'match':observed==pos(r,str(i+1)),'html':f'render/question-{i+1:03}.html'})
(E/'ui-position-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
