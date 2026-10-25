from pathlib import Path
import sys,json,shutil
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import Publisher
from generator_packages import resolve_registered_script
p=Publisher.from_environment(source=':agent/codex')
for row in json.loads((H/'capture.json').read_text())['knowledge_points']:
 kp=row['kp'];d=H/str(kp);proof=json.loads((d/'verification.json').read_text());assert proof['passed'];entry=resolve_registered_script(proof['new_reference'],ROOT,p.config.math_root);manifest=json.loads((entry.parent/'generator-package.json').read_text());local=ROOT/'generate/scratch'/str(kp)
 for name in manifest['files']:shutil.copy2(entry.parent/name,ROOT/f'generate/scratch/{kp}.py'if name=='generator.py'else local/name)
 (local/'capabilities.json').write_text(json.dumps({'supported_levels':['easy','moderate','hard'],'implementation_version':'inverse-substitution-quality-4','band_contract':'band-contract.json','maximum_records_per_call':100},indent=2)+'\n')
 (local/'README.md').write_text(f'# Inverse substitution — KP {kp}\n\nComplete calculation with no supplied substitution. Diagnostic answer choices, cancellation-aware difficulty and balanced familiar endpoint profiles. Imported labels remain unchanged; indefinite sine/tangent hard bands are explicit authored extrapolations.\n\nPublished package and verification: `reference/edb-math/repairs/2026-10-25-inverse-trig-quality/`. Older reports are historical.\n')
 print(kp,'published mirror installed')
