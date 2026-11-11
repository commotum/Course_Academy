import json,collections
from pathlib import Path
H=Path(__file__).resolve().parent;out={}
for kp in [17592186096672,17592186096673]:
 records=json.loads((H/str(kp)/'sampled.json').read_text());groups={}
 for rec in records:
  q=rec['question'];band=q[':question/difficulty'];band=band[':db/ident']if isinstance(band,dict)else band;meta=rec.get('metadata',rec.get('generation',{}));group=band.split('/')[-1]+'/'+meta.get('bank_profile',meta.get('bank'));f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];key=f[':answer-field/correct'][1];actual=next(i for i,a in enumerate(choices)if a[':answer/id']==key)
  g=groups.setdefault(group,{'n':0,'correct_position':[0]*5,'hits':collections.Counter()});g['n']+=1;g['correct_position'][actual]+=1
  # Selection functions may inspect only offered strings/order, never givens/key.
  strategies={'longest_tex':max(range(5),key=lambda i:len(choices[i][':answer/value'])),'shortest_tex':min(range(5),key=lambda i:len(choices[i][':answer/value'])),'most_minus_signs':max(range(5),key=lambda i:choices[i][':answer/value'].count('-')),'fewest_minus_signs':min(range(5),key=lambda i:choices[i][':answer/value'].count('-'))}
  for name,index in strategies.items():g['hits'][name]+=index==actual
 out[str(kp)]={'groups':groups,'interpretation':'No population-wide bank-only rule established by these bounded shape/order probes. Construction independently chooses the key exchangeably from a completed bank; a different correct designation produces a different displayed question. Candidate substitution into an original equation is an inherent final-radio limitation and is also source supported (q-20524), not a bank-only rule.','limits':'Only listed probes and saved ordinary samples; no exhaustive no-shortcuts claim; no balancing quota imposed.'}
(H/'bank-probes.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
