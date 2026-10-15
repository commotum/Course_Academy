"""Freeze this isolated review bundle after validation; no registered artifact writes."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
registered=H.parent/'17592186064250'
baseline=json.loads((H/'registered-baseline.json').read_text())
current={str(p.resolve()):sha(p) for p in [registered.with_suffix('.py'),*registered.rglob('*')] if p.is_file()}
assert baseline==current,'Registered baseline path set or contents changed'
validation=json.loads((H/'validation.json').read_text());assert validation['passed']
files=[H.with_suffix('.py'),*[p for p in H.rglob('*') if p.is_file() and p!=H/'freeze.json']]
manifest={'source_basis':2275,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','registered_artifact_unchanged':True,'registered_file_count':len(baseline),'recursive':True,'excluded':['freeze.json'],'files':{str(p.resolve()):sha(p) for p in sorted(files)}}
(H/'freeze.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Frozen',len(files),'files; numeric artifact unchanged.')
