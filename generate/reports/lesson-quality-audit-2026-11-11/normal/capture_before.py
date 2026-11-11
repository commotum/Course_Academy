import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from generator_publish import Publisher,jsonable
p=Publisher.from_environment();status=json.loads((H.parent/'status.json').read_text());basis=status['basis']
for kp in [17592186092240,17592186092384,17592186092385]:
 d=H/str(kp);d.mkdir(exist_ok=True);source=p.extract_source(kp,d/'source',basis=basis);K=p.read_kp(kp,d/'inventory',basis);inventory=p.save_inventory(kp,K,status,basis,d/'inventory')
 (d/'kp.json').write_text(json.dumps(jsonable(K),indent=2)+'\n');print(kp,len(K[':knowledge-point/questions']),source['registered_generator'][':question-generator/script'])
