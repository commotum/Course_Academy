"""Freeze the complete owned draft after validation and immutable baseline audit."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;ROOT=D.parents[2];S=D.with_suffix('.py')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((D/'registered-baseline.json').read_text())
paths=[D.parent/'17592186059829.py']+list((D.parent/'17592186059829').rglob('*'))+list((D.parent/'__pycache__').glob('17592186059829.*.pyc'))
actual={str(p.relative_to(ROOT)):h(p) for p in sorted(paths) if p.is_file()};assert actual==b
v=json.loads((D/'validation.json').read_text());assert v['generator_sha256']==h(S)
c=json.loads((D/'cli-validation.json').read_text());assert c['generator_sha256']==h(S)
vis=json.loads((D/'visual-review.json').read_text());assert vis['final_generator_sha256']==h(S)
files=[S]+[p for p in D.rglob('*') if p.is_file() and p.name!='freeze-manifest.json']
manifest={'kp_id':17592186059829,'scope':'draft only; steps3–7; independent root QA pending','generator_sha256':h(S),'registered_baseline_files':len(b),'registered_pathset_hashes_unchanged':True,'files':{str(p.relative_to(ROOT)):h(p) for p in sorted(files)},'exclusion':'Only freeze-manifest.json itself is excluded to avoid recursive self-hashing.'}
(D/'freeze-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Frozen',len(files),'owned draft files; registered104-file pathset/hash baseline unchanged; generatorSHA',h(S))
