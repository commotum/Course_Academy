import audit as a
from probes import probe
from collections import defaultdict
rs=a.json.loads((a.E/'independent-records.json').read_text());groups=defaultdict(list)
for r in rs:groups[r['generation']['template']].append(r)
out=[]
for t,rr in groups.items():
 vals=[probe(r) for r in rr];position=[];standard=[]
 for r in rr:
  f=r['question'][':question/answer-fields'][0];position.append(f[':answer-field/choices'][0][':answer/id']==f[':answer-field/correct'][1]);ids=[c[':answer/id'] for c in f[':answer-field/choices'] if a.is_standard(a.equation(c[':answer/value']))];standard.append(len(ids)==1 and ids[0]==f[':answer-field/correct'][1])
 out.append({'template':t,'total':len(rr),'first_position_correct':sum(position),'frequency_strategy_correct':sum(v['correct'] for v in vals),'frequency_strategy_unique_max':sum(v['unique_maximum'] for v in vals),'unique_standard_form_correct':sum(standard),'interpretation':'In q-8359 and q-8360 selecting the only standard-form equation is the intended source exercise, not a defect. String repetition is an incidental arrangement unrelated to the standard-form criterion.'})
a.save('all-template-probes.json',{'command':str(a.PY)+' '+str(a.E/'extra_probes.py'),'records_file':'independent-records.json','results':out})
print(out)
