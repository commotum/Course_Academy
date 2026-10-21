import json,re,hashlib,collections
from pathlib import Path
O=Path(__file__).resolve().parent
read=lambda p:json.loads((O/p).read_text())
def save(n,v):(O/n).write_text(json.dumps(v,indent=2)+'\n')
def f(r):return r['question'][':question/answer-fields'][0]
def key(r):
 v=f(r)[':answer-field/correct'];return v[1] if isinstance(v,list) else v[':answer/id']
def fnv(s):
 n=2166136261
 for c in s:n=((n^ord(c))*16777619)&0xffffffff
 return n
def ordered(r,item):
 field=f(r);return sorted(field[':answer-field/choices'],key=lambda a:fnv(f"{item}:{field[':answer-field/id']}:{a[':answer/id']}"))
actual=[]
for i,r in enumerate(read('actual-ui-records.json'),1):
 h=(O/f'render/question-{i:03}.html').read_text();h=h[h.index('<fieldset'):h.index('</fieldset>')];ids=re.findall(r'<input type="radio"[^>]* value="([^"]+)"',h)
 expect=[a[':answer/id'] for a in ordered(r,i)];assert ids==expect
 actual.append({'record_index':i,'template':r['generation']['template'],'rendered_order':ids,'correct_position':ids.index(key(r))+1,'matches_application_choiceOrder':True,'screenshot':f'render/question-{i:03}.png'})
measure=[]
for dataset in ['samples.json','delivery-easy/accepted.json','delivery-moderate/accepted.json','batch.json','delivery-batch/accepted.json']:
 rs=read(dataset)
 for offset in [0,100000]:
  by=collections.defaultdict(collections.Counter)
  for i,r in enumerate(rs,1):by[r['generation']['template']][[a[':answer/id'] for a in ordered(r,i+offset)].index(key(r))+1]+=1
  measure.append({'dataset':dataset,'item_id_offset':offset,'by_template':{t:dict(c) for t,c in by.items()}})
save('ui-position-probes.json',{'command':'python3 ui_position_checks.py','implementation':'ui/learning.js choiceOrder lines690-692; actual UI fieldControl uses contentId in preview and task itemId in live learning. FNV32 order reproduced and verified against all 13 rendered DOMs.','actual_rendered':actual,'stage_controls':measure,'result':'No fixed position across fresh controls of any template under either tested item-ID envelope. Actual batch positions vary; liquid subgroup varies. Singleton chocolate/cake members do not establish a template predictor (fresh family controls have differing positions).','limitations':['Live task-item IDs are not yet assigned; examined two explicit ID envelopes and exact renderer IDs.','Stored generator choice order is not presented order: application choiceOrder reorders it; literal position probe counts in conditional-cue-probes.json refer to serialized records. This file supplies actual presentation-stage position evidence.']})
print('actual batch positions',[x['correct_position'] for x in actual[:5]])
