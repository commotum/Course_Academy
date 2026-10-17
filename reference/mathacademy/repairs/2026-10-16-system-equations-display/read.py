"""Read all planned display repair dependencies at one current database basis."""
import json
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import dumps, kw, Tagged

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
AUDIT=ROOT/'reference/mathacademy/audits/2026-10-16-system-equations-display'
DB=EDBClient(Config(),threading.Event())
QUESTION='''[* {:question/difficulty [:db/id :db/ident]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]}
 {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}
 {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}
 {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/id :knowledge-point/title
 {[:topic/_knowledge-points :limit nil] [:db/id :topic/title]}]}
 {[:knowledge-point/_canonical-example :limit nil] [:db/id :knowledge-point/id]}]'''
ITEM='''[* {:task-item/status [:db/id :db/ident]}
 {[:task-item/responses :limit nil] [* {:answer/type [:db/id :db/ident]}]}]'''
KP_IDS=[17592186073752,17592186073753,17592186073776,17592186073778,
        17592186192654,17592186192655,17592186192656,17592186192657]

def save(name,value):
    (HERE/(name+'.json')).write_text(json.dumps(value,indent=2,default=str)+'\n')

def run():
    assert not (HERE/'snapshot.edn').exists(),'Preserve original repair snapshot'
    identity=DB.status();basis=identity['basis'];save('snapshot-identity',identity)
    findings=json.loads((AUDIT/'wide-mth341/findings.json').read_text())
    ids=sorted({f['entity'] for f in findings})
    def query(name,text,args):return DB.query(text,args,HERE/'evidence',name,basis)
    def batch(group):return query('questions-'+str(group[0]),'[:find (pull ?q '+QUESTION+') :in $ [?q ...] :where [?q :question/id _]]',[group])
    with ThreadPoolExecutor(max_workers=3) as pool:
        questions=[row for group in pool.map(batch,[ids[i:i+20] for i in range(0,len(ids),20)]) for row in group]
    tutorials=query('tutorials','[:find (pull ?e [*]) :in $ [?e ...] :where [?e :tutorial/id _]]',[[17592186199637,17592186097842]])
    generators=query('generators','''[:find (pull ?kp [* {:knowledge-point/question-generator [*]}])
        :in $ [?kp ...] :where [?kp :knowledge-point/id _]]''',[KP_IDS])
    items=query('items','[:find ?q (pull ?item '+ITEM+') :in $ [?q ...] :where [?item :task-item/content ?q]]',[ids])
    fields=sorted({f[':db/id'] for [q] in questions for f in q.get(':question/answer-fields',[])})
    answers=sorted({a[':db/id'] for [q] in questions for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])})
    incoming=query('incoming','[:find ?e ?a ?target :in $ [?target ...] :where [?e ?a ?target]]',[[Tagged('edb/ref',v) for v in fields+answers]])
    schema=query('schema','[:find ?a ?ident :where [?a :db/ident ?ident]]',[])
    qmap={q[':db/id']:q for [q] in questions}
    changed=[{'entity':f['entity'],'attribute':f['attribute'],'audited_value':f['value'],'current_value':qmap[f['entity']].get(f['attribute'])}
             for f in findings if qmap[f['entity']].get(f['attribute'])!=f['value']]
    snapshot={**identity,'questions':questions,'tutorials':tutorials,'generators':generators,'items':items,'incoming':incoming,'schema':schema}
    (HERE/'snapshot.edn').write_text(dumps(snapshot)+'\n');save('snapshot',snapshot)
    save('changed-since-audit',changed)
    print(json.dumps({'basis':basis,'questions':len(questions),'tutorials':len(tutorials),'generators':len(generators),'task_items':len(items),'changed_since_audit':len(changed)}))

if __name__=='__main__':run()
