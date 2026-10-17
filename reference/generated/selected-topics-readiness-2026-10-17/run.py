"""Run the bounded native checker read-only at the captured input basis."""
from pathlib import Path
import json,subprocess,sys,threading
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient
HERE=ROOT/'reference/generated/selected-topics-readiness-2026-10-17'
command=json.loads((HERE/'readiness-build-command.json').read_text())
binary=ROOT/command[-1]
assert binary.stat().st_mtime_ns >= (HERE/'readiness.rs').stat().st_mtime_ns, 'Recompile checker first'
db=EDBClient(Config(capture_only=True),threading.Event())
subprocess.run([str(binary),str(HERE/'input.json'),str(HERE/'result.json')],cwd=ROOT,env=db.environment,check=True)
result=json.loads((HERE/'result.json').read_text())
assert result['database_writes']==0 and result['learner_attempts_created']==0 and result['read_scope']['global_attribute_scans']==0
