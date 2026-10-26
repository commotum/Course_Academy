from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import Publisher,jsonable
from generator_packages import resolve_registered_script
p=Publisher.from_environment(source=':agent/codex');status=p.client.status();basis=status['basis'];rows=[]
for kp in(17592186059796,17592186059797,17592186059798):
 d=H/str(kp);k=p.read_kp(kp,d/'capture',basis);p._source_from_kp(kp,d/'fresh-source',status,basis,k);k=jsonable(k);(d/'before.json').write_text(json.dumps(k,indent=2)+'\n');ref=k[':knowledge-point/question-generator'][':question-generator/script'];entry=resolve_registered_script(ref,ROOT,p.config.math_root)
 import shutil
 package=d/'package';package.mkdir(exist_ok=True);manifest=json.loads((entry.parent/'generator-package.json').read_text())
 for name in manifest['files']:
  out=package/name
  if out.exists():out.chmod(out.stat().st_mode|0o200)
  shutil.copy2(entry.parent/name,out);out.chmod(out.stat().st_mode|0o200)
 rows.append({'kp':kp,'title':k[':knowledge-point/title'],'registered_generator':ref,'files':list(manifest['files']),'active_generated':len([q for q in k[':knowledge-point/questions']if not q.get(':question/math-academy-id')and not q.get(':question/retired')])})
(H/'capture.json').write_text(json.dumps({'basis':basis,'knowledge_points':rows},indent=2)+'\n');print('Captured three financial generators at',basis)
