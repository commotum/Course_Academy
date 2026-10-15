"""Compile current engine source and runner into owned draft paths only."""
from pathlib import Path
import hashlib,json,os,subprocess
D=Path(__file__).resolve().parent;R=D.parents[2];deps=R/'target/release/deps';lib=D/'reference/libcourse_academy_engine.rlib';src=R/'generate/runs/current/check-engine.rs';out=D/'check-engine'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources={str(p.relative_to(R)):h(p) for p in (R/'engine/rust').rglob('*') if p.is_file()}
command=['rustc','--crate-name','course_academy_engine','--edition=2024','--crate-type','rlib','-C','opt-level=1',str(R/'engine/rust/lib.rs'),'-L','dependency='+str(deps),'-o',str(lib)]
externs={}
for name in ['serde','serde_json','sha2','chrono','csv','regex','num_bigint','num_rational','num_traits','uuid','roxmltree']:
 files=list(deps.glob('lib'+name+'-*.rlib'));assert len(files)==1,(name,files);externs[name]=files[0];command+=['--extern',name+'='+str(files[0])]
subprocess.run(command,check=True,env={**os.environ,'CARGO_MANIFEST_DIR':str(R)})
assert sources=={str(p.relative_to(R)):h(p) for p in (R/'engine/rust').rglob('*') if p.is_file()},'source changed during compile'
subprocess.run(['rustc','--edition=2024','-O',str(src),'--extern','course_academy_engine='+str(lib),'--extern','serde_json='+str(externs['serde_json']),'-L','dependency='+str(deps),'-o',str(out)],check=True)
(D/'reference/grader-build.json').write_text(json.dumps({'source':str(src.relative_to(R)),'source_sha256':h(src),'library':str(lib.relative_to(R)),'library_sha256':h(lib),'binary':str(out.relative_to(R)),'binary_sha256':h(out),'engine_sources':sources,'dependencies':{str(p.relative_to(R)):h(p) for p in externs.values()},'command':command,'build_scope':'Current engine/rust/lib.rs compiled directly against existing dependency rlibs; output only in owned draft. No shared engine/target modifications. Source hashes checked before and after compilation.'},indent=2)+'\n')
