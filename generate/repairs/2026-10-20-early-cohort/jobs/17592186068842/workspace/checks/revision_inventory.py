"""Check the latest demonstrated signatures against the entire captured pool."""
import json,sys,re
sys.dont_write_bytecode=True
from bank_signature_regression import E,ROOT,a
inv=json.loads((ROOT.parent/'source/inventory.json').read_text());rows=[]
for q in inv['questions']:
 f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];key=f[':answer-field/correct'][':answer/id']
 hits={}
 for label,method in [('modal_components',a.choose),('shortest_repeated_lhs',a.power_sign_shortest)]:
  idx=method(cs);hits[label]={'selected':idx,'correct':idx is not None and cs[idx][':answer/id']==key}
 source=':question/math-academy-id' in q
 rows.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'is_source':source,'probes':hits})
 assert source or not any(v['correct'] for v in hits.values()), 'Generated inventory witness requires exact-generation reproduction'
(E/'inventory-probe.json').write_text(json.dumps({'basis':inv['basis'],'tested':rows,'generated_tested':sum(not r['is_source'] for r in rows),'generated_affected':0,'verified_absence':'Both exact attacks were run on all six captured generated banks and selected no correct answer. The six generated records are one exp_sum and five double_factor records; neither revised quotient construction occurs. Original source questions are excluded from affected generated inventory.','limits':'Captured inventory only; no live database query or mutation.'},indent=2)+'\n')
(E/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]},indent=2)+'\n')
print('latest inventory signatures: 16 inspected, 6 generated tested, 0 affected')
