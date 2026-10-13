import hashlib, json, subprocess
from pathlib import Path
P = Path(__file__).resolve().parent
R = P.parents[2]
subprocess.run(['cargo', 'build', '--release', '--lib'], cwd=R, check=True)
libs = list((R / 'target/release/deps').glob('libcourse_academy_engine-*.rlib'))
serde = list((R / 'target/release/deps').glob('libserde_json-*.rlib'))
assert len(libs) == len(serde) == 1
src = R / 'generate/runs/current/check-engine.rs'
exe = P / 'check-engine'
subprocess.run(['rustc', '--edition=2024', '-O', str(src), '--extern', 'course_academy_engine=' + str(libs[0]), '--extern', 'serde_json=' + str(serde[0]), '-L', 'dependency=' + str(libs[0].parent), '-o', str(exe)], check=True)
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
(P / 'reference/grader-build.json').write_text(json.dumps({
    'source': str(src.relative_to(R)), 'source_sha256': h(src),
    'library': str(libs[0].relative_to(R)), 'library_sha256': h(libs[0]),
    'binary': str(exe.relative_to(R)), 'binary_sha256': h(exe),
    'engine_sources': {str(p.relative_to(R)): h(p) for p in (R / 'engine/rust').glob('*.rs')},
}, indent=2) + '\n')
