"""Build small read-only adapters against the current application library."""
import hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
subprocess.run(['cargo','build','--release','--lib','--offline'],cwd=ROOT,check=True,timeout=55)
deps=ROOT/'target/release/deps'
libs={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime) for name in ('course_academy_engine','serde_json')}
for name in ['check-engine','check-pool']:
 src=HERE/'reference/native'/(name+'.rs');binary=HERE/'reference/native'/name
 args=['rustc','--edition=2024','-O',str(src),'-L','dependency='+str(deps),'-o',str(binary)]
 for lib,path in libs.items():args+=['--extern',lib+'='+str(path)]
 subprocess.run(args,check=True,cwd=ROOT,timeout=55)
 (binary.with_suffix('.build.json')).write_text(json.dumps({'source_sha256':sha(src),'binary_sha256':sha(binary),'libraries':{k:{'path':str(p),'sha256':sha(p)} for k,p in libs.items()}},indent=2)+'\n')
