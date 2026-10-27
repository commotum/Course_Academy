import collections,json
from pathlib import Path
h=Path('reference/edb-math/repairs/2026-10-26-structural-math');w=Path('.local/edb/structural-math-2026-10-26')
m=json.loads((w/'metadata.json').read_text());p=json.loads((w/'parents.json').read_text());first={};last={};updates=0;tx=[]
for n in ['', 'batch-02','batch-03','batch-04','batch-05']:
 d=h/n
 tx.append(json.loads((d/'verification.json').read_text())['basis_t'])
 for f in json.loads((d/'fields.json').read_text()):
  k=(f['entity'],f['attribute']);first.setdefault(k,f['before']);last[k]=f['after'];updates+=1
net={k for k,v in last.items() if v!=first[k]};todo=[e for e,a in net];seen=set();lessons=set();questions=set()
while todo:
 e=todo.pop()
 if e in seen:continue
 seen.add(e);meta=m.get(str(e),{})
 if 'topic/math-academy-id' in meta:lessons.add(e)
 if 'question/id' in meta:questions.add(e)
 todo.extend(q for q,a in p.get(str(e),[]))
 if 'activity/scope' in meta:todo.append(meta['activity/scope'])
result={'net_repaired_fields':len(net),'net_entities':len({e for e,a in net}),'lessons':len(lessons),'question_entities_with_net_changes_or_choice_repairs':len(questions),'field_updates':updates,'committed_batches':tx,'attributes':dict(collections.Counter(a for e,a in net)),'reconstruction_regression_reverted':[list(k)for k in last if k not in net]}
(h/'completion.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
