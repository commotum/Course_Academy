"""Hash every owned file recursively; manifest deliberately excludes itself."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
manifest=HERE/'freeze-manifest.json'
files=[HERE.with_suffix('.py'),*sorted(p for p in HERE.rglob('*') if p.is_file() and p!=manifest)]
entries={str(p.relative_to(ROOT)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in files}
manifest.write_text(json.dumps({'knowledge_point':17592186064207,'basis':2275,'files':entries,'directories':[str(HERE.relative_to(ROOT)),*[str(p.relative_to(ROOT)) for p in sorted(HERE.rglob('*')) if p.is_dir()]],'self_excluded':'freeze-manifest.json','numeric_tree_baseline':'numeric-baseline.json','database_writes':0},indent=2)+'\n')
print(json.dumps({'files':len(entries),'script_sha256':entries[str(HERE.with_suffix('.py').relative_to(ROOT))]['sha256'],'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest()}))
