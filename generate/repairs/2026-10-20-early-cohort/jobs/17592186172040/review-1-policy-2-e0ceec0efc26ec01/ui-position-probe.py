from review import *
import re,collections
# Exact unsigned FNV hash used by ui/learning.js choiceOrder.
def fnv(s):
 h=2166136261
 for c in s:h=((h^ord(c))*16777619)&0xffffffff
 return h
def ordered(r,item):
 f=r['question'][':question/answer-fields'][0]
 return sorted(f[':answer-field/choices'],key=lambda a:fnv(str(item)+':'+f[':answer-field/id']+':'+a[':answer/id']))
rows=[]
for label in ['controls','batch','rest','canonical']:
 records=json.loads((E/('render-'+label)/'input.json').read_text())
 for i,r in enumerate(records):
  html=(E/('render-'+label)/('question-%03d.html'%(i+1))).read_text()
  ids=re.findall(r'<input type="radio"[^>]* value="([^"]+)"',html)
  f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
  matched=[str(item) for item in ['undefined',i+1] if [a[':answer/id'] for a in ordered(r,item)]==ids]
  assert ids and matched
  rows.append({'render':label,'index':i,'question_id':r['question'][':question/id'],'template':r['generation']['template'],'choice_ids':ids,'correct_index':ids.index(correct),'matching_ui_seed_itemId':matched})
# Actual captured preview DOM data, separately from generator array order.
probes=[]
for pool in ['batch','controls','rest']:
 gr=[a for a in rows if a['render']==pool]
 for group in ['overall']+sorted({r['template'] for r in gr}):
  subset=[a for a in gr if group=='overall' or a['template']==group];counts=collections.Counter(a['correct_index'] for a in subset)
  probes.append({'pool':pool,'template':group,'correct':counts[0],'total':len(subset),'positions':dict(counts),'baseline':.2})
# Conditional on representative item IDs, evaluate live ID ordering sensitivity.
rs=json.loads((E/'delivery-batch/accepted.json').read_text());sensitivity=[]
for item in ['1','17','1001','87592186700001']:
 positions=[]
 for r in rs:
  ids=[a[':answer/id'] for a in ordered(r,item)];positions.append(ids.index(r['question'][':question/answer-fields'][0][':answer-field/correct'][1]))
 sensitivity.append({'hypothetical_item_id':item,'correct_indices':positions,'choose_first_correct':positions.count(0),'total':len(positions)})
dump('ui-position-results.json',{'command':str(P)+' ui-position-probe.py','ui_source':'ui/learning.js:690-701','captured_positions':rows,'probes':probes,'live_item_id_controls':sensitivity,'limits':'Actual preview DOM order measured. Live task item IDs are unavailable; supplied controls demonstrate ordering sensitivity, not any exact future learner sequence.'})
print('actual batch positions',[a['correct_index'] for a in rows if a['render']=='batch']);print('sensitivity',sensitivity)
