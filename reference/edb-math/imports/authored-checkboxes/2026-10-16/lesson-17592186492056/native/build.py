"""Build read-only preview and grading helpers against the deployed libraries."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from capture.scripts.config import Config
from capture.scripts.database.preview import _library

digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
library = _library(Config())
preview = HERE / 'preview'
command = ['rustc', '--edition=2024', '-O', str(HERE / 'preview.rs'),
           '--extern', 'edb_core=' + str(library), '-L', 'dependency=' + str(library.parent),
           '-o', str(preview)]
subprocess.run(command, check=True, capture_output=True, text=True)
subprocess.run(['cargo', 'build', '--offline', '--lib'], cwd=ROOT,
               check=True, capture_output=True, text=True)
deps = ROOT / 'target/debug/deps'
engine = ROOT / 'target/debug/libcourse_academy_engine.rlib'
# Cargo's current engine links the only present debug serde_json artifact.
serde_candidates = list(deps.glob('libserde_json*.rlib'))
assert len(serde_candidates) == 1, 'Resolve the exact serde_json dependency before compiling'
serde = serde_candidates[0]
grading = HERE / 'check-checkbox-engine'
grade_command = ['rustc', '--edition=2024', '-O', str(HERE / 'check-checkbox-engine.rs'),
                 '-L', 'dependency=' + str(deps), '--extern', 'course_academy_engine=' + str(engine),
                 '--extern', 'serde_json=' + str(serde), '-o', str(grading)]
subprocess.run(grade_command, check=True, capture_output=True, text=True)
files = [HERE / 'preview.rs', HERE / 'check-checkbox-engine.rs', library, engine, serde,
         ROOT / 'engine/edb/answer_fields.rs', ROOT / 'engine/edb/configuration.rs',
         ROOT / 'engine/edb/progress.rs']
manifest = {'database_writes': 0, 'preview_binary': str(preview), 'grading_binary': str(grading),
            'commands': [command, grade_command], 'input_hashes': {str(p): digest(p) for p in files},
            'binary_hashes': {str(p): digest(p) for p in [preview, grading]}}
(HERE / 'build.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'built': True, 'database_writes': 0, 'preview': str(preview), 'grading': str(grading)}))
