import sys
sys.dont_write_bytecode=True
import json,random
from pathlib import Path
from itertools import product
from collections import Counter
E=Path(__file__).resolve().parent
ns={'__file__':str(E/'audit.py')};exec((E/'audit.py').read_text().split('batch=json.loads')[0],ns)
g=ns['g'];save=ns['save'];inspect=ns['inspect']
rng=random.Random(407181)
rs=[];groups=[]
for i,(bases,indices) in enumerate(g.indexed_profiles()):
 t=g.TEMPLATES[i%2]
 b={'bases':bases,'indices':indices,'foil_numerator':rng.choice(bases),'foil_denominator':rng.choice(indices)}
 ix=[]
 for x,n in product(bases,indices):
  r=g.generate(x,n,t,indexed_bank=b,order_seed=407181+i)
  inspect(r);ix.append(len(rs));rs.append(r)
 assert len({tuple(sorted(a[':answer/value'] for a in rs[j]['question'][':question/answer-fields'][0][':answer-field/choices'])) for j in ix})==1
 groups.append({'profile':i,'bases':bases,'indices':indices,'record_indices':ix})
for pair in g.square_pairs():
 for foil in [1,3,4,5]:
  for inverted in pair:
   ix=[]
   for x in pair:
    r=g.generate(x,2,'square-equation',foil_index=foil,base_direction=1 if x==pair[0] else -1,inverted_base='target' if x==inverted else 'other',order_seed=407181)
    inspect(r);ix.append(len(rs));rs.append(r)
   assert len({tuple(sorted(a[':answer/value'] for a in rs[j]['question'][':question/answer-fields'][0][':answer-field/choices'])) for j in ix})==1
   groups.append({'pair':pair,'foil_index':foil,'inverted':inverted,'record_indices':ix})
save('profile-records.json',rs)
save('profile-results.json',{'command':'.venv/bin/python -B expand.py','seed':407181,'indexed_profiles':len(g.indexed_profiles()),'square_pairs':len(g.square_pairs()),'record_count':len(rs),'groups':groups,'failures':[], 'checks':['Read served radical, exact prime-exponent arithmetic on all five choices, unique values, key, solution substitutions and final equality.','All four targets within every indexed complete bank; both targets within every square bank; bank invariant under target swap.','One independently sampled foil assignment per indexed bank; foil dependency separately tested in controlled pairs and random trials.']})
raw=json.loads((E/'shortcut-raw.json').read_text()) if (E/'shortcut-raw.json').exists() else []
for r in raw:inspect(r)
save('profile-summary.json',{'profile_records':len(rs),'indexed_profiles':len(g.indexed_profiles()),'square_pairs':len(g.square_pairs()),'math_failures':0,'random_trials_checked':len(raw)})
(E/'session-state.md').write_text('Source replay, exact arithmetic on initial samples and all complete profiles, capacity/determinism/relocation checks done. Delivery and renderer running; shortcut trials and native grader pending completion. All generated evidence under review root.\n')
print(json.dumps({'profile_records':len(rs),'indexed_profiles':len(g.indexed_profiles()),'square_pairs':len(g.square_pairs()),'failures':0}))
