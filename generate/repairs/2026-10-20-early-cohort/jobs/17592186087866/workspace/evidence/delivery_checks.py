"""Check the repaired cue, controlled roles and native responses after filtering."""
import json
from collections import defaultdict
import validate_repair as a
import probes
E=a.E
sets={n:json.loads((E/n/'accepted.json').read_text()) for n in ('delivery','delivery-controlled','delivery-runner')}
reports={};sample=[]
for name,rs in sets.items():
 reports[name]=probes.analyze(rs)
 assert all(not c['side_frequency_max']['unique'] for c in reports[name]['cases'])
 if name=='delivery':
  seen=set()
  for r in rs:
   if r['generation']['template'] not in seen:sample.append(r);seen.add(r['generation']['template'])
 else:sample.extend(rs)
controlled=defaultdict(list)
for r in sets['delivery-controlled']:controlled[r['generation']['template']].append(r)
for t,rs in controlled.items():
 assert len(rs)==5 and len({a.key(r) for r in rs})==5
 assert len({tuple(sorted(c[':answer/value'] for c in r['question'][':question/answer-fields'][0][':answer-field/choices'])) for r in rs})==1
cases=[]
for r in sample:
 z=a.math.check(r);assert z['passed']
 cases.append({'label':'delivered '+r['generation']['template'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':c['choice_id'],'expected':'accepted' if c['standard'] and c['equivalent'] else 'rejected','purpose':'independent exact check after actual delivery normalization'} for c in z['choices']]})
a.save('delivered-grader-input.json',cases);a.save('delivery-shortcut-results.json',reports)
a.save('delivery-controlled-results.json',{'families':len(controlled),'delivered_records':len(sets['delivery-controlled']),'each_identical_bank_has_five_distinct_correct_values':True,'native_records_prepared':len(cases),'native_checks_prepared':5*len(cases)})
print('Delivered banks:',len(controlled),'complete five-way reassignment groups;',len(cases)*5,'native checks prepared.')
