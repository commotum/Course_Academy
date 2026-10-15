"""Freeze the complete owned pathset and recheck the immutable pre-import baseline."""
import sys
sys.dont_write_bytecode=True
import json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[2];S=D.with_suffix('.py');kp='17592186087699'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
baseline=json.loads((D/'immutable-baseline.json').read_text());root=R/'generate/scratch'
paths=sorted([p for p in root.rglob('*') if p.is_file() and (p==root/(kp+'.py') or root/kp in p.parents or (p.suffix=='.pyc' and kp in p.name))])
actual={str(p.relative_to(R)):sha(p) for p in paths}
assert actual==baseline['paths'];assert (root/(kp+'.py')).exists()==baseline['registered_numeric_script_exists'];assert (root/kp).exists()==baseline['registered_numeric_tree_exists']
build=json.loads((D/'reference/grader-build.json').read_text());provenance={}
for key in ['engine_sources','dependencies']:
 for p,h in build[key].items():assert sha(R/p)==h;provenance[p]=h
for key in ['source','library','binary']:
 p=build[key];h=build[key+'_sha256'];assert sha(R/p)==h;provenance[p]=h
assert len(provenance)==42 and sha(D/'check-engine')==build['binary_sha256']
assert not (D/'check-engine').stat().st_mode & 0o222
v=json.loads((D/'validation.json').read_text());assert v['script_sha256']==sha(S)
render=json.loads((D/'render-report.json').read_text());assert render['records']==46 and render['errors']==render['exposed_delimiters']==render['red_noUndefined_errors']==render['overflow']==0
visual={'actual_player_records':46,'screenshots':46,'inspected_screenshots':['hard-q-11640-3.png','moderate-q-7908-6.png','hard-q-11637-35.png','easy-e-4499-44.png'],'findings':'All three practice backbones plus completed canonical inspected. Ordinary square-bracket matrices retain two rows/two columns; dense rational entries, witness masks, aligned product chains, checkboxes and full five-choice radio bank are legible. No clipping, missing operands or stale matrix names seen. Actual player controls verify explicit false-entity submission before interaction, true-entity submission after checking, and full field-owned radio UUIDs. Automated46-record checks cover all original source masks and changed E/M/H variants.','mathjax_errors':0,'red_noUndefined':0,'overflow':0,'exposed_delimiters':0,'root_qa_approval':'pending'}
(D/'visual-qa.json').write_text(json.dumps(visual,indent=2)+'\n')
v.update({'status':'passed worker mathematical/source/native/player checks; root QA approval pending','player_records':46,'player_control_contracts':'checkbox false/true owned entities and complete field-owned radio bank checked','player_mathjax_errors':0,'player_red_noUndefined_errors':0,'player_overflow':0,'immutable_numeric_baseline_unchanged':True,'registered_generator_at_dispatch':False,'raw_changed_coefficient_profiles_validated':24,'disjoint_normal_level_guards':9,'unique_sampled_tasks':{k:x['unique_mathematical_tasks'] for k,x in json.loads((D/'variety.json').read_text()).items()},'root_qa_approval':'pending'})
(D/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
owned=[S]+[p for p in sorted(D.rglob('*')) if p.is_file() and p.name not in ('owned-freeze.json','finish-integrity.json')]
hashes={str(p.relative_to(R)):sha(p) for p in owned}
freeze={'script_sha256':sha(S),'files':hashes,'self_exclusions':['owned-freeze.json','finish-integrity.json'],'reason':'The final index excludes itself and its detached integrity record to avoid recursive hashes. Every other owned artifact, helper, source copy, rendering and code file is included.','root_qa_approval':'pending'}
(D/'owned-freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
finish={'script_sha256':sha(S),'owned_files':len(hashes),'owned_freeze_sha256':sha(D/'owned-freeze.json'),'baseline_sha256':sha(D/'immutable-baseline.json'),'numeric_baseline_pathset_and_hashes_unchanged':actual==baseline['paths'],'registered_numeric_script_tree_pycs':'absent, unchanged','grader_provenance_hashes_reverified':len(provenance),'root_qa_approval':'pending','database_writes':0,'registration_changes':0,'engine_changes':0}
(D/'finish-integrity.json').write_text(json.dumps(finish,indent=2)+'\n')
assert all(sha(R/p)==h for p,h in hashes.items());print(json.dumps(finish,indent=2))
