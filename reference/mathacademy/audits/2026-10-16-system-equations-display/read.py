"""Read-only complete topic content and selected-question history."""
import json
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import dumps, loads

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
IDS=[17592186050240,17592186048343,17592186048853,17592186049058]
DB=EDBClient(Config(),threading.Event())
identity=DB.status();basis=identity['basis']
assert not (HERE/'snapshot.json').exists(),'Preserve captured evidence'
(HERE/'snapshot.json').write_text(json.dumps(identity,indent=2)+'\n')
pattern=(ROOT/'reference/mathacademy/repairs/2026-10-14-linear-algebra-latex/lesson-pull.edn').read_text()
(HERE/'lesson-pull.edn').write_text(pattern)
(HERE/'topic-ids.json').write_text(json.dumps(IDS)+'\n')
def one(eid):
    result=DB.command('pull','--as-of',basis,'--file',HERE/'lesson-pull.edn','--entity',eid,
                      '--max-depth','40','--max-entities','50000')
    (HERE/f'{eid}.edn').write_text(result)
    return loads(result)
with ThreadPoolExecutor(max_workers=4) as pool: topics=list(pool.map(one,IDS))
query='[:find ?v ?tx ?source ?added :in $ ?q :where [?q :question/problem ?v ?tx ?source ?added]]'
(HERE/'history-query.edn').write_text(query)
(HERE/'history-inputs.edn').write_text(dumps([17592186529306]))
out=DB.command('query','--as-of',basis,'--history','--file',HERE/'history-query.edn','--inputs',HERE/'history-inputs.edn')
(HERE/'history.edn').write_text(out)
(HERE/'history.json').write_text(json.dumps(loads(out),indent=2,default=str)+'\n')
refs=sorted({r[1] for r in loads(out)}|{r[2] for r in loads(out)})
DB.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e _ _]]',[refs],HERE,'provenance',basis)
print(json.dumps({'basis':basis,'topics':[(t[':db/id'],t.get(':topic/title')) for t in topics]}))
