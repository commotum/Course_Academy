import sys,json,importlib.util,collections
from pathlib import Path
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parent;W=O.parent/'workspace'
s=importlib.util.spec_from_file_location('subject',W/'17592186078583.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def save(n,v):(O/n).write_text(json.dumps(v,indent=2)+'\n')
normal=[g.generate_easy(seed) for seed in range(108821,108836)];save('normal-easy-records.json',normal)
assert any(r['generation']['template']=='q-106877' for r in normal)
# Retain both initial bounds for changed moderate construction without a broad random sweep.
rows=[]
for t in g.DEFAULT_TEMPLATES['moderate']:
 lo,hi=(10,40) if g.TEMPLATES[t]['unit']=='C' else (50,85)
 for S in [lo,hi]:
  for I in [max(S+10,g.INITIAL_BOUNDS[t][0]),g.INITIAL_BOUNDS[t][1]]:
   r=g.generate_moderate(108853,template=t,parameters={'S':S,'I':I});rows.append(r)
   assert r==g.generate_moderate(108853,template=t,parameters={'S':S,'I':I})
save('initial-endpoint-records.json',rows)
save('sampling-coverage.json',{'normal_seed_range':[108821,108835],'normal_counts':dict(collections.Counter(r['generation']['template'] for r in normal)),'endpoints':[(r['generation']['template'],r['generation']['parameters']) for r in rows],'rejection_resampling_analysis':'generate validates finite S bounds, I>=S+10, then whole-bank symbolic uniqueness. In normal banks all S are nonzero positive and I>S; this makes ambient/initial/sum and plus/minus equilibria distinct. Oil replacement -kT has equilibrium 0 and cannot duplicate -k(T-S) for S>0. Moderate fifth is either a distinct wrong equilibrium (I+S), nonlinear, or a nonunit/positive initial coefficient. Thus no eligible decision case is removed by the retry condition; raw oil explicitly preserves its captured duplicate WRONG pair for replay only. Explicit invalid parameters are rejected rather than resampled (packaging.json). Boundary and default sampling provide independent executable controls.','finite_domain':'Task fingerprint retains ambient, unit, supplied-temperature-count; default CLI removes repeated fingerprints. Domains easy C31+F36=67 distinct tasks, moderate C31+F36=67. Initial and prose changes do not claim new core ambient tasks.'})
print('normal',collections.Counter(r['generation']['template'] for r in normal),'endpoints',len(rows))
