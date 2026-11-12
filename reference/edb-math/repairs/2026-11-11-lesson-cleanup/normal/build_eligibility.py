"""Build offline native inventory eligibility helper with exact artifact identity."""
import hashlib,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];deps=ROOT/'target/debug/deps';lib=max(deps.glob('libcourse_academy_engine*.rlib'),key=lambda p:p.stat().st_mtime);sj=next(deps.glob('libserde_json*.rlib'))
cmd=['rustc','--edition=2021',str(H/'eligibility.rs'),'-L','dependency='+str(deps),'--extern','course_academy_engine='+str(lib),'--extern','serde_json='+str(sj),'-o',str(H/'eligibility')];subprocess.run(cmd,check=True)
files=[H/'eligibility.rs',H/'eligibility',lib,sj,*sorted((ROOT/'engine/rust').glob('*.rs'))];report=dict(command=cmd,compiler=subprocess.check_output(['rustc','-Vv'],text=True).strip(),sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},database_writes=0);(H/'eligibility-build.json').write_text(json.dumps(report,indent=2)+'\n')
