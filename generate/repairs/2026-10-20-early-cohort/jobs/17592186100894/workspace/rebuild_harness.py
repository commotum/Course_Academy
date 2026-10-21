"""Rebuild only the authorized offline native grader after cargo build --release --lib."""
import pathlib,subprocess,json,hashlib
w=pathlib.Path(__file__).resolve().parent;root=w.parents[5];deps=root/'target/release/deps';args=['rustc','--edition=2024','-O',str(root/'generate/runs/current/check-engine.rs'),'-L','dependency='+str(deps),'-o',str(root/'generate/runs/current/check-engine')]
libs={}
for name in ('serde_json','course_academy_engine'):
 lib=max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime);args+=['--extern',name+'='+str(lib)];libs[name]={'path':str(lib.relative_to(root)),'sha256':hashlib.sha256(lib.read_bytes()).hexdigest()}
p=subprocess.run(args,capture_output=True,text=True);(w/'evidence-author-3/harness-build.json').write_text(json.dumps({'command':args,'libraries':libs,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr},indent=2));print('harness rebuild',p.returncode);p.check_returncode()
