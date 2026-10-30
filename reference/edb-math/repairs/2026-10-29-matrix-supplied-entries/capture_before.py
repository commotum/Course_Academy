from pathlib import Path
import json,sys,shutil
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from scripts.generator_packages import resolve_registered_script
p=Publisher.from_environment(source=':agent/codex');status=p.client.status();basis=status['basis']
k=p.read_kp(17592186115226,H/'capture',basis)
(H/'before.json').write_text(json.dumps(jsonable(k),indent=2)+'\n')
ref=k[':knowledge-point/question-generator'][':question-generator/script'];entry=resolve_registered_script(ref,ROOT,p.config.math_root)
manifest=json.loads((entry.parent/'generator-package.json').read_text())
for name in manifest['files']:
 out=H/'package'/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(entry.parent/name,out);out.chmod(out.stat().st_mode|0o200)
data={'basis':basis,'lineage':status['lineage'],'kp':k[':db/id'],'registered_generator':ref,'files':list(manifest['files']),'dependencies':manifest.get('dependencies')}
(H/'capture.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
print('Asterisk questions:',[(q[':db/id'],bool(q.get(':question/retired'))) for q in k[':knowledge-point/questions'] if '\\ast' in q.get(':question/problem','')])
