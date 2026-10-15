#!/usr/bin/env python3
"""Verify complete immutable numeric package and seal only this private draft."""
import sys
sys.dont_write_bytecode=True
import json,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[2];S=R/'generate/scratch';K='17592186092263'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((D/'numeric-baseline.json').read_text())['files']
paths=[S/(K+'.py'),*(S/K).rglob('*'),*(S/'__pycache__').glob(K+'.*.pyc')]
now={str(p.relative_to(R)):sha(p) for p in sorted(paths) if p.is_file()}
assert now==old,{'added':sorted(now.keys()-old.keys()),'removed':sorted(old.keys()-now.keys()),'changed':[p for p in now.keys()&old.keys() if now[p]!=old[p]]}
build=json.loads((D/'reference/grader-build.json').read_text());native={build['source']:build['source_sha256'],build['library']:build['library_sha256'],build['binary']:build['binary_sha256'],**build['engine_sources'],**build['dependencies']}
assert len(native)==42 and all(sha(R/p)==h for p,h in native.items())
(D/'numeric-baseline-verification.json').write_text(json.dumps({'status':'unchanged','files':len(now),'full_pathset_equal':True,'recursive_numeric_tree_and_caches':True,'matching_sibling_bytecode_caches':True,'numeric_script_sha256':now['generate/scratch/'+K+'.py'],'baseline_sha256':sha(D/'numeric-baseline.json'),'current_native_build_inputs_verified':42},indent=2)+'\n')
files=[D.with_suffix('.py'),*(p for p in D.rglob('*') if p.is_file() and p.name!='freeze.json')]
hashes={str(p.relative_to(R)):sha(p) for p in sorted(files)}
(D/'freeze.json').write_text(json.dumps({'status':'frozen_pending_independent_root_review','generator_sha256':sha(D.with_suffix('.py')),'files':hashes,'file_count':len(hashes),'all_owned_files_except_self':True,'numeric_baseline_status':'unchanged','native_binary_sha256':build['binary_sha256'],'native_limit':'One explicit wrong1 comparison unresolved; never counted as a rejection.'},indent=2)+'\n')
print(json.dumps({'owned_files':len(hashes),'numeric_files_unchanged':len(now),'generator_sha256':sha(D.with_suffix('.py')),'freeze_sha256':sha(D/'freeze.json')}))
