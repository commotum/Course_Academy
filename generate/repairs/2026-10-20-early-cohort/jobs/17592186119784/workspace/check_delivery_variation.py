#!/usr/bin/env python3
import json,collections,pathlib
from validate_repair import audit,ordinary,matrix,g
P=pathlib.Path(__file__).resolve().parent;E=P/'evidence'
def analyze(rs):
 groups=collections.defaultdict(list)
 for r in rs:
  audit(r);q=r['question'];signature=(len(matrix(q[':question/problem'])),tuple(f[':answer-field/key'] for f in q[':question/answer-fields']))
  groups[signature].append(r)
 out=[]
 for (n,keys),group in groups.items():
  patterns={tuple(ordinary(r)) for r in group}
  count_groups=collections.defaultdict(set)
  for r in group:count_groups[sum(ordinary(r)) or 1].add(tuple(ordinary(r)))
  # Each visible ordinary position toggles within this exact wording/size bank.
  assert all({v[i] for v in patterns}=={False,True} for i in range(3))
  assert len(patterns)==(5 if group[0]['generation']['level']=='hard' else 4)
  assert any(len(v)>1 for v in count_groups.values())
  out.append({'dimension':n,'ordinary_keys':keys[:3],'patterns':[list(v) for v in sorted(patterns)],'same_correct_count_ambiguous':True})
 return out
report={}
for level in ['moderate','hard']:
 before=json.loads((E/(level+'-records.json')).read_text());after=json.loads((E/('delivery-'+level)/'accepted.json').read_text())
 report[level]={'input':analyze(before),'delivered':analyze(after),'input_count':len(before),'delivered_count':len(after)}
# Compare the original template-to-answer shortcut on exact latest batch seeds.
before=json.loads((E/'before-batch.json').read_text());fresh=json.loads((E/'fresh-records.json').read_text())[:5]
old={r['generation']['template']:ordinary(r) for r in before}
comparison=[]
for r in fresh:
 sid=r['generation']['template'];m=g.TEMPLATES[sid]['source_matrix'];keys=[f[':answer-field/key'] for f in r['question'][':question/answer-fields'][:3]]
 from validate_repair import evaluate
 prediction=[evaluate(m,k)[0] for k in keys]
 comparison.append({'seed':r['generation']['seed'],'template':sid,'source_lookup_prediction':prediction,'actual':ordinary(r),'lookup_correct':prediction==ordinary(r)})
report['exact_batch_source_lookup']=comparison
report['before_batch_source_lookup_correct']=5
report['after_batch_source_lookup_correct']=sum(x['lookup_correct'] for x in comparison)
report['semantic_counts']={l:sum(len(x['patterns']) for x in report[l]['delivered']) for l in ['moderate','hard']}
report['selection_limits']='Captured inventory and shared delivery filtering exercised. question_selection.rs chooses difficulty then fresh candidates; learner history, weights, concurrent inventory and runtime draw not available. No guarantee for an arbitrary history-restricted singleton subset.'
(E/'shortcut-results.json').write_text(json.dumps(report,indent=2));print({l:(report[l]['input_count'],report[l]['delivered_count']) for l in ['moderate','hard']});print('source lookup',report['before_batch_source_lookup_correct'],'/5 before;',report['after_batch_source_lookup_correct'],'/5 after')
