"""Freeze the complete owned pair, excluding only the self-referential manifest."""
import hashlib,json
from pathlib import Path
H=Path(__file__).parent;files=[H.with_suffix('.py')]+sorted(p for p in H.rglob('*')if p.is_file()and p.name!='freeze-manifest.json')
record={'script_sha256':hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((H/'source.json').read_bytes()).hexdigest(),'file_count':len(files),'files':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in files},'database_writes':0,'registered':False}
(H/'freeze-manifest.json').write_text(json.dumps(record,indent=2)+'\n');print(record['script_sha256'],record['file_count'])
