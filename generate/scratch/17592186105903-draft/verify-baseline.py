"""Verify the registered numeric script/tree/cache remain exactly unchanged."""
import sys
sys.dont_write_bytecode=True
import hashlib,json
from pathlib import Path
D=Path(__file__).resolve().parent
base=D.parent;kp='17592186105903'
paths=[base/(kp+'.py')]+sorted((base/kp).rglob('*'))+sorted((base/'__pycache__').glob(kp+'.*.pyc'))
repo=D.parents[2]
actual={str(p.relative_to(repo)):{'kind':'file','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size} if p.is_file() else {'kind':'directory'} for p in paths}
expected=json.loads((D/'immutable-baseline.json').read_text())
assert actual==expected,'Registered numeric script/tree/cache changed'
print(json.dumps({'status':'passed','paths':len(actual),'files':sum(v['kind']=='file' for v in actual.values())}))
