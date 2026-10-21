"""Compile a read-only repair calculation against the actual application code."""
from pathlib import Path
import subprocess, tempfile, hashlib, json
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Cargo.toml').exists())
subprocess.run(['cargo','build','--release','--lib','--offline'],cwd=ROOT,check=True)
source=(ROOT/'scripts/learning_api.rs').read_text().replace('//! Local learner application boundary:', '// Local learner application boundary:',1)
for module in ['activity_history','study_stats','assignment_interaction','assignment_reader','developer_preview','page_reader','quiz_labels']:
    source=source.replace(f'mod {module};',f'#[path = "{ROOT}/scripts/{module}.rs"]\nmod {module};',1)
assert source.count('fn main() {')==1
source=source.replace('fn main() {','fn unused_application_main() {',1)
compiled=source+'\n'+(HERE/'correction_tail.rs').read_text().replace('REPO_ROOT',str(ROOT))
generated=Path(tempfile.mkdtemp(prefix='echelon-correction-'))/'repair.rs';generated.write_text(compiled)
edb=ROOT.parent/'EDB/target/release/deps';deps=ROOT/'target/release/deps'
libraries={name:max(folder.glob(f'lib{name}-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name,folder in [('edb_core',edb),('serde',deps),('serde_json',deps),('chrono',deps),('course_academy_engine',deps)]}
cmd=['rustc','--edition=2024','-O','-A','dead_code',str(generated)]
for name,path in libraries.items():cmd+=['--extern',f'{name}={path}']
cmd+=['-L',f'dependency={edb}','-L',f'dependency={deps}','-o',str(HERE/'correction')]
subprocess.run(cmd,check=True)
(HERE/'build.json').write_text(json.dumps({'application_sha256':hashlib.sha256((ROOT/'scripts/learning_api.rs').read_bytes()).hexdigest(),'generated_sha256':hashlib.sha256(compiled.encode()).hexdigest(),'command':cmd},indent=2)+'\n')
