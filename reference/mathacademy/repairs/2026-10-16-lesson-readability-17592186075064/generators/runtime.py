"""Read actual registered paths and inspect pending local pipeline requests."""
import hashlib
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from scripts.config import Config
from scripts.database.client import EDBClient

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
db = EDBClient(Config(), threading.Event())
identity = db.status()
ids = [17592186073777, 17592186073778]
rows = db.query('[:find (pull ?kp [:db/id :knowledge-point/id {:knowledge-point/question-generator [*]}]) :in $ [?kp ...] :where [?kp :knowledge-point/id _]]', [ids], HERE / 'runtime-evidence', 'registrations', identity['basis'])
jobs = []
for location in (ROOT / '.local/generation', ROOT / '.local/learning/inventory'):
    if location.exists():
        for path in location.rglob('*.json'):
            try:
                obj = json.loads(path.read_text())
            except (ValueError, OSError):
                continue
            if isinstance(obj, dict) and str(obj.get('kp_id', obj.get('knowledge_point_id', ''))) in set(map(str, ids)):
                jobs.append({'file': str(path.relative_to(ROOT)), 'status': obj.get('status'), 'data': obj})
result = {'identity': identity, 'registrations': rows, 'matching_local_job_files': jobs, 'checked_at': datetime.now(timezone.utc).isoformat(),
          'runtime_scripts': [{'knowledge_point': kp, 'path': f'generate/scratch/{kp}.py', 'sha256': hashlib.sha256((ROOT / f'generate/scratch/{kp}.py').read_bytes()).hexdigest()} for kp in ids]}
(HERE / 'runtime.json').write_text(json.dumps(result, indent=2, default=str) + '\n')
print(json.dumps(result, indent=2, default=str))
