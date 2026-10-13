"""Read all remaining questions and dependent learner state at one EDB basis."""
import importlib.util
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('easy_migration', OUT.parent / 'finder-easy/prepare.py')
edb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edb)
edb.OUT = OUT
rows = json.loads((OUT / 'audit-input.json').read_text())
ids = sorted(q['id'] for q in rows)
basis = edb.DB.basis()
questions = edb.batches('[:find (pull ?q ' + edb.QUESTION + ') :in $ [?q ...] :where [?q :question/id _]]',
    ids, 'questions', basis)
assert {r[0][':db/id'] for r in questions} == set(ids)
items = edb.batches('[:find ?q (pull ?item ' + edb.ITEM + ') :in $ [?q ...] :where [?item :task-item/content ?q]]',
    ids, 'items', basis, 64)
answers = sorted({a[':db/id'] for r in questions for f in r[0].get(':question/answer-fields', [])
    for a in f.get(':answer-field/choices', [])})
users = edb.batches('[:find ?answer (pull ?item ' + edb.ITEM + ') :in $ [?answer ...] :where [?item :task-item/responses ?answer]]',
    answers, 'response-users', basis, 128)
attrs = edb.DB.attributes(OUT / 'evidence', basis)
source = edb.read('[:find (pull ?s [:db/id :db/ident :db/doc]) :in $ ?ident :where [?s :db/ident ?ident]]',
    [edb.kw(edb.SOURCE)], 'source', basis)
assert len(source) == 1 and source[0][0][':db/ident'] == edb.SOURCE
(OUT / 'snapshot.edn').write_text(edb.dumps({'basis': basis, 'questions': questions, 'items': items,
    'response_users': users, 'attributes': attrs, 'source': source}) + '\n')
edb.save('capture.json', {'basis': basis, 'source': edb.SOURCE, 'questions': len(ids),
    'presentations': len(items), 'response_links': len(users)})
print(json.dumps({'captured': True, 'basis': basis, 'questions': len(ids),
    'presentations': len(items), 'response_links': len(users)}))
