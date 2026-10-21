from pathlib import Path
import subprocess,json,hashlib
W=Path(__file__).resolve().parents[1]
repo=next(p for p in W.parents if (p/'Cargo.toml').exists())
commands=[['cargo','build','--release','--lib']]
r=subprocess.run(commands[0],cwd=repo,capture_output=True,text=True)
(W/'evidence/engine-build.log').write_text(r.stdout+r.stderr);r.check_returncode()
deps=repo/'target/release/deps'
lib=max(deps.glob('libcourse_academy_engine-*.rlib'),key=lambda p:p.stat().st_mtime)
serde=max(deps.glob('libserde_json-*.rlib'),key=lambda p:p.stat().st_mtime)
cmd=['rustc','--edition=2024',str(repo/'generate/runs/current/check-engine.rs'),'-L','dependency='+str(deps),'--extern','course_academy_engine='+str(lib),'--extern','serde_json='+str(serde),'-o',str(repo/'generate/runs/current/check-engine')]
commands.append(cmd);subprocess.run(cmd,cwd=repo,check=True)
files=[lib,serde,repo/'engine/rust/symbolic.rs',repo/'generate/runs/current/check-engine.rs',repo/'generate/runs/current/check-engine']
(W/'evidence/native-build.json').write_text(json.dumps({'commands':commands,'sha256':{str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
print('Rebuilt shared native grader')
