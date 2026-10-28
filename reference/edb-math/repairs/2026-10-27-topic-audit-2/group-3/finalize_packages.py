import json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from generator_packages import build_manifest,manifest_digest,verify_package
H=Path(__file__).resolve().parent;rows=json.loads((H/'generator-candidates.json').read_text());evidence={r['kp']:r for r in json.loads((H/'staged-generator-evidence.json').read_text())};reloc={r['kp']:r for r in json.loads((H/'generator-relocation-validation.json').read_text())}
for row in rows:
 p=Path(row['directory']);helper=p/'math_format.py';assert helper.read_bytes()==Path('scripts/question_capture/math_format.py').read_bytes()
 ev=json.loads((p/'repair-evidence.json').read_text())if(p/'repair-evidence.json').exists()else evidence[row['kp']];ev['relocation_proof']=reloc[row['kp']];ev['latest_shared_formatter_exact_bytes']=True;ev['raw_source_note']='Retained source JSON bytes unchanged. Existing raw-source APIs stay evidence-only; for the original three packages, their preexisting formatter route can normalize source display guards, so normalized replay presentation is distinct from original retained bytes.';(p/'repair-evidence.json').write_text(json.dumps(ev,indent=2));files=sorted(set(row['files'])|{'repair-evidence.json'});m=build_manifest(p,row['entrypoint'],files,dependencies=row['dependencies']);(p/'generator-package.json').write_text(json.dumps(m,indent=2)+'\n');digest=manifest_digest(m);verify_package(p,digest);row.update(files=files,approved_digest=digest)
(H/'generator-candidates.json').write_text(json.dumps(rows,indent=2));print([(r['kp'],r['approved_digest'])for r in rows])
