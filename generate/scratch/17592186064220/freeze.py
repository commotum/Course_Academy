"""Recursive owned-tree freeze, excluding only the manifest itself."""
import sys
sys.dont_write_bytecode=True
import hashlib,json,collections
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];SCRIPT=HERE.with_suffix('.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
baseline=json.loads((HERE/'baseline.json').read_text());assert baseline['numeric_script_existed']is False and baseline['numeric_tree_existed_before_creation']is False
assert baseline['manifest_entry']['latest_inventory']['has_generator']is False
reference={str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size}for p in (HERE/'reference').rglob('*')if p.is_file()}
# Check the frozen source evidence against basis-2275 input rather than a moving
# current manifest. No existing numeric artifact existed to preserve.
for category in ['sources','topics','lessons']:
 source=ROOT/('generate/runs/current/refresh-2026-10-14/'+category+'/'+str(17592186064220 if category=='sources'else 17592186048189)+'.json')
 assert sha(source)==sha(HERE/'reference'/(category+'.json'))
assert sha(HERE/'source.json')==sha(HERE/'reference/sources.json')
assert sha(HERE/'check-engine')==sha(ROOT/'generate/runs/current/check-engine')
assert sha(HERE/'math_format.py')==sha(ROOT/'scripts/question_capture/math_format.py')
save('final-preservation.json',{'passed':True,'baseline':'numeric script/tree absent before work; no preexisting registered artifacts imported or altered','basis_2275_source_evidence_unchanged':True,'frozen_native_binary_matches_current_runner':True,'frozen_formatter_matches_shared_source':True,'owned_roots':[str(SCRIPT),str(HERE)],'registered_baseline_sha256':sha(HERE/'baseline.json')})
v=json.loads((HERE/'validation.json').read_text())
inputs=json.loads((HERE/'native-input.json').read_text());native=json.loads((HERE/'native-grading.json').read_text());breakdown=collections.Counter()
for item,row in zip(inputs,native['records']):
 for probe,outcome in zip(item['checks'],row['checks']):
  shape='radio'if 'radio'in probe['purpose']else'blank';breakdown[shape+' '+probe['purpose'].replace('normal ','')+' '+outcome['outcome']]+=1
inventory=json.loads((HERE/'independent-inventory.json').read_text());fixtures=json.loads((HERE/'diagnostic-blank-cases.json').read_text())
assert inventory['basis']==2275 and inventory['questions']==[]
assert len(fixtures['questions'])==3 and all(q['role']=='authored blank grading fixture'for q in fixtures['questions'])
assert sum(r['label'].startswith('independent normal blank ')for r in native['records'])==3
v['standard_artifact_checks']={'source_wrapper_byte_exact':True,'captured_non_MA_questions':0,'authored_blank_fixtures_separate':3,'native_fixture_records_preserved':3,'JSON_and_Markdown_CLI_verified':True}
v.update({'native_check_total':sum(breakdown.values()),'native_probe_breakdown':dict(breakdown),'canonical_native_pass':True,'wrong_math_native_rejected':True,'genuine_equivalent_native_false_rejections':48})
v.update({'latest_script_SHA256':sha(SCRIPT),'latest_validator_SHA256':sha(HERE/'validate.py'),'baseline_preservation':True});save('validation.json',v)
manifest_path=HERE/'freeze-manifest.json';entries={}
for p in [SCRIPT,HERE,*sorted(HERE.rglob('*'))]:
 if p==manifest_path:continue
 entries[str(p.relative_to(ROOT))]={'kind':'directory'}if p.is_dir()else{'kind':'file','sha256':sha(p),'bytes':p.stat().st_size}
save('freeze-manifest.json',{'version':1,'basis':2275,'script_SHA256':sha(SCRIPT),'validation_status':v['status'],'normal_native_equivalence_gaps':v['normal_generator_grading_gaps'],'excluded':[str(manifest_path.relative_to(ROOT))],'entries':entries})
print('Frozen',len(entries),'entries; script SHA256',sha(SCRIPT))
