"""Read a fixed-basis inventory of the conformability KP and learner uses."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps, kw, Tagged

HERE = Path(__file__).resolve().parent
KP = 17592186100869
SOURCE = ':agent/gpt-6.1-sol-high'
PATTERNS = {
    'questions': '[* {:question/difficulty [:db/id :db/ident]} {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/title]} {[:knowledge-point/_canonical-example :limit nil] [:db/id]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}]}]',
    'items': '[* {:task-item/status [:db/id :db/ident]} {[:task-item/responses :limit nil] [* {:answer/type [:db/id :db/ident]}]} {[:learner-task/_items :limit nil] [:db/id :learner-task/status]}]',
    'scope': '[* {[:topic/_knowledge-points :limit nil] [:db/id :topic/title]} {:knowledge-point/question-generator [*]} {[:knowledge-point/questions :limit nil] [:db/id]} {:knowledge-point/canonical-example [:db/id]}]',
}

def capture():
    db = Publisher.from_environment(source=SOURCE).client
    identity = db.status()
    directory = HERE / f"capture-{identity['basis']}"
    directory.mkdir(exist_ok=True)
    def read(name, query, inputs):
        return db.query(query, inputs, directory / 'evidence', name, identity['basis'])
    scope = read('scope', '[:find (pull ?kp ' + PATTERNS['scope'] + ') :in $ ?kp :where [?kp :knowledge-point/id _]]', [KP])
    kp = scope[0][0]
    ids = sorted({q[':db/id'] for q in kp[':knowledge-point/questions']} | {kp[':knowledge-point/canonical-example'][':db/id']})
    queries = {
        'questions': ('[:find (pull ?q ' + PATTERNS['questions'] + ') :in $ [?q ...] :where [?q :question/id _]]', [ids]),
        'items': ('[:find ?q (pull ?i ' + PATTERNS['items'] + ') :in $ [?q ...] :where [?i :task-item/content ?q]]', [ids]),
        'attributes': ('[:find ?a ?ident :where [?a :db/ident ?ident] [?a :db/valueType _]]', []),
        'source': ('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]', [kw(SOURCE)]),
    }
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {name: pool.submit(read, name, *args) for name, args in queries.items()}
        data = {name: future.result() for name, future in futures.items()}
    fields = [f for [q] in data['questions'] for f in q.get(':question/answer-fields', [])]
    entities = sorted({e[':db/id'] for f in fields for e in [f, *f[':answer-field/choices']]})
    incoming = read('incoming', '[:find ?e ?a ?target :in $ [?target ...] :where [?e ?a ?target]]', [[Tagged('edb/ref', e) for e in entities]])
    names = dict(data['attributes'])
    data['incoming'] = [[e, names[a], target] for e, a, target in incoming]
    snapshot = {**identity, **data, 'scope': scope, 'patterns': PATTERNS}
    (directory / 'snapshot.edn').write_text(dumps(snapshot) + '\n')
    (HERE / 'capture-directory.txt').write_text(str(directory.relative_to(ROOT)) + '\n')
    report = []
    for [q] in sorted(data['questions'], key=lambda row: row[0][':db/id']):
        matrices = re.findall(r'([A-Z])=\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', q[':question/problem'], re.S)
        dims = {name: (len(body.split(r'\\')), len(body.split(r'\\')[0].split('&'))) for name, body in matrices}
        products = re.findall(r'The product \$([A-Z])([A-Z])\$', q[':question/problem'])
        report.append({'id': q[':db/id'], 'source_id': q.get(':question/math-academy-id'), 'level': q.get(':question/difficulty', {}).get(':db/ident'),
                       'canonical': ':knowledge-point/_canonical-example' in q,
                       'dimensions': dims, 'products': [''.join(p) for p in products],
                       'truth': [dims[a][1] == dims[b][0] for a, b in products],
                       'fields': [{'id': f[':db/id'], 'key': f[':answer-field/key'], 'type': f[':answer-field/type'][':db/ident'], 'correct': f.get(':answer-field/correct', {}).get(':answer/value')} for f in q.get(':question/answer-fields', [])],
                       'items': [{'id': i[':db/id'], 'status': i.get(':task-item/status'), 'responses': len(i.get(':task-item/responses', []))} for qid, i in data['items'] if qid == q[':db/id']]})
    (directory / 'inventory.json').write_text(json.dumps(report, indent=2, default=str) + '\n')
    print(json.dumps({'basis': identity['basis'], 'questions': len(report), 'items': len(data['items']), 'inventory': str(directory / 'inventory.json')}, default=str))
    return directory, snapshot

if __name__ == '__main__':
    capture()
