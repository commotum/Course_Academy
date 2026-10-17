"""Small title and selection lookups for saved queue examples; no inventory scan."""
from pathlib import Path
import json,sys,threading
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import kw
HERE=ROOT/'reference/generated/generator-queue-priority-2026-10-17'
snapshot=json.loads((HERE/'queue-snapshot.json').read_text());basis=snapshot['cursor']['basis']
targets=sorted({r['topic'] for r in snapshot['selected_jobs']});examples=snapshot['top_10'];topics=sorted(set(targets)|{r['topic'] for r in examples});kps=sorted({r['knowledgePoint'] for r in examples})
db=EDBClient(Config(capture_only=True),threading.Event());identity=db.status();assert identity['lineage']==snapshot['cursor']['lineage']
names=db.query('[:find (pull ?t [:db/id :topic/title]) :in $ [?t ...] :where [?t :topic/id _]]',[topics],HERE,'example-topic-names',basis)
skills=db.query('[:find (pull ?k [:db/id :knowledge-point/title]) :in $ [?k ...] :where [?k :knowledge-point/id _]]',[kps],HERE,'example-kp-names',basis)
selections=db.query('[:find ?t ?a :in $ ?l [?t ...] [?a ...] :where [?l ?a ?t]]',[17592186045416,topics,[kw('learner/queue'),kw('learner/targets')]],HERE,'example-selections',basis)
result={'basis':basis,'topic_names':[r[0] for r in names],'kp_names':[r[0] for r in skills],'selections':selections}
(HERE/'example-titles.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
