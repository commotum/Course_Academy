"""Read original Math Academy lesson evidence at one current EDB basis."""
import json
import threading
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient

home = Path(__file__).resolve().parent
db = EDBClient(Config(), threading.Event())
identity = db.status()
queries = {
    'source-questions': None,
    'source-tutorials': '''[:find ?c
    :in $ ?t :where [?a :activity/scope ?t] [?a :activity/steps ?s]
    [?s :step/content ?c] [?c :tutorial/math-academy-id _]]''',
}
report = {'identity': identity, 'topic': 17592186050240}
for name, query in queries.items():
    if name == 'source-questions':
        rows = []
        for kp in (17592186073776, 17592186073777, 17592186073778):
            for attr in (':knowledge-point/questions', ':knowledge-point/canonical-example'):
                q = '[:find ?q :in $ ?kp :where [?kp ' + attr + ' ?q] [?q :question/math-academy-id _]]'
                rows.extend(db.query(q, [kp], home / 'source-evidence', name + '-' + str(kp) + '-' + attr.split('/')[-1], identity['basis']))
        rows = [[entity] for entity in sorted({row[0] for row in rows})]
    else:
        rows = db.query(query, [17592186050240], home / 'source-evidence', name, identity['basis'])
    entities = []
    pattern = ('[:db/id :question/math-academy-id :question/problem]' if name == 'source-questions'
               else '[:db/id :tutorial/math-academy-id :tutorial/title :tutorial/content]')
    for [entity] in rows:
        pulled = db.query('[:find (pull ?e ' + pattern + ') :in $ ?e :where [?e _ _]]',
                          [entity], home / 'source-evidence', name + '-' + str(entity), identity['basis'])
        entities.append(pulled[0][0])
    report[name] = sorted(entities, key=lambda x: x[':db/id'])
(home / 'math-academy-sources.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'basis': identity['basis'], 'questions': len(report['source-questions']),
                  'tutorials': len(report['source-tutorials'])}))
for q in report['source-questions']:
    print(q[':db/id'], q[':question/math-academy-id'], q[':question/problem'])
for tutorial in report['source-tutorials']:
    print(tutorial[':db/id'], tutorial[':tutorial/math-academy-id'], tutorial[':tutorial/title'])
