"""Choose actual affected questions across response types and difficulty bands."""
import json,sys
from collections import defaultdict
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable,QUESTION_PULL
def many(x):return x if isinstance(x,list) else [x] if x else []
p=Publisher.from_environment(source=':agent/codex');basis=json.loads((H/'audit.json').read_text())['basis'];rows=json.loads((H/'proposals.json').read_text())
ids=sorted({r['entity'] for r in rows if r['attribute'].startswith('question/')});step=max(1,len(ids)//600);candidates=ids[::step]
fids=[r['entity'] for r in rows if r['attribute']=='answer-field/key']
if fids:
    result=p.client.query('[:find (pull ?f [:db/id {:question/_answer-fields [:db/id]}]) :in $ [?f ...] :where [?f :answer-field/id _]]',[fids],H/'live-capture','checkbox-questions-indexed',basis)
    candidates += [q[':db/id'] for row in result for q in many(row[0].get(':question/_answer-fields'))]
profiles=defaultdict(list)
for start in range(0,len(candidates),400):
    result=p.client.query('[:find (pull ?q [:db/id {:question/difficulty [:db/ident]} {:question/answer-fields [{:answer-field/type [:db/ident]}]}]) :in $ [?q ...] :where [?q :question/id _]]',[candidates[start:start+400]],H/'live-capture','profiles-indexed-'+str(start),basis)
    for row in result:
        q=row[0]
        for f in q.get(':question/answer-fields',[]):profiles[str(f[':answer-field/type'][':db/ident']),str(q.get(':question/difficulty',{}).get(':db/ident'))].append(q[':db/id'])
selected=set()
for key,qs in sorted(profiles.items()):selected.update(sorted(set(qs))[:4])
data=p.client.query('[:find (pull ?q '+QUESTION_PULL+') :in $ [?q ...] :where [?q :question/id _]]',[sorted(selected)],H/'live-capture','questions',basis)
owner_rows=p.client.query('[:find (pull ?q [:db/id {:knowledge-point/_questions [:db/id {:topic/_knowledge-points [:db/id]}]} {:knowledge-point/_canonical-example [:db/id {:topic/_knowledge-points [:db/id]}]}]) :in $ [?q ...] :where [?q :question/id _]]',[sorted(selected)],H/'live-capture','topics-indexed',basis)
owners=[]
for row in owner_rows:
    q=row[0]
    for k in many(q.get(':knowledge-point/_questions'))+many(q.get(':knowledge-point/_canonical-example')):
        for t in many(k.get(':topic/_knowledge-points')):owners.append([q[':db/id'],t[':db/id']])
record={'basis':basis,'profiles':{' / '.join(k):len(v) for k,v in profiles.items()},'questions':jsonable(data),'topics':jsonable(owners)}
(H/'live-samples.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'questions':len(data),'profiles':record['profiles']}))
