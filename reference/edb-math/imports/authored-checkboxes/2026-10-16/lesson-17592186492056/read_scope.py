"""Capture the requested lesson and response dependencies at one immutable basis."""
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import dumps, kw, Tagged

HERE = Path(__file__).resolve().parent
DB = EDBClient(Config(), threading.Event())
QUESTION = '''[* {:question/difficulty [:db/id :db/ident]}
 {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:knowledge-point/_canonical-example :limit nil] [:db/id :knowledge-point/id :knowledge-point/title]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]}
 {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}
 {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]'''
ITEM = '''[* {:task-item/status [:db/id :db/ident]} {[:task-item/responses :limit nil] [*]}
 {[:learner-task/_items :limit nil] [:db/id :learner-task/status]}]'''

def save(name, value):
    (HERE / (name + '.json')).write_text(json.dumps(value, indent=2, default=str) + '\n')

def run():
    assert not (HERE / 'snapshot.edn').exists(), 'Preserve the original audit'
    identity = DB.status()
    basis = identity['basis']
    save('capture-identity', identity)
    def read(name, query, inputs):
        return DB.query(query, inputs, HERE / 'evidence', name, basis)
    seed = read('seed', '[:find (pull ?q ' + QUESTION + ') :in $ ?q :where [?q :question/id _]]', [17592186492056])
    assert len(seed) == 1
    kps = read('seed-membership', '''[:find ?kp ?topic :in $ ?q :where
      (or [?kp :knowledge-point/questions ?q] [?kp :knowledge-point/canonical-example ?q])
      [?topic :topic/knowledge-points ?kp]]''', [17592186492056])
    topics = sorted({row[1] for row in kps})
    assert topics
    scope = read('scope', '''[:find (pull ?topic [* {[:topic/knowledge-points :limit nil]
      [* {[:knowledge-point/questions :limit nil] [:db/id]}
      {:knowledge-point/canonical-example [:db/id]}]}])
      :in $ [?topic ...] :where [?topic :topic/id _]]''', [topics])
    ids = sorted({q[':db/id'] for row in scope for kp in row[0].get(':topic/knowledge-points', [])
                  for q in kp.get(':knowledge-point/questions', []) +
                  ([kp[':knowledge-point/canonical-example']] if kp.get(':knowledge-point/canonical-example') else [])})
    questions = read('questions', '[:find (pull ?q ' + QUESTION + ') :in $ [?q ...] :where [?q :question/id _]]', [ids])
    items = read('items', '[:find ?q (pull ?item '+ITEM+') :in $ [?q ...] :where [?item :task-item/content ?q]]', [ids])
    refs = sorted({r[':db/id'] for row in questions if row[0][':db/id'] in (17592186492000, 17592186492056)
                   for f in row[0].get(':question/answer-fields', [])
                   for r in [f] + f.get(':answer-field/choices', [])})
    attributes = read('attributes', '[:find (pull ?a [*]) :where [?a :db/valueType _]]', [])
    ref_attributes = read('ref-attributes', '[:find ?a :where [?a :db/valueType :db.type/ref]]', [])
    incoming = read('incoming-typed', '[:find ?e ?a ?target :in $ [?target ...] :where [?e ?a ?target]]',
                    [[Tagged('edb/ref', ref) for ref in refs]])
    contributors = read('contributors', '[:find ?s ?ident :where [?s :db/ident ?ident] [(str ?ident) ?name] [(starts-with? ?name ":agent/")]]', [])
    snapshot = {**identity, 'seed': seed, 'scope':scope, 'questions':questions,'items':items,
                'incoming':incoming,'attributes':attributes,'contributors':contributors}
    (HERE/'snapshot.edn').write_text(dumps(snapshot)+'\n')
    save('snapshot', snapshot)
    save('status', {**identity,'stage':'captured','requested_question':17592186492056,
                   'topic_ids':topics,'question_count':len(ids),'committed_ids':[]})
    print(json.dumps({'basis':basis,'topics':topics,'questions':len(ids),'items':len(items)}))

if __name__ == '__main__':
    run()
