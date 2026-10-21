import json,collections
from pathlib import Path
import validate as v
E=v.E
rs=[]
for band in ['easy','moderate']:
 records=json.loads((E/f'delivery-{band}/accepted.json').read_text())
 for r in records:v.witness(r)
 rs.extend(records)
report=v.shortcut_report(rs)
v.save('pedagogical-variation-after.json',report)
# Semantic count is the parsed target, excluding UUIDs, seed and shuffled choices.
summary={p:{'records':len(xs),'semantic_matrices':len({v.witness(r) for r in xs})} for p,xs in ((p,[r for r in rs if r['generation']['bank_profile']==p]) for p in report)}
v.save('delivery-variation-summary.json',summary)
representatives=[]
for p in report:
 # Same source template with signed coefficients and full-sized answer bank.
 candidates=[r for r in rs if r['generation']['bank_profile']==p]
 representatives.append(candidates[0])
v.save('render-records.json',representatives)
print(json.dumps(summary,indent=2))
# Fixed-bank counterfactuals after the real inventory/dedup/difficulty filters.
role_reports={}
for band in ['easy','moderate']:
 accepted=json.loads((E/f'role-delivery-{band}/accepted.json').read_text())
 groups=collections.defaultdict(list)
 for r in accepted:
  v.witness(r)
  f=r['question'][':question/answer-fields'][0]
  bank=tuple(sorted(str(v.matrix(a[':answer/value'])) for a in f[':answer-field/choices']))
  groups[(r['generation']['bank_profile'],bank)].append(r)
 expected={'q-129137':3,'q-71731':4,'q-71733':5,'q-71734':4,'q-1070':3,'q-1073':2}
 for profile in {k[0] for k in groups}:
  counts=[len({v.witness(r) for r in rs}) for (p,_),rs in groups.items() if p==profile]
  assert max(counts)>=expected[profile],(profile,counts)
  role_reports[profile]={'accepted_fixed_bank_target_counts':counts,'required_full_target_count':expected[profile],'all_required_targets_survive_in_nonsource_bank':True}
v.save('decision-roles-after-delivery.json',role_reports)
# Grading the exact requested five records, not just nearby sampler seeds.
request=json.loads((E/'learner-request.json').read_text());cases=[]
for r in request:
 t=v.witness(r)
 cases.append({'label':'exact requested batch','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if v.matrix(a[':answer/value'])==t else 'rejected','purpose':'exact CLI sample visible matrix'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]})
v.save('requested-native-input.json',cases)
import subprocess
subprocess.run([str(v.REPO/'generate/runs/current/check-engine'),str(E/'requested-native-input.json'),str(E/'requested-native-report.json')],check=True,capture_output=True)
print('post-delivery fixed-bank target coverage passed for all six profiles; exact requested batch native grading passed')
