#!/usr/bin/env python3
"""Hash the ready, private step3–7 evidence after successful verification."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(name):return json.loads((HERE/name).read_text())
validation=load('validation.json');render=load('render-validation.json');branches=load('domain-probes.json')
assert validation['status']=='passed' and render['passed'] and branches['passed']
assert validation['native_unresolved_checks']==0
assert load('source.json')['basis']==2275
assert len(load('source-cases.json'))==8 and all('record' in c for c in load('source-cases.json'))
assert sha(HERE/'reference/check-engine')=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
ready={'status':'ready for independent parent review; no registration','script':str(HERE.with_suffix('.py').relative_to(HERE.parents[2])),'script_sha256':sha(HERE.with_suffix('.py')),'validator_sha256':sha(HERE/'validate.py'),'source_basis':2275,'database_writes':0,'native_records':load('native-report.json')['accepted_checks'],'native_correct_accepted':validation['native_accepted_checks'],'native_wrong_rejected':validation['native_rejected_checks'],'native_unresolved':0,'ownership_diagnostics_separate':2,'source_prompts':8,'source_solutions':7,'source_bank_values':40,'source_complete_banks':8,'bounded_default_states':validation['bounded_instances'],'distinct_mathematical_capacity':load('capacity.json')['by_level'],'ui_records':render['records'],'ui_math_expressions':render['math_expressions'],'negative_branch_display_derivatives':branches['exact_displayed_derivative_comparisons'],'source_anomaly':'q-113876 missing difficulty, correct ref and solution preserved in observed profile; labeled authored completion for service','unresolved_source_interpretation':'historical distractor intent for opaque scalar profiles; ordinary sampling uses labeled method-error banks','runtime_private_helpers':True,'approval_owner':'root','engine_sha256':sha(HERE/'reference/check-engine')}
(HERE/'ready.json').write_text(json.dumps(ready,indent=2)+'\n')
files=[HERE.with_suffix('.py')]+[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256.json']
hashes={str(p.relative_to(HERE.parent)):sha(p) for p in sorted(files)}
(HERE/'SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n')
print(json.dumps(ready,indent=2))
