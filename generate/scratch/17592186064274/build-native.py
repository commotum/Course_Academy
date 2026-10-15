import hashlib,json,subprocess
from pathlib import Path
here=Path(__file__).resolve().parent;root=here.parents[2];deps=root/'target/release/deps'
# Use the current application's already built engine library, never alter app code.
libs={n:max(deps.glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for n in ('course_academy_engine','serde_json')}
for name,source in [('check-engine',root/'generate/runs/current/check-engine.rs'),('check-pool',root/'generate/scratch/17592186068841/check-pool.rs')]:
 target=here/(name+'.rs');target.write_bytes(source.read_bytes())
 cmd=['rustc','--edition=2024','-O',str(target)]
 for n,p in libs.items():cmd+=['--extern',n+'='+str(p)]
 cmd+=['-L','dependency='+str(deps),'-o',str(here/name)]
 subprocess.run(cmd,check=True)
files=list(libs.values())+[here/'check-engine',here/'check-engine.rs',here/'check-pool',here/'check-pool.rs',root/'engine/rust/learning.rs',root/'engine/rust/symbolic.rs']
(here/'reference/native-build.json').write_text(json.dumps({'libraries':{n:str(p.relative_to(root)) for n,p in libs.items()},'sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2))
