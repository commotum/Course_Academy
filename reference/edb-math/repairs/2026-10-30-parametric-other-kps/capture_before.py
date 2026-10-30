import json,re,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from scripts.generator_packages import resolve_registered_script
p=Publisher.from_environment(source=':agent/codex');status=p.client.status();basis=status['basis'];summary=[]
for kp in (17592186087717,17592186087722,17592186087736):
    h=H/str(kp);h.mkdir(exist_ok=True);k=p.read_kp(kp,h/'capture',basis);p._source_from_kp(kp,h/'source',status,basis,k)
    (h/'before.json').write_text(json.dumps(jsonable(k),indent=2)+'\n')
    ref=k[':knowledge-point/question-generator'][':question-generator/script'];entry=resolve_registered_script(ref,ROOT,p.config.math_root);manifest=json.loads((entry.parent/'generator-package.json').read_text())
    for name in manifest['files']:
        out=h/'package'/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(entry.parent/name,out);out.chmod(out.stat().st_mode|0o200)
    active=[q for q in k[':knowledge-point/questions'] if not q.get(':question/math-academy-id') and not q.get(':question/retired')]
    usage=p.client.query('[:find (pull ?q [:db/id {:task-item/_content [:db/id]}]) :in $ [?q ...] :where [?q :question/id _]]',[[q[':db/id'] for q in active]],h/'capture','usage',basis)
    used=[row[0][':db/id'] for row in usage if row[0].get(':task-item/_content')]
    data={'basis':basis,'lineage':status['lineage'],'kp':kp,'title':k[':knowledge-point/title'],'registered_generator':ref,'files':list(manifest['files']),'dependencies':manifest['dependencies'],'active_generated':[q[':db/id'] for q in active],'used':used}
    (h/'capture.json').write_text(json.dumps(data,indent=2)+'\n')
    data.update(imported=sum(bool(q.get(':question/math-academy-id')) for q in k[':knowledge-point/questions']),image_question_ids=[q[':db/id'] for q in k[':knowledge-point/questions'] if re.search(r'images/|<img',q.get(':question/problem','')+q.get(':question/worked-solution',''))])
    summary.append(data);print(json.dumps(data),flush=True)
(H/'inventory.json').write_text(json.dumps(summary,indent=2)+'\n')
