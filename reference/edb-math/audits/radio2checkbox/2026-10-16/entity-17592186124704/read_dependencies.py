"""Capture incoming question/field/answer references at the audit's basis."""
import json
from pathlib import Path
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import Tagged

HERE = Path(__file__).resolve().parent
snapshot = json.loads((HERE / 'snapshot.json').read_text())
client = Publisher.from_environment().client
assert client.status()['lineage'] == snapshot['lineage']
targets = set()
for [q] in snapshot['questions']:
    targets.add(q[':db/id'])
    for field in q.get(':question/answer-fields', []):
        targets.add(field[':db/id'])
        targets.update(answer[':db/id'] for answer in field.get(':answer-field/choices', []))
rows = client.query('''[:find ?entity ?attribute ?target (pull ?attribute [:db/ident])
  :in $ [?target ...] :where [?entity ?attribute ?target]]''',
  [[Tagged('edb/ref', eid) for eid in sorted(targets)]], HERE / 'evidence',
  'incoming-references', snapshot['basis'])
(HERE / 'incoming-references.json').write_text(json.dumps(rows, indent=2, default=str) + '\n')
print(json.dumps({'basis': snapshot['basis'], 'targets': len(targets), 'incoming_references': len(rows)}))
