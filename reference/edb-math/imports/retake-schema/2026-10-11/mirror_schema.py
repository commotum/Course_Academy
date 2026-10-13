"""Mirror the two verified committed definitions, preserving other schema forms."""
from pathlib import Path
import hashlib
import json
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from edn import loads, dumps, kw

assert json.loads((OUT / 'commit-verification.json').read_text())['verified']
intent = json.loads((OUT / 'intent.json').read_text())
assert hashlib.sha256((OUT / 'transaction.edn').read_bytes()).hexdigest() == intent['transaction_sha256']
definitions = [{k: v for k, v in f.items() if k != kw('db/id')}
               for f in loads((OUT / 'transaction.edn').read_text())]
names = {d[kw('db/ident')] for d in definitions}


def parse_schema(text):
    return loads('\n'.join(line for line in text.splitlines() if not line.lstrip().startswith(';')))


addition = '\n\n'.join(' {' + '\n  '.join(str(k) + ' ' + dumps(v) for k, v in d.items()) + '}'
                        for d in definitions) + '\n\n'
anchor = ' {:db/ident :learner-task/status\n'
result = []
for index, target in enumerate(map(Path, intent['schema_files_for_later_update'])):
    before_text = target.read_text()
    before_forms = parse_schema(before_text)
    existing = {f[kw('db/ident')]: f for f in before_forms}
    backup = OUT / ('workspace-schema-before.edn' if index == 0 else 'ssd-schema-before.edn')
    if names & existing.keys():
        assert names <= existing.keys()
        assert all(existing[d[kw('db/ident')]] == d for d in definitions)
        assert backup.exists(), 'Unexpected already-present definitions; inspect before editing.'
    else:
        assert before_text.count(anchor) == 1
        assert not backup.exists() or backup.read_text() == before_text
        backup.write_text(before_text)
        after_text = before_text.replace(anchor, addition + anchor, 1)
        after_forms = parse_schema(after_text)
        assert [f for f in after_forms if f[kw('db/ident')] not in names] == before_forms
        target.write_text(after_text)
    after_text = target.read_text()
    after_forms = parse_schema(after_text)
    after = {f[kw('db/ident')]: f for f in after_forms}
    assert all(after[d[kw('db/ident')]] == d for d in definitions)
    original_text = backup.read_text()
    original_forms = parse_schema(original_text)
    assert [f for f in after_forms if f[kw('db/ident')] not in names] == original_forms
    assert after_text == original_text.replace(anchor, addition + anchor, 1)
    result.append({'path': str(target), 'only_two_definitions_added': True,
                   'definitions_match_committed_transaction': True,
                   'sha256_before': hashlib.sha256(original_text.encode()).hexdigest(),
                   'sha256_after': hashlib.sha256(after_text.encode()).hexdigest()})
(OUT / 'schema-mirror-verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
