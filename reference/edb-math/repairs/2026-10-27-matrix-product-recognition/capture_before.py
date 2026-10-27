from pathlib import Path
import json,sys,shutil
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import Publisher,jsonable
from generator_packages import resolve_registered_script
p=Publisher.from_environment(source=':agent/codex');status=p.client.status();basis=status['basis'];kp=17592186059747
k=p.read_kp(kp,H/'capture',basis);p._source_from_kp(kp,H/'fresh-source',status,basis,k);k=jsonable(k)
(H/'before.json').write_text(json.dumps(k,indent=2)+'\n')
ref=k[':knowledge-point/question-generator'][':question-generator/script'];entry=resolve_registered_script(ref,ROOT,p.config.math_root)
package=H/'package';package.mkdir(exist_ok=True);manifest=json.loads((entry.parent/'generator-package.json').read_text())
for name in manifest['files']:
 out=package/name;shutil.copy2(entry.parent/name,out);out.chmod(out.stat().st_mode|0o200)
active=[q for q in k[':knowledge-point/questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired')]
rows=p.client.query('[:find (pull ?q [:db/id :question/id {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',[[q[':db/id'] for q in active]],H/'capture','old-generated-usage',basis)
data={'basis':basis,'kp':kp,'title':k[':knowledge-point/title'],'registered_generator':ref,'files':list(manifest['files']),'active_generated':len(active),'usage':jsonable([r[0] for r in rows])}
(H/'capture.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({key:value for key,value in data.items() if key!='usage'}));print('Task-linked:',[q[':db/id'] for q in data['usage'] if q.get(':task-item/_content')])
