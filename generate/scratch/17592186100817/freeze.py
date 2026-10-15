#!/usr/bin/env python3
"""Freeze complete owned script and tree; only this manifest is self-excluded."""
import sys
sys.dont_write_bytecode=True
import json,hashlib
from pathlib import Path
H=Path(__file__).parent;SCRIPT=H.with_suffix('.py');MANIFEST=H/'freeze-manifest.json'
paths=[SCRIPT]+sorted(p for p in H.rglob('*')if p.is_file()and p!=MANIFEST)
rows=[{'path':str(p.relative_to(H.parent)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in paths]
manifest={'algorithm':'sha256','whole_owned_tree':True,'only_exclusion':str(MANIFEST.relative_to(H.parent)),'file_count':len(rows),'files':rows,'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'baseline_sha256':hashlib.sha256((H/'pre-import-baseline.json').read_bytes()).hexdigest(),'source_wrapper_sha256':hashlib.sha256((H/'source.json').read_bytes()).hexdigest()}
MANIFEST.write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({k:manifest[k]for k in('file_count','script_sha256','baseline_sha256','source_wrapper_sha256')},indent=2))
