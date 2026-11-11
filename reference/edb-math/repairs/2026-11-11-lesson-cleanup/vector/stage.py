import json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from scripts.generator_publish import Publisher,jsonable
from capture.scripts.storage import file_lock,atomic_json
AUDIT=ROOT/'generate/reports/lesson-quality-audit-2026-11-11/vector'
p=Publisher.from_environment(source=':agent/codex')
for kp in [17592186096652,17592186096653,17592186096701,17592186235285]:
 d=H/str(kp);d.mkdir(exist_ok=True)
 lock=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock'
 with file_lock(lock,blocking=False):
  status=p.client.status();baseline=jsonable(p.read_kp(kp,d/'capture',status['basis']))
  atomic_json(d/'capture/status.json',status);atomic_json(d/'capture/kp.json',baseline)
  p.save_inventory(kp,baseline,status,status['basis'],d/'capture')
  p.extract_source(kp,d/'source-before',basis=status['basis'])
  old=p.config.math_root/baseline[':knowledge-point/question-generator'][':question-generator/script'];manifest=json.loads((old.parent/'generator-package.json').read_text())
  package=d/'package';package.mkdir(exist_ok=True)
  for f in manifest['files']:shutil.copy2(old.parent/f,package/f);(package/f).chmod(0o644)
  atomic_json(package/'package.json',dict(entrypoint=manifest['entrypoint'],files=list(manifest['files']),dependencies=manifest['dependencies']))
 print(kp,'captured',status['basis'],flush=True)
