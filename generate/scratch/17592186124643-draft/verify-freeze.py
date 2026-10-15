#!/usr/bin/env python3
"""Read-only complete owned-pathset and registered-absence verification."""
import sys;sys.dont_write_bytecode=True
import hashlib,json
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
freeze=json.loads((D/'freeze.json').read_text())
found={p.relative_to(R).as_posix() for p in D.rglob('*') if p.is_file() and p.name!='freeze.json'}|{D.with_suffix('.py').relative_to(R).as_posix()}
assert found=={x['path'] for x in freeze['files']},'Owned pathset changed'
for row in freeze['files']:assert sha(R/row['path'])==row['sha256'],row['path']+' changed'
base=json.loads((D/'immutable-baseline.json').read_text());found=set()
for p in [R/'generate/scratch/17592186124643.py',R/'generate/scratch/17592186124643']:
 if p.is_dir():found.update(x.relative_to(R).as_posix() for x in p.rglob('*') if x.is_file())
 elif p.is_file():found.add(p.relative_to(R).as_posix())
found.update(x.relative_to(R).as_posix() for x in (R/'generate/scratch/__pycache__').glob('17592186124643.*.pyc'))
assert found=={x['path'] for x in base['files']},'Registered numeric/cache baseline changed'
for row in base['files']:assert sha(R/row['path'])==row['sha256']
for name,source in [('source.json','sources/17592186124643.json'),('topics.json','topics/17592186048707.json'),('lessons.json','lessons/17592186048707.json')]:assert sha(D/name)==sha(R/'generate/runs/current/refresh-2026-10-14'/source)
print('Verified',len(freeze['files']),'owned immutable files; exact source wrappers; numeric script/tree/pycache absence remains intact.')
