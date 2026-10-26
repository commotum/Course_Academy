from pathlib import Path
import json,sys,shutil
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import Publisher
from generator_packages import resolve_registered_script
p=Publisher.from_environment(source=':agent/codex')
for item in json.loads((H/'capture.json').read_text())['knowledge_points']:
 kp=item['kp'];proof=json.loads((H/str(kp)/'verification.json').read_text());assert proof['passed'];entry=resolve_registered_script(proof['new_reference'],ROOT,p.config.math_root);local=ROOT/f'generate/scratch/{kp}'
 for name in json.loads((entry.parent/'generator-package.json').read_text())['files']:shutil.copy2(entry.parent/name,local/name)
 (local/'README.md').write_text(f'# Continuous compounding — KP {kp}\n\nSource-sized choice spacing is checked after rounding. Initial-amount alternatives encode calculation errors; rate/time alternatives preserve independent bank-first sampling. Full precision is kept until the final result. Existing source-supported moderate scope is retained.\n\nPublication and verification: `reference/edb-math/repairs/2026-10-26-compound-interest-answer-spacing/`.\n')
 wrapper=ROOT/f'generate/scratch/{kp}.py';wrapper.write_text('import runpy,sys\nfrom pathlib import Path\nLOCAL=Path(__file__).with_suffix("")\nsys.path.insert(0,str(LOCAL))\nif __name__=="__main__":runpy.run_path(str(LOCAL/"generator.py"),run_name="__main__")\n');print(kp,'installed verified published package')
