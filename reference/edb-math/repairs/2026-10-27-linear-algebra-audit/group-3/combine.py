import sys,json
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import loads
H=Path(__file__).resolve().parent;P=H.parent;D=json.loads((P/'inventory.json').read_text());ids=json.loads((P/'group-3.json').read_text())['topics']
read=lambda p:loads(p.read_text())
Q=[r[0] for p in sorted(H.glob('questions-[0-9]*.edn')) if not any(k in p.name for k in ('inputs','query')) for r in read(p)]
C=[r[0] for p in sorted(H.glob('content-[0-9]*.edn')) if not any(k in p.name for k in ('inputs','query')) for r in read(p)]
S={'basis_t':9047,'topics':[t for t in D['topics'] if t['entity'] in ids],'links':read(H/'links.edn'),'steps':read(H/'steps.edn'),'content':C,'questions':Q,'kps':[r[0] for r in read(H/'kps.edn')]}
(H/'snapshot.json').write_text(json.dumps(S,indent=2,default=str));print('q',len(Q),'c',len(C));print(json.dumps(S['topics'],indent=1));print(json.dumps(Q[0],default=str,indent=1)[:8000]);print(S['kps'][0])
