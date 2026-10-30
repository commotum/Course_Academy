import json,sys,shutil
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
from scripts.generator_packages import resolve_registered_script
p=Publisher.from_environment(source=':agent/codex');status=p.client.status();basis=status['basis']
k=jsonable(p.read_kp(17592186087721,H/'capture',basis))
(H/'kp.json').write_text(json.dumps(k,indent=2)+'\n')
ref=k[':knowledge-point/question-generator'][':question-generator/script'];entry=resolve_registered_script(ref,ROOT,p.config.math_root)
manifest=json.loads((entry.parent/'generator-package.json').read_text())
for name in manifest['files']:
 out=H/'package'/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(entry.parent/name,out)
q=next(q for q in k[':knowledge-point/questions'] if q[':db/id']==17592186535273)
imports=[q for q in k[':knowledge-point/questions'] if q.get(':question/math-academy-id')]
print(json.dumps({'basis':basis,'kp':k[':db/id'],'title':k[':knowledge-point/title'],'generator':ref,'files':list(manifest['files']),'question':q,'imported_count':len(imports)},indent=2))
for source in [k[':knowledge-point/canonical-example']]+imports:
 print(json.dumps({'entity':source[':db/id'],'source':source.get(':question/math-academy-id'),'difficulty':source.get(':question/difficulty'),'problem':source.get(':question/problem'),'solution':source.get(':question/worked-solution'),'choices':[(a[':db/id'],a[':answer/value']) for f in source.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])]}))
