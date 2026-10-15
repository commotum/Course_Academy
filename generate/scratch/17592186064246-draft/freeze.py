#!/usr/bin/env python3
"""Hash the whole owned draft plus numeric full path set; no shared writes."""
import hashlib,json,sys
from pathlib import Path
D=Path(__file__).resolve().parent;repo=D.parents[2];manifest=D/'freeze.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def current():
 rows={str(D.with_suffix('.py').relative_to(repo)):sha(D.with_suffix('.py'))}
 rows.update({str(p.relative_to(repo)):sha(p) for p in D.rglob('*') if p.is_file() and p!=manifest})
 return dict(sorted(rows.items()))
def immutable():
 before=json.load(open(D/'numeric-before-import.json'));root=D.parent;id='17592186064246';paths=([root/(id+'.py')] if (root/(id+'.py')).exists() else [])+list((root/id).rglob('*'))+list((root/'__pycache__').glob(id+'.*.pyc'));after={str(p):sha(p) for p in paths if p.is_file()};assert before['paths']==after,'numeric script/tree/cache full path set changed'
 if before['absent']:assert not (root/(id+'.py')).exists() and not (root/id).exists() and not list((root/'__pycache__').glob(id+'.*.pyc')),'numeric absence changed'
 proof=json.load(open(D/'reference/native-42-verification.json'));assert len(proof)==42
 for p,h in proof.items():assert sha(Path(p))==h,('native grader source/artifact changed',p)
 assert (D/'source.json').read_bytes()==(repo/'generate/runs/current/refresh-2026-10-14/sources/17592186064246.json').read_bytes(),'immutable primary source wrapper changed'
 return {'numeric_full_path_set_unchanged':True,'numeric_paths':after,'native_build_files_reverified':42,'native_binary_sha256':sha(D/'check-engine'),'source_wrapper_sha256':sha(D/'source.json')}
state=immutable()
if '--verify' in sys.argv:
 saved=json.load(open(manifest));assert saved['files']==current(),'owned draft freeze changed';print('Freeze verified:',len(saved['files']),'owned files; numeric path set unchanged; native42 unchanged.')
else:
 state.update({'files':current(),'script_sha256':sha(D.with_suffix('.py')),'database_writes':0,'registered':False,'step':'7: local generator draft and QA only'});manifest.write_text(json.dumps(state,indent=2)+'\n');print('Frozen',len(state['files']),'owned files. Script SHA256:',state['script_sha256'])
