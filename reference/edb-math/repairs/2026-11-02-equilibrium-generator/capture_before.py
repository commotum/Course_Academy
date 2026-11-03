import json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from scripts.generator_packages import resolve_registered_script
p=Publisher.from_environment(source=':agent/codex');status=p.client.status();basis=status['basis'];kp=17592186166788
k=p.read_kp(kp,H/'capture',basis);p._source_from_kp(kp,H/'source',status,basis,k)
(H/'before.json').write_text(json.dumps(jsonable(k),indent=2)+'\n')
topic=p.client.query('[:find (pull ?t [:db/id :topic/title {:topic/knowledge-points [:db/id :knowledge-point/title {:knowledge-point/question-generator [*]}]}]) :in $ ?t :where [?t :topic/id _]]',[17592186051068],H/'capture','topic',basis)[0][0]
(H/'topic.json').write_text(json.dumps(jsonable(topic),indent=2)+'\n')
ref=k[':knowledge-point/question-generator'][':question-generator/script'];entry=resolve_registered_script(ref,ROOT,p.config.math_root);manifest=json.loads((entry.parent/'generator-package.json').read_text())
for name in manifest['files']:
 out=H/'package'/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(entry.parent/name,out);out.chmod(out.stat().st_mode|0o200)
active=[q for q in k[':knowledge-point/questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired')]
usage=p.client.query('[:find (pull ?q [:db/id {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',[[q[':db/id'] for q in active]],H/'capture','usage',basis)
data={'basis':basis,'lineage':status['lineage'],'kp':kp,'registered_generator':ref,'files':list(manifest['files']),'dependencies':manifest['dependencies'],'active_generated':[q[':db/id'] for q in active],'used':[r[0][':db/id'] for r in usage if r[0].get(':task-item/_content')],'imported':sum(bool(q.get(':question/math-academy-id')) for q in k[':knowledge-point/questions'])}
(H/'capture.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2));print('Topic KPs:',[(r[':db/id'],r[':knowledge-point/title']) for r in topic[':topic/knowledge-points']])
