import json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from scripts.generator_packages import resolve_registered_script
p=Publisher.from_environment(source=':agent/codex');s=p.client.status();basis=s['basis']
topic=p.client.query('[:find (pull ?t [:db/id :topic/title {:topic/knowledge-points [:db/id :knowledge-point/title]}]) :in $ ?t :where [?t :topic/id _]]',[17592186049248],H/'capture','topic',basis)[0][0]
rows=[]
for kp in topic[':topic/knowledge-points']:
 h=H/str(kp[':db/id']);k=p.read_kp(kp[':db/id'],h/'capture',basis);p._source_from_kp(kp[':db/id'],h/'source',s,basis,k)
 (h/'before.json').write_text(json.dumps(jsonable(k),indent=2)+'\n')
 ref=k.get(':knowledge-point/question-generator',{}).get(':question-generator/script');files=[]
 if ref:
  entry=resolve_registered_script(ref,ROOT,p.config.math_root);manifest=json.loads((entry.parent/'generator-package.json').read_text());files=list(manifest['files'])
  for name in files:
   out=h/'package'/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(entry.parent/name,out);out.chmod(out.stat().st_mode|0o200)
 rows.append({'kp':kp[':db/id'],'title':k[':knowledge-point/title'],'generator':ref,'files':files,'questions':len(k[':knowledge-point/questions'])})
 print(json.dumps(rows[-1]),flush=True)
(H/'inventory.json').write_text(json.dumps({'basis':basis,'topic':jsonable(topic),'kps':rows},indent=2)+'\n')
