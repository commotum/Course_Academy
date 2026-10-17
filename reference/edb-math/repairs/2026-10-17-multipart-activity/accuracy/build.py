"""Build an isolated read-only preview using the application's exact private functions.

The generated translation unit lives in /tmp, not in application source. The only
source transformations are explicit module paths and renaming the normal main.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
subprocess.run(['cargo', 'build', '--release', '--lib', '--offline'], cwd=ROOT, check=True)
source = (ROOT / 'scripts/learning_api.rs').read_text()
source = source.replace('//! Local learner application boundary:', '// Local learner application boundary:', 1)
for module in ['activity_history', 'study_stats', 'assignment_interaction', 'assignment_reader', 'developer_preview', 'page_reader']:
    source = source.replace(f'mod {module};', f'#[path = "{ROOT}/scripts/{module}.rs"]\nmod {module};', 1)
assert source.count('fn main() {') == 1
source = source.replace('fn main() {', 'fn unused_application_main() {', 1)
tail = (HERE / 'replay_tail.rs').read_text().replace('REPO_ROOT', str(ROOT))
compiled = source + '\n' + tail
generated = Path(tempfile.mkdtemp(prefix='multipart-accuracy-replay-')) / 'preview.rs'
generated.write_text(compiled)
edb_deps = ROOT.parent / 'EDB/target/release/deps'
deps = ROOT / 'target/release/deps'
libraries = {name: max(directory.glob(f'lib{name}-*.rlib'), key=lambda p: p.stat().st_mtime_ns)
             for name, directory in [('edb_core', edb_deps), ('serde', deps), ('serde_json', deps), ('chrono', deps), ('course_academy_engine', deps)]}
command = ['rustc', '--edition=2024', '-O', '-A', 'dead_code', str(generated)]
for name, path in libraries.items():
    command += ['--extern', f'{name}={path}']
command += ['-L', f'dependency={edb_deps}', '-L', f'dependency={deps}', '-o', str(HERE / 'preview')]
subprocess.run(command, check=True)
(HERE / 'build.json').write_text(json.dumps({
    'applicationSource': str(ROOT / 'scripts/learning_api.rs'),
    'applicationSha256': hashlib.sha256((ROOT / 'scripts/learning_api.rs').read_bytes()).hexdigest(),
    'generatedSha256': hashlib.sha256(compiled.encode()).hexdigest(),
    'libraries': {name: str(path) for name, path in libraries.items()},
    'binary': str(HERE / 'preview'),
    'readOnly': True,
}, indent=2) + '\n')
print(HERE / 'preview')
