"""Protect raw submissions and check choice-bank collisions."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher,jsonable
def many(value):return value if isinstance(value,list) else [value] if value else []
p=Publisher.from_environment(source=':agent/codex');basis=json.loads((H/'audit.json').read_text())['basis'];rows=json.loads((H/'proposals.json').read_text())
planned={r['entity']:r['after'] for r in rows if r['attribute']=='answer/value'};ids=sorted(planned);owners={}
pattern='[:db/id {:task-item/_responses [:db/id]} {:answer-field/_correct [:db/id]} {:answer-field/_choices [:db/id {:answer-field/type [:db/ident]}]}]'
for start in range(0,len(ids),1000):
    result=p.client.query('[:find (pull ?a '+pattern+') :in $ [?a ...] :where [?a :answer/id _]]',[ids[start:start+1000]],H/'owners','final-answers-'+str(start),basis)
    owners.update({str(r[0][':db/id']):jsonable(r[0]) for r in result})
protected=[];fids=set()
for key,a in owners.items():
    fs=many(a.get(':answer-field/_choices'));discrete=[f for f in fs if f.get(':answer-field/type',{}).get(':db/ident') in (':answer-field.type/radio',':answer-field.type/select',':answer-field.type/checkbox')]
    if a.get(':task-item/_responses') and not a.get(':answer-field/_correct') and not discrete:protected.append(int(key))
    fids.update(f[':db/id'] for f in discrete if f[':answer-field/type'][':db/ident']!=':answer-field.type/checkbox')
(H/'answer-owners.json').write_text(json.dumps(owners,indent=2)+'\n')
assert not protected,('Raw submissions require display-only handling',protected)
fields=[];collisions=[];fids=sorted(fids)
for start in range(0,len(fids),1000):
    result=p.client.query('[:find (pull ?f [:db/id {:answer-field/choices [:db/id :answer/value]}]) :in $ [?f ...] :where [?f :answer-field/id _]]',[fids[start:start+1000]],H/'owners','banks-'+str(start),basis)
    fields.extend(jsonable(r[0]) for r in result)
for field in fields:
    choices=many(field.get(':answer-field/choices'))
    for i,a in enumerate(choices):
        for b in choices[i+1:]:
            if a[':answer/value']!=b[':answer/value'] and planned.get(a[':db/id'],a[':answer/value'])==planned.get(b[':db/id'],b[':answer/value']):collisions.append({'field':field[':db/id'],'answers':[a[':db/id'],b[':db/id']]})
report={'passed':not collisions,'answers_checked':len(owners),'used_answer_entities':sum(bool(a.get(':task-item/_responses')) for a in owners.values()),
    'raw_learner_submissions_rewritten':0,'banks_checked':len(fields),'introduced_collisions':collisions}
(H/'preflight.json').write_text(json.dumps(report,indent=2)+'\n');assert report['passed'];print(json.dumps(report,indent=2))
