"""Hold the full answer bank fixed and assign each of its five pairs as key."""
import copy,json
import validate_repair as a
from collections import Counter
records=[];results=[]
for t in a.g.FAMILIES['easy']+a.g.FAMILIES['moderate']+a.g.FAMILIES['hard']:
 level=next(level for level,ts in a.g.FAMILIES.items() if t in ts)
 r=a.g.generate(level,7100,t);d=r['generation']['decision'];base=r['generation']['parameters'];rs=[]
 for slot in range(5):
  dd=copy.deepcopy(d);p=copy.deepcopy(base);dd['correct_slot']=slot;
  if level=='easy':
   u=dd['p_candidates'][slot];v=dd['q_candidates'][slot];dd['forcing']=v
   if t=='q-16400':p['h']=u;p['c']=v
   elif 'k' in p:p['k']=u
   else:dd['linear']=u
  else:
   p['b']=dd['b_candidates'][slot]
   if level=='moderate':p['d']=dd['d_candidates'][slot]
  rr=a.g.generate(level,7101,t,parameters=p,decision=dd);assert a.math.check(rr)['passed'];rs.append(rr)
 banks=[sorted(c[':answer/value'] for c in r['question'][':question/answer-fields'][0][':answer-field/choices']) for r in rs]
 assert all(b==banks[0] for b in banks)
 assert len({a.key(r) for r in rs})==5 and len({r['question'][':question/problem'] for r in rs})==5
 results.append({'template':t,'record_indices':list(range(len(records),len(records)+5)),'identical_complete_banks':True,'distinct_correct_values':5,'distinct_prompts':5,'prompt_independent_strategy_success':'Exactly 1/5 for any deterministic rule selecting a value from the unordered five-value bank; each value becomes correct once. Option positions are tested separately. Native-grader checks included.'})
 records.extend(rs)
a.save('controlled-bank-records.json',records);a.save('controlled-easy-records.json',[r for r in records if r['generation']['difficulty']=='easy']);a.save('controlled-bank-results.json',results)
cs=[]
for r in records:
 f=r['question'][':question/answer-fields'][0];cs.append({'label':'fixed bank '+r['generation']['template'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/value']==a.key(r) else 'rejected','purpose':'controlled reassignment with identical complete bank'} for c in f[':answer-field/choices']]})
a.save('controlled-bank-grader-input.json',cs)
print('Controlled fixed banks:',len(results),'families,',len(records),'records,',len(cs)*5,'native checks prepared.')
