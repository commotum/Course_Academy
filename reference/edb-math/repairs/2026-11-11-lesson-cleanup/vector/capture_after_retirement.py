import sys,json
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from scripts.generator_publish import Publisher,jsonable
from capture.scripts.storage import file_lock,atomic_json
p=Publisher.from_environment(source=':agent/codex')
for kp in [17592186096652,17592186096653,17592186096701,17592186235285]:
 with file_lock(ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'/f'kp-{kp}.lock',blocking=False):
  d=H/str(kp);s=p.client.status();q=jsonable(p.read_kp(kp,d/'capture-after-retirement',s['basis']));atomic_json(d/'capture-after-retirement/kp.json',q);atomic_json(d/'capture-after-retirement/status.json',s);p.save_inventory(kp,q,s,s['basis'],d/'capture-after-retirement');p.extract_source(kp,d/'source',basis=s['basis']);print(kp,s['basis'],flush=True)
