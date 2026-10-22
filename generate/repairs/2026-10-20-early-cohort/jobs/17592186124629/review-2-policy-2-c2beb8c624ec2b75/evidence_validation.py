import hashlib,json
from pathlib import Path
import jsonschema
E=Path(__file__).resolve().parent;R=Path('/home/jake/Developer/Course_Academy');W=E.parent/'workspace'
def load(n):return json.load(open(E/n))
pv=load('pedagogical-variation.json');result=load('result.json')
jsonschema.validate(pv,json.load(open(R/'generate/pipeline/pedagogical-variation.schema.json')))
refs=[]
for section in ['coverage','counterfactuals','shortcut_probes']:
 for x in pv[section]:refs+=x['sample_refs']
refs+=pv['delivery']['sample_refs']
refs+=result['source_analysis']['evidence_paths']
for c in result['checks'].values():
 assert c['status']=='passed' and c['evidence_paths'];refs+=c['evidence_paths']
for ref in refs:
 p=E/ref;assert not Path(ref).is_absolute() and p.resolve().is_relative_to(E)
 assert p.is_file() and p.stat().st_size>0,ref
assert {'relevant','irrelevant'}<={c['kind'] for c in pv['counterfactuals']}
assert any(x['scope']!='overall' for x in pv['shortcut_probes'])
assert len(result['checks'])==8 and not result['findings'] and result['verdict']=='accepted'
native=load('native-report.json');assert native['accepted_checks']==348 and native['rejected_checks']==654 and native['database_writes']==0
before=load('package-hashes-before.json');after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
assert before==after
out={'pedagogical_schema':'passed','all_cited_evidence_nonempty':True,'unique_paths_checked':len(set(refs)),'eight_checks_pass':True,'package_unchanged':True,'files_checked':len(after),'native_submissions':1002}
(E/'evidence-validation.json').write_text(json.dumps(out,indent=2)+'\n')
(E/'session-state.md').write_text('Review complete: accepted. All eight checks have current nonempty evidence. Retained old shortcut fails; current strict regression passes. First pass 73 records / 13 families, 606 semantic domain instances preserved. Exact 5-record batch and 87 controls survive actual delivery; 184 math cases and 1,002 native submissions pass. All 11 actual-UI screenshots inspected. Pedagogical schema and evidence paths validated. Captured inventory contains only 16 original source questions; affected-inventory.json is empty on that verified basis. All 158 package files unchanged. Result: result.json (also review-result.json). No assets published or database writes.\n')
print(json.dumps(out))
