"""Extend the same-basis capture for defects uncovered in supplemental review."""
import gzip
import json
from pathlib import Path
import subprocess
import sys

H = Path(__file__).resolve().parent
ROOT = H.parents[3]
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher, QUESTION_PULL, dumps, loads, jsonable

target_path = H/sys.argv[1]
targets = json.loads(target_path.read_text())
if isinstance(targets, list):
    targets = {'question_ids': targets, 'target_entities': targets}
qids = set(targets['question_ids'])
eids = set(targets.get('target_entities', targets['question_ids']))
a = ROOT/'reference/edb-math/audits/2026-11-11-imported-matrix-tables'
blocks = [r for line in (a/'all-imported-tables.jsonl').open() if (r := json.loads(line))['entity'] in eids]
kids = sorted({k for r in blocks for k in r['knowledge_points']})
oldq = {q[':db/id'] for q in json.loads((H/'capture/questions.json').read_text())}
olde = {q[':db/id'] for q in json.loads((H/'capture/entities.json').read_text())}
newq, newe = sorted(qids-oldq), sorted(eids-olde)
pattern = '[:db/id :knowledge-point/id :knowledge-point/title {[:knowledge-point/questions :limit nil] [:db/id]} {:knowledge-point/canonical-example [:db/id]} {:knowledge-point/question-generator [*]}]'
groups = [['questions', QUESTION_PULL, newq], ['entities', '[*]', newe], ['parents', pattern, kids]]
w = H/sys.argv[2]
w.mkdir(exist_ok=True)
(w/'native-pulls.edn').write_text(dumps(groups)+'\n')
p = Publisher.from_environment(source=':agent/codex')
result = subprocess.run([str(ROOT/'reference/mathacademy/repairs/2026-10-17-import-source-bulk/native_read'),
    str(w), '14371'], env=p.client.environment, capture_output=True, text=True, timeout=300)
(w/'read.log').write_text(result.stdout+result.stderr)
result.check_returncode()
for name,_,_ in groups:
    values = jsonable(loads((w/(name+'.edn')).read_text()))
    (w/(name+'.json')).write_text(json.dumps(values, indent=2, ensure_ascii=False)+'\n')
    current = {r[':db/id']: r for r in json.loads((H/'capture'/(name+'.json')).read_text())}
    for row in values:
        if row[':db/id'] in current:
            assert current[row[':db/id']] == row
        current[row[':db/id']] = row
    (H/'capture'/(name+'.json')).write_text(json.dumps(list(current.values()), indent=2, ensure_ascii=False)+'\n')
fields = json.loads((H/'snapshot-fields.json').read_text())
for line in gzip.open(a/'snapshot.jsonl.gz', 'rt'):
    row = json.loads(line)
    if row['e'] in eids and row['a'] in {'question/problem', 'question/worked-solution', 'tutorial/content', 'answer/value'}:
        fields[f"{row['e']}/{row['a']}"] = row['raw_string']
(H/'snapshot-fields.json').write_text(json.dumps(fields, indent=2, ensure_ascii=False)+'\n')
print(result.stdout)
questions = json.loads((w/'questions.json').read_text())
missing = [{'entity': q[':db/id'], 'keys': [f[':answer-field/key'] for f in q.get(':question/answer-fields', []) if ':answer-field/correct' not in f]}
           for q in questions if any(':answer-field/correct' not in f for f in q.get(':question/answer-fields', []))]
(w/'incomplete.json').write_text(json.dumps(missing, indent=2)+'\n')
print('Missing keys:', json.dumps(missing))
