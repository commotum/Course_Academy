"""Read only the named topics' prerequisite ancestry; no question inventory scan."""
from pathlib import Path
import json,sys,threading
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'capture'))
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import kw
HERE=ROOT/'reference/generated/generator-layer-order-2026-10-17'
GROUPS=[[17592186050283],[17592186051059,17592186048470,17592186049879,17592186050375],[17592186049053,17592186050542],[17592186050649,17592186050245,17592186049195],[17592186050473,17592186049930],[17592186049488,17592186049570,17592186049570,17592186050149,17592186049456]]
TOPICS=list(dict.fromkeys(t for group in GROUPS for t in group));db=EDBClient(Config(capture_only=True),threading.Event());identity=db.status();basis=identity['basis']
(HERE/'input.json').write_text(json.dumps({**identity,'groups':GROUPS,'topics':TOPICS,'learner':17592186045416},indent=2)+'\n')
query='[:find (pull ?t [:db/id :topic/title {:topic/_next [:db/id]}]) :in $ [?t ...] :where [?t :topic/id _]]'
records={};pending=set(TOPICS);batches=0
while pending:
 if len(records)+len(pending)>1000:raise RuntimeError('Ancestor safety bound reached; stop instead of expanding')
 batch=sorted(pending)[:25];pending.difference_update(batch)
 rows=db.query(query,[batch],HERE,f'ancestors-{batches:02d}',basis);batches+=1
 returned={r[0][':db/id'] for r in rows};assert returned==set(batch),f'Missing topics: {set(batch)-returned}'
 for row in rows:
  t=row[0];records[t[':db/id']]={'topic':t[':db/id'],'title':t.get(':topic/title'),'prerequisites':[p[':db/id'] for p in t.get(':topic/_next',[])]}
 for row in rows:pending.update(p[':db/id'] for p in row[0].get(':topic/_next',[]) if p[':db/id'] not in records)
 print(f'Read {len(records)} topic records; {len(pending)} ancestor IDs pending',flush=True)
selections=db.query('[:find ?t ?a :in $ ?l [?t ...] [?a ...] :where [?l ?a ?t]]',[17592186045416,TOPICS,[kw('learner/queue'),kw('learner/targets')]],HERE,'selections',basis)
membership={t:set() for t in TOPICS}
for t,a in selections:membership[t].add(a)
layers={};ancestors={};active=set()
def visit(t):
 if t in layers:return
 if t in active:raise ValueError('Prerequisite cycle')
 active.add(t);parents=records[t]['prerequisites']
 for p in parents:visit(p)
 layers[t]=1+max((layers[p] for p in parents),default=0)
 ancestors[t]=set(parents).union(*(ancestors[p] for p in parents))
 active.remove(t)
for t in TOPICS:visit(t)
rows=[]
for t in TOPICS:
 children=[d for d in TOPICS if t in ancestors[d]]
 rows.append({**records[t],'display_layer':layers[t],'selected_as':sorted(membership[t]),'downstream_listed_topics':children,'downstream_listed_selected_count':sum(bool(membership[d]) for d in children),'listed_prerequisites':[p for p in TOPICS if p in ancestors[t]],'user_group':next(i for i,g in enumerate(GROUPS,1) if t in g)})
violations=[{'earlier_group':a,'later_group':b} for a in TOPICS for b in TOPICS if next(i for i,g in enumerate(GROUPS) if a in g)<next(i for i,g in enumerate(GROUPS) if b in g) and b in ancestors[a]]
result={**identity,'topics':rows,'layer_order':sorted(TOPICS,key=lambda t:(layers[t],-len([d for d in TOPICS if t in ancestors[d]]),t)),'group_prerequisite_inversions':violations,'read_scope':{'named_unique_topics':len(TOPICS),'topic_records_with_ancestors':len(records),'ancestor_pull_batches':batches,'question_records_read':0,'global_attribute_scans':0,'database_writes':0},'ancestry':list(records.values())}
(HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='ancestry'},indent=2))
