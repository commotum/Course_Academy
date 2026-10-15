"""Build scoped checks through the existing application engine."""
import sys,json,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from serve_graph_explorer import build_learning
learning=build_learning(ROOT.parent/'EDB')
libs={n:max((ROOT/'target/release/deps').glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for n in ('course_academy_engine','serde_json')}
for name,src in [('check-engine',ROOT/'generate/runs/current/check-engine.rs'),('check-pool',ROOT/'generate/scratch/17592186068841/check-pool.rs')]:
    target=HERE/'reference'/name
    subprocess.run(['rustc','--edition=2024','-O',str(src),*[x for n,p in libs.items() for x in ('--extern',n+'='+str(p))],'-L','dependency='+str(ROOT/'target/release/deps'),'-o',str(target)],check=True)
paths=list(libs.values())+[learning,HERE/'reference/check-engine',HERE/'reference/check-pool']
(HERE/'reference/native-build.json').write_text(json.dumps({'learning':str(learning),'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}},indent=2)+'\n')
print(learning)
