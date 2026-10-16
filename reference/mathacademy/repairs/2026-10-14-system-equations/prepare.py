"""Prepare guarded repairs for the reported lesson and exact matching defects."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads, dumps, kw
from normalize import repair, legacy_choice

lesson = {(e, a): t for e, a, t in json.loads((HERE / 'lesson-fields.json').read_text())}
fields = {}
for attr in ['tutorial/content', 'question/problem', 'question/worked-solution',
             'answer/value', 'answer/feedback', 'multistep/context']:
    for index in range(3):
        for eid, text in loads((HERE / 'discovery' / f'{attr.replace("/", "-")}-{index}.edn').read_text()):
            fields[eid, ':' + attr] = text
fields.update(lesson)
forms, changes = [], []
for (eid, attr), old in sorted(fields.items()):
    new = repair(old, include_cases=(eid, attr) in lesson)
    if (eid, attr) in lesson and attr == ':answer/value': new = legacy_choice(new)
    if attr == ':question/problem' and '{{field-' in new:
        new = re.sub(r'(?m)^[ \t]{4,}(?=\$(?!\$))', '', new)
    if new == old: continue
    assert repair(new, include_cases=(eid, attr) in lesson) == new, (eid, attr)
    forms.append([kw(':db/cas'), eid, kw(attr), old, new])
    changes.append({'entity': eid, 'attribute': attr, 'lesson': (eid, attr) in lesson,
                    'before': old, 'after': new})
assert {17592186240971, 17592186338974} <= {f[1] for f in forms}
(HERE / 'changes.json').write_text(json.dumps(changes, indent=2) + '\n')
(HERE / 'expected.edn').write_text(dumps([[f[1], f[2], f[4]] for f in forms]))
transaction = HERE / 'transaction.edn'
transaction.write_text(dumps(forms))
digest = hashlib.sha256(transaction.read_bytes()).hexdigest()
(HERE / 'read-query.edn').write_text('[:find ?entity ?attr ?value :in $ [[?entity ?attr]] :where [?entity ?attr ?value]]')
(HERE / 'read-inputs.edn').write_text(dumps([[[f[1], f[2]] for f in forms]]))
(HERE / 'commit-intent.json').write_text(json.dumps({
    'database': 'math', 'source': ':application/ca-engine', 'endpoint': '/tmp/edb-math/writer.sock',
    'file': str(transaction), 'sha256': digest, 'request_key': 'system-equations-' + digest,
    'fields': len(forms), 'entities': len(set(f[1] for f in forms)),
}, indent=2) + '\n')
print(f'Prepared {len(forms)} fields, {sum(c["lesson"] for c in changes)} in the reported lesson')
for name, in_lesson in [('lesson', True), ('matching', False)]:
    directory = HERE / name
    directory.mkdir(exist_ok=True)
    selected = [form for form, change in zip(forms, changes) if change['lesson'] == in_lesson]
    transaction = directory / 'transaction.edn'
    transaction.write_text(dumps(selected))
    digest = hashlib.sha256(transaction.read_bytes()).hexdigest()
    (directory / 'read-query.edn').write_text((HERE / 'read-query.edn').read_text())
    (directory / 'read-inputs.edn').write_text(dumps([[[f[1], f[2]] for f in selected]]))
    (directory / 'expected.edn').write_text(dumps([[f[1], f[2], f[4]] for f in selected]))
    (directory / 'commit-intent.json').write_text(json.dumps({
        'database': 'math', 'source': ':application/ca-engine', 'endpoint': '/tmp/edb-math/writer.sock',
        'file': str(transaction), 'sha256': digest, 'request_key': 'system-equations-' + digest,
        'fields': len(selected), 'entities': len(set(f[1] for f in selected)),
    }, indent=2) + '\n')
