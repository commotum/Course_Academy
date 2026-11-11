import sys,json
from pathlib import Path
R=Path('/home/jake/Developer/Course_Academy');sys.path[:0]=[str(R),str(R/'scripts')]
from generator_publish import Publisher,jsonable
H=Path(__file__).resolve().parent;p=Publisher.from_environment(source=':agent/codex');status=json.loads((H.parent/'status.json').read_text());basis=status['basis']
for kp in [17592186096672,17592186096673]:
 d=H/str(kp);d.mkdir(exist_ok=True);source=p.extract_source(kp,d/'source',basis=basis);stored=p.read_kp(kp,d/'stored',basis);inventory=p.save_inventory(kp,stored,status,basis,d/'stored')
 (d/'kp.json').write_text(json.dumps(jsonable(stored),indent=2)+'\n');print(kp,'stored',len(stored[':knowledge-point/questions']),flush=True)
