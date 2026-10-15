"""Raw changed-coefficient profiles and independent normal-level boundaries."""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,copy
from pathlib import Path
D=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('inverse_validate',D/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v);g=v.g
checks=[]
for sid in g.TEMPLATES:
 generated=g.generate('easy',seed=234,template=sid)
 p=generated['generation']['parameters']
 for profile in g.PROFILES:
  rec=g.generate('easy',seed=9,template=sid,profile=profile,parameters=p);v.validate_record(rec)
  checks.append({'source_id':sid,'profile':profile,'changed_coefficients':p!=g.original_parameters(sid),'actual_displayed_math_valid':True})
# Strict API guards enforce signed absolute bounds and normal level distinctions.
bounds=[]
for target in g.SUPPORTED_LEVELS:
 for source in g.SUPPORTED_LEVELS:
  rec=g.generate(source,seed=19,template='q-11640')
  try:g.generate(target,template='q-11640',parameters=rec['generation']['parameters'])
  except ValueError:accepted=False
  else:accepted=True
  # Hard's rational first matrix cannot enter E/M; quarters cannot enter easy;
  # easy lacks moderate quarters and a hard fractional first matrix.
  assert accepted==(source==target),(source,target,accepted)
  bounds.append({'source_level':source,'requested_level':target,'accepted':accepted})
# Literal raw replay never substitutes for parameterized normal changed work.
assert all(row['changed_coefficients'] for row in checks)
(D/'extended-checks.json').write_text(json.dumps({'all_profiles_changed_coefficients':checks,'disjoint_normal_level_guards':bounds},indent=2)+'\n')
print('Validated24 changed-coefficient profile calls and9 disjoint normal-level guards')
