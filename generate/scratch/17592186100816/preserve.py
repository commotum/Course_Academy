"""Read-only comparison of all pre-import numeric paths. Own pair only writes."""
import hashlib,json
from pathlib import Path
H=Path(__file__).parent;baseline=json.loads((H/'pre-import-baseline.json').read_text());changes=[];missing=[]
for name,expected in baseline['numeric_paths_sha256'].items():
 p=Path(name)
 if not p.exists():missing.append(name)
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=expected:changes.append(name)
(H/'final-preservation.json').write_text(json.dumps({'preexisting_numeric_files_checked':len(baseline['numeric_paths_sha256']),'changed_preexisting_paths':changes,'missing_preexisting_paths':missing,'scope':'Whole pre-import numeric tree baseline compared read-only; concurrent workers may own independent new pairs. This worker writes only KP00816 pair.','engine_current_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'source_wrapper_exact':Path('generate/runs/current/refresh-2026-10-14/sources/17592186100816.json').read_bytes()==(H/'source.json').read_bytes()},indent=2)+'\n')
print(len(changes),len(missing))
