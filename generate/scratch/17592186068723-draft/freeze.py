"""Freeze this private draft only after all mathematical/native checks pass."""
import hashlib,json,sys
from pathlib import Path
import sympy
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 validation=json.loads((HERE/'validation.json').read_text());assert validation['passed']
 native=json.loads((HERE/'native-grading.json').read_text());diagnostic=json.loads((HERE/'native-diagnostics.json').read_text());assert native['documented_unresolved_checks']==0
 baseline=json.loads((HERE/'registered-baseline.json').read_text());root=HERE.parents[2]
 actual={str(p.relative_to(root)):sha(p) for p in [HERE.with_name('17592186068723.py'),*HERE.with_name('17592186068723').rglob('*')] if p.is_file()};assert actual==baseline
 source=json.loads((HERE/'source.json').read_text())
 for filename,folder,id in [('source.json','sources','17592186068723'),('topic.json','topics','17592186050771'),('lesson.json','lessons','17592186050771')]:
  assert (HERE/filename).read_bytes()==(root/'generate/runs/current/refresh-2026-10-14'/folder/(id+'.json')).read_bytes()
 files=[HERE.with_suffix('.py'),*[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='freeze.json']]
 hashes={str(p):sha(p) for p in sorted(files)}
 result={'status':'ready_for_independent_root_approval','database_writes':0,'registration':False,'entry_point':str(HERE.with_suffix('.py')),'entry_sha256':sha(HERE.with_suffix('.py')),'source_basis':source['basis'],'source_lineage':source['lineage'],'actual_grader':str(HERE/'check-engine'),'actual_grader_sha256':sha(HERE/'check-engine'),'versions':{'python':sys.version.split()[0],'sympy':sympy.__version__},'normal_verified_instances':validation['normal_instances_exhaustive'],'raw_verified_instances':validation['raw_instances_exhaustive'],'native':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'valid_math_unresolved':native['documented_unresolved_checks'],'separate_diagnostic_accepted':diagnostic['accepted_checks'],'separate_diagnostic_known_equivalence_limit_rejections':diagnostic['rejected_checks'],'separate_malformed_ownership_diagnostics':diagnostic['documented_unresolved_checks']},'registered_baseline':{'protected_files':len(actual),'full_path_set_and_hashes_unchanged':True},'sha256':hashes,'private_tree_sha256':hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()}
 (HERE/'freeze.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='sha256'},indent=2))
if __name__=='__main__':main()
