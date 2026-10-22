import json
from pathlib import Path
from html.parser import HTMLParser
E=Path(__file__).resolve().parent
class P(HTMLParser):
 def __init__(self):super().__init__();self.radios=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='input' and d.get('type')=='radio':self.radios.append(d['value'])
records=json.loads((E/'render-records.json').read_text());results=[]
for i,r in enumerate(records,1):
 p=P();p.feed((E/'render'/f'question-{i:03d}.html').read_text());f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 assert set(p.radios)=={a[':answer/id'] for a in f[':answer-field/choices']}
 results.append({'index':i,'parameters':r['generation']['parameters'],'screenshot':f'render/question-{i:03d}.png','rendered_choice_ids':p.radios,'correct_rendered_position':p.radios.index(correct),'correct_id':correct})
(E/'ui-order-results.json').write_text(json.dumps({'interface':'Unmodified ui/learning.js choiceOrder, stable hash of itemId:fieldId:choiceId. Raw package order is not rendered order.','results':results,'exact_batch_positions':[r['correct_rendered_position'] for r in results[-5:]],'limits':['Preview item IDs differ from live IDs. Choice order must not be inferred from generator order; live UI adds deterministic ordering for each task item.','Answer-rank probes are invariant under both option permutations.']},indent=2))
print('actual preview batch correct positions:',[r['correct_rendered_position'] for r in results[-5:]])
