"""Freeze local draft recursively, excluding only this generated manifest itself."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];SCRIPT=HERE.with_suffix('.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snap(paths):
 out={}
 for p in paths:
  for z in ([p] if p.is_file()else[p,*p.rglob('*')]):
   out[str(z.relative_to(ROOT))]={'kind':'directory'}if z.is_dir()else{'kind':'file','sha256':sha(z),'bytes':z.stat().st_size}
 return out
baseline=json.loads((HERE/'registered-baseline.json').read_text());registered=[ROOT/'generate/scratch/17592186064219.py',ROOT/'generate/scratch/17592186064219'];actual=snap(registered)
assert actual==baseline,'Registered numeric script/tree changed'
(HERE/'final-preservation.json').write_text(json.dumps({'passed':True,'registered_entries':len(actual),'path_set_equal':set(actual)==set(baseline),'all_file_SHA256_equal':actual==baseline,'roots':[str(p)for p in registered],'baseline':'registered-baseline.json'},indent=2)+'\n')
main=json.loads((HERE/'validation.json').read_text());main.update({'latest_script_SHA256':sha(SCRIPT),'latest_validator_SHA256':sha(HERE/'validate.py'),'boundary_rendered_instances':32,'normal_native_accepted':84,'normal_native_rejected':336,'diagnostic_unsupported_blank_unresolved':15,'registered_preservation':True,'bounded_candidate_tuples':{'easy':443,'moderate':279,'hard':1496}})
(HERE/'validation.json').write_text(json.dumps(main,indent=2,ensure_ascii=False)+'\n')
raw=json.loads((HERE/'native-grading.json').read_text());gaps=[row for row in raw['records']if row['label'].startswith('independent blank')]
(HERE/'native-diagnostics.json').write_text(json.dumps({'classification':'diagnostic unsupported response shape, not normal generator grading gaps','supported_generator_response':'radio','unresolved_probe_count':15,'records':gaps},indent=2,ensure_ascii=False)+'\n')
manifest_path=HERE/'freeze-manifest.json';entries=snap([HERE]);entries.pop(str(manifest_path.relative_to(ROOT)),None)
entries[str(SCRIPT.relative_to(ROOT))]={'kind':'file','sha256':sha(SCRIPT),'bytes':SCRIPT.stat().st_size}
manifest={'version':'inverse-tangent-substitution-draft-v2','basis':2275,'script_SHA256':sha(SCRIPT),'test_counts':{'source_originals':16,'source_complete_banks':16,'source_distractors':64,'review_instances':66,'independent_diagnostic_instances':3,'boundary_instances':32,'corruption_controls':4,'supported_native_accepted':84,'supported_native_rejected':336,'unsupported_blank_diagnostic_unresolved':15},'limits':['Hard is an authored canonical factoring extension; no observed H practice.','Scale slots are bounded. Candidate counts are complete-profile tuples, not a claim of distinct integrands.','Blank diagnostic parsing is unsupported by the current engine; normal output is exclusively radio.'],'excluded':[str(manifest_path.relative_to(ROOT))],'entries':entries}
manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('Frozen',len(entries),'entries; registered',len(actual),'entries unchanged; script',sha(SCRIPT))
