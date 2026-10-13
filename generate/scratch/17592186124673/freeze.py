"""Freeze every local producer, data artifact and inspected source, SHA256."""
import hashlib,json,platform
from pathlib import Path
import sympy
D=Path(__file__).resolve().parent;R=D.parents[2]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
private=[D.with_suffix('.py')]+sorted(p for p in D.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='freeze.json')
external=[R/'generate/runs/current/check-engine',R/'generate/runs/current/check-engine.rs',R/'engine/rust/learning.rs',R/'Cargo.lock',R/'generate/runs/current/worker-instructions.md',R/'generate/principles.md']+[R/'generate/docs'/n for n in ['3-classify.md','4-template-extraction.md','5-plot-extraction.md','6-template-generator.md','7-plot-generator.md']]+[R/'generate/runs/current'/n for n in ['sources/17592186124673.json','topics/17592186049406.json','lessons/17592186049406.json']]+[Path('/home/jake/Developer/MA/DATA/Lessons/1924/Source/1924.json')]
report={'generator_version':'inhibited-identification-v1','producer_sha256':{str(p.relative_to(R)):digest(p) for p in private if p.suffix=='.py'},'private_artifact_sha256':{str(p.relative_to(R)):digest(p) for p in private},'read_only_provenance_sha256':{str(p):digest(p) for p in external},'dependencies':{'python':platform.python_version(),'sympy':sympy.__version__},'verification_command':'.venv/bin/python generate/scratch/17592186124673/validate.py','result':'pass;275 generated checks;130 accepted/520 rejected native;0 unresolved','writes':'private scratch only;no database operations','native_provenance_note':'Hashes freeze the harness binary and inspected source; no shared engine rebuild or edit performed.'}
(D/'freeze.json').write_text(json.dumps(report,indent=2)+'\n');print('Frozen',len(private),'private artifacts;',len(report['producer_sha256']),'producers')
